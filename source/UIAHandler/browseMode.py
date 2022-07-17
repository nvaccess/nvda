# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2020 NV Access Limited, Babbage B.V., Accessolutions, Julien Cochuyt

from typing import Optional
from ctypes import byref
from comtypes import COMError
from comtypes.automation import VARIANT
import array
import winUser
import UIAHandler
from .utils import (
	createUIAMultiPropertyCondition,
	getDeepestLastChildUIAElementInWalker,
	isUIAElementInWalker,
	iterUIARangeByUnit,
)
import documentBase
import treeInterceptorHandler
import cursorManager
import textInfos
import browseMode
from NVDAObjects.UIA import UIA

class UIADocumentWithTableNavigation(documentBase.DocumentWithTableNavigation):

	def _getTableCellAt(self,tableID,startPos,row,column):
		startUIAElement=startPos.UIAElementAtStart
		# Comtypes casts a tuple into a variant containing a  safearray of variants.
		# However, UIA's createPropertyCondition requires a safearay of ints.
		# By first converting the tuple to a Python int Array we can ensure this.  
		tableIDArray=array.array("l",tableID)
		UIACondition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_RuntimeIdPropertyId,tableIDArray)
		UIAWalker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		try:
			tableUIAElement=UIAWalker.normalizeElement(startUIAElement)
		except COMError:
			tableUIAElement=None
		if not tableUIAElement:
			raise LookupError
		UIAGridPattern=None
		try:
			punk=tableUIAElement.getCurrentPattern(UIAHandler.UIA_GridPatternId)
			if punk:
				UIAGridPattern=punk.QueryInterface(UIAHandler.IUIAutomationGridPattern)
		except COMError:
			raise LookupError
		if not tableUIAElement:
			raise RuntimeError
		try:
			cellElement=UIAGridPattern.getItem(row-1,column-1)
		except COMError:
			cellElement=None
		if not cellElement:
			raise LookupError
		return self.makeTextInfo(cellElement)

class UIATextRangeQuickNavItem(browseMode.TextInfoQuickNavItem):

	def __init__(self,itemType,document,UIAElementOrRange):
		if isinstance(UIAElementOrRange,UIAHandler.IUIAutomationElement):
			UIATextRange=document.rootNVDAObject.getNormalizedUIATextRangeFromElement(UIAElementOrRange)
			if not UIATextRange:
				raise ValueError("Could not get text range for UIA element")
			self._UIAElement=UIAElementOrRange
		elif isinstance(UIAElementOrRange,UIAHandler.IUIAutomationTextRange):
			UIATextRange=UIAElementOrRange
			self._UIAElement=None
		else:
			raise ValueError("Invalid UIAElementOrRange")
		textInfo=document.TextInfo(document,None,_rangeObj=UIATextRange)
		super(UIATextRangeQuickNavItem,self).__init__(itemType,document,textInfo)

	@property
	def obj(self):
		if self._UIAElement:
			UIAElement=self._UIAElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
			return UIA(UIAElement=UIAElement)
		return self.textInfo.NVDAObjectAtStart

	@property
	def label(self):
		return self._getLabelForProperties(lambda prop: getattr(self.obj, prop, None))

class TextAttribUIATextInfoQuickNavItem(browseMode.TextInfoQuickNavItem):
	attribID=None #: a UIA text attribute to search for
	wantedAttribValues=set() #: A set of attribute values acceptable to match the search.

	def __init__(self,attribValues,itemType,document,textInfo):
		self.attribValues=attribValues
		super(TextAttribUIATextInfoQuickNavItem,self).__init__(itemType,document,textInfo)

class ErrorUIATextInfoQuickNavItem(TextAttribUIATextInfoQuickNavItem):
	attribID=UIAHandler.UIA_AnnotationTypesAttributeId
	wantedAttribValues={UIAHandler.AnnotationType_SpellingError,UIAHandler.AnnotationType_GrammarError}

	@property
	def label(self):
		text=self.textInfo.text
		if (UIAHandler.AnnotationType_SpellingError in self.attribValues) and (UIAHandler.AnnotationType_GrammarError in self.attribValues):
			# Translators: The label shown for a spelling and grammar error in the NVDA Elements List dialog in Microsoft Word.
			# {text} will be replaced with the text of the spelling error.
			return _(u"spelling and grammar: {text}").format(text=text)
		elif UIAHandler.AnnotationType_SpellingError in self.attribValues:
			# Translators: The label shown for a spelling error in the NVDA Elements List dialog in Microsoft Word.
			# {text} will be replaced with the text of the spelling error.
			return _(u"spelling: {text}").format(text=text)
		elif UIAHandler.AnnotationType_GrammarError in self.attribValues:
			# Translators: The label shown for a grammar error in the NVDA Elements List dialog in Microsoft Word.
			# {text} will be replaced with the text of the spelling error.
			return _(u"grammar: {text}").format(text=text)
		else:
			return text

def UIATextAttributeQuicknavIterator(ItemClass,itemType,document,position,direction="next"):
	reverse=(direction=="previous")
	entireDocument=document.makeTextInfo(textInfos.POSITION_ALL)
	if not position:
		searchArea=entireDocument
	else:
		searchArea=position.copy()
		if reverse:
			searchArea.setEndPoint(entireDocument,"startToStart")
		else:
			searchArea.setEndPoint(entireDocument,"endToEnd")
	firstLoop=True
	for subrange in iterUIARangeByUnit(searchArea._rangeObj,UIAHandler.TextUnit_Format,reverse=reverse):
		if firstLoop:
			firstLoop=False
			if position and not reverse:
				# We are starting to search forward from a specific position
				# Skip the first subrange as it is the one we started on.
				continue
		curAttribValue=subrange.getAttributeValue(ItemClass.attribID)
		curAttribValues=curAttribValue if isinstance(curAttribValue,tuple) else (curAttribValue,)
		for wantedAttribValue in ItemClass.wantedAttribValues:
			if wantedAttribValue in curAttribValues:
				tempInfo=document.makeTextInfo(subrange)
				yield ItemClass(curAttribValues,itemType,document,tempInfo)
				break

class HeadingUIATextInfoQuickNavItem(browseMode.TextInfoQuickNavItem):

	def __init__(self,itemType,document,position,level=0):
		super(HeadingUIATextInfoQuickNavItem,self).__init__(itemType,document,position)
		self.level=level

	def isChild(self,parent):
		if not isinstance(parent,HeadingUIATextInfoQuickNavItem):
			return False
		return self.level>parent.level


def UIAHeadingQuicknavIterator(
		itemType: str,
		document: "UIABrowseModeDocument",
		position: Optional["UIABrowseModeDocumentTextInfo"],
		direction: str = "next"
):
	reverse = bool(direction == "previous")
	entireDocument = document.makeTextInfo(textInfos.POSITION_ALL)
	if position is None:
		searchArea = entireDocument
	else:
		searchArea = position.copy()
		if reverse:
			searchArea.start = entireDocument.start
		else:
			searchArea.end = entireDocument.end
	firstLoop=True
	for subrange in iterUIARangeByUnit(searchArea._rangeObj, UIAHandler.TextUnit_Paragraph, reverse=reverse):
		if firstLoop:
			firstLoop = False
			if position and not reverse:
				# We are starting to search forward from a specific position
				# Skip the first subrange as it is the one we started on.
				continue
		styleIDValue = subrange.getAttributeValue(UIAHandler.UIA_StyleIdAttributeId)
		# #9842: styleIDValue can sometimes be a pointer to IUnknown.
		# In Python 3, comparing an int with a pointer raises a TypeError.
		if isinstance(styleIDValue, int) and UIAHandler.StyleId_Heading1 <= styleIDValue <= UIAHandler.StyleId_Heading9:
			foundLevel = (styleIDValue - UIAHandler.StyleId_Heading1) + 1
			wantedLevel = int(itemType[7:]) if len(itemType) > 7 else None
			if not wantedLevel or wantedLevel==foundLevel: 
				tempInfo = document.makeTextInfo(subrange)
				yield HeadingUIATextInfoQuickNavItem(itemType, document, tempInfo, level=foundLevel)


def UIAControlQuicknavIterator(itemType,document,position,UIACondition,direction="next",itemClass=UIATextRangeQuickNavItem):
	# A part from the condition given, we must always match on the root of the document so we know when to stop walking
	runtimeID=VARIANT()
	document.rootNVDAObject.UIAElement._IUIAutomationElement__com_GetCurrentPropertyValue(UIAHandler.UIA_RuntimeIdPropertyId,byref(runtimeID))
	UIACondition=UIAHandler.handler.clientObject.createOrCondition(UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_RuntimeIdPropertyId,runtimeID),UIACondition)
	if not position:
		# All items are requested (such as for elements list)
		elements=document.rootNVDAObject.UIAElement.findAll(UIAHandler.TreeScope_Descendants,UIACondition)
		if elements:
			for index in range(elements.length):
				element=elements.getElement(index)
				try:
					elementRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(element)
				except COMError:
					elementRange=None
				if elementRange:
					yield itemClass(itemType,document,elementRange)
		return
	if direction=="up":
		walker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		element=position.UIAElementAtStart
		while element:
			element=walker.normalizeElement(element)
			if (
				not element 
				or UIAHandler.handler.clientObject.compareElements(element,document.rootNVDAObject.UIAElement) 
				or UIAHandler.handler.clientObject.compareElements(element,UIAHandler.handler.rootElement)
			):
				break
			try:
				yield itemClass(itemType,document,element)
			except ValueError:
				pass # this element was not represented in the document's text content.
			element=walker.getParentElement(element)
		return
	elif direction=="previous":
		# Fetching items previous to the given position.
		# When getting children of a UIA text range, Edge will incorrectly include a child that starts at the end of the range. 
		# Therefore move back by one character to stop this.
		toPosition=position._rangeObj.clone()
		toPosition.move(UIAHandler.TextUnit_Character,-1)
		child=toPosition.getEnclosingElement()
		childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
		toPosition.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
		# Fetch the last child of this text range.
		# But if its own range extends beyond the end of our position:
		# We know that the child is not the deepest descendant,
		# And therefore we Limit our children fetching range to the start of this child,
		# And fetch the last child again.
		zoomedOnce=False
		while True:
			children=toPosition.getChildren()
			length=children.length
			if length==0:
				if zoomedOnce:
					child=toPosition.getEnclosingElement()
				break
			child=children.getElement(length-1)
			try:
				childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
			except COMError:
				return
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_End)>0 and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,toPosition,UIAHandler.TextPatternRangeEndpoint_Start)>0:
				toPosition.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
				zoomedOnce=True
				continue
			break
		if not child or UIAHandler.handler.clientObject.compareElements(child,document.rootNVDAObject.UIAElement):
			# We're on the document itself -- probably nothing in it.
			return
		# Work out if this child is previous to our position or not.
		# If it isn't, then we know we still need to move parent or previous before it is safe to emit an item.
		try:
			childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
		except COMError:
			return
		gonePreviousOnce=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)<=0
		walker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		curElement=child
		# Start traversing from this child backward through the document, emitting items for valid elements.
		curElementMatchedCondition=False
		goneParent=False
		while curElement:
			if gonePreviousOnce and not goneParent: 
				lastChild=getDeepestLastChildUIAElementInWalker(curElement,walker)
				if lastChild:
					curElement=lastChild
					curElementMatchedCondition=True
				elif not curElementMatchedCondition and isUIAElementInWalker(curElement,walker):
					curElementMatchedCondition=True
				if curElementMatchedCondition:
					yield itemClass(itemType,document,curElement)
			previousSibling=walker.getPreviousSiblingElement(curElement)
			if previousSibling:
				gonePreviousOnce=True
				goneParent=False
				curElement=previousSibling
				curElementMatchedCondition=True
				continue
			parent=walker.getParentElement(curElement)
			if parent and not UIAHandler.handler.clientObject.compareElements(document.rootNVDAObject.UIAElement,parent):
				curElement=parent
				goneParent=True
				curElementMatchedCondition=True
				if gonePreviousOnce:
					yield itemClass(itemType,document,curElement)
				continue
			curElement=None
	else: # direction is next
		# Fetching items after the given position.
		# Extend the end of the range forward to the end of the document so that we will be able to fetch children from this point onwards. 
		# Fetch the first child of this text range.
		# But if its own range extends before the start of our position:
		# We know that the child is not the deepest descendant,
		# And therefore we Limit our children fetching range to the end of this child,
		# And fetch the first child again.
		child=position._rangeObj.getEnclosingElement()
		childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
		toPosition=position._rangeObj.clone()
		toPosition.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_End)
		zoomedOnce=False
		while True:
			children=toPosition.getChildren()
			length=children.length
			if length==0:
				if zoomedOnce:
					child=toPosition.getEnclosingElement()
				break
			child=children.getElement(0)
			try:
				childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
			except COMError:
				return
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)<0 and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,toPosition,UIAHandler.TextPatternRangeEndpoint_End)<0:
				toPosition.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_End)
				zoomedOnce=True
				continue
			break
		# Work out if this child is after our position or not.
		if not child or UIAHandler.handler.clientObject.compareElements(child,document.rootNVDAObject.UIAElement):
			# We're on the document itself -- probably nothing in it.
			return
		try:
			childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
		except COMError:
			return
		goneNextOnce=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)>0
		walker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		curElement=child
		# If we are already past our position, and this is a valid child
		# Then we can emit an item already
		if goneNextOnce and isUIAElementInWalker(curElement,walker):
			yield itemClass(itemType,document,curElement)
		# Start traversing from this child forwards through the document, emitting items for valid elements.
		while curElement:
			firstChild=walker.getFirstChildElement(curElement) if goneNextOnce else None
			if firstChild:
				curElement=firstChild
				yield itemClass(itemType,document,curElement)
			else:
				nextSibling=None
				while not nextSibling:
					nextSibling=walker.getNextSiblingElement(curElement)
					if not nextSibling:
						parent=walker.getParentElement(curElement)
						if parent and not UIAHandler.handler.clientObject.compareElements(document.rootNVDAObject.UIAElement,parent):
							curElement=parent
						else:
							return
				curElement=nextSibling
				goneNextOnce=True
				yield itemClass(itemType,document,curElement)

class UIABrowseModeDocumentTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):

	def _get_UIAElementAtStart(self):
		return self.innerTextInfo.UIAElementAtStart


class UIABrowseModeDocument(UIADocumentWithTableNavigation,browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=UIABrowseModeDocumentTextInfo
	# UIA browseMode documents cannot remember caret positions across loads (I.e. when going back a page in Edge) 
	# Because UIA TextRanges are opaque and are tied specifically to one particular document.
	shouldRememberCaretPositionAcrossLoads=False

	def event_UIA_activeTextPositionChanged(self, obj, nextHandler, textRange=None):
		if not self.isReady:
			self._initialScrollObj = obj
			return nextHandler()
		scrollInfo = self.makeTextInfo(textRange)
		if not self._handleScrollTo(scrollInfo):
			return nextHandler()

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType.startswith("heading"):
			return UIAHeadingQuicknavIterator(nodeType,self,pos,direction=direction)
		elif nodeType=="error":
			return UIATextAttributeQuicknavIterator(ErrorUIATextInfoQuickNavItem,nodeType,self,pos,direction=direction)
		elif nodeType=="link":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_HyperlinkControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="button":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_ButtonControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="checkBox":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_CheckBoxControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="radioButton":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_RadioButtonControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="comboBox":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_ComboBoxControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="graphic":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_ImageControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="table":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:[UIAHandler.UIA_TableControlTypeId,UIAHandler.UIA_DataGridControlTypeId]})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="separator":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_SeparatorControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="focusable":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_IsKeyboardFocusablePropertyId,True)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="list":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ListControlTypeId,UIAHandler.UIA_IsKeyboardFocusablePropertyId:False})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="container":
			condition = createUIAMultiPropertyCondition(
				{
					UIAHandler.UIA.UIA_ControlTypePropertyId: UIAHandler.UIA.UIA_ListControlTypeId,
					UIAHandler.UIA.UIA_IsKeyboardFocusablePropertyId: False
				},
				{
					UIAHandler.UIA.UIA_ControlTypePropertyId: [
						UIAHandler.UIA.UIA_TableControlTypeId,
						UIAHandler.UIA.UIA_DataGridControlTypeId
					]
				},
				{
					UIAHandler.UIA_ControlTypePropertyId: UIAHandler.UIA.UIA_GroupControlTypeId,
					UIAHandler.UIA_AriaRolePropertyId: ["article"]
				}
			)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="edit":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_EditControlTypeId,UIAHandler.UIA_ValueIsReadOnlyPropertyId:False},{UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ComboBoxControlTypeId,UIAHandler.UIA_IsTextPatternAvailablePropertyId:True})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="formField":
			condition = createUIAMultiPropertyCondition(
				{
					UIAHandler.UIA_ControlTypePropertyId: UIAHandler.UIA_EditControlTypeId,
					UIAHandler.UIA_ValueIsReadOnlyPropertyId: False
				},
				{
					UIAHandler.UIA_ControlTypePropertyId: UIAHandler.UIA_ListControlTypeId,
					UIAHandler.UIA_IsKeyboardFocusablePropertyId: True
				},
				{
					UIAHandler.UIA_ControlTypePropertyId: [
						UIAHandler.UIA_ButtonControlTypeId,
						UIAHandler.UIA_CheckBoxControlTypeId,
						UIAHandler.UIA_ComboBoxControlTypeId,
						UIAHandler.UIA_RadioButtonControlTypeId,
						UIAHandler.UIA_TabItemControlTypeId,
					]
				},
			)
			return UIAControlQuicknavIterator(nodeType, self, pos, condition, direction)
		elif nodeType == "landmark":
			condition = UIAHandler.handler.clientObject.createNotCondition(
				UIAHandler.handler.clientObject.createPropertyCondition(
					UIAHandler.UIA.UIA_LandmarkTypePropertyId,
					0
				)
			)
			return UIAControlQuicknavIterator(nodeType, self, pos, condition, direction)
		elif nodeType == "article":
			condition = createUIAMultiPropertyCondition({
				UIAHandler.UIA_ControlTypePropertyId: UIAHandler.UIA.UIA_GroupControlTypeId,
				UIAHandler.UIA_AriaRolePropertyId: ["article"]
			})
			return UIAControlQuicknavIterator(nodeType, self, pos, condition, direction)
		elif nodeType == "grouping":
			condition = UIAHandler.handler.clientObject.CreateAndConditionFromArray([
				UIAHandler.handler.clientObject.createPropertyCondition(
					UIAHandler.UIA.UIA_ControlTypePropertyId,
					UIAHandler.UIA.UIA_GroupControlTypeId
				),
				UIAHandler.handler.clientObject.createNotCondition(
					UIAHandler.handler.clientObject.createPropertyCondition(
						UIAHandler.UIA.UIA_NamePropertyId,
						""
					)
				)
			])
			return UIAControlQuicknavIterator(nodeType, self, pos, condition, direction)
		elif nodeType=="nonTextContainer":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ListControlTypeId,UIAHandler.UIA_IsKeyboardFocusablePropertyId:True},{UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ComboBoxControlTypeId})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="embeddedObject":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_PaneControlTypeId,UIAHandler.UIA_AriaRolePropertyId:[u"application",u"alertdialog",u"dialog"]})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		raise NotImplementedError

	def _activateNVDAObject(self,obj):
		try:
			obj.doAction()
		except NotImplementedError:
			pass

	def _get_isAlive(self):
		if not winUser.isWindow(self.rootNVDAObject.windowHandle):
			return False
		try:
			self.rootNVDAObject.UIAElement.currentProviderDescription
		except COMError:
			return False
		return True

	def __contains__(self,obj):
		if not isinstance(obj,UIA):
			return False
		# Ensure that this object is a descendant of the document or is the document itself. 
		runtimeID=VARIANT()
		self.rootNVDAObject.UIAElement._IUIAutomationElement__com_GetCurrentPropertyValue(UIAHandler.UIA_RuntimeIdPropertyId,byref(runtimeID))
		UIACondition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_RuntimeIdPropertyId,runtimeID)
		UIAWalker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		try:
			docUIAElement=UIAWalker.normalizeElement(obj.UIAElement)
		except COMError:
			docUIAElement=None
		if not docUIAElement:
			return False
		# Ensure that this object also can be reached by the document's text pattern.
		try:
			self.rootNVDAObject.makeTextInfo(obj)
		except LookupError:
			return False
		return True
