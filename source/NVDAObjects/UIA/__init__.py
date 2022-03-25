# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2009-2022 NV Access Limited, Joseph Lee, Mohammad Suliman,
# Babbage B.V., Leonard de Ruijter, Bill Dengler

"""Support for UI Automation (UIA) controls."""
import typing
from typing import (
	Optional,
	Dict,
)
from ctypes import byref
from ctypes.wintypes import POINT, RECT
from comtypes import COMError
from comtypes.automation import VARIANT
import time
import weakref
import numbers
import colors
import languageHandler
import UIAHandler
import UIAHandler.customProps
import UIAHandler.customAnnotations
import globalVars
import eventHandler
import controlTypes
from controlTypes import TextPosition
import config
import speech
import api
import textInfos
from logHandler import log
from UIAHandler.utils import (
	BulkUIATextRangeAttributeValueFetcher,
	UIATextRangeAttributeValueFetcher,
	getChildrenWithCacheFromUIATextRange,
	getEnclosingElementWithCacheFromUIATextRange,
	iterUIARangeByUnit,
	UIAMixedAttributeError,
	UIATextRangeFromElement,
)
from NVDAObjects.window import Window
from NVDAObjects import NVDAObjectTextInfo, InvalidNVDAObject
from NVDAObjects.behaviors import (
	ProgressBar,
	EditableTextWithoutAutoSelectDetection,
	EditableTextWithAutoSelectDetection,
	Dialog,
	Notification,
	EditableTextWithSuggestions,
	ToolTip
)
import braille
import locationHelper
import ui
import winVersion


paragraphIndentIDs = {
	UIAHandler.UIA_IndentationFirstLineAttributeId,
	UIAHandler.UIA_IndentationLeadingAttributeId,
	UIAHandler.UIA_IndentationTrailingAttributeId,
}


class UIATextInfo(textInfos.TextInfo):

	_cache_controlFieldNVDAObjectClass=True
	def _get_controlFieldNVDAObjectClass(self):
		"""
		The NVDAObject class to be used by the _getTextWithFieldsForUIARange method when instantiating NVDAObjects in order to generate control fields for content.
		L{UIA} is usually what you want, but if you know the class will always mutate to a certain subclass (E.g. WordDocumentNode) then performance gains can be made by returning the subclass here.
		"""
		return UIA

	# UIA property IDs that should be automatically cached for control fields
	_controlFieldUIACachedPropertyIDs={
		UIAHandler.UIA_IsValuePatternAvailablePropertyId,
		UIAHandler.UIA_HasKeyboardFocusPropertyId,
		UIAHandler.UIA_NamePropertyId,
		UIAHandler.UIA_ToggleToggleStatePropertyId,
		UIAHandler.UIA_HelpTextPropertyId,
		UIAHandler.UIA.UIA_FullDescriptionPropertyId,
		UIAHandler.UIA_AccessKeyPropertyId,
		UIAHandler.UIA_AcceleratorKeyPropertyId,
		UIAHandler.UIA_HasKeyboardFocusPropertyId,
		UIAHandler.UIA_SelectionItemIsSelectedPropertyId,
		UIAHandler.UIA_IsDataValidForFormPropertyId,
		UIAHandler.UIA_IsRequiredForFormPropertyId,
		UIAHandler.UIA_ValueIsReadOnlyPropertyId,
		UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,
		UIAHandler.UIA_ToggleToggleStatePropertyId,
		UIAHandler.UIA_IsKeyboardFocusablePropertyId,
		UIAHandler.UIA_IsPasswordPropertyId,
		UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId,
		UIAHandler.UIA_GridItemRowPropertyId,
		UIAHandler.UIA_TableItemRowHeaderItemsPropertyId,
		UIAHandler.UIA_GridItemColumnPropertyId,
		UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId,
		UIAHandler.UIA_GridRowCountPropertyId,
		UIAHandler.UIA_GridColumnCountPropertyId,
		UIAHandler.UIA_GridItemContainingGridPropertyId,
		UIAHandler.UIA_RangeValueValuePropertyId,
		UIAHandler.UIA_ValueValuePropertyId,
		UIAHandler.UIA_PositionInSetPropertyId,
		UIAHandler.UIA_SizeOfSetPropertyId,
		UIAHandler.UIA_AriaRolePropertyId,
		UIAHandler.UIA_LandmarkTypePropertyId,
		UIAHandler.UIA_AriaPropertiesPropertyId,
		UIAHandler.UIA_LevelPropertyId,
		UIAHandler.UIA_IsEnabledPropertyId,
	}

	def _get__controlFieldUIACacheRequest(self):
		""" The UIA cacheRequest object that will be used when fetching all UIA elements needed when generating control fields for this TextInfo's content."""
		cacheRequest=UIAHandler.handler.baseCacheRequest.clone()
		for ID in self._controlFieldUIACachedPropertyIDs:
			try:
				cacheRequest.addProperty(ID)
			except COMError:
				pass
		UIATextInfo._controlFieldUIACacheRequest=self._controlFieldUIACacheRequest=cacheRequest
		return cacheRequest

	#: The UI Automation text units (in order of resolution) that should be used when fetching formatting.
	UIAFormatUnits=[
		UIAHandler.TextUnit_Format,
		UIAHandler.TextUnit_Word,
		UIAHandler.TextUnit_Character
	]

	def find(self,text,caseSensitive=False,reverse=False):
		tempRange=self._rangeObj.clone()
		documentRange=self.obj.UIATextPattern.documentRange
		if reverse:
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,documentRange,UIAHandler.TextPatternRangeEndpoint_Start)
		else:
			if tempRange.move(UIAHandler.TextUnit_Character,1)==0:
				return False
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,documentRange,UIAHandler.TextPatternRangeEndpoint_End)
		try:
			r=tempRange.findText(text,reverse,not caseSensitive)
		except COMError:
			r=None
		if r:
			r.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,r,UIAHandler.TextPatternRangeEndpoint_Start)
			self._rangeObj=r
			return True
		return False

	def _getFormatFieldAtRange(self,textRange,formatConfig,ignoreMixedValues=False):
		"""
		Fetches formatting for the given UI Automation Text range.
		@param textRange: the text range whos formatting should be fetched.
		@type textRange: L{UIAutomation.IUIAutomationTextRange}
		@param formatConfig: the types of formatting requested.
		@type formatConfig: a dictionary of NVDA document formatting configuration keys
			with values set to true for those types that should be fetched.
		@param ignoreMixedValues: If True, formatting that is mixed according to UI Automation will not be included.
			If False, L{UIAHandler.utils.MixedAttributeError} will be raised if UI Automation gives back
			a mixed attribute value signifying that the caller may want to try again with a smaller range.
		@type: bool
		@return: The formatting for the given text range.
		@rtype: L{textInfos.FormatField}
		"""
		formatField=textInfos.FormatField()
		if not isinstance(textRange,UIAHandler.IUIAutomationTextRange):
			raise ValueError("%s is not a text range"%textRange)
		fetchAnnotationTypes = (
			formatConfig["reportSpellingErrors"]
			or formatConfig["reportComments"]
			or formatConfig["reportRevisions"]
			or formatConfig["reportBookmarks"]
		)
		try:
			textRange=textRange.QueryInterface(UIAHandler.IUIAutomationTextRange3)
		except (COMError,AttributeError):
			fetcher=UIATextRangeAttributeValueFetcher(textRange)
		else:
			# Precalculate all the IDs we could possibly need so that they can be fetched in one cross-process call where supported
			IDs=set()
			if formatConfig["reportFontName"]:
				IDs.add(UIAHandler.UIA_FontNameAttributeId)
			if formatConfig["reportFontSize"]:
				IDs.add(UIAHandler.UIA_FontSizeAttributeId)
			if formatConfig["reportFontAttributes"]:
				IDs.update({
					UIAHandler.UIA_FontWeightAttributeId,
					UIAHandler.UIA_IsItalicAttributeId,
					UIAHandler.UIA_UnderlineStyleAttributeId,
					UIAHandler.UIA_StrikethroughStyleAttributeId
				})
			if formatConfig["reportSuperscriptsAndSubscripts"]:
				IDs.update({
					UIAHandler.UIA_IsSuperscriptAttributeId,
					UIAHandler.UIA_IsSubscriptAttributeId
				})
			if formatConfig["reportParagraphIndentation"]:
				IDs.update(set(paragraphIndentIDs))
			if formatConfig["reportAlignment"]:
				IDs.add(UIAHandler.UIA_HorizontalTextAlignmentAttributeId)
			if formatConfig["reportColor"]:
				IDs.add(UIAHandler.UIA_BackgroundColorAttributeId)
				IDs.add(UIAHandler.UIA_ForegroundColorAttributeId)
			if formatConfig['reportLineSpacing']:
				IDs.add(UIAHandler.UIA_LineSpacingAttributeId)
			if formatConfig['reportLinks']:
				IDs.add(UIAHandler.UIA_LinkAttributeId)
			if formatConfig['reportStyle']:
				IDs.add(UIAHandler.UIA_StyleNameAttributeId)
			if formatConfig["reportHeadings"]:
				IDs.add(UIAHandler.UIA_StyleIdAttributeId)
			if fetchAnnotationTypes:
				IDs.add(UIAHandler.UIA_AnnotationTypesAttributeId)
			IDs.add(UIAHandler.UIA_CultureAttributeId)
			fetcher=BulkUIATextRangeAttributeValueFetcher(textRange,IDs)
		if formatConfig["reportFontName"]:
			val=fetcher.getValue(UIAHandler.UIA_FontNameAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField["font-name"]=val
		if formatConfig["reportFontSize"]:
			val=fetcher.getValue(UIAHandler.UIA_FontSizeAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,numbers.Number):
				formatField['font-size']="%g pt"%float(val)
		if formatConfig["reportFontAttributes"]:
			val=fetcher.getValue(UIAHandler.UIA_FontWeightAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,int):
				formatField['bold']=(val>=700)
			val=fetcher.getValue(UIAHandler.UIA_IsItalicAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['italic']=val
			val=fetcher.getValue(UIAHandler.UIA_UnderlineStyleAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['underline']=bool(val)
			val=fetcher.getValue(UIAHandler.UIA_StrikethroughStyleAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['strikethrough']=bool(val)
		if formatConfig["reportSuperscriptsAndSubscripts"]:
			textPosition=None
			val=fetcher.getValue(UIAHandler.UIA_IsSuperscriptAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue and val:
				textPosition = TextPosition.SUPERSCRIPT
			else:
				val=fetcher.getValue(UIAHandler.UIA_IsSubscriptAttributeId,ignoreMixedValues=ignoreMixedValues)
				if val!=UIAHandler.handler.reservedNotSupportedValue and val:
					textPosition = TextPosition.SUBSCRIPT
				else:
					textPosition = TextPosition.BASELINE
			formatField['text-position'] = textPosition
		if formatConfig['reportStyle']:
			val=fetcher.getValue(UIAHandler.UIA_StyleNameAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField["style"]=val
		if formatConfig["reportParagraphIndentation"]:
			formatField.update(self._getFormatFieldIndent(fetcher, ignoreMixedValues=ignoreMixedValues))
		if formatConfig["reportAlignment"]:
			val=fetcher.getValue(UIAHandler.UIA_HorizontalTextAlignmentAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val==UIAHandler.HorizontalTextAlignment_Left:
				val="left"
			elif val==UIAHandler.HorizontalTextAlignment_Centered:
				val="center"
			elif val==UIAHandler.HorizontalTextAlignment_Right:
				val="right"
			elif val==UIAHandler.HorizontalTextAlignment_Justified:
				val="justify"
			else:
				val=None
			if val:
				formatField['text-align']=val
		if formatConfig["reportColor"]:
			val=fetcher.getValue(UIAHandler.UIA_BackgroundColorAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,int):
				formatField['background-color']=colors.RGB.fromCOLORREF(val)
			val=fetcher.getValue(UIAHandler.UIA_ForegroundColorAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,int):
				formatField['color']=colors.RGB.fromCOLORREF(val)
		if formatConfig['reportLineSpacing']:
			val=fetcher.getValue(UIAHandler.UIA_LineSpacingAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				if val:
					formatField['line-spacing']=val
		if formatConfig['reportLinks']:
			val=fetcher.getValue(UIAHandler.UIA_LinkAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				if val:
					formatField['link']=True
		if formatConfig["reportHeadings"]:
			styleIDValue=fetcher.getValue(UIAHandler.UIA_StyleIdAttributeId,ignoreMixedValues=ignoreMixedValues)
			# #9842: styleIDValue can sometimes be a pointer to IUnknown.
			# In Python 3, comparing an int with a pointer raises a TypeError.
			if isinstance(styleIDValue, int) and UIAHandler.StyleId_Heading1 <= styleIDValue <= UIAHandler.StyleId_Heading9:
				formatField["heading-level"] = (styleIDValue - UIAHandler.StyleId_Heading1) + 1
		if fetchAnnotationTypes:
			annotationTypes=fetcher.getValue(UIAHandler.UIA_AnnotationTypesAttributeId,ignoreMixedValues=ignoreMixedValues)
			# Some UIA implementations return a single value rather than a tuple.
			# Always mutate to a tuple to allow for a generic x in y matching 
			if not isinstance(annotationTypes,tuple):
				annotationTypes=(annotationTypes,)
			if formatConfig["reportSpellingErrors"]:
				if UIAHandler.AnnotationType_SpellingError in annotationTypes:
					formatField["invalid-spelling"]=True
				if UIAHandler.AnnotationType_GrammarError in annotationTypes:
					formatField["invalid-grammar"]=True
			if formatConfig["reportComments"]:
				cats = self.obj._UIACustomAnnotationTypes
				if cats.microsoftWord_draftComment.id and cats.microsoftWord_draftComment.id in annotationTypes:
					formatField["comment"] = textInfos.CommentType.DRAFT
				elif cats.microsoftWord_resolvedComment.id and cats.microsoftWord_resolvedComment.id in annotationTypes:
					formatField["comment"] = textInfos.CommentType.RESOLVED
				elif UIAHandler.AnnotationType_Comment in annotationTypes:
					formatField["comment"] = True
			if formatConfig["reportRevisions"]:
				if UIAHandler.AnnotationType_InsertionChange in annotationTypes:
					formatField["revision-insertion"]=True
				elif UIAHandler.AnnotationType_DeletionChange in annotationTypes:
					formatField["revision-deletion"]=True
			if formatConfig["reportBookmarks"]:
				cats = self.obj._UIACustomAnnotationTypes
				if cats.microsoftWord_bookmark.id and cats.microsoftWord_bookmark.id in annotationTypes:
					formatField["bookmark"] = True
		cultureVal=fetcher.getValue(UIAHandler.UIA_CultureAttributeId,ignoreMixedValues=ignoreMixedValues)
		if cultureVal and isinstance(cultureVal,int):
			try:
				formatField['language']=languageHandler.windowsLCIDToLocaleName(cultureVal)
			except:
				log.debugWarning("language error",exc_info=True)
				pass
		return textInfos.FieldCommand("formatChange",formatField)

	def _getFormatFieldIndent(
			self,
			fetcher: UIATextRangeAttributeValueFetcher,
			ignoreMixedValues: bool,
	) -> textInfos.FormatField:
		"""
		Helper function to get indent formatting from the fetcher passed as parameter.
		The indent formatting is reported according to MS Word's convention.
		@param fetcher: the UIA fetcher used to get all formatting information.
		@param ignoreMixedValues: If True, formatting that is mixed according to UI Automation will not be included.
			If False, L{UIAHandler.utils.MixedAttributeError} will be raised if UI Automation gives back
			a mixed attribute value signifying that the caller may want to try again with a smaller range.
		@return: The indent formatting informations corresponding to what has been retrieved via the fetcher.
		"""
		
		formatField = textInfos.FormatField()
		val = fetcher.getValue(UIAHandler.UIA_IndentationFirstLineAttributeId, ignoreMixedValues=ignoreMixedValues)
		uiaIndentFirstLine = val if isinstance(val, float) else None
		val = fetcher.getValue(UIAHandler.UIA_IndentationLeadingAttributeId, ignoreMixedValues=ignoreMixedValues)
		uiaIndentLeading = val if isinstance(val, float) else None
		val = fetcher.getValue(UIAHandler.UIA_IndentationTrailingAttributeId, ignoreMixedValues=ignoreMixedValues)
		uiaIndentTrailing = val if isinstance(val, float) else None
		if uiaIndentFirstLine is not None and uiaIndentLeading is not None:
			reportedFirstLineIndent = uiaIndentFirstLine - uiaIndentLeading
			if reportedFirstLineIndent > 0:  # First line positive indent
				reportedLeftIndent = uiaIndentLeading
				reportedHangingIndent = None
			elif reportedFirstLineIndent < 0:  # First line negative indent
				reportedLeftIndent = uiaIndentFirstLine
				reportedHangingIndent = -reportedFirstLineIndent
				reportedFirstLineIndent = None
			else:
				reportedLeftIndent = uiaIndentLeading
				reportedFirstLineIndent = None
				reportedHangingIndent = None
			if reportedLeftIndent:
				formatField['left-indent'] = self._getIndentValueDisplayString(reportedLeftIndent)
			if reportedFirstLineIndent:
				formatField['first-line-indent'] = self._getIndentValueDisplayString(reportedFirstLineIndent)
			if reportedHangingIndent:
				formatField['hanging-indent'] = self._getIndentValueDisplayString(reportedHangingIndent)
		if uiaIndentTrailing:
			formatField['right-indent'] = self._getIndentValueDisplayString(uiaIndentTrailing)
		return formatField
	
	@staticmethod
	def _getIndentValueDisplayString(val: float) -> str:
		"""A function returning the string to display in formatting info.
		@param val: an indent value measured in points, fetched via
			an UIAHandler.UIA_Indentation*AttributeId attribute.
		@return: The string used in formatting information to report the length of an indentation.
		"""
		
		# convert points to inches (1pt = 1/72 in)
		val /= 72.0
		if languageHandler.useImperialMeasurements():
			# Translators: a measurement in inches
			valText = _("{val:.2f} in").format(val=val)
		else:
			# Convert from inches to centimetres
			val *= 2.54
			# Translators: a measurement in centimetres
			valText = _("{val:.2f} cm").format(val=val)
		return valText
	
	
	def __init__(self,obj,position,_rangeObj=None):
		super(UIATextInfo,self).__init__(obj,position)
		if _rangeObj:
			try:
				self._rangeObj=_rangeObj.clone()
			except COMError:
				# IUIAutomationTextRange::clone can sometimes fail, such as in UWP account login screens
				log.debugWarning("Could not clone range",exc_info=True)
				raise RuntimeError("Could not clone range")
		elif position in (textInfos.POSITION_CARET,textInfos.POSITION_SELECTION):
			try:
				sel=self.obj.UIATextPattern.GetSelection()
			except COMError:
				raise RuntimeError("No selection available")
			if sel.length>0:
				self._rangeObj=sel.getElement(0).clone()
			else:
				raise NotImplementedError("UIAutomationTextRangeArray is empty")
			if position==textInfos.POSITION_CARET:
				self.collapse()
		elif isinstance(position,UIATextInfo): #bookmark
			self._rangeObj=position._rangeObj
		elif position==textInfos.POSITION_FIRST:
			try:
				self._rangeObj=self.obj.UIATextPattern.documentRange
			except COMError:
				# Error: first position not supported by the UIA text pattern.
				raise RuntimeError
			self.collapse()
		elif position==textInfos.POSITION_LAST:
			self._rangeObj=self.obj.UIATextPattern.documentRange
			self.collapse(True)
		elif position==textInfos.POSITION_ALL or position==self.obj:
			self._rangeObj=self.obj.UIATextPattern.documentRange
		elif isinstance(position,UIA) or isinstance(position,UIAHandler.IUIAutomationElement):
			if isinstance(position,UIA):
				position=position.UIAElement
			try:
				self._rangeObj=self.obj.UIATextPattern.rangeFromChild(position)
			except COMError:
				raise LookupError
			# sometimes rangeFromChild can return a NULL range
			if not self._rangeObj: raise LookupError
		elif isinstance(position,locationHelper.Point):
			if winVersion.getWinVer() <= winVersion.WIN7_SP1:
				# #9435: RangeFromPoint causes a freeze in UIA client library in the Windows 7 start menu!
				raise NotImplementedError("RangeFromPoint not supported on Windows 7")
			self._rangeObj=self.obj.UIATextPattern.RangeFromPoint(position.toPOINT())
		elif isinstance(position,UIAHandler.IUIAutomationTextRange):
			self._rangeObj=position.clone()
		else:
			raise ValueError("Unknown position %s"%position)

	def __eq__(self,other):
		if self is other: return True
		if self.__class__ is not other.__class__: return False
		return bool(self._rangeObj.compare(other._rangeObj))

	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	# The default hash implementation is fine for  our purposes.
	def __hash__(self):
		return super().__hash__()

	def _get_NVDAObjectAtStart(self):
		e=self.UIAElementAtStart
		if e:
			return UIA(UIAElement=e) or self.obj
		return self.obj

	def _get_UIAElementAtStart(self):
		"""
		Fetches the deepest UIA element at the start of the text range.
		This may be via UIA's getChildren (in the case of embedded controls), or GetEnClosingElement.
		"""
		tempInfo=self.copy()
		tempInfo.collapse()
		# some implementations (Edge, Word) do not correctly  class embedded objects (graphics, checkboxes) as being the enclosing element, even when the range is completely within them. Rather, they still list the object in getChildren.
		# Thus we must check getChildren before getEnclosingElement.
		tempInfo.expand(textInfos.UNIT_CHARACTER)
		tempRange=tempInfo._rangeObj
		try:
			children=getChildrenWithCacheFromUIATextRange(tempRange,UIAHandler.handler.baseCacheRequest)
		except COMError as e:
			log.debugWarning("Could not get children from UIA text range, %s"%e)
			children=None
		if children and children.length==1:
			child=children.getElement(0)
		else:
			child=getEnclosingElementWithCacheFromUIATextRange(tempRange,UIAHandler.handler.baseCacheRequest)
		return child

	def _get_bookmark(self):
		return self.copy()

	UIAControlTypesWhereNameIsContent={
		UIAHandler.UIA_ButtonControlTypeId,
		UIAHandler.UIA_HyperlinkControlTypeId,
		UIAHandler.UIA_ImageControlTypeId,
		UIAHandler.UIA_MenuItemControlTypeId,
		UIAHandler.UIA_TabItemControlTypeId,
		UIAHandler.UIA_TextControlTypeId,
		UIAHandler.UIA_SplitButtonControlTypeId
	}

	def _getControlFieldForUIAObject(
			self,
			obj: "UIA",
			isEmbedded=False,
			startOfNode=False,
			endOfNode=False
	) -> textInfos.ControlField:
		"""
		Fetch control field information for the given UIA NVDAObject.
		@param obj: the NVDAObject the control field is for.
		@param isEmbedded: True if this NVDAObject is for a leaf node (has no useful children).
		@param startOfNode: True if the control field represents the very start of this object.
		@param endOfNode: True if the control field represents the very end of this object.
		@return: The control field for this object
		"""
		role = obj.role
		field = textInfos.ControlField()
		# Ensure this controlField is unique to the object
		runtimeID=field['runtimeID']=obj.UIAElement.getRuntimeId()
		field['_startOfNode']=startOfNode
		field['_endOfNode']=endOfNode
		field["role"] = obj.role
		states = obj.states
		# The user doesn't care about certain states, as they are obvious.
		states.discard(controlTypes.State.EDITABLE)
		states.discard(controlTypes.State.MULTILINE)
		states.discard(controlTypes.State.FOCUSED)
		field["states"] = states
		field['nameIsContent']=nameIsContent=obj.UIAElement.cachedControlType in self.UIAControlTypesWhereNameIsContent
		if not nameIsContent:
			field['name']=obj.name
		field["description"] = obj.description
		field["level"] = obj.positionInfo.get("level")
		if role == controlTypes.Role.TABLE:
			field["table-id"] = runtimeID
			try:
				field["table-rowcount"] = obj.rowCount
				field["table-columncount"] = obj.columnCount
			except NotImplementedError:
				pass
		if role in (controlTypes.Role.TABLECELL, controlTypes.Role.DATAITEM,controlTypes.Role.TABLECOLUMNHEADER, controlTypes.Role.TABLEROWHEADER,controlTypes.Role.HEADERITEM):
			try:
				field["table-rownumber"] = obj.rowNumber
				field["table-rowsspanned"] = obj.rowSpan
				field["table-columnnumber"] = obj.columnNumber
				field["table-columnsspanned"] = obj.columnSpan
				field["table-id"] = obj.table.UIAElement.getRuntimeId()
				field['role']=controlTypes.Role.TABLECELL
				field['table-columnheadertext']=obj.columnHeaderText
				field['table-rowheadertext']=obj.rowHeaderText
			except NotImplementedError:
				pass
		return field

	def _getTextFromUIARange(self, textRange):
		"""
		Fetches plain text from the given UI Automation text range.
		Just calls getText(-1). This only exists to be overridden for filtering.
		"""
		return textRange.getText(-1)

	def _getTextWithFields_text(self,textRange,formatConfig,UIAFormatUnits=None):
		"""
		Yields format fields and text for the given UI Automation text range, split up by the first available UI Automation text unit that does not result in mixed attribute values.
		@param textRange: the UI Automation text range to walk.
		@type textRange: L{UIAHandler.IUIAutomationTextRange}
		@param formatConfig: the types of formatting requested.
		@type formatConfig: a dictionary of NVDA document formatting configuration keys
			with values set to true for those types that should be fetched.
		@param UIAFormatUnits: the UI Automation text units (in order of resolution) that should be used to split the text so as to avoid mixed attribute values. This is None by default.
			If the parameter is a list of 1 or more units, The range will be split by the first unit in the list, and this method will be recursively run on each subrange, with the remaining units in this list given as the value of this parameter. 
			If this parameter is an empty list, then formatting and text is fetched for the entire range, but any mixed attribute values are ignored and no splitting occures.
			If this parameter is None, text and formatting is fetched for the entire range in one go, but if mixed attribute values are found, it will split by the first unit in self.UIAFormatUnits, and run this method recursively on each subrange, providing the remaining units from self.UIAFormatUnits as the value of this parameter. 
		@type UIAFormatUnits: List of UI Automation Text Units or None
		@rtype: a Generator yielding L{textInfos.FieldCommand} objects containing L{textInfos.FormatField} objects, and text strings.
		"""
		debug = UIAHandler._isDebug() and log.isEnabledFor(log.DEBUG)
		if debug:
			log.debug("_getTextWithFields_text start")
		if UIAFormatUnits:
			unit=UIAFormatUnits[0]
			furtherUIAFormatUnits=UIAFormatUnits[1:]
		else:
			# Fetching text and formatting from the entire range will be tried once before any possible splitting.
			unit=None
			furtherUIAFormatUnits=self.UIAFormatUnits if UIAFormatUnits is None else []
		if debug:
			log.debug(
				f"Walking by unit {unit}, "
				f"with further units of: {furtherUIAFormatUnits}"
			)
		rangeIter=iterUIARangeByUnit(textRange,unit) if unit is not None else [textRange]
		for tempRange in rangeIter:
			text=self._getTextFromUIARange(tempRange) or ""
			if text is not None:
				if debug:
					log.debug("Chunk has text. Fetching formatting")
				try:
					field=self._getFormatFieldAtRange(tempRange,formatConfig,ignoreMixedValues=len(furtherUIAFormatUnits)==0)
				except UIAMixedAttributeError:
					if debug:
						log.debug("Mixed formatting. Trying higher resolution unit")
					for subfield in self._getTextWithFields_text(tempRange,formatConfig,UIAFormatUnits=furtherUIAFormatUnits):
						yield subfield
					if debug:
						log.debug("Done yielding higher resolution unit")
					continue
				if debug:
					log.debug("Yielding formatting and text")
					log.debug(f"field: {field}, text: {text}")
				if field:
					yield field
				yield text
		if debug:
			log.debug("Done _getTextWithFields_text")

	def _getTextWithFieldsForUIARange(self,rootElement,textRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True,_rootElementClipped=(True,True)):
		"""
		Yields start and end control fields, and text, for the given UI Automation text range.
		@param rootElement: the highest ancestor that encloses the given text range. This function will not walk higher than this point.
		@type rootElement: L{UIAHandler.IUIAutomation}
		@param textRange: the UI Automation text range whos content should be fetched.
		@type textRange: L{UIAHandler.IUIAutomation}
		@param formatConfig: the types of formatting requested.
		@type formatConfig: a dictionary of NVDA document formatting configuration keys
			with values set to true for those types that should be fetched.
		@param includeRoot: If true, then a control start and end will be yielded for the root element.
		@type includeRoot: bool
		@param alwaysWalkAncestors: If true then control fields will be yielded for any element enclosing the given text range, that is a descendant of the root element. If false then the root element may be  assumed to be the only ancestor.
		@type alwaysWalkAncestors: bool
		@param recurseChildren: If true, this function will be recursively called for each child of the given text range, clipped to the bounds of this text range. Formatted text between the children will also be yielded. If false, only formatted text will be yielded.
		@type recurseChildren: bool
		@param _rootElementClipped: Indicates if textRange represents all of the given rootElement,
			or is clipped at the start or end.
		@type _rootElementClipped: 2-tuple
		@rtype: A generator that yields L{textInfo.FieldCommand} objects and text strings.
		"""
		debug = UIAHandler._isDebug() and log.isEnabledFor(log.DEBUG)
		if debug:
			log.debug("_getTextWithFieldsForUIARange")
			log.debug("rootElement: %s"%rootElement.currentLocalizedControlType if rootElement else None)
			log.debug("full text: %s"%textRange.getText(-1))
		if recurseChildren:
			childElements=getChildrenWithCacheFromUIATextRange(textRange,self._controlFieldUIACacheRequest)
			# Specific check for embedded elements (checkboxes etc)
			# Calling getChildren on their childRange always gives back the same child.
			if childElements.length==1:
				childElement=childElements.getElement(0)
				if childElement and UIAHandler.handler.clientObject.compareElements(childElement,rootElement):
					log.debug("Detected embedded child")
					recurseChildren=False
		parentElements=[]
		if alwaysWalkAncestors:
			if debug:
				log.debug("Fetching parents starting from enclosingElement")
			try:
				parentElement=getEnclosingElementWithCacheFromUIATextRange(textRange,self._controlFieldUIACacheRequest)
			except COMError:
				parentElement=None
			while parentElement:
				isRoot=UIAHandler.handler.clientObject.compareElements(parentElement,rootElement)
				if isRoot:
					if debug:
						log.debug("Hit root")
					parentElements.append((parentElement,_rootElementClipped))
					break
				else:
					if debug:
						log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
					try:
						parentRange=self.obj.UIATextPattern.rangeFromChild(parentElement)
					except COMError:
						parentRange=None
					if not parentRange:
						if debug:
							log.debug("parentRange is NULL. Breaking")
						break
					clippedStart=textRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,parentRange,UIAHandler.TextPatternRangeEndpoint_Start)>0
					clippedEnd=textRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,parentRange,UIAHandler.TextPatternRangeEndpoint_End)<0
					parentElements.append((parentElement,(clippedStart,clippedEnd)))
				parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,self._controlFieldUIACacheRequest)
		else:
			parentElements.append((rootElement,_rootElementClipped))
		if debug:
			log.debug("Done fetching parents")
		enclosingElement=parentElements[0][0] if parentElements else rootElement
		if not includeRoot and parentElements:
			del parentElements[-1]
		parentFields=[]
		if debug:
			log.debug("Generating controlFields for parents")
		windowHandle=self.obj.windowHandle
		controlFieldNVDAObjectClass=self.controlFieldNVDAObjectClass
		for index,(parentElement,parentClipped) in enumerate(parentElements):
			if debug:
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			startOfNode=not parentClipped[0]
			endOfNode=not parentClipped[1]
			try:
				obj=controlFieldNVDAObjectClass(windowHandle=windowHandle,UIAElement=parentElement,initialUIACachedPropertyIDs=self._controlFieldUIACachedPropertyIDs)
				objIsEmbedded = (index == 0 and not recurseChildren)
				field = self._getControlFieldForUIAObject(
					obj,
					isEmbedded=objIsEmbedded,
					startOfNode=startOfNode,
					endOfNode=endOfNode
				)
			except LookupError:
				if debug:
					log.debug("Failed to fetch controlField data for parentElement. Breaking")
				continue
			if not field:
				continue
			parentFields.append(field)
		if debug:
			log.debug("Done generating controlFields for parents")
			log.debug("Yielding control starts for parents")
		for field in reversed(parentFields):
			yield textInfos.FieldCommand("controlStart",field)
		if debug:
			log.debug("Done yielding control starts for parents")
		del parentElements
		if debug:
			log.debug("Yielding balanced fields for textRange")
		# Move through the text range, collecting text and recursing into children
		#: This variable is used to   span lengths of plain text between child ranges as we iterate over getChildren
		childCount=childElements.length if recurseChildren else 0
		if childCount>0:
			tempRange=textRange.clone()
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)
			if debug:
				log.debug("Child count: %s"%childElements.length)
				log.debug("Walking children")
			lastChildIndex=childCount-1
			lastChildEndDelta=0
			documentTextPattern=self.obj.UIATextPattern
			rootElementControlType=rootElement.cachedControlType
			for index in range(childCount):
				childElement=childElements.getElement(index)
				if not childElement or UIAHandler.handler.clientObject.compareElements(childElement,enclosingElement):
					if debug:
						log.debug("NULL childElement. Skipping")
					continue
				if rootElementControlType==UIAHandler.UIA_DataItemControlTypeId:
					# #9090: MS Word has a rare bug where  a child of a table cell's UIA textRange can be its containing page.
					# At very least stop the infinite recursion.
					childAutomationID=childElement.cachedAutomationId or ""
					if childAutomationID.startswith('UIA_AutomationId_Word_Page_'):
						continue
				if debug:
					log.debug("Fetched child %s (%s)"%(index,childElement.currentLocalizedControlType))
				try:
					childRange=documentTextPattern.rangeFromChild(childElement)
				except COMError as e:
					if debug:
						log.debug(f"rangeFromChild failed with {e}")
					childRange=None
				if not childRange:
					if debug:
						log.debug("NULL childRange. Skipping")
					continue
				clippedStart = False
				clippedEnd = False
				if childRange.CompareEndpoints(
					UIAHandler.TextPatternRangeEndpoint_End,
					textRange,
					UIAHandler.TextPatternRangeEndpoint_Start
				) <= 0:
					if debug:
						log.debug("Child completely before textRange. Skipping")
					continue
				if childRange.CompareEndpoints(
					UIAHandler.TextPatternRangeEndpoint_Start,
					textRange,
					UIAHandler.TextPatternRangeEndpoint_End
				) >= 0:
					if debug:
						log.debug("Child at or past end of textRange. Breaking")
					break
				lastChildEndDelta = childRange.CompareEndpoints(
					UIAHandler.TextPatternRangeEndpoint_End,
					textRange,
					UIAHandler.TextPatternRangeEndpoint_End
				)
				if lastChildEndDelta > 0:
					if debug:
						log.debug(
							"textRange ended part way through the child. "
							"Crop end of childRange to fit"
						)
					childRange.MoveEndpointByRange(
						UIAHandler.TextPatternRangeEndpoint_End,
						textRange,
						UIAHandler.TextPatternRangeEndpoint_End
					)
					clippedEnd = True
				childStartDelta=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
				if childStartDelta>0:
					# plain text before this child
					tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
					if debug:
						log.debug("Plain text before child")
					for field in self._getTextWithFields_text(tempRange,formatConfig):
						yield field
				elif childStartDelta<0:
					if debug:
						log.debug(
							"textRange started part way through child. "
							"Cropping Start of child range to fit"
						)
					childRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
					clippedStart=True
				if (index==0 or index==lastChildIndex) and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)==0:
					if debug:
						log.debug("childRange is degenerate. Skipping")
					continue
				if debug:
					log.debug(f"Recursing into child {index}")
				for field in self._getTextWithFieldsForUIARange(childElement,childRange,formatConfig,includeRoot=True,alwaysWalkAncestors=False,_rootElementClipped=(clippedStart,clippedEnd)):
					yield field
				if debug:
					log.debug(f"Done recursing into child {index}")
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)
			if debug:
				log.debug("children done")
			# Plain text after the final child
			if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_End)<0:
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
				if debug:
					log.debug("Yielding final text")
				for field in self._getTextWithFields_text(tempRange,formatConfig):
					yield field
		else: #no children 
			if debug:
				log.debug("no children")
				log.debug("Yielding text")
			for field in self._getTextWithFields_text(textRange,formatConfig):
				yield field
		for field in parentFields:
			if debug:
				log.debug("Yielding controlEnd for parentElement")
			yield textInfos.FieldCommand("controlEnd",field)
		if debug:
			log.debug("_getTextWithFieldsForUIARange end")

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.TextInfo.TextWithFieldsT:
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		fields=list(self._getTextWithFieldsForUIARange(self.obj.UIAElement,self._rangeObj,formatConfig))
		return fields

	def _get_text(self):
		return self._getTextFromUIARange(self._rangeObj)

	def _getBoundingRectsFromUIARange(self, textRange):
		"""
		Fetches per line bounding rectangles from the given UI Automation text range.
		Note that if the range object doesn't cover a whole line (e.g. a character),
		the bounding rectangle will be restricted to the range.
		@rtype: [locationHelper.RectLTWH]
		"""
		rects = []
		rectArray = textRange.GetBoundingRectangles()
		if not rectArray:
			return rects
		rectIndexes = range(0, len(rectArray), 4)
		rectGen = (locationHelper.RectLTWH.fromFloatCollection(*rectArray[i:i+4]) for i in rectIndexes)
		rects.extend(rectGen)
		return rects

	def _get_boundingRects(self):
		return self._getBoundingRectsFromUIARange(self._rangeObj)

	def expand(self,unit):
		UIAUnit=UIAHandler.NVDAUnitsToUIAUnits[unit]
		self._rangeObj.ExpandToEnclosingUnit(UIAUnit)

	def move(self,unit,direction,endPoint=None):
		UIAUnit=UIAHandler.NVDAUnitsToUIAUnits[unit]
		if endPoint=="start":
			res=self._rangeObj.MoveEndpointByUnit(UIAHandler.TextPatternRangeEndpoint_Start,UIAUnit,direction)
		elif endPoint=="end":
			res=self._rangeObj.MoveEndpointByUnit(UIAHandler.TextPatternRangeEndpoint_End,UIAUnit,direction)
		else:
			res=self._rangeObj.Move(UIAUnit,direction)
		#Some Implementations of Move and moveEndpointByUnit return a positive number even if the direction is negative
		if direction<0 and res>0:
			res=0-res
		return res

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self._rangeObj)

	def collapse(self,end=False):
		if end:
			self._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,self._rangeObj,UIAHandler.TextPatternRangeEndpoint_End)
		else:
			self._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,self._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)

	def compareEndPoints(self,other,which):
		if which.startswith('start'):
			src=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			src=UIAHandler.TextPatternRangeEndpoint_End
		if which.endswith('Start'):
			target=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			target=UIAHandler.TextPatternRangeEndpoint_End
		return self._rangeObj.CompareEndpoints(src,other._rangeObj,target)

	def setEndPoint(self,other,which):
		if which.startswith('start'):
			src=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			src=UIAHandler.TextPatternRangeEndpoint_End
		if which.endswith('Start'):
			target=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			target=UIAHandler.TextPatternRangeEndpoint_End
		self._rangeObj.MoveEndpointByRange(src,other._rangeObj,target)

	def updateSelection(self):
		self._rangeObj.Select()

	updateCaret = updateSelection

class UIA(Window):
	_UIACustomProps = UIAHandler.customProps.CustomPropertiesCommon.get()
	_UIACustomAnnotationTypes = UIAHandler.customAnnotations.CustomAnnotationTypesCommon.get()

	shouldAllowDuplicateUIAFocusEvent = False

	def _get__coreCycleUIAPropertyCacheElementCache(self):
		"""
		A dictionary per core cycle that is ready to map UIA property IDs to UIAElements with that property already cached.
		An example of where multiple cache elements may exist would be where the UIA NVDAObject was instantiated with a UIA element already containing a UI Automation cache (appropriate for generating control fields) but another UIA NVDAObject property (E.g. states) has a set of UIA properties of its own which should be bulk-fetched, and did not exist in the original cache. 
		"""
		return {}

	def _getUIACacheablePropertyValue(self,ID,ignoreDefault=False):
		"""
		Fetches the value for a UI Automation property from an element cache available in this core cycle. If not cached then a new value will be fetched.
		"""
		elementCache=self._coreCycleUIAPropertyCacheElementCache
		# If we have a UIAElement whos own cache contains the property, fetch the value from there
		cacheElement=elementCache.get(ID,None)
		if cacheElement:
			value=cacheElement.getCachedPropertyValueEx(ID,ignoreDefault)
		else:
			# The value is cached nowhere, so ask the UIAElement for its current value for the property
			value=self.UIAElement.getCurrentPropertyValueEx(ID,ignoreDefault)
		return value

	def _prefetchUIACacheForPropertyIDs(self,IDs):
		"""
		Fetch values for all the given UI Automation property IDs in one cache request, making them available for this core cycle.
		"""
		elementCache=self._coreCycleUIAPropertyCacheElementCache
		if elementCache:
			# Ignore any IDs we already have cached values or cache UIAElements for 
			IDs={x for x in IDs if  x not in elementCache}
		if len(IDs)<2:
			# Creating  a UIA cache request for 1 or 0 properties is pointless
			return
		cacheRequest=UIAHandler.handler.clientObject.createCacheRequest()
		for ID in IDs:
			try:
				cacheRequest.addProperty(ID)
			except COMError:
				log.debug("Couldn't add property ID %d to cache request, most likely unsupported on this version of Windows"%ID)
		try:
			cacheElement=self.UIAElement.buildUpdatedCache(cacheRequest)
		except COMError:
			log.debugWarning("IUIAutomationElement.buildUpdatedCache failed given IDs of %s"%IDs)
			return
		for ID in IDs:
			elementCache[ID]=cacheElement

	def findOverlayClasses(self,clsList):
		UIAControlType=self.UIAElement.cachedControlType
		UIAClassName=self.UIAElement.cachedClassName
		# #11445: to avoid COM errors, do not fetch cached UIA Automation Id from the underlying element.
		UIAAutomationId = self.UIAAutomationId
		if UIAClassName=="NetUITWMenuItem" and UIAControlType==UIAHandler.UIA_MenuItemControlTypeId and not self.name and not self.previous:
			# Bounces focus from a netUI dead placeholder menu item when no item is selected up to the menu itself.
			clsList.append(PlaceholderNetUITWMenuItem)
		elif UIAClassName=="WpfTextView":
			clsList.append(WpfTextView)
		elif (
			UIAClassName == "ListViewItem"
			and self.UIAElement.cachedFrameworkID == "WPF"
			and self.role == controlTypes.Role.DATAITEM
		):
			from NVDAObjects.behaviors import RowWithFakeNavigation
			clsList.append(RowWithFakeNavigation)
		elif UIAClassName=="NetUIDropdownAnchor":
			clsList.append(NetUIDropdownAnchor)
		elif self.windowClassName == "EXCEL6" and self.role == controlTypes.Role.PANE:
			from .excel import BadExcelFormulaEdit
			clsList.append(BadExcelFormulaEdit)
		elif self.windowClassName == "EXCEL7":
			if self.role in (controlTypes.Role.DATAITEM, controlTypes.Role.HEADERITEM):
				from .excel import ExcelCell
				clsList.append(ExcelCell)
			elif self.role == controlTypes.Role.DATAGRID:
				from .excel import ExcelWorksheet
				clsList.append(ExcelWorksheet)
			elif self.role == controlTypes.Role.EDITABLETEXT:
				from .excel import CellEdit
				clsList.append(CellEdit)
		elif self.TextInfo == UIATextInfo and (
			UIAClassName == '_WwG'
			or self.windowClassName == '_WwG'
			or UIAAutomationId.startswith('UIA_AutomationId_Word_Content')
		):
			from .wordDocument import WordDocument, WordDocumentNode
			if self.role==controlTypes.Role.DOCUMENT:
				clsList.append(WordDocument)
			else:
				clsList.append(WordDocumentNode)
		# #5136: Windows 8.x and Windows 10 uses different window class and other attributes for toast notifications.
		elif UIAClassName=="ToastContentHost" and UIAControlType==UIAHandler.UIA_ToolTipControlTypeId: #Windows 8.x
			clsList.append(Toast_win8)
		elif (
			self.windowClassName == "Windows.UI.Core.CoreWindow"
			and UIAControlType == UIAHandler.UIA_WindowControlTypeId
			and "ToastView" in UIAAutomationId
		):  # Windows 10
			clsList.append(Toast_win10)
		# #8118: treat UIA tool tips (including those found in UWP apps) as proper tool tips, especially those found in Microsoft Edge and other apps.
		# Windows 8.x toast, although a form of tool tip, is covered separately.
		elif UIAControlType==UIAHandler.UIA_ToolTipControlTypeId:
			clsList.append(ToolTip)
		elif(
			self.UIAElement.cachedFrameworkID in ("InternetExplorer", "MicrosoftEdge")
			# But not for Internet Explorer
			and not self.appModule.appName == 'iexplore'
		):
			from . import spartanEdge
			if UIAClassName in ("Internet Explorer_Server","WebView") and self.role==controlTypes.Role.PANE:
				clsList.append(spartanEdge.EdgeHTMLRootContainer)
			elif (
				self.UIATextPattern
				# #6998:
				# Edge normally gives its root node a controlType of pane, but ARIA role="document"
				# changes the controlType to document
				and self.role in (
					controlTypes.Role.PANE,
					controlTypes.Role.DOCUMENT
				)
				and self.parent
				and (
					isinstance(self.parent, spartanEdge.EdgeHTMLRootContainer)
					or not isinstance(self.parent, spartanEdge.EdgeNode)
				)
			): 
				clsList.append(spartanEdge.EdgeHTMLRoot)
			elif self.role==controlTypes.Role.LIST:
				clsList.append(spartanEdge.EdgeList)
			else:
				clsList.append(spartanEdge.EdgeNode)
		elif self.windowClassName == "Chrome_WidgetWin_1" and self.UIATextPattern:
			from . import chromium
			clsList.append(chromium.ChromiumUIA)
		elif self.windowClassName == "Chrome_RenderWidgetHostHWND":
			from . import chromium
			from . import web
			if (
				self.UIATextPattern
				and self.role == controlTypes.Role.DOCUMENT
				and self.parent
				and self.parent.role == controlTypes.Role.PANE
			):
				clsList.append(chromium.ChromiumUIADocument)
			else:
				if self.role == controlTypes.Role.LIST:
					clsList.append(web.List)
				clsList.append(chromium.ChromiumUIA)
		elif (
			self.role == controlTypes.Role.DOCUMENT
			and UIAAutomationId == "Microsoft.Windows.PDF.DocumentView"
		):
			# PDFs
			from . import spartanEdge
			clsList.append(spartanEdge.EdgeHTMLRoot)
		elif (
			UIAAutomationId == "RichEditControl"
			and "DevExpress.XtraRichEdit" in self.UIAElement.cachedProviderDescription
		):
			clsList.insert(0, DevExpressXtraRichEdit)
		if UIAControlType == UIAHandler.UIA_ProgressBarControlTypeId:
			clsList.insert(0, ProgressBar)
		if UIAClassName=="ControlPanelLink":
			clsList.append(ControlPanelLink)
		if UIAClassName=="UIColumnHeader":
			clsList.append(UIColumnHeader)
		elif UIAClassName=="UIItem":
			clsList.append(UIItem)
		elif UIAClassName=="SensitiveSlider":
			clsList.append(SensitiveSlider) 
		if UIAControlType==UIAHandler.UIA_TreeItemControlTypeId:
			clsList.append(TreeviewItem)
		if UIAControlType==UIAHandler.UIA_MenuItemControlTypeId:
			clsList.append(MenuItem)
		# Some combo boxes and looping selectors do not expose value pattern.
		elif (UIAControlType==UIAHandler.UIA_ComboBoxControlTypeId
		# #5231: Announce values in time pickers by "transforming" them into combo box without value pattern objects.
		or (UIAControlType==UIAHandler.UIA_ListControlTypeId and "LoopingSelector" in UIAClassName)):
			try:
				if not self._getUIACacheablePropertyValue(UIAHandler.UIA_IsValuePatternAvailablePropertyId):
					clsList.append(ComboBoxWithoutValuePattern)
			except COMError:
				pass
		elif UIAControlType==UIAHandler.UIA_ListItemControlTypeId:
			clsList.append(ListItem)
		# #5942: In Windows 10 build 14332 and later, Microsoft rewrote various dialog code including that of User Account Control.
		# #8405: there are more dialogs scattered throughout Windows 10 and various apps.
		# Dialog detection is a bit easier on build 17682 and later thanks to IsDialog property.
		try:
			isDialog = self._getUIACacheablePropertyValue(UIAHandler.UIA_IsDialogPropertyId)
		except COMError:
			# We can fallback to a known set of dialog classes for window elements.
			isDialog = (self.UIAIsWindowElement and UIAClassName in UIAHandler.UIADialogClassNames)
		if isDialog:
			clsList.append(Dialog)
		# #6241: Try detecting all possible suggestions containers and search fields scattered throughout Windows 10.
		if UIAAutomationId in ("SearchTextBox", "TextBox"):
			clsList.append(SearchField)
		# #12790: detect suggestions list views firing layout invalidated event.
		if UIAAutomationId == "SuggestionsList":
			clsList.append(SuggestionsList)
		try:
			# Nested block here in order to catch value error and variable binding error when attempting to access automation ID for invalid elements.
			try:
				# #6241: Raw UIA base tree walker is better than simply looking at self.parent when locating suggestion list items.
				# #10329: 2019 Windows Search results require special handling due to UI redesign.
				parentElement=UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
				# Sometimes, fetching parent (list control) via base tree walker fails, especially when dealing with suggestions in Windows10 Start menu.
				# Oddly, we need to take care of context menu for Start search suggestions as well.
				if parentElement.cachedAutomationId.lower() in ("suggestionslist", "contextmenu"):
					clsList.append(SuggestionListItem)
			except COMError:
				pass
		except ValueError:
			pass

		if self.UIAElement.cachedFrameworkID == "WPF" and self.appModule.appName in ("devenv", "ssms"):
			from . import VisualStudio
			VisualStudio.findExtraOverlayClasses(self, clsList)

		# Support Windows Console's UIA interface
		if self.windowClassName == "ConsoleWindowClass":
			from . import winConsoleUIA
			winConsoleUIA.findExtraOverlayClasses(self, clsList)
		elif UIAClassName in ("TermControl", "TermControl2"):
			# microsoft/terminal#12358: Eventually, TermControl2 should have
			# a separate overlay class that is not a descendant of LiveText.
			# TermControl2 sends inserted text using UIA notification events,
			# so it is no longer necessary to diff the object as with all
			# previous terminal implementations.
			from . import winConsoleUIA
			clsList.append(winConsoleUIA.WinTerminalUIA)

		# Add editableText support if UIA supports a text pattern
		if self.TextInfo==UIATextInfo:
			if UIAHandler.autoSelectDetectionAvailable:
				clsList.append(EditableTextWithAutoSelectDetection)
			else:
				clsList.append(EditableTextWithoutAutoSelectDetection)

		clsList.append(UIA)

		if self.UIAIsWindowElement:
			super(UIA,self).findOverlayClasses(clsList)
			if self.UIATextPattern:
				#Since there is a UIA text pattern, there is no need to use the win32 edit support at all
				import NVDAObjects.window.edit
				for x in list(clsList):
					if issubclass(x,NVDAObjects.window.edit.Edit):
						clsList.remove(x)

	@classmethod
	def kwargsFromSuper(cls, kwargs, relation=None, ignoreNonNativeElementsWithFocus=True):
		UIAElement=None
		windowHandle=kwargs.get('windowHandle')
		if isinstance(relation,tuple):
			UIAElement=UIAHandler.handler.clientObject.ElementFromPointBuildCache(POINT(relation[0],relation[1]),UIAHandler.handler.baseCacheRequest)
			# Ignore this object if it is non native.
			if not UIAHandler.handler.isNativeUIAElement(UIAElement):
				if UIAHandler._isDebug():
					log.debug(
						f"kwargsFromSuper: ignoring non native element at coordinates {relation}"
					)
				return False
			# This object may be in a different window, so we need to recalculate the window handle.
			kwargs['windowHandle'] = None
		elif relation=="focus":
			try:
				UIAElement = UIAHandler.handler.clientObject.getFocusedElementBuildCache(
					UIAHandler.handler.baseCacheRequest
				)
			except COMError:
				log.debugWarning("getFocusedElement failed", exc_info=True)
				return False
			# Ignore this object if it is non native.
			if ignoreNonNativeElementsWithFocus and not UIAHandler.handler.isNativeUIAElement(UIAElement):
				if UIAHandler._isDebug():
					log.debug(
						"kwargsFromSuper: ignoring non native element with focus"
					)
				return False
			# This object may be in a different window, so we need to recalculate the window handle.
			kwargs['windowHandle'] = None
		else:
			UIAElement=UIAHandler.handler.clientObject.ElementFromHandleBuildCache(windowHandle,UIAHandler.handler.baseCacheRequest)
		if not UIAElement:
			return False
		kwargs['UIAElement']=UIAElement
		return True

	def getNormalizedUIATextRangeFromElement(self,UIAElement):
		"""Simply fetches a UIA text range for the given UIAElement, allowing subclasses to process the range first."""
		return UIATextRangeFromElement(self.UIATextPattern,UIAElement)

	def __init__(self,windowHandle=None,UIAElement=None,initialUIACachedPropertyIDs=None):
		"""
		An NVDAObject for a UI Automation element.
		@param windowHandle: if a UIAElement is not specifically given, then this windowHandle is used to fetch its root UIAElement 
		@type windowHandle: int
		@param UIAElement: the UI Automation element that should be represented by this NVDAObject
		The UI Automation element must have been created with a L{UIAHandler.handler.baseCacheRequest}
		@type UIAElement: L{UIAHandler.IUIAutomationElement}
		@param initialUIACachedPropertyIDs: Extra UI Automation properties the given UIAElement has already had cached with a UIA cache request that inherits from L{UIAHandler.handler.baseCacheRequest}.
		Cached values of these properties will be available for the remainder of the current core cycle. After that, new values will be fetched.
		@type initialUIACachedPropertyIDs: L{UIAHandler.IUIAutomationCacheRequest}
		"""
		if not UIAElement:
			raise ValueError("needs a UIA element")

		self.UIAElement=UIAElement

		UIACachedWindowHandle=UIAElement.cachedNativeWindowHandle
		self.UIAIsWindowElement=bool(UIACachedWindowHandle)
		if not windowHandle:
			windowHandle=UIAHandler.handler.getNearestWindowHandle(UIAElement)
		if not windowHandle:
			raise InvalidNVDAObject("no windowHandle")
		super(UIA,self).__init__(windowHandle=windowHandle)

		self.initialUIACachedPropertyIDs=initialUIACachedPropertyIDs
		if initialUIACachedPropertyIDs:
			elementCache=self._coreCycleUIAPropertyCacheElementCache
			for ID in initialUIACachedPropertyIDs:
				elementCache[ID]=self.UIAElement

	def _isEqual(self,other):
		if not isinstance(other,UIA):
			return False
		try:
			return UIAHandler.handler.clientObject.CompareElements(self.UIAElement,other.UIAElement)
		except:
			return False

	def event_gainFocus(self):
		UIAHandler.handler.addLocalEventHandlerGroupToElement(self.UIAElement, isFocus=True)
		super().event_gainFocus()

	def event_loseFocus(self):
		super().event_loseFocus()
		UIAHandler.handler.removeLocalEventHandlerGroupFromElement(self.UIAElement)

	def _get_shouldAllowUIAFocusEvent(self):
		try:
			return bool(self._getUIACacheablePropertyValue(UIAHandler.UIA_HasKeyboardFocusPropertyId))
		except COMError:
			return True

	_lastLiveRegionChangeInfo=(None,None) #: Keeps track of the last live region change (text, time)
	def _get__shouldAllowUIALiveRegionChangeEvent(self):
		"""
		This property decides whether  a live region change event should be allowed. It compaires live region event with the last one received, only allowing the event if the text (name) is different, or if the time since the last one is at least 0.5 seconds. 
		"""
		oldText,oldTime=self._lastLiveRegionChangeInfo
		newText=self.name
		newTime=time.time()
		self.__class__._lastLiveRegionChangeInfo=(newText,newTime)
		if newText==oldText and oldTime is not None and (newTime-oldTime)<0.5:
			return False
		return True

	def _getUIAPattern(self,ID,interface,cache=False):
		punk=self.UIAElement.GetCachedPattern(ID) if cache else self.UIAElement.GetCurrentPattern(ID) 
		if punk:
			return punk.QueryInterface(interface)

	def _get_UIAInvokePattern(self):
		self.UIAInvokePattern=self._getUIAPattern(UIAHandler.UIA_InvokePatternId,UIAHandler.IUIAutomationInvokePattern)
		return self.UIAInvokePattern

	def _get_UIAGridPattern(self):
		self.UIAGridPattern=self._getUIAPattern(UIAHandler.UIA_GridPatternId,UIAHandler.IUIAutomationGridPattern)
		return self.UIAGridPattern

	def _get_UIARangeValuePattern(self):
		self.UIARangeValuePattern = self._getUIAPattern(
			UIAHandler.UIA_RangeValuePatternId,
			UIAHandler.IUIAutomationRangeValuePattern
		)
		return self.UIARangeValuePattern

	def _get_UIAValuePattern(self):
		self.UIAValuePattern = self._getUIAPattern(
			UIAHandler.UIA_ValuePatternId,
			UIAHandler.IUIAutomationValuePattern
		)
		return self.UIAValuePattern

	def _get_UIATogglePattern(self):
		self.UIATogglePattern=self._getUIAPattern(UIAHandler.UIA_TogglePatternId,UIAHandler.IUIAutomationTogglePattern)
		return self.UIATogglePattern

	def _get_UIASelectionItemPattern(self):
		self.UIASelectionItemPattern=self._getUIAPattern(UIAHandler.UIA_SelectionItemPatternId,UIAHandler.IUIAutomationSelectionItemPattern)
		return self.UIASelectionItemPattern

	def _get_UIASelectionPattern(self):
		self.UIASelectionPattern = self._getUIAPattern(
			UIAHandler.UIA_SelectionPatternId,
			UIAHandler.IUIAutomationSelectionPattern
		)
		return self.UIASelectionPattern

	def _get_UIASelectionPattern2(self):
		try:
			self.UIASelectionPattern2 = self._getUIAPattern(
				UIAHandler.UIA_SelectionPattern2Id,
				UIAHandler.IUIAutomationSelectionPattern2
			)
		except COMError:
			# SelectionPattern2 is not available on older Operating Systems such as Windows 7
			self.UIASelectionPattern2 = None
		return self.UIASelectionPattern2

	def getSelectedItemsCount(self, maxItems=None):
		p = self.UIASelectionPattern2
		if p:
			return p.currentItemCount
		return 0

	#: Typing information for auto-property: _get_selectionContainer
	selectionContainer: "typing.Optional[UIA]"

	def _get_selectionContainer(self) -> "typing.Optional[UIA]":
		p = self.UIASelectionItemPattern
		if not p:
			return None
		e = p.currentSelectionContainer
		if not e:
			# Some implementations of SelectionItemPattern, such as the Outlook attachment list
			# give back a NULL selectionContainer
			return None
		e = e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		obj = UIA(UIAElement=e)
		if obj.UIASelectionPattern2:
			return obj
		return None

	#: typing for auto-property: UIAAnnotationObjects
	UIAAnnotationObjects: typing.Dict[int, UIAHandler.IUIAutomationElement]

	def _get_UIAAnnotationObjects(self) -> typing.Dict[int, UIAHandler.IUIAutomationElement]:
		"""
		Returns this UIAElement's annotation objects,
		in a dict keyed by their annotation type ID.
		"""
		objsByTypeID = {}
		objs = self._getUIACacheablePropertyValue(UIAHandler.UIA_AnnotationObjectsPropertyId)
		if objs:
			objs = objs.QueryInterface(UIAHandler.IUIAutomationElementArray)
			for index in range(objs.length):
				obj = objs.getElement(index)
				typeID = obj.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId)
				objsByTypeID[typeID] = obj
		return objsByTypeID

	def _get_UIATextPattern(self):
		self.UIATextPattern = self._getUIAPattern(
			UIAHandler.UIA_TextPatternId,
			UIAHandler.IUIAutomationTextPattern,
			cache=False
		)
		return self.UIATextPattern

	def _get_UIATableItemPattern(self):
		self.UIATableItemPattern = self._getUIAPattern(
			UIAHandler.UIA_TableItemPatternId,
			UIAHandler.IUIAutomationTableItemPattern,
			cache=False
		)
		return self.UIATableItemPattern

	def _get_UIATextEditPattern(self):
		if not isinstance(UIAHandler.handler.clientObject,UIAHandler.IUIAutomation3):
			return None
		self.UIATextEditPattern=self._getUIAPattern(UIAHandler.UIA_TextEditPatternId,UIAHandler.IUIAutomationTextEditPattern,cache=False)
		return self.UIATextEditPattern

	def _get_UIALegacyIAccessiblePattern(self):
		self.UIALegacyIAccessiblePattern=self._getUIAPattern(UIAHandler.UIA_LegacyIAccessiblePatternId,UIAHandler.IUIAutomationLegacyIAccessiblePattern)
		return self.UIALegacyIAccessiblePattern

	_TextInfo=UIATextInfo
	_cache_TextInfo = False

	def _get_TextInfo(self):
		if self.UIATextPattern:
			return self._TextInfo
		textInfo = super(UIA, self).TextInfo
		if textInfo is NVDAObjectTextInfo and self.UIAIsWindowElement and self.role==controlTypes.Role.WINDOW:
			import displayModel
			return displayModel.DisplayModelTextInfo
		return textInfo

	def setFocus(self):
		self.UIAElement.setFocus()

	def _get_devInfo(self):
		info=super(UIA,self).devInfo
		info.append("UIAElement: %r"%self.UIAElement)
		# #11445: allow exceptions to be recorded when presenting Automation Id.
		try:
			ret=self.UIAElement.currentAutomationID
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA automationID: %s"%ret)
		try:
			ret=self.UIAElement.cachedFrameworkID
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA frameworkID: %s"%ret)
		try:
			ret=str(self.UIAElement.getRuntimeID())
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA runtimeID: %s"%ret)
		try:
			ret=self.UIAElement.cachedProviderDescription
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA providerDescription: %s"%ret)
		try:
			ret=self.UIAElement.currentClassName
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA className: %s"%ret)
		patternsAvailable = []
		patternAvailableConsts = dict(
			(const, name) for name, const in UIAHandler.__dict__.items()
			if name.startswith("UIA_Is") and name.endswith("PatternAvailablePropertyId")
		)
		self._prefetchUIACacheForPropertyIDs(list(patternAvailableConsts))
		for const, name in patternAvailableConsts.items():
			try:
				res = self._getUIACacheablePropertyValue(const)
			except COMError:
				res = False
			if res:
				# Every name has the same format, so the string indexes can be safely hardcoded here.
				patternsAvailable.append(name[6:-19])
		info.append("UIA patterns available: %s"%", ".join(patternsAvailable))
		return info

	def _get_UIAAutomationId(self):
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_AutomationIdPropertyId)
		except COMError:
			# #11445: due to timing errors, elements will be instantiated with no automation Id present.
			return ""

	#: Typing info for auto property _get_name()
	name: str

	def _get_name(self) -> str:
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_NamePropertyId)
		except COMError:
			return ""

	def _get_liveRegionPoliteness(self):
		try:
			return UIAHandler.UIALiveSettingtoNVDAAriaLivePoliteness.get(
				self._getUIACacheablePropertyValue(UIAHandler.UIA.UIA_LiveSettingPropertyId),
				super().liveRegionPoliteness
			)
		except COMError:
			return super().liveRegionPoliteness

	def _get_role(self):
		role=UIAHandler.UIAControlTypesToNVDARoles.get(self.UIAElement.cachedControlType,controlTypes.Role.UNKNOWN)
		if role==controlTypes.Role.BUTTON:
			try:
				s=self._getUIACacheablePropertyValue(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
			except COMError:
				s=UIAHandler.handler.reservedNotSupportedValue
			if s!=UIAHandler.handler.reservedNotSupportedValue:
				role=controlTypes.Role.TOGGLEBUTTON
		elif role in (controlTypes.Role.UNKNOWN,controlTypes.Role.PANE,controlTypes.Role.WINDOW) and self.windowHandle:
			superRole=super(UIA,self).role
			if superRole!=controlTypes.Role.WINDOW:
				role=superRole
		return role

	def _get_UIAFullDescription(self):
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_FullDescriptionPropertyId) or ""
		except COMError:
			return ""

	def _get_UIAHelpText(self):
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_HelpTextPropertyId) or ""
		except COMError:
			return ""

	def _get_description(self):
		return self.UIAFullDescription or self.UIAHelpText

	def _get_keyboardShortcut(self):
		# Build the keyboard shortcuts list early for readability.
		shortcuts = []
		accessKey = self._getUIACacheablePropertyValue(UIAHandler.UIA_AccessKeyPropertyId)
		# #6779: Don't add access key to the shortcut list if UIA says access key is None, resolves concatenation error in focus events, object navigation and so on.
		# In rare cases, access key itself is None.
		if accessKey:
			shortcuts.append(accessKey)
		acceleratorKey = self._getUIACacheablePropertyValue(UIAHandler.UIA_AcceleratorKeyPropertyId)
		# Same case as access key.
		if acceleratorKey:
			shortcuts.append(acceleratorKey)
		# #6790: Do not add two spaces unless both access key and accelerator are present in order to not waste string real estate.
		return "  ".join(shortcuts) if shortcuts else ""

	_UIAStatesPropertyIDs={
		UIAHandler.UIA_HasKeyboardFocusPropertyId,
		UIAHandler.UIA_SelectionItemIsSelectedPropertyId,
		UIAHandler.UIA_IsDataValidForFormPropertyId,
		UIAHandler.UIA_IsRequiredForFormPropertyId,
		UIAHandler.UIA_ValueIsReadOnlyPropertyId,
		UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,
		UIAHandler.UIA_ToggleToggleStatePropertyId,
		UIAHandler.UIA_IsKeyboardFocusablePropertyId,
		UIAHandler.UIA_IsPasswordPropertyId,
		UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId,
		UIAHandler.UIA_IsEnabledPropertyId,
		UIAHandler.UIA_IsOffscreenPropertyId,
		UIAHandler.UIA_AnnotationTypesPropertyId,
	}

	def _get_states(self):
		states=set()
		self._prefetchUIACacheForPropertyIDs(self._UIAStatesPropertyIDs)
		try:
			hasKeyboardFocus=self._getUIACacheablePropertyValue(UIAHandler.UIA_HasKeyboardFocusPropertyId)
		except COMError:
			hasKeyboardFocus=False
		if hasKeyboardFocus:
			states.add(controlTypes.State.FOCUSED)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsKeyboardFocusablePropertyId):
			states.add(controlTypes.State.FOCUSABLE)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsPasswordPropertyId):
			states.add(controlTypes.State.PROTECTED)
		# Don't fetch the role unless we must, but never fetch it more than once.
		role=None
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId):
			role=self.role
			states.add(controlTypes.State.CHECKABLE if role==controlTypes.Role.RADIOBUTTON else controlTypes.State.SELECTABLE)
			if self._getUIACacheablePropertyValue(UIAHandler.UIA_SelectionItemIsSelectedPropertyId):
				states.add(controlTypes.State.CHECKED if role==controlTypes.Role.RADIOBUTTON else controlTypes.State.SELECTED)
		if not self._getUIACacheablePropertyValue(UIAHandler.UIA_IsEnabledPropertyId,True):
			states.add(controlTypes.State.UNAVAILABLE)
		try:
			isOffScreen = self._getUIACacheablePropertyValue(UIAHandler.UIA_IsOffscreenPropertyId)
		except COMError:
			isOffScreen = False
		if isOffScreen:
			states.add(controlTypes.State.OFFSCREEN)
		try:
			isDataValid=self._getUIACacheablePropertyValue(UIAHandler.UIA_IsDataValidForFormPropertyId,True)
		except COMError:
			isDataValid=UIAHandler.handler.reservedNotSupportedValue
		if not isDataValid:
			states.add(controlTypes.State.INVALID_ENTRY)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsRequiredForFormPropertyId):
			states.add(controlTypes.State.REQUIRED)

		if self._getReadOnlyState():
			states.add(controlTypes.State.READONLY)

		try:
			s=self._getUIACacheablePropertyValue(UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if s==UIAHandler.ExpandCollapseState_Collapsed:
				states.add(controlTypes.State.COLLAPSED)
			elif s==UIAHandler.ExpandCollapseState_Expanded:
				states.add(controlTypes.State.EXPANDED)
		try:
			s=self._getUIACacheablePropertyValue(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if not role:
				role=self.role
			if role==controlTypes.Role.TOGGLEBUTTON:
				if s==UIAHandler.ToggleState_On:
					states.add(controlTypes.State.PRESSED)
			else:
				states.add(controlTypes.State.CHECKABLE)
				if s==UIAHandler.ToggleState_On:
					states.add(controlTypes.State.CHECKED)
		try:
			annotationTypes = self._getUIACacheablePropertyValue(UIAHandler.UIA_AnnotationTypesPropertyId)
		except COMError:
			# annotationTypes cannot be fetched on older Operating Systems such as Windows 7.
			annotationTypes = None
		if annotationTypes:
			if UIAHandler.AnnotationType_Comment in annotationTypes:
				states.add(controlTypes.State.HASCOMMENT)
		return states

	def _getReadOnlyState(self) -> bool:
		try:
			isReadOnly = self._getUIACacheablePropertyValue(UIAHandler.UIA_ValueIsReadOnlyPropertyId, True)
		except COMError:
			isReadOnly = UIAHandler.handler.reservedNotSupportedValue
		if (
			isReadOnly == UIAHandler.handler.reservedNotSupportedValue
			and self.UIATextPattern
		):
			# Most UIA text controls don't support the "ValueIsReadOnly" property,
			# so we need to look at the root document "IsReadOnly" attribute.
			try:
				document = self.UIATextPattern.documentRange
				isReadOnly = document.GetAttributeValue(UIAHandler.UIA_IsReadOnlyAttributeId)
			except COMError:
				isReadOnly = UIAHandler.handler.reservedNotSupportedValue
		if isReadOnly == UIAHandler.handler.reservedNotSupportedValue:
			return False
		return isReadOnly

	def _get_presentationType(self):
		presentationType=super(UIA,self).presentationType
		# UIA NVDAObjects can only be considered content if UI Automation considers them both a control and content.
		if presentationType==self.presType_content and not (self.UIAElement.cachedIsContentElement and self.UIAElement.cachedIsControlElement):
			presentationType=self.presType_layout
		return presentationType 

	def correctAPIForRelation(self, obj, relation=None):
		if obj and self.windowHandle != obj.windowHandle and not obj.UIAElement.cachedNativeWindowHandle:
			# The target element is not the root element for the window, so don't change API class; i.e. always use UIA.
			return obj
		return super(UIA, self).correctAPIForRelation(obj, relation)

	def _get_parent(self):
		try:
			parentElement=UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			parentElement=None
		if not parentElement:
			return super(UIA,self).parent
		if not parentElement.CachedNativeWindowHandle and not self.UIAElement.CachedNativeWindowHandle:
			# Neither self or parent have a window handle themselves, so their nearest window handle will be the same.
			# Cache this on the parent if cached on self, to avoid fetching it later.
			try:
				parentElement._nearestWindowHandle=self.UIAElement._nearestWindowHandle
			except AttributeError:
				# _nearestWindowHandle may not exist on self if self was instantiated given a windowHandle.
				pass
		return self.correctAPIForRelation(UIA(UIAElement=parentElement),relation="parent")

	def _get_previous(self):
		try:
			previousElement=UIAHandler.handler.baseTreeWalker.GetPreviousSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not previousElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=previousElement))

	#: Typing information for auto-property: _get_next
	next: "typing.Optional[UIA]"

	def _get_next(self) -> "typing.Optional[UIA]":
		try:
			nextElement=UIAHandler.handler.baseTreeWalker.GetNextSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not nextElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=nextElement))

	def _get_firstChild(self):
		try:
			firstChildElement=UIAHandler.handler.baseTreeWalker.GetFirstChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not firstChildElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=firstChildElement))

	def _get_lastChild(self):
		try:
			lastChildElement=UIAHandler.handler.baseTreeWalker.GetLastChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not lastChildElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=lastChildElement))

	def _get_UIAChildren(self):
		childrenCacheRequest = UIAHandler.handler.baseCacheRequest.clone()
		childrenCacheRequest.TreeScope = UIAHandler.TreeScope_Children
		try:
			return self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		except COMError as e:
			log.debugWarning("Could not fetch cached children from UIA element: %s"%e)
			raise e

	def _get_children(self):
		try:
			cachedChildren = self.UIAChildren
			children = []
			if not cachedChildren:
				# GetCachedChildren returns null if there are no children.
				return children
			for index in range(cachedChildren.length):
				e = cachedChildren.getElement(index)
				windowHandle = self.windowHandle
				children.append(self.correctAPIForRelation(UIA(windowHandle=windowHandle, UIAElement=e)))
			return children
		except COMError:
			return super().children

	def _get_childCount(self):
		try:
			cachedChildren = self.UIAChildren
			if not cachedChildren:
				# GetCachedChildren returns null if there are no children.
				return 0
			return cachedChildren.length
		except COMError:
			return len(super().children)

	def _get_rowNumber(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridItemRowPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

	def _get_rowSpan(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridItemRowSpanPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val
		return 1

	def _getTextFromHeaderElement(self, element: UIAHandler.IUIAutomationElement) -> typing.Optional[str]:
		obj = UIA(
			windowHandle=self.windowHandle,
			UIAElement=element.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		)
		if not obj:
			return None
		return obj.makeTextInfo(textInfos.POSITION_ALL).text

	def _get_rowHeaderText(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_TableItemRowHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in range(val.length):
			e=val.getElement(i)
			if UIAHandler.handler.clientObject.compareElements(e,self.UIAElement):
				continue
			text = self._getTextFromHeaderElement(e)
			if not text:
				continue
			textList.append(text)
		return " ".join(textList)

	def _get_columnNumber(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridItemColumnPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

	def _get_columnSpan(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridItemColumnSpanPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val
		return 1

	def _get_columnHeaderText(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in range(val.length):
			e=val.getElement(i)
			if UIAHandler.handler.clientObject.compareElements(e,self.UIAElement):
				continue
			text = self._getTextFromHeaderElement(e)
			if not text:
				continue
			textList.append(text)
		return " ".join(textList)

	def _get_rowCount(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridRowCountPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val
		raise NotImplementedError

	def _get_columnCount(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridColumnCountPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val
		raise NotImplementedError

	def _get_table(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridItemContainingGridPropertyId ,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			e=val.QueryInterface(UIAHandler.IUIAutomationElement).buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
			return UIA(UIAElement=e)
		raise NotImplementedError

	def _get_processID(self):
		if self.windowClassName == 'ConsoleWindowClass':
			# #10115: The UIA implementation for Windows console windows exposes the process ID of conhost,
			# not the actual app it is hosting.
			# Therefore, to work around this, for console windows, we fallback to getting processID from the window
			# rather than from UIA.
			# Note that we can't do this hack in the WinConsoleUIA NVDAObject
			# Because the appModule is already created and cached
			# before the UIA NVDAObject is morphed into the specific WinConsoleUIA class.
			return super().processID
		return self.UIAElement.cachedProcessId

	def _get_location(self):
		try:
			r=self._getUIACacheablePropertyValue(UIAHandler.UIA_BoundingRectanglePropertyId)
		except COMError:
			return None
		if r is None:
			return
		# r is a tuple of floats representing left, top, width and height.
		return locationHelper.RectLTWH.fromFloatCollection(*r)

	def _get_UIAValue(self) -> typing.Optional[str]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA.UIA_ValueValuePropertyId, True)
		if val != UIAHandler.handler.reservedNotSupportedValue:
			return val
		return None

	def _get_UIARangeValue(self) -> typing.Optional[float]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA.UIA_RangeValueValuePropertyId, True)
		if val != UIAHandler.handler.reservedNotSupportedValue:
			return val
		return None

	def _get_value(self) -> typing.Optional[str]:
		if self.UIAValue is not None:
			return self.UIAValue
		if self.UIARangeValue is not None:
			return f"{round(self.UIARangeValue)}"
		return None

	def _get_actionCount(self):
		if self.UIAInvokePattern:
			return 1
		return 0

	def getActionName(self,index=None):
		if not index:
			index=self.defaultActionIndex
		if index==0 and self.UIAInvokePattern:
			return _("invoke")
		raise NotImplementedError

	def doAction(self,index=None):
		if not index:
			index=self.defaultActionIndex
		if index==0:
			if self.UIAInvokePattern:
				self.UIAInvokePattern.Invoke()
			elif self.UIATogglePattern:
				self.UIATogglePattern.toggle()
			elif self.UIASelectionItemPattern:
				self.UIASelectionItemPattern.select()
			return
		raise NotImplementedError

	def _get_hasFocus(self):
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_HasKeyboardFocusPropertyId)
		except COMError:
			return False

	def _get_hasIrrelevantLocation(self):
		try:
			isOffScreen = self._getUIACacheablePropertyValue(UIAHandler.UIA_IsOffscreenPropertyId)
		except COMError:
			isOffScreen = False
		return isOffScreen or not self.location or not any(self.location)

	def _get_positionInfo(self):
		info=super(UIA,self).positionInfo or {}
		itemIndex=0
		try:
			itemIndex=self._getUIACacheablePropertyValue(UIAHandler.UIA_PositionInSetPropertyId)
		except COMError:
			pass
		if itemIndex>0:
			info['indexInGroup']=itemIndex
			itemCount=0
			try:
				itemCount=self._getUIACacheablePropertyValue(UIAHandler.UIA_SizeOfSetPropertyId)
			except COMError:
				pass
			if itemCount>0:
				info['similarItemsInGroup']=itemCount
		try:
			level=self._getUIACacheablePropertyValue(UIAHandler.UIA_LevelPropertyId)
		except COMError:
			level=None
		if level is not None and level>0:
			info["level"]=level
		return info

	def scrollIntoView(self):
		pass

	def _get_controllerFor(self):
		e=self._getUIACacheablePropertyValue(UIAHandler.UIA_ControllerForPropertyId)
		if UIAHandler.handler.clientObject.checkNotSupported(e):
			return None
		a=e.QueryInterface(UIAHandler.IUIAutomationElementArray)
		objList=[]
		for index in range(a.length):
			e=a.getElement(index)
			e=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
			obj=UIA(UIAElement=e)
			if obj:
				objList.append(obj)
		return objList

	def event_UIA_elementSelected(self):
		self.event_stateChange()

	def event_valueChange(self):
		if issubclass(self.TextInfo, UIATextInfo):
			return
		return super(UIA, self).event_valueChange()

	def event_UIA_systemAlert(self):
		"""
		A base implementation for UI Automation's system Alert event.
		This just reports the element that received the alert in speech and braille, similar to how focus is presented.
		Skype for business toast notifications being one example.
		"""
		speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)
		# Ideally, we wouldn't use getPropertiesBraille directly.
		braille.handler.message(braille.getPropertiesBraille(name=self.name, role=self.role))

	def event_UIA_notification(self, notificationKind=None, notificationProcessing=UIAHandler.NotificationProcessing_CurrentThenMostRecent, displayString=None, activityId=None):
		"""
		Introduced in Windows 10 Fall Creators Update (build 16299).
		This base implementation announces all notifications from the UIA element.
		Unlike other events, the text to be announced is not the name of the object, and parameters control how the incoming notification should be processed.
		Subclasses can override this event and can react to notification processing instructions.
		"""
		# Do not announce notifications from background apps.
		if self.appModule != api.getFocusObject().appModule:
			return
		if displayString:
			if notificationProcessing in (UIAHandler.NotificationProcessing_ImportantMostRecent, UIAHandler.NotificationProcessing_MostRecent):
				# These notifications superseed earlier notifications.
				# Note that no distinction is made between important and non-important.
				speech.cancelSpeech()
			ui.message(displayString)

class TreeviewItem(UIA):

	def _get_value(self):
		return ""

	def _get__level(self):
		level=0
		obj=self
		while obj: 
			level+=1
			parent=obj.parent=obj.parent
			if not parent or parent==obj or parent.role!=controlTypes.Role.TREEVIEWITEM:
				return level
			obj=parent
		return level

	def _get_positionInfo(self):
		info=super(TreeviewItem,self).positionInfo or {}
		info['level']=self._level
		return info

class MenuItem(UIA):

	def _get_description(self):
		name=self.name
		description=super(MenuItem,self)._get_description()
		if description!=name:
			return description
		else:
			return None

class UIColumnHeader(UIA):

	def _get_description(self):
		description = self.UIAHelpText
		try:
			itemStatus=self._getUIACacheablePropertyValue(UIAHandler.UIA_ItemStatusPropertyId)
		except COMError:
			itemStatus=""
		return " ".join([x for x in (description,itemStatus) if x and not x.isspace()])

class UIItem(UIA):
	"""UIA list items in an Items View repeate the name as the value"""

	def _get_positionInfo(self):
		info={}
		itemIndex=0
		try:
			itemIndex = self._getUIACacheablePropertyValue(self._UIACustomProps.itemIndex.id)
		except COMError:
			pass
		if itemIndex>0:
			info['indexInGroup']=itemIndex
			try:
				e=self._getUIACacheablePropertyValue(UIAHandler.UIA_SelectionItemSelectionContainerPropertyId)
				if e: e=e.QueryInterface(UIAHandler.IUIAutomationElement)
			except COMError:
				e=None
			if e:
				try:
					itemCount = e.getCurrentPropertyValue(self._UIACustomProps.itemCount.id)
				except COMError:
					itemCount=0
				if itemCount>0:
					info['similarItemsInGroup']=itemCount
		return info

	def _get_value(self):
		return ""

class SensitiveSlider(UIA):
	"""A slider that tends to give focus to its thumb control"""

	def event_focusEntered(self):
		self.reportFocus()

	def event_valueChange(self):
		focusParent=api.getFocusObject().parent
		if self==focusParent:
			speech.speakObjectProperties(self, value=True, reason=controlTypes.OutputReason.CHANGE)
		else:
			super(SensitiveSlider,self).event_valueChange()

class ControlPanelLink(UIA):

	def _get_description(self):
		desc = self.UIAHelpText
		try:
			i=desc.find('\n')
		except:
			i=None
		if i:
			desc=desc[i+1:]
		return desc

class ComboBoxWithoutValuePattern(UIA):
	"""A combo box without the Value pattern.
	UIA combo boxes don't necessarily support the Value pattern unless they take arbitrary text values.
	However, NVDA expects combo boxes to have a value and to fire valueChange events.
	The value is obtained by retrieving the selected item's name.
	The valueChange event is fired on this object by L{ListItem.event_stateChange}.
	"""

	def _get_UIASelectionPattern(self):
		punk = self.UIAElement.GetCurrentPattern(UIAHandler.UIA_SelectionPatternId)
		if punk:
			self.UIASelectionPattern = punk.QueryInterface(UIAHandler.IUIAutomationSelectionPattern)
		else:
			self.UIASelectionPattern = None
		return self.UIASelectionPattern

	def _get_value(self):
		try:
			return self.UIASelectionPattern.GetCurrentSelection().GetElement(0).CurrentName
		except (COMError, AttributeError):
			return None

class ListItem(UIA):

	def event_stateChange(self):
		if not self.hasFocus:
			parent = self.parent
			focus=api.getFocusObject()
			if parent and parent==focus and (isinstance(parent, ComboBoxWithoutValuePattern)
				or (parent._getUIACacheablePropertyValue(UIAHandler.UIA_IsValuePatternAvailablePropertyId) and parent.windowClassName.startswith("Windows.UI.Core"))):
				# #6337: This is an item in a combo box without the Value pattern or does not raise value change event.
				# This item has been selected, so notify the combo box that its value has changed.
				focus.event_valueChange()
		super(ListItem, self).event_stateChange()

class Dialog(Dialog):
	role=controlTypes.Role.DIALOG

class Toast_win8(Notification, UIA):

	event_UIA_toolTipOpened=Notification.event_alert

class Toast_win10(Notification, UIA):

	# #6096: Windows 10 build 14366 and later does not fire tooltip event when toasts appear.
	if winVersion.getWinVer() > winVersion.WIN10_1511:
		event_UIA_window_windowOpen=Notification.event_alert
	else:
		event_UIA_toolTipOpened=Notification.event_alert
	# #7128: in Creators Update (build 15063 and later), due to possible UIA Core problem, toasts are announced repeatedly if UWP apps were used for a while.
	# Therefore, have a private toast message consultant (toast timestamp and UIA element runtime ID) handy.
	_lastToastTimestamp = None
	_lastToastRuntimeID = None

	def event_UIA_window_windowOpen(self):
		if winVersion.getWinVer() >= winVersion.WIN10_1703:
			toastTimestamp = time.time()
			toastRuntimeID = self.UIAElement.getRuntimeID()
			if toastRuntimeID == self._lastToastRuntimeID and toastTimestamp-self._lastToastTimestamp < 1.0:
				return
			self.__class__._lastToastTimestamp = toastTimestamp
			self.__class__._lastToastRuntimeID = toastRuntimeID
		Notification.event_alert(self)


class ToolTip(ToolTip, UIA):

	event_UIA_toolTipOpened=ToolTip.event_show


#WpfTextView fires name state changes once a second, plus when IUIAutomationTextRange::GetAttributeValue is called.
#This causes major lags when using this control with Braille in NVDA. (#2759) 
#For now just ignore the events.
class WpfTextView(UIA):

	def event_nameChange(self):
		return

	def event_stateChange(self):
		return

class SearchField(EditableTextWithSuggestions, UIA):
	"""An edit field that presents suggestions based on a search term.
	"""

	def event_UIA_controllerFor(self):
		# Only useful if suggestions appear and disappear.
		if self == api.getFocusObject() and len(self.controllerFor)>0:
			self.event_suggestionsOpened()
		else:
			self.event_suggestionsClosed()


class SuggestionsList(UIA):
	"""A list of suggestions in response to search terms being entered.
	This list shows suggestions without selecting the top suggestion.
	Examples include suggestions lists in modern apps such as Settings app in Windows 10 and later.
	"""

	def event_UIA_layoutInvalidated(self):
		# #12790: announce number of items found
		if self.childCount == 0:
			return
		# In some cases, suggestions list fires layout invalidated event repeatedly.
		# This is the case with Microsoft Store's search field.
		speech.cancelSpeech()
		# Item count must be the last one spoken.
		suggestionsCount: int = self.childCount
		suggestionsMessage = (
			# Translators: part of the suggestions count message for one suggestion.
			_("1 suggestion")
			# Translators: part of the suggestions count message (for example: 2 suggestions).
			if suggestionsCount == 1 else _("{} suggestions").format(suggestionsCount)
		)
		ui.message(suggestionsMessage)


class SuggestionListItem(UIA):
	"""Recent Windows releases use suggestions lists for various things, including Start menu suggestions, Store, Settings app and so on.
	Unlike suggestions list class, top suggestion is automatically selected.
	"""

	role = controlTypes.Role.LISTITEM

	def event_UIA_elementSelected(self):
		focusControllerFor = api.getFocusObject().controllerFor
		if len(focusControllerFor) > 0 and focusControllerFor[0].appModule is self.appModule and self.name:
			speech.cancelSpeech()
			api.setNavigatorObject(self, isFocus=True)
			self.reportFocus()
			# Display results as flash messages.
			braille.handler.message(braille.getPropertiesBraille(
				name=self.name, role=self.role, positionInfo=self.positionInfo
			))

# NetUIDropdownAnchor comboBoxes (such as in the MS Office Options dialog)
class NetUIDropdownAnchor(UIA):

	def _get_name(self):
		name=super(NetUIDropdownAnchor,self).name
		# In MS Office 2010, these combo boxes had no name.
		# However, the name can be found as the direct previous sibling label element. 
		if not name and self.previous and self.previous.role==controlTypes.Role.STATICTEXT:
			name=self.previous.name
		return name

class PlaceholderNetUITWMenuItem(UIA):
	""" Bounces focus from a netUI dead placeholder menu item when no item is selected up to the menu itself."""

	shouldAllowUIAFocusEvent=True

	def _get_focusRedirect(self):
		# Locate the containing menu and focus that instead.
		parent=self.parent
		for count in range(4):
			if not parent:
				return
			if parent.role==controlTypes.Role.POPUPMENU:
				return parent
			parent=parent.parent


class DevExpressXtraRichEdit(UIA):
	""""At least some versions of the DevExpress Xtra Rich Edit control
	have a broken implementation of the UIA Text Pattern.
	Work around this by checking whether the document range is valid.
	"""

	def _get_TextInfo(self):
		if self.UIATextPattern and self.UIATextPattern.DocumentRange:
			return super().TextInfo
		return super(UIA, self).TextInfo


class ProgressBar(UIA, ProgressBar):
	"""#12727: In the past, UIA progress bars could have a different range than what could be expected
	from a progress bar, i.e. a percentage from 0 to 100.
	This overlay class ensures that the reported value wil be between the accepted range of progress bar values.
	"""

	def _get_value(self) -> typing.Optional[str]:
		val = self.UIARangeValue
		if val is None:
			return self.UIAValue
		minVal = self._getUIACacheablePropertyValue(UIAHandler.UIA_RangeValueMinimumPropertyId, False)
		maxVal = self._getUIACacheablePropertyValue(UIAHandler.UIA_RangeValueMaximumPropertyId, False)
		if minVal == maxVal:
			# There is no range, use the raw value from the pattern, it might be incorrect.
			pass
		else:
			val = ((val - minVal) / (maxVal - minVal)) * 100.0
		return f"{round(val)}%"
