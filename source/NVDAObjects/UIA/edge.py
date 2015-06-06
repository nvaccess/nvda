#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015 NV Access Limited

from comtypes import COMError
from comtypes.automation import VARIANT
from ctypes import byref
import eventHandler
import controlTypes
import winUser
import textInfos
import UIAHandler
import browseMode
import treeInterceptorHandler
import cursorManager
from . import UIA

class EdgeList(UIA):

	# non-focusable lists are readonly lists (ensures correct NVDA presentation category)
	def _get_states(self):
		states=super(EdgeList,self).states
		if controlTypes.STATE_FOCUSABLE not in states:
			states.add(controlTypes.STATE_READONLY)
		return states


class EdgeHTMLRootContainer(UIA):

	shouldAllowUIAFocusEvent=True

	def event_gainFocus(self):
		firstChild=self.firstChild
		if isinstance(firstChild,UIA):
			eventHandler.executeEvent("gainFocus",firstChild)
			return
		return super(EdgeHTMLRootContainer,self).event_gainFocus()

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
		UIAElement=self._UIAElement if self._UIAElement else self.textInfo._rangeObj.getEnclosingElement()
		UIAElement=UIAElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		return UIA(UIAElement=UIAElement)

def UIATextAttributeQuickNavIterator(itemType,document,position,attributeID,attributeValue,direction="next"):
	includeCurrent=False
	if not position:
		position=document.makeTextInfo(textInfos.POSITION_ALL)
		includeCurrent=True
	elif direction=="previous":
		position.expand(textInfos.UNIT_CHARACTER)
		# Hack: IUIAutomationTextRange::FindAttribute breaks after expand. copy to fix.
		position=position.copy()
		position.setEndPoint(document.TextInfo(document,textInfos.POSITION_ALL),"startToStart")
	else:
		position.setEndPoint(document.TextInfo(document,textInfos.POSITION_ALL),"endToEnd")
	while True:
		try:
			newRange=position._rangeObj.findAttribute(attributeID,attributeValue,direction=="previous")
		except COMError:
			newRange=None
		if not newRange:
			return
		if includeCurrent or newRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)>0:
			yield UIATextRangeQuickNavItem(itemType,document,newRange)
			includeCurrent=True
		if direction=="previous":
			position._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,newRange,UIAHandler.TextPatternRangeEndpoint_Start)
		else:
			position._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,newRange,UIAHandler.TextPatternRangeEndpoint_End)

def UIATextRangeFromElement(documentTextPattern,element):
	try:
		childRange=documentTextPattern.rangeFromChild(element)
	except COMError:
		childRange=None
	return childRange

def isUIAElementInWalker(element,walker):
		try:
			newElement=walker.normalizeElement(element)
		except COMError:
			newElement=None
		return newElement and UIAHandler.handler.clientObject.compareElements(element,newElement)

def getDeepestLastChildUIAElementInWalker(element,walker):
	descended=False
	while True:
		lastChild=walker.getLastChildElement(element)
		if lastChild:
			descended=True
			element=lastChild
		else:
			break
		return element if descended else None

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

class EdgeHTMLTreeInterceptorTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):
	pass

class EdgeHTMLTreeInterceptor(cursorManager.ReviewCursorManager,browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=EdgeHTMLTreeInterceptorTextInfo

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent.name

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType=="heading":
			return browseMode.mergeQuickNavItemIterators([UIATextAttributeQuickNavIterator("heading",self,pos,UIAHandler.UIA_StyleIdAttributeId,value,direction) for value in xrange(UIAHandler.StyleId_Heading1,UIAHandler.StyleId_Heading7)],direction)
		elif nodeType=="link":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_HyperlinkControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		elif nodeType=="focusable":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_IsKeyboardFocusablePropertyId,True)
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

class EdgeHTMLRoot(UIA):

	treeInterceptorClass=EdgeHTMLTreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in self.states 


	def _get_role(self):
		role=super(EdgeHTMLRoot,self).role
		if role==controlTypes.ROLE_PANE:
			role=controlTypes.ROLE_DOCUMENT
		return role

