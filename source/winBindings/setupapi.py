# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""https://learn.microsoft.com/en-us/windows/win32/api/setupapi/"""

import ctypes
from ctypes.wintypes import BOOL, DWORD, HWND, PDWORD, ULONG

from comtypes import GUID

_SETUPAPI = ctypes.windll.setupapi

HDEVINFO = ctypes.c_void_p


class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
	_fields_ = (
		("cbSize", DWORD),
		("InterfaceClassGuid", GUID),
		("Flags", DWORD),
		("Reserved", ctypes.POINTER(ULONG)),
	)

	def __str__(self):
		return f"InterfaceClassGuid:{self.InterfaceClassGuid} Flags:{self.Flags}"


PSP_DEVICE_INTERFACE_DATA = ctypes.POINTER(SP_DEVICE_INTERFACE_DATA)


PSP_DEVICE_INTERFACE_DETAIL_DATA = ctypes.c_void_p


class SP_DEVINFO_DATA(ctypes.Structure):
	_fields_ = (
		("cbSize", DWORD),
		("ClassGuid", GUID),
		("DevInst", DWORD),
		("Reserved", ctypes.POINTER(ULONG)),
	)

	def __str__(self):
		return f"ClassGuid:{self.ClassGuid} DevInst:{self.DevInst}"


PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)


class DEVPROPKEY(ctypes.Structure):
	_fields_ = (
		("DEVPROPGUID", GUID),
		("DEVPROPID", ULONG),
	)


def validHandle_errcheck(res, func, args):
	if res == 0:
		raise ctypes.WinError()
	return res


SetupDiDestroyDeviceInfoList = _SETUPAPI.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = (HDEVINFO,)
SetupDiDestroyDeviceInfoList.restype = BOOL

SetupDiGetClassDevs = _SETUPAPI.SetupDiGetClassDevsW
SetupDiGetClassDevs.argtypes = (ctypes.POINTER(GUID), ctypes.c_wchar_p, HWND, DWORD)
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = validHandle_errcheck  # HDEVINFO

SetupDiGetDeviceProperty = _SETUPAPI.SetupDiGetDevicePropertyW
SetupDiGetDeviceProperty.argtypes = (
	HDEVINFO,  # [in]            HDEVINFO         DeviceInfoSet
	PSP_DEVINFO_DATA,  # [in]            PSP_DEVINFO_DATA DeviceInfoData
	ctypes.POINTER(DEVPROPKEY),  # [in]            const DEVPROPKEY *PropertyKey
	PDWORD,  # [out]           DEVPROPTYPE      *PropertyType
	ctypes.c_void_p,  # [out, optional] PBYTE            PropertyBuffer
	DWORD,  # [in]            DWORD            PropertyBufferSize
	PDWORD,  # [out, optional] PDWORD           RequiredSize
	DWORD,  # [in]            DWORD            Flags
)
SetupDiGetDeviceProperty.restype = BOOL

SetupDiEnumDeviceInterfaces = _SETUPAPI.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.argtypes = (
	HDEVINFO,
	PSP_DEVINFO_DATA,
	ctypes.POINTER(GUID),
	DWORD,
	PSP_DEVICE_INTERFACE_DATA,
)
SetupDiEnumDeviceInterfaces.restype = BOOL

SetupDiGetDeviceInterfaceDetail = _SETUPAPI.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetail.argtypes = (
	HDEVINFO,
	PSP_DEVICE_INTERFACE_DATA,
	PSP_DEVICE_INTERFACE_DETAIL_DATA,
	DWORD,
	PDWORD,
	PSP_DEVINFO_DATA,
)
SetupDiGetDeviceInterfaceDetail.restype = BOOL

SetupDiGetDeviceRegistryProperty = _SETUPAPI.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryProperty.argtypes = (
	HDEVINFO,
	PSP_DEVINFO_DATA,
	DWORD,
	PDWORD,
	ctypes.c_void_p,
	DWORD,
	PDWORD,
)
SetupDiGetDeviceRegistryProperty.restype = BOOL

SetupDiEnumDeviceInfo = _SETUPAPI.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = (HDEVINFO, DWORD, PSP_DEVINFO_DATA)
SetupDiEnumDeviceInfo.restype = BOOL
