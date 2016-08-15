#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015-2016 NV Access Limited

from ctypes import byref
from comtypes.automation import VARIANT
import winUser
import UIAHandler
from UIAUtils import *
import treeInterceptorHandler
import cursorManager
import textInfos
import browseMode
from NVDAObjects.UIA import UIA

class UIATextRangeQuickNavItem(browseMode.TextInfoQuickNavItem):

	def __init__(self,itemType,document,UIAElementOrRange):
		if isinstance(UIAElementOrRange,UIAHandler.IUIAutomationElement):
			UIATextRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(UIAElementOrRange)
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
		if self.itemType=="landmark":
			obj=self.obj
			name=obj.name
			landmarkType=obj.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_LocalizedLandmarkTypePropertyId)
			return " ".join(x for x in (name,landmarkType) if x)
		return super(UIATextRangeQuickNavItem,self).label

class HeadingUIATextInfoQuickNavItem(browseMode.TextInfoQuickNavItem):

	def __init__(self,itemType,document,position,level=0):
		super(HeadingUIATextInfoQuickNavItem,self).__init__(itemType,document,position)
		self.level=level

	def isChild(self,parent):
		if not isinstance(parent,HeadingUIATextInfoQuickNavItem):
			return False
		return self.level>parent.level

def UIAHeadingQuicknavIterator(itemType,document,position,direction="next"):
	if position:
		curPosition=position
	else:
		curPosition=document.makeTextInfo(textInfos.POSITION_LAST if direction=="previous" else textInfos.POSITION_FIRST)
	stop=False
	firstLoop=True
	while not stop:
		tempInfo=curPosition.copy()
		tempInfo.expand(textInfos.UNIT_CHARACTER)
		styleIDValue=getUIATextAttributeValueFromRange(tempInfo._rangeObj,UIAHandler.UIA_StyleIdAttributeId)
		if (UIAHandler.StyleId_Heading1<=styleIDValue<=UIAHandler.StyleId_Heading9):
			foundLevel=(styleIDValue-UIAHandler.StyleId_Heading1)+1
			wantedLevel=int(itemType[7:]) if len(itemType)>7 else None
			if not wantedLevel or wantedLevel==foundLevel: 
				if not firstLoop or not position:
					tempInfo.expand(textInfos.UNIT_PARAGRAPH)
					yield HeadingUIATextInfoQuickNavItem(itemType,document,tempInfo,level=foundLevel)
		stop=(curPosition.move(textInfos.UNIT_PARAGRAPH,1 if direction=="next" else -1)==0)
		firstLoop=False

def UIAControlQuicknavIterator(itemType,document,position,UIACondition,direction="next"):
	# A part from the condition given, we must always match on the root of the document so we know when to stop walking
	runtimeID=VARIANT()
	document.rootNVDAObject.UIAElement._IUIAutomationElement__com_GetCurrentPropertyValue(UIAHandler.UIA_RuntimeIdPropertyId,byref(runtimeID))
	UIACondition=UIAHandler.handler.clientObject.createOrCondition(UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_RuntimeIdPropertyId,runtimeID),UIACondition)
	if not position:
		# All items are requested (such as for elements list)
		elements=document.rootNVDAObject.UIAElement.findAll(UIAHandler.TreeScope_Descendants,UIACondition)
		if elements:
			for index in xrange(elements.length):
				element=elements.getElement(index)
				try:
					elementRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(element)
				except COMError:
					elementRange=None
				if elementRange:
					yield UIATextRangeQuickNavItem(itemType,document,elementRange)
		return
	if direction=="up":
		walker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		# some implementations (Edge, Word) do not correctly  class embedded objects (graphics, checkboxes) as being the enclosing element, even when the range is completely within them. Rather, they still list the object in getChildren.
		# Thus we must check getChildren before getEnclosingElement.
		tempRange=position._rangeObj.clone()
		tempRange.expandToEnclosingUnit(UIAHandler.TextUnit_Character)
		children=tempRange.getChildren()
		if children.length==1:
			element=children.getElement(0)
		else:
			element=position._rangeObj.getEnclosingElement()
		element=walker.normalizeElement(element)
		if element and not UIAHandler.handler.clientObject.compareElements(element,document.rootNVDAObject.UIAElement) and not UIAHandler.handler.clientObject.compareElements(element,UIAHandler.handler.rootElement):
			yield UIATextRangeQuickNavItem(itemType,document,element)
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
					yield UIATextRangeQuickNavItem(itemType,document,curElement)
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
					yield UIATextRangeQuickNavItem(itemType,document,curElement)
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
			yield UIATextRangeQuickNavItem(itemType,document,curElement)
		# Start traversing from this child forwards through the document, emitting items for valid elements.
		while curElement:
			firstChild=walker.getFirstChildElement(curElement) if goneNextOnce else None
			if firstChild:
				curElement=firstChild
				yield UIATextRangeQuickNavItem(itemType,document,curElement)
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
				yield UIATextRangeQuickNavItem(itemType,document,curElement)

class UIABrowseModeDocumentTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):
	pass

class UIABrowseModeDocument(cursorManager.ReviewCursorManager,browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=UIABrowseModeDocumentTextInfo

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType.startswith("heading"):
			return UIAHeadingQuicknavIterator(nodeType,self,pos,direction=direction)
		elif nodeType=="link":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_HyperlinkControlTypeId)
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
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_TableControlTypeId)
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
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ListControlTypeId,UIAHandler.UIA_IsKeyboardFocusablePropertyId:False},{UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_TableControlTypeId})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="edit":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_EditControlTypeId,UIAHandler.UIA_ValueIsReadOnlyPropertyId:False})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="formField":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_EditControlTypeId,UIAHandler.UIA_ValueIsReadOnlyPropertyId:False},{UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ListControlTypeId,UIAHandler.UIA_IsKeyboardFocusablePropertyId:True},{UIAHandler.UIA_ControlTypePropertyId:[UIAHandler.UIA_CheckBoxControlTypeId,UIAHandler.UIA_RadioButtonControlTypeId,UIAHandler.UIA_ComboBoxControlTypeId,UIAHandler.UIA_ButtonControlTypeId]})
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="landmark":
			condition=UIAHandler.handler.clientObject.createNotCondition(UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_LocalizedLandmarkTypePropertyId,""))
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="nonTextContainer":
			condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ListControlTypeId,UIAHandler.UIA_IsKeyboardFocusablePropertyId:True},{UIAHandler.UIA_ControlTypePropertyId:UIAHandler.UIA_ComboBoxControlTypeId})
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
		try:
			self.rootNVDAObject.makeTextInfo(obj)
		except LookupError:
			return False
		return True
