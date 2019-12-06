import time
import numbers
from ctypes import POINTER, c_int
from comtypes import BSTR
from comtypes.safearray import _midlSAFEARRAY as SAFEARRAY
from comtypes.automation import VARIANT
import colors
from logHandler import log
import NVDAHelper
import UIAHandler
import textInfos

_dll=NVDAHelper.getHelperLocalWin10Dll()
initialize=_dll.uiaRemote_initialize
_getTextContent=_dll.uiaRemote_getTextContent
_getTextContent.restype=SAFEARRAY(VARIANT)

def _getUIATextAttributeIDsForFormatConfig(formatConfig):
	IDs=[]
	if formatConfig["reportFontName"]:
		IDs.append(UIAHandler.UIA_FontNameAttributeId)
	if formatConfig["reportFontSize"]:
		IDs.append(UIAHandler.UIA_FontSizeAttributeId)
	if formatConfig["reportFontAttributes"]:
		IDs.extend([
			UIAHandler.UIA_FontWeightAttributeId,
			UIAHandler.UIA_IsItalicAttributeId,
			UIAHandler.UIA_UnderlineStyleAttributeId,
			UIAHandler.UIA_StrikethroughStyleAttributeId,
			UIAHandler.UIA_IsSuperscriptAttributeId,
			UIAHandler.UIA_IsSubscriptAttributeId,
		])
	if formatConfig["reportAlignment"]:
		IDs.append(UIAHandler.UIA_HorizontalTextAlignmentAttributeId)
	if formatConfig["reportColor"]:
		IDs.append(UIAHandler.UIA_BackgroundColorAttributeId)
		IDs.append(UIAHandler.UIA_ForegroundColorAttributeId)
	if formatConfig['reportLineSpacing']:
		IDs.append(UIAHandler.UIA_LineSpacingAttributeId)
	if formatConfig['reportLinks']:
		IDs.append(UIAHandler.UIA_LinkAttributeId)
	if formatConfig['reportStyle']:
		IDs.append(UIAHandler.UIA_StyleNameAttributeId)
	if formatConfig["reportHeadings"]:
		IDs.append(UIAHandler.UIA_StyleIdAttributeId)
	return IDs

def _getFormatField(attribs,formatConfig):
	formatField=textInfos.FormatField()
	if formatConfig["reportFontName"]:
		val=attribs.get(UIAHandler.UIA_FontNameAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			formatField["font-name"]=val
	if formatConfig["reportFontSize"]:
		val=attribs.get(UIAHandler.UIA_FontSizeAttributeId)
		if isinstance(val,numbers.Number):
			formatField['font-size']="%g pt"%float(val)
	if formatConfig["reportFontAttributes"]:
		val=attribs.get(UIAHandler.UIA_FontWeightAttributeId)
		if isinstance(val,int):
			formatField['bold']=(val>=700)
		val=attribs.get(UIAHandler.UIA_IsItalicAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			formatField['italic']=val
		val=attribs.get(UIAHandler.UIA_UnderlineStyleAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			formatField['underline']=bool(val)
		val=attribs.get(UIAHandler.UIA_StrikethroughStyleAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			formatField['strikethrough']=bool(val)
		textPosition=None
		val=attribs.get(UIAHandler.UIA_IsSuperscriptAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue and val:
			textPosition='super'
		else:
			val=attribs.get(UIAHandler.UIA_IsSubscriptAttributeId)
			if val!=UIAHandler.handler.reservedNotSupportedValue and val:
				textPosition="sub"
			else:
				textPosition="baseline"
		if textPosition:
			formatField['text-position']=textPosition
	if formatConfig['reportStyle']:
		val=attribs.get(UIAHandler.UIA_StyleNameAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			formatField["style"]=val
	if formatConfig["reportAlignment"]:
		val=attribs.get(UIAHandler.UIA_HorizontalTextAlignmentAttributeId)
		if val==UIAHandler.HorizontalTextAlignment_Left:
			val="left"
		elif val==UIAHandler.HorizontalTextAlignment_Centered:
			val="center"
		elif val==UIAHandler.HorizontalTextAlignment_Right:
			val="right"
		elif val==UIAHandler.HorizontalTextAlignment_Justified:
			val="justify"
		else:
			val=None
		if val:
			formatField['text-align']=val
	if formatConfig["reportColor"]:
		val=attribs.get(UIAHandler.UIA_BackgroundColorAttributeId)
		if isinstance(val,int):
			formatField['background-color']=colors.RGB.fromCOLORREF(val)
		val=attribs.get(UIAHandler.UIA_ForegroundColorAttributeId)
		if isinstance(val,int):
			formatField['color']=colors.RGB.fromCOLORREF(val)
	if formatConfig['reportLineSpacing']:
		val=attribs.get(UIAHandler.UIA_LineSpacingAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			if val:
				formatField['line-spacing']=val
	if formatConfig['reportLinks']:
		val=attribs.get(UIAHandler.UIA_LinkAttributeId)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			if val:
				formatField['link']=True
	if formatConfig["reportHeadings"]:
		styleIDValue=attribs.get(UIAHandler.UIA_StyleIdAttributeId)
		# #9842: styleIDValue can sometimes be a pointer to IUnknown.
		# In Python 3, comparing an int with a pointer raises a TypeError.
		if isinstance(styleIDValue, int) and UIAHandler.StyleId_Heading1 <= styleIDValue <= UIAHandler.StyleId_Heading9:
			formatField["heading-level"] = (styleIDValue - UIAHandler.StyleId_Heading1) + 1
	return formatField

textContentCommand_elementStart=1
textContentCommand_text=2
textContentCommand_elementEnd=3

def getTextWithFields(textRange,formatConfig):
	attribIDs=_getUIATextAttributeIDsForFormatConfig(formatConfig)
	attribIDsArray=SAFEARRAY(c_int).from_param(attribIDs)
	startTime=time.time()
	pArray=_getTextContent(textRange,attribIDsArray)
	endTime=time.time()
	log.info(f"uiaRemote_getTextContent took {endTime-startTime} seconds")
	pArray._needsfree=True
	content=pArray.unpack()
	fields=[]
	index=0
	contentCount=len(content)
	attribCount=len(attribIDs)
	while index<contentCount:
		cmd=content[index]
		if cmd==textContentCommand_text:
			endIndex=index+1+attribCount
			attribValues=content[index+1:endIndex]
			attribs={attribIDs[x]:attribValues[x] for x in range(attribCount)}
			formatField=_getFormatField(attribs,formatConfig)
			fields.append(textInfos.FieldCommand("formatChange",formatField))
			text=content[endIndex]
			if text:
				fields.append(text)
			else:
				del fields[-1]
			index=endIndex+1
			continue
		else:
			raise RuntimeError(f"unknown command {cmd}")
		index+=1
	return fields
