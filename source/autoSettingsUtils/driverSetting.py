from baseObject import AutoPropertyObject


class DriverSetting(AutoPropertyObject):
	"""Represents a synthesizer or braille display setting such as voice, variant or dot firmness.
	"""

	def _get_configSpec(self):
		"""Returns the configuration specification of this particular setting for config file validator.
		@rtype: str
		"""
		return "string(default={defaultVal})".format(defaultVal=self.defaultVal)

	def __init__(self, id, displayNameWithAccelerator,
		availableInSettingsRing=False, defaultVal=None, displayName=None, useConfig=True):
		"""
		@param id: internal identifier of the setting
		@type id: str
		@param displayNameWithAccelerator: the localized string shown in voice or braille settings dialog
		@type displayNameWithAccelerator: str
		@param availableInSettingsRing: Will this option be available in a settings ring?
		@type availableInSettingsRing: bool
		@param defaultVal: Specifies the default value for a driver setting.
		@type param defaultVal: str or C{None}
		@param displayName: the localized string used in synth settings ring or None to use displayNameWithAccelerator
		@type displayName: str
		@param useConfig: Whether the value of this option is loaded from and saved to NVDA's configuration.
			Set this to C{False} if the driver deals with loading and saving.
		@type useConfig: bool
		"""
		self.id = id
		self.displayNameWithAccelerator = displayNameWithAccelerator
		if not displayName:
			# Strip accelerator from displayNameWithAccelerator.
			displayName = displayNameWithAccelerator.replace("&","")
		self.displayName = displayName
		self.availableInSettingsRing = availableInSettingsRing
		self.defaultVal = defaultVal
		self.useConfig = useConfig

class NumericDriverSetting(DriverSetting):
	"""Represents a numeric driver setting such as rate, volume, pitch or dot firmness."""

	def _get_configSpec(self):
		return "integer(default={defaultVal},min={minVal},max={maxVal})".format(
			defaultVal=self.defaultVal,minVal=self.minVal,maxVal=self.maxVal)

	def __init__(self, id, displayNameWithAccelerator, availableInSettingsRing=False,
		defaultVal=50, minVal=0, maxVal=100, minStep=1, normalStep=5, largeStep=10,
		displayName=None, useConfig=True):
		"""
		@param defaultVal: Specifies the default value for a numeric driver setting.
		@type defaultVal: int
		@param minVal: Specifies the minimum valid value for a numeric driver setting.
		@type minVal: int
		@param maxVal: Specifies the maximum valid value for a numeric driver setting.
		@type maxVal: int
		@param minStep: Specifies the minimum step between valid values for each numeric setting. For example, if L{minStep} is set to 10, setting values can only be multiples of 10; 10, 20, 30, etc.
		@type minStep: int
		@param normalStep: Specifies the step between values that a user will normally prefer. This is used in the settings ring.
		@type normalStep: int
		@param largeStep: Specifies the step between values if a large adjustment is desired. This is used for pageUp/pageDown on sliders in the Voice Settings dialog.
		@type largeStep: int
		@note: If necessary, the step values will be normalised so that L{minStep} <= L{normalStep} <= L{largeStep}.
		"""
		super(NumericDriverSetting,self).__init__(id, displayNameWithAccelerator, availableInSettingsRing=availableInSettingsRing,
			defaultVal=defaultVal, displayName=displayName, useConfig=useConfig)
		self.minVal=minVal
		self.maxVal=max(maxVal,self.defaultVal)
		self.minStep=minStep
		self.normalStep=max(normalStep,minStep)
		self.largeStep=max(largeStep,self.normalStep)

class BooleanDriverSetting(DriverSetting):
	"""Represents a boolean driver setting such as rate boost or automatic time sync.
	"""

	def __init__(self, id, displayNameWithAccelerator, availableInSettingsRing=False,
		displayName=None, defaultVal=False, useConfig=True):
		"""
		@param defaultVal: Specifies the default value for a boolean driver setting.
		@type defaultVal: bool
		"""
		super(BooleanDriverSetting,self).__init__(id, displayNameWithAccelerator, availableInSettingsRing=availableInSettingsRing,
			defaultVal=defaultVal, displayName=displayName, useConfig=useConfig)

	def _get_configSpec(self):
		defaultVal = repr(self.defaultVal) if self.defaultVal is not None else self.defaultVal
		return "boolean(default={defaultVal})".format(defaultVal=defaultVal)
