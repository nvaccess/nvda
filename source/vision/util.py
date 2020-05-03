# vision/util.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Utility functions for vision enhancement providers."""

from .constants import Context
import api
import locationHelper
from documentBase import TextContainerObject
from NVDAObjects import NVDAObject
from typing import Optional
import textInfos
import mouseHandler


def getReviewRect() -> locationHelper.RectLTRB:
	return getRectFromTextInfo(api.getReviewPosition())


def getCaretRect(obj: Optional[TextContainerObject] = None) -> locationHelper.RectLTRB:
	if obj is None:
		obj = api.getCaretObject()
	if api.isObjectInActiveTreeInterceptor(obj):
		obj = obj.treeInterceptor
	if api.isNVDAObject(obj):
		# Import late to avoid circular import
		import displayModel
		# Check whether there is a caret in the window.
		# Note that, even windows that don't have navigable text could have a caret, such as in Excel.
		try:
			return displayModel.getCaretRect(obj)
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
	return getRectFromTextInfo(caretInfo)


def getMouseRect() -> locationHelper.RectLTRB:
	point = locationHelper.Point(*mouseHandler.curMousePos)
	return locationHelper.RectLTRB.fromPoint(point)


def getObjectRect(obj: NVDAObject) -> locationHelper.RectLTRB:
	if not api.isNVDAObject(obj):
		raise TypeError("obj must be of type NVDAObject, %s not supported" % type(obj).__name__)
	location = obj.location
	if not location:
		raise LookupError
	return location.toLTRB()


def getContextRect(
		context: Context,
		obj: Optional[TextContainerObject] = None
) -> Optional[locationHelper.RectLTRB]:
	"""Gets a rectangle for the specified context."""
	if context == Context.FOCUS:
		return getObjectRect(obj or api.getFocusObject())
	elif context == Context.NAVIGATOR:
		return getObjectRect(obj or api.getNavigatorObject())
	elif context == Context.REVIEW:
		return getReviewRect()
	elif context == Context.BROWSEMODE:
		caret = obj or api.getCaretObject()
		if api.isCursorManager(caret):
			return getCaretRect(obj=caret)
		return None
	elif context == Context.CARET:
		caret = obj or api.getCaretObject()
		if not api.isCursorManager(caret):
			return getCaretRect(obj=caret)
		return None
	elif context == Context.MOUSE:
		return getMouseRect()


def getRectFromTextInfo(textInfo: textInfos.TextInfo) -> locationHelper.RectLTRB:
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
		rect = locationHelper.RectLTRB.fromPoint(textInfo.pointAtStart)
	return rect
