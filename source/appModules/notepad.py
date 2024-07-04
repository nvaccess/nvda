# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows Notepad.
While this app module also covers older Notepad releases,
this module provides workarounds for Windows 11 Notepad."""

from comtypes import COMError
import appModuleHandler
import api
import braille
import controlTypes
import eventHandler
import speech
import UIAHandler
from NVDAObjects.UIA import UIA
from NVDAObjects import NVDAObject
from typing import Callable


class AppModule(appModuleHandler.AppModule):
	def event_UIA_elementSelected(self, obj: NVDAObject, nextHandler: Callable[[], None]):
		# Announce currently selected tab when it changes.
		if (
			obj.role == controlTypes.Role.TAB
			# this is done because 2 selection events are sent for the same object, so to prevent double speaking.
			and not eventHandler.isPendingEvents("UIA_elementSelected")
			and controlTypes.State.SELECTED in obj.states
		):
			speech.cancelSpeech()
			speech.speakObject(obj, reason=controlTypes.OutputReason.FOCUS)
			braille.handler.message(
				braille.getPropertiesBraille(
					name=obj.name,
					role=obj.role,
					states=obj.states,
					positionInfo=obj.positionInfo,
				),
			)
		nextHandler()

	def _get_statusBar(self) -> NVDAObject:
		"""Retrieves Windows 11 Notepad status bar.
		In Windows 10 and earlier, status bar can be obtained by looking at the bottom of the screen.
		Windows 11 Notepad uses Windows 11 UI design (top-level window is labeled "DesktopWindowXamlSource",
		therefore status bar cannot be obtained by position alone.
		If visible, a child of the foreground window hosts the status bar elements.
		Status bar child position must be checked whenever Notepad is updated on stable Windows 11 releases
		as Notepad is updated through Microsoft Store as opposed to tied to specific Windows releases.
		L{api.getStatusBar} will resort to position lookup if C{NotImplementedError} is raised.
		"""
		# #13688: Notepad 11 uses Windows 11 user interface, therefore status bar is harder to obtain.
		# This does not affect earlier versions.
		notepadVersion = int(self.productVersion.split(".")[0])
		if notepadVersion < 11:
			raise NotImplementedError()
		# And no, status bar is shown when editing documents.
		# Thankfully, of all the UIA objects encountered, document window has a unique window class name.
		if api.getFocusObject().windowClassName != "RichEditD2DPT":
			raise NotImplementedError()
		# Obtain status bar text across Notepad 11 releases.
		clientObject = UIAHandler.handler.clientObject
		condition = clientObject.createPropertyCondition(
			UIAHandler.UIA_AutomationIdPropertyId,
			"ContentTextBlock",
		)
		walker = clientObject.createTreeWalker(condition)
		notepadWindow = clientObject.elementFromHandle(api.getForegroundObject().windowHandle)
		try:
			element = walker.getFirstChildElement(notepadWindow)
			# Is status bar even showing?
			element = element.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
		except (ValueError, COMError):
			raise NotImplementedError
		statusBar = UIA(UIAElement=element).parent
		return statusBar
