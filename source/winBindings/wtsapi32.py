# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by wtsapi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	POINTER,
	c_int,
	c_void_p,
	windll,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	HANDLE,
	LPWSTR,
)


dll = windll.wtsapi32


WTSFreeMemory = dll.WTSFreeMemory
"""
Frees memory allocated by a Windows Terminal Services function.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsfreememory
"""
WTSFreeMemory.restype = None
WTSFreeMemory.argtypes = (
	c_void_p,  # pMemory: Pointer to the memory to free
)

WTSQuerySessionInformation = dll.WTSQuerySessionInformationW
"""
Retrieves session information for the specified session on the specified Remote Desktop Session Host server.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsquerysessioninformationw
"""
WTSQuerySessionInformation.restype = BOOL
WTSQuerySessionInformation.argtypes = (
	HANDLE,  # hServer: Handle to the Remote Desktop Session Host server
	DWORD,  # SessionId: Session identifier
	c_int,  # WTSInfoClass: Type of information to retrieve (WTS_INFO_CLASS)
	POINTER(LPWSTR),  # ppBuffer: Pointer to a variable that receives a pointer to the requested information
	POINTER(DWORD),  # pBytesReturned: Pointer to a variable that receives the size of the data returned
)
