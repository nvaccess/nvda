import weakref
import controlTypes
from NVDAObjects.window import Window

class UIA(Window):

	def __init__(self,UIAHandlerInstance,UIAElement):
		self.UIAHandlerRef=weakref.ref(UIAHandlerInstance)
		self.UIAElement=UIAElement
		super(UIA,self).__init__(UIAElement.currentNativeWindowHandle)

	def _isEqual(self,other):
		if not isinstance(other,UIA):
			return False
		try:
			return self.UIAHandlerRef().IUIAutomationInstance.CompareElements(self.UIAElement,other.UIAElement)
		except:
			return False

	def _get_name(self):
		return self.UIAElement.currentName

	def _get_role(self):
		return self.UIAHandlerRef().UIAControlTypesToNVDARoles[self.UIAElement.currentControlType]

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
		return states

	def _get_parent(self):
		try:
			parentElement=self.UIAHandlerRef().IUIAutomationTreeWalkerInstance.GetParentElement(self.UIAElement)
		except:
			parentElement=None
		if parentElement:
			return UIA(self.UIAHandlerRef(),parentElement)

	def _get_previous(self):
		previousSiblingElement=self.UIAHandlerRef().IUIAutomationTreeWalkerInstance.GetPreviousSiblingElement(self.UIAElement)
		if previousSiblingElement:
			return UIA(self.UIAHandlerRef(),previousSiblingElement)

	def _get_next(self):
		nextSiblingElement=self.UIAHandlerRef().IUIAutomationTreeWalkerInstance.GetNextSiblingElement(self.UIAElement)
		if nextSiblingElement:
			return UIA(self.UIAHandlerRef(),nextSiblingElement)

	def _get_firstChild(self):
		firstChildElement=self.UIAHandlerRef().IUIAutomationTreeWalkerInstance.GetFirstChildElement(self.UIAElement)
		if firstChildElement:
			return UIA(self.UIAHandlerRef(),firstChildElement)

	def _get_lastChild(self):
		lastChildElement=self.UIAHandlerRef().IUIAutomationTreeWalkerInstance.GetlastChildElement(self.UIAElement)
		if lastChildElement:
			return UIA(self.UIAHandlerRef(),lastChildElement)

	def _get_windowProcessID(self):
		return self.UIAElement.currentProcessId
