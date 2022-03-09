# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2021 NV Access Limited, Babbage B.V., Leonard de Ruijter
from typing import (
	Optional,
	Dict,
)

from comtypes import COMError
from comtypes.automation import VARIANT
from ctypes import byref

import textUtils
from . import (
	UIATextInfo,
	UIA,
)

from logHandler import log
import controlTypes
import cursorManager
import re
import aria
import textInfos
from UIAHandler.browseMode import (
	UIABrowseModeDocument,
	UIABrowseModeDocumentTextInfo,
	UIATextRangeQuickNavItem,
	UIAControlQuicknavIterator,
)
from UIAHandler.utils import (
	createUIAMultiPropertyCondition,
	getUIATextAttributeValueFromRange,
)
import UIAHandler

"""
UIA.web module provides a common base for behavior and utilities relevant to web browsers.
There are specialisations for families of browsers and further specialisations for individual browsers where
necessary. Note that not all browsers support UIA.
"""


def splitUIAElementAttribs(attribsString):
	"""Split an UIA Element attributes string into a dict of attribute keys and values.
	An invalid attributes string does not cause an error, but strange results may be returned.
	@param attribsString: The UIA Element attributes string to convert.
	@type attribsString: str
	@return: A dict of the attribute keys and values, where values are strings
	@rtype: {str: str}
	"""
	attribsDict = {}
	tmp = ""
	key = ""
	inEscape = False
	for char in attribsString:
		if inEscape:
			tmp += char
			inEscape = False
		elif char == "\\":
			inEscape = True
		elif char == "=":
			# We're about to move on to the value, so save the key and clear tmp.
			key = tmp
			tmp = ""
		elif char == ";":
			# We're about to move on to a new attribute.
			if key:
				# Add this key/value pair to the dict.
				attribsDict[key] = tmp
			key = ""
			tmp = ""
		else:
			tmp += char
	# If there was no trailing semi-colon, we need to handle the last attribute.
	if key:
		# Add this key/value pair to the dict.
		attribsDict[key] = tmp
	return attribsDict


class UIAWebTextInfo(UIATextInfo):

	def _get_UIAElementAtStartWithReplacedContent(self):
		"""Fetches the deepest UIAElement at the start of the text range
		whose name has been overridden by the author (such as aria-label).
		"""
		element = self.UIAElementAtStart
		condition = createUIAMultiPropertyCondition(
			{
				UIAHandler.UIA_ControlTypePropertyId: self.UIAControlTypesWhereNameIsContent
			},
			{
				UIAHandler.UIA_ControlTypePropertyId: UIAHandler.UIA_ListControlTypeId,
				UIAHandler.UIA_IsKeyboardFocusablePropertyId: True,
			}
		)
		# A part from the condition given, we must always match on the root of the document
		# so we know when to stop walking
		runtimeID = VARIANT()
		self.obj.UIAElement._IUIAutomationElement__com_GetCurrentPropertyValue(
			UIAHandler.UIA_RuntimeIdPropertyId,
			byref(runtimeID)
		)
		condition = UIAHandler.handler.clientObject.createOrCondition(
			UIAHandler.handler.clientObject.createPropertyCondition(
				UIAHandler.UIA_RuntimeIdPropertyId,
				runtimeID
			),
			condition
		)
		walker = UIAHandler.handler.clientObject.createTreeWalker(condition)
		cacheRequest = UIAHandler.handler.clientObject.createCacheRequest()
		cacheRequest.addProperty(UIAHandler.UIA_ControlTypePropertyId)
		cacheRequest.addProperty(UIAHandler.UIA_IsKeyboardFocusablePropertyId)
		cacheRequest.addProperty(UIAHandler.UIA_NamePropertyId)
		cacheRequest.addProperty(UIAHandler.UIA_AriaPropertiesPropertyId)
		element = walker.normalizeElementBuildCache(element, cacheRequest)
		while element and not UIAHandler.handler.clientObject.compareElements(element, self.obj.UIAElement):
			# Interactive lists
			controlType = element.getCachedPropertyValue(UIAHandler.UIA_ControlTypePropertyId)
			if controlType == UIAHandler.UIA_ListControlTypeId:
				isFocusable = element.getCachedPropertyValue(UIAHandler.UIA_IsKeyboardFocusablePropertyId)
				if isFocusable:
					return element
			# Nodes with an aria label or labelledby attribute
			name = element.getCachedPropertyValue(UIAHandler.UIA_NamePropertyId)
			if name:
				ariaProperties = element.getCachedPropertyValue(UIAHandler.UIA_AriaPropertiesPropertyId)
				if ('label=' in ariaProperties) or ('labelledby=' in ariaProperties):
					return element
				try:
					textRange = self.obj.UIATextPattern.rangeFromChild(element)
				except COMError:
					return
				text = textRange.getText(-1)
				if not text or text.isspace():
					return element
			element = walker.getParentElementBuildCache(element, cacheRequest)

	def _moveToEdgeOfReplacedContent(self, back=False):
		"""If within replaced content (E.g. aria-label is used),
		moves to the first or last character covered, so that a following call to move in the same direction
		will move out of the replaced content, in order to ensure
		that the content only takes up one character stop.
		"""
		element = self.UIAElementAtStartWithReplacedContent
		if not element:
			return
		try:
			textRange = self.obj.UIATextPattern.rangeFromChild(element)
		except COMError:
			return
		if not back:
			textRange.MoveEndpointByRange(
				UIAHandler.TextPatternRangeEndpoint_Start,
				textRange,
				UIAHandler.TextPatternRangeEndpoint_End
			)
			textRange.move(UIAHandler.TextUnit_Character, -1)
		else:
			textRange.MoveEndpointByRange(
				UIAHandler.TextPatternRangeEndpoint_End,
				textRange,
				UIAHandler.TextPatternRangeEndpoint_Start
			)
		self._rangeObj = textRange

	def _collapsedMove(self, unit, direction, skipReplacedContent):
		"""A simple collapsed move (i.e. both ends move together),
		but whether it classes replaced content as one character stop
		can be configured via the skipReplacedContent argument."""
		if not skipReplacedContent:
			return super().move(unit, direction)
		if direction == 0:
			return
		chunk = 1 if direction > 0 else -1
		finalRes = 0
		while finalRes != direction:
			self._moveToEdgeOfReplacedContent(back=direction < 0)
			res = super().move(unit, chunk)
			if res == 0:
				break
			finalRes += res
		return finalRes

	def move(self, unit, direction, endPoint=None, skipReplacedContent=True):
		if not endPoint:
			return self._collapsedMove(unit, direction, skipReplacedContent)
		else:
			tempInfo = self.copy()
			res = tempInfo.move(unit, direction, skipReplacedContent=skipReplacedContent)
			if res != 0:
				self.setEndPoint(tempInfo, "endToEnd" if endPoint == "end" else "startToStart")
			return res

	def _getControlFieldForUIAObject(self, obj, isEmbedded=False, startOfNode=False, endOfNode=False):
		field = super()._getControlFieldForUIAObject(
			obj,
			isEmbedded=isEmbedded,
			startOfNode=startOfNode,
			endOfNode=endOfNode
		)
		field['embedded'] = isEmbedded
		role = field.get('role')
		# Fields should be treated as block for certain roles.
		# This can affect whether the field is presented as a container (e.g.  announcing entering and exiting)
		if role in (
			controlTypes.Role.GROUPING,
			controlTypes.Role.SECTION,
			controlTypes.Role.PARAGRAPH,
			controlTypes.Role.ARTICLE,
			controlTypes.Role.LANDMARK,
			controlTypes.Role.REGION,
		):
			field['isBlock'] = True
		ariaProperties = splitUIAElementAttribs(
			obj._getUIACacheablePropertyValue(UIAHandler.UIA_AriaPropertiesPropertyId)
		)
		# ARIA roledescription and landmarks
		field['roleText'] = ariaProperties.get('roledescription')
		# provide landmarks
		field['landmark'] = obj.landmark
		# Combo boxes with a text pattern are editable
		if obj.role == controlTypes.Role.COMBOBOX and obj.UIATextPattern:
			field['states'].add(controlTypes.State.EDITABLE)
		# report if the field is 'current'
		field['current'] = obj.isCurrent
		if obj.placeholder and obj._isTextEmpty:
			field['placeholder'] = obj.placeholder
		# For certain controls, if ARIA overrides the label, then force the field's content (value) to the label
		# Later processing in getTextWithFields will remove descendant content from fields
		# with a content attribute.
		hasAriaLabel = 'label' in ariaProperties
		hasAriaLabelledby = 'labelledby' in ariaProperties
		if field.get('nameIsContent'):
			content = ""
			field.pop('name', None)
			if hasAriaLabel or hasAriaLabelledby:
				content = obj.name
			if not content:
				text = self.obj.makeTextInfo(obj).text
				# embedded object characters (which can appear in Edgium)
				# should also be treated as whitespace
				# allowing to be replaced by an overridden label
				text = text.replace(textUtils.OBJ_REPLACEMENT_CHAR, '')
				if not text or text.isspace():
					content = obj.name or field.pop('description', None)
			if content:
				field['content'] = content
		elif isEmbedded:
			field['content'] = obj.value
			if field['role'] == controlTypes.Role.GROUPING:
				field['role'] = controlTypes.Role.EMBEDDEDOBJECT
				if not obj.value:
					field['content'] = obj.name
		elif hasAriaLabel or hasAriaLabelledby:
			field['alwaysReportName'] = True
		# Give lists an item count
		if obj.role == controlTypes.Role.LIST:
			child = UIAHandler.handler.clientObject.ControlViewWalker.GetFirstChildElement(obj.UIAElement)
			if child:
				field['_childcontrolcount'] = child.getCurrentPropertyValue(UIAHandler.UIA_SizeOfSetPropertyId)
		return field

	# C901 'getTextWithFields' is too complex
	# Note: when working on getTextWithFields, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def getTextWithFields(  # noqa: C901
		self,
		formatConfig: Optional[Dict] = None
	) -> textInfos.TextInfo.TextWithFieldsT:
		# We don't want fields for collapsed ranges.
		# This would normally be a general rule, but MS Word currently needs fields for collapsed ranges,
		# thus this code is not in the base.
		if self.isCollapsed:
			return []
		fields = super().getTextWithFields(formatConfig)
		# remove clickable state on descendants of controls with clickable state
		clickableField = None
		for field in fields:
			if isinstance(field, textInfos.FieldCommand) and field.command == "controlStart":
				states = field.field['states']
				if clickableField:
					states.discard(controlTypes.State.CLICKABLE)
				elif controlTypes.State.CLICKABLE in states:
					clickableField = field.field
			elif (
				clickableField
				and isinstance(field, textInfos.FieldCommand)
				and field.command == "controlEnd"
				and field.field is clickableField
			):
				clickableField = None
		# Chop extra whitespace off the end incorrectly put there by Edge
		numFields = len(fields)
		index = 0
		while index < len(fields):
			field = fields[index]
			if index > 1 and isinstance(field, str) and field.isspace():
				prevField = fields[index - 2]
				if isinstance(prevField, textInfos.FieldCommand) and prevField.command == "controlEnd":
					del fields[index - 1:index + 1]
			index += 1
		# chop fields off the end incorrectly placed there by Edge
		# This can happen if expanding to line covers element start chars at its end
		startCount = 0
		lastStartIndex = None
		numFields = len(fields)
		for index in range(numFields - 1, -1, -1):
			field = fields[index]
			if isinstance(field, str):
				break
			elif (
				isinstance(field, textInfos.FieldCommand)
				and field.command == "controlStart"
				and not field.field.get('embedded')
			):
				startCount += 1
				lastStartIndex = index
		if lastStartIndex:
			del fields[lastStartIndex: lastStartIndex + (startCount * 2)]
		# Remove any content from fields with a content attribute
		numFields = len(fields)
		curField = None
		for index in range(numFields - 1, -1, -1):
			field = fields[index]
			if (
				not curField
				and isinstance(field, textInfos.FieldCommand)
				and field.command == "controlEnd"
				and field.field.get('content')
			):
				curField = field.field
				endIndex = index
			elif (
				curField
				and isinstance(field, textInfos.FieldCommand)
				and field.command == "controlStart"
				and field.field is curField
			):
				fields[index + 1: endIndex] = " "
				curField = None
		return fields


class UIAWeb(UIA):

	_TextInfo = UIAWebTextInfo

	def _isIframe(self):
		role = super().role
		return (
			role == controlTypes.Role.PANE
			and self.UIATextPattern
		)

	def _get_role(self):
		if self._isIframe():
			return controlTypes.Role.INTERNALFRAME
		ariaRole = self._getUIACacheablePropertyValue(UIAHandler.UIA_AriaRolePropertyId).lower()
		# #7333: It is valid to provide multiple, space separated aria roles in HTML
		# The role used is the first role in the list that has an associated NVDA role in aria.ariaRolesToNVDARoles
		for ariaRole in ariaRole.split():
			newRole = aria.ariaRolesToNVDARoles.get(ariaRole)
			if newRole:
				return newRole
		return super().role

	def _get_states(self):
		states = super().states
		if self.role in (
			controlTypes.Role.STATICTEXT,
			controlTypes.Role.GROUPING,
			controlTypes.Role.SECTION,
			controlTypes.Role.GRAPHIC,
		) and self.UIAInvokePattern:
			states.add(controlTypes.State.CLICKABLE)
		return states

	def _get_ariaProperties(self):
		return splitUIAElementAttribs(self.UIAElement.currentAriaProperties)

	# RegEx to get the value for the aria-current property. This will be looking for a the value of 'current'
	# in a list of strings like "something=true;current=date;". We want to capture one group, after the '='
	# character and before the ';' character.
	# This could be one of: "false", "true", "page", "step", "location", "date", "time"
	# "false" is ignored by the regEx and will not produce a match
	RE_ARIA_CURRENT_PROP_VALUE = re.compile(r"current=(?!false)(\w+);")

	def _get_isCurrent(self) -> controlTypes.IsCurrent:
		ariaProperties = self._getUIACacheablePropertyValue(UIAHandler.UIA_AriaPropertiesPropertyId)
		match = self.RE_ARIA_CURRENT_PROP_VALUE.search(ariaProperties)
		if match:
			valueOfAriaCurrent = match.group(1)
			try:
				return controlTypes.IsCurrent(valueOfAriaCurrent)
			except ValueError:
				log.debugWarning(
					f"Unknown aria-current value: {valueOfAriaCurrent}, ariaProperties: {ariaProperties}"
				)
		return controlTypes.IsCurrent.NO

	def _get_roleText(self):
		roleText = self.ariaProperties.get('roledescription', None)
		if roleText:
			return roleText
		return super().roleText

	def _get_placeholder(self):
		ariaPlaceholder = self.ariaProperties.get('placeholder', None)
		return ariaPlaceholder

	def _get_landmark(self):
		landmarkId = self._getUIACacheablePropertyValue(UIAHandler.UIA_LandmarkTypePropertyId)
		if not landmarkId:  # will be 0 for non-landmarks
			return None
		landmarkRole = UIAHandler.UIALandmarkTypeIdsToLandmarkNames.get(landmarkId)
		if landmarkRole:
			return landmarkRole
		ariaRoles = self._getUIACacheablePropertyValue(UIAHandler.UIA_AriaRolePropertyId).lower()
		# #7333: It is valid to provide multiple, space separated aria roles in HTML
		# If multiple roles or even multiple landmark roles are provided, the first one is used
		ariaRole = ariaRoles.split(" ")[0]
		if ariaRole in aria.landmarkRoles and (ariaRole != 'region' or self.name):
			return ariaRole
		return None


class List(UIAWeb):

	# non-focusable lists are readonly lists (ensures correct NVDA presentation category)
	def _get_states(self):
		states = super().states
		if controlTypes.State.FOCUSABLE not in states:
			states.add(controlTypes.State.READONLY)
		return states


class HeadingControlQuickNavItem(UIATextRangeQuickNavItem):

	@property
	def level(self):
		if not hasattr(self, '_level'):
			styleVal = getUIATextAttributeValueFromRange(self.textInfo._rangeObj, UIAHandler.UIA_StyleIdAttributeId)
			if UIAHandler.StyleId_Heading1 <= styleVal <= UIAHandler.StyleId_Heading6:
				self._level = styleVal - (UIAHandler.StyleId_Heading1 - 1)
			else:
				self._level = None
		return self._level

	def isChild(self, parent):
		return self.level > parent.level


def HeadingControlQuicknavIterator(itemType, document, position, direction="next"):
	"""
	A helper for L{UIAWebTreeInterceptor._iterNodesByType}
	that specifically yields L{HeadingControlQuickNavItem} objects
	found in the given document, starting the search from the given position,  searching in the given direction.
	See L{browseMode._iterNodesByType} for details on these specific arguments.
	"""
	# Some UI Automation web implementations expose all headings as UIA elements
# 	with a controlType of text, and a level.
	# Thus we can quickly search for these.
	# However, sometimes when ARIA is used,
	# the level on the element may not match the level in the text attributes.
	# Therefore we need to search for all levels 1 through 6,
	# even if a specific level is specified.
	# Though this is still much faster than searching text attributes alone
	# #9078: this must be wrapped inside a list, as Python 3 will treat this as iteration.
	levels = list(range(1, 7))
	condition = createUIAMultiPropertyCondition({
		UIAHandler.UIA_ControlTypePropertyId: UIAHandler.UIA_TextControlTypeId,
		UIAHandler.UIA_LevelPropertyId: levels
	})
	levelString = itemType[7:]
	itemIter = UIAControlQuicknavIterator(
		itemType, document, position, condition, direction=direction, itemClass=HeadingControlQuickNavItem
	)
	for item in itemIter:
		# Verify this is the correct heading level via text attributes
		if item.level and (not levelString or levelString == str(item.level)):
			yield item


class UIAWebTreeInterceptor(cursorManager.ReviewCursorManager, UIABrowseModeDocument):
	TextInfo = UIABrowseModeDocumentTextInfo

	def makeTextInfo(self, position):
		try:
			return super().makeTextInfo(position)
		except RuntimeError as e:
			# sometimes the stored TextRange we have for the caret/selection can die if the page mutates too much.
			# Therefore, if we detect this, just give back the first position in the document,
			# updating our stored version as we go.
			if position in (textInfos.POSITION_SELECTION, textInfos.POSITION_CARET):
				log.debugWarning(f"{position} died. Using first position instead")
				info = self.makeTextInfo(textInfos.POSITION_FIRST)
				self._selection = info
				return info
			raise e

	def shouldPassThrough(self, obj, reason=None):
		# Enter focus mode for selectable list items (<select> and role=listbox)
		if (
			reason == controlTypes.OutputReason.FOCUS
			and obj.role == controlTypes.Role.LISTITEM
			and controlTypes.State.SELECTABLE in obj.states
		):
			return True
		return super().shouldPassThrough(obj, reason=reason)

	def _iterNodesByType(self, nodeType, direction="next", pos=None):
		if nodeType.startswith("heading"):
			return HeadingControlQuicknavIterator(nodeType, self, pos, direction=direction)
		else:
			return super()._iterNodesByType(nodeType, direction=direction, pos=pos)
