#NVDAObjects/IAccessible/qt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
from comtypes import COMError
import controlTypes
from NVDAObjects.IAccessible import IAccessible
import eventHandler

class Widget(IAccessible):
	IAccessibleFocusEventNeedsFocusedState = False

class Client(IAccessible):

	def event_gainFocus(self):
		if eventHandler.isPendingEvents("gainFocus"):
			return

		# If there is only one child, this is probably a widget container.
		child = self.firstChild
		if child and not child.next:
			# Redirect the focus, since QT doesn't do it properly.
			self.event_focusEntered()
			eventHandler.executeEvent("gainFocus", child)
			return

		return super(Client, self).event_gainFocus()

class Container(IAccessible):

	def _get_activeChild(self):
		# QT doesn't do accFocus properly, so find the active child ourselves.
		child = self.firstChild
		while child:
			states = child.states
			if controlTypes.STATE_FOCUSED in states or controlTypes.STATE_SELECTED in states:
				return child
			child = child.next
		return None

	def event_gainFocus(self):
		if eventHandler.isPendingEvents("gainFocus"):
			return

		child = self.activeChild
		if child:
			# QT doesn't fire focus on the active child as it should, so redirect the focus.
			self.event_focusEntered()
			eventHandler.executeEvent("gainFocus", child)
			return

		return super(Container, self).event_gainFocus()

class TreeViewItem(IAccessible):
	RE_POSITION_INFO = re.compile(r"L(?P<level>\d)+, (?P<indexInGroup>\d)+ of (?P<similarItemsInGroup>\d)+ with \d+")

	# The description and value should not be user visible.
	description = None
	value = None

	def _get_positionInfo(self):
		# QT encodes the position info in the accDescription.
		try:
			desc = self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except COMError:
			return super(TreeViewItem, self).positionInfo

		m = self.RE_POSITION_INFO.match(desc)
		if m:
			return m.groupdict()

		return super(TreeViewItem, self).positionInfo

class Menu(IAccessible):

	def _get_states(self):
		states = super(Menu, self)._get_states()
		# QT fires a focus event on the parent menu immediately after firing focus on the menu item.
		# The focus on the menu is invalid, so remove its focused state so it will be treated as such.
		states.discard(controlTypes.STATE_FOCUSED)
		return states

class LayeredPane(IAccessible):
	# QT < 4.6 uses ROLE_SYSTEM_IPADDRESS for layered pane.
	# See QT task 258413.
	role = controlTypes.ROLE_LAYEREDPANE

class Application(IAccessible):
	# QT sets the path of the application in the description, which is irrelevant to the user.
	description = None

	def _get_states(self):
		states = super(Application, self)._get_states()
		# The application should not have the focused state.
		# Otherwise, checks for the focused state will always hit the application and assume the focus is valid.
		states.discard(controlTypes.STATE_FOCUSED)
		return states
