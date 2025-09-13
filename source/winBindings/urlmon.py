# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by urlmon.dll, and supporting data structures and enumerations."""

from ctypes import (
	windll,
	POINTER,
)
from ctypes.wintypes import (
	DWORD,
	LPCWSTR,
)
from comtypes import HRESULT
from objidl import IMoniker


dll = windll.urlmon


CreateURLMonikerEx = dll.CreateURLMonikerEx
"""
Creates a URL moniker from a full or partial URL string.

.. seealso::
	https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms775103(v=vs.85)
"""
CreateURLMonikerEx.restype = HRESULT
CreateURLMonikerEx.argtypes = (
	POINTER(
		IMoniker,
	),  # pMkCtx: Pointer to the IMoniker interface of the URL moniker to use as the base for relative URLs (can be NULL)
	LPCWSTR,  # szURL: String value that contains the URL to be parsed
	POINTER(
		POINTER(IMoniker),
	),  # ppmk: Address of an IMoniker pointer variable that receives the interface pointer to the new URL moniker
	DWORD,  # dwFlags: Flags that control the creation of the URL moniker
)
