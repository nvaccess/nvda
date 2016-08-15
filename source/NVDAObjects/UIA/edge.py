#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015-2016 NV Access Limited

from comtypes import COMError
from comtypes.automation import VARIANT
from ctypes import byref
from logHandler import log
import eventHandler
import config
import controlTypes
import aria
import textInfos
import UIAHandler
from UIABrowseMode import UIABrowseModeDocument, UIABrowseModeDocumentTextInfo
import aria
from UIAUtils import *
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

class EdgeHTMLTreeInterceptorTextInfo(UIABrowseModeDocumentTextInfo):

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

class EdgeHTMLTreeInterceptor(UIABrowseModeDocument):

	TextInfo=EdgeHTMLTreeInterceptorTextInfo

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
