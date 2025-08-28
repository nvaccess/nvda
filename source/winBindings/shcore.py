# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by shcore.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_long,
	windll,
)
from comtypes import HRESULT


dll = windll.shcore


SetProcessDpiAwareness = dll.SetProcessDpiAwareness
"""
Sets the current process to a specified dots per inch (DPI) awareness level. The DPI awareness levels are from the PROCESS_DPI_AWARENESS enumeration.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness
"""
SetProcessDpiAwareness.restype = HRESULT
SetProcessDpiAwareness.argtypes = (
	c_long,  # value: The DPI awareness level to set. Possible values are from the PROCESS_DPI_AWARENESS enumeration.
)
