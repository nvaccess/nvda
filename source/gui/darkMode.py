# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2024 NV Access Limited, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Dark mode makes UI elements have a dark background with light text.

If the darkModeCanUseUndocumentedAPIs config setting is true, then we are 
able to get proper styling for popup context menus.
"""

import ctypes.wintypes
from typing import (
	Generator,
)

import config
from config.configFlags import ColorTheme
import ctypes
import ctypes.wintypes as wintypes
import logging
import wx


_initialized = False


# Documented windows APIs
_DwmSetWindowAttribute = None
_SetWindowTheme = None
_SendMessageW = None
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
WM_THEMECHANGED = 0x031A


# Undocumented windows APIs	adapted from https://github.com/ysc3839/win32-darkmode
_SetPreferredAppMode = None


def initialize():
	global _initialized
	_initialized = True

	global _SetWindowTheme
	uxtheme = ctypes.cdll.LoadLibrary("uxtheme")
	_SetWindowTheme = uxtheme.SetWindowTheme
	_SetWindowTheme.restype = ctypes.HRESULT
	_SetWindowTheme.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR]

	global _DwmSetWindowAttribute
	dwmapi = ctypes.cdll.LoadLibrary("dwmapi")
	_DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute
	_DwmSetWindowAttribute.restype = ctypes.HRESULT
	_DwmSetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, wintypes.LPCVOID, wintypes.DWORD]

	global _SendMessageW	
	user32 = ctypes.cdll.LoadLibrary("user32")
	_SendMessageW = user32.SendMessageW
	_SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]

	try:
		global _SetPreferredAppMode
		_SetPreferredAppMode = uxtheme[135]
		_SetPreferredAppMode.restype = wintypes.INT
		_SetPreferredAppMode.argtypes = [wintypes.INT]
	except Exception as err:
		logging.debug("Will not use undocumented windows api SetPreferredAppMode: " + str(err))


def _getDescendants(window: wx.Window) -> Generator[wx.Window, None, None]:
	yield window
	if hasattr(window, "GetChildren"):
		for child in window.GetChildren():
			for descendant in _getDescendants(child):
				yield descendant


def applyColorTheme(window: wx.Window):
	if not _initialized:
		return
	curTheme = config.conf["general"]["colorTheme"]
	if curTheme == ColorTheme.AUTO:
		systemAppearance: wx.SystemAppearance = wx.SystemSettings.GetAppearance()
		isDark = systemAppearance.IsDark() or systemAppearance.IsUsingDarkBackground()
	else:
		isDark = (curTheme == ColorTheme.DARK)

	if isDark:
		fgColor, bgColor, themePrefix = "White", "Dark Grey", "DarkMode"
	else:
		fgColor, bgColor, themePrefix = "Black", "Very Light Grey", "LightMode"

	# This config setting MUST be in a non-profile-specific config section, otherwise it
	# won't be available until after the main window is created, which is too late.
	canUseUndocumentedAPIs = config.conf["general"]["darkModeCanUseUndocumentedAPIs"]
	if _SetPreferredAppMode and canUseUndocumentedAPIs:
		# This makes context menus dark.
		if curTheme == ColorTheme.AUTO:
			_SetPreferredAppMode(1)
		elif curTheme == ColorTheme.DARK:
			_SetPreferredAppMode(2)
		else:
			_SetPreferredAppMode(0)

	descendants = list(_getDescendants(window))
	for child in descendants:
		child.SetBackgroundColour(bgColor)
		child.SetForegroundColour(fgColor)

		if isinstance(child, wx.Frame) or isinstance(child, wx.Dialog):
			# This makes title bars dark
			useDarkMode = ctypes.wintypes.BOOL(isDark)
			_DwmSetWindowAttribute(
				child.Handle,
				DWMWA_USE_IMMERSIVE_DARK_MODE,
				ctypes.byref(useDarkMode),
				ctypes.sizeof(ctypes.c_int32))
		elif (
			isinstance(child, wx.Button) 
			or isinstance(child, wx.ScrolledWindow) 
			or isinstance(child, wx.ToolTip) 
			or isinstance(child, wx.TextEntry)
		):
			_SetWindowTheme(child.Handle, themePrefix + "_Explorer", None)
			_SendMessageW(child.Handle, WM_THEMECHANGED, 0, 0)
		elif isinstance(child, wx.Choice):
			_SetWindowTheme(child.Handle, themePrefix + "_CFD", None)
			_SendMessageW(child.Handle, WM_THEMECHANGED, 0, 0)
		elif isinstance(child, wx.ListCtrl):
			_SetWindowTheme(child.Handle, themePrefix + "_ItemsView", None)
			_SendMessageW(child.Handle, WM_THEMECHANGED, 0, 0)
		else:
			print(child.ClassName)
			_SetWindowTheme(child.Handle, themePrefix, None)
			_SendMessageW(child.Handle, WM_THEMECHANGED, 0, 0)

	window.Refresh()