# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2022 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides functions to interact with the Windows system.
"""

from ctypes.wintypes import LPARAM
from ctypes import (
	c_bool,
	c_int,
	create_unicode_buffer,
	POINTER,
	WINFUNCTYPE,
	windll,
	WinError,
)
from typing import (
	Callable,
	List,
	NamedTuple,
	Optional,
)
import re
from SystemTestSpy.blockUntilConditionMet import _blockUntilConditionMet
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


def CloseWindow(window: Window) -> bool:
	"""
	@return: True if the window exists and the message was sent.
	"""
	if windowWithHandleExists(window.hwndVal):
		return bool(windll.user32.CloseWindow(
			window.hwndVal,
		))
	return False


Logger = Callable[[str], None]


def SetForegroundWindow(window: Window, logger: Logger) -> bool:
	"""This may be unreliable, there are conditions on which processes can set the foreground window.
	https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow#remarks
	Additionally, note that this code is run by the Robot Framework test runner, not NVDA.
	"""
	assert window is not None
	assert bool(window.hwndVal)

	if window.hwndVal == GetForegroundHwnd():
		title = _GetWindowTitle(window.hwndVal)
		logger(f"Window already focused, HWND '{window.hwndVal}' with title: {title}")
		return True

	logger(f"Focusing window to (HWND: {window.hwndVal}) (title: {window.title})")
	# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow#remarks
	# The test may not be able to set the foreground window with user32.SetForegroundWindow
	return windll.user32.SetForegroundWindow(window.hwndVal)


def GetWindowWithTitle(targetTitle: re.Pattern, logger: Logger) -> Optional[Window]:
	windows = _GetWindows(
		filterUsingWindow=lambda _window: bool(re.match(targetTitle, _window.title))
	)
	if len(windows) == 1:
		logger(f"Found window (HWND: {windows[0].hwndVal}) (title: {windows[0].title})")
		return windows[0]
	elif len(windows) == 0:
		logger(f"No windows found matching the pattern: {targetTitle}")
		return None
	else:
		logger(f"Too many windows to focus {windows}")
		return None


def GetVisibleWindowTitles() -> List[str]:
	windows = _GetVisibleWindows()
	return [w.title for w in windows]


def GetForegroundHwnd() -> HWNDVal:
	return windll.user32.GetForegroundWindow()


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
