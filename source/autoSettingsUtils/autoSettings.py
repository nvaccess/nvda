# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""autoSettings for add-ons"""
from abc import abstractmethod
from copy import deepcopy
from typing import List, Tuple, Union, Dict, Type

import config
from autoSettingsUtils.utils import paramToPercent, percentToParam, UnsupportedConfigParameterError
from baseObject import AutoPropertyObject
from logHandler import log
from .driverSetting import DriverSetting

SupportedSettingType: Type = Union[
	List[DriverSetting],
	Tuple[DriverSetting]
]


class AutoSettings(AutoPropertyObject):
	"""
	"""

	def __init__(self):
		"""
		"""
		super().__init__()
		self._registerConfigSaveAction()

	def __del__(self):
		self._unregisterConfigSaveAction()

	def _registerConfigSaveAction(self):
		"""Overrideable pre_configSave registration"""
		log.debug(f"registering pre_configSave action: {self.__class__!r}")
		config.pre_configSave.register(self.saveSettings)

	def _unregisterConfigSaveAction(self):
		"""Overrideable pre_configSave de-registration"""
		log.debug(f"de-registering pre_configSave action: {self.__class__!r}")
		config.pre_configSave.unregister(self.saveSettings)

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
		return paramToPercent(current, min, max)

	@classmethod
	def _percentToParam(cls, percent, min, max):
		return percentToParam(percent, min, max)
