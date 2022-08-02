# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2022 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides functions to interact with the Windows system.
"""

from ctypes.wintypes import HWND, LPARAM
from ctypes import (
	c_bool,
	c_int,
	create_unicode_buffer,
	POINTER,
	WINFUNCTYPE,
	windll,
	WinError,
)
import re
from SystemTestSpy.blockUntilConditionMet import _blockUntilConditionMet
from typing import Callable, List, NamedTuple
from robot.libraries.BuiltIn import BuiltIn

builtIn: BuiltIn = BuiltIn()

# rather than using the ctypes.c_void_p type, which may encourage attempting to dereference
# what may be an invalid or illegal pointer, we'll treat it as an opaque value.
HWNDVal = int


class Window(NamedTuple):
	hwndVal: HWNDVal
	title: str


def _GetWindowTitle(hwnd: HWNDVal) -> str:
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

	# BOOL CALLBACK EnumWindowsProc _In_ HWND,_In_ LPARAM
	# HWND as a pointer creates confusion, treat as an int
	# http://makble.com/the-story-of-lpclong
	@WINFUNCTYPE(c_bool, c_int, POINTER(c_int))
	def _append_title(hwnd: HWNDVal, _lParam: LPARAM) -> bool:
		if not isinstance(hwnd, (HWNDVal, c_int)):
			builtIn.log(f"Hwnd type {type(hwnd)}, value {hwnd}")
		window = Window(hwnd, _GetWindowTitle(hwnd))
		if filterUsingWindow(window):
			windows.append(window)
		return True

	if not windll.user32.EnumWindows(_append_title, 0):
		raise WinError()
	return windows


def _GetVisibleWindows() -> List[Window]:
	return _GetWindows(
		filterUsingWindow=lambda window: windll.user32.IsWindowVisible(window.hwndVal) and bool(window.title)
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
		logger(f"Found window (HWND: {windows[0].hwndVal}) (title: {windows[0].title})")
		return windll.user32.SetForegroundWindow(windows[0].hwndVal)
	elif len(windows) == 0:
		logger("No windows matching the pattern found")
	else:
		logger(f"Too many windows to focus {windows}")
	return False


def GetVisibleWindowTitles() -> List[str]:
	windows = _GetVisibleWindows()
	return [w.title for w in windows]


def GetForegroundWindowTitle() -> str:
	hwnd: HWNDVal = windll.user32.GetForegroundWindow()
	return _GetWindowTitle(hwnd)


def waitUntilWindowFocused(targetWindowTitle: str, timeoutSecs: int = 5):
	_blockUntilConditionMet(
		getValue=lambda: GetForegroundWindowTitle() == targetWindowTitle,
		giveUpAfterSeconds=timeoutSecs,
		errorMessage=f"Timed out waiting {targetWindowTitle} to focus",
	)


def getWindowHandle(windowClassName: str, windowName: str) -> HWNDVal:
	return windll.user32.FindWindowW(windowClassName, windowName)


def windowWithHandleExists(handle: HWNDVal) -> bool:
	return bool(windll.user32.IsWindow(handle))
