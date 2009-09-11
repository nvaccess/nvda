#appModules/explorer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import controlTypes
import api
import speech
import eventHandler
from NVDAObjects.window import Window

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

		if obj.windowClassName == "#32768":
			# Standard menu.
			parent = obj.parent
			if parent and not parent.parent:
				# Context menu.
				# We don't trust the names that Explorer gives to context menus, so better to have no name at all.
				obj.name = None

		if obj.windowClassName == "DV2ControlHost" and obj.role == controlTypes.ROLE_PANE:
			# Windows Vista/7 start menu.
			obj.isPresentableFocusAncestor = True

	def event_gainFocus(self, obj, nextHandler):
		if obj.windowClassName == "ToolbarWindow32" and obj.role == controlTypes.ROLE_MENUITEM and obj.parent.role == controlTypes.ROLE_MENUBAR and eventHandler.isPendingEvents("gainFocus"):
			# When exiting a menu, Explorer fires focus on the top level menu item before it returns to the previous focus.
			# Unfortunately, this focus event always occurs in a subsequent cycle, so the event limiter doesn't eliminate it.
			# Therefore, if there is a pending focus event, don't bother handling this event.
			return
		nextHandler()
