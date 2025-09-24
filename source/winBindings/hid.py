# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by hid.dll, and supporting data structures and enumerations."""

from ctypes import (
	WINFUNCTYPE,
	POINTER,
	Structure,
	c_void_p,
	sizeof,
	windll,
)
from ctypes.wintypes import (
	BOOLEAN,
	HANDLE,
	ULONG,
	USHORT,
	PCHAR,
	PULONG,
	PUSHORT,
)
from comtypes import GUID
from hidpi import (
	HIDP_CAPS,
	NTSTATUS,
	HIDP_REPORT_TYPE,
	USAGE,
	HIDP_DATA,
	HIDP_VALUE_CAPS,
	HIDP_BUTTON_CAPS,
)

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

HidD_GetAttributes = WINFUNCTYPE(None)(('HidD_GetAttributes', dll))
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

HidD_GetManufacturerString = WINFUNCTYPE(None)(('HidD_GetManufacturerString', dll))
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

HidD_GetProductString = WINFUNCTYPE(None)(('HidD_GetProductString', dll))
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

HidD_GetPreparsedData = WINFUNCTYPE(None)(('HidD_GetPreparsedData', dll))
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

HidD_FreePreparsedData = WINFUNCTYPE(None)(('HidD_FreePreparsedData', dll))
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

HidP_GetCaps = WINFUNCTYPE(None)(('HidP_GetCaps', dll))
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

HidD_GetHidGuid = WINFUNCTYPE(None)(('HidD_GetHidGuid', dll))
"""
Returns the device interface GUID for HIDClass devices.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_gethidguid
"""
HidD_GetHidGuid.argtypes = (
	LPGUID,  # HidGuid
)
HidD_GetHidGuid.restype = None


HidP_MaxUsageListLength = WINFUNCTYPE(None)(('HidP_MaxUsageListLength', dll))
"""
returns the maximum number of HID usages that HidP_GetUsages can return for a specified type of HID report and a specified top-level collection.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_maxusagelistlength
"""
HidP_MaxUsageListLength.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	USAGE,  # UsagePage
	PHIDP_PREPARSED_DATA,  # PreparsedData
)
HidP_MaxUsageListLength.restype = ULONG


HidP_MaxDataListLength = WINFUNCTYPE(None)(('HidP_MaxDataListLength', dll))
"""
Returns the maximum number of HID data structures that HidP_GetData can return for a specified type of HID report and a specified top-level collection.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_maxdatalistlength
"""
HidP_MaxDataListLength.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	PHIDP_PREPARSED_DATA,  # PreparsedData
)
HidP_MaxDataListLength.restype = ULONG


HidP_GetData = WINFUNCTYPE(None)(('HidP_GetData', dll))
"""
Extracts data from a HID report for a specified report type.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_getdata
"""
HidP_GetData.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	POINTER(HIDP_DATA),  # DataList
	PULONG,  # DataLength
	PHIDP_PREPARSED_DATA,  # PreparsedData
	PCHAR,  # Report
	ULONG,  # ReportLength
)
HidP_GetData.restype = NTSTATUS


HidP_GetUsages = WINFUNCTYPE(None)(('HidP_GetUsages', dll))
"""
Extracts usages from a HID report for a specified report type and usage page.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_getusages
"""
HidP_GetUsages.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	USAGE,  # UsagePage
	USHORT,  # LinkCollection
	POINTER(USAGE),  # UsageList
	PULONG,  # UsageLength
	PHIDP_PREPARSED_DATA,  # PreparsedData
	PCHAR,  # Report
	ULONG,  # ReportLength
)
HidP_GetUsages.restype = NTSTATUS

HidP_SetUsageValueArray = WINFUNCTYPE(None)(('HidP_SetUsageValueArray', dll))
"""
Sets an array of usage values in a HID report for a specified report type and usage page.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_setusagevaluearray
"""
HidP_SetUsageValueArray.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	USAGE,  # UsagePage
	USHORT,  # LinkCollection
	USAGE,  # Usage
	PCHAR,  # UsageValue
	USHORT,  # UsageValueByteLenth
	PHIDP_PREPARSED_DATA,  # PreparsedData
	PCHAR,  # Report
	ULONG,  # ReportLength
)
HidP_SetUsageValueArray.restype = NTSTATUS

HidP_GetButtonCaps = WINFUNCTYPE(None)(('HidP_GetButtonCaps', dll))
"""
Extracts button capability information from a HID report for a specified report type and usage page.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_getbuttoncaps
"""
HidP_GetButtonCaps.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	POINTER(HIDP_BUTTON_CAPS),  # ButtonCaps
	PUSHORT,  # ButtonCapsLength
	PHIDP_PREPARSED_DATA,  # PreparsedData
)
HidP_GetButtonCaps.restype = NTSTATUS


HidP_GetValueCaps = WINFUNCTYPE(None)(('HidP_GetValueCaps', dll))
"""
Extracts value capability information from a HID report for a specified report type and usage page.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/nf-hidpi-hidp_getvaluecaps
"""
HidP_GetValueCaps.argtypes = (
	HIDP_REPORT_TYPE,  # ReportType
	POINTER(HIDP_VALUE_CAPS),  # ValueCaps
	PUSHORT,  # ValueCapsLength
	PHIDP_PREPARSED_DATA,  # PreparsedData
)
HidP_GetValueCaps.restype = NTSTATUS

HidD_GetFeature = WINFUNCTYPE(None)(('HidD_GetFeature', dll))
"""
Retrieves a feature report from a top-level collection.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_getfeature
"""
HidD_GetFeature.argtypes = (
	HANDLE,  # HidDeviceObject
	c_void_p,  # ReportBuffer
	ULONG,  # ReportBufferLength
)
HidD_GetFeature.restype = BOOLEAN

HidD_SetFeature = WINFUNCTYPE(None)(('HidD_SetFeature', dll))
"""
The HidD_SetFeature routine sends a feature report to a top-level collection.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_setfeature
"""
HidD_SetFeature.argtypes = (
	HANDLE,  # HidDeviceObject
	c_void_p,  # ReportBuffer
	ULONG,  # ReportBufferLength
)
HidD_SetFeature.restype = BOOLEAN

HidD_SetOutputReport = WINFUNCTYPE(None)(('HidD_SetOutputReport', dll))
"""
The HidD_SetOutputReport routine sends an output report to a top-level collection.

..seealso::
	https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidsdi/nf-hidsdi-hidd_setoutputreport
"""
HidD_SetOutputReport.argtypes = (
	HANDLE,  # HidDeviceObject
	c_void_p,  # ReportBuffer
	ULONG,  # ReportBufferLength
)
HidD_SetOutputReport.restype = BOOLEAN
