# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by shlwapi.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_uint,
	c_void_p,
	c_wchar_p,
	c_wchar,
	POINTER,
	HRESULT,
	windll,
)


dll = windll.shlwapi


SHLoadIndirectString = dll.SHLoadIndirectString
"""
Extracts a specified text resource when given an indirect string.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shlwapi/nf-shlwapi-shloadindirectstring
"""
SHLoadIndirectString.restype = HRESULT
SHLoadIndirectString.argtypes = (
	c_wchar_p,  # pszSource: The indirect string to extract
	POINTER(c_wchar),  # pszOutBuf: Buffer to receive the extracted string
	c_uint,  # cchOutBuf: Size of the output buffer in characters
	c_void_p,  # ppvReserved: Reserved, must be NULL
)
