import time
import numbers
from ctypes import POINTER, c_int
from comtypes import BSTR
from comtypes.safearray import _midlSAFEARRAY as SAFEARRAY
from comtypes.automation import VARIANT
import colors
import aria
import languageHandler
from logHandler import log
import NVDAHelper
import controlTypes
import UIAHandler
import textInfos
import NVDAObjects.UIA

_dll=NVDAHelper.getHelperLocalWin10Dll()
initialize=_dll.uiaRemote_initialize
_getTextContent=_dll.uiaRemote_getTextContent
_getTextContent.restype=SAFEARRAY(VARIANT)

_UIAPropIDs=[
	UIAHandler.UIA_RuntimeIdPropertyId,
	UIAHandler.UIA_NamePropertyId,
	UIAHandler.UIA_LocalizedControlTypePropertyId,
	UIAHandler.UIA_ControlTypePropertyId,
	UIAHandler.UIA_AutomationIdPropertyId,
	UIAHandler.UIA_ClassNamePropertyId,
	UIAHandler.UIA_AriaPropertiesPropertyId,
	UIAHandler.UIA_LandmarkTypePropertyId,
	UIAHandler.UIA_AriaRolePropertyId,
	UIAHandler.UIA_IsTogglePatternAvailablePropertyId,
	UIAHandler.UIA_IsKeyboardFocusablePropertyId,
	UIAHandler.UIA_IsPasswordPropertyId,
	UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId,
	UIAHandler.UIA_SelectionItemIsSelectedPropertyId,
	UIAHandler.UIA_IsOffscreenPropertyId,
	UIAHandler.UIA_IsRequiredForFormPropertyId,
	UIAHandler.UIA_IsTextPatternAvailablePropertyId,
	UIAHandler.UIA_IsValuePatternAvailablePropertyId,
	UIAHandler.UIA_ValueIsReadOnlyPropertyId,
	UIAHandler.UIA_IsExpandCollapsePatternAvailablePropertyId,
	UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,
	UIAHandler.UIA_ToggleToggleStatePropertyId,
	UIAHandler.UIA_HelpTextPropertyId,
	UIAHandler.UIA_GridRowCountPropertyId,
	UIAHandler.UIA_GridColumnCountPropertyId,
	UIAHandler.UIA_GridItemRowPropertyId,
	UIAHandler.UIA_GridItemColumnPropertyId,
]

def _getControlField(props):
	field=textInfos.ControlField()
	UIARuntimeID = props[UIAHandler.UIA_RuntimeIdPropertyId]
	field['_UIARuntimeID'] = UIARuntimeID
	field['uniqueID']=UIARuntimeID
	UIAControlType = props[UIAHandler.UIA_ControlTypePropertyId]
	field['_UIAControlType'] = UIAControlType
	UIAAutomationID = props[UIAHandler.UIA_AutomationIdPropertyId]
	field['_UIAAutomationID'] = UIAAutomationID
	UIAClassName = props[UIAHandler.UIA_ClassNamePropertyId]
	field['_UIAClassName'] = UIAClassName
	UIALandmarkType = props[UIAHandler.UIA_LandmarkTypePropertyId]
	field['_UIALandmarkType'] = UIALandmarkType
	UIAAriaProperties = props[UIAHandler.UIA_AriaPropertiesPropertyId]
	field['_UIAAriaProperties'] = UIAAriaProperties
	UIAAriaRole = props[UIAHandler.UIA_AriaRolePropertyId]
	field['_UIAAriaRole'] = UIAAriaRole
	UIAIsTextPatternAvailable = props[UIAHandler.UIA_IsTextPatternAvailablePropertyId]
	field['_UIAIsTextPatternAvailable'] = UIAIsTextPatternAvailable
	role = UIAHandler.UIAControlTypesToNVDARoles.get(UIAControlType,controlTypes.ROLE_UNKNOWN)
	UIAIsTogglePatternAvailable = props[UIAHandler.UIA_IsTogglePatternAvailablePropertyId]
	if role==controlTypes.ROLE_BUTTON and UIAIsTogglePatternAvailable:
		role = controlTypes.ROLE_TOGGLEBUTTON
	field['role'] = role
	states = set()
	if props[UIAHandler.UIA_IsKeyboardFocusablePropertyId]:
		states.add(controlTypes.STATE_FOCUSABLE)
	if props[UIAHandler.UIA_IsPasswordPropertyId]:
		states.add(controlTypes.STATE_PROTECTED)
	UIAIsSelectionItemPatternAvailable = props[UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId]
	if UIAIsSelectionItemPatternAvailable:
		states.add(controlTypes.STATE_CHECKABLE if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTABLE)
	if props[UIAHandler.UIA_SelectionItemIsSelectedPropertyId]:
		states.add(controlTypes.STATE_CHECKED if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTED)
	if props[UIAHandler.UIA_IsOffscreenPropertyId]:
		states.add(controlTypes.STATE_OFFSCREEN)
	if props[UIAHandler.UIA_IsRequiredForFormPropertyId]:
		states.add(controlTypes.STATE_REQUIRED)
	if props[UIAHandler.UIA_ValueIsReadOnlyPropertyId]:
		states.add(controlTypes.STATE_READONLY)
	UIAIsExpandCollapsePatternAvailable = props[UIAHandler.UIA_IsExpandCollapsePatternAvailablePropertyId]
	if UIAIsExpandCollapsePatternAvailable:
		UIAExpandCollapseState = props[UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId]
		if UIAExpandCollapseState == UIAHandler.ExpandCollapseState_Collapsed:
			states.add(controlTypes.STATE_COLLAPSED)
		elif UIAExpandCollapseState == UIAHandler.ExpandCollapseState_Expanded:
			states.add(controlTypes.STATE_EXPANDED)
	if UIAIsTogglePatternAvailable:
		UIAToggleState = props[UIAHandler.UIA_ToggleToggleStatePropertyId]
		if role == controlTypes.ROLE_TOGGLEBUTTON:
			if UIAToggleState == UIAHandler.ToggleState_On:
				states.add(controlTypes.STATE_PRESSED)
		else:
			states.add(controlTypes.STATE_CHECKABLE)
			if UIAToggleState == UIAHandler.ToggleState_On:
				states.add(controlTypes.STATE_CHECKED)
	field['states'] = states
	nameIsContent = UIAControlType in NVDAObjects.UIA.UIATextInfo.UIAControlTypesWhereNameIsContent
	field['nameIsContent'] = nameIsContent
	if not nameIsContent:
		field['name'] = props[UIAHandler.UIA_NamePropertyId]
	field['description'] = props[UIAHandler.UIA_HelpTextPropertyId]
	if role==controlTypes.ROLE_TABLE:
		field["table-id"] = UIARuntimeID
		field["table-rowcount"] = props[UIAHandler.UIA_GridRowCountPropertyId]
		field["table-columncount"] = props[UIAHandler.UIA_GridColumnCountPropertyId]
	elif role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_DATAITEM,controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER,controlTypes.ROLE_HEADERITEM):
		field["table-rownumber"] = props[UIAHandler.UIA_GridItemRowPropertyId] + 1
		field["table-rowsspanned"] = 1
		field["table-columnnumber"] = props[UIAHandler.UIA_GridItemColumnPropertyId] + 1
		field["table-columnsspanned"] = 1
		field['role']=controlTypes.ROLE_TABLECELL
		field['table-columnheadertext'] = None
		field['table-rowheadertext'] = None
	# landmarks
	landmarkRole = None
	if UIALandmarkType:
		landmarkRole = UIAHandler.UIALandmarkTypeIdsToLandmarkNames.get(UIALandmarkType)
		if landmarkRole:
			field['landmark'] = landmarkRole
	if not landmarkRole:
		ariaRoles = field.get('_UIAAriaRole','').lower()
		# #7333: It is valid to provide multiple, space separated aria roles in HTML
		# If multiple roles or even multiple landmark roles are provided, the first one is used
		ariaRole = ariaRoles.split(" ")[0]
		if ariaRole in aria.landmarkRoles and (ariaRole != 'region' or field['name']):
			field['landmark'] = ariaRole
	field['_startOfNode']=True
	field['_endOfNode']=True
	return field

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
	if formatConfig["reportSpellingErrors"] or formatConfig["reportComments"] or formatConfig["reportRevisions"]:
		IDs.append(UIAHandler.UIA_AnnotationTypesAttributeId)
	IDs.append(UIAHandler.UIA_CultureAttributeId)
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
	annotationTypes=attribs.get(UIAHandler.UIA_AnnotationTypesAttributeId,())
	if not isinstance(annotationTypes,tuple):
		annotationTypes=()
	if formatConfig["reportSpellingErrors"]:
		if UIAHandler.AnnotationType_SpellingError in annotationTypes:
			formatField["invalid-spelling"]=True
		if UIAHandler.AnnotationType_GrammarError in annotationTypes:
			formatField["invalid-grammar"]=True
	if formatConfig["reportComments"]:
		if UIAHandler.AnnotationType_Comment in annotationTypes:
			formatField["comment"]=True
	if formatConfig["reportRevisions"]:
		if UIAHandler.AnnotationType_InsertionChange in annotationTypes:
			formatField["revision-insertion"]=True
		elif UIAHandler.AnnotationType_DeletionChange in annotationTypes:
			formatField["revision-deletion"]=True
	cultureVal=attribs.get(UIAHandler.UIA_CultureAttributeId)
	if cultureVal and isinstance(cultureVal,int):
		try:
			formatField['language']=languageHandler.windowsLCIDToLocaleName(cultureVal)
		except:
			log.debugWarning("language error",exc_info=True)
	return formatField

textContentCommand_elementStart=1
textContentCommand_text=2
textContentCommand_elementEnd=3

def getTextWithFields(rootElement,textRange,formatConfig):
	propIDs=_UIAPropIDs
	propIDsArray=SAFEARRAY(c_int).from_param(propIDs)
	propCount=len(propIDs)
	attribIDs=_getUIATextAttributeIDsForFormatConfig(formatConfig)
	attribIDsArray=SAFEARRAY(c_int).from_param(attribIDs)
	attribCount=len(attribIDs)
	startTime=time.time()
	pArray=_getTextContent(rootElement,textRange,propIDsArray,attribIDsArray)
	endTime=time.time()
	log.info(f"uiaRemote_getTextContent took {endTime-startTime} seconds")
	pArray._needsfree=True
	content=pArray.unpack()
	fields=[]
	index=0
	contentCount=len(content)
	controlStack=[]
	while index<contentCount:
		cmd=content[index]
		index+=1
		if cmd==textContentCommand_elementStart:
			endIndex=index+propCount
			propValues=content[index:endIndex]
			props={propIDs[x]:propValues[x] for x in range(propCount)}
			controlField = _getControlField(props)
			fields.append(textInfos.FieldCommand("controlStart",controlField))
			# Propagate table-id to a table's descendants
			if len(controlStack)>0 and controlField.get('table-id') is None:
				tableID=controlStack[-1].get('table-id')
				if tableID is not None:
					controlField['table-id']=tableID
			controlStack.append(controlField)
			index = endIndex
		elif cmd==textContentCommand_text:
			endIndex=index+attribCount
			attribValues=content[index:endIndex]
			attribs={attribIDs[x]:attribValues[x] for x in range(attribCount)}
			formatField=_getFormatField(attribs,formatConfig)
			fields.append(textInfos.FieldCommand("formatChange",formatField))
			text=content[endIndex]
			if text:
				fields.append(text)
			else:
				del fields[-1]
			index=endIndex+1
		elif cmd==textContentCommand_elementEnd:
			controlField=controlStack.pop()
			fields.append(textInfos.FieldCommand("controlEnd",controlField))
		else:
			raise RuntimeError(f"unknown command {cmd}")
	isEmbedded=False
	for field in reversed(fields):
		if isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd":
			isEmbedded=True
		elif isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
			field.field['embedded']=isEmbedded
			isEmbeded=False
		else:
			isEmbedded=False
	return fields
