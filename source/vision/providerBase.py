# vision/providerBase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module within the vision framework that contains the base vision enhancement provider class.
"""

import driverHandler
from abc import abstractmethod, ABC

from autoSettingsUtils.autoSettings import AutoSettings
from baseObject import AutoPropertyObject
from .constants import Role
from .visionHandlerExtensionPoints import EventExtensionPoints
from typing import FrozenSet, Type, Optional, List, Union, Tuple

SupportedSettingType = Union[
	List[driverHandler.DriverSetting],
	Tuple[driverHandler.DriverSetting]
]


class VisionEnhancementProviderSettings(AutoSettings, ABC):
	"""
	Base class for settings for a vision enhancement provider.
	Ensure that the following are implemented:
	- AutoSettings.getId
	- AutoSettings.getTranslatedName
	Although technically optional, derived classes probably need to implement:
	- AutoSettings._get_preInitSettings
	- AutoSettings._get_supportedSettings
	"""
	supportedSettings: SupportedSettingType  # Typing for autoprop L{_get_supportedSettings}

	def __init__(self):
		super().__init__()
		# ensure that settings are loaded at construction time.
		self.initSettings()

	@classmethod
	def _getConfigSection(cls) -> str:
		# all providers should be in the "vision" section.
		return "vision"


class VisionEnhancementProvider(AutoPropertyObject):
	"""A class for vision enhancement providers.
	Derived classes should implement:
	- terminate
	- registerEventExtensionPoints
	- canStart
	- getSettings
	To provide a custom GUI, return a SettingsPanel class type from:
	- getSettingsPanelClass
	"""
	cachePropertiesByDefault = True
	#: The roles supported by this provider.
	#: This attribute is currently not used,
	#: but might be later for presentational purposes.
	supportedRoles: FrozenSet[Role] = frozenset()

	@classmethod
	def getSettings(cls) -> VisionEnhancementProviderSettings:
		"""
		@remarks: The L{VisionEnhancementProviderSettings} class should be implemented to define the settings
			for your provider
		"""
		...

	@classmethod
	def getSettingsPanelClass(cls) -> Optional[Type]:
		"""Returns the instance to be used in order to construct a settings panel for the provider.
		@return: Optional[SettingsPanel]
		@remarks: When None is returned, L{gui.settingsDialogs.VisionProviderSubPanel_Wrapper} is used.
		"""
		return None

	def reinitialize(self):
		"""Reinitialize a vision enhancement provider, reusing the same instance.
		This base implementation simply calls terminate and __init__ consecutively.
		"""
		self.terminate()
		self.__init__()

	@abstractmethod
	def terminate(self):
		"""Terminate this driver.
		This should be used for any required clean up.
		@precondition: L{initialize} has been called.
		@postcondition: This provider can no longer be used.
		"""
		...

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
		...

	@classmethod
	@abstractmethod
	def canStart(cls) -> bool:
		"""Returns whether this provider is able to start."""
		return False
