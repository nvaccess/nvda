#NVDAObjects/IAccessible/qt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import controlTypes
from NVDAObjects.IAccessible import IAccessible
import eventHandler
from scriptHandler import isScriptWaiting

class Client(IAccessible):

	def _get__containedWidget(self):
		widget = self.firstChild
		if not widget:
			return None

		wnext = widget.next
		if not wnext:
			# There is only one child, so this is probably a widget container.
			return widget

		try:
			if wnext.firstChild.role == controlTypes.ROLE_SCROLLBAR:
				# There is only one child plus a scrollbar, so this is probably a widget container.
				return widget
		except AttributeError:
			pass

		# This is not a widget container.
		return None

	def event_gainFocus(self):
		if eventHandler.isPendingEvents("gainFocus"):
			return

		widget = self._containedWidget
		if widget:
			# This is a widget container.
			# Redirect the focus to the contained widget, since QT doesn't do it properly.
			self.event_focusEntered()
			eventHandler.executeEvent("gainFocus", widget)
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


class TableRow(Container):

	value=None
	description=None

	def _get_activeChild(self):
		# QT doesn't do accFocus properly, so find the active child ourselves.
		child = self.firstChild
		while child:
			states = child.states
			if controlTypes.STATE_FOCUSED in states:
				return child
			child = child.next
		return None


class TableCell(IAccessible):

	value=None

	def script_nextColumn(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			next=self.next
			if next and controlTypes.STATE_FOCUSED in next.states:
				eventHandler.executeEvent("gainFocus", next)

	def script_previousColumn(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			previous=self.previous
			if previous and controlTypes.STATE_FOCUSED in previous.states:
				eventHandler.executeEvent("gainFocus", previous)

	__gestures = {
		"kb:tab": "nextColumn",
		"kb:rightArrow": "nextColumn",
		"kb:shift+tab": "previousColumn",
		"kb:leftArrow": "previousColumn",
	}


class TreeViewItem(IAccessible):

	value = None

	hasEncodedAccDescription=True

class Menu(IAccessible):
	# QT incorrectly fires a focus event on the parent menu immediately after (correctly) firing focus on the menu item.
	# This is probably QT task 241161, which was apparently fixed in QT 4.5.1.
	shouldAllowIAccessibleFocusEvent = False

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
