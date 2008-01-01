import baseObject
import synthDriverHandler
import config
import itertools

class SynthSetting(baseObject.autoPropertyObject):
	""" a synth setting. Has functions to set, get, increase and decrease its value """
	def __init__(self,name,min=0,max=100,step=1):
		self.name=name
		self.min=min
		self.max=max
		self.step = step

	def increase(self):
		val = min(self.max,self.value+self.step)
		self.value = val
		return val

	def decrease(self):
		val = max(self.min,self.value-self.step)
		self.value = val
		return val

	def _get_value(self):
		return getattr(synthDriverHandler.getSynth(),self.name)

	def _set_value(self,value):
		setattr(synthDriverHandler.getSynth(),self.name,value)
		config.conf["speech"][synthDriverHandler.getSynth().name][self.name]=value

class VoiceSynthSetting(SynthSetting):

	def __init__(self):
		SynthSetting.__init__(self,"voice",1,synthDriverHandler.getSynth().voiceCount)

	def increase(self):
		SynthSetting.increase(self)
		return self.valueName		

	def decrease(self):
		SynthSetting.decrease(self)
		return self.valueName

	def _set_value(self,value):
		"""overrided to use code that supports updating user dicts when changing voice"""
		synthDriverHandler.changeVoice(synthDriverHandler.getSynth(),value)
		config.conf["speech"][synthDriverHandler.getSynth().name][self.name]=value
		
	def _get_valueName(self):
		return synthDriverHandler.getSynth().getVoiceName(self.value)

class SynthSettingsRing(baseObject.autoPropertyObject):
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
		if self.settings[self._current].name is not "voice":
			return self.settings[self._current].value
		else:
			return synthDriverHandler.getSynth().getVoiceName(self.settings[self._current].value)

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
		if synth.hasVolume: list.append(SynthSetting("volume", step=10))
		if synth.hasRate: list.append(SynthSetting("rate",step=5))
		if synth.hasPitch: list.append(SynthSetting("pitch", step=5))
		if synth.hasInflection: list.append(SynthSetting("inflection",step = 5))
		if synth.hasVoice: list.append(VoiceSynthSetting())
		if synth.hasVariant: list.append(SynthSetting("variant",0,synth.variantCount-1))
		if len(list) == 0:
			self._current = None
			self.settings = None
		else:
			self.settings = list
			self._current = 0
