# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2021 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import operator
from comtypes import COMError
import config
import ctypes
import UIAHandler
import weakref
from functools import lru_cache
from logHandler import log
from .constants import WinConsoleAPILevel


def createUIAMultiPropertyCondition(*dicts):
	"""
	A helper function that Creates a complex UI Automation Condition matching on various UI Automation properties with both 'and' and 'or'.
	Arguments to this function are dicts whos keys are UI Automation property IDs, and whos values are a list of possible values for the property ID.
	The dicts are joined with 'or', the keys in each dict are joined with 'and', and the values  for each key are joined with 'or'.
	For example,  to create a condition that matches on a controlType of button or edit and where isReadOnly is True, or, className is 'ding', you would provide arguments of:
	{UIA_ControlTypePropertyId:[UIA_ButtonControlTypeId,UIA_EditControlTypeId],UIA_Value_ValueIsReadOnly:[True]},{UIA_ClassNamePropertyId:['ding']}
	"""
	outerOrList=[]
	for dict in dicts:
		andList=[]
		for key,values in dict.items():
			innerOrList=[]
			if not isinstance(values,(list,set)):
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

def UIATextRangeFromElement(documentTextPattern,element):
	"""Wraps IUIAutomationTextRange::getEnclosingElement, returning None on  COMError."""
	try:
		childRange=documentTextPattern.rangeFromChild(element)
	except COMError:
		childRange=None
	return childRange

def isUIAElementInWalker(element,walker):
		"""
		Checks if the given IUIAutomationElement exists in the given IUIAutomationTreeWalker by calling IUIAutomationTreeWalker::normalizeElement and comparing the fetched element with the given element.
		"""
		try:
			newElement=walker.normalizeElement(element)
		except COMError:
			newElement=None
		return newElement and UIAHandler.handler.clientObject.compareElements(element,newElement)

def getDeepestLastChildUIAElementInWalker(element,walker):
	"""
	Starting from the given IUIAutomationElement, walks to the deepest last child of the given IUIAutomationTreeWalker.
	"""
	descended=False
	while True:
		lastChild=walker.getLastChildElement(element)
		if lastChild:
			descended=True
			element=lastChild
		else:
			break
		return element if descended else None

class UIAMixedAttributeError(ValueError):
	"""Raised when a function would return a UIAutomation text attribute value that is mixed."""
	pass

def getUIATextAttributeValueFromRange(rangeObj,attrib,ignoreMixedValues=False):
	"""
	Wraps IUIAutomationTextRange::getAttributeValue, returning UIAutomation's reservedNotSupportedValue on COMError, and raising UIAMixedAttributeError if a mixed value would be returned and ignoreMixedValues is False.
	"""
	try:
		val = rangeObj.GetAttributeValue(attrib)
	except COMError:
		return UIAHandler.handler.reservedNotSupportedValue
	if val==UIAHandler.handler.ReservedMixedAttributeValue:
		if not ignoreMixedValues:
			raise UIAMixedAttributeError
	return val

def iterUIARangeByUnit(rangeObj,unit,reverse=False):
	"""
	Splits a given UI Automation text range into smaller text ranges the size of the given unit and yields them.
	@param rangeObj: the UI Automation text range to split.
	@type rangeObj: L{UIAHandler.IUIAutomationTextRange}
	@param unit: a UI Automation text unit.
	@param reverse: true if the range should be walked backwards (from end to start)
	@type reverse: bool
	@rtype: a generator that yields L{UIAHandler.IUIAutomationTextRange} objects.
	"""
	Endpoint_relativeEnd=UIAHandler.TextPatternRangeEndpoint_Start if reverse else UIAHandler.TextPatternRangeEndpoint_End
	Endpoint_relativeStart=UIAHandler.TextPatternRangeEndpoint_End if reverse else UIAHandler.TextPatternRangeEndpoint_Start
	minRelativeDistance=-1 if reverse else 1
	relativeGTOperator=operator.lt if reverse else operator.gt
	relativeLTOperator=operator.gt if reverse else operator.lt
	tempRange=rangeObj.clone()
	tempRange.MoveEndpointByRange(Endpoint_relativeEnd,rangeObj,Endpoint_relativeStart)
	endRange=tempRange.Clone()
	loopCount = 0
	while relativeGTOperator(endRange.Move(unit,minRelativeDistance),0):
		loopCount += 1
		tempRange.MoveEndpointByRange(Endpoint_relativeEnd,endRange,Endpoint_relativeStart)
		pastEnd=relativeGTOperator(tempRange.CompareEndpoints(Endpoint_relativeEnd,rangeObj,Endpoint_relativeEnd),0)
		if pastEnd:
			tempRange.MoveEndpointByRange(Endpoint_relativeEnd,rangeObj,Endpoint_relativeEnd)
		yield tempRange.clone()
		if pastEnd:
			return
		tempRange.MoveEndpointByRange(Endpoint_relativeStart,tempRange,Endpoint_relativeEnd)
		delta = tempRange.CompareEndpoints(Endpoint_relativeStart, rangeObj, Endpoint_relativeEnd)
		if relativeGTOperator(delta, -1):
			# tempRange is now already entirely past the end of the given range.
			# Can be seen with MS Word bullet points: #9613
			return
	# Ensure that we always reach the end of the outer range, even if the units seem to stop somewhere inside
	if relativeLTOperator(tempRange.CompareEndpoints(Endpoint_relativeEnd,rangeObj,Endpoint_relativeEnd),0):
		tempRange.MoveEndpointByRange(Endpoint_relativeEnd,rangeObj,Endpoint_relativeEnd)
		yield tempRange.clone()
	elif loopCount == 0:
		# We Could not walk at all.
		# So just yield the original range
		yield rangeObj


def getEnclosingElementWithCacheFromUIATextRange(textRange,cacheRequest):
	"""A thin wrapper around IUIAutomationTextRange3::getEnclosingElementBuildCache if it exists, otherwise IUIAutomationTextRange::getEnclosingElement and then IUIAutomationElement::buildUpdatedCache."""
	if not isinstance(textRange,UIAHandler.IUIAutomationTextRange):
		raise ValueError("%s is not a text range"%textRange)
	try:
		textRange=textRange.QueryInterface(UIAHandler.IUIAutomationTextRange3)
	except (COMError,AttributeError):
		e=textRange.getEnclosingElement()
		if e:
			e=e.buildUpdatedCache(cacheRequest)
		return e
	return textRange.getEnclosingElementBuildCache(cacheRequest)

class CacheableUIAElementArray(object):

	def __init__(self,elementArray,cacheRequest=None):
		self._elementArray=elementArray
		self._cacheRequest=cacheRequest

	@property
	def length(self):
		return self._elementArray.length if self._elementArray else 0

	def getElement(self,index):
		e=self._elementArray.getElement(index)
		if e and self._cacheRequest:
			e=e.buildUpdatedCache(self._cacheRequest)
		return e

def getChildrenWithCacheFromUIATextRange(textRange,cacheRequest):
	"""A thin wrapper around IUIAutomationTextRange3::getChildrenBuildCache if it exists, otherwise IUIAutomationTextRange::getChildren but wraps the result in an object that automatically calls IUIAutomationElement::buildUpdateCache on any element retreaved."""
	if not isinstance(textRange,UIAHandler.IUIAutomationTextRange):
		raise ValueError("%s is not a text range"%textRange)
	try:
		textRange=textRange.QueryInterface(UIAHandler.IUIAutomationTextRange3)
	except (COMError,AttributeError):
		c=textRange.getChildren()
		c=CacheableUIAElementArray(c,cacheRequest)
		return c
	c=textRange.getChildrenBuildCache(cacheRequest)
	c=CacheableUIAElementArray(c)
	return c

def isTextRangeOffscreen(textRange, visiRanges):
	"""Given a UIA text range and a visible textRanges array (returned from obj.UIATextPattern.GetVisibleRanges), determines if the given textRange is not within the visible textRanges."""
	visiLength = visiRanges.length
	if visiLength > 0:
		firstVisiRange = visiRanges.GetElement(0)
		lastVisiRange = visiRanges.GetElement(visiLength - 1)
		return textRange.CompareEndPoints(
			UIAHandler.TextPatternRangeEndpoint_Start, firstVisiRange,
			UIAHandler.TextPatternRangeEndpoint_Start
		) < 0 or textRange.CompareEndPoints(
			UIAHandler.TextPatternRangeEndpoint_Start, lastVisiRange,
			UIAHandler.TextPatternRangeEndpoint_End) >= 0
	else:
		# Visible textRanges not available.
		raise RuntimeError("Visible textRanges array is empty or invalid.")


class UIATextRangeAttributeValueFetcher(object):

	def __init__(self,textRange):
		self.textRange=textRange

	def getValue(self,ID,ignoreMixedValues=False):
		try:
			val=self.textRange.getAttributeValue(ID)
		except COMError:
			# #7124: some text attributes are not supported in  older Operating Systems 
			return UIAHandler.handler.reservedNotSupportedValue
		if not ignoreMixedValues and val==UIAHandler.handler.ReservedMixedAttributeValue:
			raise UIAMixedAttributeError
		return val

class BulkUIATextRangeAttributeValueFetcher(UIATextRangeAttributeValueFetcher):

	def __init__(self,textRange,IDs):
		IDs=list(IDs)
		self.IDsToValues={}
		super(BulkUIATextRangeAttributeValueFetcher,self).__init__(textRange)
		IDsArray=(ctypes.c_long*len(IDs))(*IDs)
		values=textRange.GetAttributeValues(IDsArray,len(IDsArray))
		self.IDsToValues={IDs[x]:values[x] for x in range(len(IDs))}

	def getValue(self,ID,ignoreMixedValues=False):
		val=self.IDsToValues[ID]
		if not ignoreMixedValues and val==UIAHandler.handler.ReservedMixedAttributeValue:
			raise UIAMixedAttributeError
		return val


class FakeEventHandlerGroup:
	"""
	Mimics the behavior of UiAutomation 6+ Event Handler Groups for older versions.
	"""

	@property
	def clientObject(self):
		clientObject = self._clientObjectRef()
		if not clientObject:
			raise RuntimeError
		return clientObject

	def __init__(self, clientObject):
		self._clientObjectRef = weakref.ref(clientObject)
		self._automationEventHandlers = weakref.WeakValueDictionary()
		self._notificationEventHandlers = weakref.WeakValueDictionary()
		self._propertyChangedEventHandlers = weakref.WeakValueDictionary()

	def AddAutomationEventHandler(self, eventId, scope, cacheRequest, handler):
		self._automationEventHandlers[(eventId, scope, cacheRequest)] = handler

	def AddNotificationEventHandler(self, scope, cacheRequest, handler):
		if not isinstance(self.clientObject, UIAHandler.UIA.IUIAutomation5):
			raise RuntimeError
		self._notificationEventHandlers[(scope, cacheRequest)] = handler

	def AddPropertyChangedEventHandler(self, scope, cacheRequest, handler, propertyArray, propertyCount):
		properties = self.clientObject.IntNativeArrayToSafeArray(propertyArray, propertyCount)
		self._propertyChangedEventHandlers[(scope, cacheRequest, properties)] = handler

	def registerToClientObject(self, element):
		try:
			for (eventId, scope, cacheRequest), handler in self._automationEventHandlers.items():
				self.clientObject.AddAutomationEventHandler(eventId, element, scope, cacheRequest, handler)
			if isinstance(self.clientObject, UIAHandler.UIA.IUIAutomation5):
				for (scope, cacheRequest), handler in self._notificationEventHandlers.items():
					self.clientObject.AddNotificationEventHandler(element, scope, cacheRequest, handler)
			for (scope, cacheRequest, properties), handler in self._propertyChangedEventHandlers.items():
				self.clientObject.AddPropertyChangedEventHandler(element, scope, cacheRequest, handler, properties)
		except COMError as e:
			try:
				self.unregisterFromClientObject(element)
			except COMError:
				pass
			raise e

	def unregisterFromClientObject(self, element):
		for (eventId, scope, cacheRequest), handler in self._automationEventHandlers.items():
			self.clientObject.RemoveAutomationEventHandler(eventId, element, handler)
		if isinstance(self.clientObject, UIAHandler.UIA.IUIAutomation5):
			for handler in self._notificationEventHandlers.values():
				self.clientObject.RemoveNotificationEventHandler(element, handler)
		for handler in self._propertyChangedEventHandlers.values():
			self.clientObject.RemovePropertyChangedEventHandler(element, handler)


def _shouldUseUIAConsole(hwnd: int) -> bool:
	"""Determines whether to use UIA in the Windows Console."""
	setting = config.conf['UIA']['winConsoleImplementation']
	if setting == "UIA":
		return True
	elif setting == "legacy":
		return False
	else:
		# #7497: the UIA implementation in old conhost is incomplete, therefore we
		# should ignore it.
		# When the UIA implementation is improved, the below line will be replaced
		# with a check that _getConhostAPILevel >= FORMATTED.
		return False


@lru_cache(maxsize=10)
def _getConhostAPILevel(hwnd: int) -> WinConsoleAPILevel:
	"""
	This function determines which of several console UIA workarounds are
	needed in a given conhost instance.
	See the comments on the WinConsoleAPILevel enum for details.
	"""
	# microsoft/terminal#4495: In IMPROVED consoles,
	# IUIAutomationTextRange::getVisibleRanges returns one visible range.
	# Therefore, if exactly one range is returned, it is almost definitely an IMPROVED console.
	try:
		UIAElement = UIAHandler.handler.clientObject.ElementFromHandleBuildCache(
			hwnd, UIAHandler.handler.baseCacheRequest
		)
		textAreaCacheRequest = UIAHandler.handler.baseCacheRequest.clone()
		textAreaCacheRequest.TreeScope = UIAHandler.TreeScope_Children
		textAreaCacheRequest.treeFilter = UIAHandler.handler.clientObject.createPropertyCondition(
			UIAHandler.UIA_AutomationIdPropertyId,
			"Text Area"
		)
		textArea = UIAElement.buildUpdatedCache(
			textAreaCacheRequest
		).getCachedChildren().GetElement(0)
		UIATextPattern = textArea.GetCurrentPattern(
			UIAHandler.UIA_TextPatternId
		).QueryInterface(UIAHandler.IUIAutomationTextPattern)
		visiRanges = UIATextPattern.GetVisibleRanges()
		if visiRanges.length == 1:
			# Microsoft/terminal#2161: FORMATTED consoles expose text formatting
			# information to UIA.
			if isinstance(
				visiRanges.GetElement(0).GetAttributeValue(UIAHandler.UIA_FontNameAttributeId),
				str
			):
				return WinConsoleAPILevel.FORMATTED
			else:
				return WinConsoleAPILevel.IMPROVED
		else:
			return WinConsoleAPILevel.END_INCLUSIVE
	except (COMError, ValueError):
		log.exception()
		return WinConsoleAPILevel.END_INCLUSIVE
