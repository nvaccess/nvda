# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2021 NV Access Limited, Babbage B.V.

import winVersion
from logHandler import log
import eventHandler
import controlTypes
import textInfos
import UIAHandler
from UIAHandler.utils import (
	getChildrenWithCacheFromUIATextRange,
	getEnclosingElementWithCacheFromUIATextRange,
)
from . import UIA, web

"""
	A module for using the legacy Edge browser (code name spartan) via UIA.
	Specialisations on the UIA.web module.
"""


class EdgeTextInfo(web.UIAWebTextInfo):
	...


class EdgeTextInfo_preGapRemoval(EdgeTextInfo):

	def _hasEmbedded(self):
		""" Is this textInfo positioned on an embedded child?
		"""
		children = self._rangeObj.getChildren()
		if children.length:
			child = children.getElement(0)
			if not child.getCurrentPropertyValue(UIAHandler.UIA_IsTextPatternAvailablePropertyId):
				childRange = self.obj.UIATextPattern.rangeFromChild(child)
				if childRange:
					childChildren = childRange.getChildren()
				if (
					childChildren.length == 1
					and UIAHandler.handler.clientObject.compareElements(child, childChildren.getElement(0))
				):
					return True
		return False

	def move(self, unit, direction, endPoint=None, skipReplacedContent=True):
		# Skip over non-text element starts and ends
		if not endPoint:
			if direction > 0 and unit in (
				textInfos.UNIT_LINE,
				textInfos.UNIT_PARAGRAPH
			):
				return self._collapsedMove(unit, direction, skipReplacedContent)
			elif direction > 0:
				res = self._collapsedMove(unit, direction, skipReplacedContent)
				if res != 0:
					# Ensure we move past the start of any elements
					tempInfo = self.copy()
					while 0 != super(EdgeTextInfo, tempInfo).move(textInfos.UNIT_CHARACTER, 1):
						tempInfo.setEndPoint(self, "startToStart")
						if tempInfo.text or tempInfo._hasEmbedded():
							break
						tempInfo.collapse(True)
						self._rangeObj = tempInfo._rangeObj.clone()
				return res
			elif direction < 0:
				tempInfo = self.copy()
				res = self._collapsedMove(unit, direction, skipReplacedContent)
				if res != 0:
					while True:
						tempInfo.setEndPoint(self, "startToStart")
						if tempInfo.text or tempInfo._hasEmbedded():
							break
						if 0 == super(EdgeTextInfo, self).move(textInfos.UNIT_CHARACTER, -1):
							break
				return res
		else:
			tempInfo = self.copy()
			res = tempInfo.move(unit, direction, skipReplacedContent=skipReplacedContent)
			if res != 0:
				self.setEndPoint(tempInfo, "endToEnd" if endPoint == "end" else "startToStart")
			return res

	def expand(self, unit):
		# Ensure expanding to character/word correctly covers embedded controls
		if unit in (
			textInfos.UNIT_CHARACTER,
			textInfos.UNIT_WORD,
		):
			tempInfo = self.copy()
			tempInfo.move(textInfos.UNIT_CHARACTER, 1, endPoint="end", skipReplacedContent=False)
			if tempInfo._hasEmbedded():
				self.setEndPoint(tempInfo, "endToEnd")
				return
		super(EdgeTextInfo, self).expand(unit)
		return

	# C901 '_getTextWithFieldsForUIARange' is too complex
	# Note: when working here look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def _getTextWithFieldsForUIARange(  # noqa: C901
		self,
		rootElement,
		textRange,
		formatConfig,
		includeRoot=True,
		recurseChildren=True,
		alwaysWalkAncestors=True,
		_rootElementClipped=(True, True)
	):
		# Edge zooms into its children at the start.
		# Thus you are already in the deepest first child.
		# Therefore get the deepest enclosing element at the start, get its content, Then do the whole thing
		# again on the content from the end of the enclosing element to the end of its parent, and repeat!
		# In other words, get the content while slowly zooming out from the start.
		log.debug("_getTextWithFieldsForUIARange (unbalanced)")
		if not recurseChildren:
			log.debug("recurseChildren is False. Falling back to super")
			for field in super(EdgeTextInfo, self)._getTextWithFieldsForUIARange(
				rootElement,
				textRange,
				formatConfig,
				includeRoot=includeRoot,
				alwaysWalkAncestors=True,
				recurseChildren=False,
				_rootElementClipped=_rootElementClipped
			):
				yield field
			return
		if log.isEnabledFor(log.DEBUG):
			log.debug(f"rootElement: {rootElement.currentLocalizedControlType}")
			log.debug(f"full text: {textRange.getText(-1)}")
			log.debug(f"includeRoot: {includeRoot}")
		startRange = textRange.clone()
		startRange.MoveEndpointByRange(
			UIAHandler.TextPatternRangeEndpoint_End,
			startRange,
			UIAHandler.TextPatternRangeEndpoint_Start
		)
		enclosingElement = getEnclosingElementWithCacheFromUIATextRange(
			startRange,
			self._controlFieldUIACacheRequest
		)
		if not enclosingElement:
			log.debug("No enclosingElement. Returning")
			return
		enclosingRange = self.obj.getNormalizedUIATextRangeFromElement(enclosingElement)
		if not enclosingRange:
			log.debug("enclosingRange is NULL. Returning")
			return
		if log.isEnabledFor(log.DEBUG):
			log.debug(f"enclosingElement: {enclosingElement.currentLocalizedControlType}")
		startRange.MoveEndpointByRange(
			UIAHandler.TextPatternRangeEndpoint_End,
			enclosingRange,
			UIAHandler.TextPatternRangeEndpoint_End
		)
		if 0 < startRange.CompareEndpoints(
			UIAHandler.TextPatternRangeEndpoint_End,
			textRange,
			UIAHandler.TextPatternRangeEndpoint_End
		):
			startRange.MoveEndpointByRange(
				UIAHandler.TextPatternRangeEndpoint_End,
				textRange,
				UIAHandler.TextPatternRangeEndpoint_End
			)
		# Ensure we don't now have a collapsed range
		if 0 >= startRange.CompareEndpoints(
			UIAHandler.TextPatternRangeEndpoint_End,
			startRange,
			UIAHandler.TextPatternRangeEndpoint_Start
		):
			log.debug("Collapsed range. Returning")
			return
		# check for an embedded child
		childElements = getChildrenWithCacheFromUIATextRange(startRange, self._controlFieldUIACacheRequest)
		if (
			childElements.length == 1
			and UIAHandler.handler.clientObject.compareElements(
				rootElement,
				childElements.getElement(0)
			)
		):
			log.debug("Using single embedded child as enclosingElement")
			for field in super(EdgeTextInfo, self)._getTextWithFieldsForUIARange(
				rootElement,
				startRange,
				formatConfig,
				_rootElementClipped=_rootElementClipped,
				includeRoot=includeRoot,
				alwaysWalkAncestors=False,
				recurseChildren=False
			):
				yield field
			return
		parents = []
		parentElement = enclosingElement
		log.debug("Generating ancestors:")
		hasAncestors = False
		while parentElement:
			if log.isEnabledFor(log.DEBUG):
				log.debug(f"parentElement: {parentElement.currentLocalizedControlType}")
			isRoot = UIAHandler.handler.clientObject.compareElements(parentElement, rootElement)
			log.debug(f"isRoot: {isRoot}")
			if not isRoot:
				hasAncestors = True
			if parentElement is not enclosingElement:
				if includeRoot or not isRoot:
					try:
						obj = UIA(
							windowHandle=self.obj.windowHandle,
							UIAElement=parentElement,
							initialUIACachedPropertyIDs=self._controlFieldUIACachedPropertyIDs
						)
						field = self._getControlFieldForUIAObject(obj)
					except LookupError:
						log.debug("Failed to fetch controlField data for parentElement. Breaking")
						break
					parents.append((parentElement, field))
				else:
					# This is the root but it was not requested for inclusion
					# However we still need the root element itself for further recursion
					parents.append((parentElement, None))
			if isRoot:
				log.debug("Hit root. Breaking")
				break
			log.debug("Fetching next parentElement")
			parentElement = UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(
				parentElement,
				self._controlFieldUIACacheRequest
			)
		log.debug("Done generating parents")
		log.debug("Yielding parents in reverse order")
		for parentElement, field in reversed(parents):
			if field:
				yield textInfos.FieldCommand("controlStart", field)
		log.debug("Done yielding parents")
		log.debug("Yielding balanced fields for startRange")
		clippedStart = 0 > enclosingRange.CompareEndpoints(
			UIAHandler.TextPatternRangeEndpoint_Start,
			startRange,
			UIAHandler.TextPatternRangeEndpoint_Start
		)
		clippedEnd = 0 < enclosingRange.CompareEndpoints(
			UIAHandler.TextPatternRangeEndpoint_End,
			startRange,
			UIAHandler.TextPatternRangeEndpoint_End
		)
		for field in super(EdgeTextInfo, self)._getTextWithFieldsForUIARange(
			enclosingElement,
			startRange,
			formatConfig,
			_rootElementClipped=(clippedStart, clippedEnd),
			includeRoot=includeRoot or hasAncestors,
			alwaysWalkAncestors=False,
			recurseChildren=True
		):
			yield field
		tempRange = startRange.clone()
		log.debug("Walking parents to yield controlEnds and recurse unbalanced endRanges")
		for parentElement, field in parents:
			if log.isEnabledFor(log.DEBUG):
				log.debug(f"parentElement: {parentElement.currentLocalizedControlType}")
			tempRange.MoveEndpointByRange(
				UIAHandler.TextPatternRangeEndpoint_Start,
				tempRange,
				UIAHandler.TextPatternRangeEndpoint_End
			)
			parentRange = self.obj.getNormalizedUIATextRangeFromElement(parentElement)
			if parentRange:
				tempRange.MoveEndpointByRange(
					UIAHandler.TextPatternRangeEndpoint_End,
					parentRange,
					UIAHandler.TextPatternRangeEndpoint_End
				)
				if 0 < tempRange.CompareEndpoints(
					UIAHandler.TextPatternRangeEndpoint_End,
					textRange,
					UIAHandler.TextPatternRangeEndpoint_End
				):
					tempRange.MoveEndpointByRange(
						UIAHandler.TextPatternRangeEndpoint_End,
						textRange,
						UIAHandler.TextPatternRangeEndpoint_End
					)
					clippedEnd = True
				else:
					clippedEnd = False
				if field:
					clippedStart = 0 > parentRange.CompareEndpoints(
						UIAHandler.TextPatternRangeEndpoint_Start,
						textRange,
						UIAHandler.TextPatternRangeEndpoint_Start
					)
					field['_startOfNode'] = not clippedStart
					field['_endOfNode'] = not clippedEnd
				if 0 < tempRange.CompareEndpoints(
					UIAHandler.TextPatternRangeEndpoint_End,
					tempRange,
					UIAHandler.TextPatternRangeEndpoint_Start
				):
					log.debug("Recursing endRange")
					for endField in self._getTextWithFieldsForUIARange(
						parentElement,
						tempRange,
						formatConfig,
						_rootElementClipped=(clippedStart, clippedEnd),
						includeRoot=False,
						alwaysWalkAncestors=True,
						recurseChildren=True
					):
						yield endField
					log.debug("Done recursing endRange")
				else:
					log.debug("No content after parent")
			if field:
				log.debug("Yielding controlEnd for parent")
				yield textInfos.FieldCommand("controlEnd", field)
		log.debug("Done walking parents to yield controlEnds and recurse unbalanced endRanges")
		log.debug("_getTextWithFieldsForUIARange (unbalanced) end")


class EdgeNode(web.UIAWeb):

	_edgeIsPreGapRemoval = winVersion.getWinVer().build < 15048

	_TextInfo = EdgeTextInfo_preGapRemoval if _edgeIsPreGapRemoval else EdgeTextInfo

	def getNormalizedUIATextRangeFromElement(self, UIAElement):
		textRange = super().getNormalizedUIATextRangeFromElement(UIAElement)
		if not textRange or not self._edgeIsPreGapRemoval:
			return textRange
		# Move the start of a UIA text range past any element start character stops
		lastCharInfo = EdgeTextInfo_preGapRemoval(
			obj=self,
			position=None,
			_rangeObj=textRange
		)
		lastCharInfo._rangeObj = textRange
		charInfo = lastCharInfo.copy()
		charInfo.collapse()
		# charInfo is a EdgeTextInfo_preGapRemoval, so why is
		# EdgeTextInfo.move used instead of
		# EdgeTextInfo_preGapRemoval.move?
		while 0 != super(EdgeTextInfo, charInfo).move(
			textInfos.UNIT_CHARACTER,
			1
		):
			charInfo.setEndPoint(lastCharInfo, "startToStart")
			if charInfo.text or charInfo._hasEmbedded():
				break
			lastCharInfo.setEndPoint(charInfo, "startToEnd")
			charInfo.collapse(True)
		return textRange

	def _get__isTextEmpty(self):
		# NOTE: we can not check the result of the EdgeTextInfo move implementation to determine if we added
		# any characters to the range, since it seems to return 1 even when the text property has not changed.
		# Also we can not move (repeatedly by one character) since this can overrun the end of the field in edge.
		# So instead, we use self to make a text info (which should have the right range) and then use the UIA
		# specific _rangeObj.getText function to get a subset of the full range of characters.
		ti = self.makeTextInfo(self)
		if ti.isCollapsed:
			# it is collapsed therefore it is empty.
			# exit early so we do not have to do not have to fetch `ti.text` which
			# is potentially costly to performance.
			return True
		numberOfCharacters = 2
		text = ti._rangeObj.getText(numberOfCharacters)
		# Edge can report newline for empty fields:
		if text == "\n":
			return True
		return False


class EdgeList(web.List):
	...


class EdgeHTMLRootContainer(EdgeNode):

	def event_gainFocus(self):
		firstChild = self.firstChild
		if isinstance(firstChild, UIA):
			eventHandler.executeEvent("gainFocus", firstChild)
			return
		return super().event_gainFocus()


class EdgeHTMLTreeInterceptor(web.UIAWebTreeInterceptor):

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent.name


class EdgeHTMLRoot(EdgeNode):

	treeInterceptorClass = EdgeHTMLTreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role == controlTypes.Role.DOCUMENT

	def _isIframe(self):
		"""Override, the root node is never an iFrame"""
		return False

	def _get_role(self):
		role = super().role
		if role == controlTypes.Role.PANE:
			role = controlTypes.Role.DOCUMENT
		return role
