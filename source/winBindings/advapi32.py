# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by advapi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	windll,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	HANDLE,
	HKEY,
	LONG,
)
from typing import (
	Annotated,
)
from utils.ctypesUtils import (
	dllFunc,
	Pointer,
)

__all__ = (
	"OpenProcessToken",
	"RegCloseKey",
)


dll = windll.advapi32


@dllFunc(dll, annotateOriginalCFunc=True)
def OpenProcessToken(
	ProcessHandle: int | HANDLE,
	DesiredAccess: int | DWORD,
	TokenHandle: Pointer[HANDLE] | HANDLE,
) -> Annotated[int, BOOL]:
	"""
	Opens the access token associated with a process.
	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
	"""


@dllFunc(dll, annotateOriginalCFunc=True)
def RegCloseKey(hkey: int | HKEY) -> Annotated[int, LONG]:
	"""
	Closes a handle to the specified registry key.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regclosekey
	"""
