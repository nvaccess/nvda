# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2022 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides functions to interact with the Windows system.
"""

from ctypes.wintypes import HWND, LPARAM
from ctypes import c_bool, c_int, create_unicode_buffer, POINTER, WINFUNCTYPE, windll, WinError
import re
from SystemTestSpy.blockUntilConditionMet import _blockUntilConditionMet
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


def SetForegroundWindow(targetTitle: re.Pattern, logger: Callable[[str], None] = lambda _: None) -> bool:
	currentTitle = GetForegroundWindowTitle()
	if re.match(targetTitle, currentTitle):
		logger(f"Window '{currentTitle}' already focused")
		return True
	windows = _GetWindows(
		filterUsingWindow=lambda window: re.match(targetTitle, window.title)
	)
	if len(windows) == 1:
		logger(f"Focusing window to (HWND: {windows[0].hwnd}) (title: {windows[0].title})")
		return windll.user32.SetForegroundWindow(windows[0].hwnd)
	elif len(windows) == 0:
		logger("No windows matching the pattern found")
	else:
		logger(f"Too many windows to focus {windows}")
	return False


def GetVisibleWindowTitles() -> List[str]:
	windows = _GetVisibleWindows()
	return [w.title for w in windows]


def GetForegroundWindowTitle() -> str:
	hwnd = windll.user32.GetForegroundWindow()
	return _GetWindowTitle(hwnd)


def waitUntilWindowFocused(targetWindowTitle: str, timeoutSecs: int = 5):
	_blockUntilConditionMet(
		getValue=lambda: GetForegroundWindowTitle() == targetWindowTitle,
		giveUpAfterSeconds=timeoutSecs,
		errorMessage=f"Timed out waiting {targetWindowTitle} to focus",
	)


def getWindowHandle(windowClassName: str, windowName: str) -> int:
	return windll.user32.FindWindowW(windowClassName, windowName)


def windowWithHandleExists(handle: int) -> bool:
	return bool(windll.user32.IsWindow(handle))
