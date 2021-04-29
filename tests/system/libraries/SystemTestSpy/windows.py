# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides functions to interact with the Windows system.
"""

from ctypes.wintypes import HWND, LPARAM
from ctypes import c_bool, c_int, create_unicode_buffer, POINTER, WINFUNCTYPE, windll, WinError
import re
from typing import List, Tuple


def _GetWindowTitle(hwnd: HWND) -> str:
	length = windll.user32.GetWindowTextLengthW(hwnd)
	if not length:
		return ''
	buff = create_unicode_buffer(length + 1)
	if not windll.user32.GetWindowTextW(hwnd, buff, length + 1):
		raise WinError()
	return str(buff.value)


def _GetActiveWindows() -> List[Tuple[HWND, str]]:
	windows: List[Tuple[HWND, str]] = []
	EnumWindowsProc = WINFUNCTYPE(c_bool, POINTER(c_int), POINTER(c_int))

	def _append_title(hwnd: HWND, _lParam: LPARAM) -> bool:
		if windll.user32.IsWindowVisible(hwnd):
			title = _GetWindowTitle(hwnd)
			if title:
				windows.append((hwnd, title))
		return True

	if not windll.user32.EnumWindows(EnumWindowsProc(_append_title), 0):
		raise WinError()
	return windows


def SetForegroundWindow(targetTitle: re.Pattern) -> bool:
	if re.match(targetTitle, GetForegroundWindowTitle()):
		return True
	windows = _GetActiveWindows()
	for hwnd, title in windows:
		if re.match(targetTitle, title):
			return windll.user32.SetForegroundWindow(hwnd)
	return False


def GetActiveWindowTitles() -> List[str]:
	windows = _GetActiveWindows()
	return [w[1] for w in windows]


def GetForegroundWindowTitle() -> str:
	hwnd = windll.user32.GetForegroundWindow()
	return _GetWindowTitle(hwnd)
