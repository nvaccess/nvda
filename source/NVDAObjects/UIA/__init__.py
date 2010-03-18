from ctypes.wintypes import POINT
from comtypes import COMError
import weakref
import UIAHandler
import globalVars
import eventHandler
import controlTypes
import speech
import api
import textInfos
from logHandler import log
from NVDAObjects.window import Window
from NVDAObjects import NVDAObjectTextInfo, AutoSelectDetectionNVDAObject
from NVDAObjects.behaviors import ProgressBar

class UIATextInfo(textInfos.TextInfo):

	NVDAUnitsToUIAUnits={
		"character":UIAHandler.TextUnit_Character,
		"word":UIAHandler.TextUnit_Word,
		"line":UIAHandler.TextUnit_Line,
		"paragraph":UIAHandler.TextUnit_Paragraph,
	}

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
		return formatField

	def __init__(self,obj,position):
		super(UIATextInfo,self).__init__(obj,position)
		if isinstance(position,UIAHandler.IUIAutomationTextRange):
			self._rangeObj=position.Clone()
		elif position==textInfos.POSITION_CARET or position==textInfos.POSITION_SELECTION:
			sel=self.obj.UIATextPattern.GetSelection()
			if sel.length>0:
				self._rangeObj=sel.getElement(0).clone()
			else:
				raise NotImplementedError("UIAutomationTextRangeArray is empty")
		else:
			self._rangeObj=self.obj.UIATextPattern.DocumentRange

	def _get_bookmark(self):
		return self.copy()

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		rangeObj=self._rangeObj.Clone()
		rangeObj.MoveEndpointByRange(UIAHandler.TextPatternRangeEndpoint_End,rangeObj,UIAHandler.TextPatternRangeEndpoint_Start)
		rangeObj.ExpandToEnclosingUnit(UIAHandler.TextUnit_Character)
		formatField=self._getFormatFieldAtRange(rangeObj,formatConfig)
		field=textInfos.FieldCommand("formatChange",formatField)
		return [field,self.text]

	def _get_text(self):
		return self._rangeObj.GetText(-1)

	def expand(self,unit):
		UIAUnit=self.NVDAUnitsToUIAUnits[unit]
		self._rangeObj.ExpandToEnclosingUnit(UIAUnit)

	def move(self,unit,direction,endPoint=None):
		UIAUnit=self.NVDAUnitsToUIAUnits[unit]
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
		return self.__class__(self.obj,self._rangeObj)

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

class UIA(AutoSelectDetectionNVDAObject,Window):

	liveNVDAObjectTable=weakref.WeakValueDictionary()

	def findOverlayClasses(self,clsList):
		UIAControlType=self.UIAElement.cachedControlType
		UIAClassName=self.UIAElement.cachedClassName
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
		clsList.append(UIA)
		if self.UIAIsWindowElement:
			return super(UIA,self).findOverlayClasses(clsList)
		else:
			return clsList

	@classmethod
	def objectFromPoint(cls,x,y,oldNVDAObject=None,windowHandle=None):
		UIAElement=UIAHandler.handler.clientObject.ElementFromPointBuildCache(POINT(x,y),UIAHandler.handler.baseCacheRequest)
		return UIA(UIAElement=UIAElement)

	@classmethod
	def objectWithFocus(cls,windowHandle=None):
		try:
			UIAElement=UIAHandler.handler.clientObject.getFocusedElementBuildCache(UIAHandler.handler.baseCacheRequest)
		except COMError:
			log.debugWarning("getFocusedElement failed", exc_info=True)
			return None
		return UIA(UIAElement=UIAElement)

	def __new__(cls,relation=None,windowHandle=None,UIAElement=None):
		try:
			runtimeId=UIAElement.getRuntimeId()
		except COMError:
			log.debugWarning("Could not get UIA element runtime Id",exc_info=True)
			runtimeId=None
		if not runtimeId:
			obj=cls.liveNVDAObjectTable.get(runtimeId,None)
		else:
			obj=None
		if not obj:
			obj=super(UIA,cls).__new__(cls)
			if not obj:
				return None
			if runtimeId:
				cls.liveNVDAObjectTable[runtimeId]=obj
		else:
			obj.UIAElement=UIAElement
		return obj

	def __init__(self,relation=None,windowHandle=None,UIAElement=None):
		self.UIAIsWindowElement=True
		if windowHandle and not UIAElement:
			UIAElement=UIAHandler.handler.clientObject.ElementFromHandleBuildCache(windowHandle,UIAHandler.handler.baseCacheRequest)
		elif UIAElement and not windowHandle:
			windowHandle=UIAElement.cachedNativeWindowHandle
			if not windowHandle:
				self.UIAIsWindowElement=False
				windowHandle=UIAHandler.handler.getNearestWindowHandle(UIAElement)
		else:
			raise ValueError("needs either a UIA element or window handle")
		self.UIAElement=UIAElement
		super(UIA,self).__init__(windowHandle=windowHandle)

		if UIAElement.getCachedPropertyValue(UIAHandler.UIA_IsTextPatternAvailablePropertyId): 
			self.TextInfo=UIATextInfo
			self.initAutoSelectDetection()
			self.value=""
			[self.bindKey_runtime(keyName,scriptName) for keyName,scriptName in [
				("ExtendedUp","moveByLine"),
				("ExtendedDown","moveByLine"),
				("control+ExtendedUp","moveByLine"),
				("control+ExtendedDown","moveByLine"),
				("ExtendedLeft","moveByCharacter"),
				("ExtendedRight","moveByCharacter"),
				("Control+ExtendedLeft","moveByWord"),
				("Control+ExtendedRight","moveByWord"),
				("ExtendedHome","moveByCharacter"),
				("ExtendedEnd","moveByCharacter"),
				("control+extendedHome","moveByLine"),
				("control+extendedEnd","moveByLine"),
				("ExtendedDelete","delete"),
				("Back","backspaceCharacter"),
				("Control+Back","backspaceWord"),
			]]

	def _isEqual(self,other):
		if not isinstance(other,UIA):
			return False
		try:
			return UIAHandler.handler.clientObject.CompareElements(self.UIAElement,other.UIAElement)
		except:
			return False

	def _get_UIAInvokePattern(self):
		if not hasattr(self,'_UIAInvokePattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_InvokePatternId)
			if punk:
				self._UIAInvokePattern=punk.QueryInterface(UIAHandler.IUIAutomationInvokePattern)
			else:
				self._UIAInvokePattern=None
		return self._UIAInvokePattern

	def _get_UIATextPattern(self):
		if not hasattr(self,'_UIATextPattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_TextPatternId)
			if punk:
				self._UIATextPattern=punk.QueryInterface(UIAHandler.IUIAutomationTextPattern)
			else:
				self._UIATextPattern=None
		return self._UIATextPattern

	def setFocus(self):
		self.UIAElement.setFocus()

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
				return superRole
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

	def _get_states(self):
		states=set()
		try:
			hasKeyboardFocus=self.UIAElement.currentHasKeyboardFocus
		except COMError:
			hasKeyboardFocus=False
		if hasKeyboardFocus:
			states.add(controlTypes.STATE_FOCUSED)
		if self.UIAElement.cachedIsKeyboardFocusable:
			states.add(controlTypes.STATE_FOCUSABLE)
		if self.UIAElement.cachedIsPassword:
			states.add(controlTypes.STATE_PROTECTED)
		# Don't fetch the role unless we must, but never fetch it more than once.
		role=None
		if self.UIAElement.getCachedPropertyValue(UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId):
			role=self.role
			states.add(controlTypes.STATE_CHECKABLE if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTABLE)
			if self.UIAElement.getCurrentPropertyValue(UIAHandler.UIA_SelectionItemIsSelectedPropertyId):
				states.add(controlTypes.STATE_CHECKED if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTED)
		try:
			s=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,True)
		except COMError:
			s=UIAHandler.handler.reservedNotSupportedValue
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if s==UIAHandler.ExpandCollapseState_Collapsed:
				states.add(controlTypes.STATE_COLLAPSED)
			elif s==UIAHandler.ExpandCollapseState_Expanded:
				states.add(controlTypes.STATE_EXPANDED)
		try:
			s=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
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

	def _get_rowNumber(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridItemRowPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

	def _get_columnNumber(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_GridItemColumnPropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val+1
		raise NotImplementedError

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
			val=((val-minVal)/maxVal)*100.0
			return "%g"%val
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
		if index==0 and self.UIAInvokePattern:
			self.UIAInvokePattern.Invoke()
			return
		raise NotImplementedError

	def event_caret(self):
		super(UIA, self).event_caret()
		if self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
			if globalVars.caretMovesReviewCursor:
				try:
					api.setReviewPosition(self.makeTextInfo(textInfos.POSITION_CARET))
				except (NotImplementedError, RuntimeError):
					pass
			self.detectPossibleSelectionChange()

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
		return {'level':self._level}

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

	def _get_value(self):
		return ""

class SensitiveSlider(UIA):
	"""A slider that tends to give focus to its thumb control"""

	def event_focusEntered(self):
		self.reportFocus()

	def event_valueChange(self):
		focusParent=api.getFocusObject().parent
		if self==focusParent:
			speech.speakObjectProperties(self,value=True,reason=speech.REASON_CHANGE)
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

