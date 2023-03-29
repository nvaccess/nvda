# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2021 NV Access Limited, Leonard de Ruijter, Joseph Lee
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from ctypes import c_int, c_longlong, c_ubyte, c_ulong, c_ulonglong, c_wchar_p, POINTER, Structure, windll
from ctypes.wintypes import HWND, BOOL
from comtypes import HRESULT, GUID, COMMETHOD, IUnknown, tagBIND_OPTS2
from comtypes.persist import IPersist
import winKernel

WSTRING = c_wchar_p

class IOleWindow(IUnknown):
	_iid_ = GUID("{00000114-0000-0000-C000-000000000046}")
	_methods_ = [
		COMMETHOD([], HRESULT, "GetWindow",
			(["out"], POINTER(HWND), "phwnd")
		),
		COMMETHOD([], HRESULT, "ContextSensitiveHelp",
			(["in"], BOOL, "fEnterMode")
		),
	]

class _LARGE_INTEGER(Structure):
	_fields_ = [
		('QuadPart', c_longlong),
	]

class _ULARGE_INTEGER(Structure):
	_fields_ = [
		('QuadPart', c_ulonglong),
	]


class tagSTATSTG(Structure):
	_fields_ = [
		('pwcsName', WSTRING),
		('type', c_ulong),
		('cbSize', _ULARGE_INTEGER),
		('mtime', winKernel.FILETIME),
		('ctime', winKernel.FILETIME),
		('atime', winKernel.FILETIME),
		('grfMode', c_ulong),
		('grfLocksSupported', c_ulong),
		('clsid', GUID),
		('grfStateBits', c_ulong),
		('reserved', c_ulong),
	]

class ISequentialStream(IUnknown):
	_iid_ = GUID('{0C733A30-2A1C-11CE-ADE5-00AA0044773D}')
	_idlflags_ = []
	_methods_ = [
		COMMETHOD([], HRESULT, 'RemoteRead',
			( ['out'], POINTER(c_ubyte), 'pv' ),
			( ['in'], c_ulong, 'cb' ),
			( ['out'], POINTER(c_ulong), 'pcbRead' )),
		COMMETHOD([], HRESULT, 'RemoteWrite',
			( ['in'], POINTER(c_ubyte), 'pv' ),
			( ['in'], c_ulong, 'cb' ),
			( ['out'], POINTER(c_ulong), 'pcbWritten' )),
	]

class IStream(ISequentialStream):
	_iid_ = GUID('{0000000C-0000-0000-C000-000000000046}')
	_idlflags_ = []
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

class IPersistStream(IPersist):
	_iid_ = GUID('{00000109-0000-0000-C000-000000000046}')
	_idlflags_ = []
	_methods_ = [
		COMMETHOD([], HRESULT, 'IsDirty'),
		COMMETHOD([], HRESULT, 'Load',
			( ['in'], POINTER(IStream), 'pstm' )),
		COMMETHOD([], HRESULT, 'Save',
			( ['in'], POINTER(IStream), 'pstm' ),
			( ['in'], c_int, 'fClearDirty' )),
		COMMETHOD([], HRESULT, 'GetSizeMax',
			( ['out'], POINTER(_ULARGE_INTEGER), 'pcbSize' )),
	]

class IRunningObjectTable(IUnknown):
	_iid_ = GUID('{00000010-0000-0000-C000-000000000046}')
	_idlflags_ = []

	def __iter__(self):
		return self.EnumRunning()

class IEnumString(IUnknown):
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

class IBindCtx(IUnknown):
	_iid_ = GUID('{0000000E-0000-0000-C000-000000000046}')
	_idlflags_ = []
	_methods_ = [
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

class IMoniker(IPersistStream):
	_iid_ = GUID('{0000000F-0000-0000-C000-000000000046}')
	_idlflags_ = []

	def GetDisplayName(self, pbc, pmkToLeft):
		displayName = WSTRING()
		self.__com_GetDisplayName(pbc, pmkToLeft, displayName)
		ret = displayName.value
		windll.ole32.CoTaskMemFree(displayName)
		return ret

class IEnumMoniker(IUnknown):
	_iid_ = GUID('{00000102-0000-0000-C000-000000000046}')
	_idlflags_ = []

	def Next(self, celt):
		fetched = c_ulong()
		if celt == 1:
			mon = POINTER(IMoniker)()
			self.__com_Next(celt, mon, fetched)
			return mon, fetched.value
		array = (POINTER(IMoniker) * celt)()
		self.__com_Next(celt, array, fetched)
		return array[:fetched.value]

	def __iter__(self):
		return self

	def __next__(self):
		item, fetched = self.Next(1)
		if fetched:
			return item
		raise StopIteration

IEnumMoniker._methods_ = [
	COMMETHOD([], HRESULT, 'Next',
		( ['in'], c_ulong, 'celt' ),
		( ['out'], POINTER(POINTER(IMoniker)), 'rgelt' ),
		( ['out'], POINTER(c_ulong), 'pceltFetched' )),
	COMMETHOD([], HRESULT, 'Skip',
		( ['in'], c_ulong, 'celt' )),
	COMMETHOD([], HRESULT, 'Reset'),
	COMMETHOD([], HRESULT, 'Clone',
		( ['out'], POINTER(POINTER(IEnumMoniker)), 'ppenum' )),
]

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
	COMMETHOD(
		[],
		HRESULT,
		'GetTimeOfLastChange',
		( ['in'], POINTER(IBindCtx), 'pbc' ),
		( ['in'], POINTER(IMoniker), 'pmkToLeft' ),
		(['out'], POINTER(winKernel.FILETIME), 'pfiletime')
	),
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
	COMMETHOD(
		[],
		HRESULT,
		'NoteChangeTime',
		( ['in'], c_ulong, 'dwRegister' ),
		(['in'], POINTER(winKernel.FILETIME), 'pfiletime')
	),
	COMMETHOD(
		[],
		HRESULT,
		'GetTimeOfLastChange',
		( ['in'], POINTER(IMoniker), 'pmkObjectName' ),
		(['out'], POINTER(winKernel.FILETIME), 'pfiletime')
	),
	COMMETHOD([], HRESULT, 'EnumRunning',
		( ['out'], POINTER(POINTER(IEnumMoniker)), 'ppenumMoniker' )),
]
