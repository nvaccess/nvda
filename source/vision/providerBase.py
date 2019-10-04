# vision/providerBase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module within the vision framework that contains the base vision enhancement provider class.
"""

import driverHandler
from abc import abstractmethod

from baseObject import AutoPropertyObject
from .constants import Role
from .visionHandlerExtensionPoints import EventExtensionPoints
from typing import FrozenSet, Type, Optional, List, Union, Tuple

SupportedSettingType = Union[
	List[driverHandler.DriverSetting],
	Tuple[driverHandler.DriverSetting]
]


class VisionEnhancementProviderStaticSettings(driverHandler.Driver):
	_configSection = "vision"
	cachePropertiesByDefault = True

	supportedSettings: SupportedSettingType  # Typing for autoprop L{_get_supportedSettings}

	def __init__(self):
		super().__init__()
		self.initSettings()

	@property
	@abstractmethod
	def name(self):  # todo: rename this? "providerID"
		"""Application Friendly name, should be unique!"""

	@property
	@abstractmethod
	def description(self):  # todo: rename this? "translated Name"
		"""Translated name"""

	def _get_supportedSettings(self) -> SupportedSettingType:
		raise NotImplementedError(
			f"_get_supportedSettings must be implemented in Class {self.__class__.__qualname__}"
		)

	@classmethod
	def check(cls):  # todo: remove, comes from Driver
		return True

	def loadSettings(self, onlyChanged: bool = False):
		super().loadSettings(onlyChanged)

	def saveSettings(self):
		super().saveSettings()


class VisionEnhancementProvider(AutoPropertyObject):
	"""A class for vision enhancement providers.
	"""
	cachePropertiesByDefault = True
	#: The roles supported by this provider.
	#: This attribute is currently not used,
	#: but might be later for presentational purposes.
	supportedRoles: FrozenSet[Role] = frozenset()

	@classmethod
	def getSettings(cls) -> VisionEnhancementProviderStaticSettings:
		"""
		@remarks: The L{VisionEnhancementProviderStaticSettings} class should be implemented to define the settings
			for your provider
		"""
		raise NotImplementedError(
			f"getSettings must be implemented in Class {cls.__qualname__}"
		)

	@classmethod
	def getSettingsPanelClass(cls) -> Optional[Type]:
		"""Returns the instance to be used in order to construct a settings panel for the provider.
		@return: Optional[SettingsPanel]
		@remarks: When None is returned, L{gui.settingsDialogs.VisionProviderSubPanel_Default} is used.
		"""
		return None

	def reinitialize(self):
		"""Reinitialize a vision enhancement provider, reusing the same instance.
		This base implementation simply calls terminate and __init__ consecutively.
		"""
		self.terminate()
		self.__init__()

	# todo: remove saveSettings param
	def terminate(self, saveSettings: bool = True):
		"""Terminate this driver.
		This should be used for any required clean up.
		@param saveSettings: Whether settings should be saved on termination.
		@precondition: L{initialize} has been called.
		@postcondition: This driver can no longer be used.
		"""

	@abstractmethod
	def registerEventExtensionPoints(self, extensionPoints: EventExtensionPoints):
		"""
		Called at provider initialization time, this method should register the provider
		to the several event extension points that it is interested in.
		This method should only register itself with the extension points,
		and should refrain from doing anything else,
		as it might be called again several times between initialization and termination.
		@param extensionPoints: An object containing available extension points as attributes.
		"""
		pass

	@classmethod
	@abstractmethod
	def canStart(cls) -> bool:
		"""Returns whether this provider is able to start."""
		return False

	# todo: remove this, providers should do this themselves
	@classmethod
	def confirmInitWithUser(cls) -> bool:
		"""Before initialisation of the provider,
		confirm with the user that the provider should start.
		This method should be executed on the main thread.
		@returns: C{True} if initialisation should continue, C{False} otherwise.
		"""
		return True
