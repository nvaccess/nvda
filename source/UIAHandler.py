from ctypes import *
import comtypes.client
from comtypes import *
import weakref
from comInterfaces.UIAutomationClient import *
import api
import queueHandler
import controlTypes
import NVDAObjects.UIA
import eventHandler
from logHandler import log

UIAControlTypesToNVDARoles={
	UIA_ButtonControlTypeId:controlTypes.ROLE_BUTTON,
	UIA_CalendarControlTypeId:controlTypes.ROLE_CALENDAR,
	UIA_CheckBoxControlTypeId:controlTypes.ROLE_CHECKBOX,
	UIA_ComboBoxControlTypeId:controlTypes.ROLE_COMBOBOX,
	UIA_EditControlTypeId:controlTypes.ROLE_EDITABLETEXT,
	UIA_HyperlinkControlTypeId:controlTypes.ROLE_LINK,
	UIA_ImageControlTypeId:controlTypes.ROLE_GRAPHIC,
	UIA_ListItemControlTypeId:controlTypes.ROLE_LISTITEM,
	UIA_ListControlTypeId:controlTypes.ROLE_LIST,
	UIA_MenuControlTypeId:controlTypes.ROLE_POPUPMENU,
	UIA_MenuBarControlTypeId:controlTypes.ROLE_MENUBAR,
	UIA_MenuItemControlTypeId:controlTypes.ROLE_MENUITEM,
	UIA_ProgressBarControlTypeId:controlTypes.ROLE_PROGRESSBAR,
	UIA_RadioButtonControlTypeId:controlTypes.ROLE_RADIOBUTTON,
	UIA_ScrollBarControlTypeId:controlTypes.ROLE_SCROLLBAR,
	UIA_SliderControlTypeId:controlTypes.ROLE_SLIDER,
	UIA_SpinnerControlTypeId:controlTypes.ROLE_SPINBUTTON,
	UIA_StatusBarControlTypeId:controlTypes.ROLE_STATUSBAR,
	UIA_TabControlTypeId:controlTypes.ROLE_TABCONTROL,
	UIA_TabItemControlTypeId:controlTypes.ROLE_TAB,
	UIA_TextControlTypeId:controlTypes.ROLE_STATICTEXT,
	UIA_ToolBarControlTypeId:controlTypes.ROLE_TOOLBAR,
	UIA_ToolTipControlTypeId:controlTypes.ROLE_TOOLTIP,
	UIA_TreeControlTypeId:controlTypes.ROLE_TREEVIEW,
	UIA_TreeItemControlTypeId:controlTypes.ROLE_TREEVIEWITEM,
	UIA_CustomControlTypeId:controlTypes.ROLE_UNKNOWN,
	UIA_GroupControlTypeId:controlTypes.ROLE_GROUPING,
	UIA_ThumbControlTypeId:controlTypes.ROLE_THUM,
	UIA_DataGridControlTypeId:controlTypes.ROLE_DATAGRID,
	UIA_DataItemControlTypeId:controlTypes.ROLE_DATAITEM,
	UIA_DocumentControlTypeId:controlTypes.ROLE_DOCUMENT,
	UIA_SplitButtonControlTypeId:controlTypes.ROLE_SPLITBUTTON,
	UIA_WindowControlTypeId:controlTypes.ROLE_WINDOW,
	UIA_PaneControlTypeId:controlTypes.ROLE_PANE,
	UIA_HeaderControlTypeId:controlTypes.ROLE_HEADER,
	UIA_HeaderItemControlTypeId:controlTypes.ROLE_HEADERITEM,
	UIA_TableControlTypeId:controlTypes.ROLE_TABLE,
	UIA_TitleBarControlTypeId:controlTypes.ROLE_TITLEBAR,
	UIA_SeparatorControlTypeId:controlTypes.ROLE_SEPARATOR,
}

UIAPropertyIdsToNVDAEventNames={
	UIA_NamePropertyId:"nameChange",
	UIA_ExpandCollapseExpandCollapseStatePropertyId:"stateChange",
	UIA_ToggleToggleStatePropertyId:"stateChange",
	UIA_HasKeyboardFocusPropertyId:"stateChange",
	UIA_IsKeyboardFocusablePropertyId:"stateChange",
	UIA_IsEnabledPropertyId:"stateChange",
	UIA_IsPasswordPropertyId:"stateChange",
	UIA_IsOffscreenPropertyId:"stateChange",
	UIA_ValueValuePropertyId:"valueChange",
	UIA_RangeValueValuePropertyId:"valueChange",
}

UIAEventIdsToNVDAEventNames={
	#UIA_Text_TextChangedEventId:"textChanged",
	#UIA_MenuModeStartEventId:"menuModeStart",
	#UIA_SelectionItem_ElementSelectedEventId:"stateChange",
	UIA_MenuOpenedEventId:"gainFocus",
	#UIA_SelectionItem_ElementAddedToSelectionEventId:"stateChange",
	#UIA_SelectionItem_ElementRemovedFromSelectionEventId:"stateChange",
	UIA_MenuModeEndEventId:"menuModeEnd",
	#UIA_Text_TextSelectionChangedEventId:"caret",
	#UIA_ToolTipOpenedEventId:"show",
	#UIA_MenuClosedEventId:"menuClosed",
	#UIA_AsyncContentLoadedEventId:"documentLoadComplete",
	#UIA_ToolTipClosedEventId:"hide",
}


handler=None

class UIAEventListener(COMObject):
	_com_interfaces_=[IUIAutomationEventHandler,IUIAutomationFocusChangedEventHandler,IUIAutomationPropertyChangedEventHandler,IUIAutomationStructureChangedEventHandler]

	def __init__(self,UIAHandlerInstance):
		self.UIAHandlerRef=weakref.ref(UIAHandlerInstance)
		super(UIAEventListener,self).__init__()

	def IUIAutomationEventHandler_HandleAutomationEvent(self,sender,eventID):
		if eventID==UIA_MenuModeEndEventId:
			focus=self.UIAHandlerRef().IUIAutomationInstance.GetFocusedElement()
			self.IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(focus)
			return
		NVDAEventName=UIAEventIdsToNVDAEventNames.get(eventID,None)
		if not NVDAEventName:
			return
		try:
			sender.currentNativeWindowHandle
		except COMError:
			return
		obj=NVDAObjects.UIA.UIA(UIAElement=sender)
		if not obj:
			return
		focus=api.getFocusObject()
		if obj==focus:
			obj=focus
		eventHandler.queueEvent(NVDAEventName,obj)
		queueHandler.pumpAll()

		pass

	def IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(self,sender):
		try:
			sender.currentNativeWindowHandle
		except COMError:
			return
		if not sender.currentHasKeyboardFocus:
			return
		if self.UIAHandlerRef().IUIAutomationInstance.CompareElements(sender,self.UIAHandlerRef().focusedElement):
			return
		self.UIAHandlerRef().focusedElement=sender
		obj=NVDAObjects.UIA.UIA(UIAElement=sender)
		eventHandler.queueEvent("gainFocus",obj)
		queueHandler.pumpAll()

	def IUIAutomationPropertyChangedEventHandler_HandlePropertyChangedEvent(self,sender,propertyId,newValue):
		try:
			sender.currentNativeWindowHandle
		except COMError:
			return
		try:
			NVDAEventName=UIAPropertyIdsToNVDAEventNames.get(propertyId,None)
			if NVDAEventName:
				obj=NVDAObjects.UIA.UIA(UIAElement=sender)
				focus=api.getFocusObject()
				if obj==focus:
					obj=focus
				eventHandler.queueEvent(NVDAEventName,obj)
				queueHandler.pumpAll()
		except:
			log.error("property change event",exc_info=True)

	def IUIAutomationStructureChangedEventHandler_HandleStructureChangedEvent(self,sender,changeType,runtimeID):
		pass

class UIAHandler(object):

	def __init__(self):
		self.IUIAutomationInstance=CoCreateInstance(CUIAutomation._reg_clsid_,interface=IUIAutomation,clsctx=CLSCTX_INPROC_SERVER)
		rawViewCondition=self.IUIAutomationInstance.RawViewCondition
		self.IUIAutomationTreeWalkerInstance=self.IUIAutomationInstance.CreateTreeWalker(rawViewCondition)
		self.rootUIAutomationElement=self.IUIAutomationInstance.GetRootElement()
		self.focusedElement=self.IUIAutomationInstance.GetFocusedElement()
		self.eventListener=UIAEventListener(self)

	def registerEvents(self):
		self.IUIAutomationInstance.AddFocusChangedEventHandler(None,self.eventListener)
		self.IUIAutomationInstance.AddPropertyChangedEventHandler(self.rootUIAutomationElement,TreeScope_Subtree,None,self.eventListener,UIAPropertyIdsToNVDAEventNames.keys())
		for x in UIAEventIdsToNVDAEventNames.iterkeys():  
			self.IUIAutomationInstance.addAutomationEventHandler(x,self.rootUIAutomationElement,TreeScope_Subtree,None,self.eventListener)

	def unregisterEvents(self):
		self.IUIAutomationInstance.RemoveAllEventHandlers()

def initialize():
	global handler
	handler=UIAHandler()
	focusedElement=handler.IUIAutomationInstance.getFocusedElement()
	focusObject=NVDAObjects.UIA.UIA(UIAElement=focusedElement)
	eventHandler.queueEvent("gainFocus",focusObject)
	handler.registerEvents()

def terminate():
	global handler
	handler.unregisterEvents()
	handler=None
