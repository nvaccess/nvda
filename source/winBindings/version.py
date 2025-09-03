# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by version.dll, and supporting data structures and enumerations."""

from ctypes import (
	POINTER,
	c_uint,
	c_void_p,
	c_wchar_p,
	windll,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
)


dll = windll.version


GetFileVersionInfoSize = dll.GetFileVersionInfoSizeW
"""
Determines whether the operating system can retrieve version information for a specified file.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winver/nf-winver-getfileversioninfosizew
"""
GetFileVersionInfoSize.restype = DWORD
GetFileVersionInfoSize.argtypes = (
	c_wchar_p,  # lptstrFilename: Pointer to a null-terminated string that specifies the name of the file
	POINTER(DWORD),  # lpdwHandle: Pointer to a variable that the function sets to zero (can be NULL)
)

GetFileVersionInfo = dll.GetFileVersionInfoW
"""
Retrieves version information for the specified file.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winver/nf-winver-getfileversioninfow
"""
GetFileVersionInfo.restype = BOOL
GetFileVersionInfo.argtypes = (
	c_wchar_p,  # lptstrFilename: Pointer to a null-terminated string that specifies the name of the file
	DWORD,  # dwHandle: This parameter is ignored
	DWORD,  # dwLen: Specifies the size, in bytes, of the buffer pointed to by the lpData parameter
	c_void_p,  # lpData: Pointer to a buffer that receives the file-version information
)

VerQueryValue = dll.VerQueryValueW
"""
Retrieves specified version information from the specified version-information resource.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winver/nf-winver-verqueryvaluew
"""
VerQueryValue.restype = BOOL
VerQueryValue.argtypes = (
	c_void_p,  # pBlock: Pointer to the buffer containing the version-information resource
	c_wchar_p,  # lpSubBlock: Pointer to a null-terminated string that specifies the version-information value to retrieve
	POINTER(
		c_void_p,
	),  # lplpBuffer: When the function returns, points to the address of the requested version information
	POINTER(
		c_uint,
	),  # puLen: When the function returns, points to the length, in characters, of the requested version information
)
