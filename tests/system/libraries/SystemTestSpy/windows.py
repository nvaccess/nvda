# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides functions to interact with the Windows system.
"""

from ctypes.wintypes import HWND, LPARAM
from ctypes import c_bool, c_int, create_unicode_buffer, POINTER, WINFUNCTYPE, windll, WinError
import re
from typing import Callable, List, NamedTuple


class Window(NamedTuple):
    hwnd: HWND
    title: str


def _GetWindowTitle(hwnd: HWND) -> str:
	length = windll.user32.GetWindowTextLengthW(hwnd)
	if not length:
		return ''
	buff = create_unicode_buffer(length + 1)
	if not windll.user32.GetWindowTextW(hwnd, buff, length + 1):
		raise WinError()
	return str(buff.value)


def _GetWindows(
		filterUsingWindow: Callable[[Window], bool] = lambda _: True,
) -> List[Window]:
	windows: List[Window] = []
	EnumWindowsProc = WINFUNCTYPE(c_bool, POINTER(c_int), POINTER(c_int))

	def _append_title(hwnd: HWND, _lParam: LPARAM) -> bool:
		window = Window(hwnd, _GetWindowTitle(hwnd))
		if filterUsingWindow(window):
			windows.append(window)
		return True

	if not windll.user32.EnumWindows(EnumWindowsProc(_append_title), 0):
		raise WinError()
	return windows


def _GetVisibleWindows() -> List[Window]:
	return _GetWindows(
		filterUsingWindow=lambda window: windll.user32.IsWindowVisible(window.hwnd) and bool(window.title)
	)


def SetForegroundWindow(targetTitle: re.Pattern) -> bool:
	if re.match(targetTitle, GetForegroundWindowTitle()):
		return True
	windows = _GetWindows(
		filterUsingWindow=lambda window: re.match(targetTitle, window.title)
	)
	for window in windows:
		return windll.user32.SetForegroundWindow(window.hwnd)
	return False


def GetVisibleWindowTitles() -> List[str]:
	windows = _GetVisibleWindows()
	return [w.title for w in windows]


def GetForegroundWindowTitle() -> str:
	hwnd = windll.user32.GetForegroundWindow()
	return _GetWindowTitle(hwnd)
