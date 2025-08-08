# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by ole32.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_voidp,
	windll,
)
from ctypes.wintypes import (
	LPVOID,
)


dll = windll.ole32


CoTaskMemFree = dll.CoTaskMemFree
"""
Frees a block of task memory previously allocated through a call to the CoTaskMemAlloc or CoTaskMemRealloc function.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cotaskmemfree
"""
CoTaskMemFree.restype = c_voidp
CoTaskMemFree.argtypes = (
	LPVOID,  # pv: A pointer to the memory block to be freed.
)
