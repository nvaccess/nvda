# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by bthprops.cpl, and supporting data structures and enumerations."""

from ctypes import POINTER, Structure, c_ulonglong, sizeof, windll
from ctypes.wintypes import BOOL, DWORD, HANDLE, ULONG, WCHAR

from winKernel import SYSTEMTIME

cpl = windll["bthprops.cpl"]

BLUETOOTH_ADDRESS = c_ulonglong
BLUETOOTH_MAX_NAME_SIZE = 248


class BLUETOOTH_DEVICE_INFO(Structure):
	"""
	Provides information about a Bluetooth device.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/bluetoothapis/ns-bluetoothapis-bluetooth_device_info_struct
	"""

	_fields_ = (
		("dwSize", DWORD),
		("address", BLUETOOTH_ADDRESS),
		("ulClassofDevice", ULONG),
		("fConnected", BOOL),
		("fRemembered", BOOL),
		("fAuthenticated", BOOL),
		("stLastSeen", SYSTEMTIME),
		("stLastUsed", SYSTEMTIME),
		("szName", WCHAR * BLUETOOTH_MAX_NAME_SIZE),
	)

	def __init__(self, **kwargs):
		super().__init__(dwSize=sizeof(self), **kwargs)


BLUETOOTH_DEVICE_INFO_P = POINTER(BLUETOOTH_DEVICE_INFO)


BluetoothGetDeviceInfo = cpl.BluetoothGetDeviceInfo
"""
Retrieves information about a remote Bluetooth device which has been identified through a successful device inquiry function call.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/bluetoothapis/nf-bluetoothapis-bluetoothgetdeviceinfo
"""
BluetoothGetDeviceInfo.argtypes = (
	HANDLE,  # hRadio
	BLUETOOTH_DEVICE_INFO_P,  # pbtdi
)
BluetoothGetDeviceInfo.restype = DWORD
