# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by advapi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	POINTER,
	windll,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	HANDLE,
	HKEY,
	LONG,
	LPCWSTR,
)

__all__ = (
	"OpenProcessToken",
	"RegCloseKey",
	"RegDeleteTreeW",
)


dll = windll.advapi32
OpenProcessToken = dll.OpenProcessToken
"""
Opens the access token associated with a process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
"""
OpenProcessToken.argtypes = (
	HANDLE,  # ProcessHandle
	DWORD,  # DesiredAccess
	POINTER(HANDLE),  # TokenHandle
)
OpenProcessToken.restype = BOOL

RegCloseKey = dll.RegCloseKey
"""
Closes a handle to the specified registry key.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regclosekey
"""
RegCloseKey.argtypes = (
	HKEY,  # hKey
)
RegCloseKey.restype = LONG

RegDeleteTreeW = dll.RegDeleteTreeW
"""
Deletes a subkey and all its descendants.
https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regdeletetreew

This function can be replaced with winreg.DeleteTree in python 3.14.
https://github.com/python/cpython/pull/138388
"""
RegDeleteTreeW.argtypes = (
	HKEY,  # hKey
	LPCWSTR,  # lpSubKey
)
RegDeleteTreeW.restype = LONG
