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
			focus=self.UIAHandlerRef().clientObject.GetFocusedElementBuildCache(self.UIAHandlerRef().baseCacheRequest)
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
		obj.UIAElement=sender
		eventHandler.queueEvent(NVDAEventName,obj)
		queueHandler.pumpAll()

	def IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(self,sender):
		try:
			sender.currentNativeWindowHandle
		except COMError:
			return
		if not sender.currentHasKeyboardFocus:
			return
		if self.UIAHandlerRef().clientObject.CompareElements(sender,self.UIAHandlerRef().focusedElement):
			return
		self.UIAHandlerRef().focusedElement=sender
		obj=NVDAObjects.UIA.UIA(UIAElement=sender)
		obj.UIAElement=sender
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
				obj.UIAElement=sender
				eventHandler.queueEvent(NVDAEventName,obj)
				queueHandler.pumpAll()
		except:
			log.error("property change event",exc_info=True)

	def IUIAutomationStructureChangedEventHandler_HandleStructureChangedEvent(self,sender,changeType,runtimeID):
		pass

class UIAHandler(object):

	def __init__(self):
		self.clientObject=CoCreateInstance(CUIAutomation._reg_clsid_,interface=IUIAutomation,clsctx=CLSCTX_INPROC_SERVER)
		self.treeWalker=self.clientObject.RawViewWalker
		r=self.clientObject.CreateCacheRequest()
		for propertyId in (UIA_ControlTypePropertyId,UIA_IsKeyboardFocusablePropertyId,UIA_IsPasswordPropertyId,UIA_NativeWindowHandlePropertyId,UIA_ProcessIdPropertyId,UIA_IsTextPatternAvailablePropertyId):
			r.addProperty(propertyId)
		self.baseCacheRequest=r
		self.reservedNotSupportedValue=self.clientObject.ReservedNotSupportedValue
		self.rootElement=self.clientObject.GetRootElementBuildCache(self.baseCacheRequest)
		self.focusedElement=self.clientObject.GetFocusedElementBuildCache(self.baseCacheRequest)
		self.eventListener=UIAEventListener(self)

	def registerEvents(self):
		self.clientObject.AddFocusChangedEventHandler(self.baseCacheRequest,self.eventListener)
		self.clientObject.AddPropertyChangedEventHandler(self.rootElement,TreeScope_Subtree,self.baseCacheRequest,self.eventListener,UIAPropertyIdsToNVDAEventNames.keys())
		for x in UIAEventIdsToNVDAEventNames.iterkeys():  
			self.clientObject.addAutomationEventHandler(x,self.rootElement,TreeScope_Subtree,self.baseCacheRequest,self.eventListener)

	def unregisterEvents(self):
		pass #self.clientObject.RemoveAllEventHandlers()

def initialize():
	global handler
	handler=UIAHandler()
	focusObject=NVDAObjects.UIA.UIA(UIAElement=handler.focusedElement)
	eventHandler.queueEvent("gainFocus",focusObject)
	handler.registerEvents()

def terminate():
	global handler
	handler.unregisterEvents()
	handler=None
