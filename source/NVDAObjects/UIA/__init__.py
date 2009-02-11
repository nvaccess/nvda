from ctypes.wintypes import POINT
from comtypes import COMError
import weakref
import UIAHandler
import controlTypes
import speech
import api
import textHandler
from NVDAObjects.window import Window
from NVDAObjects import NVDAObjectTextInfo, AutoSelectDetectionNVDAObject

class UIATextInfo(textHandler.TextInfo):

	NVDAUnitsToUIAUnits={
		"character":UIAHandler.TextUnit_Character,
		"word":UIAHandler.TextUnit_Word,
		"line":UIAHandler.TextUnit_Line,
		"paragraph":UIAHandler.TextUnit_Paragraph,
	}

	def __init__(self,obj,position):
		super(UIATextInfo,self).__init__(obj,position)
		if isinstance(position,UIAHandler.IUIAutomationTextRange):
			self._rangeObj=position.Clone()
		elif position==textHandler.POSITION_CARET or position==textHandler.POSITION_SELECTION:
			sel=self.obj.UIATextPattern.GetSelection()
			if sel.length>0:
				self._rangeObj=sel.getElement(0).clone()
			else:
				raise NotImplementedError("UIAutomationTextRangeArray is empty")
		else:
			self._rangeObj=self.obj.UIATextPattern.DocumentRange

	def _get_bookmark(self):
		return self.copy()

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
			res=self._rangeObj.MoveEndpointByUnit(UIAHandler.TextPatternRangeEndpoint_Start,UIAUnit,direction)
		else:
			res=self._rangeObj.Move(UIAUnit,direction)
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

class UIA(AutoSelectDetectionNVDAObject,Window):

	liveNVDAObjectTable=weakref.WeakValueDictionary()

	@classmethod
	def findBestClass(cls,clsList,kwargs):
		windowHandle=kwargs.get('windowHandle',None)
		UIAElement=kwargs.get('UIAElement',None)
		if windowHandle and not UIAElement:
			UIAElement=UIAHandler.handler.clientObject.ElementFromHandleBuildCache(windowHandle,UIAHandler.handler.baseCacheRequest)
		elif UIAElement and not windowHandle:
			windowHandle=UIAElement.cachedNativeWindowHandle
		else:
			raise ValueError("needs either a UIA element or window handle")
		kwargs['windowHandle']=windowHandle
		kwargs['UIAElement']=UIAElement
		UIAClassName=UIAElement.currentClassName
		if UIAClassName=="UIItem":
			clsList.append(UIItem)
		elif UIAClassName=="SensitiveSlider":
			clsList.append(SensitiveSlider) 
		clsList.append(UIA)
		if windowHandle:
			return super(UIA,cls).findBestClass(clsList,kwargs)
		else:
			return clsList,kwargs

	@classmethod
	def objectFromPoint(cls,x,y,oldNVDAObject=None,windowHandle=None):
		UIAElement=UIAHandler.handler.clientObject.ElementFromPointBuildCache(POINT(x,y),UIAHandler.handler.baseCacheRequest)
		return UIA(UIAElement=UIAElement)

	def __new__(cls,windowHandle=None,UIAElement=None):
		try:
			runtimeId=UIAElement.getRuntimeId()
		except COMError:
			log.debugWarning("Could not get UIA element runtime Id",exc_info=True)
			return None
		obj=cls.liveNVDAObjectTable.get(runtimeId,None)
		if not obj:
			obj=super(UIA,cls).__new__(cls)
			if not obj:
				return None
			cls.liveNVDAObjectTable[runtimeId]=obj
		return obj

	def __init__(self,windowHandle=None,UIAElement=None):
		if getattr(self,'_doneInit',False):
			return
		self._doneInit=True
		self.UIAElement=UIAElement
		super(UIA,self).__init__(windowHandle)
		if UIAElement.getCachedPropertyValue(UIAHandler.UIA_IsTextPatternAvailablePropertyId): 
			self.TextInfo=UIATextInfo
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
				("Back","backspace"),
			]]

	def _isEqual(self,other):
		if not isinstance(other,UIA):
			return False
		try:
			return UIAHandler.handler.clientObject.CompareElements(self.UIAElement,other.UIAElement)
		except:
			return False

	def _get_UIAExpandCollapsePattern(self):
		if not hasattr(self,'_UIAExpandCollapsePattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_ExpandCollapsePatternId)
			if punk:
				self._UIAExpandCollapsePattern=punk.QueryInterface(UIAHandler.IUIAutomationExpandCollapsePattern)
			else:
				self._UIAExpandCollapsePattern=None
		return self._UIAExpandCollapsePattern

	def _get_UIATogglePattern(self):
		if not hasattr(self,'_UIATogglePattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_TogglePatternId)
			if punk:
				self._UIATogglePattern=punk.QueryInterface(UIAHandler.IUIAutomationTogglePattern)
			else:
				self._UIATogglePattern=None
		return self._UIATogglePattern

	def _get_UIARangeValuePattern(self):
		if not hasattr(self,'_UIARangeValuePattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_RangeValuePatternId)
			if punk:
				self._UIARangeValuePattern=punk.QueryInterface(UIAHandler.IUIAutomationRangeValuePattern)
			else:
				self._UIARangeValuePattern=None
		return self._UIARangeValuePattern

	def _get_UIAValuePattern(self):
		if not hasattr(self,'_UIAValuePattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_ValuePatternId)
			if punk:
				self._UIAValuePattern=punk.QueryInterface(UIAHandler.IUIAutomationValuePattern)
			else:
				self._UIAValuePattern=None
		return self._UIAValuePattern

	def _get_UIATextPattern(self):
		if not hasattr(self,'_UIATextPattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_TextPatternId)
			if punk:
				self._UIATextPattern=punk.QueryInterface(UIAHandler.IUIAutomationTextPattern)
			else:
				self._UIATextPattern=None
		return self._UIATextPattern

	def _get_name(self):
		return self.UIAElement.currentName

	def _get_role(self):
		role=UIAHandler.UIAControlTypesToNVDARoles.get(self.UIAElement.cachedControlType,controlTypes.ROLE_UNKNOWN)
		if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_PANE,controlTypes.ROLE_WINDOW):
			return super(UIA,self).role
		return role


	def _get_description(self):
		return self.UIAElement.currentHelpText

	def _get_keyboardShortcut(self):
		return self.UIAElement.currentAccessKey

	def _get_states(self):
		states=set()
		if self.UIAElement.currentHasKeyboardFocus:
			states.add(controlTypes.STATE_FOCUSED)
		if self.UIAElement.cachedIsKeyboardFocusable:
			states.add(controlTypes.STATE_FOCUSABLE)
		if self.UIAElement.cachedIsPassword:
			states.add(controlTypes.STATE_PROTECTED)
		s=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_ExpandCollapseExpandCollapseStatePropertyId,True)
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			if s==UIAHandler.ExpandCollapseState_Collapsed:
				states.add(controlTypes.STATE_COLLAPSED)
			elif s==UIAHandler.ExpandCollapseState_Expanded:
				states.add(controlTypes.STATE_EXPANDED)
		s=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_ToggleToggleStatePropertyId,True)
		if s!=UIAHandler.handler.reservedNotSupportedValue:
			r=self.role
			if r in (controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX) and s==UIAHandler.ToggleState_On:
				states.add(controlTypes.STATE_CHECKED)
			elif s==UIAHandler.ToggleState_On:
				states.add(controlTypes.STATE_PRESSED)
		return states

	def _get_parent(self):
		try:
			parentElement=UIAHandler.handler.treeWalker.GetParentElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		except COMError:
			parentElement=None
		if not parentElement:
			return super(UIA,self).parent
		parentWindowHandle=parentElement.cachedNativeWindowHandle
		if parentWindowHandle and self.windowHandle and parentWindowHandle!=self.windowHandle and super(UIA,self).findBestAPIClass(windowHandle=parentWindowHandle)!=UIA:
			return Window(windowHandle=parentWindowHandle)
		return UIA(UIAElement=parentElement)

	def _get_previous(self):
		previousElement=UIAHandler.handler.treeWalker.GetPreviousSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		if not previousElement:
			return None
		previousWindowHandle=previousElement.cachedNativeWindowHandle
		if previousWindowHandle and self.windowHandle and previousWindowHandle!=self.windowHandle and super(UIA,self).findBestAPIClass(windowHandle=previousWindowHandle)!=UIA:
			return Window(windowHandle=previousWindowHandle)
		return UIA(UIAElement=previousElement)

	def _get_next(self):
		nextElement=UIAHandler.handler.treeWalker.GetNextSiblingElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		if not nextElement:
			return None
		nextWindowHandle=nextElement.cachedNativeWindowHandle
		if nextWindowHandle and self.windowHandle and nextWindowHandle!=self.windowHandle and super(UIA,self).findBestAPIClass(windowHandle=nextWindowHandle)!=UIA:
			return Window(windowHandle=nextWindowHandle)
		return UIA(UIAElement=nextElement)

	def _get_firstChild(self):
		firstChildElement=UIAHandler.handler.treeWalker.GetFirstChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		if not firstChildElement:
			return None
		firstChildWindowHandle=firstChildElement.cachedNativeWindowHandle
		if firstChildWindowHandle and self.windowHandle and firstChildWindowHandle!=self.windowHandle and super(UIA,self).findBestAPIClass(windowHandle=firstChildWindowHandle)!=UIA:
			return Window(windowHandle=firstChildWindowHandle)
		return UIA(UIAElement=firstChildElement)

	def _get_lastChild(self):
		lastChildElement=UIAHandler.handler.treeWalker.GetLastChildElementBuildCache(self.UIAElement,UIAHandler.handler.baseCacheRequest)
		if not lastChildElement:
			return None
		lastChildWindowHandle=lastChildElement.cachedNativeWindowHandle
		if lastChildWindowHandle and self.windowHandle and lastChildWindowHandle!=self.windowHandle and super(UIA,self).findBestAPIClass(windowHandle=lastChildWindowHandle)!=UIA:
			return Window(windowHandle=lastChildWindowHandle)
		return UIA(UIAElement=lastChildElement)

	def _get_processID(self):
		return self.UIAElement.cachedProcessId

	def _get_location(self):
		r=self.UIAElement.currentBoundingRectangle
		left=r.left
		top=r.top
		width=r.right-left
		height=r.bottom-top
		return left,top,width,height

	def _get_value(self):
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_RangeValueValuePropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return "%g"%val
		val=self.UIAElement.getCurrentPropertyValueEx(UIAHandler.UIA_ValueValuePropertyId,True)
		if val!=UIAHandler.handler.reservedNotSupportedValue:
			return val

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
