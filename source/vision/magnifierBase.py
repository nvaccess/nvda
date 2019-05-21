#vision/magnifierBase.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the magnifier base class.
A magnifier is used to magnify the full screen or a part of it.
"""

from .providerBase import VisionEnhancementProvider
import driverHandler
from abc import abstractmethod
from .constants import *

class Magnifier(VisionEnhancementProvider):
	"""A vision enhancement provider that supports magnifying (a part of) the screen.
	Subclasses should at least implement the L{initializeMagnifier},
	L{terminateMagnifier} and L{trackToRectangle} methods,
	and should implement the L{magnificationLevel} property.
	Supported contexts should be listed in L{supportedTrackingContexts}.
	"""

	__role = ROLE_MAGNIFIER

	#: Tuple of supported contexts for this magnifier to track to.
	supportedTrackingContexts = tuple()

	@abstractmethod
	def initializeMagnifier(self):
		"""Initializes a magnifier.
		Subclasses must extend this method.
		"""

	@abstractmethod
	def terminateMagnifier(self):
		"""Terminates a magnifier.
		Subclasses must extend this method.
		"""

	@classmethod
	def TrackToSetting(cls, context, displayName, defaultVal=True):
		"""Factory function for creating track to setting."""
		return driverHandler.BooleanDriverSetting(
			'trackTo%s' % (context[0].upper() + context[1:]),
			displayName,
			defaultVal=defaultVal
		)

	def trackToObject(self, obj=None, context=CONTEXT_UNDETERMINED, area=None):
		"""Tracks the magnifier to the given object.
		If object is C{None}, the appropriate object is fetched automatically.
		The base implementation simply tracks to the location of the object.
		Subclasses may override this method to implement context specific behaviour at the object level.
		"""
		if context not in self.enabledTrackingContexts:
			return
		try:
			rect = self.getContextRect(context, obj)
		except (LookupError, NotImplementedError):
			rect = None
		if not rect:
			return
		self.trackToRectangle(rect, context=context, area=area)

	@abstractmethod
	def trackToRectangle(self, rect, context=CONTEXT_UNDETERMINED, area=None):
		"""Tracks the magnifier to the given rectangle."""
		raise NotImplementedError

	def trackToPoint(self, point, context=CONTEXT_UNDETERMINED, area=None):
		"""Tracks the magnifier to the given point.
		The base implementation creates a rectangle from a point and tracks to that rectangle."""
		x, y = point
		rect = RectLTRB(x, y, x+1, y+1)
		self.trackToRectangle((rect), context=context, area=area)

	_abstract_magnificationLevel = True
	def _get_magnificationLevel(self):
		raise NotImplementedError

	def _set_magnificationLevel(self, level):
		raise NotImplementedError

	def _get_isMagnifying(self):
		"""Returns C{True} if the magnifier is magnifying the screen, C{False} otherwise.
		By default, this property is based on L{enabled} and L{magnificationLevel}
		"""
		return ROLE_MAGNIFIER in self.activeRoles and self.magnificationLevel > 1.0

	def _get_enabledTrackingContexts(self):
		"""Gets the contexts for which the magnifier is enabled.
		If L{isMagnifying} is C{False} this returns an empty tuple.
		"""
		if not self.isMagnifying:
			return ()
		return tuple(
			context for context in self.supportedTrackingContexts
			if getattr(self, 'trackTo%s' % (context[0].upper() + context[1:]))
		)
