# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by advapi32.dll, and supporting data structurs and enumerations."""

from ctypes import (
	POINTER,
	windll,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	HANDLE,
)

__all__ = ("OpenProcessToken",)


dll = windll.advapi32
OpenProcessToken = dll.OpenProcessToken
"""
opens the access token associated with a process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
"""
OpenProcessToken.argtypes = (
	HANDLE,  # ProcessHandle
	DWORD,  # DesiredAccess
	POINTER(HANDLE),  # TokenHandle
)
OpenProcessToken.restype = BOOL
