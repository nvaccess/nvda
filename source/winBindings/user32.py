# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by user32.dll, and supporting data structures and enumerations."""

from ctypes import WINFUNCTYPE, c_int, c_long, c_longlong, c_void_p, sizeof, windll
from ctypes.wintypes import BOOL, DWORD, HHOOK, HINSTANCE, HWND, LPARAM, LPMSG, UINT, WPARAM

__all__ = (
	"LRESULT",
	"CallNextHookEx",
	"GetMessage",
	"HOOKPROC",
	"SetWindowsHookEx",
	"DefWindowProc",
)


# LRESULT is defined as LONG_PTR (signed type)
if sizeof(c_long) == sizeof(c_void_p):
	LRESULT = c_long
elif sizeof(c_longlong) == sizeof(c_void_p):
	LRESULT = c_longlong
else:
	raise RuntimeError("Unsupported platform")


dll = windll.user32

CallNextHookEx = dll.CallNextHookEx
"""
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callnexthookex
"""
CallNextHookEx.argtypes = (
	HHOOK,  # hook
	c_int,  # code
	WPARAM,
	LPARAM,
)
CallNextHookEx.restype = LRESULT

GetMessage = dll.GetMessageW
"""
Retrieves a message from the calling thread's message queue, dispatching incoming sent messages until a posted message is available for retrieval.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessagew
"""
GetMessage.argtypes = (
	LPMSG,  # lpMsg
	HWND,  # hWnd
	UINT,  # wMsgFilterMin
	UINT,  # wMsgFilterMax
)
GetMessage.restype = BOOL

HOOKPROC = WINFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)  # noqa: F405

SetWindowsHookEx = dll.SetWindowsHookExW
SetWindowsHookEx.argtypes = (
	c_int,  # idHook
	HOOKPROC,  # lpfn
	HINSTANCE,  # hMod
	DWORD,  # dwThreadId
)
SetWindowsHookEx.restype = HHOOK

DefWindowProc = dll.DefWindowProcW
"""
Calls the default window procedure to provide default processing for any window messages that an application does not process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-defwindowprocw
"""
DefWindowProc.argtypes = (
	HWND,
	UINT,  # msg
	WPARAM,
	LPARAM,
)
DefWindowProc.restype = LRESULT
