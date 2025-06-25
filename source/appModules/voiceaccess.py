# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 11 Voice Access (Version 22H2 and later).
Voice Access allows users to dictate text and perform voice commands, replacing Windows Speech Recognition.
This app module cannot be used in portable version of NVDA."""

import appModuleHandler
import UIAHandler


class AppModule(appModuleHandler.AppModule):
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
