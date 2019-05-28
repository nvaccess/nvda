#vision/utilities.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Utility functions for vision enhancement providers.
"""

from .constants import *

def getContextObject(context):
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

def getContextRect(context, obj=None):
	"""Gets a rectangle for the specified context.
	If L{obj} is not C{None}, the object is used to get the rectangle from, if necessary.
	Otherwise, the base implementation calls L{getContextObject} and gets a rectangle from the object, if necessary."""
	if context == CONTEXT_REVIEW:
		return _getRectFromTextInfo(api.getReviewPosition())
	if not obj:
		obj = getContextObject(context)
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
		return _getRectFromTextInfo(caretInfo)
	assert isinstance(obj, NVDAObjects.NVDAObject), "Unexpected object type %r" % obj
	location = obj.location
	if not location:
		raise LookupError
	return location.toLTRB()

@classmethod
def _getRectFromTextInfo(textInfo):
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
