import functools
import pickle
from logHandler import log
import synthDriverHandler
from autoSettingsUtils.driverSetting import DriverSetting, NumericDriverSetting, BooleanDriverSetting
from synthDriverHandler import (
	synthIndexReached,
	synthDoneSpeaking,
	VoiceInfo,
)


class SynthDriverProxy(synthDriverHandler.SynthDriver):
	_synthDriverService = None

	def __init__(self, synthDriverService):
		super().__init__()
		self._synthDriverService = synthDriverService
		for notification in self.supportedNotifications:
			if notification is synthIndexReached:
				log.info("Registering synthIndexReached notification with synth driver service")
				def localCallback(index):
					synthIndexReached.notify(synth=self, index=index)
				self._synthDriverService.registerNotification('synthIndexReached', localCallback)
			elif notification is synthDoneSpeaking:
				log.info("Registering synthDoneSpeaking notification with synth driver service")
				def localCallback():
					synthDoneSpeaking.notify(synth=self)
				self._synthDriverService.registerNotification('synthDoneSpeaking', localCallback)

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
		return {ID: VoiceInfo(ID, name, language) for ID, name, language in data}

	def _getAvailableVariants(self):
		data = self._synthDriverService.getAvailableVariants()
		return {ID: VoiceInfo(ID, name) for ID, name in data}

	def speak(self, speechSequence):
		data = pickle.dumps(speechSequence)
		return self._synthDriverService.speak(data)

	def cancel(self):
		return self._synthDriverService.cancel()

	def pause(self, switch: bool):
		return self._synthDriverService.pause(switch)

	def _get_voice(self):
		return self._synthDriverService.getParam('voice')

	def _set_voice(self, voice):
			self._synthDriverService.setParam('voice', voice)
			self._supportedSettingsCache = None

	def _get_rate(self):
		return self._synthDriverService.getParam('rate')

	def _set_rate(self, rate):
		self._synthDriverService.setParam('rate', rate)

	def _get_pitch(self):
		return self._synthDriverService.getParam('pitch')

	def _set_pitch(self, pitch):
		self._synthDriverService.setParam('pitch', pitch)

	def _get_volume(self):
		return self._synthDriverService.getParam('volume')

	def _set_volume(self, volume):
		self._synthDriverService.setParam('volume', volume)

	def _get_variant(self):
		return self._synthDriverService.getParam('variant')

	def _set_variant(self, variant):
		self._synthDriverService.setParam('variant', variant)
