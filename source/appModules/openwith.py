# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2011-2023 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import appModuleHandler
import controlTypes
from NVDAObjects.UIA import UIA
from NVDAObjects.behaviors import Dialog
import winUser
from winAPI.types import HWNDValT


# win8hack: the nondefault items in the list of applications are not labeled
class NonDefaultAppTile(UIA):
	def _get_name(self):
		firstChild = self.firstChild
		if firstChild:
			next = firstChild.next
			if next:
				return next.name
		return super(NonDefaultAppTile, self).name


class ImmersiveOpenWithFlyout(Dialog, UIA):
	role = controlTypes.Role.DIALOG

	# win8hack: This window never actually gets the physical focus thus tabbing etc goes to the original window
	# So Force it to get focus
	def event_focusEntered(self):
		self.setFocus()
		super(ImmersiveOpenWithFlyout, self).event_focusEntered()


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA):
			automationId = obj.UIAAutomationId
			if automationId == "NonDefaultAppTile":
				clsList.insert(0, NonDefaultAppTile)
			elif automationId == "ImmersiveOpenWithFlyout":
				clsList.insert(0, ImmersiveOpenWithFlyout)

	def isGoodUIAWindow(self, hwnd: HWNDValT) -> bool:
		if winUser.getClassName(hwnd) in (
			# #11335: Open With dialog isn't read in Windows 10 Version 2004 (May 2020 Update).
			# Note that treating the below window as a UIA window will make NVDA no longer announce "pane".
			"Shell_Flyout",
			# #14538: Windows 11 Version 22H2 (2022 Update) comes with a modernized Open With dialog
			# but prevents proper mouse and touch interaction.
			"Open With",
		):
			return True
		return False
