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
from typing import List, Tuple, Dict, Union


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
		self._registerConfigSaveAction()

	def _registerConfigSaveAction(self):
		log.debug(f"registering: {self.__class__!r}")
		config.pre_configSave.register(self.saveSettings)

	@classmethod
	def _initSpecificSettings(cls, clsOrInst, settings: List):
		firstLoad = not config.conf[cls._configSection].isSet(cls.name)
		if firstLoad:
			# Create the new section.
			config.conf[cls._configSection][cls.name] = {}
		# Make sure the config spec is up to date, so the config validator does its work.
		config.conf[cls._configSection][cls.name].spec.update(
			cls._getConfigSPecForSettings(settings)
		)
		# Make sure the clsOrInst has attributes for every setting
		for setting in settings:
			if not hasattr(clsOrInst, setting.id):
				setattr(clsOrInst, setting.id, setting.defaultVal)
		if firstLoad:
			cls._saveSpecificSettings(clsOrInst, settings)  # save defaults
		else:
			cls._loadSpecificSettings(clsOrInst, settings)

	def initSettings(self):
		"""
		Initializes the configuration for this driver.
		This method is called when initializing the driver.
		"""
		self._initSpecificSettings(self, self.supportedSettings)

	def terminate(self, saveSettings: bool = True):
		"""Terminate this driver.
		This should be used for any required clean up.
		@param saveSettings: Whether settings should be saved on termination.
		@precondition: L{initialize} has been called.
		@postcondition: This driver can no longer be used.
		"""
		if saveSettings:
			self.saveSettings()
		config.pre_configSave.unregister(self.saveSettings)

	@classmethod
	def _get_preInitSettings(self) -> Union[List, Tuple]:
		"""The settings supported by the driver at pre initialisation time.
		@rtype: list or tuple of L{DriverSetting}
		"""
		return ()

	_abstract_supportedSettings = True

	def _get_supportedSettings(self) -> Union[List, Tuple]:
		"""The settings supported by the driver.
		When overriding this property, subclasses are encouraged to extend the getter method
		to ensure that L{preInitSettings} is part of the list of supported settings.
		@rtype: list or tuple of L{DriverSetting}
		"""
		return self.preInitSettings

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

	@classmethod
	def _getConfigSPecForSettings(
			cls,
			settings: Union[List, Tuple]
	) -> Dict:
		spec = deepcopy(config.confspec[cls._configSection]["__many__"])
		for setting in settings:
			if not setting.useConfig:
				continue
			spec[setting.id]=setting.configSpec
		return spec

	def getConfigSpec(self):
		return self._getConfigSPecForSettings(self.supportedSettings)

	@classmethod
	def _saveSpecificSettings(
			cls,
			clsOrInst,
			settings: Union[List, Tuple]
	):
		conf = config.conf[cls._configSection][cls.name]
		for setting in settings:
			if not setting.useConfig:
				continue
			try:
				conf[setting.id] = getattr(clsOrInst, setting.id)
			except UnsupportedConfigParameterError:
				log.debugWarning(
					f"Unsupported setting {setting.id!r}; ignoring",
					exc_info=True
				)
				continue
		if settings:
			log.debug(f"Saved settings for {cls.__qualname__}")

	def saveSettings(self):
		"""
		Saves the current settings for the driver to the configuration.
		This method is also executed when the driver is loaded for the first time,
		in order to populate the configuration with the initial settings..
		"""
		self._saveSpecificSettings(self, self.supportedSettings)

	@classmethod
	def _loadSpecificSettings(
			cls,
			clsOrInst,
			settings: Union[List, Tuple],
			onlyChanged: bool = False
	):
		log.debug(f"loading {cls._configSection} {cls.name}")
		conf = config.conf[cls._configSection][cls.name]
		for setting in settings:
			if not setting.useConfig or conf.get(setting.id) is None:
				continue
			val = conf[setting.id]
			if onlyChanged and getattr(clsOrInst, setting.id) == val:
				continue
			try:
				setattr(clsOrInst, setting.id, val)
			except UnsupportedConfigParameterError:
				log.debugWarning(
					f"Unsupported setting {setting.name!r}; ignoring",
					exc_info=True
				)
				continue
		if settings:
			log.debug(
				f"Loaded changed settings for {cls.__qualname__}"
				if onlyChanged else
				f"Loaded settings for {cls.__qualname__}"
			)

	def loadSettings(self, onlyChanged: bool = False):
		"""
		Loads settings for this driver from the configuration.
		This method assumes that the instance has attributes o/properties
		corresponding with the name of every setting in L{supportedSettings}.
		@param onlyChanged: When loading settings, only apply those for which
			the value in the configuration differs from the current value.
		"""
		self._loadSpecificSettings(self, self.supportedSettings, onlyChanged)

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
