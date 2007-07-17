# typelib <unable to determine filename>
_lcid = 0 # change this if required
from ctypes import *
WSTRING = c_wchar_p
from comtypes import IUnknown
LONG_PTR = c_int
from comtypes import GUID
from comtypes import IUnknown
from ctypes import HRESULT
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes.persist import IPersist
from comtypes import wireHWND
from comtypes import GUID
from comtypes import _COAUTHIDENTITY
UINT_PTR = c_ulong
from comtypes import tagBIND_OPTS2
from comtypes import _COSERVERINFO
from comtypes import _COAUTHINFO
from comtypes import tagBIND_OPTS2


class tagDVTARGETDEVICE(Structure):
    pass
tagDVTARGETDEVICE._fields_ = [
    ('tdSize', c_ulong),
    ('tdDriverNameOffset', c_ushort),
    ('tdDeviceNameOffset', c_ushort),
    ('tdPortNameOffset', c_ushort),
    ('tdExtDevmodeOffset', c_ushort),
    ('tdData', POINTER(c_ubyte)),
]
assert sizeof(tagDVTARGETDEVICE) == 16, sizeof(tagDVTARGETDEVICE)
assert alignment(tagDVTARGETDEVICE) == 4, alignment(tagDVTARGETDEVICE)
class _BYTE_BLOB(Structure):
    pass
_BYTE_BLOB._fields_ = [
    ('clSize', c_ulong),
    ('abData', POINTER(c_ubyte)),
]
assert sizeof(_BYTE_BLOB) == 8, sizeof(_BYTE_BLOB)
assert alignment(_BYTE_BLOB) == 4, alignment(_BYTE_BLOB)
class tagRECT(Structure):
    pass
tagRECT._fields_ = [
    ('left', c_int),
    ('top', c_int),
    ('right', c_int),
    ('bottom', c_int),
]
assert sizeof(tagRECT) == 16, sizeof(tagRECT)
assert alignment(tagRECT) == 4, alignment(tagRECT)
class __MIDL_IWinTypes_0003(Union):
    pass
class _FLAGGED_BYTE_BLOB(Structure):
    pass
__MIDL_IWinTypes_0003._fields_ = [
    ('hInproc', c_int),
    ('hRemote', POINTER(_FLAGGED_BYTE_BLOB)),
    ('hInproc64', c_longlong),
]
assert sizeof(__MIDL_IWinTypes_0003) == 8, sizeof(__MIDL_IWinTypes_0003)
assert alignment(__MIDL_IWinTypes_0003) == 8, alignment(__MIDL_IWinTypes_0003)
class _userSTGMEDIUM(Structure):
    pass
class _STGMEDIUM_UNION(Structure):
    pass
class __MIDL_IAdviseSink_0003(Union):
    pass
class _userHMETAFILEPICT(Structure):
    pass
class _userHENHMETAFILE(Structure):
    pass
class _GDI_OBJECT(Structure):
    pass
class _userHGLOBAL(Structure):
    pass
__MIDL_IAdviseSink_0003._fields_ = [
    ('hMetaFilePict', POINTER(_userHMETAFILEPICT)),
    ('hHEnhMetaFile', POINTER(_userHENHMETAFILE)),
    ('hGdiHandle', POINTER(_GDI_OBJECT)),
    ('hGlobal', POINTER(_userHGLOBAL)),
    ('lpszFileName', WSTRING),
    ('pstm', POINTER(_BYTE_BLOB)),
    ('pstg', POINTER(_BYTE_BLOB)),
]
assert sizeof(__MIDL_IAdviseSink_0003) == 4, sizeof(__MIDL_IAdviseSink_0003)
assert alignment(__MIDL_IAdviseSink_0003) == 4, alignment(__MIDL_IAdviseSink_0003)
_STGMEDIUM_UNION._fields_ = [
    ('tymed', c_ulong),
    ('u', __MIDL_IAdviseSink_0003),
]
assert sizeof(_STGMEDIUM_UNION) == 8, sizeof(_STGMEDIUM_UNION)
assert alignment(_STGMEDIUM_UNION) == 4, alignment(_STGMEDIUM_UNION)
_userSTGMEDIUM._fields_ = [
    ('__MIDL__IAdviseSink0003', _STGMEDIUM_UNION),
    ('pUnkForRelease', POINTER(IUnknown)),
]
assert sizeof(_userSTGMEDIUM) == 12, sizeof(_userSTGMEDIUM)
assert alignment(_userSTGMEDIUM) == 4, alignment(_userSTGMEDIUM)
class tagLOGPALETTE(Structure):
    pass
class tagPALETTEENTRY(Structure):
    pass
tagLOGPALETTE._pack_ = 2
tagLOGPALETTE._fields_ = [
    ('palVersion', c_ushort),
    ('palNumEntries', c_ushort),
    ('palPalEntry', POINTER(tagPALETTEENTRY)),
]
assert sizeof(tagLOGPALETTE) == 8, sizeof(tagLOGPALETTE)
assert alignment(tagLOGPALETTE) == 2, alignment(tagLOGPALETTE)
wireASYNC_STGMEDIUM = POINTER(_userSTGMEDIUM)
class IEnumOLEVERB(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000104-0000-0000-C000-000000000046}')
    _idlflags_ = []
class tagOLEVERB(Structure):
    pass
IEnumOLEVERB._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteNext',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(tagOLEVERB), 'rgelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumOLEVERB)), 'ppenum' )),
]
class IRunningObjectTable(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000010-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IPersistStream(IPersist):
    _case_insensitive_ = True
    _iid_ = GUID('{00000109-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IMoniker(IPersistStream):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000F-0000-0000-C000-000000000046}')
    _idlflags_ = []
class _FILETIME(Structure):
    pass
class IEnumMoniker(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000102-0000-0000-C000-000000000046}')
    _idlflags_ = []
IRunningObjectTable._methods_ = [
    COMMETHOD([], HRESULT, 'Register',
              ( ['in'], c_ulong, 'grfFlags' ),
              ( ['in'], POINTER(IUnknown), 'punkObject' ),
              ( ['in'], POINTER(IMoniker), 'pmkObjectName' ),
              ( ['out'], POINTER(c_ulong), 'pdwRegister' )),
    COMMETHOD([], HRESULT, 'Revoke',
              ( ['in'], c_ulong, 'dwRegister' )),
    COMMETHOD([], HRESULT, 'IsRunning',
              ( ['in'], POINTER(IMoniker), 'pmkObjectName' )),
    COMMETHOD([], HRESULT, 'GetObject',
              ( ['in'], POINTER(IMoniker), 'pmkObjectName' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppunkObject' )),
    COMMETHOD([], HRESULT, 'NoteChangeTime',
              ( ['in'], c_ulong, 'dwRegister' ),
              ( ['in'], POINTER(_FILETIME), 'pfiletime' )),
    COMMETHOD([], HRESULT, 'GetTimeOfLastChange',
              ( ['in'], POINTER(IMoniker), 'pmkObjectName' ),
              ( ['out'], POINTER(_FILETIME), 'pfiletime' )),
    COMMETHOD([], HRESULT, 'EnumRunning',
              ( ['out'], POINTER(POINTER(IEnumMoniker)), 'ppenumMoniker' )),
]
class _LARGE_INTEGER(Structure):
    pass
_LARGE_INTEGER._fields_ = [
    ('QuadPart', c_longlong),
]
assert sizeof(_LARGE_INTEGER) == 8, sizeof(_LARGE_INTEGER)
assert alignment(_LARGE_INTEGER) == 8, alignment(_LARGE_INTEGER)
class IEnumUnknown(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000100-0000-0000-C000-000000000046}')
    _idlflags_ = []
IEnumUnknown._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteNext',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'rgelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumUnknown)), 'ppenum' )),
]
class _RemotableHandle(Structure):
    pass
class __MIDL_IWinTypes_0009(Union):
    pass
__MIDL_IWinTypes_0009._fields_ = [
    ('hInproc', c_int),
    ('hRemote', c_int),
]
assert sizeof(__MIDL_IWinTypes_0009) == 4, sizeof(__MIDL_IWinTypes_0009)
assert alignment(__MIDL_IWinTypes_0009) == 4, alignment(__MIDL_IWinTypes_0009)
_RemotableHandle._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0009),
]
assert sizeof(_RemotableHandle) == 8, sizeof(_RemotableHandle)
assert alignment(_RemotableHandle) == 4, alignment(_RemotableHandle)
IEnumMoniker._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteNext',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'rgelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumMoniker)), 'ppenum' )),
]
class _userHMETAFILE(Structure):
    pass
class __MIDL_IWinTypes_0004(Union):
    pass
__MIDL_IWinTypes_0004._fields_ = [
    ('hInproc', c_int),
    ('hRemote', POINTER(_BYTE_BLOB)),
    ('hInproc64', c_longlong),
]
assert sizeof(__MIDL_IWinTypes_0004) == 8, sizeof(__MIDL_IWinTypes_0004)
assert alignment(__MIDL_IWinTypes_0004) == 8, alignment(__MIDL_IWinTypes_0004)
_userHMETAFILE._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0004),
]
assert sizeof(_userHMETAFILE) == 16, sizeof(_userHMETAFILE)
assert alignment(_userHMETAFILE) == 8, alignment(_userHMETAFILE)
wireSTGMEDIUM = POINTER(_userSTGMEDIUM)
class _userHPALETTE(Structure):
    pass
class __MIDL_IWinTypes_0008(Union):
    pass
__MIDL_IWinTypes_0008._fields_ = [
    ('hInproc', c_int),
    ('hRemote', POINTER(tagLOGPALETTE)),
    ('hInproc64', c_longlong),
]
assert sizeof(__MIDL_IWinTypes_0008) == 8, sizeof(__MIDL_IWinTypes_0008)
assert alignment(__MIDL_IWinTypes_0008) == 8, alignment(__MIDL_IWinTypes_0008)
_userHPALETTE._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0008),
]
assert sizeof(_userHPALETTE) == 16, sizeof(_userHPALETTE)
assert alignment(_userHPALETTE) == 8, alignment(_userHPALETTE)
class __MIDL_IWinTypes_0007(Union):
    pass
class _userBITMAP(Structure):
    pass
__MIDL_IWinTypes_0007._fields_ = [
    ('hInproc', c_int),
    ('hRemote', POINTER(_userBITMAP)),
    ('hInproc64', c_longlong),
]
assert sizeof(__MIDL_IWinTypes_0007) == 8, sizeof(__MIDL_IWinTypes_0007)
assert alignment(__MIDL_IWinTypes_0007) == 8, alignment(__MIDL_IWinTypes_0007)
class IParseDisplayName(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0000011A-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IOleContainer(IParseDisplayName):
    _case_insensitive_ = True
    _iid_ = GUID('{0000011B-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IBindCtx(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000E-0000-0000-C000-000000000046}')
    _idlflags_ = []
IParseDisplayName._methods_ = [
    COMMETHOD([], HRESULT, 'ParseDisplayName',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], WSTRING, 'pszDisplayName' ),
              ( ['out'], POINTER(c_ulong), 'pchEaten' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmkOut' )),
]
IOleContainer._methods_ = [
    COMMETHOD([], HRESULT, 'EnumObjects',
              ( ['in'], c_ulong, 'grfFlags' ),
              ( ['out'], POINTER(POINTER(IEnumUnknown)), 'ppenum' )),
    COMMETHOD([], HRESULT, 'LockContainer',
              ( ['in'], c_int, 'fLock' )),
]
class ISequentialStream(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0C733A30-2A1C-11CE-ADE5-00AA0044773D}')
    _idlflags_ = []
class IStream(ISequentialStream):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000C-0000-0000-C000-000000000046}')
    _idlflags_ = []
class _ULARGE_INTEGER(Structure):
    pass
IPersistStream._methods_ = [
    COMMETHOD([], HRESULT, 'IsDirty'),
    COMMETHOD([], HRESULT, 'Load',
              ( ['in'], POINTER(IStream), 'pstm' )),
    COMMETHOD([], HRESULT, 'Save',
              ( ['in'], POINTER(IStream), 'pstm' ),
              ( ['in'], c_int, 'fClearDirty' )),
    COMMETHOD([], HRESULT, 'GetSizeMax',
              ( ['out'], POINTER(_ULARGE_INTEGER), 'pcbSize' )),
]
class IOleObject(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000112-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IOleClientSite(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000118-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IDataObject(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0000010E-0000-0000-C000-000000000046}')
    _idlflags_ = []
class tagMSG(Structure):
    pass
class tagSIZEL(Structure):
    pass
class IAdviseSink(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0000010F-0000-0000-C000-000000000046}')
    _idlflags_ = []
class IEnumSTATDATA(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000105-0000-0000-C000-000000000046}')
    _idlflags_ = []
IOleObject._methods_ = [
    COMMETHOD([], HRESULT, 'SetClientSite',
              ( ['in'], POINTER(IOleClientSite), 'pClientSite' )),
    COMMETHOD([], HRESULT, 'GetClientSite',
              ( ['out'], POINTER(POINTER(IOleClientSite)), 'ppClientSite' )),
    COMMETHOD([], HRESULT, 'SetHostNames',
              ( ['in'], WSTRING, 'szContainerApp' ),
              ( ['in'], WSTRING, 'szContainerObj' )),
    COMMETHOD([], HRESULT, 'Close',
              ( ['in'], c_ulong, 'dwSaveOption' )),
    COMMETHOD([], HRESULT, 'SetMoniker',
              ( ['in'], c_ulong, 'dwWhichMoniker' ),
              ( ['in'], POINTER(IMoniker), 'pmk' )),
    COMMETHOD([], HRESULT, 'GetMoniker',
              ( ['in'], c_ulong, 'dwAssign' ),
              ( ['in'], c_ulong, 'dwWhichMoniker' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmk' )),
    COMMETHOD([], HRESULT, 'InitFromData',
              ( ['in'], POINTER(IDataObject), 'pDataObject' ),
              ( ['in'], c_int, 'fCreation' ),
              ( ['in'], c_ulong, 'dwReserved' )),
    COMMETHOD([], HRESULT, 'GetClipboardData',
              ( ['in'], c_ulong, 'dwReserved' ),
              ( ['out'], POINTER(POINTER(IDataObject)), 'ppDataObject' )),
    COMMETHOD([], HRESULT, 'DoVerb',
              ( ['in'], c_int, 'iVerb' ),
              ( ['in'], POINTER(tagMSG), 'lpmsg' ),
              ( ['in'], POINTER(IOleClientSite), 'pActiveSite' ),
              ( ['in'], c_int, 'lindex' ),
              ( ['in'], wireHWND, 'hwndParent' ),
              ( ['in'], POINTER(tagRECT), 'lprcPosRect' )),
    COMMETHOD([], HRESULT, 'EnumVerbs',
              ( ['out'], POINTER(POINTER(IEnumOLEVERB)), 'ppEnumOleVerb' )),
    COMMETHOD([], HRESULT, 'Update'),
    COMMETHOD([], HRESULT, 'IsUpToDate'),
    COMMETHOD([], HRESULT, 'GetUserClassID',
              ( ['out'], POINTER(GUID), 'pClsid' )),
    COMMETHOD([], HRESULT, 'GetUserType',
              ( ['in'], c_ulong, 'dwFormOfType' ),
              ( ['out'], POINTER(WSTRING), 'pszUserType' )),
    COMMETHOD([], HRESULT, 'SetExtent',
              ( ['in'], c_ulong, 'dwDrawAspect' ),
              ( ['in'], POINTER(tagSIZEL), 'psizel' )),
    COMMETHOD([], HRESULT, 'GetExtent',
              ( ['in'], c_ulong, 'dwDrawAspect' ),
              ( ['out'], POINTER(tagSIZEL), 'psizel' )),
    COMMETHOD([], HRESULT, 'Advise',
              ( ['in'], POINTER(IAdviseSink), 'pAdvSink' ),
              ( ['out'], POINTER(c_ulong), 'pdwConnection' )),
    COMMETHOD([], HRESULT, 'Unadvise',
              ( ['in'], c_ulong, 'dwConnection' )),
    COMMETHOD([], HRESULT, 'EnumAdvise',
              ( ['out'], POINTER(POINTER(IEnumSTATDATA)), 'ppenumAdvise' )),
    COMMETHOD([], HRESULT, 'GetMiscStatus',
              ( ['in'], c_ulong, 'dwAspect' ),
              ( ['out'], POINTER(c_ulong), 'pdwStatus' )),
    COMMETHOD([], HRESULT, 'SetColorScheme',
              ( ['in'], POINTER(tagLOGPALETTE), 'pLogpal' )),
]
class __MIDL_IWinTypes_0005(Union):
    pass
class _remoteMETAFILEPICT(Structure):
    pass
__MIDL_IWinTypes_0005._fields_ = [
    ('hInproc', c_int),
    ('hRemote', POINTER(_remoteMETAFILEPICT)),
    ('hInproc64', c_longlong),
]
assert sizeof(__MIDL_IWinTypes_0005) == 8, sizeof(__MIDL_IWinTypes_0005)
assert alignment(__MIDL_IWinTypes_0005) == 8, alignment(__MIDL_IWinTypes_0005)
_userHMETAFILEPICT._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0005),
]
assert sizeof(_userHMETAFILEPICT) == 16, sizeof(_userHMETAFILEPICT)
assert alignment(_userHMETAFILEPICT) == 8, alignment(_userHMETAFILEPICT)
tagOLEVERB._fields_ = [
    ('lVerb', c_int),
    ('lpszVerbName', WSTRING),
    ('fuFlags', c_ulong),
    ('grfAttribs', c_ulong),
]
assert sizeof(tagOLEVERB) == 16, sizeof(tagOLEVERB)
assert alignment(tagOLEVERB) == 4, alignment(tagOLEVERB)
class _userCLIPFORMAT(Structure):
    pass
class __MIDL_IWinTypes_0001(Union):
    pass
__MIDL_IWinTypes_0001._fields_ = [
    ('dwValue', c_ulong),
    ('pwszName', WSTRING),
]
assert sizeof(__MIDL_IWinTypes_0001) == 4, sizeof(__MIDL_IWinTypes_0001)
assert alignment(__MIDL_IWinTypes_0001) == 4, alignment(__MIDL_IWinTypes_0001)
_userCLIPFORMAT._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0001),
]
assert sizeof(_userCLIPFORMAT) == 8, sizeof(_userCLIPFORMAT)
assert alignment(_userCLIPFORMAT) == 4, alignment(_userCLIPFORMAT)
IMoniker._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteBindToObject',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
              ( ['in'], POINTER(GUID), 'riidResult' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppvResult' )),
    COMMETHOD([], HRESULT, 'RemoteBindToStorage',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
              ( ['in'], POINTER(GUID), 'riid' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppvObj' )),
    COMMETHOD([], HRESULT, 'Reduce',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], c_ulong, 'dwReduceHowFar' ),
              ( ['in', 'out'], POINTER(POINTER(IMoniker)), 'ppmkToLeft' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmkReduced' )),
    COMMETHOD([], HRESULT, 'ComposeWith',
              ( ['in'], POINTER(IMoniker), 'pmkRight' ),
              ( ['in'], c_int, 'fOnlyIfNotGeneric' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmkComposite' )),
    COMMETHOD([], HRESULT, 'Enum',
              ( ['in'], c_int, 'fForward' ),
              ( ['out'], POINTER(POINTER(IEnumMoniker)), 'ppenumMoniker' )),
    COMMETHOD([], HRESULT, 'IsEqual',
              ( ['in'], POINTER(IMoniker), 'pmkOtherMoniker' )),
    COMMETHOD([], HRESULT, 'Hash',
              ( ['out'], POINTER(c_ulong), 'pdwHash' )),
    COMMETHOD([], HRESULT, 'IsRunning',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
              ( ['in'], POINTER(IMoniker), 'pmkNewlyRunning' )),
    COMMETHOD([], HRESULT, 'GetTimeOfLastChange',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
              ( ['out'], POINTER(_FILETIME), 'pfiletime' )),
    COMMETHOD([], HRESULT, 'Inverse',
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmk' )),
    COMMETHOD([], HRESULT, 'CommonPrefixWith',
              ( ['in'], POINTER(IMoniker), 'pmkOther' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmkPrefix' )),
    COMMETHOD([], HRESULT, 'RelativePathTo',
              ( ['in'], POINTER(IMoniker), 'pmkOther' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmkRelPath' )),
    COMMETHOD([], HRESULT, 'GetDisplayName',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
              ( ['out'], POINTER(WSTRING), 'ppszDisplayName' )),
    COMMETHOD([], HRESULT, 'ParseDisplayName',
              ( ['in'], POINTER(IBindCtx), 'pbc' ),
              ( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
              ( ['in'], WSTRING, 'pszDisplayName' ),
              ( ['out'], POINTER(c_ulong), 'pchEaten' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmkOut' )),
    COMMETHOD([], HRESULT, 'IsSystemMoniker',
              ( ['out'], POINTER(c_ulong), 'pdwMksys' )),
]
class IServiceProvider(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6D5140C1-7436-11CE-8034-00AA006009FA}')
    _idlflags_ = []
IServiceProvider._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteQueryService',
              ( ['in'], POINTER(GUID), 'guidService' ),
              ( ['in'], POINTER(GUID), 'riid' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppvObject' )),
]
ISequentialStream._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteRead',
              ( ['out'], POINTER(c_ubyte), 'pv' ),
              ( ['in'], c_ulong, 'cb' ),
              ( ['out'], POINTER(c_ulong), 'pcbRead' )),
    COMMETHOD([], HRESULT, 'RemoteWrite',
              ( ['in'], POINTER(c_ubyte), 'pv' ),
              ( ['in'], c_ulong, 'cb' ),
              ( ['out'], POINTER(c_ulong), 'pcbWritten' )),
]
_ULARGE_INTEGER._fields_ = [
    ('QuadPart', c_ulonglong),
]
assert sizeof(_ULARGE_INTEGER) == 8, sizeof(_ULARGE_INTEGER)
assert alignment(_ULARGE_INTEGER) == 8, alignment(_ULARGE_INTEGER)
class tagSTATSTG(Structure):
    pass
IStream._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteSeek',
              ( ['in'], _LARGE_INTEGER, 'dlibMove' ),
              ( ['in'], c_ulong, 'dwOrigin' ),
              ( ['out'], POINTER(_ULARGE_INTEGER), 'plibNewPosition' )),
    COMMETHOD([], HRESULT, 'SetSize',
              ( ['in'], _ULARGE_INTEGER, 'libNewSize' )),
    COMMETHOD([], HRESULT, 'RemoteCopyTo',
              ( ['in'], POINTER(IStream), 'pstm' ),
              ( ['in'], _ULARGE_INTEGER, 'cb' ),
              ( ['out'], POINTER(_ULARGE_INTEGER), 'pcbRead' ),
              ( ['out'], POINTER(_ULARGE_INTEGER), 'pcbWritten' )),
    COMMETHOD([], HRESULT, 'Commit',
              ( ['in'], c_ulong, 'grfCommitFlags' )),
    COMMETHOD([], HRESULT, 'Revert'),
    COMMETHOD([], HRESULT, 'LockRegion',
              ( ['in'], _ULARGE_INTEGER, 'libOffset' ),
              ( ['in'], _ULARGE_INTEGER, 'cb' ),
              ( ['in'], c_ulong, 'dwLockType' )),
    COMMETHOD([], HRESULT, 'UnlockRegion',
              ( ['in'], _ULARGE_INTEGER, 'libOffset' ),
              ( ['in'], _ULARGE_INTEGER, 'cb' ),
              ( ['in'], c_ulong, 'dwLockType' )),
    COMMETHOD([], HRESULT, 'Stat',
              ( ['out'], POINTER(tagSTATSTG), 'pstatstg' ),
              ( ['in'], c_ulong, 'grfStatFlag' )),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IStream)), 'ppstm' )),
]
class IEnumString(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000101-0000-0000-C000-000000000046}')
    _idlflags_ = []
IEnumString._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteNext',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(WSTRING), 'rgelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumString)), 'ppenum' )),
]
wireCLIPFORMAT = POINTER(_userCLIPFORMAT)
class __MIDL_IWinTypes_0006(Union):
    pass
__MIDL_IWinTypes_0006._fields_ = [
    ('hInproc', c_int),
    ('hRemote', POINTER(_BYTE_BLOB)),
    ('hInproc64', c_longlong),
]
assert sizeof(__MIDL_IWinTypes_0006) == 8, sizeof(__MIDL_IWinTypes_0006)
assert alignment(__MIDL_IWinTypes_0006) == 8, alignment(__MIDL_IWinTypes_0006)
_userHENHMETAFILE._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0006),
]
assert sizeof(_userHENHMETAFILE) == 16, sizeof(_userHENHMETAFILE)
assert alignment(_userHENHMETAFILE) == 8, alignment(_userHENHMETAFILE)
class tagFORMATETC(Structure):
    pass
tagFORMATETC._fields_ = [
    ('cfFormat', wireCLIPFORMAT),
    ('ptd', POINTER(tagDVTARGETDEVICE)),
    ('dwAspect', c_ulong),
    ('lindex', c_int),
    ('tymed', c_ulong),
]
assert sizeof(tagFORMATETC) == 20, sizeof(tagFORMATETC)
assert alignment(tagFORMATETC) == 4, alignment(tagFORMATETC)
_userHGLOBAL._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0003),
]
assert sizeof(_userHGLOBAL) == 16, sizeof(_userHGLOBAL)
assert alignment(_userHGLOBAL) == 8, alignment(_userHGLOBAL)
IOleClientSite._methods_ = [
    COMMETHOD([], HRESULT, 'SaveObject'),
    COMMETHOD([], HRESULT, 'GetMoniker',
              ( ['in'], c_ulong, 'dwAssign' ),
              ( ['in'], c_ulong, 'dwWhichMoniker' ),
              ( ['out'], POINTER(POINTER(IMoniker)), 'ppmk' )),
    COMMETHOD([], HRESULT, 'GetContainer',
              ( ['out'], POINTER(POINTER(IOleContainer)), 'ppContainer' )),
    COMMETHOD([], HRESULT, 'ShowObject'),
    COMMETHOD([], HRESULT, 'OnShowWindow',
              ( ['in'], c_int, 'fShow' )),
    COMMETHOD([], HRESULT, 'RequestNewObjectLayout'),
]
class __MIDL_IAdviseSink_0002(Union):
    pass
class _userHBITMAP(Structure):
    pass
__MIDL_IAdviseSink_0002._fields_ = [
    ('hBitmap', POINTER(_userHBITMAP)),
    ('hPalette', POINTER(_userHPALETTE)),
    ('hGeneric', POINTER(_userHGLOBAL)),
]
assert sizeof(__MIDL_IAdviseSink_0002) == 4, sizeof(__MIDL_IAdviseSink_0002)
assert alignment(__MIDL_IAdviseSink_0002) == 4, alignment(__MIDL_IAdviseSink_0002)
_GDI_OBJECT._fields_ = [
    ('ObjectType', c_ulong),
    ('u', __MIDL_IAdviseSink_0002),
]
assert sizeof(_GDI_OBJECT) == 8, sizeof(_GDI_OBJECT)
assert alignment(_GDI_OBJECT) == 4, alignment(_GDI_OBJECT)
class _userFLAG_STGMEDIUM(Structure):
    pass
wireFLAG_STGMEDIUM = POINTER(_userFLAG_STGMEDIUM)
class IEnumFORMATETC(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{00000103-0000-0000-C000-000000000046}')
    _idlflags_ = []
IDataObject._methods_ = [
    COMMETHOD([], HRESULT, 'GetData',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetcIn' ),
              ( ['out'], POINTER(wireSTGMEDIUM), 'pmedium' )),
    COMMETHOD([], HRESULT, 'RemoteGetData',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetcIn' ),
              ( ['out'], POINTER(wireSTGMEDIUM), 'pRemoteMedium' )),
    COMMETHOD([], HRESULT, 'RemoteGetDataHere',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetc' ),
              ( ['in', 'out'], POINTER(wireSTGMEDIUM), 'pRemoteMedium' )),
    COMMETHOD([], HRESULT, 'QueryGetData',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetc' )),
    COMMETHOD([], HRESULT, 'GetCanonicalFormatEtc',
              ( ['in'], POINTER(tagFORMATETC), 'pformatectIn' ),
              ( ['out'], POINTER(tagFORMATETC), 'pformatetcOut' )),
    COMMETHOD([], HRESULT, 'RemoteSetData',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetc' ),
              ( ['in'], POINTER(wireFLAG_STGMEDIUM), 'pmedium' ),
              ( ['in'], c_int, 'fRelease' )),
    COMMETHOD([], HRESULT, 'EnumFormatEtc',
              ( ['in'], c_ulong, 'dwDirection' ),
              ( ['out'], POINTER(POINTER(IEnumFORMATETC)), 'ppenumFormatEtc' )),
    COMMETHOD([], HRESULT, 'DAdvise',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetc' ),
              ( ['in'], c_ulong, 'advf' ),
              ( ['in'], POINTER(IAdviseSink), 'pAdvSink' ),
              ( ['out'], POINTER(c_ulong), 'pdwConnection' )),
    COMMETHOD([], HRESULT, 'DUnadvise',
              ( ['in'], c_ulong, 'dwConnection' )),
    COMMETHOD([], HRESULT, 'EnumDAdvise',
              ( ['out'], POINTER(POINTER(IEnumSTATDATA)), 'ppenumAdvise' )),
]
class tagPOINT(Structure):
    pass
tagPOINT._fields_ = [
    ('x', c_int),
    ('y', c_int),
]
assert sizeof(tagPOINT) == 8, sizeof(tagPOINT)
assert alignment(tagPOINT) == 4, alignment(tagPOINT)
IAdviseSink._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteOnDataChange',
              ( ['in'], POINTER(tagFORMATETC), 'pformatetc' ),
              ( ['in'], POINTER(wireASYNC_STGMEDIUM), 'pStgmed' )),
    COMMETHOD([], HRESULT, 'RemoteOnViewChange',
              ( ['in'], c_ulong, 'dwAspect' ),
              ( ['in'], c_int, 'lindex' )),
    COMMETHOD([], HRESULT, 'RemoteOnRename',
              ( ['in'], POINTER(IMoniker), 'pmk' )),
    COMMETHOD([], HRESULT, 'RemoteOnSave'),
    COMMETHOD([], HRESULT, 'RemoteOnClose'),
]
class __MIDL___MIDL_itf_oleTypes_0005_0001_0001(Structure):
    pass
__MIDL___MIDL_itf_oleTypes_0005_0001_0001._fields_ = [
    ('Data1', c_ulong),
    ('Data2', c_ushort),
    ('Data3', c_ushort),
    ('Data4', c_ubyte * 8),
]
assert sizeof(__MIDL___MIDL_itf_oleTypes_0005_0001_0001) == 16, sizeof(__MIDL___MIDL_itf_oleTypes_0005_0001_0001)
assert alignment(__MIDL___MIDL_itf_oleTypes_0005_0001_0001) == 4, alignment(__MIDL___MIDL_itf_oleTypes_0005_0001_0001)
IBindCtx._methods_ = [
    COMMETHOD([], HRESULT, 'RegisterObjectBound',
              ( ['in'], POINTER(IUnknown), 'punk' )),
    COMMETHOD([], HRESULT, 'RevokeObjectBound',
              ( ['in'], POINTER(IUnknown), 'punk' )),
    COMMETHOD([], HRESULT, 'ReleaseBoundObjects'),
    COMMETHOD([], HRESULT, 'RemoteSetBindOptions',
              ( ['in'], POINTER(tagBIND_OPTS2), 'pbindopts' )),
    COMMETHOD([], HRESULT, 'RemoteGetBindOptions',
              ( ['in', 'out'], POINTER(tagBIND_OPTS2), 'pbindopts' )),
    COMMETHOD([], HRESULT, 'GetRunningObjectTable',
              ( ['out'], POINTER(POINTER(IRunningObjectTable)), 'pprot' )),
    COMMETHOD([], HRESULT, 'RegisterObjectParam',
              ( ['in'], WSTRING, 'pszKey' ),
              ( ['in'], POINTER(IUnknown), 'punk' )),
    COMMETHOD([], HRESULT, 'GetObjectParam',
              ( ['in'], WSTRING, 'pszKey' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppunk' )),
    COMMETHOD([], HRESULT, 'EnumObjectParam',
              ( ['out'], POINTER(POINTER(IEnumString)), 'ppenum' )),
    COMMETHOD([], HRESULT, 'RevokeObjectParam',
              ( ['in'], WSTRING, 'pszKey' )),
]
_userFLAG_STGMEDIUM._fields_ = [
    ('ContextFlags', c_int),
    ('fPassOwnership', c_int),
    ('Stgmed', _userSTGMEDIUM),
]
assert sizeof(_userFLAG_STGMEDIUM) == 20, sizeof(_userFLAG_STGMEDIUM)
assert alignment(_userFLAG_STGMEDIUM) == 4, alignment(_userFLAG_STGMEDIUM)
class tagSTATDATA(Structure):
    pass
IEnumSTATDATA._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteNext',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(tagSTATDATA), 'rgelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumSTATDATA)), 'ppenum' )),
]
tagSIZEL._fields_ = [
    ('cx', c_int),
    ('cy', c_int),
]
assert sizeof(tagSIZEL) == 8, sizeof(tagSIZEL)
assert alignment(tagSIZEL) == 4, alignment(tagSIZEL)
_FILETIME._fields_ = [
    ('dwLowDateTime', c_ulong),
    ('dwHighDateTime', c_ulong),
]
assert sizeof(_FILETIME) == 8, sizeof(_FILETIME)
assert alignment(_FILETIME) == 4, alignment(_FILETIME)
tagSTATSTG._fields_ = [
    ('pwcsName', WSTRING),
    ('type', c_ulong),
    ('cbSize', _ULARGE_INTEGER),
    ('mtime', _FILETIME),
    ('ctime', _FILETIME),
    ('atime', _FILETIME),
    ('grfMode', c_ulong),
    ('grfLocksSupported', c_ulong),
    ('clsid', GUID),
    ('grfStateBits', c_ulong),
    ('reserved', c_ulong),
]
assert sizeof(tagSTATSTG) == 72, sizeof(tagSTATSTG)
assert alignment(tagSTATSTG) == 8, alignment(tagSTATSTG)
tagMSG._fields_ = [
    ('hwnd', wireHWND),
    ('message', c_uint),
    ('wParam', UINT_PTR),
    ('lParam', LONG_PTR),
    ('time', c_ulong),
    ('pt', tagPOINT),
]
assert sizeof(tagMSG) == 28, sizeof(tagMSG)
assert alignment(tagMSG) == 4, alignment(tagMSG)
IEnumFORMATETC._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteNext',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(tagFORMATETC), 'rgelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumFORMATETC)), 'ppenum' )),
]
_FLAGGED_BYTE_BLOB._fields_ = [
    ('fFlags', c_ulong),
    ('clSize', c_ulong),
    ('abData', POINTER(c_ubyte)),
]
assert sizeof(_FLAGGED_BYTE_BLOB) == 12, sizeof(_FLAGGED_BYTE_BLOB)
assert alignment(_FLAGGED_BYTE_BLOB) == 4, alignment(_FLAGGED_BYTE_BLOB)
_userBITMAP._fields_ = [
    ('bmType', c_int),
    ('bmWidth', c_int),
    ('bmHeight', c_int),
    ('bmWidthBytes', c_int),
    ('bmPlanes', c_ushort),
    ('bmBitsPixel', c_ushort),
    ('cbSize', c_ulong),
    ('pBuffer', POINTER(c_ubyte)),
]
assert sizeof(_userBITMAP) == 28, sizeof(_userBITMAP)
assert alignment(_userBITMAP) == 4, alignment(_userBITMAP)
_remoteMETAFILEPICT._fields_ = [
    ('mm', c_int),
    ('xExt', c_int),
    ('yExt', c_int),
    ('hMF', POINTER(_userHMETAFILE)),
]
assert sizeof(_remoteMETAFILEPICT) == 16, sizeof(_remoteMETAFILEPICT)
assert alignment(_remoteMETAFILEPICT) == 4, alignment(_remoteMETAFILEPICT)
tagSTATDATA._fields_ = [
    ('formatetc', tagFORMATETC),
    ('advf', c_ulong),
    ('pAdvSink', POINTER(IAdviseSink)),
    ('dwConnection', c_ulong),
]
assert sizeof(tagSTATDATA) == 32, sizeof(tagSTATDATA)
assert alignment(tagSTATDATA) == 4, alignment(tagSTATDATA)
_userHBITMAP._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0007),
]
assert sizeof(_userHBITMAP) == 16, sizeof(_userHBITMAP)
assert alignment(_userHBITMAP) == 8, alignment(_userHBITMAP)
tagPALETTEENTRY._fields_ = [
    ('peRed', c_ubyte),
    ('peGreen', c_ubyte),
    ('peBlue', c_ubyte),
    ('peFlags', c_ubyte),
]
assert sizeof(tagPALETTEENTRY) == 4, sizeof(tagPALETTEENTRY)
assert alignment(tagPALETTEENTRY) == 1, alignment(tagPALETTEENTRY)
