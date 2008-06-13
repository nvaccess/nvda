import baseObject
import synthDriverHandler
import config
import itertools

class SynthSetting(baseObject.AutoPropertyObject):
	""" a synth setting. Has functions to set, get, increase and decrease its value """
	def __init__(self,name,min=0,max=100,step=1):
		self.name=name
		self.min=min
		self.max=max
		self.step = step

	def increase(self):
		val = min(self.max,self.value+self.step)
		self.value = val
		return self._getReportValue(val)

	def decrease(self):
		val = max(self.min,self.value-self.step)
		self.value = val
		return self._getReportValue(val)

	def _get_value(self):
		return getattr(synthDriverHandler.getSynth(),self.name)

	def _set_value(self,value):
		setattr(synthDriverHandler.getSynth(),self.name,value)
		config.conf["speech"][synthDriverHandler.getSynth().name][self.name]=value

	def _getReportValue(self, val):
		return str(val)

	def _get_reportValue(self):
		return self._getReportValue(self.value)

class VoiceSynthSetting(SynthSetting):

	def __init__(self):
		super(VoiceSynthSetting,self).__init__("voice",1,synthDriverHandler.getSynth().voiceCount)

	def _set_value(self,value):
		"""overrided to use code that supports updating speech dicts when changing voice"""
		synthDriverHandler.changeVoice(synthDriverHandler.getSynth(),value)
		config.conf["speech"][synthDriverHandler.getSynth().name][self.name]=value

	def _getReportValue(self, val):
		return synthDriverHandler.getSynth().getVoiceName(val)

class VariantSynthSetting(SynthSetting):

	def __init__(self):
		super(VariantSynthSetting,self).__init__("variant",0,synthDriverHandler.getSynth().variantCount-1)

	def _get_value(self):
		currentVariant=synthDriverHandler.getSynth().variant
		for x in range(0,synthDriverHandler.getSynth().variantCount):
			if currentVariant==synthDriverHandler.getSynth().getVariantIdentifier(x):
				break
		return x

	def _set_value(self,value):
		synthDriverHandler.getSynth().variant=synthDriverHandler.getSynth().getVariantIdentifier(value)

	def _getReportValue(self, val):
		return synthDriverHandler.getSynth().getVariantName(val)

class SynthSettingsRing(baseObject.AutoPropertyObject):
	"""
	 A synth settings ring which enables the user to change to the next and previous settings and ajust the selected one
	It was written to facilitate the implementation of a way to change the settings resembling the window-eyes way.
	"""

	#dictionary with each attribute name translated so the settings name is returned 
	#in the users language
	_I18nAttributeNames = {"volume": _("volume"),
	"rate": _("rate"),
	"pitch": _("pitch"),
	"inflection": _("inflection"),
	"voice": _("voice"),
	"variant": _("variant")}

	def __init__(self):
		self.updateSupportedSettings()

	def _get_currentSettingName(self):
		""" returns the current setting's name """
		if self._current is not None:
			return SynthSettingsRing._I18nAttributeNames[self.settings[self._current].name]
		return None

	def _get_currentSettingValue(self):
		return self.settings[self._current].reportValue

	def _set_currentSettingValue(self,value):
		if self._current is not None: 
			self.settings[_current].value = val

	def next(self):
		""" changes to the next setting and returns its name """
		if self._current is not None:
			self._current = (self._current + 1) % len(self.settings)
			return self.currentSettingName
		return None

	def previous(self):
		if self._current is not None:
			self._current = (self._current - 1) % len(self.settings)
			return self.currentSettingName
		return None

	def increase(self):
		""" increases the currentSetting and returns its new value """
		if self._current is not None: 
			return self.settings[self._current].increase()
		return None

	def decrease(self):
		""" decreases the currentSetting and returns its new value """
		if self._current is not None:
			return self.settings[self._current].decrease()
		return None

	def updateSupportedSettings(self):
		list = []
		synth = synthDriverHandler.getSynth()
		if synth.hasVolume: list.append(SynthSetting("volume", step=max(synth.volumeMinStep, 10)))
		if synth.hasRate: list.append(SynthSetting("rate",step=max(synth.rateMinStep, 5)))
		if synth.hasPitch: list.append(SynthSetting("pitch", step=max(synth.pitchMinStep, 5)))
		if synth.hasInflection: list.append(SynthSetting("inflection",step = max(synth.inflectionMinStep, 5)))
		if synth.hasVoice: list.append(VoiceSynthSetting())
		if synth.hasVariant: list.append(VariantSynthSetting())
		if len(list) == 0:
			self._current = None
			self.settings = None
		else:
			self.settings = list
			self._current = 0
