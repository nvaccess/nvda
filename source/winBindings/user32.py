# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by user32.dll, and supporting data structures and enumerations."""

from ctypes import (
	Structure,
	WINFUNCTYPE,
	c_int,
	c_uint,
	c_long,
	c_longlong,
	c_void_p,
	sizeof,
	windll,
	POINTER,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	BYTE,
	RECT,
	HANDLE,
	HHOOK,
	HINSTANCE,
	HMENU,
	HICON,
	HBRUSH,
	HDC,
	HWND,
	LPARAM,
	LPWSTR,
	LPCWSTR,
	LPMSG,
	UINT,
	WPARAM,
	ATOM,
)

class PAINTSTRUCT(Structure):
	_fields_ = [
		("hdc", HDC),
		("fErase", BOOL),
		("rcPaint", RECT),
		("fRestore", BOOL),
		("fIncUpdate", BOOL),
		("rgbReserved", BYTE * 32),
	]

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


HCURSOR = HANDLE

WNDPROC = WINFUNCTYPE(LRESULT, HWND, c_uint, WPARAM, LPARAM)

class WNDCLASSEXW(Structure):
	_fields_ = [
		("cbSize", c_uint),  # noqa: F405
		("style", c_uint),  # noqa: F405
		("lpfnWndProc", WNDPROC),
		("cbClsExtra", c_int),
		("cbWndExtra", c_int),
		("hInstance", HINSTANCE),  # noqa: F405
		("hIcon", HICON),  # noqa: F405
		("HCURSOR", HCURSOR),
		("hbrBackground", HBRUSH),  # noqa: F405
		("lpszMenuName", LPWSTR),  # noqa: F405
		("lpszClassName", LPWSTR),  # noqa: F405
		("hIconSm", HICON),  # noqa: F405
	]


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

CreateWindowEx = dll.CreateWindowExW
"""
Creates an overlapped, pop-up, or child window with an extended window style.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexw
"""
CreateWindowEx.argtypes = (
	DWORD,  # dwExStyle
	LPCWSTR,  # lpClassName
	LPCWSTR,  # lpWindowName
	DWORD,  # dwStyle
	c_int,  # x
	c_int,  # y
	c_int,  # nWidth
	c_int,  # nHeight
	HWND,  # hWndParent
	HMENU,  # hMenu
	HINSTANCE,  # hInstance
	c_void_p,  # lpParam
)
CreateWindowEx.restype = HWND

RegisterClassEx = dll.RegisterClassExW
"""
Registers a window class for subsequent use in calls to the CreateWindow or CreateWindowEx function.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclassexw
"""
RegisterClassEx.argtypes = (
	POINTER(WNDCLASSEXW),  # lpWndClass
)
RegisterClassEx.restype = ATOM

UnregisterClass = dll.UnregisterClassW
"""
Unregisters a window class, freeing the memory used by the class and removing it from the system.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unregisterclassw
"""
UnregisterClass.argtypes = (
	LPCWSTR,  # lpClassName
	HINSTANCE,  # hInstance
)
UnregisterClass.restype = BOOL

BeginPaint = dll.BeginPaint
"""
Begins painting in the specified window by filling a PAINTSTRUCT structure with information about the painting.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-beginpaint
"""
BeginPaint.argtypes = (
	HWND,  # hWnd
	POINTER(PAINTSTRUCT), # lpPaint
)
BeginPaint.restype = HDC

EndPaint = dll.EndPaint
"""
Ends painting in the specified window by releasing the device context (DC) and invalidating the PAINTSTRUCT structure.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-endpaint
"""
EndPaint.argtypes = (
	HWND,  # hWnd
	POINTER(PAINTSTRUCT),  # lpPaint
)
EndPaint.restype = BOOL
