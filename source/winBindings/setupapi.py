# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by setupapi.dll, and supporting data structures and enumerations."""

from ctypes import POINTER, Structure, WinError, c_void_p, c_wchar_p, sizeof, windll
from ctypes.wintypes import BOOL, DWORD, HKEY, HWND, PDWORD, PULONG, ULONG, WCHAR
from enum import IntEnum

from comtypes import GUID

dll = windll.setupapi


class DIGCF(IntEnum):
	"""Possible flags for the ``Flags`` parameter of ``SetupDiGetClassDevs``."""

	PRESENT = 0x02
	"""Return only devices that are currently present in a system."""

	DEVICEINTERFACE = 0x10
	"""Return devices that support device interfaces for the specified device interface classes."""


class SPDRP(IntEnum):
	"""Possible values for the ``Property`` parameter to ``SetupDiGetDeviceRegistryProperty``."""

	DEVICEDESC = 0x00
	"""The function retrieves a ``REG_SZ`` string that contains the description of a device."""

	HARDWAREID = 0x01
	"""The function retrieves a ``REG_MULTI_SZ`` string that contains the list of hardware IDs for a device."""

	FRIENDLYNAME = 0x0C
	"""The function retrieves a ``REG_SZ`` string that contains the friendly name of a device."""

	LOCATION_INFORMATION = 0x0D
	"""The function retrieves a ``REG_SZ`` string that contains the hardware location of a device."""


class DICS_FLAG(IntEnum):
	"""Possible values of the ``Scope`` parameter of ``SetupDiOpenDevRegKey``."""

	GLOBAL = 0x01
	"""Open a key to store global configuration information, rooted at HKEY_LOCAL_MACHINE."""

	CONFIGSPECIFIC = 0x02
	"""Open a key to store hardware profile-specific configuration information, rooted at one of the hardware-profile specific branches, instead of HKEY_LOCAL_MACHINE."""


class DIREG(IntEnum):
	"""Possible values of the ``KeyType`` parameter to ``SetupDiOpenDevRegKey``."""

	DEV = 0x01
	"""Open a hardware key for the device."""

	DRV = 0x02
	"""Open a software key for the device."""


HDEVINFO = c_void_p


class DEVPROPKEY(Structure):
	"""
	Represents a device property key for a device property in the unified device property model.

	..seealso::
		https://learn.microsoft.com/en-us/windows-hardware/drivers/install/devpropkey
	"""

	_fields_ = (
		("DEVPROPGUID", GUID),
		("DEVPROPID", ULONG),
	)


GUID_CLASS_COMPORT = GUID("{86e0d1e0-8089-11d0-9ce4-08003e301f73}")
"""
Identifier for the device interface class for devices that support a 16550 UART-compatible hardware interface.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/install/guid-class-comport
"""

GUID_DEVINTERFACE_USB_DEVICE = GUID("{a5dcbf10-6530-11d2-901f-00c04fb951ed}")
"""
The GUID_DEVINTERFACE_USB_DEVICE device interface class is defined for USB devices that are attached to a USB hub.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/install/guid-devinterface-usb-device
"""

DEVPKEY_Device_BusReportedDeviceDesc = DEVPROPKEY(GUID("{540b947e-8b40-45bc-a8a2-6a0b894cbda2}"), 4)
"""
Represents a string value that was reported by the bus driver for the device instance.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/install/devpkey-device-busreporteddevicedesc
"""


class SP_DEVINFO_DATA(Structure):
	"""
	An SP_DEVINFO_DATA structure defines a device instance that is a member of a device information set.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/setupapi/ns-setupapi-sp_devinfo_data
	"""

	_fields_ = (
		("cbSize", DWORD),
		("ClassGuid", GUID),
		("DevInst", DWORD),
		("Reserved", PULONG),
	)

	def __str__(self):
		return f"ClassGuid:{self.ClassGuid} DevInst:{self.DevInst}"


PSP_DEVINFO_DATA = POINTER(SP_DEVINFO_DATA)


class SP_DEVICE_INTERFACE_DATA(Structure):
	"""
	Defines a device interface in a device information set.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/setupapi/ns-setupapi-sp_device_interface_data
	"""

	_fields_ = (
		("cbSize", DWORD),
		("InterfaceClassGuid", GUID),
		("Flags", DWORD),
		("Reserved", PULONG),
	)

	def __str__(self):
		return f"InterfaceClassGuid:{self.InterfaceClassGuid} Flags:{self.Flags}"


PSP_DEVICE_INTERFACE_DATA = POINTER(SP_DEVICE_INTERFACE_DATA)


class _Dummy(Structure):
	_fields_ = (("d1", DWORD), ("d2", WCHAR))
	# SetupAPI.h in the Windows headers includes pshpack8.h when 64 bit, pshpack1.h otherwise
	_pack_ = 8 if sizeof(c_void_p) == 8 else 1


SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W = sizeof(_Dummy)

PSP_DEVICE_INTERFACE_DETAIL_DATA = c_void_p


SetupDiDestroyDeviceInfoList = dll.SetupDiDestroyDeviceInfoList
"""
Deletes a device information set and frees all associated memory.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdidestroydeviceinfolist
"""
SetupDiDestroyDeviceInfoList.argtypes = (
	HDEVINFO,  # DeviceInfoSet
)
SetupDiDestroyDeviceInfoList.restype = BOOL


def _validHandle_errcheck(res, func, args):
	if res == 0:
		raise WinError()
	return res


SetupDiGetClassDevs = dll.SetupDiGetClassDevsW
"""
Returns a handle to a device information set that contains requested device information elements for a local computer.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdigetclassdevsw
"""
SetupDiGetClassDevs.argtypes = (
	POINTER(GUID),  # ClassGuid
	c_wchar_p,  # Enumerator
	HWND,  # hwndParent
	DWORD,  # Flags
)
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = _validHandle_errcheck  # HDEVINFO

SetupDiGetDeviceProperty = dll.SetupDiGetDevicePropertyW
"""
The SetupDiGetDeviceProperty function retrieves a device instance property.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdigetdevicepropertyw
"""
SetupDiGetDeviceProperty.argtypes = (
	HDEVINFO,  # DeviceInfoSet
	PSP_DEVINFO_DATA,  # DeviceInfoData
	POINTER(DEVPROPKEY),  # PropertyKey
	PDWORD,  # PropertyType
	c_void_p,  # PropertyBuffer
	DWORD,  # PropertyBufferSize
	PDWORD,  # RequiredSize
	DWORD,  # Flags
)
SetupDiGetDeviceProperty.restype = BOOL

SetupDiEnumDeviceInterfaces = dll.SetupDiEnumDeviceInterfaces
"""
Enumerates the device interfaces that are contained in a device information set.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdienumdeviceinterfaces
"""
SetupDiEnumDeviceInterfaces.argtypes = (
	HDEVINFO,  # DeviceInfoSet
	PSP_DEVINFO_DATA,  # DeviceInfoData
	POINTER(GUID),  # InterfaceClassGuid
	DWORD,  # MemberIndex
	PSP_DEVICE_INTERFACE_DATA,  # DeviceInterfaceData
)
SetupDiEnumDeviceInterfaces.restype = BOOL

SetupDiGetDeviceInterfaceDetail = dll.SetupDiGetDeviceInterfaceDetailW
"""
Returns details about a device interface.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdigetdeviceinterfacedetailw
"""
SetupDiGetDeviceInterfaceDetail.argtypes = (
	HDEVINFO,  # DeviceInfoSet
	PSP_DEVICE_INTERFACE_DATA,  # DeviceInterfaceData
	PSP_DEVICE_INTERFACE_DETAIL_DATA,  # DeviceInterfaceDetailData
	DWORD,  # DeviceInterfaceDetailDataSize
	PDWORD,  # RequiredSize
	PSP_DEVINFO_DATA,  # DeviceInfoData
)
SetupDiGetDeviceInterfaceDetail.restype = BOOL

SetupDiGetDeviceRegistryProperty = dll.SetupDiGetDeviceRegistryPropertyW
"""
Retrieves a specified Plug and Play device property.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdigetdeviceregistrypropertyw
"""
SetupDiGetDeviceRegistryProperty.argtypes = (
	HDEVINFO,  # DeviceInfoSet
	PSP_DEVINFO_DATA,  # DeviceInfoData
	DWORD,  # Property
	PDWORD,  # PropertyRegDataType
	c_void_p,  # PropertyBuffer
	DWORD,  # PropertyBufferSize
	PDWORD,  # RequiredSize
)
SetupDiGetDeviceRegistryProperty.restype = BOOL

SetupDiEnumDeviceInfo = dll.SetupDiEnumDeviceInfo
"""
Returns a SP_DEVINFO_DATA structure that specifies a device information element in a device information set.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdienumdeviceinfo
"""
SetupDiEnumDeviceInfo.argtypes = (
	HDEVINFO,  # DeviceInfoSet
	DWORD,  # MemberIndex
	PSP_DEVINFO_DATA,  # DeviceInfoData
)
SetupDiEnumDeviceInfo.restype = BOOL

SetupDiOpenDevRegKey = dll.SetupDiOpenDevRegKey
"""
Opens a registry key for device-specific configuration information.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-setupdiopendevregkey
"""
SetupDiOpenDevRegKey.argtypes = (
	HDEVINFO,  # DeviceInfoSet
	PSP_DEVINFO_DATA,  # DeviceInfoData
	DWORD,  # Scope
	DWORD,  # HwProfile
	DWORD,  # KeyType
	DWORD,  # samDesired
)
SetupDiOpenDevRegKey.restype = HKEY
