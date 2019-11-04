# vision/providerBase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module within the vision framework that contains the base vision enhancement provider class.
"""

from abc import abstractmethod, ABC

from autoSettingsUtils.autoSettings import AutoSettings, SupportedSettingType
from baseObject import AutoPropertyObject
from .visionHandlerExtensionPoints import EventExtensionPoints
from typing import Optional, Any


class VisionEnhancementProviderSettings(AutoSettings, ABC):
	"""
	Base class for settings for a vision enhancement provider.
	Ensure that the following are implemented:
	- AutoSettings.getId:
			This is case sensitive. Used in the config file. Does not have to match the module name.
	- AutoSettings.getTranslatedName:
			The string that should appear in the GUI as the name
	- AutoSettings._get_supportedSettings:
			The "runtime" settings for your provider
	Although technically optional, derived classes probably need to implement:
	- AutoSettings._get_preInitSettings:
			The settings always configurable for your provider
	"""
	supportedSettings: SupportedSettingType  # Typing for autoprop L{_get_supportedSettings}

	def __init__(self):
		super().__init__()
		self.initSettings()  # ensure that settings are loaded at construction time.

	@classmethod
	def _getConfigSection(cls) -> str:
		return "vision"  # all providers should be in the "vision" section.


class VisionProviderStateControl:
	""" Stub showing the interface for controlling the start/termination of a single provider.
			Implementors of this class should handle the outcome when things go wrong.
	"""

	@abstractmethod
	def startProvider(self) -> None:
		"""Initializes the provider in a way that is GUI friendly,
		showing an error if appropriate.
		@note: Use getProviderInstance to determine success
		"""

	@abstractmethod
	def terminateProvider(self, verbose: bool = False) -> None:
		"""Terminates one or more providers in a way that is GUI friendly,
		@verbose: Whether to show a termination error.
		@note: Use getProviderInstance to determine success
		"""

	@abstractmethod
	def getProviderInstance(self):
		"""Gets an instance of the provider if it already exists
		@rtype: Optional[VisionEnhancementProvider]
		"""

	@abstractmethod
	def getProviderInfo(self):
		"""
		@return: The provider info
		@rtype: providerInfo.ProviderInfo
		"""


class VisionEnhancementProvider(AutoPropertyObject):
	"""A class for vision enhancement providers.
	Derived classes should implement:
	- terminate:
			How to shutdown the provider
	- registerEventExtensionPoints:
			Allows the provider to receive updates form NVDA
	- canStart:
			Checks startup dependencies are satisfied
	- getSettings:
			Returns your implementation of VisionEnhancementProviderSettings
	Optional: To provide a custom GUI, return a SettingsPanel class type from:
	- getSettingsPanelClass
	"""
	cachePropertiesByDefault = True

	@classmethod
	def getSettings(cls) -> VisionEnhancementProviderSettings:
		"""
		@remarks: The L{VisionEnhancementProviderSettings} class should be implemented to define the settings
			for your provider
		"""
		...

	@classmethod
	def getSettingsPanelClass(cls) -> Optional[Any]:
		"""Returns the class to be used in order to construct a settingsPanel instance for the provider.
		The returned class must have a constructor which accepts:
			- parent: wx.Window
			- providerControl: VisionProviderStateControl
		EG:
		``` python
		class mySettingsPanel(gui.settingsDialogs.SettingsPanel):
			def __init__(self, parent: wx.Window, providerControl: VisionProviderStateControl):
				super().__init__(parent=parent)
		```
		@rtype: Optional[SettingsPanel]
		@remarks: When None is returned, L{gui.settingsDialogs.VisionProviderSubPanel_Wrapper} is used.
		"""
		return None

	def reinitialize(self) -> None:
		"""Reinitialize a vision enhancement provider, reusing the same instance.
		This base implementation simply calls terminate and __init__ consecutively.
		"""
		self.terminate()
		self.__init__()

	@abstractmethod
	def terminate(self) -> None:
		"""Terminate this driver.
		This should be used for any required clean up.
		@precondition: L{initialize} has been called.
		@postcondition: This provider can no longer be used.
		"""
		...

	@abstractmethod
	def registerEventExtensionPoints(self, extensionPoints: EventExtensionPoints) -> None:
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
