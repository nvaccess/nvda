import baseObject
import config
import synthDriverHandler
import queueHandler
import driverHandler

class DriverSetting(baseObject.AutoPropertyObject):
	"""a numeric driver setting. Has functions to set, get, increase and decrease its value """
	def __init__(self,driver,setting,min=0,max=100):
		self.driver = driver
		self.setting = setting
		self.min = setting.minVal  if isinstance(setting,driverHandler.NumericDriverSetting) else min
		self.max = setting.maxVal  if isinstance(setting,driverHandler.NumericDriverSetting) else max
		self.step = setting.normalStep if isinstance(setting,driverHandler.NumericDriverSetting) else 1

	def increase(self):
		val = min(self.max,self.value+self.step)
		self.value = val
		return self._getReportValue(val)

	def decrease(self):
		val = max(self.min,self.value-self.step)
		self.value = val
		return self._getReportValue(val)

	def _get_value(self):
		return getattr(self.driver,self.setting.name)

	def _set_value(self,value):
		setattr(self.driver,self.setting.name,value)
		config.conf[self.driver.configSection][self.driver.name][self.setting.name]=value

	def _getReportValue(self, val):
		return str(val)

	def _get_reportValue(self):
		return self._getReportValue(self.value)

class StringDriverSetting(DriverSetting):
	def __init__(self,driver,setting):
		self._values=getattr(driver,"available%ss"%setting.name.capitalize()).values()
		super(StringDriverSetting,self).__init__(driver,setting,0,len(self._values)-1)

	def _get_value(self):
		curID=getattr(self.driver,self.setting.name)
		for e,v in enumerate(self._values):
			if curID==v.ID:
				return e 

	def _set_value(self,value):
		"""Overridden to use code that supports updating speech dicts when changing voice"""
		ID=self._values[value].ID
		if isinstance(self.driver, synthDriverHandler.SynthDriver) and self.setting.name=="voice":
			synthDriverHandler.changeVoice(self.driver,ID)
			# Voice parameters may change when the voice changes, so update the config.
			self.driver.saveSettings()
		else:
			super(StringDriverSetting,self)._set_value(ID)

	def _getReportValue(self, val):
		return self._values[val].name

class BooleanDriverSetting(DriverSetting):

	def __init__(self, driver, setting):
		super(BooleanDriverSetting, self).__init__(driver, setting, 0, 1)

	def _get_value(self):
		return int(super(BooleanDriverSetting, self).value)

	def _set_value(self, val):
		super(BooleanDriverSetting, self)._set_value(bool(val))

	def _getReportValue(self, val):
		return _("on") if val else _("off")

class SettingsRing(baseObject.AutoPropertyObject):
	"""
	A settings ring which enables the user to change to the next and previous settings and adjust the selected one
	It was written to facilitate the implementation of a way to change the settings resembling the window-eyes way.
	"""

	def __init__(self,driver):
		try:
			self._current = driver.initialSettingsRingSetting
		except ValueError:
			self._current=None
		self.updateSupportedSettings(driver)

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

	def updateSupportedSettings(self,driver):
		import ui
		from scriptHandler import _isScriptRunning
		#Save name of the current setting to restore ring position after reconstruction
		prevName=self.settings[self._current].setting.name if self._current is not None and hasattr(self,'settings') else None
		list = []
		for s in driver.supportedSettings:
			if not s.availableInSettingsRing: continue
			if prevName==s.name: #restore the last setting
				self._current=len(list)
			if isinstance(s,driverHandler.NumericDriverSetting):
				cls=DriverSetting
			elif isinstance(s,driverHandler.BooleanDriverSetting):
				cls=BooleanDriverSetting
			else:
				cls=StringDriverSetting
			list.append(cls(driver,s))
		if len(list) == 0:
			self._current = None
			self.settings = None
		else:
			self.settings = list
		if not prevName or not self.settings or len(self.settings)<=self._current or prevName!=self.settings[self._current].setting.name:
			#Previous chosen setting doesn't exists. Set position to default
			self._current = driver.initialSettingsRingSetting
			if _isScriptRunning:
				#User changed some setting from ring and that setting no more exists. We have just reverted to first setting, so report this change to user
				queueHandler.queueFunction(queueHandler.eventQueue,ui.message,"%s %s" % (self.currentSettingName,self.currentSettingValue))
