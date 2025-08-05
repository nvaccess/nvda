from ctypes import POINTER, Structure, c_ulonglong, sizeof, windll
from ctypes.wintypes import BOOL, DWORD, HANDLE, ULONG, WCHAR
from winKernel import SYSTEMTIME

cpl = windll["bthprops.cpl"]

BLUETOOTH_ADDRESS = c_ulonglong
BLUETOOTH_MAX_NAME_SIZE = 248


class BLUETOOTH_DEVICE_INFO(Structure):
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
BluetoothGetDeviceInfo.argtypes = (HANDLE, BLUETOOTH_DEVICE_INFO_P)
BluetoothGetDeviceInfo.restype = DWORD
