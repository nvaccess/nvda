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

	def _normalizeUIARange(self,range):
		info=self.copy()
		info._rangeObj=range
		tempInfo=info.copy()
		tempInfo.collapse()
		while super(EdgeTextInfo,tempInfo).move(textInfos.UNIT_CHARACTER,1)!=0:
			tempInfo.setEndPoint(info,"startToStart")
			if tempInfo.text or tempInfo._hasEmbedded():
				break
			info.setEndPoint(tempInfo,"startToEnd")
			tempInfo.collapse(True)

	def _hasEmbedded(self):
		children=self._rangeObj.getChildren()
		if children.length:
			child=children.getElement(0)
			if not child.getCurrentPropertyValue(UIAHandler.UIA_IsTextPatternAvailablePropertyId):
				childRange=self.obj.UIATextPattern.rangeFromChild(child)
				if childRange:
					childChildren=childRange.getChildren()
				if childChildren.length==1 and UIAHandler.handler.clientObject.compareElements(child,childChildren.getElement(0)):
					return True
		return False

	def move(self,unit,direction,endPoint=None):
		# Skip over non-text element starts and ends
		if not endPoint:
			if direction>0 and unit in (textInfos.UNIT_LINE,textInfos.UNIT_PARAGRAPH):
				return super(EdgeTextInfo,self).move(unit,direction)
			elif direction>0:
				res=super(EdgeTextInfo,self).move(unit,direction)
				if res!=0:
					# Ensure we move past the start of any elements 
					tempInfo=self.copy()
					while super(EdgeTextInfo,tempInfo).move(textInfos.UNIT_CHARACTER,1)!=0:
						tempInfo.setEndPoint(self,"startToStart")
						if tempInfo.text or tempInfo._hasEmbedded():
							break
						tempInfo.collapse(True)
						self._rangeObj=tempInfo._rangeObj.clone()
				return res
			elif direction<0:
				tempInfo=self.copy()
				res=super(EdgeTextInfo,self).move(unit,direction)
				if res!=0:
					tempInfo.setEndPoint(self,"startToStart")
					if not tempInfo.text and not tempInfo._hasEmbedded():
						self.move(textInfos.UNIT_CHARACTER,-1)
				return res
		else:
			tempInfo=self.copy()
			res=tempInfo.move(unit,direction)
			if res!=0:
				self.setEndPoint(tempInfo,"endToEnd" if endPoint=="end" else "startToStart")
			return res

	def expand(self,unit):
		# Ensure expanding to character/word correctly covers embedded controls
		tempInfo=self.copy()
		tempInfo.move(textInfos.UNIT_CHARACTER,1,endPoint="end")
		if tempInfo._hasEmbedded():
			self.setEndPoint(tempInfo,"endToEnd")
			return
		super(EdgeTextInfo,self).expand(unit)
		return

	def _getControlFieldForObject(self,obj,isEmbedded=False,startOfNode=False,endOfNode=False):
		field=super(EdgeTextInfo,self)._getControlFieldForObject(obj,isEmbedded=isEmbedded,startOfNode=startOfNode,endOfNode=endOfNode)
		landmark=obj.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_LocalizedLandmarkTypePropertyId)
		if landmark and (landmark!='region' or field.get('name')):
			field['landmark']=aria.landmarkRoles.get(landmark)
		if obj.role==controlTypes.ROLE_EDITABLETEXT:
			field["name"] = obj.name
		ariaProperties=obj.UIAElement.currentAriaProperties
		hasAriaLabel=('label=' in ariaProperties)
		hasAriaLabelledby=('labelledby=' in ariaProperties)
		if hasAriaLabelledby:
			field['name']=obj.name
		if hasAriaLabel or hasAriaLabelledby:
			if obj.role in (controlTypes.ROLE_LINK,controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_BUTTON):
				field['value']=obj.name
				field['alwaysReportValue']=True
			elif obj.role in (controlTypes.ROLE_GROUPING,controlTypes.ROLE_PANE):
				field['alwaysReportName']=True
		if obj.role==controlTypes.ROLE_LIST:
			child=UIAHandler.handler.clientObject.ControlViewWalker.GetFirstChildElement(obj.UIAElement)
			if child:
				field['_childcontrolcount']=child.getCurrentPropertyValue(UIAHandler.UIA_SizeOfSetPropertyId)
		return field

	def _getTextWithFieldsForUIARange(self,rootElement,textRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True,_rootElementRange=None):
		log.debug("_getTextWithFieldsForUIARange (unbalanced)")
		if not recurseChildren:
			log.debug("recurseChildren is False. Falling back to super")
			for field in super(EdgeTextInfo,self)._getTextWithFieldsForUIARange(rootElement,textRange,formatConfig,includeRoot=includeRoot,alwaysWalkAncestors=True,recurseChildren=False,_rootElementRange=_rootElementRange):
				yield field
			return
		if log.isEnabledFor(log.DEBUG):
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
		startRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,enclosingRange,UIAHandler.TextPatternRangeEndpoint_End)
		self._normalizeUIARange(enclosingRange)
		if startRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)>0:
			startRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
		# check for an embedded child
		childElements=startRange.getChildren()
		if childElements.length==1 and UIAHandler.handler.clientObject.compareElements(rootElement,childElements.getElement(0)):
			log.debug("Using single embedded child as enclosingElement")
			for field in super(EdgeTextInfo,self)._getTextWithFieldsForUIARange(rootElement,startRange,formatConfig,_rootElementRange=_rootElementRange,includeRoot=includeRoot,alwaysWalkAncestors=False,recurseChildren=False):
				yield field
			return
		parents=[]
		parentElement=enclosingElement
		log.debug("Generating ancestors:")
		hasAncestors=False
		while parentElement:
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			isRoot=UIAHandler.handler.clientObject.compareElements(parentElement,rootElement)
			log.debug("isRoot: %s"%isRoot)
			if not isRoot:
				hasAncestors=True
			if not includeRoot and isRoot:
				log.debug("root not requested. Breaking")
				break
			if parentElement is not enclosingElement:
				try:
					obj=UIA(UIAElement=parentElement)
					field=self._getControlFieldForObject(obj)
				except LookupError:
					log.debug("Failed to fetch controlField data for parentElement. Breaking")
					break
				parents.append((parentElement,field))
			if isRoot:
				log.debug("Hit root. Breaking")
				break
			log.debug("Fetching next parentElement")
			parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,UIAHandler.handler.baseCacheRequest)
		log.debug("Done generating parents")
		log.debug("Yielding parents in reverse order")
		for parentElement,field in reversed(parents):
			yield textInfos.FieldCommand("controlStart",field)
		log.debug("Done yielding parents")
		log.debug("Yielding balanced fields for startRange")
		for field in super(EdgeTextInfo,self)._getTextWithFieldsForUIARange(enclosingElement,startRange,formatConfig,_rootElementRange=enclosingRange,includeRoot=includeRoot or hasAncestors,alwaysWalkAncestors=False,recurseChildren=True):
			yield field
		tempRange=startRange.clone()
		log.debug("Walking parents to yield controlEnds and recurse unbalanced endRanges")
		for parentElement,field in parents:
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			log.debug("is enclosingElement: False")
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
			try:
				parentRange=self.obj.UIATextPattern.rangeFromChild(parentElement)
			except COMError:
				log.debug("Error fetching parent range")
				parentRange=None
			if parentRange:
				self._normalizeUIARange(parentRange)
				clippedStart=parentRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_Start)<0
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,parentRange,UIAHandler.TextPatternRangeEndpoint_End)
				if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)>0:
					tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
					clippedEnd=True
				else:
					clippedEnd=False
				field['_startOfNode']=not clippedStart
				field['_endOfNode']=not clippedEnd
				if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)>0:
					log.debug("Recursing endRange")
					for endField in self._getTextWithFieldsForUIARange(parentElement,tempRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True):
						yield endField
					log.debug("Done recursing endRange")
			log.debug("Yielding controlEnd for parent")
			yield textInfos.FieldCommand("controlEnd",field)
		log.debug("Done walking parents to yield controlEnds and recurse unbalanced endRanges")
		log.debug("_getTextWithFieldsForUIARange (unbalanced) end")

	def getTextWithFields(self,formatConfig=None):
		fields=super(EdgeTextInfo,self).getTextWithFields(formatConfig)
		seenText=False
		curStarts=[]
		# Chop extra fields off the end incorrectly put there by Edge
		numFields=len(fields)
		for index in xrange(numFields-1,-1,-1):
			field=fields[index]
			if index>1 and isinstance(field,basestring) and field.isspace():
				prevField=fields[index-2]
				if isinstance(prevField,textInfos.FieldCommand) and prevField.command=="controlEnd":
					del fields[index-1:index+1]
		startCount=0
		lastStartIndex=None
		numFields=len(fields)
		for index in xrange(numFields-1,-1,-1):
			field=fields[index]
			if isinstance(field,basestring):
				break
			elif isinstance(field,textInfos.FieldCommand) and field.command=="controlStart" and not field.field.get('embedded'):
				startCount+=1
				lastStartIndex=index
		if lastStartIndex:
			del fields[lastStartIndex:lastStartIndex+(startCount*2)]
		# Remove any content from fields with a value
		numFields=len(fields)
		curField=None
		for index in xrange(numFields-1,-1,-1):
			field=fields[index]
			if not curField and isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd" and field.field.get('value'):
				curField=field.field
				endIndex=index
			elif curField and isinstance(field,textInfos.FieldCommand) and field.command=="controlStart" and field.field is curField:
				fields[index+1:endIndex]=" " #curField.pop('value')
				curField=None
		return fields

class EdgeNode(UIA):

	_TextInfo=EdgeTextInfo

	def _get_role(self):
		role=super(EdgeNode,self).role
		if not isinstance(self,EdgeHTMLRoot) and role==controlTypes.ROLE_PANE and self.UIATextPattern:
			return controlTypes.ROLE_INTERNALFRAME
		ariaRole=self.UIAElement.currentAriaRole
		for ariaRole in ariaRole.split():
			newRole=aria.ariaRolesToNVDARoles.get(ariaRole)
			if newRole:
				role=newRole
				break
		return role

	def _get_states(self):
		states=super(EdgeNode,self).states
		if self.role in (controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_GROUPING,controlTypes.ROLE_SECTION,controlTypes.ROLE_GRAPHIC) and self.UIAInvokePattern:
			states.add(controlTypes.STATE_CLICKABLE)
		return states

class EdgeList(EdgeNode):

	# non-focusable lists are readonly lists (ensures correct NVDA presentation category)
	def _get_states(self):
		states=super(EdgeList,self).states
		if controlTypes.STATE_FOCUSABLE not in states:
			states.add(controlTypes.STATE_READONLY)
		return states

class EdgeHTMLRootContainer(EdgeNode):

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
		if direction=="previous":
			curPosition.move(textInfos.UNIT_CHARACTER,-1,endPoint="end")
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
		styleIDValue=tempInfo.innerTextInfo._getUIATextAttributeValueFromRange(tempInfo._rangeObj,UIAHandler.UIA_StyleIdAttributeId)
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

class EdgeHTMLTreeInterceptorTextInfo(browseMode.BrowseModeDocumentTextInfo,treeInterceptorHandler.RootProxyTextInfo):

	def _get_focusableNVDAObjectAtStart(self):
		# Work around MS Edge bug 8246010
		obj=self.NVDAObjectAtStart
		condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_IsKeyboardFocusablePropertyId,True)
		runtimeID=VARIANT()
		self.obj.rootNVDAObject.UIAElement._IUIAutomationElement__com_GetCurrentPropertyValue(UIAHandler.UIA_RuntimeIdPropertyId,byref(runtimeID))
		condition=UIAHandler.handler.clientObject.createOrCondition(UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_RuntimeIdPropertyId,runtimeID),condition)
		walker=UIAHandler.handler.clientObject.createTreeWalker(condition)
		e=walker.normalizeElementBuildCache(obj.UIAElement,UIAHandler.handler.baseCacheRequest)
		if e:
			obj=UIA(UIAElement=e)
			if obj:
				return obj
		return self.obj.rootNVDAObject

class EdgeHTMLTreeInterceptor(cursorManager.ReviewCursorManager,browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=EdgeHTMLTreeInterceptorTextInfo

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent.name

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

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent.name

	def shouldPassThrough(self,obj,reason=None):
		if reason==controlTypes.REASON_FOCUS and obj.role==controlTypes.ROLE_LISTITEM and controlTypes.STATE_SELECTABLE in obj.states:
			return True
		return super(EdgeHTMLTreeInterceptor,self).shouldPassThrough(obj,reason=reason)

class EdgeHTMLRoot(EdgeNode):

	treeInterceptorClass=EdgeHTMLTreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in self.states 

	def _get_role(self):
		role=super(EdgeHTMLRoot,self).role
		if role==controlTypes.ROLE_PANE:
			role=controlTypes.ROLE_DOCUMENT
		return role
