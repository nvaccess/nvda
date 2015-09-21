from ctypes import *
from ctypes.wintypes import *
import comtypes.client
from comtypes.automation import VT_EMPTY
from comtypes import *
import weakref
import threading
import time
import api
import appModuleHandler
import queueHandler
import controlTypes
import NVDAHelper
import winKernel
import winUser
import eventHandler
from logHandler import log

from comtypes.gen.UIAutomationClient import *

#Some new win8 UIA constants that could be missing
UIA_StyleIdAttributeId=40034
UIA_AnnotationAnnotationTypeIdPropertyId=30113
UIA_AnnotationTypesAttributeId=40031
AnnotationType_SpellingError=60001
UIA_AnnotationObjectsAttributeId=40032
StyleId_Heading1=70001
StyleId_Heading9=70009
ItemIndex_Property_GUID=GUID("{92A053DA-2969-4021-BF27-514CFC2E4A69}")
ItemCount_Property_GUID=GUID("{ABBF5C45-5CCC-47b7-BB4E-87CB87BBD162}")
UIA_LevelPropertyId=30154
UIA_PositionInSetPropertyId=30152
UIA_SizeOfSetPropertyId=30153

badUIAWindowClassNames=[
	"SysTreeView32",
	"WuDuiListView",
	"ComboBox",
	"msctls_progress32",
	"Edit",
	"CommonPlacesWrapperWndClass",
	"SysMonthCal32",
	"SUPERGRID", #Outlook 2010 message list
	"RichEdit",
	"RichEdit20",
	"RICHEDIT50W",
	"SysListView32",
	"_WwG",
	'_WwN',
	"EXCEL7",
	"Button",
]

NVDAUnitsToUIAUnits={
	"character":TextUnit_Character,
	"word":TextUnit_Word,
	"line":TextUnit_Line,
	"paragraph":TextUnit_Paragraph,
	"readingChunk":TextUnit_Line,
}

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
	UIA_ThumbControlTypeId:controlTypes.ROLE_THUMB,
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
	UIA_HelpTextPropertyId:"descriptionChange",
	UIA_ExpandCollapseExpandCollapseStatePropertyId:"stateChange",
	UIA_ToggleToggleStatePropertyId:"stateChange",
	UIA_IsEnabledPropertyId:"stateChange",
	UIA_ValueValuePropertyId:"valueChange",
	UIA_RangeValueValuePropertyId:"valueChange",
}

UIAEventIdsToNVDAEventNames={
	#UIA_Text_TextChangedEventId:"textChanged",
	UIA_SelectionItem_ElementSelectedEventId:"UIA_elementSelected",
	UIA_MenuOpenedEventId:"gainFocus",
	UIA_SelectionItem_ElementAddedToSelectionEventId:"stateChange",
	UIA_SelectionItem_ElementRemovedFromSelectionEventId:"stateChange",
	#UIA_MenuModeEndEventId:"menuModeEnd",
	#UIA_Text_TextSelectionChangedEventId:"caret",
	UIA_ToolTipOpenedEventId:"alert",
	#UIA_AsyncContentLoadedEventId:"documentLoadComplete",
	#UIA_ToolTipClosedEventId:"hide",
}

class UIAHandler(COMObject):
	_com_interfaces_=[IUIAutomationEventHandler,IUIAutomationFocusChangedEventHandler,IUIAutomationPropertyChangedEventHandler]

	def __init__(self):
		super(UIAHandler,self).__init__()
		self.MTAThreadInitEvent=threading.Event()
		self.MTAThreadStopEvent=threading.Event()
		self.MTAThreadInitException=None
		self.MTAThread=threading.Thread(target=self.MTAThreadFunc)
		self.MTAThread.daemon=True
		self.MTAThread.start()
		self.MTAThreadInitEvent.wait(2)
		if self.MTAThreadInitException:
			raise self.MTAThreadInitException

	def terminate(self):
		MTAThreadHandle=HANDLE(windll.kernel32.OpenThread(winKernel.SYNCHRONIZE,False,self.MTAThread.ident))
		self.MTAThreadStopEvent.set()
		#Wait for the MTA thread to die (while still message pumping)
		if windll.user32.MsgWaitForMultipleObjects(1,byref(MTAThreadHandle),False,200,0)!=0:
			log.debugWarning("Timeout or error while waiting for UIAHandler MTA thread")
		windll.kernel32.CloseHandle(MTAThreadHandle)
		del self.MTAThread

	def MTAThreadFunc(self):
		try:
			oledll.ole32.CoInitializeEx(None,comtypes.COINIT_MULTITHREADED) 
			self.clientObject=CoCreateInstance(CUIAutomation._reg_clsid_,interface=IUIAutomation,clsctx=CLSCTX_INPROC_SERVER)
			self.windowTreeWalker=self.clientObject.createTreeWalker(self.clientObject.CreateNotCondition(self.clientObject.CreatePropertyCondition(UIA_NativeWindowHandlePropertyId,0)))
			self.windowCacheRequest=self.clientObject.CreateCacheRequest()
			self.windowCacheRequest.AddProperty(UIA_NativeWindowHandlePropertyId)
			self.UIAWindowHandleCache={}
			self.baseTreeWalker=self.clientObject.RawViewWalker
			self.baseCacheRequest=self.windowCacheRequest.Clone()
			import UIAHandler
			self.ItemIndex_PropertyId=NVDAHelper.localLib.registerUIAProperty(byref(ItemIndex_Property_GUID),u"ItemIndex",1)
			self.ItemCount_PropertyId=NVDAHelper.localLib.registerUIAProperty(byref(ItemCount_Property_GUID),u"ItemCount",1)
			for propertyId in (UIA_FrameworkIdPropertyId,UIA_AutomationIdPropertyId,UIA_ClassNamePropertyId,UIA_ControlTypePropertyId,UIA_ProviderDescriptionPropertyId,UIA_ProcessIdPropertyId,UIA_IsTextPatternAvailablePropertyId):
				self.baseCacheRequest.addProperty(propertyId)
			self.baseCacheRequest.addPattern(UIA_TextPatternId)
			self.rootElement=self.clientObject.getRootElementBuildCache(self.baseCacheRequest)
			self.reservedNotSupportedValue=self.clientObject.ReservedNotSupportedValue
			self.ReservedMixedAttributeValue=self.clientObject.ReservedMixedAttributeValue
			self.clientObject.AddFocusChangedEventHandler(self.baseCacheRequest,self)
			self.clientObject.AddPropertyChangedEventHandler(self.rootElement,TreeScope_Subtree,self.baseCacheRequest,self,UIAPropertyIdsToNVDAEventNames.keys())
			for x in UIAEventIdsToNVDAEventNames.iterkeys():  
				self.clientObject.addAutomationEventHandler(x,self.rootElement,TreeScope_Subtree,self.baseCacheRequest,self)
		except Exception as e:
			self.MTAThreadInitException=e
		finally:
			self.MTAThreadInitEvent.set()
		self.MTAThreadStopEvent.wait()
		self.clientObject.RemoveAllEventHandlers()

	def IUIAutomationEventHandler_HandleAutomationEvent(self,sender,eventID):
		if not self.MTAThreadInitEvent.isSet():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			return
		if eventID==UIA_MenuOpenedEventId and eventHandler.isPendingEvents("gainFocus"):
			# We don't need the menuOpened event if focus has been fired,
			# as focus should be more correct.
			return
		NVDAEventName=UIAEventIdsToNVDAEventNames.get(eventID,None)
		if not NVDAEventName:
			return
		if not self.isNativeUIAElement(sender):
			return
		window=self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent(NVDAEventName,windowHandle=window):
			return
		import NVDAObjects.UIA
		obj=NVDAObjects.UIA.UIA(UIAElement=sender)
		if not obj or (NVDAEventName=="gainFocus" and not obj.shouldAllowUIAFocusEvent):
			return
		focus=api.getFocusObject()
		if obj==focus:
			obj=focus
		eventHandler.queueEvent(NVDAEventName,obj)

	def IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(self,sender):
		if not self.MTAThreadInitEvent.isSet():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			return
		if not self.isNativeUIAElement(sender):
			return
		import NVDAObjects.UIA
		if isinstance(eventHandler.lastQueuedFocusObject,NVDAObjects.UIA.UIA):
			lastFocus=eventHandler.lastQueuedFocusObject.UIAElement
			# Ignore duplicate focus events.
			# It seems that it is possible for compareElements to return True, even though the objects are different.
			# Therefore, don't ignore the event if the last focus object has lost its hasKeyboardFocus state.
			if self.clientObject.compareElements(sender,lastFocus) and lastFocus.currentHasKeyboardFocus:
				return
		window=self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent("gainFocus",windowHandle=window):
			return
		obj=NVDAObjects.UIA.UIA(UIAElement=sender)
		if not obj or not obj.shouldAllowUIAFocusEvent:
			return
		eventHandler.queueEvent("gainFocus",obj)

	def IUIAutomationPropertyChangedEventHandler_HandlePropertyChangedEvent(self,sender,propertyId,newValue):
		# #3867: For now manually force this VARIANT type to empty to get around a nasty double free in comtypes/ctypes.
		# We also don't use the value in this callback.
		newValue.vt=VT_EMPTY
		if not self.MTAThreadInitEvent.isSet():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			return
		NVDAEventName=UIAPropertyIdsToNVDAEventNames.get(propertyId,None)
		if not NVDAEventName:
			return
		if not self.isNativeUIAElement(sender):
			return
		window=self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent(NVDAEventName,windowHandle=window):
			return
		import NVDAObjects.UIA
		obj=NVDAObjects.UIA.UIA(UIAElement=sender)
		if not obj:
			return
		focus=api.getFocusObject()
		if obj==focus:
			obj=focus
		eventHandler.queueEvent(NVDAEventName,obj)

	def _isUIAWindowHelper(self,hwnd):
		# UIA in NVDA's process freezes in Windows 7 and below
		processID=winUser.getWindowThreadProcessID(hwnd)[0]
		if windll.kernel32.GetCurrentProcessId()==processID:
			return False
		import NVDAObjects.window
		windowClass=NVDAObjects.window.Window.normalizeWindowClassName(winUser.getClassName(hwnd))
		# There are certain window classes that just had bad UIA implementations
		if windowClass in badUIAWindowClassNames:
			return False
		if windowClass=="NetUIHWND":
			parentHwnd=winUser.getAncestor(hwnd,winUser.GA_ROOT)
			# #2816: Outlook 2010 auto complete does not fire enough UIA events, IAccessible is better.
			# #4056: Combo boxes in Office 2010 Options dialogs don't expose a name via UIA, but do via MSAA.
			if winUser.getClassName(parentHwnd) in {"Net UI Tool Window","NUIDialog"}:
				return False
		# allow the appModule for the window to also choose if this window is bad
		appModule=appModuleHandler.getAppModuleFromProcessID(processID)
		if appModule and appModule.isBadUIAWindow(hwnd):
			return False
		# Ask the window if it supports UIA natively
		return windll.UIAutomationCore.UiaHasServerSideProvider(hwnd)

	def isUIAWindow(self,hwnd):
		now=time.time()
		v=self.UIAWindowHandleCache.get(hwnd,None)
		if not v or (now-v[1])>0.5:
			v=self._isUIAWindowHelper(hwnd),now
			self.UIAWindowHandleCache[hwnd]=v
		return v[0]

	def getNearestWindowHandle(self,UIAElement):
		if hasattr(UIAElement,"_nearestWindowHandle"):
			# Called previously. Use cached result.
			return UIAElement._nearestWindowHandle
		try:
			window=UIAElement.cachedNativeWindowHandle
		except COMError:
			window=None
		if not window:
			# This element reports no window handle, so use the nearest ancestor window handle.
			try:
				new=self.windowTreeWalker.NormalizeElementBuildCache(UIAElement,self.windowCacheRequest)
			except COMError:
				return None
			try:
				window=new.cachedNativeWindowHandle
			except COMError:
				window=None
		# Cache for future use to improve performance.
		UIAElement._nearestWindowHandle=window
		return window

	def isNativeUIAElement(self,UIAElement):
		#Due to issues dealing with UIA elements coming from the same process, we do not class these UIA elements as usable.
		#It seems to be safe enough to retreave the cached processID, but using tree walkers or fetching other properties causes a freeze.
		try:
			processID=UIAElement.cachedProcessId
		except COMError:
			return False
		if processID==windll.kernel32.GetCurrentProcessId():
			return False
		# Whether this is a native element depends on whether its window natively supports UIA.
		windowHandle=self.getNearestWindowHandle(UIAElement)
		if windowHandle:
			if self.isUIAWindow(windowHandle):
				return True
			if winUser.getClassName(windowHandle)=="DirectUIHWND" and "IEFRAME.dll" in UIAElement.cachedProviderDescription and UIAElement.currentClassName in ("DownloadBox", "accessiblebutton", "DUIToolbarButton", "PushButton"):
				# This is the IE 9 downloads list.
				# #3354: UiaHasServerSideProvider returns false for the IE 9 downloads list window,
				# so we'd normally use MSAA for this control.
				# However, its MSAA implementation is broken (fires invalid events) if UIA is initialised,
				# whereas its UIA implementation works correctly.
				# Therefore, we must use UIA here.
				return True
		return False
