# -*- coding: UTF-8 -*-
#driverHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2018 NV Access Limited, Leonard de Ruijter

"""Handler for driver functionality that is global to synthesizers and braille displays."""

from baseObject import AutoPropertyObject
import config
from copy import deepcopy
from logHandler import log

class Driver(AutoPropertyObject):
	"""
	Abstract base class for drivers, such as speech synthesizer and braille display drivers.
	Abstract subclasses such as L{braille.BrailleDisplayDriver} should set L{_configSection}.

	At a minimum, drivers must set L{name} and L{description} and override the L{check} method.

	L{supportedSettings} should be set as appropriate for the settings supported by the driver.
	Each setting is retrieved and set using attributes named after the setting;
	e.g. the L{dotFirmness} attribute is used for the L{dotFirmness} setting.
	These will usually be properties.
	"""

	#: The name of the driver; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the driver.
	#: @type: str
	description = ""
	#: The configuration section where driver specific subsections should be saved.
	#: @type: str
	_configSection = ""

	def __init__(self):
		"""Initialize this driver.
		This method can also set default settings for the driver.
		@raise Exception: If an error occurs.
		@postcondition: This driver can be used.
		"""
		super(Driver, self).__init__()
		config.pre_configSave.register(self.saveSettings)

	def initSettings(self):
		"""
		Initializes the configuration for this driver.
		This method is called when initializing the driver.
		"""
		firstLoad = not config.conf[self._configSection].isSet(self.name)
		if firstLoad:
			# Create the new section.
			config.conf[self._configSection][self.name] = {}
		# Make sure the config spec is up to date, so the config validator does its work.
		config.conf[self._configSection][self.name].spec.update(self.getConfigSpec())
		# Make sure the instance has attributes for every setting
		for setting in self.supportedSettings:
			if not hasattr(self, setting.id):
				setattr(self, setting.id, setting.defaultVal)
		if firstLoad:
			self.saveSettings() #save defaults
		else:
			self.loadSettings()

	def terminate(self):
		"""Terminate this driver.
		This should be used for any required clean up.
		@precondition: L{initialize} has been called.
		@postcondition: This driver can no longer be used.
		"""
		self.saveSettings()
		config.pre_configSave.unregister(self.saveSettings)

	_abstract_supportedSettings = True
	def _get_supportedSettings(self):
		"""The settings supported by the driver.
		@rtype: list or tuple of L{DriverSetting}
		"""
		return ()

	@classmethod
	def check(cls):
		"""Determine whether this driver is available.
		The driver will be excluded from the list of available drivers if this method returns C{False}.
		For example, if a speech synthesizer requires installation and it is not installed, C{False} should be returned.
		@return: C{True} if this driver is available, C{False} if not.
		@rtype: bool
		"""
		return False

	def isSupported(self,settingID):
		"""Checks whether given setting is supported by the driver.
		@rtype: l{bool}
		"""
		for s in self.supportedSettings:
			if s.id == settingID: return True
		return False

	def getConfigSpec(self):
		spec=deepcopy(config.confspec[self._configSection]["__many__"])
		for setting in self.supportedSettings:
			if not setting.useConfig:
				continue
			spec[setting.id]=setting.configSpec
		return spec

	def saveSettings(self):
		"""
		Saves the current settings for the driver to the configuration.
		This method is also executed when the driver is loaded for the first time,
		in order to populate the configuration with the initial settings..
		"""
		conf=config.conf[self._configSection][self.name]
		for setting in self.supportedSettings:
			if not setting.useConfig:
				continue
			try:
				conf[setting.id] = getattr(self,setting.id)
			except UnsupportedConfigParameterError:
				log.debugWarning("Unsupported setting %s; ignoring"%s.id, exc_info=True)
				continue
		if self.supportedSettings:
			log.debug("Saved settings for {} {}".format(self.__class__.__name__, self.name))

	def loadSettings(self, onlyChanged=False):
		"""
		Loads settings for this driver from the configuration.
		This method assumes that the instance has attributes o/properties
		corresponding with the name of every setting in L{supportedSettings}.
		@param onlyChanged: When loading settings, only apply those for which
			the value in the configuration differs from the current value.
		@type onlyChanged: bool
		"""
		conf=config.conf[self._configSection][self.name]
		for setting in self.supportedSettings:
			if not setting.useConfig or conf.get(setting.id) is None:
				continue
			val=conf[setting.id]
			if onlyChanged and getattr(self,setting.id) == val:
				continue
			try:
				setattr(self,setting.id, val)
			except UnsupportedConfigParameterError:
				log.debugWarning("Unsupported setting %s; ignoring"%setting.name, exc_info=True)
				continue
		if self.supportedSettings:
			log.debug(
				(
					"Loaded changed settings for {} {}"
					if onlyChanged else
					"Loaded settings for {} {}"
				).format(self.__class__.__name__, self.name))

	@classmethod
	def _paramToPercent(cls, current, min, max):
		"""Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
		@param current: The current value.
		@type current: int
		@param min: The minimum value.
		@type current: int
		@param max: The maximum value.
		@type max: int
		"""
		return int(round(float(current - min) / (max - min) * 100))

	@classmethod
	def _percentToParam(cls, percent, min, max):
		"""Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum raw parameter values.
		@param percent: The current percentage.
		@type percent: int
		@param min: The minimum raw parameter value.
		@type min: int
		@param max: The maximum raw parameter value.
		@type max: int
		"""
		return int(round(float(percent) / 100 * (max - min) + min))

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

class UnsupportedConfigParameterError(NotImplementedError):
	"""
	Raised when changing or retrieving a driver setting that is unsupported for the connected device.
	"""

class StringParameterInfo(object):
	"""
	The base class used to represent a value of a string driver setting.
	"""

	def __init__(self, id, displayName):
		"""
		@param id: The unique identifier of the value.
		@type id: str
		@param displayName: The name of the value, visible to the user.
		@type displayName: str
		"""
		self.id = id
		self.displayName = displayName
		# Keep backwards compatibility
		self.ID = id
		self.name = displayName
