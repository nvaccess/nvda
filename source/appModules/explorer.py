# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Joseph Lee, Łukasz Golonka, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows Explorer (aka Windows shell and renamed to File Explorer in Windows 8).
Provides workarounds for controls such as identifying Start button, notification area and others.
"""

from comtypes import COMError
import time
import appModuleHandler
import controlTypes
import winUser
import winVersion
import api
import speech
import eventHandler
import mouseHandler
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import IAccessible, List
from NVDAObjects.UIA import UIA
from NVDAObjects.behaviors import ToolTip
from NVDAObjects.window.edit import RichEdit50, EditTextInfo
import config


# Suppress incorrect Win 10 Task switching window focus
class MultitaskingViewFrameWindow(UIA):
	shouldAllowUIAFocusEvent=False


# Suppress focus ancestry for task switching list items if alt is held down (alt+tab)
class MultitaskingViewFrameListItem(UIA):

	def _get_container(self):
		if winUser.getAsyncKeyState(winUser.VK_MENU)&32768:
			return api.getDesktopObject()
		else:
			return super(MultitaskingViewFrameListItem,self).container


# Support for Win8 start screen search suggestions.
class SuggestionListItem(UIA):

	def event_UIA_elementSelected(self):
		speech.cancelSpeech()
		api.setNavigatorObject(self, isFocus=True)
		self.reportFocus()
		super(SuggestionListItem,self).event_UIA_elementSelected()


# Windows 8 hack: Class to disable incorrect focus on windows 8 search box (containing the already correctly focused edit field)
class SearchBoxClient(IAccessible):
	shouldAllowIAccessibleFocusEvent=False


# Class for menu items  for Windows Places and Frequently used Programs (in start menu)
# Also used for desktop items
class SysListView32EmittingDuplicateFocusEvents(IAccessible):

	# #474: When focus moves to these items, an extra focus is fired on the parent
	# However NVDA redirects it to the real focus.
	# But this means double focus events on the item, so filter the second one out
	# #2988: Also seen when coming back to the Windows 7 desktop from different applications.
	def _get_shouldAllowIAccessibleFocusEvent(self):
		res = super().shouldAllowIAccessibleFocusEvent
		if not res:
			return False
		focus = eventHandler.lastQueuedFocusObject
		if type(focus)!=type(self) or (self.event_windowHandle,self.event_objectID,self.event_childID)!=(focus.event_windowHandle,focus.event_objectID,focus.event_childID):
			return True
		return False

class NotificationArea(IAccessible):
	"""The Windows notification area, a.k.a. system tray.
	"""
	lastKnownLocation = None

	def event_gainFocus(self):
		NotificationArea.lastKnownLocation = self.location
		if mouseHandler.lastMouseEventTime < time.time() - 0.2:
			# This focus change was not caused by a mouse event.
			# If the mouse is on another systray control, the notification area toolbar will rudely
			# bounce the focus back to the object under the mouse after a brief pause.
			# Moving the mouse to the focus object isn't a good solution because
			# sometimes, the focus can't be moved away from the object under the mouse.
			# Therefore, move the mouse out of the way.
			if self.location:
				systrayLeft, systrayTop, systrayWidth, systrayHeight = self.location
				mouseLeft, mouseTop = winUser.getCursorPos()
				if (
					systrayLeft <= mouseLeft <= systrayLeft + systrayWidth
					and systrayTop <= mouseTop <= systrayTop + systrayHeight
				):
					winUser.setCursorPos(0, 0)

		if self.role == controlTypes.Role.TOOLBAR:
			# Sometimes, the toolbar itself receives the focus instead of the focused child.
			# However, the focused child still has the focused state.
			for child in self.children:
				if child.hasFocus:
					# Redirect the focus to the focused child.
					eventHandler.executeEvent("gainFocus", child)
					return
			# We've really landed on the toolbar itself.
			# This was probably caused by moving the mouse out of the way in a previous focus event.
			# This previous focus event is no longer useful, so cancel speech.
			speech.cancelSpeech()

		if eventHandler.isPendingEvents("gainFocus"):
			return
		super(NotificationArea, self).event_gainFocus()


class ExplorerToolTip(ToolTip):

	def shouldReport(self):
		# Avoid reporting systray tool-tips if their text equals the focused systray icon name (#6656)

		# Don't bother checking if reporting of tool-tips is disabled
		if not config.conf["presentation"]["reportTooltips"]:
			return False

		focus = api.getFocusObject()

		# Report if either
		#  - the mouse has just moved
		#  - the focus is not in the systray
		#  - we do not know (yet) where the systray is located
		if (
			mouseHandler.lastMouseEventTime >= time.time() - 0.2
			or not isinstance(focus, NotificationArea)
			or NotificationArea.lastKnownLocation is None
		):
			return True

		# Report if the mouse is indeed located in the systray
		systrayLeft, systrayTop, systrayWidth, systrayHeight = NotificationArea.lastKnownLocation
		mouseLeft, mouseTop = winUser.getCursorPos()
		if (
			systrayLeft <= mouseLeft <= systrayLeft + systrayWidth
			and systrayTop <= mouseTop <= systrayTop + systrayHeight
		):
			return True

		# Report is the next are different
		if focus.name != self.name:
			return True

		# Do not report otherwise
		return False

	def event_show(self):
		if self.shouldReport():
			super().event_show()


class GridTileElement(UIA):

	role=controlTypes.Role.TABLECELL

	def _get_description(self):
		name=self.name
		descriptionStrings=[]
		for child in self.children:
			description=child.basicText
			if not description or description==name: continue
			descriptionStrings.append(description)
		return " ".join(descriptionStrings)
		return description


class GridListTileElement(UIA):
	role=controlTypes.Role.TABLECELL
	description=None


class GridGroup(UIA):
	"""A group in the Windows 8 Start Menu.
	"""
	presentationType=UIA.presType_content

	# Normally the name is the first tile which is rather redundant
	# However some groups have custom header text which should be read instead
	def _get_name(self):
		child = self.firstChild
		if isinstance(child, UIA):
			if child.UIAAutomationId == "GridListGroupHeader":
				return child.name


class ImmersiveLauncher(UIA):
	# When the Windows 8 start screen opens, focus correctly goes to the first tile, but then incorrectly back to the root of the window.
	# Ignore focus events on this object.
	shouldAllowUIAFocusEvent=False


class StartButton(IAccessible):
	"""For Windows 8.1 and 10 Start buttons to be recognized as proper buttons and to suppress selection announcement."""

	role = controlTypes.Role.BUTTON

	def _get_states(self):
		# #5178: Selection announcement should be suppressed.
		# Borrowed from Mozilla objects in NVDAObjects/IAccessible/Mozilla.py.
		states = super(StartButton, self).states
		states.discard(controlTypes.State.SELECTED)
		return states
		
CHAR_LTR_MARK = u'\u200E'
CHAR_RTL_MARK = u'\u200F'
class UIProperty(UIA):
	#Used for columns in Windows Explorer Details view.
	#These can contain dates that include unwanted left-to-right and right-to-left indicator characters.
	
	def _get_value(self):
		value = super(UIProperty, self).value
		if value is None:
			return value
		return value.replace(CHAR_LTR_MARK,'').replace(CHAR_RTL_MARK,'')

class ReadOnlyEditBox(IAccessible):
#Used for read-only edit boxes in a properties window.
#These can contain dates that include unwanted left-to-right and right-to-left indicator characters.

	def _get_windowText(self):
		windowText = super(ReadOnlyEditBox, self).windowText
		if windowText is not None:
			return windowText.replace(CHAR_LTR_MARK,'').replace(CHAR_RTL_MARK,'')
		return windowText


class MetadataEditField(RichEdit50):
	""" Used for metadata edit fields in Windows Explorer in Windows 7.
	By default these fields would use ITextDocumentTextInfo ,
	but to avoid Windows Explorer crashes we need to use EditTextInfo here. """
	@classmethod
	def _get_TextInfo(cls):
		if winVersion.getWinVer() <= winVersion.WIN7_SP1:
			cls.TextInfo = EditTextInfo
		else:
			cls.TextInfo = super().TextInfo
		return cls.TextInfo


class WorkerW(IAccessible):
	def event_gainFocus(self):
		# #6671: Normally we do not allow WorkerW thread to send gain focus event,
		# as it causes 'pane" to be announced when minimizing windows or moving to desktop.
		# However when closing Windows 7 Start Menu in some  cases
		# focus lands  on it instead of the focused desktop item.
		# Simply ignore the event if running on anything other than Win 7.
		if winVersion.getWinVer() > winVersion.WIN7_SP1:
			return
		if eventHandler.isPendingEvents("gainFocus"):
			return
		if self.simpleFirstChild:
			# If focus is not going to be moved autotically
			# we need to forcefully move it to the focused desktop item.
			# As we are interested in the first focusable object below the pane use simpleFirstChild.
			self.simpleFirstChild.setFocus()
			return
		super().event_gainFocus()


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		role = obj.role

		if windowClass in ("Search Box","UniversalSearchBand") and role==controlTypes.Role.PANE and isinstance(obj,IAccessible):
			clsList.insert(0,SearchBoxClient)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		if windowClass == "ToolbarWindow32":
			if role != controlTypes.Role.POPUPMENU:
				try:
					# The toolbar's immediate parent is its window object, so we need to go one further.
					toolbarParent = obj.parent.parent
					if role != controlTypes.Role.TOOLBAR:
						# Toolbar item.
						toolbarParent = toolbarParent.parent
				except AttributeError:
					toolbarParent = None
				if toolbarParent and toolbarParent.windowClassName == "SysPager":
					clsList.insert(0, NotificationArea)
			return

		if obj.role == controlTypes.Role.TOOLTIP:
			clsList.insert(0, ExplorerToolTip)
			return

		if windowClass == "Edit" and controlTypes.State.READONLY in obj.states:
			clsList.insert(0, ReadOnlyEditBox)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		if windowClass == "SysListView32":
			if(
				role == controlTypes.Role.MENUITEM
				or(
					role == controlTypes.Role.LISTITEM
					and obj.simpleParent
					and obj.simpleParent.simpleParent
					and obj.simpleParent.simpleParent == api.getDesktopObject()
				)
			):
				clsList.insert(0, SysListView32EmittingDuplicateFocusEvents)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		# #5178: Start button in Windows 8.1 and 10 should not have been a list in the first place.
		if windowClass == "Start" and role in (controlTypes.Role.LIST, controlTypes.Role.BUTTON):
			if role == controlTypes.Role.LIST:
				clsList.remove(List)
			clsList.insert(0, StartButton)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		if windowClass == 'RICHEDIT50W' and obj.windowControlID == 256:
			clsList.insert(0, MetadataEditField)
			return  # Optimization: return early to avoid comparing class names and roles that will never match.

		if windowClass == "WorkerW" and role == controlTypes.Role.PANE and obj.name is None:
			clsList.insert(0, WorkerW)
			return  # Optimization: return early to avoid comparing class names and roles that will never match.

		if isinstance(obj, UIA):
			uiaClassName = obj.UIAElement.cachedClassName
			if uiaClassName == "GridTileElement":
				clsList.insert(0, GridTileElement)
			elif uiaClassName == "GridListTileElement":
				clsList.insert(0, GridListTileElement)
			elif uiaClassName == "GridGroup":
				clsList.insert(0, GridGroup)
			elif uiaClassName == "ImmersiveLauncher" and role == controlTypes.Role.PANE:
				clsList.insert(0, ImmersiveLauncher)
			elif uiaClassName == "ListViewItem" and obj.UIAAutomationId.startswith('Suggestion_'):
				clsList.insert(0, SuggestionListItem)
			# Multitasking view frame window
			elif (
				# Windows 10 and earlier
				(uiaClassName == "MultitaskingViewFrame" and role == controlTypes.Role.WINDOW)
				# Windows 11 where a pane window receives focus when switching tasks
				or (uiaClassName == "Windows.UI.Input.InputSite.WindowClass" and role == controlTypes.Role.PANE)
			):
				clsList.insert(0, MultitaskingViewFrameWindow)
			# Windows 10 task switch list
			elif role == controlTypes.Role.LISTITEM and (
				# RS4 and below we can match on a window class
				windowClass == "MultitaskingViewFrame" or
				# RS5 and above we must look for a particular UIA automationID on the list
				isinstance(obj.parent, UIA) and obj.parent.UIAAutomationId == "SwitchItemListControl"
			):
				clsList.insert(0, MultitaskingViewFrameListItem)
			elif uiaClassName == "UIProperty" and role == controlTypes.Role.EDITABLETEXT:
				clsList.insert(0, UIProperty)

	def _get_statusBar(self):
		foreground = api.getForegroundObject()
		if not isinstance(foreground, UIA) or not foreground.windowClassName == "CabinetWClass":
			# This is not the file explorer window. Resort to standard behavior.
			raise NotImplementedError
		import UIAHandler
		clientObject = UIAHandler.handler.clientObject
		condition = clientObject.createPropertyCondition(
			UIAHandler.UIA_ControlTypePropertyId,
			UIAHandler.UIA_StatusBarControlTypeId
		)
		walker = clientObject.createTreeWalker(condition)
		try:
			element = walker.getFirstChildElement(foreground.UIAElement)
		except COMError:
			# We could not find the expected object. Resort to standard behavior.
			raise NotImplementedError()
		element = element.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		statusBar = UIA(UIAElement=element)
		return statusBar

	@staticmethod
	def _getStatusBarTextWin7(obj) -> str:
		"""For status bar in Windows 7 Windows Explorer we're interested only in the name of the first child
		the rest are either empty or contain garbage."""
		if obj.firstChild and obj.firstChild.name:
			return obj.firstChild.name
		raise NotImplementedError

	@staticmethod
	def _getStatusBarTextPostWin7(obj) -> str:
		# The expected status bar, as of Windows 10 20H2 at least, contains:
		#  - A grouping with a single static text child presenting the total number of elements
		#  - Optionally, a grouping with a single static text child presenting the number of
		#    selected elements and their total size, missing if no element is selected.
		#  - A grouping with two radio buttons to control the display mode.
		parts = []
		for index, child in enumerate(obj.children):
			if (
				child.role == controlTypes.Role.GROUPING
				and child.childCount == 1
				and child.firstChild.role == controlTypes.Role.STATICTEXT
			):
				parts.append(child.firstChild.name)
			elif (
				child.role == controlTypes.Role.GROUPING
				and child.childCount > 1
				and not any(
					grandChild for grandChild in child.children
					if grandChild.role != controlTypes.Role.RADIOBUTTON
				)
			):
				selected = next(iter(
					grandChild for grandChild in child.children
					if controlTypes.State.CHECKED in grandChild.states
				), None)
				if selected is not None:
					parts.append(" ".join(
						[child.name]
						+ ([selected.name] if selected is not None else [])
					))
			else:
				# Unexpected child, try to retrieve something useful.
				parts.append(" ".join(
					chunk
					for chunk in (child.name, child.value)
					if chunk and isinstance(chunk, str) and not chunk.isspace()
				))
		if not parts:
			# We couldn't retrieve anything. Resort to standard behavior.
			raise NotImplementedError
		return ", ".join(parts)

	def getStatusBarText(self, obj) -> str:
		if obj.windowClassName == "msctls_statusbar32":  # Windows 7
			return self._getStatusBarTextWin7(obj)
		if (
			isinstance(obj, UIA) or obj.UIAElement.cachedClassname == "StatusBarModuleInner"
		):  # Windows 8 or later
			return self._getStatusBarTextPostWin7(obj)
		else:
			# This is not the file explorer status bar. Resort to standard behavior.
			raise NotImplementedError

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		role = obj.role

		if windowClass == "ToolbarWindow32" and role == controlTypes.Role.POPUPMENU:
			parent = obj.parent
			if parent and parent.windowClassName == "SysPager" and not (obj.windowStyle & 0x80):
				# This is the menu for a group of icons on the task bar, which Windows stupidly names "Application".
				obj.name = None
			return

		if windowClass == "#32768":
			# Standard menu.
			parent = obj.parent
			if parent and not parent.parent:
				# Context menu.
				# We don't trust the names that Explorer gives to context menus, so better to have no name at all.
				obj.name = None
			return

		if windowClass == "DV2ControlHost" and role == controlTypes.Role.PANE:
			# Windows 7 start menu.
			obj.presentationType=obj.presType_content
			obj.isPresentableFocusAncestor = True
			# In Windows 7, the description of this pane is extremely verbose help text, so nuke it.
			obj.description = None
			return

		# The Address bar is embedded inside a progressbar, how strange.
		# Lets hide that
		if windowClass=="msctls_progress32" and winUser.getClassName(winUser.getAncestor(obj.windowHandle,winUser.GA_PARENT))=="Address Band Root":
			obj.presentationType=obj.presType_layout
			return

		if windowClass == "DirectUIHWND" and role == controlTypes.Role.LIST:
			# Is this a list containing search results in Windows 7 start menu?
			isWin7SearchResultsList = False
			try:
				if obj.parent and obj.parent.parent:
					parent = obj.parent.parent.parent
					isWin7SearchResultsList = parent is not None and parent.windowClassName == "Desktop Search Open View"
			except AttributeError:
				isWin7SearchResultsList = False
			if isWin7SearchResultsList:
				# Namae of this list is not useful and should be  discarded.
				obj.name = None
				return

	def event_gainFocus(self, obj, nextHandler):
		wClass = obj.windowClassName
		if wClass == "ToolbarWindow32" and obj.role == controlTypes.Role.MENUITEM and obj.parent.role == controlTypes.Role.MENUBAR and eventHandler.isPendingEvents("gainFocus"):
			# When exiting a menu, Explorer fires focus on the top level menu item before it returns to the previous focus.
			# Unfortunately, this focus event always occurs in a subsequent cycle, so the event limiter doesn't eliminate it.
			# Therefore, if there is a pending focus event, don't bother handling this event.
			return

		if wClass in ("ForegroundStaging", "LauncherTipWnd", "ApplicationManager_DesktopShellWindow"):
			# #5116: The Windows 10 Task View fires foreground/focus on this weird invisible window and foreground staging screen before and after it appears.
			# This causes NVDA to report "unknown", so ignore it.
			# We can't do this using shouldAllowIAccessibleFocusEvent because this isn't checked for foreground.
			# #8137: also seen when opening quick link menu (Windows+X) on Windows 8 and later.
			return

		nextHandler()

	def isGoodUIAWindow(self, hwnd):
		currentWinVer = winVersion.getWinVer()
		# #9204: shell raises window open event for emoji panel in build 18305 and later.
		if (
			currentWinVer >= winVersion.WIN10_1903
			and winUser.getClassName(hwnd) == "ApplicationFrameWindow"
		):
			return True
		# #13506: Windows 11 UI elements such as Taskbar should be reclassified as UIA windows,
		# letting NVDA announce shell elements when navigating with mouse and/or touch,
		# notably when interacting with windows labeled "DesktopWindowXamlSource".
		# WORKAROUND UNTIL A PERMANENT FIX IS FOUND ACROSS APPS
		if (
			currentWinVer >= winVersion.WIN11
			# Traverse parents until arriving at the top-level window with the below class names.
			# This is more so for the shell root (first class name), and for others, class name check would work
			# since they are top-level windows for windows shown on screen such as Task View.
			# However, look for the ancestor for consistency.
			and winUser.getClassName(winUser.getAncestor(hwnd, winUser.GA_ROOT)) in (
				# Windows 11 shell UI root, housing various shell elements shown on screen if enabled.
				"Shell_TrayWnd",  # Start, Search, Widgets, other shell elements
				# Top-level window class names from Windows 11 shell features
				"Shell_InputSwitchTopLevelWindow",  # Language switcher
				"XamlExplorerHostIslandWindow",  # Task View and Snap Layouts
			)
		):
			return True
		return False

	def event_UIA_window_windowOpen(self, obj, nextHandler):
		# Send UIA window open event to input app window.
		if isinstance(obj, UIA) and obj.UIAElement.cachedClassName == "ApplicationFrameWindow":
			inputPanelWindow = obj.firstChild
			inputPanelAppName = (
				# 19H2 and earlier
				"windowsinternal_composableshell_experiences_textinput_inputapp",
				# 20H1 and later
				"textinputhost"
			)
			if inputPanelWindow and inputPanelWindow.appModule.appName in inputPanelAppName:
				eventHandler.executeEvent("UIA_window_windowOpen", inputPanelWindow)
				return
		nextHandler()
