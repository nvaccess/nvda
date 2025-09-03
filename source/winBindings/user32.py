# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

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
	POINTER(PAINTSTRUCT),  # lpPaint
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

OpenClipboard = dll.OpenClipboard
"""
Opens the clipboard for examination and prevents other applications from modifying the clipboard content until the clipboard is closed.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-openclipboard
"""
OpenClipboard.argtypes = (
	HWND,  # hWndNewOwner
)
OpenClipboard.restype = BOOL

CloseClipboard = dll.CloseClipboard
"""
Closes the clipboard and releases ownership of the clipboard to other applications.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-closeclipboard
"""
CloseClipboard.argtypes = ()
CloseClipboard.restype = BOOL

GetClipboardData = dll.GetClipboardData
"""
Retrieves data from the clipboard in a specified format.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclipboarddata
"""
GetClipboardData.argtypes = (
	UINT,  # uFormat
)
GetClipboardData.restype = HANDLE

SetClipboardData = dll.SetClipboardData
"""
Places data on the clipboard in a specified format.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setclipboarddata
"""
SetClipboardData.argtypes = (
	UINT,  # uFormat
	HANDLE,  # hMem
)
SetClipboardData.restype = HANDLE

WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
"""
An application-defined callback function used with the EnumWindows or EnumDesktopWindows function.
It receives top-level window handles.
"""

EnumWindows = dll.EnumWindows
"""
Enumerates all top-level windows on the screen by passing the handle to each window,
in turn, to an application-defined callback function.
EnumWindows continues until the last top-level window is enumerated or the callback function returns FALSE.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows
"""
EnumWindows.argtypes = (
	WNDENUMPROC,  # lpEnumFunc
	LPARAM,  # lParam
)
EnumWindows.restype = BOOL
