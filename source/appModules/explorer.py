#appModules/explorer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows Explorer (aka Windows shell).
Provides workarounds for controls such as identifying Start button, notification area and others.
"""

from comtypes import COMError
import time
import appModuleHandler
import controlTypes
import winUser
import api
import speech
import eventHandler
import mouseHandler
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import sysListView32, IAccessible, List
from NVDAObjects.UIA import UIA

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
class SysListView32MenuItem(sysListView32.ListItemWithoutColumnSupport):

	# #474: When focus moves to these items, an extra focus is fired on the parent
	# However NVDA redirects it to the real focus.
	# But this means double focus events on the item, so filter the second one out
	def _get_shouldAllowIAccessibleFocusEvent(self):
		res=super(SysListView32MenuItem,self).shouldAllowIAccessibleFocusEvent
		if not res:
			return False
		focus=eventHandler.lastQueuedFocusObject
		if type(focus)!=type(self) or (self.event_windowHandle,self.event_objectID,self.event_childID)!=(focus.event_windowHandle,focus.event_objectID,focus.event_childID):
			return True
		return False


class ClassicStartMenu(Window):
	# Override the name, as Windows names this the "Application" menu contrary to all documentation.
	# Translators: The title of Start menu/screen in your language (only the word start).
	name = _("Start")

	def event_gainFocus(self):
		# In Windows XP, the Start button will get focus first, so silence this.
		speech.cancelSpeech()
		super(ClassicStartMenu, self).event_gainFocus()


class NotificationArea(IAccessible):
	"""The Windows notification area, a.k.a. system tray.
	"""

	def event_gainFocus(self):
		if mouseHandler.lastMouseEventTime < time.time() - 0.2:
			# This focus change was not caused by a mouse event.
			# If the mouse is on another toolbar control, the notification area toolbar will rudely
			# bounce the focus back to the object under the mouse after a brief pause.
			# Moving the mouse to the focus object isn't a good solution because
			# sometimes, the focus can't be moved away from the object under the mouse.
			# Therefore, move the mouse out of the way.
			winUser.setCursorPos(0, 0)

		if self.role == controlTypes.ROLE_TOOLBAR:
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


class GridTileElement(UIA):

	role=controlTypes.ROLE_TABLECELL

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
	role=controlTypes.ROLE_TABLECELL
	description=None


class GridGroup(UIA):
	"""A group in the Windows 8 Start Menu.
	"""
	presentationType=UIA.presType_content

	# Normally the name is the first tile which is rather redundant
	# However some groups have custom header text which should be read instead
	def _get_name(self):
		child=self.firstChild
		if isinstance(child,UIA):
			try:
				automationID=child.UIAElement.currentAutomationID
			except COMError:
				automationID=None
			if automationID=="GridListGroupHeader":
				return child.name


class ImmersiveLauncher(UIA):
	# When the Windows 8 start screen opens, focus correctly goes to the first tile, but then incorrectly back to the root of the window.
	# Ignore focus events on this object.
	shouldAllowUIAFocusEvent=False


class StartButton(IAccessible):
	"""For Windows 8.1 and 10 Start buttons to be recognized as proper buttons and to suppress selection announcement."""

	role = controlTypes.ROLE_BUTTON

	def _get_states(self):
		# #5178: Selection announcement should be suppressed.
		# Borrowed from Mozilla objects in NVDAObjects/IAccessible/Mozilla.py.
		states = super(StartButton, self).states
		states.discard(controlTypes.STATE_SELECTED)
		return states
		
CHAR_LTR_MARK = u'\u200E'
CHAR_RTL_MARK = u'\u200F'
class UIProperty(UIA):
	#Used for columns in Windows Explorer Details view.
	#These can contain dates that include unwanted left-to-right and right-to-left indicator characters.
	
	def _get_value(self):
		value = super(UIProperty, self).value
		return value.replace(CHAR_LTR_MARK,'').replace(CHAR_RTL_MARK,'')


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		role = obj.role

		if windowClass in ("Search Box","UniversalSearchBand") and role==controlTypes.ROLE_PANE and isinstance(obj,IAccessible):
			clsList.insert(0,SearchBoxClient)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		if windowClass == "ToolbarWindow32":
			if role == controlTypes.ROLE_POPUPMENU:
				parent = obj.parent
				if parent and parent.windowClassName == "SysPager" and obj.windowStyle & 0x80:
					clsList.insert(0, ClassicStartMenu)
			else:
				# Check whether this is the notification area, a.k.a. system tray.
				if isinstance(obj.parent, ClassicStartMenu):
					return # This can't be a notification area
				try:
					# The toolbar's immediate parent is its window object, so we need to go one further.
					toolbarParent = obj.parent.parent
					if role != controlTypes.ROLE_TOOLBAR:
						# Toolbar item.
						toolbarParent = toolbarParent.parent
				except AttributeError:
					toolbarParent = None
				if toolbarParent and toolbarParent.windowClassName == "SysPager":
					clsList.insert(0, NotificationArea)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		if windowClass == "SysListView32" and role == controlTypes.ROLE_MENUITEM:
			clsList.insert(0, SysListView32MenuItem)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		# #5178: Start button in Windows 8.1 and 10 should not have been a list in the first place.
		if windowClass == "Start" and role in (controlTypes.ROLE_LIST, controlTypes.ROLE_BUTTON):
			if role == controlTypes.ROLE_LIST:
				clsList.remove(List)
			clsList.insert(0, StartButton)
			return # Optimization: return early to avoid comparing class names and roles that will never match.

		if isinstance(obj, UIA):
			uiaClassName = obj.UIAElement.cachedClassName
			if uiaClassName == "GridTileElement":
				clsList.insert(0, GridTileElement)
			elif uiaClassName == "GridListTileElement":
				clsList.insert(0, GridListTileElement)
			elif uiaClassName == "GridGroup":
				clsList.insert(0, GridGroup)
			elif uiaClassName == "ImmersiveLauncher" and role == controlTypes.ROLE_PANE:
				clsList.insert(0, ImmersiveLauncher)
			elif uiaClassName == "ListViewItem" and obj.UIAElement.cachedAutomationId.startswith('Suggestion_'):
				clsList.insert(0, SuggestionListItem)
			elif uiaClassName == "MultitaskingViewFrame" and role == controlTypes.ROLE_WINDOW:
				clsList.insert(0, MultitaskingViewFrameWindow)
			elif windowClass == "MultitaskingViewFrame" and role == controlTypes.ROLE_LISTITEM:
				# Use windowClass here as there is no uiaClassName for these list items.
				clsList.insert(0, MultitaskingViewFrameListItem)
			elif uiaClassName == "UIProperty" and role == controlTypes.ROLE_EDITABLETEXT:
				clsList.insert(0, UIProperty)

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		role = obj.role

		if windowClass == "ToolbarWindow32" and role == controlTypes.ROLE_POPUPMENU:
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

		if windowClass == "DV2ControlHost" and role == controlTypes.ROLE_PANE:
			# Windows Vista/7 start menu.
			obj.presentationType=obj.presType_content
			obj.isPresentableFocusAncestor = True
			# In Windows 7, the description of this pane is extremely verbose help text, so nuke it.
			obj.description = None
			return

		# The Address bar is embedded inside a progressbar, how strange.
		# Lets hide that
		if windowClass=="msctls_progress32" and winUser.getClassName(winUser.getAncestor(obj.windowHandle,winUser.GA_PARENT))=="Address Band Root":
			obj.presentationType=obj.presType_layout

	def event_gainFocus(self, obj, nextHandler):
		wClass = obj.windowClassName
		if wClass == "ToolbarWindow32" and obj.role == controlTypes.ROLE_MENUITEM and obj.parent.role == controlTypes.ROLE_MENUBAR and eventHandler.isPendingEvents("gainFocus"):
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

		if wClass == "WorkerW" and obj.role == controlTypes.ROLE_PANE and obj.name is None:
			# #6671: Never allow WorkerW thread to send gain focus event, as it causes 'pane" to be announced when minimizing windows or moving to desktop.
			return

		nextHandler()
