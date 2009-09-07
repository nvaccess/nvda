from ctypes import *
import comtypes.client
from comtypes import *
import weakref
import time
import api
import queueHandler
import controlTypes
import winUser
import eventHandler
from logHandler import log

try:
	comtypes.client.GetModule('UIAutomationCore.dll')
	from comtypes.gen.UIAutomationClient import *
	isUIAAvailable=True
except (WindowsError, ImportError):
	isUIAAvailable=False

badUIAWindowClassNames=[
	"SysTreeView32",
	"WuDuiListView",
	"ComboBox",
	"msctls_progress32",
	"Edit",
]


if isUIAAvailable: UIAControlTypesToNVDARoles={
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

if isUIAAvailable: UIAPropertyIdsToNVDAEventNames={
	UIA_NamePropertyId:"nameChange",
	UIA_HelpTextPropertyId:"descriptionChange",
	UIA_ExpandCollapseExpandCollapseStatePropertyId:"stateChange",
	UIA_ToggleToggleStatePropertyId:"stateChange",
	UIA_IsEnabledPropertyId:"stateChange",
	UIA_ValueValuePropertyId:"valueChange",
	UIA_RangeValueValuePropertyId:"valueChange",
}

if isUIAAvailable: UIAEventIdsToNVDAEventNames={
	UIA_Text_TextChangedEventId:"textChanged",
	UIA_SelectionItem_ElementSelectedEventId:"stateChange",
	#UIA_MenuOpenedEventId:"gainFocus",
	UIA_SelectionItem_ElementAddedToSelectionEventId:"stateChange",
	UIA_SelectionItem_ElementRemovedFromSelectionEventId:"stateChange",
	#UIA_MenuModeEndEventId:"menuModeEnd",
	UIA_Text_TextSelectionChangedEventId:"caret",
	#UIA_ToolTipOpenedEventId:"show",
	#UIA_AsyncContentLoadedEventId:"documentLoadComplete",
	#UIA_ToolTipClosedEventId:"hide",
}

if isUIAAvailable: 
	class UIAEventListener(COMObject):
		_com_interfaces_=[IUIAutomationEventHandler,IUIAutomationFocusChangedEventHandler,IUIAutomationPropertyChangedEventHandler,IUIAutomationStructureChangedEventHandler]

		def __init__(self,UIAHandlerInstance):
			self.UIAHandlerRef=weakref.ref(UIAHandlerInstance)
			super(UIAEventListener,self).__init__()

		def IUIAutomationEventHandler_HandleAutomationEvent(self,sender,eventID):
			NVDAEventName=UIAEventIdsToNVDAEventNames.get(eventID,None)
			if not NVDAEventName:
				return
			if not self.UIAHandlerRef().isNativeUIAElement(sender):
				return
			import NVDAObjects.UIA
			obj=NVDAObjects.UIA.UIA(UIAElement=sender)
			if not obj:
				return
			eventHandler.queueEvent(NVDAEventName,obj)

		def IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(self,sender):
			if not self.UIAHandlerRef().isNativeUIAElement(sender):
				return
			try:
				hasFocus=sender.currentHasKeyboardFocus
			except COMError:
				return
			if not hasFocus: 
				return
			import NVDAObjects.UIA
			if isinstance(eventHandler.lastQueuedFocusObject,NVDAObjects.UIA.UIA):
				lastFocus=eventHandler.lastQueuedFocusObject.UIAElement
				# Ignore duplicate focus events.
				# It seems that it is possible for compareElements to return True, even though the objects are different.
				# Therefore, don't ignore the event if the last focus object has lost its hasKeyboardFocus state.
				if self.UIAHandlerRef().clientObject.compareElements(sender,lastFocus) and lastFocus.currentHasKeyboardFocus:
					return
			obj=NVDAObjects.UIA.UIA(UIAElement=sender)
			eventHandler.queueEvent("gainFocus",obj)

		def IUIAutomationPropertyChangedEventHandler_HandlePropertyChangedEvent(self,sender,propertyId,newValue):
			NVDAEventName=UIAPropertyIdsToNVDAEventNames.get(propertyId,None)
			if not NVDAEventName:
				return
			if not self.UIAHandlerRef().isNativeUIAElement(sender):
				return
			import NVDAObjects.UIA
			obj=NVDAObjects.UIA.UIA(UIAElement=sender)
			if not obj:
				return
			eventHandler.queueEvent(NVDAEventName,obj)

		def IUIAutomationStructureChangedEventHandler_HandleStructureChangedEvent(self,sender,changeType,runtimeID):
			pass

class UIAHandler(object):

	def __init__(self):
		self.clientObject=CoCreateInstance(CUIAutomation._reg_clsid_,interface=IUIAutomation,clsctx=CLSCTX_INPROC_SERVER)
		self.windowTreeWalker=self.clientObject.createTreeWalker(self.clientObject.CreateNotCondition(self.clientObject.CreatePropertyCondition(UIA_NativeWindowHandlePropertyId,0)))
		self.windowCacheRequest=self.clientObject.CreateCacheRequest()
		self.windowCacheRequest.AddProperty(UIA_NativeWindowHandlePropertyId)
		self.UIAWindowHandleCache={}
		self.baseTreeWalker=self.clientObject.RawViewWalker
		self.baseCacheRequest=self.windowCacheRequest.Clone()
		for propertyId in (UIA_ClassNamePropertyId,UIA_ControlTypePropertyId,UIA_IsKeyboardFocusablePropertyId,UIA_IsPasswordPropertyId,UIA_NativeWindowHandlePropertyId,UIA_ProcessIdPropertyId,UIA_IsSelectionItemPatternAvailablePropertyId,UIA_IsTextPatternAvailablePropertyId):
			self.baseCacheRequest.addProperty(propertyId)
		self.rootElement=self.clientObject.getRootElementBuildCache(self.baseCacheRequest)
		self.reservedNotSupportedValue=self.clientObject.ReservedNotSupportedValue
		self.eventListener=UIAEventListener(self)
		self.registerEvents()

	def __del__(self):
		self.unregisterEvents()

	def isUIAWindow(self,hwnd):
		now=time.time()
		v=self.UIAWindowHandleCache.get(hwnd,None)
		if not v or (now-v[1])>0.5:
			windowClassName=winUser.getClassName(hwnd)
			if windowClassName in badUIAWindowClassNames:
				isUIA=False
			else:
				isUIA=windll.UIAutomationCore.UiaHasServerSideProvider(hwnd)
			self.UIAWindowHandleCache[hwnd]=(isUIA,now)
			return isUIA
		return v[0]

	def isNativeUIAElement(self,UIAElement):
		try:
			UIAElement=self.windowTreeWalker.NormalizeElementBuildCache(UIAElement,self.windowCacheRequest)
		except COMError:
			return False
		try:
			windowHandle=UIAElement.cachedNativeWindowHandle
		except COMError:
			return False
		return self.isUIAWindow(windowHandle)

	def registerEvents(self):
		self.clientObject.AddFocusChangedEventHandler(self.baseCacheRequest,self.eventListener)
		self.clientObject.AddPropertyChangedEventHandler(self.rootElement,TreeScope_Subtree,self.baseCacheRequest,self.eventListener,UIAPropertyIdsToNVDAEventNames.keys())
		for x in UIAEventIdsToNVDAEventNames.iterkeys():  
			self.clientObject.addAutomationEventHandler(x,self.rootElement,TreeScope_Subtree,self.baseCacheRequest,self.eventListener)

	def unregisterEvents(self):
		pass #self.clientObject.RemoveAllEventHandlers()

handler=None

def initialize():
	global handler
	if isUIAAvailable:
		handler=UIAHandler()

def terminate():
	global handler
	handler=None
