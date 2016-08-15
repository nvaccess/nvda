#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 20015-2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import UIAHandler

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

class UIAMixedAttributeError(ValueError):
	pass

def getUIATextAttributeValueFromRange(range,attrib):
	try:
		val=range.GetAttributeValue(attrib)
	except COMError:
		return UIAHandler.handler.reservedNotSupportedValue
	if val==UIAHandler.handler.ReservedMixedAttributeValue:
		raise UIAMixedAttributeError
	return val

def iterUIARangeByUnit(rangeObj,unit):
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
