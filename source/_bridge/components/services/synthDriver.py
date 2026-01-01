# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import typing
import pickle
import rpyc
from logHandler import log
from synthDriverHandler import (
	SynthDriver,
	synthIndexReached,
	synthDoneSpeaking,
)
from _bridge.base import Service, Connection

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

	@Service.exposed
	def registerSynthIndexReachedNotification(self, callback: typing.Callable[[int], typing.Any]):
		def localCallback_synthIndexReached(synth, index):
			log.debug(f"synthIndexReached localCallback called with index {index}")
			if synth is self._synth:
				callback(index)
		self._synthIndexReachedCallback = localCallback_synthIndexReached
		synthIndexReached.register(localCallback_synthIndexReached)

	@Service.exposed
	def registerSynthDoneSpeakingNotification(self, callback: typing.Callable[[], typing.Any]):
		def localCallback_synthDoneSpeaking(synth):
			log.debug(f"synthDoneSpeaking localCallback called with synth {synth}")
			if synth is self._synth:
				callback()
		self._synthDoneSpeakingCallback = localCallback_synthDoneSpeaking
		synthDoneSpeaking.register(localCallback_synthDoneSpeaking)

	@Service.exposed
	def getSupportedSettings(self) -> tuple:
		return tuple((setting.__class__.__name__, tuple((k, v) for k, v in setting.__dict__.items() if not k.startswith('_'))) for setting in self._synth.supportedSettings)

	@Service.exposed
	def getSupportedNotifications(self) -> frozenset[str]:
		notifications = []
		for item in self._synth.supportedNotifications:
			if item is synthIndexReached:
				notifications.append('synthIndexReached')
			elif item is synthDoneSpeaking:
				notifications.append('synthDoneSpeaking')
			else:
				raise ValueError("Unknown notification")
		return frozenset(notifications)

	@Service.exposed
	def getAvailableVoices(self):
		return tuple(
			(v.id, v.displayName, v.language)
			for v in self._synth._getAvailableVoices().values()
		)

	@Service.exposed
	def getAvailableVariants(self):
		return tuple(
			(v.id, v.displayName)
			for v in self._synth._getAvailableVariants().values()
		)

	@Service.exposed
	def speak(self, data):
		# fixme: replace Pickle with a safer serialization method
		speechSequence = pickle.loads(data)
		return self._synth.speak(speechSequence)

	@Service.exposed
	def cancel(self):
		return self._synth.cancel()

	@Service.exposed
	def pause(self, switch: bool):
		return self._synth.pause(switch)

	@Service.exposed
	def getParam(self, param):
		if not any(param == setting.id for setting in self._synth.supportedSettings):
			raise AttributeError(f"{param} not a supported setting")
		return getattr(self._synth, param)

	@Service.exposed
	def setParam(self, param, val):
		if not any(param == setting.id for setting in self._synth.supportedSettings):
			raise AttributeError(f"{param} not a supported setting")
		setattr(self._synth, param, val)

	def terminate(self):
		if self._synthIndexReachedCallback:
			log.debug(f"Unregistering synthIndexReached callback for {self._synth.name} of SynthDriverService")
			synthIndexReached.unregister(self._synthIndexReachedCallback)
			self._synthIndexReachedCallback = None
		if self._synthDoneSpeakingCallback:
			log.debug(f"Unregistering synthDoneSpeaking callback for {self._synth.name} of SynthDriverService")
			synthDoneSpeaking.unregister(self._synthDoneSpeakingCallback)
			self._synthDoneSpeakingCallback = None
		log.debug(f"Terminating SynthDriver instance {self._synth.name} of SynthDriverService")
		self._synth.terminate()
		del self._synth
		super().terminate()
