# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by mshtml.dll, and supporting data structures and enumerations."""

from ctypes import (
	windll,
	POINTER,
)
from ctypes.wintypes import (
	DWORD,
	HWND,
	LPWSTR,
)
from comtypes import HRESULT
from comtypes.automation import VARIANT
from objidl import IMoniker


dll = windll.mshtml


ShowHTMLDialogEx = dll.ShowHTMLDialogEx
"""
Creates a modeless HTML dialog box.

.. seealso::
	https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa741859(v=vs.85)
"""
ShowHTMLDialogEx.restype = HRESULT
ShowHTMLDialogEx.argtypes = (
	HWND,  # hwndParent: Handle to the parent window
	POINTER(IMoniker),  # pMk: IMoniker interface pointer for the URL
	DWORD,  # dwDialogFlags: Dialog behavior flags
	POINTER(VARIANT),  # pvarArgIn: VARIANT pointer for input arguments
	LPWSTR,  # pchOptions: Dialog options string
	POINTER(VARIANT),  # pvarArgOut: VARIANT pointer for output arguments (can be NULL)
)
