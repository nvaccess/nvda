# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by user32.dll, and supporting data structures and enumerations."""

from ctypes import (
	Structure,
	WINFUNCTYPE,
	c_int,
	c_size_t,
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
	LONG,
	PMSG,
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
	SHORT,
	UINT,
	WPARAM,
	ATOM,
)

UINT_PTR = c_size_t


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

GetSystemMetrics = dll.GetSystemMetrics
"""
Retrieves the specified system metric or system configuration setting.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
"""
GetSystemMetrics.restype = c_int
GetSystemMetrics.argTypes = (
	c_int,  # nIndex: The system metric or configuration setting to be retrieved
)

ChangeWindowMessageFilter = dll.ChangeWindowMessageFilter
"""
Adds or removes a message from the User Interface Privilege Isolation (UIPI) message filter.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-changewindowmessagefilter
"""
ChangeWindowMessageFilter.restype = BOOL
ChangeWindowMessageFilter.argTypes = (
	UINT,  # message: The message to add to or remove from the filter
	DWORD,  # dwFlag: The action to be performed
)

GetKeyState = dll.GetKeyState
"""
Retrieves the status (up, down, or toggled) of the specified virtual key.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeystate
"""
GetKeyState.restype = SHORT
GetKeyState.argtypes = (
	c_int,  # nVirtKey: A virtual key
)

SystemParametersInfoW = dll.SystemParametersInfoW
"""
Retrieves or sets the value of one of the system-wide parameters.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
"""
SystemParametersInfoW.restype = BOOL
SystemParametersInfoW.argtypes = (
	UINT,  # uiAction: The system-wide parameter to be retrieved or set
	UINT,  # uiParam: A parameter whose usage and format depends on the system parameter being queried or set
	c_void_p,  # pvParam: A parameter whose usage and format depends on the system parameter being queried or set
	UINT,  # fWinIni: If setting a system parameter, Whether to update the user profile, and if so, whether to  broadcast the change
)

WaitMessage = dll.WaitMessage
"""
Blocks thread execution until the thread needs to process a new message.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-waitmessage
"""
WaitMessage.restype = BOOL
WaitMessage.argtypes = ()

TranslateMessage = dll.TranslateMessage
"""
Translates virtual-key messages into character messages.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-translatemessage
"""
TranslateMessage.restype = BOOL
TranslateMessage.argtypes = (
	PMSG,  # lpMsg: A message retrieved from the calling thread's message queue
)

DispatchMessage = dll.DispatchMessageW
"""
Dispatches a message to a window procedure.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dispatchmessagew
"""
DispatchMessage.restype = LRESULT
DispatchMessage.argtypes = (
	PMSG,  # lpMsg
)

PeekMessage = dll.PeekMessageW
"""
Dispatches incoming nonqueued messages, checks the thread message queue for a posted message, and retrieves the message (if any exist).

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-peekmessagew
"""
PeekMessage.restype = BOOL
PeekMessage.argtypes = (
	LPMSG,  # lpMsg: Pointer to an MSG structure that receives message information
	HWND,  # hWnd: Handle to the window whose messages are to be retrieved
	UINT,  # wMsgFilterMin: The value of the first message in the range of messages to be examined
	UINT,  # wMsgFilterMax: The value of the last message in the range of messages to be examined
	UINT,  # wRemoveMsg: Specifies how messages are to be handled
)

GetAsyncKeyState = dll.GetAsyncKeyState
"""
Determines whether a key is up or down at the time the function is called.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getasynckeystate
"""
GetAsyncKeyState.restype = SHORT
GetAsyncKeyState.argtypes = (
	c_int,  # vKey: The virtual-key code
)

IsWindow = dll.IsWindow
"""
Determines whether the specified window handle identifies an existing window.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindow
"""
IsWindow.restype = BOOL
IsWindow.argtypes = (
	HWND,  # hWnd: A handle to the window to be tested
)

IsChild = dll.IsChild
"""
Determines whether a window is a child or descendant window of a specified parent window.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-ischild
"""
IsChild.restype = BOOL
IsChild.argtypes = (
	HWND,  # hWndParent: Handle to the parent window
	HWND,  # hWnd: Handle to the window to be tested
)

GetForegroundWindow = dll.GetForegroundWindow
"""
Retrieves a handle to the foreground window (the window with which the user is currently working)

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getforegroundwindow
"""
GetForegroundWindow.restype = HWND
GetForegroundWindow.argtypes = ()

SetForegroundWindow = dll.SetForegroundWindow
"""
Brings the thread that created the specified window into the foreground and activates the window.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow
"""
SetForegroundWindow.restype = BOOL
SetForegroundWindow.argtypes = (
	HWND,  # hWnd: Handle to the window that should be activated and brought to the foreground.
)

SetFocus = dll.SetFocus
"""
Sets the keyboard focus to the specified window.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setfocus
"""
SetFocus.restype = HWND
SetFocus.argtypes = (
	HWND,  # hWnd: Handle to the window that will receive the keyboard input
)

GetDesktopWindow = dll.GetDesktopWindow
"""
Retrieves a handle to the desktop window.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdesktopwindow
"""
GetDesktopWindow.restype = HWND
GetDesktopWindow.argtypes = ()

GetWindowLong = dll.GetWindowLongW
"""
Retrieves information about the specified window.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongw
"""
GetWindowLong.restype = LONG
GetWindowLong.argtypes = (
	HWND,  # hWnd: Handle to the window and, indirectly, the class to which the window belongs
	c_int,  # nIndex: Zero-based offset to the value to be retrieved
)

TIMERPROC = WINFUNCTYPE(None, HWND, UINT, UINT_PTR, DWORD)
"""
An application-defined callback function that processes WM_TIMER messages.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-timerproc
"""

SetTimer = dll.SetTimer
"""
Creates a timer with the specified time-out value.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-settimer
"""
SetTimer.restype = UINT_PTR
SetTimer.argtypes = (
	HWND,  # hWnd: handle to the window to be associated with the timer
	UINT_PTR,  # nIDEvent: A nonzero timer identifier
	UINT,  # uElapse: The time-out value, in milliseconds
	TIMERPROC,  # lpTimerFunc: Pointer to the function to be notified when the time-out value elapses
)

KillTimer = dll.KillTimer
"""
Destroys the specified timer.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-killtimer
"""
KillTimer.restype = BOOL
KillTimer.argTypes = (
	HWND,  # hWnd: Handle to the window associated with the specified timer
	UINT_PTR,  # uIDEvent: The timer to be destroyed
)


SetWinEventHook = dll.SetWinEventHook
UnhookWinEvent = dll.UnhookWinEvent
SendMessage = dll.SendMessageW
GetWindowThreadProcessId = dll.GetWindowThreadProcessId
GetClassName = dll.GetClassNameW
keybd_event = dll.keybd_event
mouse_event = dll.mouse_event
GetAncestor = dll.GetAncestor
SetPhysicalCursorPos = dll.SetPhysicalCursorPos
GetPhysicalCursorPos = dll.GetPhysicalCursorPos
GetCaretPos = dll.GetCaretPos
GetTopWindow = dll.GetTopWindow
InternalGetWindowText = dll.InternalGetWindowText
GetWindow = dll.GetWindow
IsWindowVisible = dll.IsWindowVisible
IsWindowEnabled = dll.IsWindowEnabled
GetGUIThreadInfo = dll.GetGUIThreadInfo
SetWindowLong = dll.SetWindowLongW
SetLayeredWindowAttributes = dll.SetLayeredWindowAttributes
GetKeyboardLayout = dll.GetKeyboardLayout
RedrawWindow = dll.RedrawWindow
GetKeyNameText = dll.GetKeyNameTextW
FindWindow = dll.FindWindowW
MessageBox = dll.MessageBoxW
PostMessage = dll.PostMessageW
VkKeyScanEx = dll.VkKeyScanExW
VkKeyScanEx.restype = SHORT
ScreenToClient = dll.ScreenToClient
ClientToScreen = dll.ClientToScreen
NotifyWinEvent = dll.NotifyWinEvent
SendInput = dll.SendInput
