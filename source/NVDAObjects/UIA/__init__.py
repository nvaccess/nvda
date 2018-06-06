#NVDAObjects/UIA/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2018 NV Access Limited, Joseph Lee, Mohammad Suliman, Babbage B.V.

"""Support for UI Automation (UIA) controls."""

from ctypes import byref
from ctypes.wintypes import POINT, RECT
from comtypes import COMError
from comtypes.automation import VARIANT
import time
import weakref
import sys
import numbers
import colors
import languageHandler
import UIAHandler
import globalVars
import eventHandler
import controlTypes
import config
import speech
import api
import textInfos
from logHandler import log
from UIAUtils import *
from NVDAObjects.window import Window
from NVDAObjects import NVDAObjectTextInfo, InvalidNVDAObject
from NVDAObjects.behaviors import ProgressBar, EditableTextWithoutAutoSelectDetection, Dialog, Notification, EditableTextWithSuggestions
import braille
import time
from locationHelper import RectLTWH
import ui

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
		UIAHandler.UIA_RangeValueMinimumPropertyId,
		UIAHandler.UIA_RangeValueMaximumPropertyId,
		UIAHandler.UIA_ValueValuePropertyId,
		UIAHandler.UIA_PositionInSetPropertyId,
		UIAHandler.UIA_SizeOfSetPropertyId,
		UIAHandler.UIA_AriaRolePropertyId,
		UIAHandler.UIA_LandmarkTypePropertyId,
		UIAHandler.UIA_AriaPropertiesPropertyId,
		UIAHandler.UIA_LevelPropertyId,
		UIAHandler.UIA_IsEnabledPropertyId,
	} if UIAHandler.isUIAAvailable else set()

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
	] if UIAHandler.isUIAAvailable else []

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
		@ param textRange: the text range whos formatting should be fetched.
		@type textRange: L{UIAutomation.IUIAutomationTextRange}
		@param formatConfig: the types of formatting requested.
		@ type formatConfig: a dictionary of NVDA document formatting configuration keys with values set to true for those types that should be fetched.
		@param ignoreMixedValues: If True, formatting that is mixed according to UI Automation will not be included. If False, L{UIAUtils.MixedAttributeError} will be raised if UI Automation gives back a mixed attribute value signifying that the caller may want to try again with a smaller range. 
		@type: bool
		@return: The formatting for the given text range.
		@rtype: L{textInfos.FormatField}
		"""
		formatField=textInfos.FormatField()
		if not isinstance(textRange,UIAHandler.IUIAutomationTextRange):
			raise ValueError("%s is not a text range"%textRange)
		fetchAnnotationTypes=False
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
				IDs.update({UIAHandler.UIA_FontWeightAttributeId,UIAHandler.UIA_IsItalicAttributeId,UIAHandler.UIA_UnderlineStyleAttributeId,UIAHandler.UIA_StrikethroughStyleAttributeId,UIAHandler.UIA_IsSuperscriptAttributeId,UIAHandler.UIA_IsSubscriptAttributeId,})
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
			if formatConfig["reportSpellingErrors"] or formatConfig["reportComments"] or formatConfig["reportRevisions"]:
				fetchAnnotationTypes=True
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
			textPosition=None
			val=fetcher.getValue(UIAHandler.UIA_IsSuperscriptAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue and val:
				textPosition='super'
			else:
				val=fetcher.getValue(UIAHandler.UIA_IsSubscriptAttributeId,ignoreMixedValues=ignoreMixedValues)
				if val!=UIAHandler.handler.reservedNotSupportedValue and val:
					textPosition="sub"
				else:
					textPosition="baseline"
			if textPosition:
				formatField['text-position']=textPosition
		if formatConfig['reportStyle']:
			val=fetcher.getValue(UIAHandler.UIA_StyleNameAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField["style"]=val
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
			if UIAHandler.StyleId_Heading1<=styleIDValue<=UIAHandler.StyleId_Heading9: 
				formatField["heading-level"]=(styleIDValue-UIAHandler.StyleId_Heading1)+1
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
				if UIAHandler.AnnotationType_Comment in annotationTypes:
					formatField["comment"]=True
			if formatConfig["reportRevisions"]:
				if UIAHandler.AnnotationType_InsertionChange in annotationTypes:
					formatField["revision-insertion"]=True
				elif UIAHandler.AnnotationType_DeletionChange in annotationTypes:
					formatField["revision-deletion"]=True
		cultureVal=fetcher.getValue(UIAHandler.UIA_CultureAttributeId,ignoreMixedValues=ignoreMixedValues)
		if cultureVal and isinstance(cultureVal,int):
			try:
				formatField['language']=languageHandler.windowsLCIDToLocaleName(cultureVal)
			except:
				log.debugWarning("language error",exc_info=True)
				pass
		return textInfos.FieldCommand("formatChange",formatField)

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
		elif isinstance(position,textInfos.Point):
			#rangeFromPoint used to cause a freeze in UIA client library!
			p=POINT(position.x,position.y)
			self._rangeObj=self.obj.UIATextPattern.RangeFromPoint(p)
		elif isinstance(position,UIAHandler.IUIAutomationTextRange):
			self._rangeObj=position.clone()
		else:
			raise ValueError("Unknown position %s"%position)

	def __eq__(self,other):
		if self is other: return True
		if self.__class__ is not other.__class__: return False
		return bool(self._rangeObj.compare(other._rangeObj))

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
		children=getChildrenWithCacheFromUIATextRange(tempRange,UIAHandler.handler.baseCacheRequest)
		if children.length==1:
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
	} if UIAHandler.isUIAAvailable else None


	def _getControlFieldForObject(self, obj,isEmbedded=False,startOfNode=False,endOfNode=False):
		"""
		Fetch control field information for the given UIA NVDAObject.
		@ param obj: the NVDAObject the control field is for.
		@type obj: L{UIA}
		@param isEmbedded: True if this NVDAObject is for a leaf node (has no useful children).
		@ type isEmbedded: bool
		@param startOfNode: True if the control field represents the very start of this object.
		@type startOfNode: bool
		@param endOfNode: True if the control field represents the very end of this object.
		@type endOfNode: bool
		@return: The control field for this object
		@rtype: textInfos.ControlField containing NVDA control field data.
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
		states.discard(controlTypes.STATE_EDITABLE)
		states.discard(controlTypes.STATE_MULTILINE)
		states.discard(controlTypes.STATE_FOCUSED)
		field["states"] = states
		field['nameIsContent']=nameIsContent=obj.UIAElement.cachedControlType in self.UIAControlTypesWhereNameIsContent
		if not nameIsContent:
			field['name']=obj.name
		field["description"] = obj.description
		field["level"] = obj.positionInfo.get("level")
		if role == controlTypes.ROLE_TABLE:
			field["table-id"] = runtimeID
			try:
				field["table-rowcount"] = obj.rowCount
				field["table-columncount"] = obj.columnCount
			except NotImplementedError:
				pass
		if role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_DATAITEM,controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER,controlTypes.ROLE_HEADERITEM):
			try:
				field["table-rownumber"] = obj.rowNumber
				field["table-rowsspanned"] = obj.rowSpan
				field["table-columnnumber"] = obj.columnNumber
				field["table-columnsspanned"] = obj.columnSpan
				field["table-id"] = obj.table.UIAElement.getRuntimeId()
				field['role']=controlTypes.ROLE_TABLECELL
				field['table-columnheadertext']=obj.columnHeaderText
				field['table-rowheadertext']=obj.rowHeaderText
			except NotImplementedError:
				pass
		return field

	def _getTextFromUIARange(self,range):
		"""
		Fetches plain text from the given UI Automation text range.
		Just calls getText(-1). This only exists to be overridden for filtering.
		"""
		return range.getText(-1)

	def _getTextWithFields_text(self,textRange,formatConfig,UIAFormatUnits=None):
		"""
		Yields format fields and text for the given UI Automation text range, split up by the first available UI Automation text unit that does not result in mixed attribute values.
		@param textRange: the UI Automation text range to walk.
		@type textRange: L{UIAHandler.IUIAutomationTextRange}
		@param formatConfig: the types of formatting requested.
		@ type formatConfig: a dictionary of NVDA document formatting configuration keys with values set to true for those types that should be fetched.
		@param UIAFormatUnits: the UI Automation text units (in order of resolution) that should be used to split the text so as to avoid mixed attribute values. This is None by default.
			If the parameter is a list of 1 or more units, The range will be split by the first unit in the list, and this method will be recursively run on each subrange, with the remaining units in this list given as the value of this parameter. 
			If this parameter is an empty list, then formatting and text is fetched for the entire range, but any mixed attribute values are ignored and no splitting occures.
			If this parameter is None, text and formatting is fetched for the entire range in one go, but if mixed attribute values are found, it will split by the first unit in self.UIAFormatUnits, and run this method recursively on each subrange, providing the remaining units from self.UIAFormatUnits as the value of this parameter. 
		@type UIAFormatUnits: List of UI Automation Text Units or None
		@rtype: a Generator yielding L{textInfos.FieldCommand} objects containing L{textInfos.FormatField} objects, and text strings.
		"""
		log.debug("_getTextWithFields_text start")
		if UIAFormatUnits:
			unit=UIAFormatUnits[0]
			furtherUIAFormatUnits=UIAFormatUnits[1:]
		else:
			# Fetching text and formatting from the entire range will be tried once before any possible splitting.
			unit=None
			furtherUIAFormatUnits=self.UIAFormatUnits if UIAFormatUnits is None else []
		log.debug("Walking by unit %s"%unit)
		log.debug("With further units of: %s"%furtherUIAFormatUnits)
		rangeIter=iterUIARangeByUnit(textRange,unit) if unit is not None else [textRange]
		for tempRange in rangeIter:
			text=self._getTextFromUIARange(tempRange)
			if text:
				log.debug("Chunk has text. Fetching formatting")
				try:
					field=self._getFormatFieldAtRange(tempRange,formatConfig,ignoreMixedValues=len(furtherUIAFormatUnits)==0)
				except UIAMixedAttributeError:
					log.debug("Mixed formatting. Trying higher resolution unit")
					for subfield in self._getTextWithFields_text(tempRange,formatConfig,UIAFormatUnits=furtherUIAFormatUnits):
						yield subfield
					log.debug("Done yielding higher resolution unit")
					continue
				log.debug("Yielding formatting and text")
				yield field
				yield text
		log.debug("Done _getTextWithFields_text")

	def _getTextWithFieldsForUIARange(self,rootElement,textRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True,_rootElementClipped=(True,True)):
		"""
		Yields start and end control fields, and text, for the given UI Automation text range.
		@param rootElement: the highest ancestor that encloses the given text range. This function will not walk higher than this point.
		@type rootElement: L{UIAHandler.IUIAutomation}
		@param textRange: the UI Automation text range whos content should be fetched.
		@type textRange: L{UIAHandler.IUIAutomation}
		@param formatConfig: the types of formatting requested.
		@ type formatConfig: a dictionary of NVDA document formatting configuration keys with values set to true for those types that should be fetched.
		@param includeRoot: If true, then a control start and end will be yielded for the root element.
		@ type includeRoot: bool
		@param alwaysWalkAncestors: If true then control fields will be yielded for any element enclosing the given text range, that is a descendant of the root element. If false then the root element may be  assumed to be the only ancestor.
		@type alwaysWalkAncestors: bool
		@param recurseChildren: If true, this function will be recursively called for each child of the given text range, clipped to the bounds of this text range. Formatted text between the children will also be yielded. If false, only formatted text will be yielded.
		@type recurseChildren: bool
		@param _rootElementClipped: Indicates if textRange represents all of the given rootElement, or is clipped at the start or end.
		@type _rootElementClipped: 2-tuple
		@rtype: A generator that yields L{textInfo.FieldCommand} objects and text strings.
		"""
		
		if log.isEnabledFor(log.DEBUG):
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
			log.debug("Fetching parents starting from enclosingElement")
			try:
				parentElement=getEnclosingElementWithCacheFromUIATextRange(textRange,self._controlFieldUIACacheRequest)
			except COMError:
				parentElement=None
			while parentElement:
				isRoot=UIAHandler.handler.clientObject.compareElements(parentElement,rootElement)
				if isRoot:
					log.debug("Hit root")
					parentElements.append((parentElement,_rootElementClipped))
					break
				else:
					if log.isEnabledFor(log.DEBUG):
						log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
					try:
						parentRange=self.obj.UIATextPattern.rangeFromChild(parentElement)
					except COMError:
						parentRange=None
					if not parentRange:
						log.debug("parentRange is NULL. Breaking")
						break
					clippedStart=textRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,parentRange,UIAHandler.TextPatternRangeEndpoint_Start)>0
					clippedEnd=textRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,parentRange,UIAHandler.TextPatternRangeEndpoint_End)<0
					parentElements.append((parentElement,(clippedStart,clippedEnd)))
				parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,self._controlFieldUIACacheRequest)
		else:
			parentElements.append((rootElement,_rootElementClipped))
		log.debug("Done fetching parents")
		enclosingElement=parentElements[0][0] if parentElements else rootElement
		if not includeRoot and parentElements:
			del parentElements[-1]
		parentFields=[]
		log.debug("Generating controlFields for parents")
		windowHandle=self.obj.windowHandle
		controlFieldNVDAObjectClass=self.controlFieldNVDAObjectClass
		for index,(parentElement,parentClipped) in enumerate(parentElements):
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			startOfNode=not parentClipped[0]
			endOfNode=not parentClipped[1]
			try:
				obj=controlFieldNVDAObjectClass(windowHandle=windowHandle,UIAElement=parentElement,initialUIACachedPropertyIDs=self._controlFieldUIACachedPropertyIDs)
				field=self._getControlFieldForObject(obj,isEmbedded=(index==0 and not recurseChildren),startOfNode=startOfNode,endOfNode=endOfNode)
			except LookupError:
				log.debug("Failed to fetch controlField data for parentElement. Breaking")
				continue
			if not field:
				continue
			parentFields.append(field)
		log.debug("Done generating controlFields for parents")
		log.debug("Yielding control starts for parents")
		for field in reversed(parentFields):
			yield textInfos.FieldCommand("controlStart",field)
		log.debug("Done yielding control starts for parents")
		del parentElements
		log.debug("Yielding balanced fields for textRange")
		# Move through the text range, collecting text and recursing into children
		#: This variable is used to   span lengths of plain text between child ranges as we iterate over getChildren
		childCount=childElements.length if recurseChildren else 0
		if childCount>0:
			tempRange=textRange.clone()
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)
			if log.isEnabledFor(log.DEBUG):
				log.debug("Child count: %s"%childElements.length)
				log.debug("Walking children")
			lastChildIndex=childCount-1
			lastChildEndDelta=0
			documentTextPattern=self.obj.UIATextPattern
			for index in xrange(childCount):
				childElement=childElements.getElement(index)
				if not childElement or UIAHandler.handler.clientObject.compareElements(childElement,enclosingElement):
					log.debug("NULL childElement. Skipping")
					continue
				if log.isEnabledFor(log.DEBUG):
					log.debug("Fetched child %s (%s)"%(index,childElement.currentLocalizedControlType))
				try:
					childRange=documentTextPattern.rangeFromChild(childElement)
				except COMError as e:
					log.debug("rangeFromChild failed with %s"%e)
					childRange=None
				if not childRange:
					log.debug("NULL childRange. Skipping")
					continue
				clippedStart=clippedEnd=False
				if index==lastChildIndex and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_End)>=0:
					log.debug("Child at or past end of textRange. Breaking")
					break
				if index==lastChildIndex:
					lastChildEndDelta=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
					if lastChildEndDelta>0:
						log.debug("textRange ended part way through the child. Crop end of childRange to fit")
						childRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
						clippedEnd=True
				childStartDelta=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
				if childStartDelta>0:
					# plain text before this child
					tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
					log.debug("Plain text before child")
					for field in self._getTextWithFields_text(tempRange,formatConfig):
						yield field
				elif childStartDelta<0:
					log.debug("textRange started part way through child. Cropping Start of child range to fit" )
					childRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
					clippedStart=True
				if (index==0 or index==lastChildIndex) and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)==0:
					log.debug("childRange is degenerate. Skipping")
					continue
				log.debug("Recursing into child %s"%index)
				for field in self._getTextWithFieldsForUIARange(childElement,childRange,formatConfig,includeRoot=True,alwaysWalkAncestors=False,_rootElementClipped=(clippedStart,clippedEnd)):
					yield field
				log.debug("Done recursing into child %s"%index)
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)
			log.debug("children done")
			# Plain text after the final child
			if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_End)<0:
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
				log.debug("Yielding final text")
				for field in self._getTextWithFields_text(tempRange,formatConfig):
					yield field
		else: #no children 
			log.debug("no children")
			log.debug("Yielding text") 
			for field in self._getTextWithFields_text(textRange,formatConfig):
				yield field
		for field in parentFields:
			log.debug("Yielding controlEnd for parentElement")
			yield textInfos.FieldCommand("controlEnd",field)
		log.debug("_getTextWithFieldsForUIARange end")

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		fields=list(self._getTextWithFieldsForUIARange(self.obj.UIAElement,self._rangeObj,formatConfig))
		return fields

	def _get_text(self):
		return self._getTextFromUIARange(self._rangeObj)

	def _getBoundingRectsFromUIARange(self,range):
		"""
		Fetches per line bounding rectangles from the given UI Automation text range.
		Note that if the range object doesn't cover a whole line (e.g. a character),
		the bounding rectangle will be restriked to the range.
		@rtype: [locationHelper.RectLTWH]
		"""
		rects = []
		rectArray = range.GetBoundingRectangles()
		if not rectArray:
			return rects
		rects.extend(
			RectLTWH.fromFloatCollection(*rectArray[i:i+4])
			for i in xrange(0, len(rectArray), 4)
		)
		return rects

	def _get_boundingRect(self):
		rects = self._getBoundingRectsFromUIARange(self._rangeObj)
		if not rects:
			raise LookupError
		return RectLTWH.fromCollection(*rects)

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
		cacheElement=self.UIAElement.buildUpdatedCache(cacheRequest)
		for ID in IDs:
			elementCache[ID]=cacheElement

	def findOverlayClasses(self,clsList):
		UIAControlType=self.UIAElement.cachedControlType
		UIAClassName=self.UIAElement.cachedClassName
		if UIAClassName=="WpfTextView":
			clsList.append(WpfTextView)
		elif self.TextInfo==UIATextInfo and (UIAClassName=='_WwG' or self.windowClassName=='_WwG' or self.UIAElement.cachedAutomationID.startswith('UIA_AutomationId_Word_Content')):
			from .wordDocument import WordDocument, WordDocumentNode
			if self.role==controlTypes.ROLE_DOCUMENT:
				clsList.append(WordDocument)
			else:
				clsList.append(WordDocumentNode)
		# #5136: Windows 8.x and Windows 10 uses different window class and other attributes for toast notifications.
		elif UIAClassName=="ToastContentHost" and UIAControlType==UIAHandler.UIA_ToolTipControlTypeId: #Windows 8.x
			clsList.append(Toast_win8)
		elif self.windowClassName=="Windows.UI.Core.CoreWindow" and UIAControlType==UIAHandler.UIA_WindowControlTypeId and "ToastView" in self.UIAElement.cachedAutomationId: # Windows 10
			clsList.append(Toast_win10)
		elif self.UIAElement.cachedFrameworkID in ("InternetExplorer","MicrosoftEdge"):
			import edge
			if UIAClassName in ("Internet Explorer_Server","WebView") and self.role==controlTypes.ROLE_PANE:
				clsList.append(edge.EdgeHTMLRootContainer)
			elif (self.UIATextPattern and
				# #6998: Edge normally gives its root node a controlType of pane, but ARIA role="document"  changes the controlType to document
				self.role in (controlTypes.ROLE_PANE,controlTypes.ROLE_DOCUMENT) and 
				self.parent and (isinstance(self.parent,edge.EdgeHTMLRootContainer) or not isinstance(self.parent,edge.EdgeNode))
			): 
				clsList.append(edge.EdgeHTMLRoot)
			elif self.role==controlTypes.ROLE_LIST:
				clsList.append(edge.EdgeList)
			else:
				clsList.append(edge.EdgeNode)
		elif self.role==controlTypes.ROLE_DOCUMENT and self.UIAElement.cachedAutomationId=="Microsoft.Windows.PDF.DocumentView":
				# PDFs
				import edge
				clsList.append(edge.EdgeHTMLRoot)
		if UIAControlType==UIAHandler.UIA_ProgressBarControlTypeId:
			clsList.append(ProgressBar)
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
		elif UIAControlType==UIAHandler.UIA_ComboBoxControlTypeId:
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
		# In Windows 10, allow Start menu search box and Edge's address omnibar to participate in announcing appearance of auto-suggestions.
		if self.UIAElement.cachedAutomationID in ("SearchTextBox", "TextBox", "addressEditBox"):
			clsList.append(SearchField)
		try:
			# Nested block here in order to catch value error and variable binding error when attempting to access automation ID for invalid elements.
			try:
				# #6241: Raw UIA base tree walker is better than simply looking at self.parent when locating suggestion list items.
				parentElement=UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
				# Sometimes, fetching parent (list control) via base tree walker fails, especially when dealing with suggestions in Windows10 Start menu.
				# Oddly, we need to take care of context menu for Start search suggestions as well.
				if parentElement.cachedAutomationId.lower() in ("suggestionslist", "contextmenu"):
					clsList.append(SuggestionListItem)
			except COMError:
				pass
		except ValueError:
			pass

		# Add editableText support if UIA supports a text pattern
		if self.TextInfo==UIATextInfo:
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
	def kwargsFromSuper(cls,kwargs,relation=None):
		UIAElement=None
		windowHandle=kwargs.get('windowHandle')
		if isinstance(relation,tuple):
			UIAElement=UIAHandler.handler.clientObject.ElementFromPointBuildCache(POINT(relation[0],relation[1]),UIAHandler.handler.baseCacheRequest)
		elif relation=="focus":
			try:
				UIAElement=UIAHandler.handler.clientObject.getFocusedElementBuildCache(UIAHandler.handler.baseCacheRequest)
				# This object may be in a different window, so we need to recalculate the window handle.
				kwargs['windowHandle']=None
			except COMError:
				log.debugWarning("getFocusedElement failed", exc_info=True)
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

	def _get_UIATogglePattern(self):
		self.UIATogglePattern=self._getUIAPattern(UIAHandler.UIA_TogglePatternId,UIAHandler.IUIAutomationTogglePattern)
		return self.UIATogglePattern

	def _get_UIASelectionItemPattern(self):
		self.UIASelectionItemPattern=self._getUIAPattern(UIAHandler.UIA_SelectionItemPatternId,UIAHandler.IUIAutomationSelectionItemPattern)
		return self.UIASelectionItemPattern

	def _get_UIATextPattern(self):
		self.UIATextPattern=self._getUIAPattern(UIAHandler.UIA_TextPatternId,UIAHandler.IUIAutomationTextPattern,cache=True)
		return self.UIATextPattern

	def _get_UIATextEditPattern(self):
		if not isinstance(UIAHandler.handler.clientObject,UIAHandler.IUIAutomation3):
			return None
		self.UIATextEditPattern=self._getUIAPattern(UIAHandler.UIA_TextEditPatternId,UIAHandler.IUIAutomationTextEditPattern,cache=False)
		return self.UIATextEditPattern

	def _get_UIALegacyIAccessiblePattern(self):
		self.UIALegacyIAccessiblePattern=self._getUIAPattern(UIAHandler.UIA_LegacyIAccessiblePatternId,UIAHandler.IUIAutomationLegacyIAccessiblePattern)
		return self.UIALegacyIAccessiblePattern

	_TextInfo=UIATextInfo
	def _get_TextInfo(self):
		if self.UIATextPattern: return self._TextInfo
		textInfo=super(UIA,self).TextInfo
		if textInfo is NVDAObjectTextInfo and self.UIAIsWindowElement and self.role==controlTypes.ROLE_WINDOW:
			import displayModel
			return displayModel.DisplayModelTextInfo
		return textInfo

	def setFocus(self):
		self.UIAElement.setFocus()

	def _get_devInfo(self):
		info=super(UIA,self).devInfo
		info.append("UIAElement: %r"%self.UIAElement)
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
			(const, name) for name, const in UIAHandler.__dict__.iteritems()
			if name.startswith("UIA_Is") and name.endswith("PatternAvailablePropertyId")
		)
		self._prefetchUIACacheForPropertyIDs(list(patternAvailableConsts))
		for const, name in patternAvailableConsts.iteritems():
			try:
				res = self._getUIACacheablePropertyValue(const)
			except COMError:
				res = False
			if res:
				# Every name has the same format, so the string indexes can be safely hardcoded here.
				patternsAvailable.append(name[6:-19])
		info.append("UIA patterns available: %s"%", ".join(patternsAvailable))
		return info

	def _get_name(self):
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_NamePropertyId)
		except COMError:
			return ""

	def _get_role(self):
		role=UIAHandler.UIAControlTypesToNVDARoles.get(self.UIAElement.cachedControlType,controlTypes.ROLE_UNKNOWN)
		if role==controlTypes.ROLE_BUTTON:
			try:
				s=self._getUIACacheablePropertyValue(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
			except COMError:
				s=UIAHandler.handler.reservedNotSupportedValue
			if s!=UIAHandler.handler.reservedNotSupportedValue:
				role=controlTypes.ROLE_TOGGLEBUTTON
		elif role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_PANE,controlTypes.ROLE_WINDOW) and self.windowHandle:
			superRole=super(UIA,self).role
			if superRole!=controlTypes.ROLE_WINDOW:
				role=superRole
		return role

	def _get_description(self):
		try:
			return self._getUIACacheablePropertyValue(UIAHandler.UIA_HelpTextPropertyId) or ""
		except COMError:
			return ""

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
	}  if UIAHandler.isUIAAvailable else set()

	def _get_states(self):
		states=set()
		self._prefetchUIACacheForPropertyIDs(self._UIAStatesPropertyIDs)
		try:
			hasKeyboardFocus=self._getUIACacheablePropertyValue(UIAHandler.UIA_HasKeyboardFocusPropertyId)
		except COMError:
			hasKeyboardFocus=False
		if hasKeyboardFocus:
			states.add(controlTypes.STATE_FOCUSED)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsKeyboardFocusablePropertyId):
			states.add(controlTypes.STATE_FOCUSABLE)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsPasswordPropertyId):
			states.add(controlTypes.STATE_PROTECTED)
		# Don't fetch the role unless we must, but never fetch it more than once.
		role=None
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId):
			role=self.role
			states.add(controlTypes.STATE_CHECKABLE if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTABLE)
			if self._getUIACacheablePropertyValue(UIAHandler.UIA_SelectionItemIsSelectedPropertyId):
				states.add(controlTypes.STATE_CHECKED if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTED)
		if not self._getUIACacheablePropertyValue(UIAHandler.UIA_IsEnabledPropertyId,True):
			states.add(controlTypes.STATE_UNAVAILABLE)
		try:
			isOffScreen = self._getUIACacheablePropertyValue(UIAHandler.UIA_IsOffscreenPropertyId)
		except COMError:
			isOffScreen = False
		if isOffScreen:
			states.add(controlTypes.STATE_OFFSCREEN)
		try:
			isDataValid=self._getUIACacheablePropertyValue(UIAHandler.UIA_IsDataValidForFormPropertyId,True)
		except COMError:
			isDataValid=UIAHandler.handler.reservedNotSupportedValue
		if not isDataValid:
			states.add(controlTypes.STATE_INVALID_ENTRY)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsRequiredForFormPropertyId):
			states.add(controlTypes.STATE_REQUIRED)
		try:
			isReadOnly=self._getUIACacheablePropertyValue(UIAHandler.UIA_ValueIsReadOnlyPropertyId,True)
		except COMError:
			isReadOnly=UIAHandler.handler.reservedNotSupportedValue
		if isReadOnly and isReadOnly!=UIAHandler.handler.reservedNotSupportedValue:
			states.add(controlTypes.STATE_READONLY)
		try:
			s=self._getUIACacheablePropertyValue(UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if s==UIAHandler.ExpandCollapseState_Collapsed:
				states.add(controlTypes.STATE_COLLAPSED)
			elif s==UIAHandler.ExpandCollapseState_Expanded:
				states.add(controlTypes.STATE_EXPANDED)
		try:
			s=self._getUIACacheablePropertyValue(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if not role:
				role=self.role
			if role==controlTypes.ROLE_TOGGLEBUTTON:
				if s==UIAHandler.ToggleState_On:
					states.add(controlTypes.STATE_PRESSED)
			else:
				states.add(controlTypes.STATE_CHECKABLE)
				if s==UIAHandler.ToggleState_On:
					states.add(controlTypes.STATE_CHECKED)
		return states

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

	def _get_next(self):
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

	def _get_children(self):
		childrenCacheRequest=UIAHandler.handler.baseCacheRequest.clone()
		childrenCacheRequest.TreeScope=UIAHandler.TreeScope_Children
		try:
			cachedChildren=self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		except COMError as e:
			log.debugWarning("Could not fetch cached children from UIA element: %s"%e)
			return super(UIA,self).children
		children=[]
		if not cachedChildren:
			# GetCachedChildren returns null if there are no children.
			return children
		for index in xrange(cachedChildren.length):
			e=cachedChildren.getElement(index)
			windowHandle=self.windowHandle
			children.append(self.correctAPIForRelation(UIA(windowHandle=windowHandle,UIAElement=e)))
		return children

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

	def _get_rowHeaderText(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_TableItemRowHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in xrange(val.length):
			e=val.getElement(i)
			if UIAHandler.handler.clientObject.compareElements(e,self.UIAElement):
				continue
			obj=UIA(windowHandle=self.windowHandle,UIAElement=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
			if not obj: continue
			text=obj.makeTextInfo(textInfos.POSITION_ALL).text
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
		for i in xrange(val.length):
			e=val.getElement(i)
			if UIAHandler.handler.clientObject.compareElements(e,self.UIAElement):
				continue
			obj=UIA(windowHandle=self.windowHandle,UIAElement=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
			if not obj: continue
			text=obj.makeTextInfo(textInfos.POSITION_ALL).text
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
		return self.UIAElement.cachedProcessId

	def _get_location(self):
		try:
			r=self._getUIACacheablePropertyValue(UIAHandler.UIA_BoundingRectanglePropertyId)
		except COMError:
			return None
		if r is None:
			return
		# r is a tuple of floats representing left, top, width and height.
		return RectLTWH.fromFloatCollection(*r)

	def _get_value(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_RangeValueValuePropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			minVal=self._getUIACacheablePropertyValue(UIAHandler.UIA_RangeValueMinimumPropertyId,False)
			maxVal=self._getUIACacheablePropertyValue(UIAHandler.UIA_RangeValueMaximumPropertyId,False)
			if minVal==maxVal:
				# There is no range.
				return "0"
			val=((val-minVal)/(maxVal-minVal))*100.0
			return "%d"%round(val,4)
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_ValueValuePropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val

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
		for index in xrange(a.length):
			e=a.getElement(index)
			e=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
			obj=UIA(UIAElement=e)
			if obj:
				objList.append(obj)
		return objList

	def event_UIA_elementSelected(self):
		self.event_stateChange()

	def event_valueChange(self):
		if isinstance(self, EditableTextWithoutAutoSelectDetection):
			return
		return super(UIA, self).event_valueChange()

	def event_UIA_systemAlert(self):
		"""
		A base implementation for UI Automation's system Alert event.
		This just reports the element that received the alert in speech and braille, similar to how focus is presented.
		Skype for business toast notifications being one example.
		"""
		speech.speakObject(self, reason=controlTypes.REASON_FOCUS)
		# Ideally, we wouldn't use getBrailleTextForProperties directly.
		braille.handler.message(braille.getBrailleTextForProperties(name=self.name, role=self.role))

	def event_UIA_notification(self, notificationKind=None, notificationProcessing=None, displayString=None, activityId=None):
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
			if not parent or parent==obj or parent.role!=controlTypes.ROLE_TREEVIEWITEM:
				return level
			obj=parent
		return level

	def _get_positionInfo(self):
		info=super(TreeviewItem,self).positionInfo or {}
		info['level']=self._level
		return info

class UIColumnHeader(UIA):

	def _get_description(self):
		description=super(UIColumnHeader,self).description
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
			itemIndex=self._getUIACacheablePropertyValue(UIAHandler.handler.ItemIndex_PropertyId)
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
					itemCount=e.getCurrentPropertyValue(UIAHandler.handler.ItemCount_PropertyId)
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
			speech.speakObjectProperties(self,value=True,reason=controlTypes.REASON_CHANGE)
		else:
			super(SensitiveSlider,self).event_valueChange()

class ControlPanelLink(UIA):

	def _get_description(self):
		desc=super(ControlPanelLink,self).description
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
	role=controlTypes.ROLE_DIALOG

class Toast_win8(Notification, UIA):

	event_UIA_toolTipOpened=Notification.event_alert

class Toast_win10(Notification, UIA):

	# #6096: Windows 10 build 14366 and later does not fire tooltip event when toasts appear.
	if sys.getwindowsversion().build > 10586:
		event_UIA_window_windowOpen=Notification.event_alert
	else:
		event_UIA_toolTipOpened=Notification.event_alert
	# #7128: in Creators Update (build 15063 and later), due to possible UIA Core problem, toasts are announced repeatedly if UWP apps were used for a while.
	# Therefore, have a private toast message consultant (toast timestamp and UIA element runtime ID) handy.
	_lastToastTimestamp = None
	_lastToastRuntimeID = None

	def event_UIA_window_windowOpen(self):
		if sys.getwindowsversion().build >= 15063:
			toastTimestamp = time.time()
			toastRuntimeID = self.UIAElement.getRuntimeID()
			if toastRuntimeID == self._lastToastRuntimeID and toastTimestamp-self._lastToastTimestamp < 1.0:
				return
			self.__class__._lastToastTimestamp = toastTimestamp
			self.__class__._lastToastRuntimeID = toastRuntimeID
		Notification.event_alert(self)

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


class SuggestionListItem(UIA):
	"""Recent Windows releases use suggestions lists for various things, including Start menu suggestions, Store, Settings app and so on.
	"""

	role=controlTypes.ROLE_LISTITEM

	def event_UIA_elementSelected(self):
		focusControllerFor=api.getFocusObject().controllerFor
		if len(focusControllerFor)>0 and focusControllerFor[0].appModule is self.appModule and self.name:
			speech.cancelSpeech()
			api.setNavigatorObject(self, isFocus=True)
			self.reportFocus()
			# Display results as flash messages.
			braille.handler.message(braille.getBrailleTextForProperties(name=self.name, role=self.role, positionInfo=self.positionInfo))
