# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by wtsapi32.dll, and supporting data structures and enumerations."""

from ctypes import (  # noqa: I001
	WINFUNCTYPE,
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
from typing import Any


try:
	dll = windll.wtsapi32
except (AttributeError, OSError) as e:
	dll = None
	WTSAPI32_LOAD_ERROR: Exception | None = e
else:
	WTSAPI32_LOAD_ERROR = None

WTSAPI32_AVAILABLE: bool = dll is not None
"""True if the Windows Terminal Services API is available."""


def _unavailable(*args: Any, **kwargs: Any) -> None:
	raise OSError("The Windows Terminal Services API is not available")


def _bind(name: str, prototype: Any) -> Any:
	if dll is None:
		return _unavailable
	return prototype((name, dll))


WTSFreeMemory = _bind("WTSFreeMemory", WINFUNCTYPE(None))
"""
Frees memory allocated by a Windows Terminal Services function.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsfreememory
"""
WTSFreeMemory.restype = None
WTSFreeMemory.argtypes = (
	c_void_p,  # pMemory: Pointer to the memory to free
)

WTSQuerySessionInformation = _bind("WTSQuerySessionInformationW", WINFUNCTYPE(None))
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
