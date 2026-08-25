# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
When working on this file, consider moving to winAPI.
"""

import threading  # noqa: I001
from ctypes import (
	Structure,
	byref,
	c_void_p,
)
from ctypes.wintypes import (
	MSG,
	DWORD,
	POINT,
)

import winBindings.user32
import watchdog
import winUser
from winBindings import user32, kernel32


# Some Windows constants
HC_ACTION = 0
WH_KEYBOARD_LL = 13
LLKHF_UP = 128
LLKHF_EXTENDED = 1
LLKHF_INJECTED = 16
WH_MOUSE_LL = 14
LLMHF_INJECTED = 1


class KBDLLHOOKSTRUCT(Structure):
	_fields_ = [
		("vkCode", DWORD),
		("scanCode", DWORD),
		("flags", DWORD),
		("time", DWORD),
		("dwExtraInfo", DWORD),
	]


class MSLLHOOKSTRUCT(Structure):
	_fields_ = [
		("pt", POINT),
		("mouseData", DWORD),
		("flags", DWORD),
		("time", DWORD),
		("dwExtraInfo", DWORD),
	]


LRESULT = c_void_p


keyDownCallback = None
keyUpCallback = None
mouseCallback = None


@user32.HOOKPROC
def keyboardHook(code, wParam, lParam):
	if code != HC_ACTION:
		return user32.CallNextHookEx(0, code, wParam, lParam)
	kbd = KBDLLHOOKSTRUCT.from_address(lParam)
	if keyUpCallback and kbd.flags & LLKHF_UP:
		if not keyUpCallback(
			kbd.vkCode,
			kbd.scanCode,
			bool(kbd.flags & LLKHF_EXTENDED),
			bool(kbd.flags & LLKHF_INJECTED),
		):
			return 1
	elif keyDownCallback:  # noqa: SIM102
		if not keyDownCallback(
			kbd.vkCode,
			kbd.scanCode,
			bool(kbd.flags & LLKHF_EXTENDED),
			bool(kbd.flags & LLKHF_INJECTED),
		):
			return 1
	return user32.CallNextHookEx(0, code, wParam, lParam)


@user32.HOOKPROC
def mouseHook(code, wParam, lParam):
	if watchdog.isAttemptingRecovery or code != HC_ACTION:
		return user32.CallNextHookEx(0, code, wParam, lParam)
	msll = MSLLHOOKSTRUCT.from_address(lParam)
	if mouseCallback:  # noqa: SIM102
		if not mouseCallback(wParam, msll.pt.x, msll.pt.y, msll.flags & LLMHF_INJECTED):
			return 1
	return user32.CallNextHookEx(0, code, wParam, lParam)


hookThread = None
hookThreadRefCount = 0


def hookThreadFunc():
	keyHookID = user32.SetWindowsHookEx(
		WH_KEYBOARD_LL,
		keyboardHook,
		kernel32.GetModuleHandle(None),
		0,
	)
	if keyHookID == 0:
		raise OSError("Could not register keyboard hook")
	mouseHookID = user32.SetWindowsHookEx(
		WH_MOUSE_LL,
		mouseHook,
		kernel32.GetModuleHandle(None),
		0,
	)
	if mouseHookID == 0:
		raise OSError("Could not register mouse hook")
	msg = MSG()
	while winBindings.user32.GetMessage(byref(msg), None, 0, 0):
		pass
	if user32.UnhookWindowsHookEx(keyHookID) == 0:
		raise OSError("could not unregister key hook %s" % keyHookID)  # noqa: UP031
	if user32.UnhookWindowsHookEx(mouseHookID) == 0:
		raise OSError("could not unregister mouse hook %s" % mouseHookID)  # noqa: UP031


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
		user32.PostThreadMessage(hookThread.ident, winUser.WM_QUIT, 0, 0)
		hookThread.join()
		hookThread = None
