# typelib <unable to determine filename>
_lcid = 0  # change this if required
from ctypes import *  # noqa: E402, F403

WSTRING = c_wchar_p  # noqa: F405
from comtypes import IUnknown  # noqa: E402

LONG_PTR = c_int  # noqa: F405
from comtypes import GUID  # noqa: E402
from ctypes import HRESULT  # noqa: E402
from comtypes import COMMETHOD  # noqa: E402
from comtypes import wireHWND  # noqa: E402

UINT_PTR = c_ulong  # noqa: F405
from objidl import IBindCtx, IMoniker  # noqa: E402


class tagDVTARGETDEVICE(Structure):  # noqa: F405
	pass


tagDVTARGETDEVICE._fields_ = [
	("tdSize", c_ulong),  # noqa: F405
	("tdDriverNameOffset", c_ushort),  # noqa: F405
	("tdDeviceNameOffset", c_ushort),  # noqa: F405
	("tdPortNameOffset", c_ushort),  # noqa: F405
	("tdExtDevmodeOffset", c_ushort),  # noqa: F405
	("tdData", POINTER(c_ubyte)),  # noqa: F405
]
assert sizeof(tagDVTARGETDEVICE) == 16, sizeof(tagDVTARGETDEVICE)  # noqa: F405
assert alignment(tagDVTARGETDEVICE) == 4, alignment(tagDVTARGETDEVICE)  # noqa: F405


class _BYTE_BLOB(Structure):  # noqa: F405
	pass


_BYTE_BLOB._fields_ = [
	("clSize", c_ulong),  # noqa: F405
	("abData", POINTER(c_ubyte)),  # noqa: F405
]
assert sizeof(_BYTE_BLOB) == 8, sizeof(_BYTE_BLOB)  # noqa: F405
assert alignment(_BYTE_BLOB) == 4, alignment(_BYTE_BLOB)  # noqa: F405


class tagRECT(Structure):  # noqa: F405
	pass


tagRECT._fields_ = [
	("left", c_int),  # noqa: F405
	("top", c_int),  # noqa: F405
	("right", c_int),  # noqa: F405
	("bottom", c_int),  # noqa: F405
]
assert sizeof(tagRECT) == 16, sizeof(tagRECT)  # noqa: F405
assert alignment(tagRECT) == 4, alignment(tagRECT)  # noqa: F405


class __MIDL_IWinTypes_0003(Union):  # noqa: F405
	pass


class _FLAGGED_BYTE_BLOB(Structure):  # noqa: F405
	pass


__MIDL_IWinTypes_0003._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", POINTER(_FLAGGED_BYTE_BLOB)),  # noqa: F405
	("hInproc64", c_longlong),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0003) == 8, sizeof(__MIDL_IWinTypes_0003)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0003) == 8, alignment(__MIDL_IWinTypes_0003)  # noqa: F405


class _userSTGMEDIUM(Structure):  # noqa: F405
	pass


class _STGMEDIUM_UNION(Structure):  # noqa: F405
	pass


class __MIDL_IAdviseSink_0003(Union):  # noqa: F405
	pass


class _userHMETAFILEPICT(Structure):  # noqa: F405
	pass


class _userHENHMETAFILE(Structure):  # noqa: F405
	pass


class _GDI_OBJECT(Structure):  # noqa: F405
	pass


class _userHGLOBAL(Structure):  # noqa: F405
	pass


__MIDL_IAdviseSink_0003._fields_ = [
	("hMetaFilePict", POINTER(_userHMETAFILEPICT)),  # noqa: F405
	("hHEnhMetaFile", POINTER(_userHENHMETAFILE)),  # noqa: F405
	("hGdiHandle", POINTER(_GDI_OBJECT)),  # noqa: F405
	("hGlobal", POINTER(_userHGLOBAL)),  # noqa: F405
	("lpszFileName", WSTRING),
	("pstm", POINTER(_BYTE_BLOB)),  # noqa: F405
	("pstg", POINTER(_BYTE_BLOB)),  # noqa: F405
]
assert sizeof(__MIDL_IAdviseSink_0003) == 4, sizeof(__MIDL_IAdviseSink_0003)  # noqa: F405
assert alignment(__MIDL_IAdviseSink_0003) == 4, alignment(__MIDL_IAdviseSink_0003)  # noqa: F405
_STGMEDIUM_UNION._fields_ = [
	("tymed", c_ulong),  # noqa: F405
	("u", __MIDL_IAdviseSink_0003),
]
assert sizeof(_STGMEDIUM_UNION) == 8, sizeof(_STGMEDIUM_UNION)  # noqa: F405
assert alignment(_STGMEDIUM_UNION) == 4, alignment(_STGMEDIUM_UNION)  # noqa: F405
_userSTGMEDIUM._fields_ = [
	("__MIDL__IAdviseSink0003", _STGMEDIUM_UNION),
	("pUnkForRelease", POINTER(IUnknown)),  # noqa: F405
]
assert sizeof(_userSTGMEDIUM) == 12, sizeof(_userSTGMEDIUM)  # noqa: F405
assert alignment(_userSTGMEDIUM) == 4, alignment(_userSTGMEDIUM)  # noqa: F405


class tagLOGPALETTE(Structure):  # noqa: F405
	pass


class tagPALETTEENTRY(Structure):  # noqa: F405
	pass


tagLOGPALETTE._pack_ = 2
tagLOGPALETTE._fields_ = [
	("palVersion", c_ushort),  # noqa: F405
	("palNumEntries", c_ushort),  # noqa: F405
	("palPalEntry", POINTER(tagPALETTEENTRY)),  # noqa: F405
]
assert sizeof(tagLOGPALETTE) == 8, sizeof(tagLOGPALETTE)  # noqa: F405
assert alignment(tagLOGPALETTE) == 2, alignment(tagLOGPALETTE)  # noqa: F405
wireASYNC_STGMEDIUM = POINTER(_userSTGMEDIUM)  # noqa: F405


class IEnumOLEVERB(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{00000104-0000-0000-C000-000000000046}")
	_idlflags_ = []


class tagOLEVERB(Structure):  # noqa: F405
	pass


IEnumOLEVERB._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"RemoteNext",
		(["in"], c_ulong, "celt"),  # noqa: F405
		(["out"], POINTER(tagOLEVERB), "rgelt"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pceltFetched"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"Skip",
		(["in"], c_ulong, "celt"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "Reset"),
	COMMETHOD(
		[],
		HRESULT,
		"Clone",
		(["out"], POINTER(POINTER(IEnumOLEVERB)), "ppenum"),  # noqa: F405
	),  # noqa: F405
]


class IEnumUnknown(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{00000100-0000-0000-C000-000000000046}")
	_idlflags_ = []


IEnumUnknown._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"RemoteNext",
		(["in"], c_ulong, "celt"),  # noqa: F405
		(["out"], POINTER(POINTER(IUnknown)), "rgelt"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pceltFetched"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"Skip",
		(["in"], c_ulong, "celt"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "Reset"),
	COMMETHOD(
		[],
		HRESULT,
		"Clone",
		(["out"], POINTER(POINTER(IEnumUnknown)), "ppenum"),  # noqa: F405
	),  # noqa: F405
]


class _RemotableHandle(Structure):  # noqa: F405
	pass


class __MIDL_IWinTypes_0009(Union):  # noqa: F405
	pass


__MIDL_IWinTypes_0009._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", c_int),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0009) == 4, sizeof(__MIDL_IWinTypes_0009)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0009) == 4, alignment(__MIDL_IWinTypes_0009)  # noqa: F405
_RemotableHandle._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0009),
]
assert sizeof(_RemotableHandle) == 8, sizeof(_RemotableHandle)  # noqa: F405
assert alignment(_RemotableHandle) == 4, alignment(_RemotableHandle)  # noqa: F405


class _userHMETAFILE(Structure):  # noqa: F405
	pass


class __MIDL_IWinTypes_0004(Union):  # noqa: F405
	pass


__MIDL_IWinTypes_0004._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", POINTER(_BYTE_BLOB)),  # noqa: F405
	("hInproc64", c_longlong),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0004) == 8, sizeof(__MIDL_IWinTypes_0004)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0004) == 8, alignment(__MIDL_IWinTypes_0004)  # noqa: F405
_userHMETAFILE._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0004),
]
assert sizeof(_userHMETAFILE) == 16, sizeof(_userHMETAFILE)  # noqa: F405
assert alignment(_userHMETAFILE) == 8, alignment(_userHMETAFILE)  # noqa: F405
wireSTGMEDIUM = POINTER(_userSTGMEDIUM)  # noqa: F405


class _userHPALETTE(Structure):  # noqa: F405
	pass


class __MIDL_IWinTypes_0008(Union):  # noqa: F405
	pass


__MIDL_IWinTypes_0008._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", POINTER(tagLOGPALETTE)),  # noqa: F405
	("hInproc64", c_longlong),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0008) == 8, sizeof(__MIDL_IWinTypes_0008)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0008) == 8, alignment(__MIDL_IWinTypes_0008)  # noqa: F405
_userHPALETTE._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0008),
]
assert sizeof(_userHPALETTE) == 16, sizeof(_userHPALETTE)  # noqa: F405
assert alignment(_userHPALETTE) == 8, alignment(_userHPALETTE)  # noqa: F405


class __MIDL_IWinTypes_0007(Union):  # noqa: F405
	pass


class _userBITMAP(Structure):  # noqa: F405
	pass


__MIDL_IWinTypes_0007._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", POINTER(_userBITMAP)),  # noqa: F405
	("hInproc64", c_longlong),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0007) == 8, sizeof(__MIDL_IWinTypes_0007)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0007) == 8, alignment(__MIDL_IWinTypes_0007)  # noqa: F405


class IParseDisplayName(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{0000011A-0000-0000-C000-000000000046}")
	_idlflags_ = []


class IOleContainer(IParseDisplayName):
	_case_insensitive_ = True
	_iid_ = GUID("{0000011B-0000-0000-C000-000000000046}")
	_idlflags_ = []


IParseDisplayName._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"ParseDisplayName",
		(["in"], POINTER(IBindCtx), "pbc"),  # noqa: F405
		(["in"], WSTRING, "pszDisplayName"),
		(["out"], POINTER(c_ulong), "pchEaten"),  # noqa: F405
		(["out"], POINTER(POINTER(IMoniker)), "ppmkOut"),  # noqa: F405
	),  # noqa: F405
]
IOleContainer._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"EnumObjects",
		(["in"], c_ulong, "grfFlags"),  # noqa: F405
		(["out"], POINTER(POINTER(IEnumUnknown)), "ppenum"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"LockContainer",
		(["in"], c_int, "fLock"),  # noqa: F405
	),  # noqa: F405
]


class IOleObject(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{00000112-0000-0000-C000-000000000046}")
	_idlflags_ = []


class IOleClientSite(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{00000118-0000-0000-C000-000000000046}")
	_idlflags_ = []


class IDataObject(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{0000010E-0000-0000-C000-000000000046}")
	_idlflags_ = []


class tagMSG(Structure):  # noqa: F405
	pass


class tagSIZEL(Structure):  # noqa: F405
	pass


class IAdviseSink(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{0000010F-0000-0000-C000-000000000046}")
	_idlflags_ = []


class IEnumSTATDATA(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{00000105-0000-0000-C000-000000000046}")
	_idlflags_ = []


IOleObject._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"SetClientSite",
		(["in"], POINTER(IOleClientSite), "pClientSite"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetClientSite",
		(["out"], POINTER(POINTER(IOleClientSite)), "ppClientSite"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"SetHostNames",
		(["in"], WSTRING, "szContainerApp"),
		(["in"], WSTRING, "szContainerObj"),
	),
	COMMETHOD(
		[],
		HRESULT,
		"Close",
		(["in"], c_ulong, "dwSaveOption"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"SetMoniker",
		(["in"], c_ulong, "dwWhichMoniker"),  # noqa: F405
		(["in"], POINTER(IMoniker), "pmk"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetMoniker",
		(["in"], c_ulong, "dwAssign"),  # noqa: F405
		(["in"], c_ulong, "dwWhichMoniker"),  # noqa: F405
		(["out"], POINTER(POINTER(IMoniker)), "ppmk"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"InitFromData",
		(["in"], POINTER(IDataObject), "pDataObject"),  # noqa: F405
		(["in"], c_int, "fCreation"),  # noqa: F405
		(["in"], c_ulong, "dwReserved"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetClipboardData",
		(["in"], c_ulong, "dwReserved"),  # noqa: F405
		(["out"], POINTER(POINTER(IDataObject)), "ppDataObject"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"DoVerb",
		(["in"], c_int, "iVerb"),  # noqa: F405
		(["in"], POINTER(tagMSG), "lpmsg"),  # noqa: F405
		(["in"], POINTER(IOleClientSite), "pActiveSite"),  # noqa: F405
		(["in"], c_int, "lindex"),  # noqa: F405
		(["in"], wireHWND, "hwndParent"),
		(["in"], POINTER(tagRECT), "lprcPosRect"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"EnumVerbs",
		(["out"], POINTER(POINTER(IEnumOLEVERB)), "ppEnumOleVerb"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "Update"),
	COMMETHOD([], HRESULT, "IsUpToDate"),
	COMMETHOD(
		[],
		HRESULT,
		"GetUserClassID",
		(["out"], POINTER(GUID), "pClsid"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetUserType",
		(["in"], c_ulong, "dwFormOfType"),  # noqa: F405
		(["out"], POINTER(WSTRING), "pszUserType"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"SetExtent",
		(["in"], c_ulong, "dwDrawAspect"),  # noqa: F405
		(["in"], POINTER(tagSIZEL), "psizel"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetExtent",
		(["in"], c_ulong, "dwDrawAspect"),  # noqa: F405
		(["out"], POINTER(tagSIZEL), "psizel"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"Advise",
		(["in"], POINTER(IAdviseSink), "pAdvSink"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pdwConnection"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"Unadvise",
		(["in"], c_ulong, "dwConnection"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"EnumAdvise",
		(["out"], POINTER(POINTER(IEnumSTATDATA)), "ppenumAdvise"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetMiscStatus",
		(["in"], c_ulong, "dwAspect"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pdwStatus"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"SetColorScheme",
		(["in"], POINTER(tagLOGPALETTE), "pLogpal"),  # noqa: F405
	),  # noqa: F405
]


class __MIDL_IWinTypes_0005(Union):  # noqa: F405
	pass


class _remoteMETAFILEPICT(Structure):  # noqa: F405
	pass


__MIDL_IWinTypes_0005._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", POINTER(_remoteMETAFILEPICT)),  # noqa: F405
	("hInproc64", c_longlong),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0005) == 8, sizeof(__MIDL_IWinTypes_0005)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0005) == 8, alignment(__MIDL_IWinTypes_0005)  # noqa: F405
_userHMETAFILEPICT._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0005),
]
assert sizeof(_userHMETAFILEPICT) == 16, sizeof(_userHMETAFILEPICT)  # noqa: F405
assert alignment(_userHMETAFILEPICT) == 8, alignment(_userHMETAFILEPICT)  # noqa: F405
tagOLEVERB._fields_ = [
	("lVerb", c_int),  # noqa: F405
	("lpszVerbName", WSTRING),
	("fuFlags", c_ulong),  # noqa: F405
	("grfAttribs", c_ulong),  # noqa: F405
]
assert sizeof(tagOLEVERB) == 16, sizeof(tagOLEVERB)  # noqa: F405
assert alignment(tagOLEVERB) == 4, alignment(tagOLEVERB)  # noqa: F405


class _userCLIPFORMAT(Structure):  # noqa: F405
	pass


class __MIDL_IWinTypes_0001(Union):  # noqa: F405
	pass


__MIDL_IWinTypes_0001._fields_ = [
	("dwValue", c_ulong),  # noqa: F405
	("pwszName", WSTRING),
]
assert sizeof(__MIDL_IWinTypes_0001) == 4, sizeof(__MIDL_IWinTypes_0001)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0001) == 4, alignment(__MIDL_IWinTypes_0001)  # noqa: F405
_userCLIPFORMAT._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0001),
]
assert sizeof(_userCLIPFORMAT) == 8, sizeof(_userCLIPFORMAT)  # noqa: F405
assert alignment(_userCLIPFORMAT) == 4, alignment(_userCLIPFORMAT)  # noqa: F405
wireCLIPFORMAT = POINTER(_userCLIPFORMAT)  # noqa: F405


class __MIDL_IWinTypes_0006(Union):  # noqa: F405
	pass


__MIDL_IWinTypes_0006._fields_ = [
	("hInproc", c_int),  # noqa: F405
	("hRemote", POINTER(_BYTE_BLOB)),  # noqa: F405
	("hInproc64", c_longlong),  # noqa: F405
]
assert sizeof(__MIDL_IWinTypes_0006) == 8, sizeof(__MIDL_IWinTypes_0006)  # noqa: F405
assert alignment(__MIDL_IWinTypes_0006) == 8, alignment(__MIDL_IWinTypes_0006)  # noqa: F405
_userHENHMETAFILE._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0006),
]
assert sizeof(_userHENHMETAFILE) == 16, sizeof(_userHENHMETAFILE)  # noqa: F405
assert alignment(_userHENHMETAFILE) == 8, alignment(_userHENHMETAFILE)  # noqa: F405


class tagFORMATETC(Structure):  # noqa: F405
	pass


tagFORMATETC._fields_ = [
	("cfFormat", wireCLIPFORMAT),
	("ptd", POINTER(tagDVTARGETDEVICE)),  # noqa: F405
	("dwAspect", c_ulong),  # noqa: F405
	("lindex", c_int),  # noqa: F405
	("tymed", c_ulong),  # noqa: F405
]
assert sizeof(tagFORMATETC) == 20, sizeof(tagFORMATETC)  # noqa: F405
assert alignment(tagFORMATETC) == 4, alignment(tagFORMATETC)  # noqa: F405
_userHGLOBAL._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0003),
]
assert sizeof(_userHGLOBAL) == 16, sizeof(_userHGLOBAL)  # noqa: F405
assert alignment(_userHGLOBAL) == 8, alignment(_userHGLOBAL)  # noqa: F405
IOleClientSite._methods_ = [
	COMMETHOD([], HRESULT, "SaveObject"),
	COMMETHOD(
		[],
		HRESULT,
		"GetMoniker",
		(["in"], c_ulong, "dwAssign"),  # noqa: F405
		(["in"], c_ulong, "dwWhichMoniker"),  # noqa: F405
		(["out"], POINTER(POINTER(IMoniker)), "ppmk"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetContainer",
		(["out"], POINTER(POINTER(IOleContainer)), "ppContainer"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "ShowObject"),
	COMMETHOD(
		[],
		HRESULT,
		"OnShowWindow",
		(["in"], c_int, "fShow"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "RequestNewObjectLayout"),
]


class __MIDL_IAdviseSink_0002(Union):  # noqa: F405
	pass


class _userHBITMAP(Structure):  # noqa: F405
	pass


__MIDL_IAdviseSink_0002._fields_ = [
	("hBitmap", POINTER(_userHBITMAP)),  # noqa: F405
	("hPalette", POINTER(_userHPALETTE)),  # noqa: F405
	("hGeneric", POINTER(_userHGLOBAL)),  # noqa: F405
]
assert sizeof(__MIDL_IAdviseSink_0002) == 4, sizeof(__MIDL_IAdviseSink_0002)  # noqa: F405
assert alignment(__MIDL_IAdviseSink_0002) == 4, alignment(__MIDL_IAdviseSink_0002)  # noqa: F405
_GDI_OBJECT._fields_ = [
	("ObjectType", c_ulong),  # noqa: F405
	("u", __MIDL_IAdviseSink_0002),
]
assert sizeof(_GDI_OBJECT) == 8, sizeof(_GDI_OBJECT)  # noqa: F405
assert alignment(_GDI_OBJECT) == 4, alignment(_GDI_OBJECT)  # noqa: F405


class _userFLAG_STGMEDIUM(Structure):  # noqa: F405
	pass


wireFLAG_STGMEDIUM = POINTER(_userFLAG_STGMEDIUM)  # noqa: F405


class IEnumFORMATETC(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID("{00000103-0000-0000-C000-000000000046}")
	_idlflags_ = []


IDataObject._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"GetData",
		(["in"], POINTER(tagFORMATETC), "pformatetcIn"),  # noqa: F405
		(["out"], POINTER(wireSTGMEDIUM), "pmedium"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"RemoteGetData",
		(["in"], POINTER(tagFORMATETC), "pformatetcIn"),  # noqa: F405
		(["out"], POINTER(wireSTGMEDIUM), "pRemoteMedium"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"RemoteGetDataHere",
		(["in"], POINTER(tagFORMATETC), "pformatetc"),  # noqa: F405
		(["in", "out"], POINTER(wireSTGMEDIUM), "pRemoteMedium"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"QueryGetData",
		(["in"], POINTER(tagFORMATETC), "pformatetc"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"GetCanonicalFormatEtc",
		(["in"], POINTER(tagFORMATETC), "pformatectIn"),  # noqa: F405
		(["out"], POINTER(tagFORMATETC), "pformatetcOut"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"RemoteSetData",
		(["in"], POINTER(tagFORMATETC), "pformatetc"),  # noqa: F405
		(["in"], POINTER(wireFLAG_STGMEDIUM), "pmedium"),  # noqa: F405
		(["in"], c_int, "fRelease"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"EnumFormatEtc",
		(["in"], c_ulong, "dwDirection"),  # noqa: F405
		(["out"], POINTER(POINTER(IEnumFORMATETC)), "ppenumFormatEtc"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"DAdvise",
		(["in"], POINTER(tagFORMATETC), "pformatetc"),  # noqa: F405
		(["in"], c_ulong, "advf"),  # noqa: F405
		(["in"], POINTER(IAdviseSink), "pAdvSink"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pdwConnection"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"DUnadvise",
		(["in"], c_ulong, "dwConnection"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"EnumDAdvise",
		(["out"], POINTER(POINTER(IEnumSTATDATA)), "ppenumAdvise"),  # noqa: F405
	),  # noqa: F405
]


class tagPOINT(Structure):  # noqa: F405
	pass


tagPOINT._fields_ = [
	("x", c_int),  # noqa: F405
	("y", c_int),  # noqa: F405
]
assert sizeof(tagPOINT) == 8, sizeof(tagPOINT)  # noqa: F405
assert alignment(tagPOINT) == 4, alignment(tagPOINT)  # noqa: F405
IAdviseSink._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"RemoteOnDataChange",
		(["in"], POINTER(tagFORMATETC), "pformatetc"),  # noqa: F405
		(["in"], POINTER(wireASYNC_STGMEDIUM), "pStgmed"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"RemoteOnViewChange",
		(["in"], c_ulong, "dwAspect"),  # noqa: F405
		(["in"], c_int, "lindex"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"RemoteOnRename",
		(["in"], POINTER(IMoniker), "pmk"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "RemoteOnSave"),
	COMMETHOD([], HRESULT, "RemoteOnClose"),
]


class __MIDL___MIDL_itf_oleTypes_0005_0001_0001(Structure):  # noqa: F405
	pass


__MIDL___MIDL_itf_oleTypes_0005_0001_0001._fields_ = [
	("Data1", c_ulong),  # noqa: F405
	("Data2", c_ushort),  # noqa: F405
	("Data3", c_ushort),  # noqa: F405
	("Data4", c_ubyte * 8),  # noqa: F405
]
assert sizeof(__MIDL___MIDL_itf_oleTypes_0005_0001_0001) == 16, sizeof(  # noqa: F405
	__MIDL___MIDL_itf_oleTypes_0005_0001_0001,
)  # noqa: F405
assert alignment(__MIDL___MIDL_itf_oleTypes_0005_0001_0001) == 4, alignment(  # noqa: F405
	__MIDL___MIDL_itf_oleTypes_0005_0001_0001,
)  # noqa: F405
_userFLAG_STGMEDIUM._fields_ = [
	("ContextFlags", c_int),  # noqa: F405
	("fPassOwnership", c_int),  # noqa: F405
	("Stgmed", _userSTGMEDIUM),
]
assert sizeof(_userFLAG_STGMEDIUM) == 20, sizeof(_userFLAG_STGMEDIUM)  # noqa: F405
assert alignment(_userFLAG_STGMEDIUM) == 4, alignment(_userFLAG_STGMEDIUM)  # noqa: F405


class tagSTATDATA(Structure):  # noqa: F405
	pass


IEnumSTATDATA._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"RemoteNext",
		(["in"], c_ulong, "celt"),  # noqa: F405
		(["out"], POINTER(tagSTATDATA), "rgelt"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pceltFetched"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"Skip",
		(["in"], c_ulong, "celt"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "Reset"),
	COMMETHOD(
		[],
		HRESULT,
		"Clone",
		(["out"], POINTER(POINTER(IEnumSTATDATA)), "ppenum"),  # noqa: F405
	),  # noqa: F405
]
tagSIZEL._fields_ = [
	("cx", c_int),  # noqa: F405
	("cy", c_int),  # noqa: F405
]
assert sizeof(tagSIZEL) == 8, sizeof(tagSIZEL)  # noqa: F405
assert alignment(tagSIZEL) == 4, alignment(tagSIZEL)  # noqa: F405
tagMSG._fields_ = [
	("hwnd", wireHWND),
	("message", c_uint),  # noqa: F405
	("wParam", UINT_PTR),
	("lParam", LONG_PTR),
	("time", c_ulong),  # noqa: F405
	("pt", tagPOINT),
]
assert sizeof(tagMSG) == 28, sizeof(tagMSG)  # noqa: F405
assert alignment(tagMSG) == 4, alignment(tagMSG)  # noqa: F405
IEnumFORMATETC._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"RemoteNext",
		(["in"], c_ulong, "celt"),  # noqa: F405
		(["out"], POINTER(tagFORMATETC), "rgelt"),  # noqa: F405
		(["out"], POINTER(c_ulong), "pceltFetched"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD(
		[],
		HRESULT,
		"Skip",
		(["in"], c_ulong, "celt"),  # noqa: F405
	),  # noqa: F405
	COMMETHOD([], HRESULT, "Reset"),
	COMMETHOD(
		[],
		HRESULT,
		"Clone",
		(["out"], POINTER(POINTER(IEnumFORMATETC)), "ppenum"),  # noqa: F405
	),  # noqa: F405
]
_FLAGGED_BYTE_BLOB._fields_ = [
	("fFlags", c_ulong),  # noqa: F405
	("clSize", c_ulong),  # noqa: F405
	("abData", POINTER(c_ubyte)),  # noqa: F405
]
assert sizeof(_FLAGGED_BYTE_BLOB) == 12, sizeof(_FLAGGED_BYTE_BLOB)  # noqa: F405
assert alignment(_FLAGGED_BYTE_BLOB) == 4, alignment(_FLAGGED_BYTE_BLOB)  # noqa: F405
_userBITMAP._fields_ = [
	("bmType", c_int),  # noqa: F405
	("bmWidth", c_int),  # noqa: F405
	("bmHeight", c_int),  # noqa: F405
	("bmWidthBytes", c_int),  # noqa: F405
	("bmPlanes", c_ushort),  # noqa: F405
	("bmBitsPixel", c_ushort),  # noqa: F405
	("cbSize", c_ulong),  # noqa: F405
	("pBuffer", POINTER(c_ubyte)),  # noqa: F405
]
assert sizeof(_userBITMAP) == 28, sizeof(_userBITMAP)  # noqa: F405
assert alignment(_userBITMAP) == 4, alignment(_userBITMAP)  # noqa: F405
_remoteMETAFILEPICT._fields_ = [
	("mm", c_int),  # noqa: F405
	("xExt", c_int),  # noqa: F405
	("yExt", c_int),  # noqa: F405
	("hMF", POINTER(_userHMETAFILE)),  # noqa: F405
]
assert sizeof(_remoteMETAFILEPICT) == 16, sizeof(_remoteMETAFILEPICT)  # noqa: F405
assert alignment(_remoteMETAFILEPICT) == 4, alignment(_remoteMETAFILEPICT)  # noqa: F405
tagSTATDATA._fields_ = [
	("formatetc", tagFORMATETC),
	("advf", c_ulong),  # noqa: F405
	("pAdvSink", POINTER(IAdviseSink)),  # noqa: F405
	("dwConnection", c_ulong),  # noqa: F405
]
assert sizeof(tagSTATDATA) == 32, sizeof(tagSTATDATA)  # noqa: F405
assert alignment(tagSTATDATA) == 4, alignment(tagSTATDATA)  # noqa: F405
_userHBITMAP._fields_ = [
	("fContext", c_int),  # noqa: F405
	("u", __MIDL_IWinTypes_0007),
]
assert sizeof(_userHBITMAP) == 16, sizeof(_userHBITMAP)  # noqa: F405
assert alignment(_userHBITMAP) == 8, alignment(_userHBITMAP)  # noqa: F405
tagPALETTEENTRY._fields_ = [
	("peRed", c_ubyte),  # noqa: F405
	("peGreen", c_ubyte),  # noqa: F405
	("peBlue", c_ubyte),  # noqa: F405
	("peFlags", c_ubyte),  # noqa: F405
]
assert sizeof(tagPALETTEENTRY) == 4, sizeof(tagPALETTEENTRY)  # noqa: F405
assert alignment(tagPALETTEENTRY) == 1, alignment(tagPALETTEENTRY)  # noqa: F405
