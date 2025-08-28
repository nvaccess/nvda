# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by UIAutomationCore.dll, and supporting data structures and enumerations."""

from ctypes import windll
from ctypes.wintypes import (
	BOOL,
	HWND,
)

__all__ = ("UiaHasServerSideProvider",)


dll = windll.UIAutomationCore

UiaHasServerSideProvider = dll.UiaHasServerSideProvider
"""
Returns a Boolean value that indicates whether a window has a Microsoft UI Automation server-side provider.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiahasserversideprovider
"""
UiaHasServerSideProvider.argtypes = (HWND,)
UiaHasServerSideProvider.restype = BOOL
