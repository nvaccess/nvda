#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015 NV Access Limited

from comtypes import COMError
from comtypes.automation import VARIANT
from ctypes import byref
from logHandler import log
import eventHandler
import config
import controlTypes
import aria
import winUser
import textInfos
import UIAHandler
import browseMode
import treeInterceptorHandler
import cursorManager
import aria
from . import UIA, UIATextInfo

class EdgeTextInfo(UIATextInfo):

	def _getControlFieldForObject(self,obj):
		field=super(EdgeTextInfo,self)._getControlFieldForObject(obj)
		lct=obj.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_LocalizedControlTypePropertyId)
		landmark=None
		if lct in aria.landmarkRoles:
			landmark=lct
		else:
			ar=obj.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_AriaRolePropertyId)
			if ar:
				for ar in ar.split():
					if ar in aria.landmarkRoles:
						landmark=ar
						break
		if landmark and (landmark!='region' or field.get('name')):
			field['landmark']=landmark
		return field

	def _getTextWithFields_text(self,textRange,formatConfig):
		log.debug("_getTextWithFields_text start")
		tempRange=textRange.clone()
		if log.isEnabledFor(log.DEBUG):
			log.debug("full text: %s"%textRange.getText(-1))
		tempRange.MoveEndPointByRange(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)
		delta=-1
		while delta<0:
			if tempRange.MoveEndPointByUnit(UIAHandler.TextUnit_Format,1,UIAHandler.TextPatternRangeEndpoint_End)==0:
				log.debug("Failed to move end by format. Breaking")
				break
			log.debug("Moved end by format")
			delta=tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
			if delta>0:
				log.debug("Moved past end of textRange. Cropping to fit")
				tempRange.MoveEndPointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
			if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)==0:
				log.debug("range is now degenerate. Breaking")
				break
			text=tempRange.getText(-1)
			if text:
				yield self._getFormatFieldAtRange(tempRange,formatConfig)
				yield text
			tempRange.MoveEndPointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
		log.debug("_getTextWithFields_text end")

	def _getTextWithFields_balanced(self,rootElement,textRange,formatConfig,includeRoot=True):
		if log.isEnabledFor(log.DEBUG):
			log.debug("_getTextWithFields_balanced")
			log.debug("rootElement: %s"%rootElement.currentLocalizedControlType)
			log.debug("full text: %s"%textRange.getText(-1))
			log.debug("includeRoot: %s"%includeRoot)
		enclosingElement=textRange.getEnclosingElement()
		if enclosingElement:
			enclosingElement=enclosingElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		else:
			log.debug("No enclosingElement. Returning")
			return
		if log.isEnabledFor(log.DEBUG):
			log.debug("enclosingElement: %s"%enclosingElement.currentLocalizedControlType)
		parents=[]
		parentElement=enclosingElement
		log.debug("Generating parents")
		while parentElement:
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			isRoot=UIAHandler.handler.clientObject.compareElements(parentElement,rootElement)
			log.debug("isRoot: %s"%isRoot)
			try:
				obj=UIA(UIAElement=parentElement)
				field=self._getControlFieldForObject(obj)
			except LookupError:
				log.debug("Failed to fetch controlField data for parent. Falling back to rootElement")
				parents=[]
				isRoot=True
				try:
					obj=UIA(UIAElement=rootElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
					field=self._getControlFieldForObject(obj)
				except LookupError:
					log.debug("Failed to fetch controlField data on rootElement. Breaking")
					break
			parents.append((parentElement,field,isRoot))
			if isRoot:
				break
			log.debug("Fetching next parentElement")
			parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,UIAHandler.handler.baseCacheRequest)
		log.debug("Done generating parents")
		log.debug("Yielding parent controlStarts")
		for parentElement,field,isRoot in reversed(parents):
			if includeRoot or not isRoot:
				yield textInfos.FieldCommand("controlStart",field)
		log.debug("Done yielding parent controlStarts")
		# Move through the text range, collecting text and recursing into children
		tempRange=textRange.clone()
		tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)
		childElements=textRange.getChildren()
		if log.isEnabledFor(log.DEBUG):
			log.debug("Child count: %s"%childElements.length)
			log.debug("Walking children")
		for index in xrange(childElements.length):
			childElement=childElements.getElement(index)
			if log.isEnabledFor(log.DEBUG):
				log.debug("Fetched child %s (%s)"%(index,childElement.currentLocalizedControlType))
			if UIAHandler.handler.clientObject.compareElements(childElement,rootElement):
				log.debug("childElement is rootElement. Breaking")
				break
			childRange=self.obj.UIATextPattern.rangeFromChild(childElement)
			if not childRange:
				log.debug("NULL childRange. Skipping")
				continue
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_End)>=0:
				log.debug("Child at or past end of textRange. Breaking")
				break
			childStartDelta=childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
			if childStartDelta>0 and childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_Start)>0:
				# plain text before this child
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
				log.debug("Plain text before child")
				for field in self._getTextWithFields_text(tempRange,formatConfig):
					yield field
			elif childStartDelta<0:
				log.debug("textRange started part way through child. Cropping Start of child range to fit" )
				childRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)>0:
				log.debug("textRange ended part way through the child. Crop end of childRange to fit")
				childRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)==0:
				log.debug("childRange is degenerate. Skipping")
				continue
			log.debug("Recursing into child %s"%index)
			for field in self._getTextWithFields_balanced(childElement,childRange,formatConfig):
				yield field
			log.debug("Done recursing into child %s"%index)
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)
		log.debug("children done")
		# Plain text after the final child
		if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)<0:
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
			log.debug("Yielding final text")
			for field in self._getTextWithFields_text(tempRange,formatConfig):
				yield field
		log.debug("Done yielding final text")
		log.debug("Yielding controlEnds for parents")
		for parentElement,field,isRoot in parents:
			if includeRoot or not isRoot:
				yield textInfos.FieldCommand("controlEnd",field)
		log.debug("Done yielding controlEnds for parents")
		log.debug("_getTextWithFields_balanced end")

	def _getTextWithFields_unbalanced(self,rootElement,textRange,formatConfig,includeRoot=True):
		if log.isEnabledFor(log.DEBUG):
			log.debug("_getTextWithFields_unbalanced")
			log.debug("rootElement: %s"%rootElement.currentLocalizedControlType)
			log.debug("full text: %s"%textRange.getText(-1))
			log.debug("includeRoot: %s"%includeRoot)
		startRange=textRange.clone()
		startRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,startRange,UIAHandler.TextPatternRangeEndpoint_Start)
		enclosingElement=startRange.getEnclosingElement()
		if enclosingElement:
			enclosingElement=enclosingElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		else:
			log.debug("No enclosingElement. Returning")
			return
		enclosingRange=self.obj.UIATextPattern.rangeFromChild(enclosingElement)
		if not enclosingRange:
			log.debug("enclosingRange is NULL. Returning")
			return
		if log.isEnabledFor(log.DEBUG):
			log.debug("enclosingElement: %s"%enclosingElement.currentLocalizedControlType)
		parents=[]
		parentElement=enclosingElement
		log.debug("Generating ancestors:")
		while parentElement:
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			isRoot=UIAHandler.handler.clientObject.compareElements(parentElement,rootElement)
			log.debug("isRoot: %s"%isRoot)
			try:
				obj=UIA(UIAElement=parentElement)
				field=self._getControlFieldForObject(obj)
			except LookupError:
				log.debug("Failed to fetch controlField data for parentElement. Falling back to rootElement")
				parents=[]
				isRoot=True
				try:
					obj=UIA(UIAElement=rootElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
					field=self._getControlFieldForObject(obj)
				except LookupError:
					log.debug("Failed to fetch controlField data on rootElement. Breaking")
					break
			parents.append((parentElement,field,isRoot))
			if isRoot:
				break
			log.debug("Fetching next parentElement")
			parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,UIAHandler.handler.baseCacheRequest)
		log.debug("Done generating parents")
		log.debug("Yielding parents in reverse order")
		for parentElement,field,isRoot in reversed(parents):
			if includeRoot or not isRoot:
				yield textInfos.FieldCommand("controlStart",field)
		log.debug("Done yielding parents")
		enclosingRange=self.obj.UIATextPattern.rangeFromChild(enclosingElement)
		startRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,enclosingRange,UIAHandler.TextPatternRangeEndpoint_End)
		if startRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)>0:
			startRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
		log.debug("Yielding balanced fields for startRange")
		for field in self._getTextWithFields_balanced(enclosingElement,startRange,formatConfig,includeRoot=False):
			yield field
		log.debug("Done yielding balanced fields for startRange")
		tempRange=startRange.clone()
		log.debug("Walking parents to yield controlEnds and recurse unbalanced endRanges")
		for parentElement,field,isRoot in parents:
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			if parentElement is not enclosingElement:
				log.debug("is enclosingElement: True")
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
				try:
					parentRange=self.obj.UIATextPattern.rangeFromChild(parentElement)
				except COMError:
					parentRange=None
				if parentRange:
					tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,parentRange,UIAHandler.TextPatternRangeEndpoint_End)
				else:
					log.debug("NULL parentRange")
					if isRoot:
						log.debug("falling back to textRange as parent is root")
						tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
				if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)>0:
					tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
				if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)>0:
					log.debug("Recursing endRange")
					for endField in self._getTextWithFields_unbalanced(parentElement,tempRange,formatConfig,includeRoot=False):
						yield endField
					log.debug("Done recursing endRange")
			if includeRoot or not isRoot:
				"Yielding controlEnd for parent"
				yield textInfos.FieldCommand("controlEnd",field)
		log.debug("Done walking parents to yield controlEnds and recurse unbalanced endRanges")
		log.debug("_getTextWithFields_unbalanced end")

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		fields=[]
		for field in self._getTextWithFields_unbalanced(self.obj.UIAElement,self._rangeObj,formatConfig,False):
			if log.isEnabledFor(log.DEBUG):
				log.debug("field: %s"%field)
			fields.append(field)
		return fields

class EdgeNode(UIA):

	_TextInfo=EdgeTextInfo

	def _get_role(self):
		role=super(EdgeNode,self).role
		ariaRole=self.UIAElement.currentAriaRole
		for ariaRole in ariaRole.split():
			newRole=aria.ariaRolesToNVDARoles.get(ariaRole)
			if newRole:
				role=newRole
				break
		return role

class EdgeList(EdgeNode):

	# non-focusable lists are readonly lists (ensures correct NVDA presentation category)
	def _get_states(self):
		states=super(EdgeList,self).states
		if controlTypes.STATE_FOCUSABLE not in states:
			states.add(controlTypes.STATE_READONLY)
		return states

class EdgeHTMLRootContainer(EdgeNode):

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

class HeadingUIATextRangeQuickNavItem(UIATextRangeQuickNavItem):

	@property
	def level(self):
		return int(self.itemType[7:]) if len(self.itemType)>7 else 0

	def isChild(self,parent):
		if not isinstance(parent,HeadingUIATextRangeQuickNavItem):
			return False
		return self.level>parent.level

def createUIAMultiPropertyCondition(*dicts):
	outerOrList=[]
	for dict in dicts:
		andList=[]
		for key,values in dict.iteritems():
			innerOrList=[]
			if not isinstance(values,list):
				values=[values]
			for value in values:
				condition=UIAHandler.handler.clientObject.createPropertyCondition(key,value)
				innerOrList.append(condition)
			if len(innerOrList)==0:
				continue
			elif len(innerOrList)==1:
				condition=innerOrList[0]
			else:
				condition=UIAHandler.handler.clientObject.createOrConditionFromArray(innerOrList)
			andList.append(condition)
		if len(andList)==0:
			continue
		elif len(andList)==1:
			condition=andList[0]
		else:
			condition=UIAHandler.handler.clientObject.createAndConditionFromArray(andList)
		outerOrList.append(condition)
	if len(outerOrList)==0:
		raise ValueError("no properties")
	elif len(outerOrList)==1:
		condition=outerOrList[0]
	else:
		condition=UIAHandler.handler.clientObject.createOrConditionFromArray(outerOrList)
	return condition

def UIATextAttributeQuickNavIterator(itemType,document,position,attributeID,attributeValue,direction="next",ItemClass=UIATextRangeQuickNavItem):
	includeCurrent=False
	story=document.makeTextInfo(textInfos.POSITION_ALL)
	if not position:
		curPosition=story
		includeCurrent=True
	else:
		curPosition=position.copy()
		curPosition.setEndPoint(story,"startToStart" if direction=="previous" else "endToEnd")
	while True:
		try:
			newRange=curPosition._rangeObj.findAttribute(attributeID,attributeValue,direction=="previous")
		except COMError:
			newRange=None
		if not newRange:
			return
		newPosition=document.TextInfo(document,None,_rangeObj=newRange)
		if includeCurrent or not newPosition.isOverlapping(position):
			yield ItemClass(itemType,document,newRange)
		curPosition.setEndPoint(newPosition,"endToStart" if direction=="previous" else "startToEnd")

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

class EdgeHTMLTreeInterceptorTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):
	pass

class EdgeHTMLTreeInterceptor(cursorManager.ReviewCursorManager,browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=EdgeHTMLTreeInterceptorTextInfo

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent.name

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType=="heading":
			return browseMode.mergeQuickNavItemIterators([UIATextAttributeQuickNavIterator("heading%d"%level,self,pos,UIAHandler.UIA_StyleIdAttributeId,UIAHandler.StyleId_Heading1+(level-1),direction,HeadingUIATextRangeQuickNavItem) for level in xrange(1,7)],direction)
		elif nodeType.startswith("heading"):
			level=int(nodeType[7:])
			return UIATextAttributeQuickNavIterator(nodeType,self,pos,UIAHandler.UIA_StyleIdAttributeId,UIAHandler.StyleId_Heading1+(level-1),direction,HeadingUIATextRangeQuickNavItem)
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

class EdgeHTMLRoot(EdgeNode):

	treeInterceptorClass=EdgeHTMLTreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in self.states 

	def _get_role(self):
		role=super(EdgeHTMLRoot,self).role
		if role==controlTypes.ROLE_PANE:
			role=controlTypes.ROLE_DOCUMENT
		return role
