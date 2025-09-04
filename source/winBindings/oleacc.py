# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by oleacc.dll, and supporting data structures and enumerations."""

from ctypes import (
	HRESULT,
	windll,
	POINTER,
	c_uint,
	c_long,
	c_void_p,
)
from ctypes.wintypes import (
	HANDLE,
	WPARAM,
	HWND,
	DWORD,
	LPWSTR,
	POINT,
)
from .user32 import LRESULT
from comInterfaces.Accessibility import IAccessible
from comtypes.automation import VARIANT
from comtypes import IUnknown, GUID


dll = windll.oleacc

GetProcessHandleFromHwnd = dll.GetProcessHandleFromHwnd
"""
Retrieves a process handle from a window handle.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/winauto/getprocesshandlefromhwnd
"""
GetProcessHandleFromHwnd.argtypes = (
	HWND,  # windowHandle
)
GetProcessHandleFromHwnd.restype = HANDLE

AccNotifyTouchInteraction = dll.AccNotifyTouchInteraction
"""
Notifies the system that a touch interaction has occurred.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accnotifytouchinteraction
"""
AccNotifyTouchInteraction.argtypes = (
	HWND,  # hwndApp
	HWND,  # hwndTarget
	POINT,  # ptTarget
)
AccNotifyTouchInteraction.restype = HRESULT

AccSetRunningUtilityState = dll.AccSetRunningUtilityState
"""
Sets the running utility state for accessibility.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accsetrunningutilitystate
"""
AccSetRunningUtilityState.argtypes = (
	HWND,  # hwndApp
	DWORD,  # dwUtilityStateMask
	DWORD,  # dwUtilityState
)
AccSetRunningUtilityState.restype = HRESULT

AccessibleChildren = dll.AccessibleChildren
"""
Retrieves the specified children of an accessible object.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessiblechildren
"""
AccessibleChildren.argtypes = (
	POINTER(IAccessible),  # paccContainer
	c_long,  # iChildStart
	c_long,  # cChildren
	POINTER(VARIANT),  # rgvarChildren
	POINTER(c_long),  # pcObtained
)
AccessibleChildren.restype = HRESULT

AccessibleObjectFromEvent = dll.AccessibleObjectFromEvent
"""
Retrieves the address of the IAccessible interface for the object that generated the event and the child ID.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessibleobjectfromevent
"""
AccessibleObjectFromEvent.argtypes = (
	HWND,  # hwnd
	DWORD,  # dwObjectID
	DWORD,  # dwChildID
	POINTER(POINTER(IAccessible)),  # ppacc
	POINTER(VARIANT),  # pvarChild
)
AccessibleObjectFromEvent.restype = HRESULT

AccessibleObjectFromPoint = dll.AccessibleObjectFromPoint
"""
Retrieves the address of the IAccessible interface pointer for the object displayed at a specified point on the screen.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessibleobjectfrompoint
"""
AccessibleObjectFromPoint.argtypes = (
	POINT,  # ptScreen
	POINTER(POINTER(IAccessible)),  # ppacc
	POINTER(VARIANT),  # pvarChild
)
AccessibleObjectFromPoint.restype = HRESULT

AccessibleObjectFromWindow = dll.AccessibleObjectFromWindow
"""
Retrieves the address of the IAccessible interface for the object associated with the specified window.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessibleobjectfromwindow
"""
AccessibleObjectFromWindow.argtypes = (
	HWND,  # hwnd
	DWORD,  # dwId
	POINTER(GUID),  # riid
	POINTER(c_void_p),  # ppvObject
)
AccessibleObjectFromWindow.restype = HRESULT

CreateStdAccessibleObject = dll.CreateStdAccessibleObject
"""
Creates a standard object that exposes an IAccessible interface.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-createstdaccessibleobject
"""
CreateStdAccessibleObject.argtypes = (
	HWND,  # hwnd
	DWORD,  # idObject
	POINTER(GUID),  # riid
	POINTER(c_void_p),  # ppvObject
)
CreateStdAccessibleObject.restype = HRESULT

CreateStdAccessibleProxy = dll.CreateStdAccessibleProxyW
"""
Creates a proxy accessible object for a window.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-createstdaccessibleproxyw
"""
CreateStdAccessibleProxy.argtypes = (
	HWND,  # hwnd
	LPWSTR,  # lpszClassName
	DWORD,  # idObject
	POINTER(GUID),  # riid
	POINTER(c_void_p),  # ppvObject
)
CreateStdAccessibleProxy.restype = HRESULT

GetRoleText = dll.GetRoleTextW
"""
Retrieves a localized string that describes an object's role for the specified role value.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-getroletextw
"""
GetRoleText.argtypes = (
	DWORD,  # dwRole
	LPWSTR,  # lpszRole
	c_uint,  # cchRoleMax
)
GetRoleText.restype = c_uint

GetStateText = dll.GetStateTextW
"""
Retrieves a localized string that describes an object's state for the specified state value.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-getstatetextw
"""
GetStateText.argtypes = (
	DWORD,  # dwStateBit
	LPWSTR,  # lpszState
	c_uint,  # cchState
)
GetStateText.restype = c_uint

LresultFromObject = dll.LresultFromObject
"""
Creates an LRESULT value containing a pointer to a COM interface.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-lresultfromobject
"""
LresultFromObject.argtypes = (
	POINTER(GUID),  # riid
	WPARAM,  # wParam
	POINTER(IUnknown),  # punk
)
LresultFromObject.restype = LRESULT

ObjectFromLresult = dll.ObjectFromLresult
"""
Retrieves a COM interface pointer from an LRESULT value.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-objectfromlresult
"""
ObjectFromLresult.argtypes = (
	LRESULT,  # lResult
	POINTER(GUID),  # riid
	WPARAM,  # wParam
	POINTER(c_void_p),  # ppvObject
)
ObjectFromLresult.restype = HRESULT

WindowFromAccessibleObject = dll.WindowFromAccessibleObject
"""
Retrieves the window handle for the window that contains the specified accessible object.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-windowfromaccessibleobject
"""
WindowFromAccessibleObject.argtypes = (
	POINTER(IAccessible),  # pacc
	POINTER(HWND),  # phwnd
)
WindowFromAccessibleObject.restype = HRESULT
