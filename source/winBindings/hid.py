from ctypes import POINTER, Structure, c_void_p, sizeof, windll
from ctypes.wintypes import BOOLEAN, HANDLE, ULONG, USHORT

from comtypes import GUID
from hidpi import HIDP_CAPS, NTSTATUS

dll = windll.hid


class HIDD_ATTRIBUTES(Structure):
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
HidD_GetAttributes.argtypes = (HANDLE, PHID_ATTRIBUTES)
HidD_GetAttributes.restype = BOOLEAN

HidD_GetManufacturerString = dll.HidD_GetManufacturerString
HidD_GetManufacturerString.argtypes = (HANDLE, c_void_p, ULONG)
HidD_GetManufacturerString.restype = BOOLEAN

HidD_GetProductString = dll.HidD_GetProductString
HidD_GetProductString.argtypes = (HANDLE, c_void_p, ULONG)
HidD_GetProductString.restype = BOOLEAN

PHIDP_PREPARSED_DATA = c_void_p

HidD_GetPreparsedData = dll.HidD_GetPreparsedData
HidD_GetPreparsedData.argtypes = (HANDLE, PHIDP_PREPARSED_DATA)
HidD_GetPreparsedData.restype = BOOLEAN

PHIDP_CAPS = POINTER(HIDP_CAPS)

HidP_GetCaps = dll.HidP_GetCaps
HidP_GetCaps.argtypes = (PHIDP_PREPARSED_DATA, PHIDP_CAPS)
HidP_GetCaps.restype = NTSTATUS

HidD_FreePreparsedData = dll.HidD_FreePreparsedData
HidD_FreePreparsedData.argtypes = (PHIDP_PREPARSED_DATA,)
HidD_FreePreparsedData.restype = BOOLEAN

LPGUID = POINTER(GUID)

HidD_GetHidGuid = dll.HidD_GetHidGuid
HidD_GetHidGuid.argtypes = (LPGUID,)
HidD_GetHidGuid.restype = None
