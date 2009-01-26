import UIAHandler
import controlTypes
import textHandler
from NVDAObjects.window import Window
from NVDAObjects import NVDAObjectTextInfo

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

class UIA(Window):

	@classmethod
	def findBestClass(cls,clsList,kwargs):
		windowHandle=kwargs.get('windowHandle',None)
		UIAElement=kwargs.get('UIAElement',None)
		if windowHandle and not UIAElement:
			UIAElement=UIAHandler.handler.UIAutomationInstance.GetElementByHandle(windowHandle)
		elif UIAElement and not windowHandle:
			windowHandle=UIAElement.currentNativeWindowHandle
		else:
			raise ValueError("needs either a UIA element or window handle")
		kwargs['windowHandle']=windowHandle
		kwargs['UIAElement']=UIAElement
		clsList.append(UIA)
		if windowHandle:
			return super(UIA,cls).findBestClass(clsList,kwargs)
		else:
			return clsList,kwargs

	def __init__(self,windowHandle=None,UIAElement=None):
		if getattr(self,'_doneInit',False):
			return
		self._doneInit=True
		self.UIAElement=UIAElement
		super(UIA,self).__init__(windowHandle)
		if self.UIATextPattern:
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
			return UIAHandler.handler.IUIAutomationInstance.CompareElements(self.UIAElement,other.UIAElement)
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
		role=UIAHandler.UIAControlTypesToNVDARoles.get(self.UIAElement.currentControlType,controlTypes.ROLE_UNKNOWN)
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
		if self.UIAElement.currentIsKeyboardFocusable:
			states.add(controlTypes.STATE_FOCUSABLE)
		if self.UIAElement.currentIsPassword:
			states.add(controlTypes.STATE_PROTECTED)
		if self.UIAExpandCollapsePattern:
			s=self.UIAExpandCollapsePattern.currentExpandCollapseState
			if s==0:
				states.add(controlTypes.STATE_COLLAPSED)
			elif s==1:
				states.add(controlTypes.STATE_EXPANDED)
		if self.UIATogglePattern:
			s=self.UIATogglePattern.currentToggleState
			r=self.role
			if r in (controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX) and s:
				states.add(controlTypes.STATE_CHECKED)
			elif s:
				states.add(controlTypes.STATE_PRESSED)
		return states

	def _get_parent(self):
		try:
			parentElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetParentElement(self.UIAElement)
		except:
			parentElement=None
		if parentElement:
			return UIA(UIAElement=parentElement)

	def _get_previous(self):
		previousSiblingElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetPreviousSiblingElement(self.UIAElement)
		if previousSiblingElement:
			return UIA(UIAElement=previousSiblingElement)

	def _get_next(self):
		nextSiblingElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetNextSiblingElement(self.UIAElement)
		if nextSiblingElement:
			return UIA(UIAElement=nextSiblingElement)

	def _get_firstChild(self):
		firstChildElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetFirstChildElement(self.UIAElement)
		if firstChildElement:
			return UIA(UIAElement=firstChildElement)

	def _get_lastChild(self):
		lastChildElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetlastChildElement(self.UIAElement)
		if lastChildElement:
			return UIA(UIAElement=lastChildElement)

	def _get_processID(self):
		return self.UIAElement.currentProcessId

	def _get_location(self):
		r=self.UIAElement.currentBoundingRectangle
		left=r.left
		top=r.top
		width=r.right-left
		height=r.bottom-top
		return left,top,width,height

	def _get_value(self):
		if self.UIARangeValuePattern:
			return str(self.UIARangeValuePattern.currentValue) 
		elif self.UIAValuePattern:
			return self.UIAValuePattern.currentValue
