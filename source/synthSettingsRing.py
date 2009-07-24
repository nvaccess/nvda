import baseObject
import config
import synthDriverHandler

class SynthSetting(baseObject.AutoPropertyObject):
	""" a synth setting. Has functions to set, get, increase and decrease its value """
	def __init__(self,synth,setting,min=0,max=100):
		self.synth=synth
		self.setting=setting
		self.min=min
		self.max=max
		self.step = setting.data if setting.isNumeric() else 1

	def increase(self):
		val = min(self.max,self.value+self.step)
		self.value = val
		return self._getReportValue(val)

	def decrease(self):
		val = max(self.min,self.value-self.step)
		self.value = val
		return self._getReportValue(val)

	def _get_value(self):
		return getattr(self.synth,self.setting.name)

	def _set_value(self,value):
		setattr(self.synth,self.setting.name,value)
		config.conf["speech"][self.synth.name][self.setting.name]=value

	def _getReportValue(self, val):
		return str(val)

	def _get_reportValue(self):
		return self._getReportValue(self.value)

class StringSynthSetting(SynthSetting):

	def __init__(self,synth,setting):
		self._values=getattr(synth,"available%ss"%setting.name.capitalize())
		super(StringSynthSetting,self).__init__(synth,setting,0,len(self._values)-1)

	def _get_value(self):
		curID=getattr(self.synth,self.setting.name)
		for e,v in enumerate(self._values):
			if curID==v.ID:
				return e 

	def _set_value(self,value):
		"""Overridden to use code that supports updating speech dicts when changing voice"""
		ID=self._values[value].ID
		if self.setting.name=="voice":
			synthDriverHandler.changeVoice(self.synth,ID)
			# Voice parameters may change when the voice changes, so update the config.
			self.synth.saveSettings()
		else:
			setattr(self.synth,self.setting.name,ID)

	def _getReportValue(self, val):
		return self._values[val].name

class SynthSettingsRing(baseObject.AutoPropertyObject):
	"""
	 A synth settings ring which enables the user to change to the next and previous settings and ajust the selected one
	It was written to facilitate the implementation of a way to change the settings resembling the window-eyes way.
	"""

	def __init__(self,synth):
		self._current=0
		self.updateSupportedSettings(synth)

	def _get_currentSettingName(self):
		""" returns the current setting's name """
		if self._current is not None and hasattr(self,'settings'):
			return self.settings[self._current].setting.i18nName
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

	def updateSupportedSettings(self,synth):
		import ui
		from scriptHandler import _isScriptRunning
		prevName=self.settings[self._current].setting.name if hasattr(self,'settings') else None
		list = []
		for s in synth.supportedSettings:
			if not s.availableInSynthSettingsRing: continue
			index=0
			if prevName==s.name:
				index=len(list)
			p=SynthSetting if s.isNumeric() else StringSynthSetting
			list.append(p(synth,s))
		if len(list) == 0:
			self._current = None
			self.settings = None
		else:
			self.settings = list
			if index>=len(list):
				index = 0
			self._current = index
		if _isScriptRunning and prevName!=self.settings[self._current].setting.name:
			ui.message("%s %s" % (self.currentSettingName,self.currentSettingValue))
