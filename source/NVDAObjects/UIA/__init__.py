import UIAHandler
import controlTypes
from NVDAObjects.window import Window

class UIA(Window):

	def __init__(self,UIAElement):
		self.UIAElement=UIAElement
		super(UIA,self).__init__(UIAElement.currentNativeWindowHandle)

	def _isEqual(self,other):
		if not isinstance(other,UIA):
			return False
		try:
			return UIAHandler.handler.IUIAutomationInstance.CompareElements(self.UIAElement,other.UIAElement)
		except:
			from logHandler import log
			log.error("ding",exc_info=True)
			return False

	def _get_UIAExpandCollapsePattern(self):
		if not hasattr(self,'_UIAExpandCollapsePattern'):
			punk=self.UIAElement.GetCurrentPattern(UIAHandler.UIA_ExpandCollapsePatternId)
			if punk:
				self._UIAExpandCollapsePattern=punk.QueryInterface(UIAHandler.IUIAutomationExpandCollapsePattern)
			else:
				self._UIAExpandCollapsePattern=None
		return self._UIAExpandCollapsePattern

	def _get_name(self):
		return self.UIAElement.currentName

	def _get_role(self):
		return UIAHandler.UIAControlTypesToNVDARoles[self.UIAElement.currentControlType]

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
		return states

	def _get_parent(self):
		try:
			parentElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetParentElement(self.UIAElement)
		except:
			parentElement=None
		if parentElement:
			return UIA(parentElement)

	def _get_previous(self):
		previousSiblingElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetPreviousSiblingElement(self.UIAElement)
		if previousSiblingElement:
			return UIA(previousSiblingElement)

	def _get_next(self):
		nextSiblingElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetNextSiblingElement(self.UIAElement)
		if nextSiblingElement:
			return UIA(nextSiblingElement)

	def _get_firstChild(self):
		firstChildElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetFirstChildElement(self.UIAElement)
		if firstChildElement:
			return UIA(firstChildElement)

	def _get_lastChild(self):
		lastChildElement=UIAHandler.handler.IUIAutomationTreeWalkerInstance.GetlastChildElement(self.UIAElement)
		if lastChildElement:
			return UIA(lastChildElement)

	def _get_windowProcessID(self):
		return self.UIAElement.currentProcessId

	def _get_location(self):
		r=self.UIAElement.currentBoundingRectangle
		left=r.left
		top=r.top
		width=r.right-left
		height=r.bottom-top
		return left,top,width,height

 