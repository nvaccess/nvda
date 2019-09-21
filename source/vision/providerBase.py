# vision/providerBase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module within the vision framework that contains the base vision enhancement provider class.
"""

import driverHandler
from abc import abstractmethod
from .constants import Role
from .visionHandlerExtensionPoints import EventExtensionPoints
from typing import FrozenSet


class VisionEnhancementProviderStaticSettings(driverHandler.Driver):
	_configSection = "vision"

class VisionEnhancementProvider(driverHandler.Driver):
	"""A class for vision enhancement providers.
	"""

	_configSection = "vision"
	cachePropertiesByDefault = True
	#: The roles supported by this provider.
	#: This attribute is currently not used,
	#: but might be later for presentational purposes.
	supportedRoles: FrozenSet[Role] = frozenset()

	def _get_supportedSettings(self):
		return super().supportedSettings

	@classmethod
	def getSettingsPanel(cls):
		"""Returns the instance to be used in order to construct a settings panel for the provider.
		@return: Optional[SettingsPanel]
		@remarks: When None is returned, L{gui.settingsDialogs.VisionProviderSubPanel_Default} is used.
		"""
		return None

	def reinitialize(self):
		"""Reinitializes a vision enhancement provider, reusing the same instance.
		This base implementation simply calls terminate and __init__ consecutively.
		"""
		self.terminate()
		self.__init__()

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

	@classmethod
	def check(cls) -> bool:
		return cls.canStart()

	@classmethod
	def confirmInitWithUser(cls) -> bool:
		"""Before initialisation of the provider,
		confirm with the user that the provider should start.
		This method should be executed on the main thread.
		@returns: C{True} if initialisation should continue, C{False} otherwise.
		"""
		return True
