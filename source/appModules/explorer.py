#appModules/explorer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

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
from NVDAObjects.IAccessible import sysListView32, IAccessible
from NVDAObjects.UIA import UIA

# Suppress incorrect Win 10 Task switching window focus
class MultitaskingViewFrameWindow(UIA):
	shouldAllowUIAFocusEvent=False

# suppress focus ancestry for task switching list items if alt is held down (alt+tab)
class MultitaskingViewFrameListItem(UIA):

	def _get_container(self):
		if winUser.getAsyncKeyState(winUser.VK_MENU)&32768:
			return api.getDesktopObject()
		else:
			return super(MultitaskingViewFrameListItem,self).container

# support for Win8 start screen search suggestions.
class SuggestionListItem(UIA):

	def event_UIA_elementSelected(self):
		speech.cancelSpeech()
		api.setNavigatorObject(self)
		self.reportFocus()
		super(SuggestionListItem,self).event_UIA_elementSelected()

#win8hack: Class to disable incorrect focus on windows 8 search box (containing the already correctly focused edit field)
class SearchBoxClient(IAccessible):
	shouldAllowIAccessibleFocusEvent=False

#Class for menu items  for Windows Places and Frequently used Programs (in start menu)
class SysListView32MenuItem(sysListView32.ListItemWithoutColumnSupport):

	#When focus moves to these items, an extra focus is fired on the parent
	#However NVDA redirects it to the real focus.
	#But this means double focus events on the item, so filter the second one out
	#Ticket #474
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

	#Normally the name is the first tile which is rather redundant
	#However some groups have custom header text which should be read instead
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
	#When the win8 start screen openes, focus correctly goes to the first tile, but then incorrectly back to the root of the window.
	#Ignore focus events on this object.
	shouldAllowUIAFocusEvent=False

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		role = obj.role

		if windowClass in ("Search Box","UniversalSearchBand") and role==controlTypes.ROLE_PANE and isinstance(obj,IAccessible):
			clsList.insert(0,SearchBoxClient)
			return

		if windowClass == "ToolbarWindow32" and role == controlTypes.ROLE_POPUPMENU:
			parent = obj.parent
			if parent and parent.windowClassName == "SysPager" and obj.windowStyle & 0x80:
				clsList.insert(0, ClassicStartMenu)
			return

		if windowClass == "SysListView32" and role == controlTypes.ROLE_MENUITEM:
			clsList.insert(0, SysListView32MenuItem)
			return

		if windowClass == "ToolbarWindow32":
			# Check whether this is the notification area, a.k.a. system tray.
			if isinstance(obj.parent, ClassicStartMenu):
				return #This can't be a notification area
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
				return

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
			elif uiaClassName=="ListViewItem" and obj.UIAElement.cachedAutomationId.startswith('Suggestion_'):
				clsList.insert(0,SuggestionListItem)
			elif uiaClassName=="MultitaskingViewFrame" and role==controlTypes.ROLE_WINDOW:
				clsList.insert(0,MultitaskingViewFrameWindow)
			elif obj.windowClassName=="MultitaskingViewFrame" and role==controlTypes.ROLE_LISTITEM:
				clsList.insert(0,MultitaskingViewFrameListItem)

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

		#The Address bar is embedded inside a progressbar, how strange.
		#Lets hide that
		if windowClass=="msctls_progress32" and winUser.getClassName(winUser.getAncestor(obj.windowHandle,winUser.GA_PARENT))=="Address Band Root":
			obj.presentationType=obj.presType_layout

	def event_gainFocus(self, obj, nextHandler):
		wClass = obj.windowClassName
		if wClass == "ToolbarWindow32" and obj.role == controlTypes.ROLE_MENUITEM and obj.parent.role == controlTypes.ROLE_MENUBAR and eventHandler.isPendingEvents("gainFocus"):
			# When exiting a menu, Explorer fires focus on the top level menu item before it returns to the previous focus.
			# Unfortunately, this focus event always occurs in a subsequent cycle, so the event limiter doesn't eliminate it.
			# Therefore, if there is a pending focus event, don't bother handling this event.
			return

		if wClass == "ForegroundStaging":
			# #5116: The Windows 10 Task View fires foreground/focus on this weird invisible window before and after it appears.
			# This causes NVDA to report "unknown", so ignore it.
			# We can't do this using shouldAllowIAccessibleFocusEvent because this isn't checked for foreground.
			return

		nextHandler()
