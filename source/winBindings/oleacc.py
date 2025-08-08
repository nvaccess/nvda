# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by oleacc.dll, and supporting data structures and enumerations."""

from ctypes import (
	windll,
)
from ctypes.wintypes import (
	HANDLE,
	HWND,
)
from typing import Annotated
from utils.ctypesUtils import (
	dllFunc,
)

dll = windll.oleacc


@dllFunc(dll, annotateOriginalCFunc=True)
def GetProcessHandleFromHwnd(windowHandle: int | HWND) -> Annotated[int, HANDLE]:
	"""
	Retrieves a process handle from a window handle.
	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/winauto/getprocesshandlefromhwnd
	"""
