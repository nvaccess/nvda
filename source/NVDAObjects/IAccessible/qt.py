#NVDAObjects/IAccessible/qt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2019 NV Access Limited, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import controlTypes
from NVDAObjects.IAccessible import IAccessible
import eventHandler
from scriptHandler import isScriptWaiting

def _getActiveChild(obj):
	# QT doesn't do accFocus properly, so find the active child ourselves.
	child = obj.firstChild
	for i in range(obj.childCount):
		states = child.states
		if controlTypes.State.FOCUSED in states or controlTypes.State.SELECTED in states:
			return child
		oldChild = child
		child = child.next
		# 9202: In Virtualbox 5.2 and above, accNavigate is severely broken,
		# returning the current object when calling next, causing an endless loop.
		if oldChild == child:
			break
	else:
		return None				
	for child in obj.children:
		states = child.states
		if controlTypes.State.FOCUSED in states or controlTypes.State.SELECTED in states:
			return child
	return None

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
			if wnext.firstChild.role == controlTypes.Role.SCROLLBAR:
				# There is only one child plus a scrollbar, so this is probably a widget container.
				return widget
		except AttributeError:
			pass

		# This is not a widget container.
		return None

	def _get_focusRedirect(self):
		return self._containedWidget

class Container(IAccessible):

	def _get_activeChild(self):
		return _getActiveChild(self)

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# QT doesn't fire focus on the active child as it should, so we will bounce the focus to it.
		# However, as the container does not have the focused state in QT5, we must still ensure we can get the event if we are going to bounce it
		res=super(Container,self).shouldAllowIAccessibleFocusEvent
		if not res:
			res=bool(self.activeChild)
		return res

	def _get_focusRedirect(self):
		return self.activeChild

class TableRow(Container):

	value=None
	description=None

	def _get_activeChild(self):
		return _getActiveChild(self)

class TableCell(IAccessible):

	value=None

	def script_nextColumn(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			next=self.next
			if next and controlTypes.State.FOCUSED in next.states:
				eventHandler.executeEvent("gainFocus", next)

	def script_previousColumn(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			previous=self.previous
			if previous and controlTypes.State.FOCUSED in previous.states:
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
	role = controlTypes.Role.LAYEREDPANE

class Application(IAccessible):
	# QT sets the path of the application in the description, which is irrelevant to the user.
	description = None

	def _get_states(self):
		states = super(Application, self)._get_states()
		# The application should not have the focused state.
		# Otherwise, checks for the focused state will always hit the application and assume the focus is valid.
		states.discard(controlTypes.State.FOCUSED)
		return states
