# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import time
import config
import eventHandler
import api
import UIAHandler
from NVDAObjects.UIA import UIA
import winUser
import winVersion
import controlTypes
import appModuleHandler
from NVDAObjects.window import DisplayModelEditableText
from NVDAObjects.window.edit import UnidentifiedEdit
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import IAccessible


class Excel6(Window):
	"""
	The Excel cell edit window.
	If it is not accessible (no displayModel) then wait for the CellEdit UIA element to get focus and redirect to that.
	"""

	def _get_focusRedirect(self):
		if self.role==controlTypes.Role.UNKNOWN:
			# The control is inaccessible, try several times to find the CellEdit UIA element with focus and use that instead.
			for count in range(10):
				if count>=1:
					api.processPendingEvents(processEventQueue=False)
					if eventHandler.isPendingEvents("gainFocus"):
						return
					time.sleep(0.05)
				e=UIAHandler.handler.lastFocusedUIAElement
				if e and e.cachedAutomationID=="CellEdit":
					obj=UIA(UIAElement=e)
					# Set the UIA edit control's parent to the parent of self.
					# otherwise a whole bunch of UIA focus ancestors for the edit control will be reported.
					obj.parent = self.parent
					# Cache this for as long as this object exists.
					self.focusRedirect=obj
					return obj


class Excel6_WhenUIAEnabled(IAccessible):
	"""
	#12303: When accessing Microsoft Excel via UI Automation
	MSAA focus events on the old formula edit window should be completely ignored.
	UI Automation will fire its own ones.
	"""

	shouldAllowIAccessibleFocusEvent = False


class AppModule(appModuleHandler.AppModule):

	def isGoodUIAWindow(self, hwnd: int) -> bool:
		windowClass = winUser.getClassName(hwnd)
		versionMajor = int(self.productVersion.split('.')[0])
		if (
			versionMajor >= 16
			and windowClass == "RICHEDIT60W"
			and winVersion.getWinVer() >= winVersion.WIN10
		):
			# RICHEDIT60W In Excel 2016+ on Windows 10+
			# has a very good UI Automation implementation,
			# Though oddly IsServerSideProvider returns false for these windows.
			# Examples: Password field in the Protect sheet dialog.
			return True
		return False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		# #9042: Edit fields in Excel have to be accessed via displayModel.
		if windowClass == "EDTBX":
			try:
				clsList.remove(UnidentifiedEdit)
			except ValueError:
				pass
			clsList.insert(0, DisplayModelEditableText)
		if windowClass=="EXCEL6":
			if config.conf["UIA"]["useInMSExcelWhenAvailable"]:
				# #12303: When accessing Microsoft Excel via UI Automation
				# MSAA focus events on the old formula edit window should be completely ignored.
				# UI Automation will fire its own ones.
				clsList.insert(0, Excel6_WhenUIAEnabled)
			else:
				# #12303: The old Formula Edit window in recent versions of Excel
				# may not be accessible with display models as GDI is no longer used.
				# However, UI Automation does expose an accessible edit control within the active cell,
				# So use a class that will redirect focus to that.
				clsList.insert(0, Excel6)
