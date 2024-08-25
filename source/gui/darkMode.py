# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2024 NV Access Limited, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Dark mode makes UI elements have a dark background with light text.

This is a best-effort attempt to implement dark mode.  There are some remaining known issues:

1) MessageBox'es are not themed.  An example is the NVDA About dialog.  These dialogs
are extremely modal, and there is no way to gain control until after the user dismisses
the message box.

2) Menu bars are not themed.  An example can be seen in the Debug Log.  Supporting themed
menu bars would require intercepting several undocumented events and drawing the menu items
ourselves.  An example implementation is described in
https://github.com/adzm/win32-custom-menubar-aero-theme

3) Column titles are not themed.  An example can be seen in the Dictionary dialogs.
This is implemented by the wx.ListCtrl class.  The C++ implementation of
wxListCtrl::OnPaint hardcodes penColour, and there is no way to override it.
See https://github.com/wxWidgets/wxWidgets/blob/master/src/msw/listctrl.cpp

4) Tab controls are not themed.  An example can be seen at the top of the Add-In Store.
This is implemented by the wx.Notebook class.  I have not been able to figure out how
to influence the colors it uses.

Note: Config settings must be in a non-profile-specific config section (e.g. "general").
Profile-specific config sections (e.g. "vision") aren't available to read until after
the main app window is created.  But _SetPreferredAppMode must be called BEFORE the main
window is created in order for popup context menus to be properly styled.
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

	try:
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
	except Exception as err:
		logging.debug("Error initializing dark mode: " + str(err))

	try:
		global _SetPreferredAppMode
		_SetPreferredAppMode = uxtheme[135]
		_SetPreferredAppMode.restype = wintypes.INT
		_SetPreferredAppMode.argtypes = [wintypes.INT]
	except Exception as err:
		logging.debug("Will not use undocumented windows api SetPreferredAppMode: " + str(err))


def DwmSetWindowAttribute_ImmersiveDarkMode(window: wx.Window, isDark: bool):
	"""This makes title bars dark"""
	if _DwmSetWindowAttribute:
		try:
			useDarkMode = ctypes.wintypes.BOOL(isDark)
			_DwmSetWindowAttribute(
				window.Handle,
				DWMWA_USE_IMMERSIVE_DARK_MODE,
				ctypes.byref(useDarkMode),
				ctypes.sizeof(ctypes.c_int32),
			)
		except Exception as err:
			logging.debug("Error calling DwmSetWindowAttribute: " + str(err))


def SetPreferredAppMode(curTheme: ColorTheme):
	"""This makes popup context menus dark"""
	if _SetPreferredAppMode and config.conf["general"]["darkModeCanUseUndocumentedAPIs"]:
		try:
			if curTheme == ColorTheme.AUTO:
				_SetPreferredAppMode(1)
			elif curTheme == ColorTheme.DARK:
				_SetPreferredAppMode(2)
			else:
				_SetPreferredAppMode(0)
		except Exception as err:
			logging.debug("Error calling SetPreferredAppMode: " + str(err))

def SetWindowTheme(window: wx.Window, theme: str):
	if _SetWindowTheme and _SendMessageW:
		try:
			_SetWindowTheme(window.Handle, theme, None)
			_SendMessageW(window.Handle, WM_THEMECHANGED, 0, 0)
		except Exception as err:
			logging.debug("Error calling SetWindowTheme: " + str(err))


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
		isDark = curTheme == ColorTheme.DARK
	if isDark:
		fgColor, bgColor, themePrefix = "White", "Dark Grey", "DarkMode"
	else:
		fgColor, bgColor, themePrefix = "Black", "Very Light Grey", "LightMode"

	if eventType == wx.wxEVT_CREATE:
		SetPreferredAppMode(curTheme)

		# For some controls, colors must be set in EVT_CREATE otherwise it has no effect.
		if isinstance(window, wx.CheckListBox):
			# Unfortunately CheckListBoxes always seem to use a black foreground color for the labels,
			# which means they become illegible if you make the background too dark.  So we compromise
			# by setting the background to be a little bit darker while still being readable.
			if isDark:
				window.SetBackgroundColour("Light Grey")
			else:
				window.SetBackgroundColour("White")
			window.SetForegroundColour(fgColor)
		elif isinstance(window, wx.TextCtrl) or isinstance(window, wx.ListCtrl):
			window.SetBackgroundColour(bgColor)
			# Foreground colors for TextCtrls are surprisingly tricky, because their behavior is
			# inconsistent.  In particular, the Add-On Store Details pane behaves differently than
			# the Debug Log, Python Console, etc.  Here is a table of what happens with different
			# possibilites:
			#
			# Color           Add-on Store     Debug Log      Usable?
			# -----           ------------     ---------      -------
			# white           white            black          no
			# light grey      black            white          no
			# yellow          yellow           white          no
			# 0xFEFEFE        white            white          YES
			# black           black            black          YES
			if isDark:
				window.SetForegroundColour(wx.Colour(254, 254, 254))
			else:
				window.SetForegroundColour("Black")

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
