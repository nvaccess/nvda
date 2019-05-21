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

class VisionEnhancementProvider(driverHandler.Driver):
	"""A basic, abstract class for vision enhancement providers.
	Providers should usually base themselves on one or more of its subclasses.
	"""

	_configSection = "vision"
	#: A vision enhancement provider is a singleton.
	_instance = None
	cachePropertiesByDefault = True
	__role = None

	@classmethod
	def __new__(cls, *args, **kwargs):
		# Make this a singleton.
		inst = cls._instance() if cls._instance else None
		if not inst:
			obj = super(VisionEnhancementProvider, cls).__new__(cls, *args, **kwargs)
			obj.activeRoles = set()
			cls._instance = weakref.ref(obj)
			return obj
		return inst

	def __init__(self, *roles):
		"""Constructor.
		Subclasses may extend this method.
		They must extend this method if additional initialization has to be performed before all roles are initialized,
		e.g. when a library has to be loaded or initialized.
		"""
		super(VisionEnhancementProvider, self).__init__()
		if not roles:
			roles = self.supportedRoles
		for role in roles:
			if role not in self.supportedRoles:
				raise RuntimeError("Role %s not supported by %s" % (role, self.name))
			if role in self.activeRoles:
				log.debug("Role %s for provider %s is already initialized, silently ignoring" % (role, self.name))
				continue
			getattr(self, "initialize%s" % (role[0].upper()+role[1:]))()
			self.activeRoles.add(role)

	@classmethod
	def _get_supportedRoles(cls):
		"""Returns the roles supported by this provider."""
		return frozenset(
			getattr(subCls, "_%s__role" % subCls.__name__)
			for subCls in VisionEnhancementProvider.__subclasses__()
			if issubclass(cls, subCls)
		)

	@classmethod
	def getContextObject(cls, context):
		"""Gets the appropriate NVDAObject or CursorManager associated with the provided context."""
		if context == CONTEXT_FOCUS:
			return api.getFocusObject()
		elif context == CONTEXT_FOREGROUND:
			return api.getForegroundObject()
		elif context == CONTEXT_CARET:
			obj = api.getCaretObject()
			# Import late to avoid circular import
			import cursorManager
			if isinstance(obj, cursorManager.CursorManager):
				obj = None
			return obj
		elif context == CONTEXT_BROWSEMODE:
			obj = api.getCaretObject()
			# Import late to avoid circular import
			import cursorManager
			if not isinstance(obj, cursorManager.CursorManager):
				obj = None
			return obj
		elif context == CONTEXT_REVIEW:
			return api.getReviewPosition().obj
		elif context == CONTEXT_NAVIGATOR:
			return api.getNavigatorObject()
		elif context == CONTEXT_MOUSE:
			return api.getMouseObject()
		else:
			raise NotImplementedError("Couldn't get object for context %s" % context)

	@classmethod
	def getContextRect(cls, context, obj=None):
		"""Gets a rectangle for the specified context.
		If L{obj} is not C{None}, the object is used to get the rectangle from, if necessary.
		Otherwise, the base implementation calls L{getContextObject} and gets a rectangle from the object, if necessary."""
		if context == CONTEXT_REVIEW:
			return cls._getRectFromTextInfo(api.getReviewPosition())
		if not obj:
			obj = cls.getContextObject(context)
		if not obj:
			raise LookupError
		if getattr(obj, "treeInterceptor", None) and not obj.treeInterceptor.passThrough:
			obj = obj.treeInterceptor
		if context == CONTEXT_CARET:
			if isinstance(obj, NVDAObjects.NVDAObject):
				# Import late to avoid circular import
				from displayModel import getCaretRect
				# Check whether there is a caret in the window.
				# Note that, even windows that don't have navigable text could have a caret, such as in Excel.
				try:
					return RectLTRB.fromCompatibleType(getCaretRect(obj))
				except RuntimeError:
					if not obj._hasNavigableText:
						return None
		# Import late to avoid circular import
		import treeInterceptorHandler
		if (
			context in (CONTEXT_CARET, CONTEXT_BROWSEMODE)
			or isinstance(obj, treeInterceptorHandler.TreeInterceptor)
		):
			try:
				caretInfo = obj.makeTextInfo(textInfos.POSITION_CARET)
			except (NotImplementedError, RuntimeError):
				# Try a selection
				try:
					caretInfo = obj.makeTextInfo(textInfos.POSITION_SELECTION)
				except (NotImplementedError, RuntimeError):
					# There is nothing to do here
					raise LookupError
			return cls._getRectFromTextInfo(caretInfo)
		assert isinstance(obj, NVDAObjects.NVDAObject), "Unexpected object type %r" % obj
		location = obj.location
		if not location:
			raise LookupError
		return location.toLTRB()

	@classmethod
	def _getRectFromTextInfo(cls, textInfo):
		if textInfo.isCollapsed:
			textInfo.expand(textInfos.UNIT_CHARACTER)
		try:
			rects = textInfo.boundingRects
		except NotImplementedError:
			rects = None
		if rects:
			index = 0 if textInfo.obj.isTextSelectionAnchoredAtStart else -1
			rect = rects[index].toLTRB()
		else:
			rect = RectLTRB.fromPoint(textInfo.pointAtStart)
		return rect

	def terminate(self, *roles):
		"""Executed when terminating this provider.
		Subclasses may extend this method.
		They must extend this method if additional cleanup has to be performed after all roles are terminated,
		e.g. when resources have to be freed or a process has to be terminated.
		"""
		super(VisionEnhancementProvider,self).terminate()
		if not roles:
			roles = self.activeRoles.copy()
		for role in roles:
			if role not in self.supportedRoles:
				raise RuntimeError("Role %s not supported by %s" % (role, self.name))
			if role not in self.activeRoles:
				log.debug("Role %s for provider %s is not initialized, silently ignoring" % (role, self.name))
				continue
			getattr(self, "terminate%s" % (role[0].upper()+role[1:]))()
			self.activeRoles.remove(role)
