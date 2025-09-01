# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by gdi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_int,
	windll,
)
from ctypes.wintypes import (
	HDC,
)


dll = windll.gdi32


GetDeviceCaps = dll.GetDeviceCaps
"""
Retrieves device-specific information for the specified device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdevicecaps
"""
GetDeviceCaps.restype = c_int
GetDeviceCaps.argtypes = (
	HDC,    # hdc: A handle to the DC
	c_int,  # nIndex: The item to be returned
)
