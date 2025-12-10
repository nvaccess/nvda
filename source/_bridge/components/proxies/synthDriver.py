# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import typing
from collections import OrderedDict
import pickle
from logHandler import log
import synthDriverHandler
from autoSettingsUtils.driverSetting import DriverSetting, NumericDriverSetting, BooleanDriverSetting
from synthDriverHandler import (
	synthIndexReached,
	synthDoneSpeaking,
	VoiceInfo,
)
if typing.TYPE_CHECKING:
	from ..services.synthDriver import SynthDriverService


class SynthDriverProxy(synthDriverHandler.SynthDriver):
	""" Wraps a remote SynthDriverService, providing the same interface as a local SynthDriver. """
	_synthDriverService: SynthDriverService

	def __init__(self, synthDriverService:  SynthDriverService):
		super().__init__()
		self._synthDriverService = synthDriverService
		for notification in self.supportedNotifications:
			if notification is synthIndexReached:
				log.info("Registering synthIndexReached notification with synth driver service")
				def localCallback_synthIndexReached(index):
					synthIndexReached.notify(synth=self, index=index)
				self._synthDriverService.registerSynthIndexReachedNotification(localCallback_synthIndexReached)
			elif notification is synthDoneSpeaking:
				log.info("Registering synthDoneSpeaking notification with synth driver service")
				def localCallback_synthDoneSpeaking():
					synthDoneSpeaking.notify(synth=self)
				self._synthDriverService.registerSynthDoneSpeakingNotification(localCallback_synthDoneSpeaking)

	_supportedSettingsCache = None
	def _get_supportedSettings(self):
		if self._supportedSettingsCache is not None:
			return self._supportedSettingsCache
		data = self._synthDriverService.getSupportedSettings()
		settings = []
		for item in data:
			clsName, params = item
			params = {k: v for k, v in params}
			if clsName == 'DriverSetting':
				setting = DriverSetting(**params)
			elif clsName == 'NumericDriverSetting':
				setting = NumericDriverSetting(**params)
			elif clsName == 'BooleanDriverSetting':
				setting = BooleanDriverSetting(**params)
			else:
				raise ValueError(f"Unknown setting class name: {clsName}")
			settings.append(setting)
		self._supportedSettingsCache = settings
		return settings

	_supportedNotificationsCache = None
	def _get_supportedNotifications(self):
		if self._supportedNotificationsCache is not None:
			return self._supportedNotificationsCache
		data = self._synthDriverService.getSupportedNotifications()
		notifications = set()
		for item in data:
			if item == 'synthIndexReached':
				notifications.add(synthIndexReached)
			elif item == 'synthDoneSpeaking':
				notifications.add(synthDoneSpeaking)
			else:
				raise ValueError(f"Unknown notification: {item}")
		self._supportedNotificationsCache = notifications
		return notifications

	def _getAvailableVoices(self):
		data = self._synthDriverService.getAvailableVoices()
		voices = OrderedDict()
		for ID, name, language in data:
			voices[ID] = VoiceInfo(ID, name, language)
		return voices

	def _getAvailableVariants(self):
		data = self._synthDriverService.getAvailableVariants()
		variants = OrderedDict()
		for ID, name in data:
			variants[ID] = VoiceInfo(ID, name, None)
		return variants

	def speak(self, speechSequence):
		data = pickle.dumps(speechSequence)
		return self._synthDriverService.speak(data)

	def cancel(self):
		return self._synthDriverService.cancel()

	def pause(self, switch: bool):
		return self._synthDriverService.pause(switch)

	def _get_voice(self):
		return self._synthDriverService.getParam('voice')

	def _set_voice(self, value):
			self._synthDriverService.setParam('voice', value)
			# changing the voice may change the supported settings
			self._supportedSettingsCache = None

	def _get_rate(self):
		return self._synthDriverService.getParam('rate')

	def _set_rate(self, value):
		self._synthDriverService.setParam('rate', value)

	def _get_pitch(self):
		return self._synthDriverService.getParam('pitch')

	def _set_pitch(self, value):
		self._synthDriverService.setParam('pitch', value)

	def _get_volume(self):
		return self._synthDriverService.getParam('volume')

	def _set_volume(self, value):
		self._synthDriverService.setParam('volume', value)

	def _get_variant(self):
		return self._synthDriverService.getParam('variant')

	def _set_variant(self, value):
		self._synthDriverService.setParam('variant', value)
