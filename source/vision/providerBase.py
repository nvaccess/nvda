# vision/providerBase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module within the vision framework that contains the base vision enhancement provider class.
"""

from abc import abstractmethod
import config
from autoSettingsUtils.autoSettings import AutoSettings
from baseObject import AutoPropertyObject
from .visionHandlerExtensionPoints import EventExtensionPoints
from typing import Optional, Any


class VisionEnhancementProviderSettings(AutoSettings):
	"""
	Base class for settings for a vision enhancement provider.
	Ensure that the following are implemented:
	- AutoSettings.getId:
			This is case sensitive. Used in the config file. Does not have to match the module name.
	- AutoSettings.getDisplayName:
			The string that should appear in the GUI as the name.
	- AutoSettings._get_supportedSettings:
			The settings for your provider, the returned list is permitted to change during
			start / termination of the provider.
			The implementation must handle how to modify the returned settings based on external (software,
			hardware) dependencies.
	@note
	If the vision enhancement provider has settings, it will provide an implementation of this class.
	The provider will hold a reference to an instance of this class, this is accessed through the class method
	L{VisionEnhancementProvider.getSettings}.
	One way to handle settings that are strictly runtime:
	- During initialization, the vision enhancement provider can instruct the settings instance what it should
	expose using the L{utoSettings._get_supportedSettings} property.
	- "_exampleProvider_autoGui.py" provides an example of this.
	"""
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
	def getProviderInfo(self):
		"""
		@return: The provider info
		@rtype: providerInfo.ProviderInfo
		"""

	@abstractmethod
	def getProviderInstance(self):
		"""Gets an instance for the provider if it already exists
		@rtype: Optional[VisionEnhancementProvider]
		"""

	@abstractmethod
	def startProvider(self, shouldPromptOnError: bool) -> bool:
		"""Initializes the provider, prompting user with the error if necessary.
		@param shouldPromptOnError: True if  the user should be presented with any errors that may occur.
		@return: True on success
		"""

	@abstractmethod
	def terminateProvider(self, shouldPromptOnError: bool) -> bool:
		"""Terminate the provider, prompting user with the error if necessary.
		@param shouldPromptOnError: True if  the user should be presented with any errors that may occur.
		@return: True on success
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
	@abstractmethod
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
		"""Terminate this provider.
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

	@classmethod
	def enableInConfig(cls, enable: bool) -> None:
		"""Enables or disables the provider in the current configuration.
		@param enable: Whether to enable (C{True}) or disable (C{False}) the provider in the configuration.
		"""
		settings = cls.getSettings()
		config.conf[settings._getConfigSection()][settings.getId()]["enabled"] = enable

	@classmethod
	def isEnabledInConfig(cls) -> bool:
		"""Returns whether the provider is enabled in the configuration."""
		settings = cls.getSettings()
		return config.conf[settings._getConfigSection()][settings.getId()]["enabled"]
