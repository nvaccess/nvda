# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by cfgmgr32.dll, and supporting data structures and enumerations."""

from ctypes import c_wchar_p, windll
from ctypes.wintypes import DWORD, ULONG

dll = windll.cfgmgr32

CR_SUCCESS = 0
MAX_DEVICE_ID_LEN = 200

CM_Get_Device_ID = dll.CM_Get_Device_IDW
"""
Retrieves the device instance ID for a specified device instance on the local machine.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/cfgmgr32/nf-cfgmgr32-cm_get_device_idw
"""
CM_Get_Device_ID.argtypes = (
	DWORD,  # dnDevInst
	c_wchar_p,  # Buffer
	ULONG,  # BufferLen
	ULONG,  # ulFlags
)
CM_Get_Device_ID.restype = DWORD
