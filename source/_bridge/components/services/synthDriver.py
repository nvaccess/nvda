# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import (
	Callable,
	Any,
	TypeAlias,
)
import json
import rpyc
from logHandler import log
import config
from synthDriverHandler import (
	SynthDriver,
	synthIndexReached,
	synthDoneSpeaking,
)
from speech.commands import (
	IndexCommand,
	CharacterModeCommand,
	LangChangeCommand,
	BreakCommand,
	BaseProsodyCommand,
	PitchCommand,
	RateCommand,
	VolumeCommand,
	PhonemeCommand,
)
from _bridge.base import Service


@rpyc.service
class SynthDriverService(Service):
	"""
	Wraps a SynthDriver instance, exposing wire-safe methods for remote usage.
	When accessed remotely, this service must be wrapped in a `_bridge.components.proxies.synthDriver.SynthDriverProxy` which will handle any deserialization and provide the same interface as a local SynthDriver.
	Arguments and return types on the methods here are an internal detail and not thoroughly documented, as they should not be used directly.
	:ivar _synth: The SynthDriver instance being wrapped.
	"""

	_synth: SynthDriver

	def __init__(self, synthDriver: SynthDriver):
		super().__init__()
		self._synth = synthDriver
		self._synthIndexReachedCallback = None
		self._synthDoneSpeakingCallback = None
		# Ensure default pitch, rate, and volume settings exist in config
		speechConf = config.conf['speech']
		if self._synth.name not in speechConf:
			synthConf = speechConf[self._synth.name] = {}
		else:
			synthConf = speechConf[self.name]
		if 'pitch' not in synthConf:
			synthConf['pitch'] = self._synth.pitch
		if 'rate' not in synthConf:
			synthConf['rate'] = self._synth.rate
		if 'volume' not in synthConf:
			synthConf['volume'] = self._synth.volume

	@Service.exposed
	def registerSynthIndexReachedNotification(self, callback: Callable[[int], Any]):
		def localCallback_synthIndexReached(synth: SynthDriver, index: int):
			log.debug(f"synthIndexReached localCallback called with index {index}")
			if synth is self._synth:
				callback(index)

		self._synthIndexReachedCallback = localCallback_synthIndexReached
		synthIndexReached.register(localCallback_synthIndexReached)

	@Service.exposed
	def registerSynthDoneSpeakingNotification(self, callback: Callable[[], Any]):
		def localCallback_synthDoneSpeaking(synth: SynthDriver):
			log.debug(f"synthDoneSpeaking localCallback called with synth {synth}")
			if synth is self._synth:
				callback()

		self._synthDoneSpeakingCallback = localCallback_synthDoneSpeaking
		synthDoneSpeaking.register(localCallback_synthDoneSpeaking)

	_SerializedSettingKV: TypeAlias = tuple[str, Any]
	_SerializedSettingData: TypeAlias = tuple[str, tuple[_SerializedSettingKV, ...]]
	_SerializedSupportedSettings: TypeAlias = tuple[_SerializedSettingData, ...]

	@Service.exposed
	def getSupportedSettings(self) -> _SerializedSupportedSettings:
		return tuple(
			(
				setting.__class__.__name__,
				tuple((k, v) for k, v in setting.__dict__.items() if not k.startswith("_")),
			)
			for setting in self._synth.supportedSettings
		)

	@Service.exposed
	def getSupportedCommands(self) -> frozenset[str]:
		commands: list[str] = []
		for item in self._synth.supportedCommands:
			if issubclass(item, (IndexCommand, CharacterModeCommand, LangChangeCommand, BreakCommand, PitchCommand, RateCommand, VolumeCommand, PhonemeCommand)):
				name = item.__name__
			else:
				log.debugWarning(f"Unknown command type in supportedCommands: {item}")
				continue
			commands.append(name)
		return frozenset(commands)


	@Service.exposed
	def getSupportedNotifications(self) -> frozenset[str]:
		notifications = []
		for item in self._synth.supportedNotifications:
			if item is synthIndexReached:
				notifications.append("synthIndexReached")
			elif item is synthDoneSpeaking:
				notifications.append("synthDoneSpeaking")
			else:
				raise ValueError("Unknown notification")
		return frozenset(notifications)

	@Service.exposed
	def getAvailableVoices(self) -> tuple[tuple[str, str, str], ...]:
		return tuple((v.id, v.displayName, v.language) for v in self._synth._getAvailableVoices().values())

	@Service.exposed
	def getAvailableVariants(self) -> tuple[tuple[str, str], ...]:
		return tuple((v.id, v.displayName) for v in self._synth._getAvailableVariants().values())

	@Service.exposed
	def speak(self, data: str):
		data = json.loads(data)
		log.debug(f"Received speak request with data: {data}")
		speechSequence = []
		for item in data:
			if item["type"] == "str":
				speechSequence.append(item["value"])
			elif item["type"] == "IndexCommand":
				speechSequence.append(
					IndexCommand(index=item["index"])
				)
			elif item["type"] == "CharacterModeCommand":
				speechSequence.append(
					CharacterModeCommand(state=item["state"])
				)
			elif item["type"] == "LangChangeCommand":
				speechSequence.append(
					LangChangeCommand(lang=item["lang"])
				)
			elif item["type"] == "BreakCommand":
				speechSequence.append(
					BreakCommand(time=item["time"])
				)
			elif item["type"] in (
				"PitchCommand",
				"RateCommand",
				"VolumeCommand",
			):
				cls = globals()[item["type"]]
				log.debug(f"Reconstructing {cls}, with data {item}")
				speechSequence.append(
					cls(
						offset=item["offset"],
						multiplier=item["multiplier"],
					)
				)
			elif item["type"] == "PhonemeCommand":
				speechSequence.append(
					PhonemeCommand(
						ipa=item["ipa"],
						text=item["text"],
					)
				)
			else:
				log.debugWarning(f"Unsupported speech sequence item type: {item['type']}")
				continue
		return self._synth.speak(speechSequence)

	@Service.exposed
	def cancel(self):
		self._synth.cancel()

	@Service.exposed
	def pause(self, switch: bool):
		self._synth.pause(switch)

	@Service.exposed
	def getParam(self, param: str) -> Any:
		if not any(param == setting.id for setting in self._synth.supportedSettings):
			raise AttributeError(f"{param} not a supported setting")
		return getattr(self._synth, param)

	@Service.exposed
	def setParam(self, param: str, val: Any):
		if not any(param == setting.id for setting in self._synth.supportedSettings):
			raise AttributeError(f"{param} not a supported setting")
		setattr(self._synth, param, val)
		# Update local config
		# So synthCommands can use current defaults.
		synthConf = config.conf['speech'][self._synth.name]
		synthConf[param] = val

	def terminate(self):
		if self._synthIndexReachedCallback:
			log.debug(
				f"Unregistering synthIndexReached callback for {self._synth.name} of SynthDriverService",
			)
			synthIndexReached.unregister(self._synthIndexReachedCallback)
			self._synthIndexReachedCallback = None
		if self._synthDoneSpeakingCallback:
			log.debug(
				f"Unregistering synthDoneSpeaking callback for {self._synth.name} of SynthDriverService",
			)
			synthDoneSpeaking.unregister(self._synthDoneSpeakingCallback)
			self._synthDoneSpeakingCallback = None
		log.debug(f"Terminating SynthDriver instance {self._synth.name} of SynthDriverService")
		self._synth.terminate()
		del self._synth
		super().terminate()
