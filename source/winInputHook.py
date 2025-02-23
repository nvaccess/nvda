# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
When working on this file, consider moving to winAPI.
"""

import threading
from ctypes import (
	Structure,
	byref,
	c_void_p,
	windll,
	WINFUNCTYPE,
	c_int,
	c_wchar_p,
)
from ctypes.wintypes import (
	UINT,
	HINSTANCE,
	HHOOK,
	HWND,
	HMODULE,
	MSG,
	LPMSG,
	WPARAM,
	LPARAM,
	DWORD,
	POINT,
)

import watchdog
import winUser

windll.user32.CallNextHookEx.argtypes = (
	HHOOK,   # hook
	c_int,  # code
	WPARAM,
	LPARAM,
)

windll.user32.GetMessageW.argtypes = (
	LPMSG,  # lpMsg
	HWND,  # hWnd
	UINT,  # wMsgFilterMin
	UINT,  # wMsgFilterMax
)

windll.kernel32.GetModuleHandleW.restype = HMODULE
windll.kernel32.GetModuleHandleW.argtypes = (
	c_wchar_p,
)

# Some Windows constants
HC_ACTION = 0
WH_KEYBOARD_LL = 13
LLKHF_UP = 128
LLKHF_EXTENDED = 1
LLKHF_INJECTED = 16
WH_MOUSE_LL = 14
LLMHF_INJECTED = 1


class KBDLLHOOKSTRUCT(Structure):  # noqa: F405
	_fields_ = [
		("vkCode", DWORD),  # noqa: F405
		("scanCode", DWORD),  # noqa: F405
		("flags", DWORD),  # noqa: F405
		("time", DWORD),  # noqa: F405
		("dwExtraInfo", DWORD),  # noqa: F405
	]


class MSLLHOOKSTRUCT(Structure):  # noqa: F405
	_fields_ = [
		("pt", POINT),  # noqa: F405
		("mouseData", DWORD),  # noqa: F405
		("flags", DWORD),  # noqa: F405
		("time", DWORD),  # noqa: F405
		("dwExtraInfo", DWORD),  # noqa: F405
	]

LRESULT = c_void_p

HOOKPROC = WINFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)  # noqa: F405

windll.user32.SetWindowsHookExW.restype = HHOOK
windll.user32.SetWindowsHookExW.argtypes = (
	c_int,  # idHook
	HOOKPROC,  # lpfn
	HINSTANCE,  # hMod
	DWORD,  # dwThreadId
)


keyDownCallback = None
keyUpCallback = None
mouseCallback = None


@HOOKPROC
def keyboardHook(code, wParam, lParam):
	if code != HC_ACTION:
		return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
	kbd = KBDLLHOOKSTRUCT.from_address(lParam)
	if keyUpCallback and kbd.flags & LLKHF_UP:
		if not keyUpCallback(
			kbd.vkCode,
			kbd.scanCode,
			bool(kbd.flags & LLKHF_EXTENDED),
			bool(kbd.flags & LLKHF_INJECTED),
		):
			return 1
	elif keyDownCallback:
		if not keyDownCallback(
			kbd.vkCode,
			kbd.scanCode,
			bool(kbd.flags & LLKHF_EXTENDED),
			bool(kbd.flags & LLKHF_INJECTED),
		):
			return 1
	return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405


@HOOKPROC
def mouseHook(code, wParam, lParam):
	if watchdog.isAttemptingRecovery or code != HC_ACTION:
		return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
	msll = MSLLHOOKSTRUCT.from_address(lParam)
	if mouseCallback:
		if not mouseCallback(wParam, msll.pt.x, msll.pt.y, msll.flags & LLMHF_INJECTED):
			return 1
	return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405


hookThread = None
hookThreadRefCount = 0


def hookThreadFunc():
	keyHookID = windll.user32.SetWindowsHookExW(  # noqa: F405
		WH_KEYBOARD_LL,
		keyboardHook,
		windll.kernel32.GetModuleHandleW(None),  # noqa: F405
		0,  # noqa: F405
	)  # noqa: F405
	if keyHookID == 0:
		raise OSError("Could not register keyboard hook")
	mouseHookID = windll.user32.SetWindowsHookExW(  # noqa: F405
		WH_MOUSE_LL,
		mouseHook,
		windll.kernel32.GetModuleHandleW(None),  # noqa: F405
		0,  # noqa: F405
	)  # noqa: F405
	if mouseHookID == 0:
		raise OSError("Could not register mouse hook")
	msg = MSG()  # noqa: F405
	while windll.user32.GetMessageW(byref(msg), None, 0, 0):  # noqa: F405
		pass
	if windll.user32.UnhookWindowsHookEx(keyHookID) == 0:  # noqa: F405
		raise OSError("could not unregister key hook %s" % keyHookID)
	if windll.user32.UnhookWindowsHookEx(mouseHookID) == 0:  # noqa: F405
		raise OSError("could not unregister mouse hook %s" % mouseHookID)


def initialize():
	global hookThread, hookThreadRefCount
	hookThreadRefCount += 1
	if hookThreadRefCount == 1:
		hookThread = threading.Thread(
			name=__name__,  # winInputHook
			target=hookThreadFunc,
			daemon=True,
		)
		hookThread.start()


def setCallbacks(keyUp=None, keyDown=None, mouse=None):
	global keyUpCallback, keyDownCallback, mouseCallback
	if keyUp:
		keyUpCallback = keyUp
	if keyDown:
		keyDownCallback = keyDown
	if mouse:
		mouseCallback = mouse


def terminate():
	global hookThread, hookThreadRefCount
	if not hookThread:
		raise RuntimeError("winInputHook not running")
	hookThreadRefCount -= 1
	if hookThreadRefCount == 0:
		windll.user32.PostThreadMessageW(hookThread.ident, winUser.WM_QUIT, 0, 0)  # noqa: F405
		hookThread.join()
		hookThread = None
