# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2025 NV Access Limited, Joseph Lee, Babbage B.V., Leonard de Ruijter, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Optional
import ctypes
import ctypes.wintypes
from ctypes import (
	oledll,
	windll,
	POINTER,
	CFUNCTYPE,  # noqa: F401
	c_voidp,  # noqa: F401
)

import comtypes.client
from comtypes.automation import VT_EMPTY
from comtypes import (
	COMError,
	COMObject,
	byref,
	CLSCTX_INPROC_SERVER,
	CoCreateInstance,
	IUnknown,
)

import threading
import time
import IAccessibleHandler.internalWinEventHandler
import config
from config import (
	AllowUiaInChromium,
	AllowUiaInMSWord,
)
import api
import appModuleHandler
import controlTypes
import globalVars
import winKernel
import winUser
import winVersion
import eventHandler
from logHandler import log
from . import utils
from comInterfaces import UIAutomationClient as UIA

# F403: unable to detect undefined names
from comInterfaces.UIAutomationClient import *  # noqa:  F403
import textInfos
from typing import Dict
from queue import Queue
import aria
import NVDAHelper
from . import remote as UIARemote


baseCachePropertyIDs = {
	UIA.UIA_FrameworkIdPropertyId,
	UIA.UIA_AutomationIdPropertyId,
	UIA.UIA_ClassNamePropertyId,
	UIA.UIA_ControlTypePropertyId,
	UIA.UIA_ProviderDescriptionPropertyId,
	UIA.UIA_ProcessIdPropertyId,
	UIA.UIA_IsTextPatternAvailablePropertyId,
	UIA.UIA_IsContentElementPropertyId,
	UIA.UIA_IsControlElementPropertyId,
	UIA.UIA_NamePropertyId,
	UIA.UIA_LocalizedControlTypePropertyId,
}

#: The window class name for Microsoft Word documents.
# Microsoft Word's UI Automation implementation
# also exposes this value as the document UIA element's classname property.
MS_WORD_DOCUMENT_WINDOW_CLASS = "_WwG"

HorizontalTextAlignment_Left = 0
HorizontalTextAlignment_Centered = 1
HorizontalTextAlignment_Right = 2
HorizontalTextAlignment_Justified = 3


# The name of the WDAG (Windows Defender Application Guard) process
WDAG_PROCESS_NAME = "hvsirdpclient"
# The window class of the WDAG (Windows Defender Application Guard) main window
WDAG_WINDOW_CLASS_NAME = "RAIL_WINDOW"

goodUIAWindowClassNames = (
	# A WDAG (Windows Defender Application Guard) Window is always native UIA, even if it doesn't report as such.
	"RAIL_WINDOW",
	# #17407, #17771: WinUI 3 top-level pane window class name.
	"Microsoft.UI.Content.DesktopChildSiteBridge",
)

badUIAWindowClassNames = (
	# UIA events of candidate window interfere with MSAA events.
	"Microsoft.IME.CandidateWindow.View",
	"SysTreeView32",
	"WuDuiListView",
	"ComboBox",
	"msctls_progress32",
	"Edit",
	"CommonPlacesWrapperWndClass",
	"SysMonthCal32",
	"SUPERGRID",  # Outlook 2010 message list
	"RichEdit",
	"RichEdit20",
	"RICHEDIT50W",
	"Button",
	# #8944: The Foxit UIA implementation is incomplete and should not be used for now.
	"FoxitDocWnd",
	# Mozilla Gecko (Firefox, etc.) has a native UIA implementation. However, IA2
	# is still better for web content in screen readers for now.
	"MozillaWindowClass",
	"MozillaDropShadowWindowClass",
	"MozillaDialogClass",
	"MozillaContentWindowClass",
)

# #8405: used to detect UIA dialogs prior to Windows 10 RS5.
UIADialogClassNames = [
	"#32770",
	"NUIDialog",
	"Credential Dialog Xaml Host",  # UAC dialog in Anniversary Update and later
	"Shell_Dialog",
	"Shell_Flyout",
	"Shell_SystemDialog",  # Various dialogs in Windows 10 Settings app
]

textChangeUIAAutomationIDs = (
	"Text Area",  # Windows Console Host
)

textChangeUIAClassNames = (
	"_WwG",  # Microsoft Word
)

windowsTerminalUIAClassNames = (
	"TermControl",
	"WPFTermControl",
)

NVDAUnitsToUIAUnits: Dict[str, int] = {
	textInfos.UNIT_CHARACTER: UIA.TextUnit_Character,
	textInfos.UNIT_WORD: UIA.TextUnit_Word,
	textInfos.UNIT_LINE: UIA.TextUnit_Line,
	textInfos.UNIT_PARAGRAPH: UIA.TextUnit_Paragraph,
	textInfos.UNIT_PAGE: UIA.TextUnit_Page,
	textInfos.UNIT_READINGCHUNK: UIA.TextUnit_Line,
	textInfos.UNIT_STORY: UIA.TextUnit_Document,
	textInfos.UNIT_FORMATFIELD: UIA.TextUnit_Format,
}

UIAControlTypesToNVDARoles = {
	UIA_ButtonControlTypeId: controlTypes.Role.BUTTON,  # noqa: F405
	UIA_CalendarControlTypeId: controlTypes.Role.CALENDAR,  # noqa: F405
	UIA_CheckBoxControlTypeId: controlTypes.Role.CHECKBOX,  # noqa: F405
	UIA_ComboBoxControlTypeId: controlTypes.Role.COMBOBOX,  # noqa: F405
	UIA_EditControlTypeId: controlTypes.Role.EDITABLETEXT,  # noqa: F405
	UIA_HyperlinkControlTypeId: controlTypes.Role.LINK,  # noqa: F405
	UIA_ImageControlTypeId: controlTypes.Role.GRAPHIC,  # noqa: F405
	UIA_ListItemControlTypeId: controlTypes.Role.LISTITEM,  # noqa: F405
	UIA_ListControlTypeId: controlTypes.Role.LIST,  # noqa: F405
	UIA_MenuControlTypeId: controlTypes.Role.POPUPMENU,  # noqa: F405
	UIA_MenuBarControlTypeId: controlTypes.Role.MENUBAR,  # noqa: F405
	UIA_MenuItemControlTypeId: controlTypes.Role.MENUITEM,  # noqa: F405
	UIA_ProgressBarControlTypeId: controlTypes.Role.PROGRESSBAR,  # noqa: F405
	UIA_RadioButtonControlTypeId: controlTypes.Role.RADIOBUTTON,  # noqa: F405
	UIA_ScrollBarControlTypeId: controlTypes.Role.SCROLLBAR,  # noqa: F405
	UIA_SliderControlTypeId: controlTypes.Role.SLIDER,  # noqa: F405
	UIA_SpinnerControlTypeId: controlTypes.Role.SPINBUTTON,  # noqa: F405
	UIA_StatusBarControlTypeId: controlTypes.Role.STATUSBAR,  # noqa: F405
	UIA_TabControlTypeId: controlTypes.Role.TABCONTROL,  # noqa: F405
	UIA_TabItemControlTypeId: controlTypes.Role.TAB,  # noqa: F405
	UIA_TextControlTypeId: controlTypes.Role.STATICTEXT,  # noqa: F405
	UIA_ToolBarControlTypeId: controlTypes.Role.TOOLBAR,  # noqa: F405
	UIA_ToolTipControlTypeId: controlTypes.Role.TOOLTIP,  # noqa: F405
	UIA_TreeControlTypeId: controlTypes.Role.TREEVIEW,  # noqa: F405
	UIA_TreeItemControlTypeId: controlTypes.Role.TREEVIEWITEM,  # noqa: F405
	UIA_CustomControlTypeId: controlTypes.Role.UNKNOWN,  # noqa: F405
	UIA_GroupControlTypeId: controlTypes.Role.GROUPING,  # noqa: F405
	UIA_ThumbControlTypeId: controlTypes.Role.THUMB,  # noqa: F405
	UIA_DataGridControlTypeId: controlTypes.Role.DATAGRID,  # noqa: F405
	UIA_DataItemControlTypeId: controlTypes.Role.DATAITEM,  # noqa: F405
	UIA_DocumentControlTypeId: controlTypes.Role.DOCUMENT,  # noqa: F405
	UIA_SplitButtonControlTypeId: controlTypes.Role.SPLITBUTTON,  # noqa: F405
	UIA_WindowControlTypeId: controlTypes.Role.WINDOW,  # noqa: F405
	UIA_PaneControlTypeId: controlTypes.Role.PANE,  # noqa: F405
	UIA_HeaderControlTypeId: controlTypes.Role.HEADER,  # noqa: F405
	UIA_HeaderItemControlTypeId: controlTypes.Role.HEADERITEM,  # noqa: F405
	UIA_TableControlTypeId: controlTypes.Role.TABLE,  # noqa: F405
	UIA_TitleBarControlTypeId: controlTypes.Role.TITLEBAR,  # noqa: F405
	UIA_SeparatorControlTypeId: controlTypes.Role.SEPARATOR,  # noqa: F405
}

UIALiveSettingtoNVDAAriaLivePoliteness: Dict[str, aria.AriaLivePoliteness] = {
	UIA.Off: aria.AriaLivePoliteness.OFF,
	UIA.Polite: aria.AriaLivePoliteness.POLITE,
	UIA.Assertive: aria.AriaLivePoliteness.ASSERTIVE,
}

UIAPropertyIdsToNVDAEventNames = {
	UIA.UIA_NamePropertyId: "nameChange",
	UIA.UIA_HelpTextPropertyId: "descriptionChange",
	UIA.UIA_ExpandCollapseExpandCollapseStatePropertyId: "stateChange",
	UIA.UIA_ToggleToggleStatePropertyId: "stateChange",
	UIA.UIA_IsEnabledPropertyId: "stateChange",
	UIA.UIA_ValueValuePropertyId: "valueChange",
	UIA.UIA_RangeValueValuePropertyId: "valueChange",
	UIA.UIA_ControllerForPropertyId: "UIA_controllerFor",
	UIA.UIA_ItemStatusPropertyId: "UIA_itemStatus",
	UIA.UIA_DragDropEffectPropertyId: "UIA_dragDropEffect",
	UIA.UIA_DropTargetDropTargetEffectPropertyId: "UIA_dropTargetEffect",
}

globalEventHandlerGroupUIAPropertyIds = {
	UIA.UIA_RangeValueValuePropertyId,
	UIA.UIA_DragDropEffectPropertyId,
	UIA.UIA_DropTargetDropTargetEffectPropertyId,
}

localEventHandlerGroupUIAPropertyIds = (
	set(UIAPropertyIdsToNVDAEventNames) - globalEventHandlerGroupUIAPropertyIds
)

UIALandmarkTypeIdsToLandmarkNames: Dict[int, str] = {
	UIA.UIA_FormLandmarkTypeId: "form",
	UIA.UIA_NavigationLandmarkTypeId: "navigation",
	UIA.UIA_MainLandmarkTypeId: "main",
	UIA.UIA_SearchLandmarkTypeId: "search",
}

UIAEventIdsToNVDAEventNames: Dict[int, str] = {
	UIA.UIA_LiveRegionChangedEventId: "liveRegionChange",
	UIA.UIA_SelectionItem_ElementSelectedEventId: "UIA_elementSelected",
	UIA.UIA_MenuOpenedEventId: "gainFocus",
	UIA.UIA_SelectionItem_ElementAddedToSelectionEventId: "stateChange",
	UIA.UIA_SelectionItem_ElementRemovedFromSelectionEventId: "stateChange",
	# UIA_MenuModeEndEventId:"menuModeEnd",
	UIA.UIA_ToolTipOpenedEventId: "UIA_toolTipOpened",
	# UIA_AsyncContentLoadedEventId:"documentLoadComplete",
	# UIA_ToolTipClosedEventId:"hide",
	UIA.UIA_Window_WindowOpenedEventId: "UIA_window_windowOpen",
	UIA.UIA_SystemAlertEventId: "UIA_systemAlert",
	UIA.UIA_LayoutInvalidatedEventId: "UIA_layoutInvalidated",
	UIA.UIA_Drag_DragStartEventId: "stateChange",
	UIA.UIA_Drag_DragCancelEventId: "stateChange",
	UIA.UIA_Drag_DragCompleteEventId: "stateChange",
}

localEventHandlerGroupUIAEventIds = set()

autoSelectDetectionAvailable = False
if winVersion.getWinVer() >= winVersion.WIN10:
	UIAEventIdsToNVDAEventNames.update(
		{
			UIA.UIA_Text_TextSelectionChangedEventId: "caret",
		},
	)
	localEventHandlerGroupUIAEventIds.update(
		{
			UIA.UIA_Text_TextSelectionChangedEventId,
		},
	)
	autoSelectDetectionAvailable = True

globalEventHandlerGroupUIAEventIds = set(UIAEventIdsToNVDAEventNames) - localEventHandlerGroupUIAEventIds

ignoreWinEventsMap = {
	UIA_AutomationPropertyChangedEventId: list(UIAPropertyIdsToNVDAEventNames.keys()),  # noqa: F405
}
for id in UIAEventIdsToNVDAEventNames.keys():
	ignoreWinEventsMap[id] = [0]


def shouldUseUIAInMSWord(appModule: appModuleHandler.AppModule) -> bool:
	allow = AllowUiaInMSWord.getConfig()
	if allow == AllowUiaInMSWord.ALWAYS:
		log.debug("User has requested UIA in MS Word always")
		return True
	canUseOlderInProcessApproach = bool(appModule.helperLocalBindingHandle)
	if not canUseOlderInProcessApproach:
		log.debug("Using UIA in MS Word as no alternative object model available")
		return True
	if winVersion.getWinVer() < winVersion.WIN11:
		log.debug("Not using UIA in MS Word on pre Windows 11 OS due to missing custom extensions")
		return False
	if allow != AllowUiaInMSWord.WHERE_SUITABLE:
		log.debug("User does not want UIA in MS Word unless necessary")
		return False
	isOfficeApp = appModule.productName.startswith(("Microsoft Office", "Microsoft Outlook"))
	if not isOfficeApp:
		log.debug(f"Unknown Office app: {appModule.productName}")
		return False
	try:
		officeVersion = tuple(int(x) for x in appModule.productVersion.split(".")[:3])
	except Exception:
		log.debugWarning(f"Unable to parse office version: {appModule.productVersion}", exc_info=True)
		return False
	if officeVersion < (16, 0, 15000):
		log.debug(f"MS word too old for suitable UIA, Office version: {officeVersion}")
		return False
	log.debug(f"Using UIA due to suitable Office version: {officeVersion}")
	return True


class UIAHandler(COMObject):
	_com_interfaces_ = [
		UIA.IUIAutomationEventHandler,
		UIA.IUIAutomationFocusChangedEventHandler,
		UIA.IUIAutomationPropertyChangedEventHandler,
		UIA.IUIAutomationNotificationEventHandler,
		UIA.IUIAutomationActiveTextPositionChangedEventHandler,
	]
	_rateLimitedEventHandler: IUnknown | None = None

	#: A cache of UIA notification kinds to friendly names for logging
	_notificationKindsToNamesCache = {
		v: k[len("NotificationKind_") :] for k, v in vars(UIA).items() if k.startswith("NotificationKind_")
	}

	def getUIANotificationKindDebugString(self, notificationKind: int) -> str:
		"""
		Generates a string representation of the given UIA notification kind,
		suitable for logging.
		This is the name part of the NotificationKind_* constant.
		If a matching constant can not be found,
		then a string representation of the NotificationKind value itself is used.
		E.g. "unknown notification kind 1234".
		"""
		name = self._notificationKindsToNamesCache.get(notificationKind)
		if not name:
			name = f"unknown notification kind {notificationKind}"
		return name

	#: A cache of UIA notification processing values  to friendly names for logging
	_notificationProcessingValuesToNamesCache = {
		v: k[len("NotificationProcessing_") :]
		for k, v in vars(UIA).items()
		if k.startswith("NotificationProcessing_")
	}

	def getUIANotificationProcessingValueDebugString(self, notificationProcessing: int) -> str:
		"""
		Generates a string representation of the given UIA notification processing value,
		suitable for logging.
		This is the name part of the NotificationProcessing_* constant.
		If a matching constant can not be found,
		then a string representation of the NotificationProcessing value itself is used.
		E.g. "unknown notification processing value 1234".
		"""
		name = self._notificationProcessingValuesToNamesCache.get(notificationProcessing)
		if not name:
			name = f"unknown notification processing value {notificationProcessing}"
		return name

	def getUIAPropertyIDDebugString(self, propertyID: int) -> str:
		"""
		Generates a string representation of the given property ID,
		suitable for logging.
		For constant or registered property IDs,
		the name is the programmatic name registered for the property in UIA.
		If no name can be found, then a string representation of the ID itself is used.
		E.g. "unknown property ID 1234".
		"""
		try:
			name = self.clientObject.GetPropertyProgrammaticName(propertyID)
		except COMError:
			name = None
		if not name:
			name = f"unknown property ID {propertyID}"
		return name

	#: A cache of UIA event IDs to friendly names for logging
	_eventIDsToNamesCache = {
		v: k[len("UIA_") : -len("EventId")] for k, v in vars(UIA).items() if k.endswith("EventId")
	}

	def getUIAEventIDDebugString(self, eventID: int) -> str:
		"""
		Generates a string representation of the given UIA event ID,
		suitable for logging.
		This is the name part of the UIA_*EventId constant.
		If a matching constant can not be found, then a string representation of the ID itself is used.
		E.g. "unknown event ID 1234".
		"""
		name = self._eventIDsToNamesCache.get(eventID)
		if not name:
			name = f"unknown event ID {eventID}"
		return name

	def getUIAElementPropertyDebugString(self, element: UIA.IUIAutomationElement, propertyId: int) -> str:
		"""
		Fetches a property from a UIA element,
		for the specific purpose of logging.
		NULL value and exceptions are also given a string representation.
		"""
		try:
			return element.GetCachedPropertyValue(propertyId) or "[None]"
		except COMError:
			return "[COMError exception]"

	def getWindowHandleDebugString(self, windowHandle: int) -> str:
		"""
		Generates a string representation of the given window handle
		suitable for logging.
		Includes the handle value and the window's class name.
		"""
		windowClassName = winUser.getClassName(windowHandle) or "[unknown]"
		return f"hwnd 0X{windowHandle:X} of class {windowClassName}"

	def getUIAElementDebugString(self, element: UIA.IUIAutomationElement) -> str:
		"""
		Generates a string representation of the given UIA element
		suitable for logging.
		Including info such as name, controlType and automation Id.
		"""
		name = self.getUIAElementPropertyDebugString(element, UIA.UIA_NamePropertyId)
		controlType = self.getUIAElementPropertyDebugString(element, UIA.UIA_LocalizedControlTypePropertyId)
		automationID = self.getUIAElementPropertyDebugString(element, UIA.UIA_AutomationIdPropertyId)
		className = self.getUIAElementPropertyDebugString(element, UIA.UIA_ClassNamePropertyId)
		frameworkID = self.getUIAElementPropertyDebugString(element, UIA.UIA_FrameworkIdPropertyId)
		return (
			f"{name} {controlType} "
			f"with automationID {automationID}, "
			f"className {className} "
			f"and frameworkID {frameworkID}"
		)

	def __init__(self):
		super(UIAHandler, self).__init__()
		self.globalEventHandlerGroup = None
		self.localEventHandlerGroup = None
		self.localEventHandlerGroupWithTextChanges = None
		self._localEventHandlerGroupElements = set()
		self.MTAThreadInitEvent = threading.Event()
		self.MTAThreadQueue = Queue()
		self.MTAThreadInitException = None
		self.MTAThread = threading.Thread(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}.MTAThread",
			target=self.MTAThreadFunc,
			daemon=True,
		)
		self.MTAThread.start()
		self.MTAThreadInitEvent.wait(2)
		if self.MTAThreadInitException:
			raise self.MTAThreadInitException

	def terminate(self):
		# Terminate the rate limited event handler if it exists.
		# We must do this from the main thread to totally ensure that the thread is terminated,
		# As this is a c++ thread so Python cannot kill it off at process exit.
		if config.conf["UIA"]["enhancedEventProcessing"]:
			if self._rateLimitedEventHandler:
				log.debug("UIAHandler: Terminating enhanced event processing")
				NVDAHelper.localLib.rateLimitedUIAEventHandler_terminate(self._rateLimitedEventHandler)

		# Terminate the MTA thread
		MTAThreadHandle = ctypes.wintypes.HANDLE(
			windll.kernel32.OpenThread(
				winKernel.SYNCHRONIZE,
				False,
				self.MTAThread.ident,
			),
		)
		self.MTAThreadQueue.put_nowait(None)
		# Wait for the MTA thread to die (while still message pumping)
		if windll.user32.MsgWaitForMultipleObjects(1, byref(MTAThreadHandle), False, 200, 0) != 0:
			log.debugWarning("Timeout or error while waiting for UIAHandler MTA thread")
		windll.kernel32.CloseHandle(MTAThreadHandle)
		del self.MTAThread

	def MTAThreadFunc(self):
		try:
			oledll.ole32.CoInitializeEx(None, comtypes.COINIT_MULTITHREADED)
			self.clientObject = CoCreateInstance(
				UIA.CUIAutomation8._reg_clsid_,
				# Minimum interface is IUIAutomation3 (Windows 8.1).
				interface=UIA.CUIAutomation8._com_interfaces_[1],
				clsctx=CLSCTX_INPROC_SERVER,
			)
			# #7345: Instruct UIA to never map MSAA winEvents to UIA propertyChange events.
			# These events are not needed by NVDA, and they can cause the UI Automation client library to become unresponsive if an application firing winEvents has a slow message pump.
			pfm = self.clientObject.proxyFactoryMapping
			for index in range(pfm.count):
				e = pfm.getEntry(index)
				entryChanged = False
				for eventId, propertyIds in ignoreWinEventsMap.items():
					for propertyId in propertyIds:
						# Check if this proxy has mapped any winEvents to the UIA propertyChange event for this property ID
						try:
							oldWinEvents = e.getWinEventsForAutomationEvent(eventId, propertyId)
						except IndexError:
							# comtypes does not seem to correctly handle a returned empty SAFEARRAY, raising IndexError
							oldWinEvents = None
						if oldWinEvents:
							# As winEvents were mapped, replace them with an empty list
							e.setWinEventsForAutomationEvent(eventId, propertyId, [])
							entryChanged = True
				if entryChanged:
					# Changes to an entry are not automatically picked up.
					# Therefore remove the entry and re-insert it.
					pfm.removeEntry(index)
					pfm.insertEntry(index, e)
			# #8009: use appropriate interface based on highest supported interface.
			# #8338: made easier by traversing interfaces supported on Windows 8 and later in reverse.
			for interface in reversed(UIA.CUIAutomation8._com_interfaces_):
				try:
					self.clientObject = self.clientObject.QueryInterface(interface)
					break
				except COMError:
					pass
			# Windows 10 RS5 provides new performance features for UI Automation
			# including event coalescing and connection recovery.
			# Enable all of these where available.
			if isinstance(self.clientObject, UIA.IUIAutomation6):
				self.clientObject.CoalesceEvents = UIA.CoalesceEventsOptions_Enabled
				self.clientObject.ConnectionRecoveryBehavior = UIA.ConnectionRecoveryBehaviorOptions_Enabled
			log.info(f"UIAutomation: {self.clientObject.__class__.__mro__[1].__name__}")
			self.windowTreeWalker = self.clientObject.createTreeWalker(
				self.clientObject.CreateNotCondition(
					self.clientObject.CreatePropertyCondition(UIA_NativeWindowHandlePropertyId, 0),  # noqa: F405
				),
			)  # noqa: F405
			self.windowCacheRequest = self.clientObject.CreateCacheRequest()
			self.windowCacheRequest.AddProperty(UIA_NativeWindowHandlePropertyId)  # noqa: F405
			self.UIAWindowHandleCache = {}
			self.baseTreeWalker = self.clientObject.RawViewWalker
			self.baseCacheRequest = self.windowCacheRequest.Clone()
			for propertyId in baseCachePropertyIDs:
				self.baseCacheRequest.addProperty(propertyId)
			self.baseCacheRequest.addPattern(UIA_TextPatternId)  # noqa: F405
			self.rootElement = self.clientObject.getRootElementBuildCache(self.baseCacheRequest)
			self.reservedNotSupportedValue = self.clientObject.ReservedNotSupportedValue
			self.ReservedMixedAttributeValue = self.clientObject.ReservedMixedAttributeValue
			if config.conf["UIA"]["enhancedEventProcessing"]:
				handler = self._rateLimitedEventHandler = POINTER(IUnknown)()
				NVDAHelper.localLib.rateLimitedUIAEventHandler_create(
					self._com_pointers_[IUnknown._iid_],
					byref(self._rateLimitedEventHandler),
				)
			else:
				handler = self
			if utils._shouldSelectivelyRegister():
				self._createLocalEventHandlerGroup(handler)
			self._registerGlobalEventHandlers(handler)
			if winVersion.getWinVer() >= winVersion.WIN11:
				UIARemote.initialize(True, self.clientObject)
		except Exception as e:
			self.MTAThreadInitException = e
		finally:
			self.MTAThreadInitEvent.set()
		while True:
			func = self.MTAThreadQueue.get()
			if func:
				try:
					func()
				except Exception:
					log.error("Exception in function queued to UIA MTA thread", exc_info=True)
			else:
				break
		self.clientObject.RemoveAllEventHandlers()
		del self.localEventHandlerGroup
		del self.localEventHandlerGroupWithTextChanges
		del self.globalEventHandlerGroup
		self._rateLimitedEventHandler = None
		if winVersion.getWinVer() >= winVersion.WIN11:
			UIARemote.terminate()

	def _registerGlobalEventHandlers(self, handler: "UIAHandler"):
		self.clientObject.AddFocusChangedEventHandler(self.baseCacheRequest, handler)
		if isinstance(self.clientObject, UIA.IUIAutomation6):
			self.globalEventHandlerGroup = self.clientObject.CreateEventHandlerGroup()
		else:
			self.globalEventHandlerGroup = utils.FakeEventHandlerGroup(self.clientObject)
		self.globalEventHandlerGroup.AddPropertyChangedEventHandler(
			UIA.TreeScope_Subtree,
			self.baseCacheRequest,
			handler,
			*self.clientObject.IntSafeArrayToNativeArray(
				globalEventHandlerGroupUIAPropertyIds
				if utils._shouldSelectivelyRegister()
				else UIAPropertyIdsToNVDAEventNames,
			),
		)
		for eventId in (
			globalEventHandlerGroupUIAEventIds
			if utils._shouldSelectivelyRegister()
			else UIAEventIdsToNVDAEventNames
		):
			self.globalEventHandlerGroup.AddAutomationEventHandler(
				eventId,
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				handler,
			)
		if not utils._shouldSelectivelyRegister() and winVersion.getWinVer() >= winVersion.WIN10:
			# #14067: Due to poor performance, textChange requires special handling
			self.globalEventHandlerGroup.AddAutomationEventHandler(
				UIA.UIA_Text_TextChangedEventId,
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				handler,
			)
		# #7984: add support for notification event (IUIAutomation5, part of Windows 10 build 16299 and later).
		if isinstance(self.clientObject, UIA.IUIAutomation5):
			self.globalEventHandlerGroup.AddNotificationEventHandler(
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				handler,
			)
		if isinstance(self.clientObject, UIA.IUIAutomation6):
			self.globalEventHandlerGroup.AddActiveTextPositionChangedEventHandler(
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				handler,
			)
		self.addEventHandlerGroup(self.rootElement, self.globalEventHandlerGroup)

	def _createLocalEventHandlerGroup(self, handler: "UIAHandler"):
		if isinstance(self.clientObject, UIA.IUIAutomation6):
			self.localEventHandlerGroup = self.clientObject.CreateEventHandlerGroup()
			self.localEventHandlerGroupWithTextChanges = self.clientObject.CreateEventHandlerGroup()
		else:
			self.localEventHandlerGroup = utils.FakeEventHandlerGroup(self.clientObject)
			self.localEventHandlerGroupWithTextChanges = utils.FakeEventHandlerGroup(self.clientObject)
		self.localEventHandlerGroup.AddPropertyChangedEventHandler(
			UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
			self.baseCacheRequest,
			handler,
			*self.clientObject.IntSafeArrayToNativeArray(localEventHandlerGroupUIAPropertyIds),
		)
		self.localEventHandlerGroupWithTextChanges.AddPropertyChangedEventHandler(
			UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
			self.baseCacheRequest,
			handler,
			*self.clientObject.IntSafeArrayToNativeArray(localEventHandlerGroupUIAPropertyIds),
		)
		for eventId in localEventHandlerGroupUIAEventIds:
			self.localEventHandlerGroup.AddAutomationEventHandler(
				eventId,
				UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
				self.baseCacheRequest,
				handler,
			)
			self.localEventHandlerGroupWithTextChanges.AddAutomationEventHandler(
				eventId,
				UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
				self.baseCacheRequest,
				handler,
			)
		self.localEventHandlerGroupWithTextChanges.AddAutomationEventHandler(
			UIA.UIA_Text_TextChangedEventId,
			UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
			self.baseCacheRequest,
			handler,
		)

	def addEventHandlerGroup(self, element, eventHandlerGroup):
		if isinstance(eventHandlerGroup, UIA.IUIAutomationEventHandlerGroup):
			self.clientObject.AddEventHandlerGroup(element, eventHandlerGroup)
		elif isinstance(eventHandlerGroup, utils.FakeEventHandlerGroup):
			eventHandlerGroup.registerToClientObject(element)
		else:
			raise NotImplementedError

	def removeEventHandlerGroup(self, element, eventHandlerGroup):
		if isinstance(eventHandlerGroup, UIA.IUIAutomationEventHandlerGroup):
			self.clientObject.RemoveEventHandlerGroup(element, eventHandlerGroup)
		elif isinstance(eventHandlerGroup, utils.FakeEventHandlerGroup):
			eventHandlerGroup.unregisterFromClientObject(element)
		else:
			raise NotImplementedError

	def addLocalEventHandlerGroupToElement(self, element, isFocus=False):
		if not self.localEventHandlerGroup or element in self._localEventHandlerGroupElements:
			return

		def func():
			if isFocus:
				try:
					isStillFocus = self.clientObject.CompareElements(
						self.clientObject.GetFocusedElement(),
						element,
					)
				except COMError:
					isStillFocus = False
				if not isStillFocus:
					return
			try:
				if (
					element.currentClassName in textChangeUIAClassNames
					or element.CachedAutomationID in textChangeUIAAutomationIDs
					or (
						not utils._shouldUseWindowsTerminalNotifications()
						and element.currentClassName in windowsTerminalUIAClassNames
					)
				):
					group = self.localEventHandlerGroupWithTextChanges
					logPrefix = "Explicitly"
				else:
					group = self.localEventHandlerGroup
					logPrefix = "Not"

				if _isDebug():
					log.debugWarning(
						f"{logPrefix} registering for textChange events from UIA element "
						f"with class name {repr(element.currentClassName)} "
						f"and automation ID {repr(element.CachedAutomationID)}",
					)
				self.addEventHandlerGroup(element, group)
			except COMError:
				log.error("Could not register for UIA events for element", exc_info=True)
			else:
				self._localEventHandlerGroupElements.add(element)

		self.MTAThreadQueue.put_nowait(func)

	def removeLocalEventHandlerGroupFromElement(self, element):
		if not self.localEventHandlerGroup or element not in self._localEventHandlerGroupElements:
			return

		def func():
			try:
				self.removeEventHandlerGroup(element, self.localEventHandlerGroup)
			except COMError:
				# The old UIAElement has probably died as the window was closed.
				# The system should forget the old event registration itself.
				# Yet, as we don't expect this to happen very often, log a debug warning.
				log.debugWarning("Could not unregister for UIA events for element", exc_info=True)
			self._localEventHandlerGroupElements.remove(element)

		self.MTAThreadQueue.put_nowait(func)

	def IUIAutomationEventHandler_HandleAutomationEvent(self, sender, eventID):
		if _isDebug():
			log.debug(
				f"handleAutomationEvent called with event {self.getUIAEventIDDebugString(eventID)} "
				f"for element {self.getUIAElementDebugString(sender)}",
			)
		if not self.MTAThreadInitEvent.is_set():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandleAutomationEvent: event received while not fully initialized")
			return
		if eventID == UIA_MenuOpenedEventId and eventHandler.isPendingEvents("gainFocus"):  # noqa: F405
			# We don't need the menuOpened event if focus has been fired,
			# as focus should be more correct.
			if _isDebug():
				log.debug("HandleAutomationEvent: Ignored MenuOpenedEvent while focus event pending")
			return
		if eventID == UIA.UIA_Text_TextChangedEventId:
			if (
				sender.currentClassName in textChangeUIAClassNames
				or sender.CachedAutomationID in textChangeUIAAutomationIDs
				or (
					not utils._shouldUseWindowsTerminalNotifications()
					and sender.currentClassName in windowsTerminalUIAClassNames
				)
			):
				NVDAEventName = "textChange"
			else:
				if _isDebug():
					log.debugWarning(
						"HandleAutomationEvent: Dropping textChange event "
						f"from element {self.getUIAElementDebugString(sender)}",
					)
				return
		else:
			NVDAEventName = UIAEventIdsToNVDAEventNames.get(eventID, None)
		if not NVDAEventName:
			if _isDebug():
				log.debugWarning(f"HandleAutomationEvent: Don't know how to handle event {eventID}")
			return
		obj = None
		focus = api.getFocusObject()
		import NVDAObjects.UIA

		if isinstance(focus, NVDAObjects.UIA.UIA) and self.clientObject.compareElements(
			focus.UIAElement,
			sender,
		):
			if _isDebug():
				log.debug(
					"handleAutomationEvent: element matches focus. "
					f"Redirecting event to focus NVDAObject {focus}",
				)
			obj = focus
		elif not self.isNativeUIAElement(sender):
			if _isDebug():
				log.debug(
					f"HandleAutomationEvent: Ignoring event {NVDAEventName} for non native element",
				)
			return
		window = obj.windowHandle if obj else self.getNearestWindowHandle(sender)
		if window:
			if _isDebug():
				log.debug(
					f"Checking if should accept NVDA event {NVDAEventName} "
					f"with window {self.getWindowHandleDebugString(window)}",
				)
			if not eventHandler.shouldAcceptEvent(NVDAEventName, windowHandle=window):
				if _isDebug():
					log.debug(
						f"HandleAutomationEvent: Ignoring event {NVDAEventName} for shouldAcceptEvent=False",
					)
				return
		if not obj:
			try:
				obj = NVDAObjects.UIA.UIA(windowHandle=window, UIAElement=sender)
			except Exception:
				if _isDebug():
					log.debugWarning(
						f"HandleAutomationEvent: Exception while creating object for event {NVDAEventName}",
						exc_info=True,
					)
				return
			if not obj:
				if _isDebug():
					log.debug("handleAutomationEvent: No NVDAObject could be created")
				return
			if _isDebug():
				log.debug(
					f"handleAutomationEvent: created object {obj} ",
				)
		if (NVDAEventName == "gainFocus" and not obj.shouldAllowUIAFocusEvent) or (
			NVDAEventName == "liveRegionChange" and not obj._shouldAllowUIALiveRegionChangeEvent
		):
			if _isDebug():
				log.debug(
					f"HandleAutomationEvent: Ignoring event {NVDAEventName} because ignored by object itself",
				)
			return
		if _isDebug():
			log.debug(
				f"handleAutomationEvent: queuing NVDA event {NVDAEventName} for NVDAObject {obj} ",
			)
		eventHandler.queueEvent(NVDAEventName, obj)

	# The last UIAElement that received a UIA focus event
	# This is updated no matter if this is a native element, the window is UIA blacklisted by NVDA, or  the element is proxied from MSAA
	lastFocusedUIAElement = None

	def IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(self, sender):
		if _isDebug():
			log.debug(f"handleFocusChangedEvent called with element {self.getUIAElementDebugString(sender)}")
		if not self.MTAThreadInitEvent.is_set():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandleFocusChangedEvent: event received while not fully initialized")
			return
		self.lastFocusedUIAElement = sender
		if not self.isNativeUIAElement(sender):
			# #12982: This element may be the root of an MS Word document
			# for which we may be refusing to use UIA as its implementation may be incomplete.
			# However, there are some controls embedded in the MS Word document window
			# such as the Modern comments side track pane
			# for which we do have to use UIA.
			# But, if focus jumps from one of these controls back to the document (E.g. the user presses escape),
			# we receive no MSAA focus event, only a UIA focus event.
			# As we are not treating the Word doc as UIA, we need to manually fire an MSAA focus event on the document.
			self._emitMSAAFocusForWordDocIfNecessary(sender)
			if _isDebug():
				log.debug(f"Ignoring for non native element {self.getUIAElementDebugString(sender)}")
			return
		import NVDAObjects.UIA

		if isinstance(eventHandler.lastQueuedFocusObject, NVDAObjects.UIA.UIA):
			lastFocusObj = eventHandler.lastQueuedFocusObject
			# Ignore duplicate focus events.
			# It seems that it is possible for compareElements to return True, even though the objects are different.
			# Therefore, don't ignore the event if the last focus object has lost its hasKeyboardFocus state.
			try:
				if (
					not lastFocusObj.shouldAllowDuplicateUIAFocusEvent
					and self.clientObject.compareElements(sender, lastFocusObj.UIAElement)
					and lastFocusObj.UIAElement.currentHasKeyboardFocus
				):
					if _isDebug():
						log.debugWarning(
							"HandleFocusChangedEvent: Ignoring duplicate focus event ",
						)
					return
			except COMError:
				if _isDebug():
					log.debugWarning(
						"HandleFocusChangedEvent: Couldn't check for duplicate focus event ",
						exc_info=True,
					)
		window = self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent("gainFocus", windowHandle=window):
			if _isDebug():
				log.debug(
					"HandleFocusChangedEvent: Ignoring for shouldAcceptEvent=False",
				)
			return
		try:
			obj = NVDAObjects.UIA.UIA(windowHandle=window, UIAElement=sender)
		except Exception:
			if _isDebug():
				log.debugWarning(
					"HandleFocusChangedEvent: Exception while creating NVDAObject ",
					exc_info=True,
				)
			obj = None
		if not obj:
			if _isDebug():
				log.debug(
					"handleFocusChangedEvent: Could not create an NVDAObject ",
				)
			return
		if _isDebug():
			log.debug(f"Created object {obj} for element {self.getUIAElementDebugString(sender)}")
		if not obj.shouldAllowUIAFocusEvent:
			if _isDebug():
				log.debug(
					"HandleFocusChangedEvent: NVDAObject chose to ignore event ",
				)
			return
		if _isDebug():
			log.debug(
				f"handleFocusChangedEvent: Queuing NVDA gainFocus event for obj {obj} ",
			)
		eventHandler.queueEvent("gainFocus", obj)

	def IUIAutomationPropertyChangedEventHandler_HandlePropertyChangedEvent(
		self,
		sender,
		propertyId,
		newValue,
	):
		if _isDebug():
			log.debug(
				f"handlePropertyChangeEvent called with property {self.getUIAPropertyIDDebugString(propertyId)}, "
				f"value {str(newValue.value)[:50]} "
				f"for element {self.getUIAElementDebugString(sender)}",
			)
		# #3867: For now manually force this VARIANT type to empty to get around a nasty double free in comtypes/ctypes.
		# We also don't use the value in this callback.
		newValue.vt = VT_EMPTY
		if not self.MTAThreadInitEvent.is_set():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandlePropertyChangedEvent: event received while not fully initialized")
			return
		try:
			processId = sender.CachedProcessID
		except COMError:
			pass
		else:
			appMod = appModuleHandler.getAppModuleFromProcessID(processId)
			if not appMod.shouldProcessUIAPropertyChangedEvent(sender, propertyId):
				if _isDebug():
					log.debug(
						f"handlePropertyChangeEvent: dropping property {self.getUIAPropertyIDDebugString(propertyId)} "
						f"at request of appModule {appMod.appName}",
					)
				return
		NVDAEventName = UIAPropertyIdsToNVDAEventNames.get(propertyId, None)
		if not NVDAEventName:
			if _isDebug():
				log.debugWarning(
					f"HandlePropertyChangedEvent: Don't know how to handle property {propertyId}",
				)
			return
		obj = None
		focus = api.getFocusObject()
		import NVDAObjects.UIA

		if isinstance(focus, NVDAObjects.UIA.UIA) and self.clientObject.compareElements(
			focus.UIAElement,
			sender,
		):
			if _isDebug():
				log.debug(
					f"propertyChange event is for focus. Redirecting event to focus NVDAObject {focus}",
				)
			obj = focus
		elif not self.isNativeUIAElement(sender):
			if _isDebug():
				log.debug(
					f"HandlePropertyChangedEvent: Ignoring event {NVDAEventName} for non native element",
				)
			return
		window = obj.windowHandle if obj else self.getNearestWindowHandle(sender)
		if window:
			if _isDebug():
				log.debug(
					f"Checking if should accept NVDA event {NVDAEventName} "
					f"with window {self.getWindowHandleDebugString(window)}",
				)
			if not eventHandler.shouldAcceptEvent(NVDAEventName, windowHandle=window):
				if _isDebug():
					log.debug(
						f"HandlePropertyChangedEvent: Ignoring event {NVDAEventName} for shouldAcceptEvent=False",
					)
				return
		if not obj:
			try:
				obj = NVDAObjects.UIA.UIA(windowHandle=window, UIAElement=sender)
			except Exception:
				if _isDebug():
					log.debugWarning(
						f"HandlePropertyChangedEvent: Exception while creating object for event {NVDAEventName}",
						exc_info=True,
					)
				return
			if not obj:
				if _isDebug():
					log.debug(f"HandlePropertyChangedEvent: Ignoring event {NVDAEventName} because no object")
				return
			if _isDebug():
				log.debug(
					f"handlePropertyChangeEvent: created object {obj} ",
				)
		if _isDebug():
			log.debug(
				f"handlePropertyChangeEvent: queuing NVDA {NVDAEventName} event for NVDAObject {obj} ",
			)
		eventHandler.queueEvent(NVDAEventName, obj)

	def IUIAutomationNotificationEventHandler_HandleNotificationEvent(
		self,
		sender,
		NotificationKind,
		NotificationProcessing,
		displayString,
		activityId,
	):
		if _isDebug():
			log.debug(
				"handleNotificationEvent called "
				f"with notificationKind {self.getUIANotificationKindDebugString(NotificationKind)}, "
				f"notificationProcessing {self.getUIANotificationProcessingValueDebugString(NotificationProcessing)}, "
				f"displayString {str(displayString)[:50]}, "
				f"activityID {activityId}, "
				f"for element {self.getUIAElementDebugString(sender)}",
			)
		if not self.MTAThreadInitEvent.is_set():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandleNotificationEvent: event received while not fully initialized")
			return
		import NVDAObjects.UIA

		try:
			obj = NVDAObjects.UIA.UIA(UIAElement=sender)
		except Exception:
			if _isDebug():
				log.debugWarning(
					"HandleNotificationEvent: Exception while creating object: "
					f"NotificationProcessing={NotificationProcessing} "
					f"displayString={displayString} "
					f"activityId={activityId}",
					exc_info=True,
				)
			return
		if not obj:
			# Sometimes notification events can be fired on a UIAElement that has no windowHandle and does not connect through parents back to the desktop.
			# There is nothing we can do with these.
			if _isDebug():
				log.debug(
					"HandleNotificationEvent: Ignoring because no object: "
					f"NotificationProcessing={NotificationProcessing} "
					f"displayString={displayString} "
					f"activityId={activityId}",
				)
			return
		if _isDebug():
			log.debug(
				f"Queuing UIA_notification NVDA event for NVDAObject {obj}",
			)
		eventHandler.queueEvent(
			"UIA_notification",
			obj,
			notificationKind=NotificationKind,
			notificationProcessing=NotificationProcessing,
			displayString=displayString,
			activityId=activityId,
		)

	def IUIAutomationActiveTextPositionChangedEventHandler_HandleActiveTextPositionChangedEvent(
		self,
		sender,
		textRange,
	):
		if _isDebug():
			log.debug(
				f"HandleActiveTextPositionChangedEvent called for element {self.getUIAElementDebugString(sender)}",
			)
		if not self.MTAThreadInitEvent.is_set():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandleActiveTextPositionchangedEvent: event received while not fully initialized")
			return
		import NVDAObjects.UIA

		try:
			obj = NVDAObjects.UIA.UIA(UIAElement=sender)
		except Exception:
			if _isDebug():
				log.debugWarning(
					"HandleActiveTextPositionChangedEvent: Exception while creating object: ",
					exc_info=True,
				)
			return
		if not obj:
			if _isDebug():
				log.debug(
					"HandleActiveTextPositionchangedEvent: Ignoring because no object: ",
				)
			return
		if _isDebug():
			log.debug(
				"handleActiveTextPositionChange: Queuing UIA_activeTextPositionChanged NVDA event "
				f"for NVDAObject {obj}",
			)
		eventHandler.queueEvent("UIA_activeTextPositionChanged", obj, textRange=textRange)

	# C901: '_isUIAWindowHelper' is too complex
	# Note: when working on _isUIAWindowHelper, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def _isUIAWindowHelper(self, hwnd: int, isDebug=False) -> bool:  # noqa: C901
		if isDebug:
			log.debug(f"checking window {self.getWindowHandleDebugString(hwnd)}")
		# UIA in NVDA's process freezes in Windows 7 and below
		processID = winUser.getWindowThreadProcessID(hwnd)[0]
		if globalVars.appPid == processID:
			if isDebug:
				log.debug("Window is from NVDA's process. Treating as non-UIA")
			return False
		import NVDAObjects.window

		rawWindowClass = winUser.getClassName(hwnd)
		windowClass = NVDAObjects.window.Window.normalizeWindowClassName(rawWindowClass)
		# For certain window classes, we always want to use UIA.
		if windowClass in goodUIAWindowClassNames:
			if isDebug:
				log.debug("Window found in goodUIAWindowClassNames. Treating as UIA")
			return True
		# allow the appModule for the window to also choose if this window is good
		# An appModule should be able to override bad UIA class names as prescribed by core
		appModule = appModuleHandler.getAppModuleFromProcessID(processID)
		if appModule and appModule.isGoodUIAWindow(hwnd):
			if isDebug:
				log.debug(
					f"appModule {appModule.appName} says to treat window as UIA",
				)
			return True
		# There are certain window classes that just had bad UIA implementations
		if windowClass in badUIAWindowClassNames:
			if isDebug:
				log.debug("Window found in baddUIAWindowClassNames. Treating as non-UIA")
			return False
		# allow the appModule for the window to also choose if this window is bad
		if appModule and appModule.isBadUIAWindow(hwnd):
			if isDebug:
				log.debug(
					f"appModule {appModule.appName} says to not treat window as UIA",
				)
			return False
		if windowClass == "NetUIHWND" and appModule:
			# NetUIHWND is used for various controls in MS Office.
			# IAccessible should be used for NetUIHWND in versions older than 2016
			# Fixes: lack of focus reporting (#4207),
			# Fixes: strange reporting of context menu items(#9252),
			# fixes: not being able to report ribbon sections when they starts with an edit  field (#7067)
			# Note that #7067 is not fixed for Office 2016 and never.
			# Using IAccessible for NetUIHWND controls causes focus changes not to be reported
			# when the ribbon is collapsed.
			# Testing shows that these controls emits proper events but they are ignored by NVDA.
			try:
				isOfficeApp = appModule.productName.startswith(("Microsoft Office", "Microsoft Outlook"))
				isOffice2013OrOlder = isOfficeApp and int(appModule.productVersion.split(".")[0]) < 16
			except RuntimeError:
				# this is not necessarily an office app, or an app with version information, for example geekbench 6.
				log.debugWarning(
					"Failed parsing productName / productVersion, version information likely missing",
					exc_info=True,
				)
				isOfficeApp = False
				isOffice2013OrOlder = False
			if isOfficeApp and isOffice2013OrOlder:
				parentHwnd = winUser.getAncestor(hwnd, winUser.GA_PARENT)
				while parentHwnd:
					if winUser.getClassName(parentHwnd) in ("Net UI Tool Window", "MsoCommandBar"):
						if isDebug:
							log.debug("Office 2013 ribon or older. Treating as non-UIA")
						return False
					parentHwnd = winUser.getAncestor(parentHwnd, winUser.GA_PARENT)
		# Ask the window if it supports UIA natively
		res = windll.UIAutomationCore.UiaHasServerSideProvider(hwnd)
		if res:
			if isDebug:
				log.debug("window has UIA server side provider")
			canUseOlderInProcessApproach = bool(appModule.helperLocalBindingHandle)
			if windowClass == MS_WORD_DOCUMENT_WINDOW_CLASS:
				# The window does support UIA natively, but MS Word documents now
				# have a fairly usable UI Automation implementation.
				# However, builds of MS Office 2016 before build 15000 or so had bugs which
				# we cannot work around.
				# Therefore, if we can inject in-process, refuse to use UIA and instead
				# fall back to the MS Word object model.
				if not shouldUseUIAInMSWord(appModule):
					if isDebug:
						log.debug("MS word document treated as non-UIA")
					return False
			# MS Excel spreadsheets now have a fairly usable UI Automation implementation.
			# However, builds of MS Office 2016 before build 9000 or so had bugs which we
			# cannot work around.
			# And even current builds of Office 2016 are still missing enough info from UIA
			# that it is still impossible to switch to UIA completely.
			# Therefore, if we can inject in-process, refuse to use UIA and instead fall
			# back to the MS Excel object model.
			elif (
				# An MS Excel spreadsheet window
				windowClass == "EXCEL7"
				# Disabling is only useful if we can inject in-process (and use our older code)
				and appModule.helperLocalBindingHandle
				# Allow the user to explicitly force UIA support for MS Excel spreadsheets
				# no matter the Office version
				and not config.conf["UIA"]["useInMSExcelWhenAvailable"]
			):
				if isDebug:
					log.debug("MS Excel spreadsheet  treated as non-UIA")
				return False
			elif windowClass == "Chrome_RenderWidgetHostHWND":
				# Unless explicitly allowed, all Chromium implementations (including Edge) should not be UIA,
				# As their IA2 implementation is still better at the moment.
				# However, in cases where Chromium is running under another logon session,
				# the IAccessible2 implementation is unavailable.
				# 'brchrome' is part of HP SureClick, a chromium-based browser which runs webpages to run in separate
				# virtual machines - it supports UIA remoting but not IAccessible2 remoting.
				hasAccessToIA2 = (
					not appModule.isRunningUnderDifferentLogonSession and not appModule.appName == "brchrome"
				)
				if (
					AllowUiaInChromium.getConfig() == AllowUiaInChromium.NO
					# Disabling is only useful if we can inject in-process (and use our older code)
					or (
						canUseOlderInProcessApproach
						and hasAccessToIA2
						and AllowUiaInChromium.getConfig()
						!= AllowUiaInChromium.YES  # Users can prefer to use UIA
					)
				):
					if isDebug:
						log.debug("_isUIAWindowHelper:Chromium window treated as non-UIA")
					return False
			elif windowClass == "ConsoleWindowClass":
				if not utils._shouldUseUIAConsole(hwnd):
					if isDebug:
						log.debug("Windows console treated as non-UIA")
					return False
			elif windowClass == "SysListView32":
				# #15283: SysListView32 controls in Windows Forms have a native UIA implementation
				# and lack a MSAA implementation.
				# We need to rely on UIA for these controls, as otherwise parent/child navigation is broken.
				# For other instances however, even when the control advertises a native UIA implementation,
				# the implementation is likely to be incomplete and MSAA should be prefered.
				if isDebug:
					log.debug(f"Checking framework of {rawWindowClass} window ")
				if not utils._isFrameworkIdWinForm(hwnd):
					if isDebug:
						log.debug("SysListView32 treated as non-UIA")
					return False
			if isDebug:
				log.debug("Treating as UIA")
		else:
			if isDebug:
				log.debug("window does not have UIA server side provider. Treating as non-UIA")
		return bool(res)

	def isUIAWindow(self, hwnd: int, isDebug: bool = False) -> bool:
		# debugging for this function is explicitly controled via an argument
		# as this function may be also called from MSAA code.
		now = time.time()
		v = self.UIAWindowHandleCache.get(hwnd, None)
		if not v or (now - v[1]) > 0.5:
			v = (
				self._isUIAWindowHelper(hwnd, isDebug=isDebug),
				now,
			)
			self.UIAWindowHandleCache[hwnd] = v
		elif isDebug:
			log.debug(f"Found cached is UIA window {v[0]} for hwnd {self.getWindowHandleDebugString(hwnd)}")
		return v[0]

	def getNearestWindowHandle(self, UIAElement):
		if hasattr(UIAElement, "_nearestWindowHandle"):
			# Called previously. Use cached result.
			windowHandle = UIAElement._nearestWindowHandle
			if _isDebug():
				log.debug(
					"Got previously cached nearest windowHandle "
					f"of {self.getWindowHandleDebugString(windowHandle)} "
					f"for element {self.getUIAElementDebugString(UIAElement)}",
				)
			return windowHandle
		if _isDebug():
			log.debug(
				"Locating nearest ancestor windowHandle "
				f"for element {self.getUIAElementDebugString(UIAElement)}",
			)
		try:
			processID = UIAElement.cachedProcessID
		except COMError:
			return None
		appModule = appModuleHandler.getAppModuleFromProcessID(processID)
		# WDAG (Windows Defender application Guard) UIA elements should be treated as being from a remote machine, and therefore their window handles are completely invalid on this machine.
		# Unfortunately the remote UIA tree is not parented into the local tree.
		# Therefore, just use the currently active WDAG local window as the nearest window.
		if appModule.appName == WDAG_PROCESS_NAME:
			if _isDebug():
				log.debug("Detected WDAG element")
			gi = winUser.getGUIThreadInfo(0)
			if (
				winUser.getClassName(gi.hwndActive) == WDAG_WINDOW_CLASS_NAME
				and winUser.getWindowThreadProcessID(gi.hwndActive)[0] == processID
			):
				if _isDebug():
					log.debug(
						f"using active WDAG local window {self.getWindowHandleDebugString(gi.hwndActive)}",
					)
				return gi.hwndActive
			else:
				if _isDebug():
					log.debug(
						f"Active window is not WDAG or is wrong instance:  {self.getWindowHandleDebugString(gi.hwndActive)}",
					)
				return None
			condition = utils.createUIAMultiPropertyCondition(
				{UIA.UIA_ClassNamePropertyId: ["ApplicationFrameWindow", "CabinetWClass"]},
			)
			walker = self.clientObject.createTreeWalker(condition)
		else:
			# Not WDAG, just walk up to the nearest valid windowHandle
			walker = self.windowTreeWalker
		cacheRequest = self.windowCacheRequest
		if _isDebug():
			# When debugging we want some extra properties cached for logging.
			cacheRequest = self.baseCacheRequest
		try:
			new = walker.NormalizeElementBuildCache(UIAElement, cacheRequest)
		except COMError:
			log.debugWarning(
				"error walking up to an element with a valid windowHandle",
				exc_info=True,
			)
			return None
		try:
			window = new.cachedNativeWindowHandle
		except COMError:
			if _isDebug():
				log.debugWarning(
					"Unable to get cachedNativeWindowHandle from found ancestor element",
					exc_info=True,
				)
			return None
		if _isDebug():
			log.debug(
				f"Found ancestor element with valid windowHandle {self.getWindowHandleDebugString(window)}",
			)
		# Cache for future use to improve performance.
		UIAElement._nearestWindowHandle = window
		return window

	def _isNetUIEmbeddedInWordDoc(self, element: UIA.IUIAutomationElement) -> bool:
		"""
		Detects if the given UIA element represents a control in a NetUI container
		embedded within a MS Word document window.
		E.g. the Modern Comments side track pane.
		This method also caches the answer on the element itself
		to both speed up checking later and to allow checking on an already dead element
		E.g. a previous focus.
		"""
		if getattr(element, "_isNetUIEmbeddedInWordDoc", False):
			return True
		windowHandle = self.getNearestWindowHandle(element)
		if winUser.getClassName(windowHandle) != MS_WORD_DOCUMENT_WINDOW_CLASS:
			return False
		condition = utils.createUIAMultiPropertyCondition(
			{UIA.UIA_ClassNamePropertyId: "NetUIHWNDElement"},
			{UIA.UIA_NativeWindowHandlePropertyId: windowHandle},
		)
		walker = self.clientObject.createTreeWalker(condition)
		cacheRequest = self.clientObject.createCacheRequest()
		cacheRequest.AddProperty(UIA.UIA_ClassNamePropertyId)
		cacheRequest.AddProperty(UIA.UIA_NativeWindowHandlePropertyId)
		ancestor = walker.NormalizeElementBuildCache(element, cacheRequest)
		# ancestor will either be the embedded NetUIElement, or just hit the root of the MS Word document window
		if ancestor.CachedClassName != "NetUIHWNDElement":
			return False
		element._isNetUIEmbeddedInWordDoc = True
		return True

	def _emitMSAAFocusForWordDocIfNecessary(self, element: UIA.IUIAutomationElement) -> None:
		"""
		Fires an MSAA focus event on the given UIA element
		if the element is the root of a Word document,
		and the focus was previously in a NetUI container embedded in this Word document.
		"""
		import NVDAObjects.UIA

		oldFocus = eventHandler.lastQueuedFocusObject
		if (
			isinstance(oldFocus, NVDAObjects.UIA.UIA)
			and getattr(oldFocus.UIAElement, "_isNetUIEmbeddedInWordDoc", False)
			and element.CachedClassName == MS_WORD_DOCUMENT_WINDOW_CLASS
			and element.CachedControlType == UIA.UIA_DocumentControlTypeId
			and self.getNearestWindowHandle(element) == oldFocus.windowHandle
			and not self.isUIAWindow(oldFocus.windowHandle)
		):
			IAccessibleHandler.internalWinEventHandler.winEventLimiter.addEvent(
				winUser.EVENT_OBJECT_FOCUS,
				oldFocus.windowHandle,
				winUser.OBJID_CLIENT,
				0,
				oldFocus.windowThreadID,
			)

	def isNativeUIAElement(self, UIAElement):
		if _isDebug():
			log.debug(f"checking if is native UIA  element: {self.getUIAElementDebugString(UIAElement)}")
		# Due to issues dealing with UIA elements coming from the same process, we do not class these UIA elements as usable.
		# It seems to be safe enough to retrieve the cached processID,
		# but using tree walkers or fetching other properties causes a freeze.
		try:
			processID = UIAElement.cachedProcessId
		except COMError:
			if _isDebug():
				log.debug(f"could not fetch processId. {self.getUIAElementDebugString(UIAElement)}")
			return False
		if processID == globalVars.appPid:
			if _isDebug():
				log.debug(
					"element is local to NVDA, treating as non-native.",
				)
			return False
		# Whether this is a native element depends on whether its window natively supports UIA.
		windowHandle = self.getNearestWindowHandle(UIAElement)
		if windowHandle:
			if self.isUIAWindow(windowHandle, isDebug=_isDebug()):
				if _isDebug():
					log.debug(
						"treating element as native due to "
						f"windowHandle {self.getWindowHandleDebugString(windowHandle)}. ",
					)
				return True
			# #12982: although NVDA by default may not treat this element's window as native UIA,
			# E.g. it is proxied from MSAA, or NVDA has specifically black listed it,
			# It may be an element from a NetUIcontainer embedded in a Word document,
			# such as the MS Word Modern Comments side track pane.
			# These elements are only exposed via UIA, and not MSAA,
			# thus we must treat these elements as native UIA.
			if self._isNetUIEmbeddedInWordDoc(UIAElement):
				if _isDebug():
					log.debug(
						"treating as native as is a netUI embedded in word doc. ",
					)
				return True
			if (
				winUser.getClassName(windowHandle) == "DirectUIHWND"
				and "IEFRAME.dll" in UIAElement.cachedProviderDescription
				and UIAElement.currentClassName
				in ("DownloadBox", "accessiblebutton", "DUIToolbarButton", "PushButton")
			):
				# This is the IE 9 downloads list.
				# #3354: UiaHasServerSideProvider returns false for the IE 9 downloads list window,
				# so we'd normally use MSAA for this control.
				# However, its MSAA implementation is broken (fires invalid events) if UIA is initialised,
				# whereas its UIA implementation works correctly.
				# Therefore, we must use UIA here.
				if _isDebug():
					log.debug(
						"treating as native as is in IE9 downloads list. ",
					)
				return True
		if _isDebug():
			log.debug("Treating element as non-native")
		return False


handler: Optional[UIAHandler] = None


def initialize():
	global handler
	if not config.conf["UIA"]["enabled"]:
		raise RuntimeError("UIA forcefully disabled in configuration")
	try:
		handler = UIAHandler()
	except COMError:
		handler = None
		raise


def terminate():
	global handler
	if handler:
		handler.terminate()
		handler = None


def _isDebug():
	return config.conf["debugLog"]["UIA"]
