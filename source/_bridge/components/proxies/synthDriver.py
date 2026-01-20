# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import weakref
import typing
from collections import OrderedDict
import pickle
from logHandler import log
from _bridge.base import Proxy
from autoSettingsUtils.driverSetting import DriverSetting, NumericDriverSetting, BooleanDriverSetting
from synthDriverHandler import (
	SynthDriver,
	synthIndexReached,
	synthDoneSpeaking,
	VoiceInfo,
)

if typing.TYPE_CHECKING:
	import extensionPoints
	from ..services.synthDriver import SynthDriverService
	from _bridge.base import Proxy


class SynthDriverProxy(Proxy, SynthDriver):
	"""Wraps a remote SynthDriverService, providing the same interface as a local SynthDriver."""

	def __init__(self, service: SynthDriverService):
		log.debug(f"Creating SynthDriverProxy instance for remote synth driver '{self.name}'")
		super().__init__(service)
		selfRef = weakref.ref(self)
		for notification in self.supportedNotifications:
			if notification is synthIndexReached:
				log.debug("Registering synthIndexReached notification with synth driver service")

				def localCallback_synthIndexReached(index: int):
					synth = selfRef()
					if synth is not None:
						synthIndexReached.notify(synth=synth, index=index)

				self._remoteService.registerSynthIndexReachedNotification(localCallback_synthIndexReached)
			elif notification is synthDoneSpeaking:
				log.debug("Registering synthDoneSpeaking notification with synth driver service")

				def localCallback_synthDoneSpeaking():
					synth = selfRef()
					if synth is not None:
						synthDoneSpeaking.notify(synth=synth)

				self._remoteService.registerSynthDoneSpeakingNotification(localCallback_synthDoneSpeaking)

	_supportedSettingsCache: list[DriverSetting] | None  = None

	def _get_supportedSettings(self) -> list[DriverSetting]:
		if self._supportedSettingsCache is not None:
			return self._supportedSettingsCache
		data = self._remoteService.getSupportedSettings()
		settings = []
		for item in data:
			clsName, params = item
			params = {k: v for k, v in params}
			if clsName == "DriverSetting":
				setting = DriverSetting(**params)
			elif clsName == "NumericDriverSetting":
				setting = NumericDriverSetting(**params)
			elif clsName == "BooleanDriverSetting":
				setting = BooleanDriverSetting(**params)
			else:
				raise ValueError(f"Unknown setting class name: {clsName}")
			settings.append(setting)
		self._supportedSettingsCache = settings
		return settings

	_supportedNotificationsCache: set[extensionPoints.Action] | None = None

	def _get_supportedNotifications(self) -> set[extensionPoints.Action]:
		if self._supportedNotificationsCache is not None:
			return self._supportedNotificationsCache
		data = self._remoteService.getSupportedNotifications()
		notifications = set()
		for item in data:
			if item == "synthIndexReached":
				notifications.add(synthIndexReached)
			elif item == "synthDoneSpeaking":
				notifications.add(synthDoneSpeaking)
			else:
				raise ValueError(f"Unknown notification: {item}")
		self._supportedNotificationsCache = notifications
		return notifications

	def _getAvailableVoices(self):
		data = self._remoteService.getAvailableVoices()
		voices = OrderedDict()
		for ID, name, language in data:
			voices[ID] = VoiceInfo(ID, name, language)
		return voices

	def _getAvailableVariants(self):
		data = self._remoteService.getAvailableVariants()
		variants = OrderedDict()
		for ID, name in data:
			variants[ID] = VoiceInfo(ID, name, None)
		return variants

	def speak(self, speechSequence):
		# Pickle should be replaced with a much safer serialization method in future.
		# But as only internal synth drivers are supported currently, this is acceptable for now.
		data = pickle.dumps(speechSequence)
		return self._remoteService.speak(data)

	def cancel(self):
		return self._remoteService.cancel()

	def pause(self, switch: bool):
		return self._remoteService.pause(switch)

	def _get_voice(self):
		return self._remoteService.getParam("voice")

	def _set_voice(self, value):
		self._remoteService.setParam("voice", value)
		# changing the voice may change the supported settings
		self._supportedSettingsCache = None

	def _get_rate(self):
		return self._remoteService.getParam("rate")

	def _set_rate(self, value):
		self._remoteService.setParam("rate", value)

	def _get_pitch(self):
		return self._remoteService.getParam("pitch")

	def _set_pitch(self, value):
		self._remoteService.setParam("pitch", value)

	def _get_volume(self):
		return self._remoteService.getParam("volume")

	def _set_volume(self, value):
		self._remoteService.setParam("volume", value)

	def _get_variant(self):
		return self._remoteService.getParam("variant")

	def _set_variant(self, value):
		self._remoteService.setParam("variant", value)
