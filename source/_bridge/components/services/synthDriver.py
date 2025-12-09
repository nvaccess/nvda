import pickle
import importlib
import rpyc
from logHandler import log
from autoSettingsUtils.driverSetting import (
	DriverSetting,
	NumericDriverSetting,
	BooleanDriverSetting,
)
from synthDriverHandler import (
	synthIndexReached,
	synthDoneSpeaking,
)


class SynthDriverService(rpyc.Service):

	def __init__(self, name):
		mod = importlib.import_module(f'synthDrivers.{name}')
		self._synth = mod.SynthDriver()

	def exposed_registerNotification(self, name, callback):
		if name == 'synthIndexReached':
			log.debug("Registering synthIndexReached notification")
			def localCallback_synthIndexReached(synth, index):
				log.debug(f"synthIndexReached localCallback called with index {index}")
				if synth is self._synth:
					callback(index)
			self._synthIndexReachedCallback = localCallback_synthIndexReached
			synthIndexReached.register(localCallback_synthIndexReached)
		elif name == 'synthDoneSpeaking':
			log.debug("Registering synthDoneSpeaking notification")
			def localCallback_synthDoneSpeaking(synth):
				log.debug(f"synthDoneSpeaking localCallback called with synth {synth}")
				if synth is self._synth:
					callback()
			self._synthDoneSpeakingCallback = localCallback_synthDoneSpeaking
			synthDoneSpeaking.register(localCallback_synthDoneSpeaking)

	def exposed_getSupportedSettings(self):
		return tuple((setting.__class__.__name__, tuple((k, v) for k, v in setting.__dict__.items() if not k.startswith('_'))) for setting in self._synth.supportedSettings)

	def exposed_getSupportedNotifications(self):
		notifications = []
		for item in self._synth.supportedNotifications:
			if item is synthIndexReached:
				notifications.append('synthIndexReached')
			elif item is synthDoneSpeaking:
				notifications.append('synthDoneSpeaking')
			else:
				raise ValueError("Unknown notification")
		return frozenset(notifications)

	def exposed_getAvailableVoices(self):
		return tuple(
			(v.id, v.displayName, v.language)
			for v in self._synth._getAvailableVoices().values()
		)

	def exposed_getAvailableVariants(self):
		return tuple(
			(v.id, v.displayName)
			for v in self._synth._getAvailableVariants().values()
		)

	def exposed_speak(self, data):
		speechSequence = pickle.loads(data)
		return self._synth.speak(speechSequence)

	def exposed_cancel(self):
		return self._synth.cancel()

	def exposed_pause(self, switch: bool):
		return self._synth.pause(switch)

	def exposed_getParam(self, param):
		if not any(param == setting.id for setting in self._synth.supportedSettings):
			raise AttributeError(f"{param} not a supported setting")
		return getattr(self._synth, param)

	def exposed_setParam(self, param, val):
		if not any(param == setting.id for setting in self._synth.supportedSettings):
			raise AttributeError(f"{param} not a supported setting")
		setattr(self._synth, param, val)
