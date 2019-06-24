#vision/util.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Utility functions for vision enhancement providers.
"""

from .constants import Role, Context
import api
import locationHelper

def getReviewRectangle():
	return _getRectFromTextInfo(api.getReviewPosition())

def getCaretRectangle(obj=None):
	if obj is None:
		obj = api.getCaretObject()
	if api.isObjectInActiveTreeInterceptor(obj):
		obj = obj.treeInterceptor
	if api.isNVDAObject(obj):
		# Import late to avoid circular import
		from displayModel import getCaretRect
		# Check whether there is a caret in the window.
		# Note that, even windows that don't have navigable text could have a caret, such as in Excel.
		try:
			return RectLTRB.fromCompatibleType(getCaretRect(obj))
		except RuntimeError:
			if not obj._hasNavigableText:
				raise LookupError
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

def getMouseRectangle():
	point = locationHelper.Point(*mouseHandler.curMousePos)
	return locationHelper.RectLTRB.fromPoint(point)

def getObjectRectangle(obj):
	if not api.isNVDAObject(obj):
		raise TypeError("obj must be of type NVDAObject")
	location = obj.location
	if not location:
		raise LookupError
	return location.toLTRB()

def getContextRect(context, obj=None):
	"""Gets a rectangle for the specified context."""
	if context == Context.FOCUS:
		return getObjectRectangle(obj or api.getFocusObject())
	elif context == Context.NAVIGATOR:
		return getObjectRectangle(obj or api.getNavigatorObject())
	elif context == Context.REVIEW:
		return getReviewRectangle()
	elif context == Context.BROWSEMODE:
		caret = obj or api.getCaretObject()
		if api.isCursorManager(caret):
			return getCaretRectangle(obj=caret)
		return None
	elif context == Context.CARET:
		caret = obj or api.getCaretObject()
		if not api.isCursorManager(caret):
			return getCaretRectangle(obj=caret)
		return None
	elif context == Context.MOUSE:
		return getMouseRectangle()

def getRectFromTextInfo(textInfo):
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
