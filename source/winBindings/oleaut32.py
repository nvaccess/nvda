# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by oleaut32.dll, and supporting data structures and enumerations."""

from ctypes import (
	POINTER,
	windll,
)
from comtypes import BSTR

# SIZE_T is not in ctypes.wintypes, but it's equivalent to c_size_t


dll = windll.oleaut32


SysFreeString = dll.SysFreeString
"""
Frees a string allocated previously by the SysAllocString, SysAllocStringLen, SysAlloc
StringByteLen, or SysReAllocString functions.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/oleauto/nf-oleauto-sysfreestring
"""
SysFreeString.argtypes = (
	POINTER(BSTR),  # bstrString
)
SysFreeString.restype = None
