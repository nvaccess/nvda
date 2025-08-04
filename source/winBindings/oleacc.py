# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by oleacc.dll, and supporting data structures and enumerations."""

from ctypes import (
	windll,
)
from ctypes.wintypes import (
	HANDLE,
	HWND,
)


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
