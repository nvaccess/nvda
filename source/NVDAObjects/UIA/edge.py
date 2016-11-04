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
import cursorManager
import aria
import textInfos
import UIAHandler
from UIABrowseMode import UIABrowseModeDocument, UIABrowseModeDocumentTextInfo
import aria
from UIAUtils import *
from . import UIA, UIATextInfo

class EdgeTextInfo(UIATextInfo):

	def _hasEmbedded(self):
		"""Is this textInfo positioned on an embedded child?"""
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

	def _get_UIAElementAtStartWithReplacedContent(self):
		"""Fetches the deepest UIAElement at the start of the text range whos name has been overridden by the author (such as aria-label)."""
		element=self.UIAElementAtStart
		condition=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:self.UIAControlTypesWhereNameIsContent})
		# A part from the condition given, we must always match on the root of the document so we know when to stop walking
		runtimeID=VARIANT()
		self.obj.UIAElement._IUIAutomationElement__com_GetCurrentPropertyValue(UIAHandler.UIA_RuntimeIdPropertyId,byref(runtimeID))
		condition=UIAHandler.handler.clientObject.createOrCondition(UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_RuntimeIdPropertyId,runtimeID),condition)
		walker=UIAHandler.handler.clientObject.createTreeWalker(condition)
		cacheRequest=UIAHandler.handler.clientObject.createCacheRequest()
		cacheRequest.addProperty(UIAHandler.UIA_AriaPropertiesPropertyId)
		element=walker.normalizeElementBuildCache(element,cacheRequest)
		while element and not UIAHandler.handler.clientObject.compareElements(element,self.obj.UIAElement):
			ariaProperties=element.getCachedPropertyValue(UIAHandler.UIA_AriaPropertiesPropertyId)
			if ('label=' in ariaProperties)  or ('labelledby=' in ariaProperties):
				return element
			try:
				range=self.obj.UIATextPattern.rangeFromChild(element)
			except COMEror:
				return
			text=range.getText(-1)
			if not text or text.isspace():
				return element
			element=walker.getParentElementBuildCache(element,cacheRequest)

	def _moveToEdgeOfReplacedContent(self,back=False):
		"""If within replaced content (E.g. aria-label is used), moves to the first or last character covered, so that a following call to move in the same direction will move out of the replaced content, in order to ensure that the content only takes up one character stop.""" 
		element=self.UIAElementAtStartWithReplacedContent
		if not element:
			return
		try:
			range=self.obj.UIATextPattern.rangeFromChild(element)
		except COMError:
			return
		if not back:
			range.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,range,UIAHandler.TextPatternRangeEndpoint_End)
		else:
			range.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,range,UIAHandler.TextPatternRangeEndpoint_Start)
			range.move(UIAHandler.TextUnit_Character,1)
		self._rangeObj=range

	def _collapsedMove(self,unit,direction,skipReplacedContent):
		"""A simple collapsed move (i.e. both ends move together), but whether it classes replaced content as one character stop can be configured via the skipReplacedContent argument."""
		if not skipReplacedContent: 
			return super(EdgeTextInfo,self).move(unit,direction)
		if direction==0: 
			return
		chunk=1 if direction>0 else -1
		finalRes=0
		while finalRes!=direction:
			self._moveToEdgeOfReplacedContent(back=direction<0)
			res=super(EdgeTextInfo,self).move(unit,chunk)
			if res==0:
				break
			finalRes+=res
		return finalRes

	def move(self,unit,direction,endPoint=None,skipReplacedContent=True):
		# Skip over non-text element starts and ends
		if not endPoint:
			if direction>0 and unit in (textInfos.UNIT_LINE,textInfos.UNIT_PARAGRAPH):
				return self._collapsedMove(unit,direction,skipReplacedContent)
			elif direction>0:
				res=self._collapsedMove(unit,direction,skipReplacedContent)
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
				res=self._collapsedMove(unit,direction,skipReplacedContent)
				if res!=0:
					while True:
						tempInfo.setEndPoint(self,"startToStart")
						if tempInfo.text or tempInfo._hasEmbedded():
							break
						if super(EdgeTextInfo,self).move(textInfos.UNIT_CHARACTER,-1)==0:
							break
				return res
		else:
			tempInfo=self.copy()
			res=tempInfo.move(unit,direction,skipReplacedContent=skipReplacedContent)
			if res!=0:
				self.setEndPoint(tempInfo,"endToEnd" if endPoint=="end" else "startToStart")
			return res

	def expand(self,unit):
		# Ensure expanding to character/word correctly covers embedded controls
		if unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD):
			tempInfo=self.copy()
			tempInfo.move(textInfos.UNIT_CHARACTER,1,endPoint="end",skipReplacedContent=False)
			if tempInfo._hasEmbedded():
				self.setEndPoint(tempInfo,"endToEnd")
				return
		super(EdgeTextInfo,self).expand(unit)
		return

	def _getControlFieldForObject(self,obj,isEmbedded=False,startOfNode=False,endOfNode=False):
		field=super(EdgeTextInfo,self)._getControlFieldForObject(obj,isEmbedded=isEmbedded,startOfNode=startOfNode,endOfNode=endOfNode)
		field['embedded']=isEmbedded
		# report landmarks
		landmark=obj.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_LocalizedLandmarkTypePropertyId)
		if landmark and (landmark!='region' or field.get('name')):
			field['landmark']=aria.landmarkRoles.get(landmark)
		# Combo boxes with a text pattern are editable
		if obj.role==controlTypes.ROLE_COMBOBOX and obj.UIATextPattern:
			field['states'].add(controlTypes.STATE_EDITABLE)
		# For certain controls, if ARIA overrides the label, then force the field's content (value) to the label
		# Later processing in Edge's getTextWithFields will remove descendant content from fields with a content attribute.
		ariaProperties=obj.UIAElement.currentAriaProperties
		hasAriaLabel=('label=' in ariaProperties)
		hasAriaLabelledby=('labelledby=' in ariaProperties)
		if field.get('nameIsContent'):
			content=""
			field.pop('name',None)
			if hasAriaLabel or hasAriaLabelledby:
				content=obj.name
			if not content:
				text=self.obj.makeTextInfo(obj).text
				if not text or text.isspace():
					content=obj.name or field.pop('description',None)
			if content:
				field['content']=content
		elif isEmbedded:
			field['content']=obj.value
			if field['role']==controlTypes.ROLE_GROUPING:
				field['role']=controlTypes.ROLE_EMBEDDEDOBJECT
				if not obj.value:
					field['content']=obj.name
		# Give lists an item count
		if obj.role==controlTypes.ROLE_LIST:
			child=UIAHandler.handler.clientObject.ControlViewWalker.GetFirstChildElement(obj.UIAElement)
			if child:
				field['_childcontrolcount']=child.getCurrentPropertyValue(UIAHandler.UIA_SizeOfSetPropertyId)
		return field

	def _getTextWithFieldsForUIARange(self,rootElement,textRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True,_rootElementRange=None):
		# Edge zooms into its children at the start.
		# Thus you are already in the deepest first child.
		# Therefore get the deepest enclosing element at the start, get its content, Then do the whole thing again on the content from the end of the enclosing element to the end of its parent, and repete!
		# In other words, get the content while slowly zooming out from the start.
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
		enclosingRange=self.obj.getNormalizedUIATextRangeFromElement(enclosingElement)
		if not enclosingRange:
			log.debug("enclosingRange is NULL. Returning")
			return
		if log.isEnabledFor(log.DEBUG):
			log.debug("enclosingElement: %s"%enclosingElement.currentLocalizedControlType)
		startRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,enclosingRange,UIAHandler.TextPatternRangeEndpoint_End)
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
			if parentElement is not enclosingElement:
				if includeRoot or not isRoot:
					try:
						obj=UIA(windowHandle=self.obj.windowHandle,UIAElement=parentElement)
						field=self._getControlFieldForObject(obj)
					except LookupError:
						log.debug("Failed to fetch controlField data for parentElement. Breaking")
						break
					parents.append((parentElement,field))
				else:
					# This is the root but it was not requested for inclusion
					# However we still need the root element itself for further recursion
					parents.append((parentElement,None))
			if isRoot:
				log.debug("Hit root. Breaking")
				break
			log.debug("Fetching next parentElement")
			parentElement=UIAHandler.handler.baseTreeWalker.getParentElementBuildCache(parentElement,UIAHandler.handler.baseCacheRequest)
		log.debug("Done generating parents")
		log.debug("Yielding parents in reverse order")
		for parentElement,field in reversed(parents):
			if field: yield textInfos.FieldCommand("controlStart",field)
		log.debug("Done yielding parents")
		log.debug("Yielding balanced fields for startRange")
		for field in super(EdgeTextInfo,self)._getTextWithFieldsForUIARange(enclosingElement,startRange,formatConfig,_rootElementRange=enclosingRange,includeRoot=includeRoot or hasAncestors,alwaysWalkAncestors=False,recurseChildren=True):
			yield field
		tempRange=startRange.clone()
		log.debug("Walking parents to yield controlEnds and recurse unbalanced endRanges")
		for parentElement,field in parents:
			if log.isEnabledFor(log.DEBUG):
				log.debug("parentElement: %s"%parentElement.currentLocalizedControlType)
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
			parentRange=self.obj.getNormalizedUIATextRangeFromElement(parentElement)
			if parentRange:
				tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,parentRange,UIAHandler.TextPatternRangeEndpoint_End)
				if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)>0:
					tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,textRange,UIAHandler.TextPatternRangeEndpoint_End)
					clippedEnd=True
				else:
					clippedEnd=False
				if field:
					clippedStart=parentRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,textRange,UIAHandler.TextPatternRangeEndpoint_Start)<0
					field['_startOfNode']=not clippedStart
					field['_endOfNode']=not clippedEnd
				if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)>0:
					log.debug("Recursing endRange")
					for endField in self._getTextWithFieldsForUIARange(parentElement,tempRange,formatConfig,includeRoot=False,alwaysWalkAncestors=True,recurseChildren=True):
						yield endField
					log.debug("Done recursing endRange")
				else:
					log.debug("No content after parent")
			if field:
				log.debug("Yielding controlEnd for parent")
				yield textInfos.FieldCommand("controlEnd",field)
		log.debug("Done walking parents to yield controlEnds and recurse unbalanced endRanges")
		log.debug("_getTextWithFieldsForUIARange (unbalanced) end")

	def getTextWithFields(self,formatConfig=None):
		# We don't want fields for collapsed ranges.
		# This would normally be a general rule, but MS Word currently needs fields for collapsed ranges, thus this code is not in the base.
		if self.isCollapsed:
			return []
		fields=super(EdgeTextInfo,self).getTextWithFields(formatConfig)
		seenText=False
		curStarts=[]
		# remove clickable state on descendants of controls with clickable state
		clickableField=None
		for field in fields:
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				states=field.field['states']
				if clickableField:
					states.discard(controlTypes.STATE_CLICKABLE)
				elif controlTypes.STATE_CLICKABLE in states:
					clickableField=field.field
			elif clickableField and isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd" and field.field is clickableField:
				clickableField=None
		# Chop extra whitespace off the end incorrectly put there by Edge
		numFields=len(fields)
		index=0
		while index<len(fields):
			field=fields[index]
			if index>1 and isinstance(field,basestring) and field.isspace():
				prevField=fields[index-2]
				if isinstance(prevField,textInfos.FieldCommand) and prevField.command=="controlEnd":
					del fields[index-1:index+1]
			index+=1
		# chop fields off the end incorrectly placed there by Edge
		# This can happen if expanding to line covers element start chars at its end
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
		# Remove any content from fields with a content attribute
		numFields=len(fields)
		curField=None
		for index in xrange(numFields-1,-1,-1):
			field=fields[index]
			if not curField and isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd" and field.field.get('content'):
				curField=field.field
				endIndex=index
			elif curField and isinstance(field,textInfos.FieldCommand) and field.command=="controlStart" and field.field is curField:
				fields[index+1:endIndex]=" "
				curField=None
		return fields

class EdgeNode(UIA):

	_TextInfo=EdgeTextInfo

	def getNormalizedUIATextRangeFromElement(self,UIAElement):
		range=super(EdgeNode,self).getNormalizedUIATextRangeFromElement(UIAElement)
		if not range:
			return
		#Move the start of a UIA text range past any element start character stops
		lastCharInfo=EdgeTextInfo(self,None,_rangeObj=range)
		lastCharInfo._rangeObj=range
		charInfo=lastCharInfo.copy()
		charInfo.collapse()
		while super(EdgeTextInfo,charInfo).move(textInfos.UNIT_CHARACTER,1)!=0:
			charInfo.setEndPoint(lastCharInfo,"startToStart")
			if charInfo.text or charInfo._hasEmbedded():
				break
			lastCharInfo.setEndPoint(charInfo,"startToEnd")
			charInfo.collapse(True)
		return range

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

	def _get_description(self):
		ariaProperties=self.UIAElement.currentAriaProperties
		if 'describedby=' in ariaProperties:
			try:
				return self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_FullDescriptionPropertyId) or ""
			except COMError:
				pass
		return super(EdgeNode,self).description

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

class EdgeHTMLTreeInterceptor(cursorManager.ReviewCursorManager,UIABrowseModeDocument):

	TextInfo=UIABrowseModeDocumentTextInfo

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent.name

	def shouldPassThrough(self,obj,reason=None):
		# Enter focus mode for selectable list items (<select> and role=listbox)
		if reason==controlTypes.REASON_FOCUS and obj.role==controlTypes.ROLE_LISTITEM and controlTypes.STATE_SELECTABLE in obj.states:
			return True
		return super(EdgeHTMLTreeInterceptor,self).shouldPassThrough(obj,reason=reason)

class EdgeHTMLRoot(EdgeNode):

	treeInterceptorClass=EdgeHTMLTreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role==controlTypes.ROLE_DOCUMENT

	def _get_role(self):
		role=super(EdgeHTMLRoot,self).role
		if role==controlTypes.ROLE_PANE:
			role=controlTypes.ROLE_DOCUMENT
		return role
