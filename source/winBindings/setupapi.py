# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by setupapi.dll, and supporting data structures and enumerations."""

from ctypes import POINTER, Structure, WinError, c_void_p, c_wchar_p, windll
from ctypes.wintypes import BOOL, DWORD, HKEY, HWND, PDWORD, ULONG
from comtypes import GUID

dll = windll.setupapi


HDEVINFO = c_void_p


class DEVPROPKEY(Structure):
	_fields_ = (
		("DEVPROPGUID", GUID),
		("DEVPROPID", ULONG),
	)


class SP_DEVINFO_DATA(Structure):
	_fields_ = (
		("cbSize", DWORD),
		("ClassGuid", GUID),
		("DevInst", DWORD),
		("Reserved", POINTER(ULONG)),
	)

	def __str__(self):
		return f"ClassGuid:{self.ClassGuid} DevInst:{self.DevInst}"


PSP_DEVINFO_DATA = POINTER(SP_DEVINFO_DATA)


class SP_DEVICE_INTERFACE_DATA(Structure):
	_fields_ = (
		("cbSize", DWORD),
		("InterfaceClassGuid", GUID),
		("Flags", DWORD),
		("Reserved", POINTER(ULONG)),
	)

	def __str__(self):
		return f"InterfaceClassGuid:{self.InterfaceClassGuid} Flags:{self.Flags}"


PSP_DEVICE_INTERFACE_DATA = POINTER(SP_DEVICE_INTERFACE_DATA)

PSP_DEVICE_INTERFACE_DETAIL_DATA = c_void_p


SetupDiDestroyDeviceInfoList = dll.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = (HDEVINFO,)
SetupDiDestroyDeviceInfoList.restype = BOOL


def _validHandle_errcheck(res, func, args):
	if res == 0:
		raise WinError()
	return res


SetupDiGetClassDevs = dll.SetupDiGetClassDevsW
SetupDiGetClassDevs.argtypes = (POINTER(GUID), c_wchar_p, HWND, DWORD)
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = _validHandle_errcheck  # HDEVINFO

SetupDiGetDeviceProperty = dll.SetupDiGetDevicePropertyW
SetupDiGetDeviceProperty.argtypes = (
	HDEVINFO,  # [in]            HDEVINFO         DeviceInfoSet
	PSP_DEVINFO_DATA,  # [in]            PSP_DEVINFO_DATA DeviceInfoData
	POINTER(DEVPROPKEY),  # [in]            const DEVPROPKEY *PropertyKey
	PDWORD,  # [out]           DEVPROPTYPE      *PropertyType
	c_void_p,  # [out, optional] PBYTE            PropertyBuffer
	DWORD,  # [in]            DWORD            PropertyBufferSize
	PDWORD,  # [out, optional] PDWORD           RequiredSize
	DWORD,  # [in]            DWORD            Flags
)
SetupDiGetDeviceProperty.restype = BOOL

SetupDiEnumDeviceInterfaces = dll.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.argtypes = (
	HDEVINFO,
	PSP_DEVINFO_DATA,
	POINTER(GUID),
	DWORD,
	PSP_DEVICE_INTERFACE_DATA,
)
SetupDiEnumDeviceInterfaces.restype = BOOL

SetupDiGetDeviceInterfaceDetail = dll.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetail.argtypes = (
	HDEVINFO,
	PSP_DEVICE_INTERFACE_DATA,
	PSP_DEVICE_INTERFACE_DETAIL_DATA,
	DWORD,
	PDWORD,
	PSP_DEVINFO_DATA,
)
SetupDiGetDeviceInterfaceDetail.restype = BOOL

SetupDiGetDeviceRegistryProperty = dll.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryProperty.argtypes = (
	HDEVINFO,
	PSP_DEVINFO_DATA,
	DWORD,
	PDWORD,
	c_void_p,
	DWORD,
	PDWORD,
)
SetupDiGetDeviceRegistryProperty.restype = BOOL

SetupDiEnumDeviceInfo = dll.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = (HDEVINFO, DWORD, PSP_DEVINFO_DATA)
SetupDiEnumDeviceInfo.restype = BOOL

SetupDiOpenDevRegKey = dll.SetupDiOpenDevRegKey
SetupDiOpenDevRegKey.argTypes = (HDEVINFO, PSP_DEVINFO_DATA, DWORD, DWORD, DWORD, DWORD)
SetupDiOpenDevRegKey.restype = HKEY
