# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2024 NV Access Limited, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Dark mode makes UI elements have a dark background with light text.

Note: Config settings must be in a non-profile-specific config section (e.g. "general").
Profile-specific config sections (e.g. "vision") aren't available to read until after
the main app window is created.  But _SetPreferredAppMode must be called BEFORE the main
window is created in order for popup context menus to be properly styled.

TODO: dictionary dialogs and the add-on store look bad because column titles aren't styled.
These are wx.Notebook controls.
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


def DwmSetWindowAttribute_ImmersiveDarkMode(window: wx.Window, isDark: bool):
	"""This makes title bars dark"""
	useDarkMode = ctypes.wintypes.BOOL(isDark)
	_DwmSetWindowAttribute(
		window.Handle,
		DWMWA_USE_IMMERSIVE_DARK_MODE,
		ctypes.byref(useDarkMode),
		ctypes.sizeof(ctypes.c_int32))


def SetPreferredAppMode(curTheme: ColorTheme):
	"""This makes popup context menus dark"""
	if _SetPreferredAppMode and config.conf["general"]["darkModeCanUseUndocumentedAPIs"]:
		if curTheme == ColorTheme.AUTO:
			_SetPreferredAppMode(1)
		elif curTheme == ColorTheme.DARK:
			_SetPreferredAppMode(2)
		else:
			_SetPreferredAppMode(0)


def SetWindowTheme(window: wx.Window, theme: str):
	_SetWindowTheme(window.Handle, theme, None)
	_SendMessageW(window.Handle, WM_THEMECHANGED, 0, 0)


def _getDescendants(window: wx.Window) -> Generator[wx.Window, None, None]:
	yield window
	if hasattr(window, "GetChildren"):
		for child in window.GetChildren():
			for descendant in _getDescendants(child):
				yield descendant


def handleEvent(window: wx.Window, eventType):
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

	if eventType == wx.wxEVT_CREATE:
		SetPreferredAppMode(curTheme)
		if (
			# Necessary for background of ListBoxes such as Settings >> Audio >> Cycle sound split mode.
			# TODO: this breaks lists of checkboxes
			isinstance(window, wx.ListBox)

			# Necessary for Add-on store >> Documentation >> Other details.
			# TODO: this fixes Add-on store >> Documentation >> Other details, but breaks the 
			# ExpandoTextCtrl used by the debug log, python console, etc
			#or isinstance(window, wx.TextCtrl)
		):
			window.SetBackgroundColour(bgColor)
			window.SetForegroundColour(fgColor)
	elif eventType == wx.wxEVT_SHOW:
		for child in _getDescendants(window):
			child.SetBackgroundColour(bgColor)
			child.SetForegroundColour(fgColor)

			if isinstance(child, wx.Frame) or isinstance(child, wx.Dialog):
				DwmSetWindowAttribute_ImmersiveDarkMode(child, isDark)
			elif (
				isinstance(child, wx.Button)
				or isinstance(child, wx.ScrolledWindow)
				or isinstance(child, wx.ToolTip)
				or isinstance(child, wx.TextEntry)
			):
				SetWindowTheme(child, themePrefix + "_Explorer")
			elif isinstance(child, wx.Choice):
				SetWindowTheme(child, themePrefix + "_CFD")
			elif isinstance(child, wx.ListCtrl):
				SetWindowTheme(child, themePrefix + "_ItemsView")
			else:
				SetWindowTheme(child, themePrefix)

		window.Refresh()