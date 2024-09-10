# appModules/thunderbird.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2012 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Thunderbird email client."""

import appModuleHandler
import controlTypes
import api
import speech
import winUser
from NVDAObjects import NVDAObject
from typing import Callable


class AppModule(appModuleHandler.AppModule):
	def _isPopupMenuItem(self, obj: NVDAObject):
		attributes = getattr(obj, "IA2Attributes", None)

		if attributes and "class" in attributes:
			tag = attributes["tag"]
			classes = attributes["class"].split()
			return tag == "div" and "popup-menuitem" in classes

		return False

	def event_NVDAObject_init(self, obj: NVDAObject):
		if obj.role == controlTypes.Role.SECTION and not obj.name and self._isPopupMenuItem(obj):
			obj.role = controlTypes.Role.MENUITEM
			obj.name = obj.IAccessibleObject.accChild(1).accName(0)

	def event_gainFocus(self, obj, nextHandler):
		if (
			obj.role == controlTypes.Role.DOCUMENT
			and controlTypes.State.BUSY in obj.states
			and winUser.isWindowVisible(obj.windowHandle)
		):
			statusBar = api.getStatusBar()
			if statusBar:
				try:
					# The document loading status is contained in the second field of the status bar.
					statusText = statusBar.firstChild.next.name
				except:  # noqa: E722
					# Fall back to reading the entire status bar.
					statusText = api.getStatusBarText(statusBar)
				speech.speakMessage(controlTypes.State.BUSY.displayString)
				speech.speakMessage(statusText)
				return
		nextHandler()

	def event_nameChange(self, obj: NVDAObject, nextHandler: Callable[[], None]) -> None:
		focusObj: NVDAObject = api.getFocusObject()
		if focusObj.windowClassName == "MozillaDropShadowWindowClass" and focusObj.windowControlID == 0:
			# Report state changes in "select columns to display" menu
			focusObj.event_stateChange()
		nextHandler()
