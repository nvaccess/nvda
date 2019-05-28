#vision/providerBase.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module within the vision framework that contains the base vision enhancement provider class.
"""

from .constants import *
import driverHandler
import api
import weakref
from logHandler import log
import NVDAObjects
import textInfos
from locationHelper import RectLTRB
from abc import abstractmethod

class VisionEnhancementProvider(driverHandler.Driver):
	"""A class for vision enhancement providers.
	"""

	_configSection = "vision"
	cachePropertiesByDefault = True
	supportedSettings = ()
	#: The roles supported by this provider.
	#: This attribute is currently not used,
	#: but might be later for presentational purposes.
	supportedRoles = frozenset()

	def reinitialize(self):
		"""Reinitializes a vision enhancement provider, reusing the same instance.
		The base method simply calls terminate and __init__ consecutively.
		"""
		self.terminate()
		self.__init__()

	@abstractmethod
	def registerEventExtensionPoints(self, extensionPoints):
		"""
		Called at provider initialization time, this method should register the provider
		to the several event extension points that it is interested in.
		@param extensionPoints: An object containing available extension points as attributes.
		@type extensionPoints: L{visionHandlerExtensionPoints.EventExtensionPoints}
		"""
		pass
