import baseObject
import config
import synthDriverHandler
import queueHandler
from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting


class SynthSetting(baseObject.AutoPropertyObject):
	"""a numeric synth setting. Has functions to set, get, increase and decrease its value """
	def __init__(self,synth,setting,min=0,max=100):
		self.synth = synth
		self.setting = setting
		self.min = setting.minVal if isinstance(setting, NumericDriverSetting) else min
		self.max = setting.maxVal if isinstance(setting, NumericDriverSetting) else max
		self.step = setting.normalStep if isinstance(setting, NumericDriverSetting) else 1

	def increase(self):
		val = min(self.max,self.value+self.step)
		self.value = val
		return self._getReportValue(val)

	def decrease(self):
		val = max(self.min,self.value-self.step)
		self.value = val
		return self._getReportValue(val)

	def _get_value(self):
		return getattr(self.synth,self.setting.id)

	def _set_value(self,value):
		setattr(self.synth,self.setting.id, value)
		config.conf["speech"][self.synth.name][self.setting.id]=value

	def _getReportValue(self, val):
		return str(val)

	def _get_reportValue(self):
		return self._getReportValue(self.value)

class StringSynthSetting(SynthSetting):
	def __init__(self,synth,setting):
		self._values=list(getattr(synth,"available%ss"%setting.id.capitalize()).values())
		super(StringSynthSetting,self).__init__(synth,setting,0,len(self._values)-1)

	def _get_value(self):
		curID=getattr(self.synth,self.setting.id)
		for e,v in enumerate(self._values):
			if curID==v.id:
				return e 

	def _set_value(self,value):
		"""Overridden to use code that supports updating speech dicts when changing voice"""
		id = self._values[value].id
		if self.setting.id == "voice":
			synthDriverHandler.changeVoice(self.synth, id)
			# Voice parameters may change when the voice changes, so update the config.
			self.synth.saveSettings()
		else:
			super(StringSynthSetting,self)._set_value(id)

	def _getReportValue(self, val):
		return self._values[val].displayName

class BooleanSynthSetting(SynthSetting):

	def __init__(self, synth, setting):
		super(BooleanSynthSetting, self).__init__(synth, setting, 0, 1)

	def _get_value(self):
		return int(super(BooleanSynthSetting, self).value)

	def _set_value(self, val):
		super(BooleanSynthSetting, self)._set_value(bool(val))

	def _getReportValue(self, val):
		return _("on") if val else _("off")

class SynthSettingsRing(baseObject.AutoPropertyObject):
	"""
	A synth settings ring which enables the user to change to the next and previous settings and ajust the selected one
	It was written to facilitate the implementation of a way to change the settings resembling the window-eyes way.
	"""

	def __init__(self,synth):
		try:
			self._current = synth.initialSettingsRingSetting
		except ValueError:
			self._current=None
		self.updateSupportedSettings(synth)

	def _get_currentSettingName(self):
		""" returns the current setting's name """
		if self._current is not None and hasattr(self,'settings'):
			return self.settings[self._current].setting.displayName
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
		#Save ID of the current setting to restore ring position after reconstruction
		prevID = (
			self.settings[self._current].setting.id
			if self._current is not None and hasattr(self,'settings')
			else None
		)
		list = []
		for s in synth.supportedSettings:
			if not s.availableInSettingsRing: continue
			if prevID == s.id: #restore the last setting
				self._current=len(list)
			if isinstance(s, NumericDriverSetting):
				cls=SynthSetting
			elif isinstance(s, BooleanDriverSetting):
				cls=BooleanSynthSetting
			else:
				cls=StringSynthSetting
			list.append(cls(synth,s))
		if len(list) == 0:
			self._current = None
			self.settings = None
		else:
			self.settings = list
		if (
			not prevID
			or not self.settings
			or len(self.settings) <= self._current
			or prevID != self.settings[self._current].setting.id
		):
			# Previous chosen setting doesn't exists. Set position to default
			self._current = synth.initialSettingsRingSetting
			if _isScriptRunning:
				# User changed some setting from ring and that setting no longer exists.
				# We have just reverted to first setting, so report this change to user
				queueHandler.queueFunction(
					queueHandler.eventQueue,
					ui.message,"%s %s" % (self.currentSettingName,self.currentSettingValue)
				)
