# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by cfgmgr32.dll, and supporting data structurs and enumerations."""

from ctypes import c_wchar_p, windll
from ctypes.wintypes import DWORD, ULONG

dll = windll.cfgmgr32

CM_Get_Device_ID = dll.CM_Get_Device_IDW
CM_Get_Device_ID.argtypes = (DWORD, c_wchar_p, ULONG, ULONG)
CM_Get_Device_ID.restype = DWORD
