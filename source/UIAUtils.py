#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import UIAHandler

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
		for key,values in dict.iteritems():
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

def getUIATextAttributeValueFromRange(range,attrib,ignoreMixedValues=False):
	"""
	Wraps IUIAutomationTextRange::getAttributeValue, returning UIAutomation's reservedNotSupportedValue on COMError, and raising UIAMixedAttributeError if a mixed value would be returned and ignoreMixedValues is False.
	"""
	try:
		val=range.GetAttributeValue(attrib)
	except COMError:
		return UIAHandler.handler.reservedNotSupportedValue
	if val==UIAHandler.handler.ReservedMixedAttributeValue:
		if not ignoreMixedValues:
			raise UIAMixedAttributeError
	return val

def iterUIARangeByUnit(rangeObj,unit):
	"""
	Splits a given UI Automation text range into smaller text ranges the size of the given unit and yields them.
	@param rangeObj: the UI Automation text range to split.
	@type rangeObj: L{UIAHandler.IUIAutomationTextRange}
	@param unit: a UI Automation text unit.
	@rtype: a generator that yields L{UIAHandler.IUIAutomationTextRange} objects.
	"""
	tempRange=rangeObj.clone()
	tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)
	endRange=tempRange.Clone()
	while endRange.Move(unit,1)>0:
		tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,endRange,UIAHandler.TextPatternRangeEndpoint_Start)
		pastEnd=tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)>0
		if pastEnd:
			tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)
		yield tempRange.clone()
		if pastEnd:
			return
		tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)
	# Ensure that we always reach the end of the outer range, even if the units seem to stop somewhere inside
	if tempRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)<0:
		tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)
		yield tempRange.clone()
