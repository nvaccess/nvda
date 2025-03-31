# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""https://learn.microsoft.com/en-us/windows/win32/api/cfgmgr32/"""

import ctypes
from ctypes.wintypes import DWORD, ULONG

CM_Get_Device_ID = ctypes.windll.cfgmgr32.CM_Get_Device_IDW
CM_Get_Device_ID.argtypes = (DWORD, ctypes.c_wchar_p, ULONG, ULONG)
CM_Get_Device_ID.restype = DWORD
