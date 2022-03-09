# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""autoSettings for add-ons"""
from abc import abstractmethod
from copy import deepcopy
from typing import Dict, Type, Any, Iterable

import config
from autoSettingsUtils.utils import paramToPercent, percentToParam, UnsupportedConfigParameterError
from baseObject import AutoPropertyObject
from logHandler import log
from .driverSetting import DriverSetting

SupportedSettingType: Type = Iterable[DriverSetting]


class AutoSettings(AutoPropertyObject):
	""" An AutoSettings instance is used to simplify the load/save of user config for NVDA extensions
	(Synth drivers, braille drivers, vision providers) and make it possible to automatically provide a
	standard GUI for these settings.
	Derived classes must implement:
	- getId
	- getDisplayName
	- _get_supportedSettings
	"""

	def __init__(self):
		"""Perform any initialisation
		@note: registers with the config save action extension point
		"""
		super().__init__()
		self._registerConfigSaveAction()

	def __del__(self):
		self._unregisterConfigSaveAction()

	def _registerConfigSaveAction(self):
		""" Overrideable pre_configSave registration
		"""
		log.debug(f"registering pre_configSave action: {self.__class__!r}")
		config.pre_configSave.register(self.saveSettings)

	def _unregisterConfigSaveAction(self):
		""" Overrideable pre_configSave de-registration
		"""
		config.pre_configSave.unregister(self.saveSettings)

	@classmethod
	@abstractmethod
	def getId(cls) -> str:
		"""
		@return: Application friendly name, should be globally unique, however since this is used in the config file
		human readable is also beneficial.
		"""
		...

	@classmethod
	@abstractmethod
	def getDisplayName(cls) -> str:
		"""
		@return: The translated name for this collection of settings. This is for use in the GUI to represent the
		group of these settings.
		"""
		...

	@classmethod
	@abstractmethod
	def _getConfigSection(cls) -> str:
		"""
		@return: The section of the config that these settings belong in.
		"""
		...

	@classmethod
	def _initSpecificSettings(
			cls,
			clsOrInst: Any,
			settings: SupportedSettingType
	) -> None:
		section = cls._getConfigSection()
		settingsId = cls.getId()
		firstLoad = not config.conf[section].isSet(settingsId)
		if firstLoad:
			# Create the new section.
			config.conf[section][settingsId] = {}
		# Make sure the config spec is up to date, so the config validator does its work.
		config.conf[section][settingsId].spec.update(
			cls._getConfigSpecForSettings(settings)
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
		"""Initializes the configuration for this AutoSettings instance.
		This method is called when initializing the AutoSettings instance.
		"""
		self._initSpecificSettings(self, self.supportedSettings)

	#: Typing for auto property L{_get_supportedSettings}
	supportedSettings: SupportedSettingType

	# make supportedSettings an abstract property
	_abstract_supportedSettings = True

	def _get_supportedSettings(self) -> SupportedSettingType:
		"""The settings supported by the AutoSettings instance. Abstract.
		"""
		return []

	def isSupported(self, settingID) -> bool:
		"""Checks whether given setting is supported by the AutoSettings instance.
		"""
		for s in self.supportedSettings:
			if s.id == settingID:
				return True
		return False

	@classmethod
	def _getConfigSpecForSettings(
			cls,
			settings: SupportedSettingType
	) -> Dict:
		section = cls._getConfigSection()
		spec = deepcopy(config.confspec[section]["__many__"])
		for setting in settings:
			if not setting.useConfig:
				continue
			spec[setting.id] = setting.configSpec
		return spec

	def getConfigSpec(self):
		return self._getConfigSpecForSettings(self.supportedSettings)

	@classmethod
	def _saveSpecificSettings(
			cls,
			clsOrInst: Any,
			settings: SupportedSettingType
	) -> None:
		"""
		Save values for settings to config.
		The values from the attributes of `clsOrInst` that match the `id` of each setting are saved to config.
		@param clsOrInst: Destination for the values.
		@param settings: The settings to load.
		"""
		section = cls._getConfigSection()
		settingsId = cls.getId()
		conf = config.conf[section][settingsId]
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
		Saves the current settings for the AutoSettings instance to the configuration.
		This method is also executed when the AutoSettings instance is loaded for the first time,
		in order to populate the configuration with the initial settings..
		"""
		self._saveSpecificSettings(self, self.supportedSettings)

	@classmethod
	def _loadSpecificSettings(
			cls,
			clsOrInst: Any,
			settings: SupportedSettingType,
			onlyChanged: bool = False
	) -> None:
		"""
		Load settings from config, set them on `clsOrInst`.
		@param clsOrInst: Destination for the values.
		@param settings: The settings to load.
		@param onlyChanged: When True, only settings that no longer match the config are set.
		@note: attributes are set on clsOrInst using setattr.
			The id of each setting in `settings` is used as the attribute name.
		"""
		section = cls._getConfigSection()
		settingsID = cls.getId()
		log.debug(f"loading {section} {settingsID}")
		conf = config.conf[section][settingsID]
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
					f"Unsupported setting {setting.id!r}; ignoring",
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
		Loads settings for this AutoSettings instance from the configuration.
		This method assumes that the instance has attributes o/properties
		corresponding with the name of every setting in L{supportedSettings}.
		@param onlyChanged: When loading settings, only apply those for which
			the value in the configuration differs from the current value.
		"""
		self._loadSpecificSettings(self, self.supportedSettings, onlyChanged)

	@classmethod
	def _paramToPercent(cls, current: int, min: int, max: int) -> int:
		"""Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
		@param current: The current value.
		@param min: The minimum value.
		@param max: The maximum value.
		"""
		return paramToPercent(current, min, max)

	@classmethod
	def _percentToParam(cls, percent: int, min: int, max: int) -> int:
		"""Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum
		raw parameter values.
		@param percent: The current percentage.
		@param min: The minimum raw parameter value.
		@param max: The maximum raw parameter value.
		"""
		return percentToParam(percent, min, max)
