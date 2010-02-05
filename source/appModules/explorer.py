#appModules/explorer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import controlTypes
import winUser
import api
import speech
import eventHandler
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import sysListView32

#Class for menu items  for Windows Places and Frequently used Programs (in start menu)
class SysListView32MenuItem(sysListView32.ListItem):

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
	name = _("Start")

	def event_gainFocus(self):
		# In Windows XP, the Start button will get focus first, so silence this.
		speech.cancelSpeech()
		super(ClassicStartMenu, self).event_gainFocus()

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "ToolbarWindow32" and obj.role == controlTypes.ROLE_POPUPMENU:
			parent = obj.parent
			if parent and parent.windowClassName == "SysPager":
				if obj.windowStyle & 0x80:
					self.overlayCustomNVDAObjectClass(obj,ClassicStartMenu,outerMost=True)
				else:
					# This is the menu for a group of icons on the task bar, which Windows stupidly names "Application".
					obj.name = None
			return

		if obj.windowClassName=="SysListView32" and obj.role==controlTypes.ROLE_MENUITEM:
			self.overlayCustomNVDAObjectClass(obj,SysListView32MenuItem,outerMost=True)

		if obj.windowClassName == "#32768":
			# Standard menu.
			parent = obj.parent
			if parent and not parent.parent:
				# Context menu.
				# We don't trust the names that Explorer gives to context menus, so better to have no name at all.
				obj.name = None

		if obj.windowClassName == "DV2ControlHost" and obj.role == controlTypes.ROLE_PANE:
			# Windows Vista/7 start menu.
			obj.isPresentable=True
			obj.isPresentableFocusAncestor = True
			# In Windows 7, the description of this pane is extremely verbose help text, so nuke it.
			obj.description = None

		#The Address bar is embedded inside a progressbar, how strange.
		#Lets hide that
		if obj.windowClassName=="msctls_progress32" and winUser.getClassName(winUser.getAncestor(obj.windowHandle,winUser.GA_PARENT))=="Address Band Root":
			obj.isPresentable=False

	def event_gainFocus(self, obj, nextHandler):
		if obj.windowClassName == "ToolbarWindow32" and obj.role == controlTypes.ROLE_MENUITEM and obj.parent.role == controlTypes.ROLE_MENUBAR and eventHandler.isPendingEvents("gainFocus"):
			# When exiting a menu, Explorer fires focus on the top level menu item before it returns to the previous focus.
			# Unfortunately, this focus event always occurs in a subsequent cycle, so the event limiter doesn't eliminate it.
			# Therefore, if there is a pending focus event, don't bother handling this event.
			return
		nextHandler()
