# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by hid.dll, and supporting data structures and enumerations."""

from ctypes import POINTER, Structure, c_void_p, sizeof, windll
from ctypes.wintypes import BOOLEAN, HANDLE, ULONG, USHORT

from comtypes import GUID
from hidpi import HIDP_CAPS, NTSTATUS

dll = windll.hid


class HIDD_ATTRIBUTES(Structure):
	"""
	The HIDD_ATTRIBUTES structure contains vendor information about a HIDClass device.

	..seealso::
		https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/ns-hidsdi-_hidd_attributes
	"""

	_fields_ = (
		("Size", ULONG),
		("VendorID", USHORT),
		("ProductID", USHORT),
		("VersionNumber", USHORT),
	)

	def __init__(self, **kwargs):
		super().__init__(Size=sizeof(HIDD_ATTRIBUTES), **kwargs)


PHID_ATTRIBUTES = POINTER(HIDD_ATTRIBUTES)

HidD_GetAttributes = dll.HidD_GetAttributes
"""
The HidD_GetAttributes routine returns the attributes of a specified top-level collection.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_getattributes
"""
HidD_GetAttributes.argtypes = (
	HANDLE,  # HidDeviceObject
	PHID_ATTRIBUTES,  # Attributes
)
HidD_GetAttributes.restype = BOOLEAN

HidD_GetManufacturerString = dll.HidD_GetManufacturerString
"""
Returns a top-level collection's embedded string that identifies the manufacturer.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_getmanufacturerstring
"""
HidD_GetManufacturerString.argtypes = (
	HANDLE,  # HidDeviceObject
	c_void_p,  # Buffer
	ULONG,  # BufferLength
)
HidD_GetManufacturerString.restype = BOOLEAN

HidD_GetProductString = dll.HidD_GetProductString
"""
The HidD_GetProductString routine returns the embedded string of a top-level collection that identifies the manufacturer's product.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_getproductstring
"""
HidD_GetProductString.argtypes = (
	HANDLE,  # HidDeviceObject
	c_void_p,  # Buffer
	ULONG,  # BufferLength
)
HidD_GetProductString.restype = BOOLEAN

PHIDP_PREPARSED_DATA = c_void_p

HidD_GetPreparsedData = dll.HidD_GetPreparsedData
"""
The HidD_GetPreparsedData routine returns a top-level collection's preparsed data.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_getpreparseddata
"""
HidD_GetPreparsedData.argtypes = (
	HANDLE,  # HidDeviceObject
	PHIDP_PREPARSED_DATA,  # PreparsedData
)
HidD_GetPreparsedData.restype = BOOLEAN

HidD_FreePreparsedData = dll.HidD_FreePreparsedData
"""
The HidD_FreePreparsedData routine releases the resources that the HID class driver allocated to hold a top-level collection's preparsed data.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-Hidd_freepreparseddata
"""
HidD_FreePreparsedData.argtypes = (
	PHIDP_PREPARSED_DATA,  # PreparsedData
)
HidD_FreePreparsedData.restype = BOOLEAN

PHIDP_CAPS = POINTER(HIDP_CAPS)

HidP_GetCaps = dll.HidP_GetCaps
"""
Returns a top-level collection's HIDP_CAPS structure.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_getcaps
"""
HidP_GetCaps.argtypes = (
	PHIDP_PREPARSED_DATA,  # PreparsedData
	PHIDP_CAPS,  # Capabilities
)
HidP_GetCaps.restype = NTSTATUS

LPGUID = POINTER(GUID)

HidD_GetHidGuid = dll.HidD_GetHidGuid
"""
Returns the device interface GUID for HIDClass devices.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_gethidguid
"""
HidD_GetHidGuid.argtypes = (
	LPGUID,  # HidGuid
)
HidD_GetHidGuid.restype = None
