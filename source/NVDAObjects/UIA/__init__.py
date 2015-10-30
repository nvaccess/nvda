#NVDAObjects/UIA/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2015 NV Access Limited

from ctypes import byref
from ctypes.wintypes import POINT, RECT
from comtypes import COMError
import weakref
import UIAHandler
import globalVars
import eventHandler
import controlTypes
import config
import speech
import api
import textInfos
from logHandler import log
from NVDAObjects.window import Window
from NVDAObjects import NVDAObjectTextInfo, InvalidNVDAObject
from NVDAObjects.behaviors import ProgressBar, EditableTextWithoutAutoSelectDetection, Dialog
import braille

class UIATextInfo(textInfos.TextInfo):

	def _getFormatFieldAtRange(self,range,formatConfig):
		formatField=textInfos.FormatField()
		if formatConfig["reportFontName"]:
			try:
				fontNameValue=range.GetAttributeValue(UIAHandler.UIA_FontNameAttributeId)
			except COMError:
				fontNameValue=UIAHandler.handler.reservedNotSupportedValue
			if fontNameValue!=UIAHandler.handler.reservedNotSupportedValue:
				formatField["font-name"]=fontNameValue
		if formatConfig["reportFontSize"]:
			try:
				fontSizeValue=range.GetAttributeValue(UIAHandler.UIA_FontSizeAttributeId)
			except COMError:
				fontSizeValue=UIAHandler.handler.reservedNotSupportedValue
			if fontSizeValue!=UIAHandler.handler.reservedNotSupportedValue:
				formatField['font-size']="%g pt"%float(fontSizeValue)
		if formatConfig["reportHeadings"]:
			try:
				styleIDValue=range.GetAttributeValue(UIAHandler.UIA_StyleIdAttributeId)
			except COMError:
				styleIDValue=UIAHandler.handler.reservedNotSupportedValue
			if UIAHandler.StyleId_Heading1<=styleIDValue<=UIAHandler.StyleId_Heading9: 
				formatField["heading-level"]=(styleIDValue-UIAHandler.StyleId_Heading1)+1
		return textInfos.FieldCommand("formatChange",formatField)

	def __init__(self,obj,position,_rangeObj=None):
		super(UIATextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.clone()
		elif position in (textInfos.POSITION_CARET,textInfos.POSITION_SELECTION):
			sel=self.obj.UIATextPattern.GetSelection()
			if sel.length>0:
				self._rangeObj=sel.getElement(0).clone()
			else:
				raise NotImplementedError("UIAutomationTextRangeArray is empty")
			if position==textInfos.POSITION_CARET:
				self.collapse()
		elif isinstance(position,UIATextInfo): #bookmark
			self._rangeObj=position._rangeObj
		elif position==textInfos.POSITION_FIRST:
			self._rangeObj=self.obj.UIATextPattern.documentRange
			self.collapse()
		elif position==textInfos.POSITION_LAST:
			self._rangeObj=self.obj.UIATextPattern.documentRange
			self.collapse(True)
		elif position==textInfos.POSITION_ALL:
			self._rangeObj=self.obj.UIATextPattern.documentRange
		elif isinstance(position,UIA):
			try:
				self._rangeObj=self.obj.UIATextPattern.rangeFromChild(position.UIAElement)
			except COMError:
				raise LookupError
		elif isinstance(position,textInfos.Point):
			#rangeFromPoint causes a freeze in UIA client library!
			#p=POINT(position.x,position.y)
			#self._rangeObj=self.obj.UIATextPattern.RangeFromPoint(p)
			raise NotImplementedError
		else:
			raise ValueError("Unknown position %s"%position)

	def __eq__(self,other):
		if self is other: return True
		if self.__class__ is not other.__class__: return False
		return bool(self._rangeObj.compare(other._rangeObj))

	def _get_NVDAObjectAtStart(self):
		tempRange=self._rangeObj.clone()
		tempRange.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)
		# some implementations (Edge, Word) do not correctly  class embedded objects (graphics, checkboxes) as being the enclosing element, even when the range is completely within them. Rather, they still list the object in getChildren.
		# Thus we must check getChildren before getEnclosingElement.
		tempRange.expandToEnclosingUnit(UIAHandler.TextUnit_Character)
		children=tempRange.getChildren()
		if children.length==1:
			child=children.getElement(0)
		else:
			child=tempRange.getEnclosingElement()
		return UIA(UIAElement=child.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)) or self.obj

	def _get_bookmark(self):
		return self.copy()

	def _getControlFieldForObject(self, obj):
		role = obj.role
		field = textInfos.ControlField()
		field["role"] = obj.role
		states = obj.states
		# The user doesn't care about certain states, as they are obvious.
		states.discard(controlTypes.STATE_EDITABLE)
		states.discard(controlTypes.STATE_MULTILINE)
		states.discard(controlTypes.STATE_FOCUSED)
		field["states"] = states
		# Only include name if the object's inner text is empty.
		# could be unperformant.
		text=self.obj.makeTextInfo(obj).text
		if not text or text.isspace():
			field["name"] = obj.name
		#field["_childcount"] = obj.childCount
		field["level"] = obj.positionInfo.get("level")
		if role == controlTypes.ROLE_TABLE:
			field["table-id"] = 1 # FIXME
			try:
				field["table-rowcount"] = obj.rowCount
				field["table-columncount"] = obj.columnCount
			except NotImplementedError:
				pass
		if role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_DATAITEM,controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER,controlTypes.ROLE_HEADERITEM):
			try:
				field["table-rownumber"] = obj.rowNumber
				field["table-columnnumber"] = obj.columnNumber
				field["table-id"] = 1 # FIXME
				field['role']=controlTypes.ROLE_TABLECELL
				field['table-columnheadertext']=obj.columnHeaderText
				field['table-rowheadertext']=obj.rowHeaderText
			except NotImplementedError:
				pass
		return field

	def _iterUIARangeByUnit(self,rangeObj,unit):
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

	allowGetFormatFieldsAndTextOnDegenerateUIARanges=False #: _getFormatFieldsAndText should not return anything for degenerate ranges.
	def _getFormatFieldsAndText(self,tempRange,formatConfig):
		if not self.allowGetFormatFieldsAndTextOnDegenerateUIARanges and tempRange.compareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_End)==0:
			return
		formatField=self._getFormatFieldAtRange(tempRange,formatConfig)
		if formatConfig["reportSpellingErrors"]:
			try:
				annotationTypes=tempRange.GetAttributeValue(UIAHandler.UIA_AnnotationTypesAttributeId)
			except COMError:
				annotationTypes=UIAHandler.handler.reservedNotSupportedValue
			if annotationTypes==UIAHandler.AnnotationType_SpellingError:
				formatField.field["invalid-spelling"]=True
				yield formatField
				yield tempRange.GetText(-1)
			elif annotationTypes==UIAHandler.handler.ReservedMixedAttributeValue:
				for r in self._iterUIARangeByUnit(tempRange,UIAHandler.TextUnit_Word):
					text=r.GetText(-1)
					if not text:
						continue
					r.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,r,UIAHandler.TextPatternRangeEndpoint_Start)
					r.ExpandToEnclosingUnit(UIAHandler.TextUnit_Character)
					try:
						annotationTypes=r.GetAttributeValue(UIAHandler.UIA_AnnotationTypesAttributeId)
					except COMError:
						annotationTypes=UIAHandler.handler.reservedNotSupportedValue
					newField=textInfos.FormatField()
					newField.update(formatField.field)
					if annotationTypes==UIAHandler.AnnotationType_SpellingError:
						newField["invalid-spelling"]=True
					yield textInfos.FieldCommand("formatChange",newField)
					yield text
			else:
				yield formatField
				yield tempRange.GetText(-1)
		else:
			yield formatField
			yield tempRange.GetText(-1)

	def _getTextWithFieldsForRange(self,obj,rangeObj,formatConfig):
		#Graphics usually have no actual text, so render the name instead
		if rangeObj.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)==0 and obj!=self.obj:
			for x in obj.makeTextInfo("all").getTextWithFields(formatConfig):
				yield x
			return
		tempRange=rangeObj.clone()
		children=rangeObj.getChildren()
		for index in xrange(children.length):
			child=children.getElement(index)
			childObj=UIA(UIAElement=child.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
			#Sometimes a child range can contain the same children as its parent (causing an infinite loop)
			# Example: checkboxes, graphics, in Edge.
			if childObj==obj:
				continue
			childRange=self.obj.UIATextPattern.rangeFromChild(child)
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)<=0 or childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)>=0:
				continue
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)<0:
				childRange.moveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)
			if childRange.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)>0:
				childRange.moveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)
			tempRange.moveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,childRange,UIAHandler.TextPatternRangeEndpoint_Start)
			for f in self._getFormatFieldsAndText(tempRange,formatConfig):
				yield f
			field=self._getControlFieldForObject(childObj) if childObj else None
			if field:
				yield textInfos.FieldCommand("controlStart",field)
			for x in self._getTextWithFieldsForRange(childObj,childRange,formatConfig):
				yield x
			if field:
				yield textInfos.FieldCommand("controlEnd",None)
			tempRange.moveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,childRange,UIAHandler.TextPatternRangeEndpoint_End)
		tempRange.moveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_End)
		for f in self._getFormatFieldsAndText(tempRange,formatConfig):
			yield f

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		fields=[]
		try:
			e=self._rangeObj.getEnclosingElement().buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		except COMError:
			e=None
		fields=[]
		if e:
			obj=UIA(UIAElement=e)
			while obj and obj!=self.obj:
				field=self._getControlFieldForObject(obj)
				if field:
					field=textInfos.FieldCommand("controlStart",field)
					fields.append(field)
				obj=obj.parent
			fields.reverse()
		ancestorCount=len(fields)
		fields.extend(self._getTextWithFieldsForRange(self.obj,self._rangeObj,formatConfig))
		fields.extend(textInfos.FieldCommand("controlEnd",None) for x in xrange(ancestorCount))
		return fields

	def _get_text(self):
		return self._rangeObj.GetText(-1)

	def expand(self,unit):
		UIAUnit=UIAHandler.NVDAUnitsToUIAUnits[unit]
		self._rangeObj.ExpandToEnclosingUnit(UIAUnit)

	def move(self,unit,direction,endPoint=None):
		UIAUnit=UIAHandler.NVDAUnitsToUIAUnits[unit]
		if endPoint=="start":
			res=self._rangeObj.MoveEndpointByUnit(UIAHandler.TextPatternRangeEndpoint_Start,UIAUnit,direction)
		elif endPoint=="end":
			res=self._rangeObj.MoveEndpointByUnit(UIAHandler.TextPatternRangeEndpoint_End,UIAUnit,direction)
		else:
			res=self._rangeObj.Move(UIAUnit,direction)
		#Some Implementations of Move and moveEndpointByUnit return a positive number even if the direction is negative
		if direction<0 and res>0:
			res=0-res
		return res

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self._rangeObj)

	def collapse(self,end=False):
		if end:
			self._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_Start,self._rangeObj,UIAHandler.TextPatternRangeEndpoint_End)
		else:
			self._rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,self._rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)

	def compareEndPoints(self,other,which):
		if which.startswith('start'):
			src=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			src=UIAHandler.TextPatternRangeEndpoint_End
		if which.endswith('Start'):
			target=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			target=UIAHandler.TextPatternRangeEndpoint_End
		return self._rangeObj.CompareEndpoints(src,other._rangeObj,target)

	def setEndPoint(self,other,which):
		if which.startswith('start'):
			src=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			src=UIAHandler.TextPatternRangeEndpoint_End
		if which.endswith('Start'):
			target=UIAHandler.TextPatternRangeEndpoint_Start
		else:
			target=UIAHandler.TextPatternRangeEndpoint_End
		self._rangeObj.MoveEndpointByRange(src,other._rangeObj,target)

	def updateSelection(self):
		self._rangeObj.Select()

	updateCaret = updateSelection

class UIA(Window):

	def findOverlayClasses(self,clsList):
		if self.TextInfo==UIATextInfo:
			clsList.append(EditableTextWithoutAutoSelectDetection)

		UIAControlType=self.UIAElement.cachedControlType
		UIAClassName=self.UIAElement.cachedClassName
		if UIAClassName=="WpfTextView":
			clsList.append(WpfTextView)
		# #5136: Windows 8.x and Windows 10 uses different window class and other attributes for toast notifications.
		elif ((UIAClassName=="ToastContentHost" and UIAControlType==UIAHandler.UIA_ToolTipControlTypeId) #Windows 8.x
		or (self.windowClassName=="Windows.UI.Core.CoreWindow" and UIAControlType==UIAHandler.UIA_WindowControlTypeId and self.UIAElement.cachedAutomationId=="NormalToastView")): # Windows 10
			clsList.append(Toast)
		elif self.UIAElement.cachedFrameworkID=="InternetExplorer":
			import edge
			if UIAClassName in ("Internet Explorer_Server","WebView") and self.role==controlTypes.ROLE_PANE:
				clsList.append(edge.EdgeHTMLRootContainer)
			elif isinstance(self.parent,edge.EdgeHTMLRootContainer):
				clsList.append(edge.EdgeHTMLRoot)
			elif self.role==controlTypes.ROLE_LIST:
				clsList.append(edge.EdgeList)
			else:
				clsList.append(edge.EdgeNode)
		if UIAControlType==UIAHandler.UIA_ProgressBarControlTypeId:
			clsList.append(ProgressBar)
		if UIAClassName=="ControlPanelLink":
			clsList.append(ControlPanelLink)
		if UIAClassName=="UIColumnHeader":
			clsList.append(UIColumnHeader)
		elif UIAClassName=="UIItem":
			clsList.append(UIItem)
		elif UIAClassName=="SensitiveSlider":
			clsList.append(SensitiveSlider) 
		if UIAControlType==UIAHandler.UIA_TreeItemControlTypeId:
			clsList.append(TreeviewItem)
		elif UIAControlType==UIAHandler.UIA_ComboBoxControlTypeId:
			try:
				if not self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_IsValuePatternAvailablePropertyId):
					clsList.append(ComboBoxWithoutValuePattern)
			except COMError:
				pass
		elif UIAControlType==UIAHandler.UIA_ListItemControlTypeId:
			clsList.append(ListItem)
		if self.UIAIsWindowElement and UIAClassName in ("#32770","NUIDialog"):
			clsList.append(Dialog)

		clsList.append(UIA)

		if self.UIAIsWindowElement:
			super(UIA,self).findOverlayClasses(clsList)
			if self.UIATextPattern:
				#Since there is a UIA text pattern, there is no need to use the win32 edit support at all
				import NVDAObjects.window.edit
				for x in list(clsList):
					if issubclass(x,NVDAObjects.window.edit.Edit):
						clsList.remove(x)

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		UIAElement=None
		windowHandle=kwargs.get('windowHandle')
		if isinstance(relation,tuple):
			UIAElement=UIAHandler.handler.clientObject.ElementFromPointBuildCache(POINT(relation[0],relation[1]),UIAHandler.handler.baseCacheRequest)
		elif relation=="focus":
			try:
				UIAElement=UIAHandler.handler.clientObject.getFocusedElementBuildCache(UIAHandler.handler.baseCacheRequest)
				# This object may be in a different window, so we need to recalculate the window handle.
				kwargs['windowHandle']=None
			except COMError:
				log.debugWarning("getFocusedElement failed", exc_info=True)
		else:
			UIAElement=UIAHandler.handler.clientObject.ElementFromHandleBuildCache(windowHandle,UIAHandler.handler.baseCacheRequest)
		if not UIAElement:
			return False
		kwargs['UIAElement']=UIAElement
		return True

	def __init__(self,windowHandle=None,UIAElement=None):
		if not UIAElement:
			raise ValueError("needs a UIA element")

		self.UIAElement=UIAElement

		UIACachedWindowHandle=UIAElement.cachedNativeWindowHandle
		self.UIAIsWindowElement=bool(UIACachedWindowHandle)
		if UIACachedWindowHandle:
			windowHandle=UIACachedWindowHandle
		if not windowHandle:
			windowHandle=UIAHandler.handler.getNearestWindowHandle(UIAElement)
		if not windowHandle:
			raise InvalidNVDAObject("no windowHandle")
		super(UIA,self).__init__(windowHandle=windowHandle)

	def _isEqual(self,other):
		if not isinstance(other,UIA):
			return False
		try:
			return UIAHandler.handler.clientObject.CompareElements(self.UIAElement,other.UIAElement)
		except:
			return False

	def _get_shouldAllowUIAFocusEvent(self):
		try:
			return bool(self.UIAElement.currentHasKeyboardFocus)
		except COMError:
			return True

	def _getUIAPattern(self,ID,interface,cache=False):
		punk=self.UIAElement.GetCachedPattern(ID) if cache else self.UIAElement.GetCurrentPattern(ID) 
		if punk:
			return punk.QueryInterface(interface)

	def _get_UIAInvokePattern(self):
		self.UIAInvokePattern=self._getUIAPattern(UIAHandler.UIA_InvokePatternId,UIAHandler.IUIAutomationInvokePattern)
		return self.UIAInvokePattern

	def _get_UIATogglePattern(self):
		self.UIATogglePattern=self._getUIAPattern(UIAHandler.UIA_TogglePatternId,UIAHandler.IUIAutomationTogglePattern)
		return self.UIATogglePattern

	def _get_UIASelectionItemPattern(self):
		self.UIASelectionItemPattern=self._getUIAPattern(UIAHandler.UIA_SelectionItemPatternId,UIAHandler.IUIAutomationSelectionItemPattern)
		return self.UIASelectionItemPattern

	def _get_UIATextPattern(self):
		self.UIATextPattern=self._getUIAPattern(UIAHandler.UIA_TextPatternId,UIAHandler.IUIAutomationTextPattern,cache=True)
		return self.UIATextPattern

	def _get_UIALegacyIAccessiblePattern(self):
		self.UIALegacyIAccessiblePattern=self._getUIAPattern(UIAHandler.UIA_LegacyIAccessiblePatternId,UIAHandler.IUIAutomationLegacyIAccessiblePattern)
		return self.UIALegacyIAccessiblePattern

	def _get_TextInfo(self):
		if self.UIATextPattern: return UIATextInfo
		textInfo=super(UIA,self).TextInfo
		if textInfo is NVDAObjectTextInfo and self.UIAIsWindowElement and self.role==controlTypes.ROLE_WINDOW:
			import displayModel
			return displayModel.DisplayModelTextInfo
		return textInfo

	def setFocus(self):
		self.UIAElement.setFocus()

	def _get_devInfo(self):
		info=super(UIA,self).devInfo
		info.append("UIAElement: %r"%self.UIAElement)
		try:
			ret=self.UIAElement.currentAutomationID
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA automationID: %s"%ret)
		try:
			ret=self.UIAElement.cachedFrameworkID
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA frameworkID: %s"%ret)
		try:
			ret=str(self.UIAElement.getRuntimeID())
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA runtimeID: %s"%ret)
		try:
			ret=self.UIAElement.cachedProviderDescription
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA providerDescription: %s"%ret)
		try:
			ret=self.UIAElement.currentClassName
		except Exception as e:
			ret="Exception: %s"%e
		info.append("UIA className: %s"%ret)
		return info

	def _get_name(self):
		try:
			return self.UIAElement.currentName
		except COMError:
			return ""

	def _get_role(self):
		role=UIAHandler.UIAControlTypesToNVDARoles.get(self.UIAElement.cachedControlType,controlTypes.ROLE_UNKNOWN)
		if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_PANE,controlTypes.ROLE_WINDOW) and self.windowHandle:
			superRole=super(UIA,self).role
			if superRole!=controlTypes.ROLE_WINDOW:
				role=superRole
		return role

	def _get_description(self):
		try:
			return self.UIAElement.currentHelpText
		except COMError:
			return ""

	def _get_keyboardShortcut(self):
		try:
			return self.UIAElement.currentAccessKey
		except COMError:
			return None

	def _get_UIACachedStatesElement(self):
		statesCacheRequest=UIAHandler.handler.clientObject.createCacheRequest()
		for prop in (UIAHandler.UIA_HasKeyboardFocusPropertyId,UIAHandler.UIA_SelectionItemIsSelectedPropertyId,UIAHandler.UIA_IsDataValidForFormPropertyId,UIAHandler.UIA_IsRequiredForFormPropertyId,UIAHandler.UIA_ValueIsReadOnlyPropertyId,UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,UIAHandler.UIA_ToggleToggleStatePropertyId,UIAHandler.UIA_IsKeyboardFocusablePropertyId,UIAHandler.UIA_IsPasswordPropertyId,UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId):
			statesCacheRequest.addProperty(prop)
		return self.UIAElement.buildUpdatedCache(statesCacheRequest)

	def _get_states(self):
		states=set()
		e=self.UIACachedStatesElement
		try:
			hasKeyboardFocus=e.cachedHasKeyboardFocus
		except COMError:
			hasKeyboardFocus=False
		if hasKeyboardFocus:
			states.add(controlTypes.STATE_FOCUSED)
		if e.cachedIsKeyboardFocusable:
			states.add(controlTypes.STATE_FOCUSABLE)
		if e.cachedIsPassword:
			states.add(controlTypes.STATE_PROTECTED)
		# Don't fetch the role unless we must, but never fetch it more than once.
		role=None
		if e.getCachedPropertyValue(UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId):
			role=self.role
			states.add(controlTypes.STATE_CHECKABLE if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTABLE)
			if e.getCachedPropertyValue(UIAHandler.UIA_SelectionItemIsSelectedPropertyId):
				states.add(controlTypes.STATE_CHECKED if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTED)
		try:
			isDataValid=e.getCachedPropertyValueEx(UIAHandler.UIA_IsDataValidForFormPropertyId,True)
		except COMError:
			isDataValid=UIAHandler.handler.reservedNotSupportedValue
		if not isDataValid:
			states.add(controlTypes.STATE_INVALID_ENTRY)
		if e.getCachedPropertyValue(UIAHandler.UIA_IsRequiredForFormPropertyId):
			states.add(controlTypes.STATE_REQUIRED)
		if e.getCachedPropertyValue(UIAHandler.UIA_ValueIsReadOnlyPropertyId):
			states.add(controlTypes.STATE_READONLY)
		try:
			s=e.getCachedPropertyValueEx(UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if s==UIAHandler.ExpandCollapseState_Collapsed:
				states.add(controlTypes.STATE_COLLAPSED)
			elif s==UIAHandler.ExpandCollapseState_Expanded:
				states.add(controlTypes.STATE_EXPANDED)
		try:
			s=e.getCachedPropertyValueEx(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if not role:
				role=self.role
			if role==controlTypes.ROLE_BUTTON:
				if s==UIAHandler.ToggleState_On:
					states.add(controlTypes.STATE_PRESSED)
			else:
				states.add(controlTypes.STATE_CHECKABLE)
				if s==UIAHandler.ToggleState_On:
					states.add(controlTypes.STATE_CHECKED)
		return states

	def correctAPIForRelation(self, obj, relation=None):
		if obj and self.windowHandle != obj.windowHandle and not obj.UIAElement.cachedNativeWindowHandle:
			# The target element is not the root element for the window, so don't change API class; i.e. always use UIA.
			return obj
		return super(UIA, self).correctAPIForRelation(obj, relation)

	def _get_parent(self):
		try:
			parentElement=UIAHandler.handler.baseTreeWalker.GetParentElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			parentElement=None
		if not parentElement:
			return super(UIA,self).parent
		if not parentElement.CachedNativeWindowHandle and not self.UIAElement.CachedNativeWindowHandle:
			# Neither self or parent have a window handle themselves, so their nearest window handle will be the same.
			# Cache this on the parent if cached on self, to avoid fetching it later.
			try:
				parentElement._nearestWindowHandle=self.UIAElement._nearestWindowHandle
			except AttributeError:
				# _nearestWindowHandle may not exist on self if self was instantiated given a windowHandle.
				pass
		return self.correctAPIForRelation(UIA(UIAElement=parentElement),relation="parent")

	def _get_previous(self):
		try:
			previousElement=UIAHandler.handler.baseTreeWalker.GetPreviousSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not previousElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=previousElement))

	def _get_next(self):
		try:
			nextElement=UIAHandler.handler.baseTreeWalker.GetNextSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not nextElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=nextElement))

	def _get_firstChild(self):
		try:
			firstChildElement=UIAHandler.handler.baseTreeWalker.GetFirstChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not firstChildElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=firstChildElement))

	def _get_lastChild(self):
		try:
			lastChildElement=UIAHandler.handler.baseTreeWalker.GetLastChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("Tree walker failed", exc_info=True)
			return None
		if not lastChildElement:
			return None
		return self.correctAPIForRelation(UIA(UIAElement=lastChildElement))

	def _get_children(self):
		childrenCacheRequest=UIAHandler.handler.baseCacheRequest.clone()
		childrenCacheRequest.TreeScope=UIAHandler.TreeScope_Children
		cachedChildren=self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		children=[]
		if not cachedChildren:
			# GetCachedChildren returns null if there are no children.
			return children
		for index in xrange(cachedChildren.length):
			e=cachedChildren.getElement(index)
			windowHandle=e.cachedNativeWindowHandle or self.windowHandle
			children.append(self.correctAPIForRelation(UIA(windowHandle=windowHandle,UIAElement=e)))
		return children

	def _get_rowNumber(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridItemRowPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

	def _get_rowHeaderText(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_TableItemRowHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in xrange(val.length):
			e=val.getElement(i)
			obj=UIA(windowHandle=self.windowHandle,UIAElement=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
			if not obj: continue
			text=obj.makeTextInfo(textInfos.POSITION_ALL).text
			textList.append(text)
		return " ".join(textList)

	def _get_columnNumber(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridItemColumnPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

	def _get_columnHeaderText(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId ,True)
		if val==UIAHandler.handler.reservedNotSupportedValue:
			raise NotImplementedError
		val=val.QueryInterface(UIAHandler.IUIAutomationElementArray)
		textList=[]
		for i in xrange(val.length):
			e=val.getElement(i)
			obj=UIA(windowHandle=self.windowHandle,UIAElement=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest))
			if not obj: continue
			text=obj.makeTextInfo(textInfos.POSITION_ALL).text
			textList.append(text)
		return " ".join(textList)

	def _get_rowCount(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridRowCountPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val
		raise NotImplementedError

	def _get_columnCount(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridColumnCountPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val
		raise NotImplementedError

	def _get_table(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridItemContainingGridPropertyId ,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return UIA(UIAElement=val)
		raise NotImplementedError

	def _get_processID(self):
		return self.UIAElement.cachedProcessId

	def _get_location(self):
		try:
			r=self.UIAElement.currentBoundingRectangle
		except COMError:
			return None
		left=r.left
		top=r.top
		width=r.right-left
		height=r.bottom-top
		return left,top,width,height

	def _get_value(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_RangeValueValuePropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			minVal=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_RangeValueMinimumPropertyId,False)
			maxVal=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_RangeValueMaximumPropertyId,False)
			if minVal==maxVal:
				# There is no range.
				return "0"
			val=((val-minVal)/(maxVal-minVal))*100.0
			return "%d"%round(val,4)
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_ValueValuePropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val

	def _get_actionCount(self):
		if self.UIAInvokePattern:
			return 1
		return 0

	def getActionName(self,index=None):
		if not index:
			index=self.defaultActionIndex
		if index==0 and self.UIAInvokePattern:
			return _("invoke")
		raise NotImplementedError

	def doAction(self,index=None):
		if not index:
			index=self.defaultActionIndex
		if index==0:
			if self.UIAInvokePattern:
				self.UIAInvokePattern.Invoke()
			elif self.UIATogglePattern:
				self.UIATogglePattern.toggle()
			elif self.UIASelectionItemPattern:
				self.UIASelectionItemPattern.select()
			return
		raise NotImplementedError

	def _get_hasFocus(self):
		try:
			return self.UIAElement.currentHasKeyboardFocus
		except COMError:
			return False

	def _get_positionInfo(self):
		info=super(UIA,self).positionInfo or {}
		itemIndex=0
		try:
			itemIndex=self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_PositionInSetPropertyId)
		except COMError:
			pass
		if itemIndex>0:
			info['indexInGroup']=itemIndex
			itemCount=0
			try:
				itemCount=self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_SizeOfSetPropertyId)
			except COMError:
				pass
			if itemCount>0:
				info['similarItemsInGroup']=itemCount
		try:
			level=self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_LevelPropertyId)
		except COMError:
			level=None
		if level is not None and level>0:
			info["level"]=level
		return info

	def scrollIntoView(self):
		pass

	def _get_controllerFor(self):
		e=self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_ControllerForPropertyId)
		if UIAHandler.handler.clientObject.checkNotSupported(e):
			return None
		a=e.QueryInterface(UIAHandler.IUIAutomationElementArray)
		objList=[]
		for index in xrange(a.length):
			e=a.getElement(index)
			e=e.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
			obj=UIA(UIAElement=e)
			if obj:
				objList.append(obj)
		return objList

	def event_UIA_elementSelected(self):
		self.event_stateChange()

	def event_valueChange(self):
		if isinstance(self, EditableTextWithoutAutoSelectDetection):
			return
		return super(UIA, self).event_valueChange()

class TreeviewItem(UIA):

	def _get_value(self):
		return ""

	def _get__level(self):
		level=0
		obj=self
		while obj: 
			level+=1
			parent=obj.parent=obj.parent
			if not parent or parent==obj or parent.role!=controlTypes.ROLE_TREEVIEWITEM:
				return level
			obj=parent
		return level

	def _get_positionInfo(self):
		info=super(TreeviewItem,self).positionInfo or {}
		info['level']=self._level
		return info

class UIColumnHeader(UIA):

	def _get_description(self):
		description=super(UIColumnHeader,self).description
		try:
			itemStatus=self.UIAElement.currentItemStatus
		except COMError:
			itemStatus=""
		return " ".join([x for x in (description,itemStatus) if x and not x.isspace()])

class UIItem(UIA):
	"""UIA list items in an Items View repeate the name as the value"""

	def _get_positionInfo(self):
		info={}
		itemIndex=0
		try:
			itemIndex=self.UIAElement.getCurrentPropertyValue(UIAHandler.handler.ItemIndex_PropertyId)
		except COMError:
			pass
		if itemIndex>0:
			info['indexInGroup']=itemIndex
			try:
				e=self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_SelectionItemSelectionContainerPropertyId)
				if e: e=e.QueryInterface(UIAHandler.IUIAutomationElement)
			except COMError:
				e=None
			if e:
				try:
					itemCount=e.getCurrentPropertyValue(UIAHandler.handler.ItemCount_PropertyId)
				except COMError:
					itemCount=0
				if itemCount>0:
					info['similarItemsInGroup']=itemCount
		return info

	def _get_value(self):
		return ""

class SensitiveSlider(UIA):
	"""A slider that tends to give focus to its thumb control"""

	def event_focusEntered(self):
		self.reportFocus()

	def event_valueChange(self):
		focusParent=api.getFocusObject().parent
		if self==focusParent:
			speech.speakObjectProperties(self,value=True,reason=controlTypes.REASON_CHANGE)
		else:
			super(SensitiveSlider,self).event_valueChange()

class ControlPanelLink(UIA):

	def _get_description(self):
		desc=super(ControlPanelLink,self).description
		try:
			i=desc.find('\n')
		except:
			i=None
		if i:
			desc=desc[i+1:]
		return desc

class ComboBoxWithoutValuePattern(UIA):
	"""A combo box without the Value pattern.
	UIA combo boxes don't necessarily support the Value pattern unless they take arbitrary text values.
	However, NVDA expects combo boxes to have a value and to fire valueChange events.
	The value is obtained by retrieving the selected item's name.
	The valueChange event is fired on this object by L{ListItem.event_stateChange}.
	"""

	def _get_UIASelectionPattern(self):
		punk = self.UIAElement.GetCurrentPattern(UIAHandler.UIA_SelectionPatternId)
		if punk:
			self.UIASelectionPattern = punk.QueryInterface(UIAHandler.IUIAutomationSelectionPattern)
		else:
			self.UIASelectionPattern = None
		return self.UIASelectionPattern

	def _get_value(self):
		try:
			return self.UIASelectionPattern.GetCurrentSelection().GetElement(0).CurrentName
		except COMError:
			return None

class ListItem(UIA):

	def event_stateChange(self):
		if not self.hasFocus:
			parent = self.parent
			focus=api.getFocusObject()
			if parent and isinstance(parent, ComboBoxWithoutValuePattern) and parent==focus: 
				# This is an item in a combo box without the Value pattern.
				# This item has been selected, so notify the combo box that its value has changed.
				focus.event_valueChange()
		super(ListItem, self).event_stateChange()

class Dialog(Dialog):
	role=controlTypes.ROLE_DIALOG

class Toast(UIA):

	def event_alert(self):
		if not config.conf["presentation"]["reportHelpBalloons"]:
			return
		speech.speakObject(self,reason=controlTypes.REASON_FOCUS)
		# TODO: Don't use getBrailleTextForProperties directly.
		braille.handler.message(braille.getBrailleTextForProperties(name=self.name, role=self.role))

#WpfTextView fires name state changes once a second, plus when IUIAutomationTextRange::GetAttributeValue is called.
#This causes major lags when using this control with Braille in NVDA. (#2759) 
#For now just ignore the events.
class WpfTextView(UIA):

	def event_nameChange(self):
		return

	def event_stateChange(self):
		return

