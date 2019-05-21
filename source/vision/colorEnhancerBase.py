#vision/colorEnhancerBase.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the color enhancer base class.
A color enhancer is used to change the color presentation of the whole screen or a part of it.
"""

from .providerBase import VisionEnhancementProvider
import driverHandler
from abc import abstractmethod
from collections import OrderedDict
from .constants import ROLE_COLORENHANCER

class ColorTransformationInfo(driverHandler.StringParameterInfo):
	"""Represents a color transformation.
	"""

	def __init__(self, id, name, value):
		#: The value that contains the color transformation info (e.g. a matrix).
		self.value = value
		super(ColorTransformationInfo,self).__init__(id, name)

class ColorEnhancer(VisionEnhancementProvider):
	"""A vision enhancement provider that changes the coloring of the screen.
	For example, it could implement high contrast schemes,
	or act as a screen curtain in making the screen invisible for users.
	Subclasses should at least implement the L{initializeColorEnhancer}
	and L{terminateColorEnhancer} methods.
	If the enhancer supports multiple transformations (color schemes or enhancements),
	they should be returned when calling L{_getAvailableTransformations}.
	In this case, the L{transformation} property ought to be implemented
	to retrieve or change the current transformation.
	"""

	__role = ROLE_COLORENHANCER

	@abstractmethod
	def initializeColorEnhancer(self):
		"""Initializes a color enhancer.
		Subclasses must extend this method.
		"""

	@abstractmethod
	def terminateColorEnhancer(self):
		"""Terminates a color enhancer.
		Subclasses must extend this method.
		"""

	@abstractmethod
	def _getAvailableTransformations(self):
		"""Returns the color transformations supported by this color enhancer.
		@rtype: [L{ColorTransformationInfo}]
		"""
		return []

	def _get_availableTransformations(self):
		return OrderedDict((info.ID,info) for info in self._getAvailableTransformations())

	@classmethod
	def TransformationSetting(cls):
		"""Factory function for creating transformation setting."""
		# Translators: Label for a color enhancer setting.
		return driverHandler.DriverSetting("transformation",_("&Color transformation"))

	def _get_transformation(self):
		return None
