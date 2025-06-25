# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 11 Voice Access (Version 22H2 and later).
Voice Access allows users to dictate text and perform voice commands, replacing Windows Speech Recognition.
"""

from typing import Callable
import appModuleHandler
import ui
import winUser
from NVDAObjects import NVDAObject
from winAPI.types import HWNDValT
import UIAHandler


class AppModule(appModuleHandler.AppModule):
	def isGoodUIAWindow(self, hwnd: HWNDValT) -> bool:
		# Allow proper mouse and touch interaction from main Voice access interface.
		if winUser.getClassName(hwnd) == "Voice access":
			return True
		return False

	def shouldProcessUIANotificationEvent(
		self,
		sender: UIAHandler.UIA.IUIAutomationElement,
		notificationKind: int | None = None,
		notificationProcessing: int | None = None,
		displayString: str = "",
		activityId: str = "",
	) -> bool:
		# #16862: Voice Access notification elements do not have native window handle.
		# Say "yes" so notifications from these elements, including text dictation, can be announced.
		return True

	def event_UIA_notification(
		self,
		obj: NVDAObject,
		nextHandler: Callable[[], None],
		notificationKind: int | None = None,
		notificationProcessing: int | None = None,
		displayString: str | None = None,
		activityId: str | None = None,
	):
		# #16862: report Voice access messages such as microphone toggle from everywhere.
		# #17384: this also allows dictated text to be announced.
		if displayString is not None:
			ui.message(displayString)
