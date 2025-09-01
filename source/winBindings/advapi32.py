# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by advapi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	POINTER,
	windll,
	c_void_p,
)
from ctypes.wintypes import (
	BOOL,
	BYTE,
	DWORD,
	HANDLE,
	HKEY,
	LONG,
	LPCWSTR,
)

__all__ = (
	"OpenProcessToken",
	"RegCloseKey",
	"RegOpenKeyEx",
	"RegQueryValueEx",
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

RegOpenKeyEx = dll.RegOpenKeyExW
"""
Opens the specified registry key.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regopenkeyexw
"""
RegOpenKeyEx.argtypes = (
	HKEY,  # hKey
	LPCWSTR,  # lpSubKey
	DWORD,  # ulOptions
	DWORD,  # samDesired
	POINTER(HKEY),  # phkResult
)
RegOpenKeyEx.restype = LONG

RegQueryValueEx = dll.RegQueryValueExW
"""
Retrieves the type and data for a specified value name associated with an open registry key.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regqueryvalueexw
"""
RegQueryValueEx.argtypes = (
	HKEY,  # hKey
	LPCWSTR,  # lpValueName
	POINTER(DWORD),  # lpReserved
	POINTER(DWORD),  # lpType
	c_void_p,  # lpData
	POINTER(DWORD),  # lpcbData
)
RegQueryValueEx.restype = LONG
