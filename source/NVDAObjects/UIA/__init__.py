#NVDAObjects/UIA/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2016 NV Access Limited, Joseph Lee, Mohammad Suliman

from ctypes import byref
from ctypes.wintypes import POINT, RECT
from comtypes import COMError
import weakref
import sys
import numbers
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
from NVDAObjects.behaviors import ProgressBar, EditableTextWithoutAutoSelectDetection, Dialog, Notification
import braille

class UIATextInfo(textInfos.TextInfo):

	def _get_controlFieldNVDAObjectClass(self):
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
		UIAHandler.UIA_LocalizedLandmarkTypePropertyId,
		UIAHandler.UIA_AriaPropertiesPropertyId,
		UIAHandler.UIA_LevelPropertyId,
	} if UIAHandler.isUIAAvailable else set()

	def _get__controlFieldUIACacheRequest(self):
		cacheRequest=UIAHandler.handler.baseCacheRequest.clone()
		for ID in self._controlFieldUIACachedPropertyIDs:
			cacheRequest.addProperty(ID)
		self._controlFieldUIACacheRequest=cacheRequest
		return cacheRequest

	def _get__controlFieldUIACacheRequestWithChildren(self):
		cacheRequest=self._controlFieldUIACacheRequest.clone()
		cacheRequest.treeScope=UIAHandler.TreeScope_Subtree
		self._controlFieldUIACacheRequestWithChildren=cacheRequest
		return cacheRequest

	#: The UI Automation text units (in order of resolution) that should be used when fetching formatting.
	UIAFormatUnits=[
		UIAHandler.TextUnit_Format,
		UIAHandler.TextUnit_Word,
		UIAHandler.TextUnit_Character
	] if UIAHandler.isUIAAvailable else []

	def _getFormatFieldAtRange(self,range,formatConfig,ignoreMixedValues=False):
		"""
		Fetches formatting for the given UI Automation Text range.
		@ param range: the text range whos formatting should be fetched.
		@type range: L{UIAutomation.IUIAutomationTextRange}
		@param formatConfig: the types of formatting requested.
		@ type formatConfig: a dictionary of NVDA document formatting configuration keys with values set to true for those types that should be fetched.
		@param ignoreMixedValues: If True, formatting that is mixed according to UI Automation will not be included. If False, L{UIAUtils.MixedAttributeError} will be raised if UI Automation gives back a mixed attribute value signifying that the caller may want to try again with a smaller range. 
		@type: bool
		@return: The formatting for the given text range.
		@rtype: L{textInfos.FormatField}
		"""
		formatField=textInfos.FormatField()
		fetcher=BulkUIATextRangeAttributeValueFetcher(range,[UIAHandler.UIA_LinkAttributeId,UIAHandler.UIA_StyleIdAttributeId,UIAHandler.UIA_AnnotationTypesAttributeId])
		if formatConfig["reportFontName"]:
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_FontNameAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField["font-name"]=val
		if formatConfig["reportFontSize"]:
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_FontSizeAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,numbers.Number):
				formatField['font-size']="%g pt"%float(val)
		if formatConfig["reportFontAttributes"]:
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_FontWeightAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,int):
				formatField['bold']=(val>=700)
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_IsItalicAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['italic']=val
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_UnderlineStyleAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['underline']=bool(val)
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_StrikethroughStyleAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['strikethrough']=bool(val)
			textPosition=None
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_IsSuperscriptAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue and val:
				textPosition='super'
			else:
				val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_IsSubscriptAttributeId,ignoreMixedValues=ignoreMixedValues)
				if val!=UIAHandler.handler.reservedNotSupportedValue and val:
					textPosition="sub"
				else:
					textPosition="baseline"
			if textPosition:
				formatField['text-position']=textPosition
		if formatConfig["reportAlignment"]:
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_HorizontalTextAlignmentAttributeId,ignoreMixedValues=ignoreMixedValues)
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
			import colors
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_BackgroundColorAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,int):
				formatField['background-color']=colors.RGB.fromCOLORREF(val)
			val=getUIATextAttributeValueFromRange(range,UIAHandler.UIA_ForegroundColorAttributeId,ignoreMixedValues=ignoreMixedValues)
			if isinstance(val,int):
				formatField['color']=colors.RGB.fromCOLORREF(val)
		if formatConfig['reportLinks']:
			val=fetcher.getValue(UIAHandler.UIA_LinkAttributeId,ignoreMixedValues=ignoreMixedValues)
			if val!=UIAHandler.handler.reservedNotSupportedValue:
				if val:
					formatField['link']
		if formatConfig["reportHeadings"]:
			styleIDValue=fetcher.getValue(UIAHandler.UIA_StyleIdAttributeId,ignoreMixedValues=ignoreMixedValues)
			if UIAHandler.StyleId_Heading1<=styleIDValue<=UIAHandler.StyleId_Heading9: 
				formatField["heading-level"]=(styleIDValue-UIAHandler.StyleId_Heading1)+1
		if formatConfig["reportSpellingErrors"]:
			annotationTypes=fetcher.getValue(UIAHandler.UIA_AnnotationTypesAttributeId,ignoreMixedValues=ignoreMixedValues)
			if annotationTypes==UIAHandler.AnnotationType_SpellingError:
				formatField["invalid-spelling"]=True
		return textInfos.FieldCommand("formatChange",formatField)

	def __init__(self,obj,position,_rangeObj=None):
		super(UIATextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.clone()
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
			self._rangeObj=self.obj.UIATextPattern.documentRange
			self.collapse()
		elif position==textInfos.POSITION_LAST:
			self._rangeObj=self.obj.UIATextPattern.documentRange
			self.collapse(True)
		elif position==textInfos.POSITION_ALL:
			self._rangeObj=self.obj.UIATextPattern.documentRange
		elif isinstance(position,UIA):
			try:
				self._rangeObj=self.obj.UIATextPattern.rangeFromChild(position.UIAElement)
			except COMError:
				raise LookupError
			# sometimes rangeFromChild can return a NULL range
			if not self._rangeObj: raise LookupError
		elif isinstance(position,textInfos.Point):
			#rangeFromPoint causes a freeze in UIA client library!
			#p=POINT(position.x,position.y)
			#self._rangeObj=self.obj.UIATextPattern.RangeFromPoint(p)
			raise NotImplementedError
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
		field = textInfos.ControlField()
		role = obj.role
		# Ensure this controlField is unique to the object
		field['runtimeID']=obj.UIAElement.getRuntimeID()
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
			field["table-id"] = 1 # FIXME
			try:
				field["table-rowcount"] = obj.rowCount
				field["table-columncount"] = obj.columnCount
			except NotImplementedError:
				pass
		if role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_DATAITEM,controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER,controlTypes.ROLE_HEADERITEM):
			try:
				field["table-rownumber"] = obj.rowNumber
				field["table-columnnumber"] = obj.columnNumber
				field["table-id"] = 1 # FIXME
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

	def _getTextWithFieldsForUIARange(self,rootElement,textRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True,_rootElementRange=None,_children=None):
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
		@param _rootElementRange: Optimization argument: the actual text range for the root element, as it is usually already known when making recursive calls.
		@type rootElementRange: L{UIAHandler.IUIAutomationTextRange} 
		@param _children: Optimization argument: the children already fetched from textRange.getChildren / getChildrenBuildCache
		@type _children: UIA elementArray
		@rtype: A generator that yields L{textInfo.FieldCommand} objects and text strings.
		"""
		if log.isEnabledFor(log.DEBUG):
			log.debug("_getTextWithFieldsForUIARange")
			log.debug("rootElement: %s"%rootElement.currentLocalizedControlType if rootElement else None)
			log.debug("full text: %s"%textRange.getText(-1))
		if recurseChildren:
			childElements=_children if _children else getChildrenWithCacheFromUIATextRange(textRange,self._controlFieldUIACacheRequestWithChildren)
			# Specific check for embedded elements (checkboxes etc)
			# Calling getChildren on their childRange always gives back the same child.
			if childElements.length==1:
				childElement=childElements.getElement(0)
				if childElement and UIAHandler.handler.clientObject.compareElements(childElement,rootElement):
					log.debug("Detected embedded child")
					childElement=childElement.buildUpdatedCache(self._controlFieldUIACacheRequest)
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
				if log.isEnabledFor(log.DEBUG):
					log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
				if isRoot and not includeRoot:
					log.debug("Is root, and root not requested. Breaking")
					break
				try:
					parentRange=self.obj.UIATextPattern.rangeFromChild(parentElement)
				except COMError:
					parentRange=None
				if not parentRange:
					log.debug("parentRange is NULL. Breaking")
					break
				parentElements.append((parentElement,parentRange))
				if isRoot:
					log.debug("Hit root. Breaking")
					break
				parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,self._controlFieldUIACacheRequest)
		else: # not alwaysWalkAncestors
			if includeRoot:
				log.debug("Using rootElement as only parent")
				rootElementRange=_rootElementRange if _rootElementRange else self.obj.UIATextPattern.rangeFromChild(rootElement)
				parentElements.append((rootElement,rootElementRange))
		log.debug("Done fetching parents")
		enclosingElement=parentElements[0][0] if parentElements else rootElement
		parentFields=[]
		log.debug("Generating controlFields for parents")
		for index,(parentElement,parentRange) in enumerate(parentElements):
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			startOfNode=textRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,parentRange,UIAHandler.TextPatternRangeEndpoint_Start)<=0
			endOfNode=textRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,parentRange,UIAHandler.TextPatternRangeEndpoint_End)>=0
			try:
				obj=self.controlFieldNVDAObjectClass(windowHandle=self.obj.windowHandle,UIAElement=parentElement,initialUIACachedPropertyIDs=self._controlFieldUIACachedPropertyIDs)
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
		tempRange=textRange.clone()
		if recurseChildren:
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)
			if log.isEnabledFor(log.DEBUG):
				log.debug("Child count: %s"%childElements.length)
				log.debug("Walking children")
			childCount=childElements.length
			lastChildIndex=childCount-1
			lastChildEndDelta=0
			for index in xrange(childCount):
				childElement=childElements.getElement(index)
				if not childElement or UIAHandler.handler.clientObject.compareElements(childElement,enclosingElement):
					log.debug("NULL childElement. Skipping")
					continue
				if log.isEnabledFor(log.DEBUG):
					log.debug("Fetched child %s (%s)"%(index,childElement.currentLocalizedControlType))
				childRange=self.obj.UIATextPattern.rangeFromChild(childElement)
				if not childRange:
					log.debug("NULL childRange. Skipping")
					continue
				if index==lastChildIndex and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_End)>=0:
					log.debug("Child at or past end of textRange. Breaking")
					break
				origChildRange=childRange.clone()
				if index==lastChildIndex:
					lastChildEndDelta=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
					if lastChildEndDelta>0:
						log.debug("textRange ended part way through the child. Crop end of childRange to fit")
						childRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
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
				if (index==0 or index==lastChildIndex) and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)==0:
					log.debug("childRange is degenerate. Skipping")
					continue
				log.debug("Recursing into child %s"%index)
				for field in self._getTextWithFieldsForUIARange(childElement,childRange,formatConfig,_rootElementRange=origChildRange,includeRoot=True,alwaysWalkAncestors=False,_children=childElement.getCachedChildren()):
					yield field
				log.debug("Done recursing into child %s"%index)
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)
			log.debug("children done")
		else: #isEmbeddedChild==True
			log.debug("isEmbeddedChild, not recursing children.")
		# Plain text after the final child
		if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_End):
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
			log.debug("Yielding final text")
			for field in self._getTextWithFields_text(tempRange,formatConfig):
				yield field
		log.debug("Done yielding final text")
		log.debug("Done yielding balanced fields for textRange")
		for field in reversed(parentFields):
			log.debug("Yielding controlEnd for parentElement")
			yield textInfos.FieldCommand("controlEnd",field)
		log.debug("_getTextWithFieldsForUIARange end")

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		fields=[]
		for field in self._getTextWithFieldsForUIARange(self.obj.UIAElement,self._rangeObj,formatConfig):
			if log.isEnabledFor(log.DEBUG):
				log.debug("Field: %s"%field)
			fields.append(field)
		return fields

	def _get_text(self):
		return self._getTextFromUIARange(self._rangeObj)

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

	def _get__coreCycleUIAPropertyValueCache(self):
		"""A dictionary per core cycle, that is ready to map (propertyID,ignoreDefault) pares to property values."""
		return {}

	def _get__coreCycleUIAPropertyCacheElementCache(self):
		"""A dictionary per core cycle that is ready to map UIA property IDs to UIAElements with that property already cached."""
		return {}

	def _getUIACacheablePropertyValue(self,ID,ignoreDefault=False,onlyCached=False):
		valueCache=self._coreCycleUIAPropertyValueCache
		key=(ID,ignoreDefault)
		# If we have cached the value for this property in this core cycle already, return it.
		try:
			return valueCache[key]
		except KeyError:
			pass
		else:
			log.info("Was value cached")
		elementCache=self._coreCycleUIAPropertyCacheElementCache
		# If we have a UIAElement who's own cache contains the property, fetch the value from there
		cacheElement=elementCache.get(ID,None)
		if cacheElement:
			value=cacheElement.getCachedPropertyValueEx(ID,ignoreDefault)
		elif not onlyCached:
			# The value is cached nowhere, so ask the UIAElement for its current value for the property
			log.info("Fetching non-cached value")
			value=self.UIAElement.getCurrentPropertyValueEx(ID,ignoreDefault)
		else:
			raise ValueError("UIA property value not cached")
		# cache and return the value
		valueCache[key]=value
		return value

	def _prefetchUIACacheForPropertyIDs(self,IDs):
		#log.info("Requesting cache prefetch for properties: %s"%[UIAHandler.handler.clientObject.GetPropertyProgrammaticName(x) for x in IDs])
		valueCache=self._coreCycleUIAPropertyValueCache
		elementCache=self._coreCycleUIAPropertyCacheElementCache
		# Ignore any IDs we already have cached values or cache UIAElements for 
		IDs={x for x in IDs if x not in valueCache and x not in elementCache}
		if len(IDs)<2:
			# Creating  a UIA cache request for 1 or 0 properties is pointless
			return
		cacheRequest=UIAHandler.handler.clientObject.createCacheRequest()
		for ID in IDs:
			cacheRequest.addProperty(ID)
		cacheElement=self.UIAElement.buildUpdatedCache(cacheRequest)
		#log.info("adding cacheRequest for properties: %s"%[UIAHandler.handler.clientObject.GetPropertyProgrammaticName(x) for x in IDs])
		for ID in IDs:
			elementCache[ID]=cacheElement

	def findOverlayClasses(self,clsList):
		if self.TextInfo==UIATextInfo:
			clsList.append(EditableTextWithoutAutoSelectDetection)

		UIAControlType=self.UIAElement.cachedControlType
		UIAClassName=self.UIAElement.cachedClassName
		if UIAClassName=="WpfTextView":
			clsList.append(WpfTextView)
		elif EditableTextWithoutAutoSelectDetection in clsList and (UIAClassName=='_WwG' or self.UIAElement.cachedAutomationID.startswith('UIA_AutomationId_Word_Content')):
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
			elif self.UIATextPattern and isinstance(self.parent,edge.EdgeHTMLRootContainer):
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
		# #5942: In recent Windows 10 Redstone builds (14332 and later), Microsoft rewrote various dialog code including that of User Account Control.
		if self.UIAIsWindowElement and UIAClassName in ("#32770","NUIDialog", "Credential Dialog Xaml Host"):
			clsList.append(Dialog)

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
		if not UIAElement:
			raise ValueError("needs a UIA element")

		self.UIAElement=UIAElement

		UIACachedWindowHandle=UIAElement.cachedNativeWindowHandle
		self.UIAIsWindowElement=bool(UIACachedWindowHandle)
		if UIACachedWindowHandle:
			windowHandle=UIACachedWindowHandle
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

	def _getUIAPattern(self,ID,interface,cache=False):
		punk=self.UIAElement.GetCachedPattern(ID) if cache else self.UIAElement.GetCurrentPattern(ID) 
		if punk:
			return punk.QueryInterface(interface)

	def _get_UIAInvokePattern(self):
		self.UIAInvokePattern=self._getUIAPattern(UIAHandler.UIA_InvokePatternId,UIAHandler.IUIAutomationInvokePattern)
		return self.UIAInvokePattern

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
		ret = ""
		try:
			ret += self._getUIACacheablePropertyValue(UIAHandler.UIA_AccessKeyPropertyId)
		except COMError:
			pass
		if ret:
			#add a double space to the end of the string
			ret +="  "
		try:
			ret += self._getUIACacheablePropertyValue(UIAHandler.UIA_AcceleratorKeyPropertyId)
		except COMError:
			pass
		return ret

	_UIAStatesPropertyIDs={UIAHandler.UIA_HasKeyboardFocusPropertyId,UIAHandler.UIA_SelectionItemIsSelectedPropertyId,UIAHandler.UIA_IsDataValidForFormPropertyId,UIAHandler.UIA_IsRequiredForFormPropertyId,UIAHandler.UIA_ValueIsReadOnlyPropertyId,UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,UIAHandler.UIA_ToggleToggleStatePropertyId,UIAHandler.UIA_IsKeyboardFocusablePropertyId,UIAHandler.UIA_IsPasswordPropertyId,UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId}

	def _get_states(self):
		states=set()
		self._prefetchUIACacheForPropertyIDs(self._UIAStatesPropertyIDs)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_HasKeyboardFocusPropertyId,onlyCached=True):
			states.add(controlTypes.STATE_FOCUSED)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsKeyboardFocusablePropertyId,onlyCached=True):
			states.add(controlTypes.STATE_FOCUSABLE)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsPasswordPropertyId,onlyCached=True):
			states.add(controlTypes.STATE_PROTECTED)
		# Don't fetch the role unless we must, but never fetch it more than once.
		role=None
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId,onlyCached=True):
			role=self.role
			states.add(controlTypes.STATE_CHECKABLE if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTABLE)
			if self._getUIACacheablePropertyValue(UIAHandler.UIA_SelectionItemIsSelectedPropertyId,onlyCached=True):
				states.add(controlTypes.STATE_CHECKED if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTED)
		if not self._getUIACacheablePropertyValue(UIAHandler.UIA_IsDataValidForFormPropertyId,ignoreDefault=True,onlyCached=True):
			states.add(controlTypes.STATE_INVALID_ENTRY)
		if self._getUIACacheablePropertyValue(UIAHandler.UIA_IsRequiredForFormPropertyId,onlyCached=True):
			states.add(controlTypes.STATE_REQUIRED)
		isReadOnly=self._getUIACacheablePropertyValue(UIAHandler.UIA_ValueIsReadOnlyPropertyId,ignoreDefault=True,onlyCached=True)
		if isReadOnly and isReadOnly!=UIAHandler.handler.reservedNotSupportedValue:
			states.add(controlTypes.STATE_READONLY)
		expandCollapseState=self._getUIACacheablePropertyValue(UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,ignoreDefault=True,onlyCached=True)
		if expandCollapseState!=UIAHandler.handler.reservedNotSupportedValue:
			if expandCollapseState==UIAHandler.ExpandCollapseState_Collapsed:
				states.add(controlTypes.STATE_COLLAPSED)
			elif expandCollapseState==UIAHandler.ExpandCollapseState_Expanded:
				states.add(controlTypes.STATE_EXPANDED)
		toggleState=self._getUIACacheablePropertyValue(UIAHandler.UIA_ToggleToggleStatePropertyId,ignoreDefault=True,onlyCached=True)
		if toggleState!=UIAHandler.handler.reservedNotSupportedValue:
			if not role:
				role=self.role
			if role==controlTypes.ROLE_TOGGLEBUTTON:
				if toggleState==UIAHandler.ToggleState_On:
					states.add(controlTypes.STATE_PRESSED)
			else:
				states.add(controlTypes.STATE_CHECKABLE)
				if toggleState==UIAHandler.ToggleState_On:
					states.add(controlTypes.STATE_CHECKED)
		return states

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
			windowHandle=e.cachedNativeWindowHandle or self.windowHandle
			children.append(self.correctAPIForRelation(UIA(windowHandle=windowHandle,UIAElement=e)))
		return children

	def _get_rowNumber(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_GridItemRowPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

	def _get_rowHeaderText(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_TableItemRowHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in xrange(val.length):
			e=val.getElement(i)
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

	def _get_columnHeaderText(self):
		val=self._getUIACacheablePropertyValue(UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in xrange(val.length):
			e=val.getElement(i)
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
			return UIA(UIAElement=val)
		raise NotImplementedError

	def _get_processID(self):
		return self.UIAElement.cachedProcessId

	def _get_location(self):
		try:
			r=self._getUIACacheablePropertyValue(UIAHandler.UIA_BoundingRectanglePropertyId)
		except COMError:
			return None
		left=r.left
		top=r.top
		width=r.right-left
		height=r.bottom-top
		return left,top,width,height

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
		except COMError:
			return None

class ListItem(UIA):

	def event_stateChange(self):
		if not self.hasFocus:
			parent = self.parent
			focus=api.getFocusObject()
			if parent and isinstance(parent, ComboBoxWithoutValuePattern) and parent==focus: 
				# This is an item in a combo box without the Value pattern.
				# This item has been selected, so notify the combo box that its value has changed.
				focus.event_valueChange()
		super(ListItem, self).event_stateChange()

class Dialog(Dialog):
	role=controlTypes.ROLE_DIALOG

class Toast_win8(Notification, UIA):

	event_UIA_toolTipOpened=Notification.event_alert

class Toast_win10(Notification, UIA):

	# #6096: Windows 10 Redstone build 14366 and later does not fire tooltip event when toasts appear.
	if sys.getwindowsversion().build > 10586:
		event_UIA_window_windowOpen=Notification.event_alert
	else:
		event_UIA_toolTipOpened=Notification.event_alert

#WpfTextView fires name state changes once a second, plus when IUIAutomationTextRange::GetAttributeValue is called.
#This causes major lags when using this control with Braille in NVDA. (#2759) 
#For now just ignore the events.
class WpfTextView(UIA):

	def event_nameChange(self):
		return

	def event_stateChange(self):
		return

