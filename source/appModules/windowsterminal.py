# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""App module for the Windows Terminal application (wt.exe / WindowsTerminal.exe)."""

import appModuleHandler
import winUser
from winAPI.types import HWNDValT


class AppModule(appModuleHandler.AppModule):
	def isGoodUIAWindow(self, hwnd: HWNDValT) -> bool:
		# Windows Terminal hosts its content in a XAML island whose child window
		# (Windows.UI.Composition.DesktopWindowContentBridge) is the one that actually
		# exposes a UIA server-side provider.
		# However, the top-level CASCADIA_HOSTING_WINDOW_CLASS window
		# reports no server-side provider.
		if winUser.getClassName(hwnd) == "CASCADIA_HOSTING_WINDOW_CLASS":
			return True
		return False
