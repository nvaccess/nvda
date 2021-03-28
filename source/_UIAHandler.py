# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2011-2021 NV Access Limited, Joseph Lee, Babbage B.V., Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes
import ctypes.wintypes
from ctypes import (
	oledll,
	windll,
)
from enum import (
	Enum,
)

import comtypes.client
from comtypes.automation import VT_EMPTY
from comtypes import (
	COMError,
	COMObject,
	byref,
	CLSCTX_INPROC_SERVER,
	CoCreateInstance,
)

import threading
import time
import config
import api
import appModuleHandler
import controlTypes
import winKernel
import winUser
import winVersion
import eventHandler
from logHandler import log
import UIAUtils
from comInterfaces import UIAutomationClient as UIA
# F403: unable to detect undefined names
from comInterfaces .UIAutomationClient import *  # noqa:  F403
import textInfos
from typing import Dict
from queue import Queue
import aria



HorizontalTextAlignment_Left=0
HorizontalTextAlignment_Centered=1
HorizontalTextAlignment_Right=2
HorizontalTextAlignment_Justified=3



# The name of the WDAG (Windows Defender Application Guard) process
WDAG_PROCESS_NAME=u'hvsirdpclient'

goodUIAWindowClassNames=[
	# A WDAG (Windows Defender Application Guard) Window is always native UIA, even if it doesn't report as such.
	'RAIL_WINDOW',
	"EXCEL6",
]

badUIAWindowClassNames=[
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
	"SysListView32",
	"Button",
	# #8944: The Foxit UIA implementation is incomplete and should not be used for now.
	"FoxitDocWnd",
]

# #8405: used to detect UIA dialogs prior to Windows 10 RS5.
UIADialogClassNames=[
	"#32770",
	"NUIDialog",
	"Credential Dialog Xaml Host", # UAC dialog in Anniversary Update and later
	"Shell_Dialog",
	"Shell_Flyout",
	"Shell_SystemDialog", # Various dialogs in Windows 10 Settings app
]

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

UIALiveSettingtoNVDAAriaLivePoliteness: Dict[str, aria.AriaLivePoliteness] = {
	UIA.Off: aria.AriaLivePoliteness.OFF,
	UIA.Polite: aria.AriaLivePoliteness.POLITE,
	UIA.Assertive: aria.AriaLivePoliteness.ASSERTIVE,
}

UIAPropertyIdsToNVDAEventNames={
	UIA_NamePropertyId:"nameChange",
	UIA_HelpTextPropertyId:"descriptionChange",
	UIA_ExpandCollapseExpandCollapseStatePropertyId:"stateChange",
	UIA_ToggleToggleStatePropertyId:"stateChange",
	UIA_IsEnabledPropertyId:"stateChange",
	UIA_ValueValuePropertyId:"valueChange",
	UIA_RangeValueValuePropertyId:"valueChange",
	UIA_ControllerForPropertyId:"UIA_controllerFor",
	UIA_ItemStatusPropertyId:"UIA_itemStatus",
}

globalEventHandlerGroupUIAPropertyIds = {
	UIA.UIA_RangeValueValuePropertyId
}

localEventHandlerGroupUIAPropertyIds = (
	set(UIAPropertyIdsToNVDAEventNames)
	- globalEventHandlerGroupUIAPropertyIds
)

UIALandmarkTypeIdsToLandmarkNames: Dict[int, str] = {
	UIA.UIA_FormLandmarkTypeId: "form",
	UIA.UIA_NavigationLandmarkTypeId: "navigation",
	UIA.UIA_MainLandmarkTypeId: "main",
	UIA.UIA_SearchLandmarkTypeId: "search",
}

UIAEventIdsToNVDAEventNames={
	UIA_LiveRegionChangedEventId:"liveRegionChange",
	UIA_SelectionItem_ElementSelectedEventId:"UIA_elementSelected",
	UIA_MenuOpenedEventId:"gainFocus",
	UIA_SelectionItem_ElementAddedToSelectionEventId:"stateChange",
	UIA_SelectionItem_ElementRemovedFromSelectionEventId:"stateChange",
	#UIA_MenuModeEndEventId:"menuModeEnd",
	UIA_ToolTipOpenedEventId:"UIA_toolTipOpened",
	#UIA_AsyncContentLoadedEventId:"documentLoadComplete",
	#UIA_ToolTipClosedEventId:"hide",
	UIA_Window_WindowOpenedEventId:"UIA_window_windowOpen",
	UIA_SystemAlertEventId:"UIA_systemAlert",
}

localEventHandlerGroupUIAEventIds = set()

autoSelectDetectionAvailable = False
if winVersion.getWinVer() >= winVersion.WIN10:
	UIAEventIdsToNVDAEventNames.update({
		UIA.UIA_Text_TextChangedEventId: "textChange",
		UIA.UIA_Text_TextSelectionChangedEventId: "caret",
	})
	localEventHandlerGroupUIAEventIds.update({
		UIA.UIA_Text_TextChangedEventId,
		UIA.UIA_Text_TextSelectionChangedEventId,
	})
	autoSelectDetectionAvailable = True

globalEventHandlerGroupUIAEventIds = set(UIAEventIdsToNVDAEventNames) - localEventHandlerGroupUIAEventIds

ignoreWinEventsMap = {
	UIA_AutomationPropertyChangedEventId: list(UIAPropertyIdsToNVDAEventNames.keys()),
}
for id in UIAEventIdsToNVDAEventNames.keys():
	ignoreWinEventsMap[id] = [0]


class AllowUiaInChromium(Enum):
	_DEFAULT = 0  # maps to 'when necessary'
	WHEN_NECESSARY = 1  # the current default
	YES = 2
	NO = 3

	@staticmethod
	def getConfig() -> 'AllowUiaInChromium':
		allow = AllowUiaInChromium(config.conf['UIA']['allowInChromium'])
		if allow == AllowUiaInChromium._DEFAULT:
			return AllowUiaInChromium.WHEN_NECESSARY
		return allow


class UIAHandler(COMObject):
	_com_interfaces_ = [
		UIA.IUIAutomationEventHandler,
		UIA.IUIAutomationFocusChangedEventHandler,
		UIA.IUIAutomationPropertyChangedEventHandler,
		UIA.IUIAutomationNotificationEventHandler,
		UIA.IUIAutomationActiveTextPositionChangedEventHandler,
	]

	def __init__(self):
		super(UIAHandler,self).__init__()
		self.globalEventHandlerGroup = None
		self.localEventHandlerGroup = None
		self._localEventHandlerGroupElements = set()
		self.MTAThreadInitEvent=threading.Event()
		self.MTAThreadQueue = Queue()
		self.MTAThreadInitException=None
		self.MTAThread = threading.Thread(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}.MTAThread",
			target=self.MTAThreadFunc
		)
		self.MTAThread.daemon=True
		self.MTAThread.start()
		self.MTAThreadInitEvent.wait(2)
		if self.MTAThreadInitException:
			raise self.MTAThreadInitException

	def terminate(self):
		MTAThreadHandle = ctypes.wintypes.HANDLE(
			windll.kernel32.OpenThread(
				winKernel.SYNCHRONIZE,
				False,
				self.MTAThread.ident
			)
		)
		self.MTAThreadQueue.put_nowait(None)
		#Wait for the MTA thread to die (while still message pumping)
		if windll.user32.MsgWaitForMultipleObjects(1,byref(MTAThreadHandle),False,200,0)!=0:
			log.debugWarning("Timeout or error while waiting for UIAHandler MTA thread")
		windll.kernel32.CloseHandle(MTAThreadHandle)
		del self.MTAThread

	def MTAThreadFunc(self):
		try:
			oledll.ole32.CoInitializeEx(None,comtypes.COINIT_MULTITHREADED) 
			isUIA8=False
			try:
				self.clientObject=CoCreateInstance(CUIAutomation8._reg_clsid_,interface=IUIAutomation,clsctx=CLSCTX_INPROC_SERVER)
				isUIA8=True
			except (COMError,WindowsError,NameError):
				self.clientObject=CoCreateInstance(CUIAutomation._reg_clsid_,interface=IUIAutomation,clsctx=CLSCTX_INPROC_SERVER)
			# #7345: Instruct UIA to never map MSAA winEvents to UIA propertyChange events.
			# These events are not needed by NVDA, and they can cause the UI Automation client library to become unresponsive if an application firing winEvents has a slow message pump. 
			pfm=self.clientObject.proxyFactoryMapping
			for index in range(pfm.count):
				e=pfm.getEntry(index)
				entryChanged = False
				for eventId, propertyIds in ignoreWinEventsMap.items():
					for propertyId in propertyIds:
						# Check if this proxy has mapped any winEvents to the UIA propertyChange event for this property ID 
						try:
							oldWinEvents=e.getWinEventsForAutomationEvent(eventId,propertyId)
						except IndexError:
							# comtypes does not seem to correctly handle a returned empty SAFEARRAY, raising IndexError
							oldWinEvents=None
						if oldWinEvents:
							# As winEvents were mapped, replace them with an empty list
							e.setWinEventsForAutomationEvent(eventId,propertyId,[])
							entryChanged = True
				if entryChanged:
					# Changes to an entry are not automatically picked up.
					# Therefore remove the entry and re-insert it.
					pfm.removeEntry(index)
					pfm.insertEntry(index,e)
			if isUIA8:
				# #8009: use appropriate interface based on highest supported interface.
				# #8338: made easier by traversing interfaces supported on Windows 8 and later in reverse.
				for interface in reversed(CUIAutomation8._com_interfaces_):
					try:
						self.clientObject=self.clientObject.QueryInterface(interface)
						break
					except COMError:
						pass
				# Windows 10 RS5 provides new performance features for UI Automation including event coalescing and connection recovery. 
				# Enable all of these where available.
				if isinstance(self.clientObject,IUIAutomation6):
					self.clientObject.CoalesceEvents=CoalesceEventsOptions_Enabled
					self.clientObject.ConnectionRecoveryBehavior=ConnectionRecoveryBehaviorOptions_Enabled
			log.info("UIAutomation: %s"%self.clientObject.__class__.__mro__[1].__name__)
			self.windowTreeWalker=self.clientObject.createTreeWalker(self.clientObject.CreateNotCondition(self.clientObject.CreatePropertyCondition(UIA_NativeWindowHandlePropertyId,0)))
			self.windowCacheRequest=self.clientObject.CreateCacheRequest()
			self.windowCacheRequest.AddProperty(UIA_NativeWindowHandlePropertyId)
			self.UIAWindowHandleCache={}
			self.baseTreeWalker=self.clientObject.RawViewWalker
			self.baseCacheRequest=self.windowCacheRequest.Clone()
			for propertyId in (UIA_FrameworkIdPropertyId,UIA_AutomationIdPropertyId,UIA_ClassNamePropertyId,UIA_ControlTypePropertyId,UIA_ProviderDescriptionPropertyId,UIA_ProcessIdPropertyId,UIA_IsTextPatternAvailablePropertyId,UIA_IsContentElementPropertyId,UIA_IsControlElementPropertyId):
				self.baseCacheRequest.addProperty(propertyId)
			self.baseCacheRequest.addPattern(UIA_TextPatternId)
			self.rootElement=self.clientObject.getRootElementBuildCache(self.baseCacheRequest)
			self.reservedNotSupportedValue=self.clientObject.ReservedNotSupportedValue
			self.ReservedMixedAttributeValue=self.clientObject.ReservedMixedAttributeValue
			if config.conf['UIA']['selectiveEventRegistration']:
				self._createLocalEventHandlerGroup()
			self._registerGlobalEventHandlers()
		except Exception as e:
			self.MTAThreadInitException=e
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

	def _registerGlobalEventHandlers(self):
		self.clientObject.AddFocusChangedEventHandler(self.baseCacheRequest, self)
		if isinstance(self.clientObject, UIA.IUIAutomation6):
			self.globalEventHandlerGroup = self.clientObject.CreateEventHandlerGroup()
		else:
			self.globalEventHandlerGroup = UIAUtils.FakeEventHandlerGroup(self.clientObject)
		self.globalEventHandlerGroup.AddPropertyChangedEventHandler(
			UIA.TreeScope_Subtree,
			self.baseCacheRequest,
			self,
			*self.clientObject.IntSafeArrayToNativeArray(
				globalEventHandlerGroupUIAPropertyIds
				if config.conf['UIA']['selectiveEventRegistration']
				else UIAPropertyIdsToNVDAEventNames
			)
		)
		for eventId in (
			globalEventHandlerGroupUIAEventIds
			if config.conf['UIA']['selectiveEventRegistration']
			else UIAEventIdsToNVDAEventNames
		):
			self.globalEventHandlerGroup.AddAutomationEventHandler(
				eventId,
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				self
			)
		# #7984: add support for notification event (IUIAutomation5, part of Windows 10 build 16299 and later).
		if isinstance(self.clientObject, UIA.IUIAutomation5):
			self.globalEventHandlerGroup.AddNotificationEventHandler(
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				self
			)
		if isinstance(self.clientObject, UIA.IUIAutomation6):
			self.globalEventHandlerGroup.AddActiveTextPositionChangedEventHandler(
				UIA.TreeScope_Subtree,
				self.baseCacheRequest,
				self
			)
		self.addEventHandlerGroup(self.rootElement, self.globalEventHandlerGroup)

	def _createLocalEventHandlerGroup(self):
		if isinstance(self.clientObject, UIA.IUIAutomation6):
			self.localEventHandlerGroup = self.clientObject.CreateEventHandlerGroup()
		else:
			self.localEventHandlerGroup = UIAUtils.FakeEventHandlerGroup(self.clientObject)
		self.localEventHandlerGroup.AddPropertyChangedEventHandler(
			UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
			self.baseCacheRequest,
			self,
			*self.clientObject.IntSafeArrayToNativeArray(localEventHandlerGroupUIAPropertyIds)
		)
		for eventId in localEventHandlerGroupUIAEventIds:
			self.localEventHandlerGroup.AddAutomationEventHandler(
				eventId,
				UIA.TreeScope_Ancestors | UIA.TreeScope_Element,
				self.baseCacheRequest,
				self
			)

	def addEventHandlerGroup(self, element, eventHandlerGroup):
		if isinstance(eventHandlerGroup, UIA.IUIAutomationEventHandlerGroup):
			self.clientObject.AddEventHandlerGroup(element, eventHandlerGroup)
		elif isinstance(eventHandlerGroup, UIAUtils.FakeEventHandlerGroup):
			eventHandlerGroup.registerToClientObject(element)
		else:
			raise NotImplementedError

	def removeEventHandlerGroup(self, element, eventHandlerGroup):
		if isinstance(eventHandlerGroup, UIA.IUIAutomationEventHandlerGroup):
			self.clientObject.RemoveEventHandlerGroup(element, eventHandlerGroup)
		elif isinstance(eventHandlerGroup, UIAUtils.FakeEventHandlerGroup):
			eventHandlerGroup.unregisterFromClientObject(element)
		else:
			raise NotImplementedError

	def addLocalEventHandlerGroupToElement(self, element, isFocus=False):
		if not self.localEventHandlerGroup or element in self._localEventHandlerGroupElements:
			return

		def func():
			if isFocus:
				try:
					isStillFocus = self.clientObject.CompareElements(self.clientObject.GetFocusedElement(), element)
				except COMError:
					isStillFocus = False
				if not isStillFocus:
					return
			try:
				self.addEventHandlerGroup(element, self.localEventHandlerGroup)
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

	def IUIAutomationEventHandler_HandleAutomationEvent(self,sender,eventID):
		if not self.MTAThreadInitEvent.isSet():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandleAutomationEvent: event received while not fully initialized")
			return
		if eventID==UIA_MenuOpenedEventId and eventHandler.isPendingEvents("gainFocus"):
			# We don't need the menuOpened event if focus has been fired,
			# as focus should be more correct.
			if _isDebug():
				log.debug("HandleAutomationEvent: Ignored MenuOpenedEvent while focus event pending")
			return
		NVDAEventName=UIAEventIdsToNVDAEventNames.get(eventID,None)
		if not NVDAEventName:
			if _isDebug():
				log.debugWarning(f"HandleAutomationEvent: Don't know how to handle event {eventID}")
			return
		focus = api.getFocusObject()
		import NVDAObjects.UIA
		if (
			isinstance(focus, NVDAObjects.UIA.UIA)
			and self.clientObject.compareElements(focus.UIAElement, sender)
		):
			pass
		elif not self.isNativeUIAElement(sender):
			if _isDebug():
				log.debug(
					f"HandleAutomationEvent: Ignoring event {NVDAEventName} for non native element"
				)
			return
		window = self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent(NVDAEventName, windowHandle=window):
			if _isDebug():
				log.debug(
					f"HandleAutomationEvent: Ignoring event {NVDAEventName} for shouldAcceptEvent=False"
				)
			return
		try:
			obj = NVDAObjects.UIA.UIA(UIAElement=sender)
		except Exception:
			if _isDebug():
				log.debugWarning(
					f"HandleAutomationEvent: Exception while creating object for event {NVDAEventName}",
					exc_info=True
				)
			return
		if (
			not obj
			or (NVDAEventName=="gainFocus" and not obj.shouldAllowUIAFocusEvent)
			or (NVDAEventName=="liveRegionChange" and not obj._shouldAllowUIALiveRegionChangeEvent)
		):
			if _isDebug():
				log.debug(
					"HandleAutomationEvent: "
					f"Ignoring event {NVDAEventName} because no object or ignored by object itself"
				)
			return
		if obj==focus:
			obj=focus
		eventHandler.queueEvent(NVDAEventName,obj)

	# The last UIAElement that received a UIA focus event
	# This is updated no matter if this is a native element, the window is UIA blacklisted by NVDA, or  the element is proxied from MSAA 
	lastFocusedUIAElement=None

	def IUIAutomationFocusChangedEventHandler_HandleFocusChangedEvent(self,sender):
		if not self.MTAThreadInitEvent.isSet():
			# UIAHandler hasn't finished initialising yet, so just ignore this event.
			if _isDebug():
				log.debug("HandleFocusChangedEvent: event received while not fully initialized")
			return
		self.lastFocusedUIAElement = sender
		if not self.isNativeUIAElement(sender):
			if _isDebug():
				log.debug("HandleFocusChangedEvent: Ignoring for non native element")
			return
		import NVDAObjects.UIA
		if isinstance(eventHandler.lastQueuedFocusObject,NVDAObjects.UIA.UIA):
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
						log.debugWarning("HandleFocusChangedEvent: Ignoring duplicate focus event")
					return
			except COMError:
				if _isDebug():
					log.debugWarning(
						"HandleFocusChangedEvent: Couldn't check for duplicate focus event",
						exc_info=True
					)
		window = self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent("gainFocus", windowHandle=window):
			if _isDebug():
				log.debug("HandleFocusChangedEvent: Ignoring for shouldAcceptEvent=False")
			return
		try:
			obj = NVDAObjects.UIA.UIA(UIAElement=sender)
		except Exception:
			if _isDebug():
				log.debugWarning(
					"HandleFocusChangedEvent: Exception while creating object",
					exc_info=True
				)
			return
		if not obj or not obj.shouldAllowUIAFocusEvent:
			if _isDebug():
				log.debug(
					"HandleFocusChangedEvent: Ignoring because no object or ignored by object itself"
				)
			return
		eventHandler.queueEvent("gainFocus",obj)

	def IUIAutomationPropertyChangedEventHandler_HandlePropertyChangedEvent(self,sender,propertyId,newValue):
		# #3867: For now manually force this VARIANT type to empty to get around a nasty double free in comtypes/ctypes.
		# We also don't use the value in this callback.
		newValue.vt=VT_EMPTY
		if not self.MTAThreadInitEvent.isSet():
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
				return
		NVDAEventName=UIAPropertyIdsToNVDAEventNames.get(propertyId,None)
		if not NVDAEventName:
			if _isDebug():
				log.debugWarning(f"HandlePropertyChangedEvent: Don't know how to handle property {propertyId}")
			return
		focus = api.getFocusObject()
		import NVDAObjects.UIA
		if (
			isinstance(focus, NVDAObjects.UIA.UIA)
			and self.clientObject.compareElements(focus.UIAElement, sender)
		):
			pass
		elif not self.isNativeUIAElement(sender):
			if _isDebug():
				log.debug(
					f"HandlePropertyChangedEvent: Ignoring event {NVDAEventName} for non native element"
				)
			return
		window = self.getNearestWindowHandle(sender)
		if window and not eventHandler.shouldAcceptEvent(NVDAEventName, windowHandle=window):
			if _isDebug():
				log.debug(
					f"HandlePropertyChangedEvent: Ignoring event {NVDAEventName} for shouldAcceptEvent=False"
				)
			return
		try:
			obj = NVDAObjects.UIA.UIA(UIAElement=sender)
		except Exception:
			if _isDebug():
				log.debugWarning(
					f"HandlePropertyChangedEvent: Exception while creating object for event {NVDAEventName}",
					exc_info=True
				)
			return
		if not obj:
			if _isDebug():
				log.debug(f"HandlePropertyChangedEvent: Ignoring event {NVDAEventName} because no object")
			return
		if obj==focus:
			obj=focus
		eventHandler.queueEvent(NVDAEventName,obj)

	def IUIAutomationNotificationEventHandler_HandleNotificationEvent(
			self,
			sender,
			NotificationKind,
			NotificationProcessing,
			displayString,
			activityId
	):
		if not self.MTAThreadInitEvent.isSet():
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
					exc_info=True
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
					f"activityId={activityId}"
				)
			return
		eventHandler.queueEvent("UIA_notification",obj, notificationKind=NotificationKind, notificationProcessing=NotificationProcessing, displayString=displayString, activityId=activityId)

	def IUIAutomationActiveTextPositionChangedEventHandler_HandleActiveTextPositionChangedEvent(
			self,
			sender,
			textRange
	):
		if not self.MTAThreadInitEvent.isSet():
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
					exc_info=True
				)
			return
		if not obj:
			if _isDebug():
				log.debug(
					"HandleActiveTextPositionchangedEvent: Ignoring because no object: "
				)
			return
		eventHandler.queueEvent("UIA_activeTextPositionChanged", obj, textRange=textRange)

	def _isBadUIAWindowClassName(self, windowClass):
		"Given a windowClassName, returns True if this is a known problematic UIA implementation."
		# #7497: Windows 10 Fall Creators Update has an incomplete UIA
		# implementation for console windows, therefore for now we should
		# ignore it.
		# It does not implement caret/selection, and probably has no new text
		# events.
		if windowClass == "ConsoleWindowClass" and config.conf['UIA']['winConsoleImplementation'] != "UIA":
			return True
		return windowClass in badUIAWindowClassNames

	def _isUIAWindowHelper(self,hwnd):
		# UIA in NVDA's process freezes in Windows 7 and below
		processID=winUser.getWindowThreadProcessID(hwnd)[0]
		if windll.kernel32.GetCurrentProcessId()==processID:
			return False
		import NVDAObjects.window
		windowClass=NVDAObjects.window.Window.normalizeWindowClassName(winUser.getClassName(hwnd))
		# For certain window classes, we always want to use UIA.
		if windowClass in goodUIAWindowClassNames:
			return True
		# allow the appModule for the window to also choose if this window is good
		# An appModule should be able to override bad UIA class names as prescribed by core
		appModule=appModuleHandler.getAppModuleFromProcessID(processID)
		if appModule and appModule.isGoodUIAWindow(hwnd):
			return True
		# There are certain window classes that just had bad UIA implementations
		if self._isBadUIAWindowClassName(windowClass):
			return False
		# allow the appModule for the window to also choose if this window is bad
		if appModule and appModule.isBadUIAWindow(hwnd):
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
			isOfficeApp = appModule.productName.startswith(("Microsoft Office", "Microsoft Outlook"))
			isOffice2013OrOlder = int(appModule.productVersion.split(".")[0]) < 16
			if isOfficeApp and isOffice2013OrOlder:
				parentHwnd = winUser.getAncestor(hwnd, winUser.GA_PARENT)
				while parentHwnd:
					if winUser.getClassName(parentHwnd) in ("Net UI Tool Window", "MsoCommandBar",):
						return False
					parentHwnd = winUser.getAncestor(parentHwnd, winUser.GA_PARENT)
		# Ask the window if it supports UIA natively
		res=windll.UIAutomationCore.UiaHasServerSideProvider(hwnd)
		if res:
			# The window does support UIA natively, but MS Word documents now
			# have a fairly usable UI Automation implementation.
			# However, builds of MS Office 2016 before build 9000 or so had bugs which
			# we cannot work around.
			# And even current builds of Office 2016 are still missing enough info from
			# UIA that it is still impossible to switch to UIA completely.
			# Therefore, if we can inject in-process, refuse to use UIA and instead
			# fall back to the MS Word object model.
			canUseOlderInProcessApproach = bool(appModule.helperLocalBindingHandle)
			if (
				# An MS Word document window 
				windowClass=="_WwG" 
				# Disabling is only useful if we can inject in-process (and use our older code)
				and canUseOlderInProcessApproach
				# Allow the user to explicitly force UIA support for MS Word documents
				# no matter the Office version
				and not config.conf['UIA']['useInMSWordWhenAvailable']
			):
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
				and not config.conf['UIA']['useInMSExcelWhenAvailable']
			):
				return False
			# Unless explicitly allowed, all Chromium implementations (including Edge) should not be UIA,
			# As their IA2 implementation is still better at the moment.
			elif (
				windowClass == "Chrome_RenderWidgetHostHWND"
				and (
					AllowUiaInChromium.getConfig() == AllowUiaInChromium.NO
					# Disabling is only useful if we can inject in-process (and use our older code)
					or (
						canUseOlderInProcessApproach
						and AllowUiaInChromium.getConfig() != AllowUiaInChromium.YES  # Users can prefer to use UIA
					)
				)
			):
				return False
		return bool(res)

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
			processID=UIAElement.cachedProcessID
		except COMError:
			return None
		appModule=appModuleHandler.getAppModuleFromProcessID(processID)
		# WDAG (Windows Defender application Guard) UIA elements should be treated as being from a remote machine, and therefore their window handles are completely invalid on this machine.
		# Therefore, jump all the way up to the root of the WDAG process and use that window handle as it is local to this machine.
		if appModule.appName==WDAG_PROCESS_NAME:
			condition=UIAUtils.createUIAMultiPropertyCondition({UIA_ClassNamePropertyId:[u'ApplicationFrameWindow',u'CabinetWClass']})
			walker=self.clientObject.createTreeWalker(condition)
		else:
			# Not WDAG, just walk up to the nearest valid windowHandle
			walker=self.windowTreeWalker
		try:
			new=walker.NormalizeElementBuildCache(UIAElement,self.windowCacheRequest)
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


def _isDebug():
	return config.conf["debugLog"]["UIA"]
