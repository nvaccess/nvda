#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015 NV Access Limited

from comtypes import COMError
import eventHandler
import controlTypes
import winUser
import textInfos
import UIAHandler
import browseMode
import treeInterceptorHandler
import cursorManager
from . import UIA

class EdgeHTMLRootContainer(UIA):

	shouldAllowUIAFocusEvent=True

	def event_gainFocus(self):
		firstChild=self.firstChild
		if isinstance(firstChild,UIA):
			eventHandler.executeEvent("gainFocus",firstChild)
			return
		return super(EdgeHTML,self).event_gainFocus()

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
		curPosition=document.TextInfo(document,None,_rangeObj=newRange)
		if includeCurrent or curPosition.compareEndPoints(position,"startToStart")>0:
			yield browseMode.TextInfoQuickNavItem(itemType,document,curPosition)
			includeCurrent=True
		position.setEndPoint(curPosition,"endToStart" if direction=="previous" else "startToEnd")

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
	if not position:
		# All items are request (such as for elements list)
		elements=document.rootNVDAObject.UIAElement.findAll(UIAHandler.TreeScope_Descendants,UIACondition)
		for index in xrange(elements.length):
			element=elements.getElement(index)
			try:
				elementRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(element)
			except COMError:
				elementRange=None
			if elementRange:
				info=document.TextInfo(document,None,_rangeObj=elementRange)
				yield browseMode.TextInfoQuickNavItem(itemType,document,info)
		return
	if direction=="previous":
		# Fetching items previous to the given position.
		toPosition=position.copy()
		# When getting children of a UIA text range, Edge will incorrectly include a child that starts at the end of the range. 
		# Therefore move back by one character to stop this.
		toPosition.move(textInfos.UNIT_CHARACTER,-1)
		# Extend the start of the range back to the start of the document so that we will be able to fetch children all the way up to this point.
		toPosition.setEndPoint(document.TextInfo(document,textInfos.POSITION_ALL),"startToStart")
		# Fetch the last child of this text range.
		# But if its own range extends beyond the end of our position:
		# We know that the child is not the deepest descendant,
		# And therefore we Limit our children fetching range to the start of this child,
		# And fetch the last child again.
		child=None
		zoomedOnce=False
		while True:
			children=toPosition._rangeObj.getChildren()
			length=children.length
			if length==0:
				break
			child=children.getElement(length-1)
			try:
				childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
			except COMError:
				return
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_End)>0 and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,toPosition._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)>0:
				toPosition._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
				zoomedOnce=True
				continue
			break
		if not child:
			if not zoomedOnce:
				return
			# If we have zoomed in at all, yet this level has no children,
			# Then we can use the element enclosing this range as that will be the deepest.
			child=toPosition._rangeObj.getEnclosingElement()
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
					yield browseMode.TextInfoQuickNavItem(itemType,document,document.TextInfo(document,None,_rangeObj=document.rootNVDAObject.UIATextPattern.rangeFromChild(curElement)))
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
					yield browseMode.TextInfoQuickNavItem(itemType,document,document.TextInfo(document,None,_rangeObj=document.rootNVDAObject.UIATextPattern.rangeFromChild(curElement)))
				continue
			curElement=None
	elif True:
				# Fetching items after the given position.
		toPosition=position.copy()
		# Extend the end of the range forward to the end of the document so that we will be able to fetch children from this point onwards. 
		toPosition.setEndPoint(document.TextInfo(document,textInfos.POSITION_ALL),"endToEnd")
		# Fetch the first child of this text range.
		# But if its own range extends before the start of our position:
		# We know that the child is not the deepest descendant,
		# And therefore we Limit our children fetching range to the end of this child,
		# And fetch the first child again.
		child=None
		zoomedOnce=False
		while True:
			children=toPosition._rangeObj.getChildren()
			length=children.length
			if length==0:
				break
			child=children.getElement(0)
			try:
				childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
			except COMError:
				return
			print "childRange text: %s"%childRange.getText(-1)
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)<0 and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,toPosition._rangeObj,UIAHandler.TextPatternRangeEndpoint_End)<0:
				toPosition._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_End)
				zoomedOnce=True
				continue
			break
		if not child:
			if not zoomedOnce:
				return
			# If we have zoomed in at all, yet this level has no children,
			# Then we can use the element enclosing this range as that will be the deepest.
			child=toPosition._rangeObj.getEnclosingElement()
			if UIAHandler.handler.clientObject.comareElements(child,document.rootNVDAObject.UIAElement):
				import tones; tones.beep(550,50)
				return
		# Work out if this child is after our position or not.
		try:
			childRange=document.rootNVDAObject.UIATextPattern.rangeFromChild(child)
		except COMError:
			return
		print "childRange text: %s"%childRange.getText(-1)
		goneNextOnce=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,position._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)>0
		print "goneNextOnce: %s"%goneNextOnce
		walker=UIAHandler.handler.clientObject.createTreeWalker(UIACondition)
		curElement=child
		# If we are already past our position, and this is a valid child
		# Then we can emmit an item already
		if goneNextOnce and isUIAElementInWalker(curElement,walker):
			yield browseMode.TextInfoQuickNavItem(itemType,document,document.TextInfo(document,None,_rangeObj=document.rootNVDAObject.UIATextPattern.rangeFromChild(curElement)))
		# Start traversing from this child forwards through the document, emitting items for valid elements.
		while curElement:
			# Ensure this element is really represented in the document's text.
			if not UIATextRangeFromElement(document.rootNVDAObject.UIATextPattern,curElement):
				return
			firstChild=walker.getFirstChildElement(curElement)
			if firstChild:
				curElement=firstChild
				yield browseMode.TextInfoQuickNavItem(itemType,document,document.TextInfo(document,None,_rangeObj=document.rootNVDAObject.UIATextPattern.rangeFromChild(curElement)))
				continue
			nextSibling=None
			while curElement:
				nextSibling=walker.getNextSiblingElement(curElement)
				if not nextSibling:
					parent=walker.getParentElement(curElement)
					if not parent or not UIATextRangeFromElement(document.rootNVDAObject.UIATextPattern,parent):
						return
					curElement=parent
				else:
					break
			if nextSibling:
				curElement=nextSibling
				childRange=UIATextRangeFromElement(document.rootNVDAObject.UIATextPattern,curElement)
				if not childRange:
					return
				yield browseMode.TextInfoQuickNavItem(itemType,document,document.TextInfo(document,None,_rangeObj=childRange))
		curElement=None

class EdgeHTMLTreeInterceptor(cursorManager.ReviewCursorManager,browseMode.BrowseModeTreeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor):

	TextInfo=treeInterceptorHandler.RootProxyTextInfo

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType=="heading":
			return browseMode.mergeQuickNavItemIterators([UIATextAttributeQuickNavIterator("heading",self,pos,UIAHandler.UIA_StyleIdAttributeId,value,direction) for value in xrange(UIAHandler.StyleId_Heading1,UIAHandler.StyleId_Heading7)],direction)
		elif nodeType=="link":
			condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_HyperlinkControlTypeId)
			return UIAControlQuicknavIterator(nodeType,self,pos,condition,direction)
		raise NotImplementedError

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

	def event_gainFocus(self,obj,nextHandler):
		info=self.makeTextInfo(obj)
		info.updateCaret()
		nextHandler()

class EdgeHTMLRoot(UIA):

	treeInterceptorClass=EdgeHTMLTreeInterceptor
	role=controlTypes.ROLE_DOCUMENT
