# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import Structure, Union, byref, windll
from ctypes.wintypes import DWORD, LONG, LPWSTR, ULARGE_INTEGER, VARIANT_BOOL, WORD

from comtypes import GUID
from comtypes.automation import VARTYPE, VT_BOOL, VT_CLSID, VT_LPWSTR, VT_UI4


class PROPVARIANT_UNION(Union):
	_fields_ = [
		("lVal", LONG),
		("uhVal", ULARGE_INTEGER),
		("boolVal", VARIANT_BOOL),
		("pwszVal", LPWSTR),
		("puuid", GUID),
	]


class PROPVARIANT(Structure):
	_fields_ = [
		("vt", VARTYPE),
		("reserved1", WORD),
		("reserved2", WORD),
		("reserved3", WORD),
		("union", PROPVARIANT_UNION),
	]

	def GetValue(self):
		vt = self.vt
		if vt == VT_BOOL:
			return self.union.boolVal != 0
		elif vt == VT_LPWSTR:
			# return Marshal.PtrToStringUni(union.pwszVal)
			return self.union.pwszVal
		elif vt == VT_UI4:
			return self.union.lVal
		elif vt == VT_CLSID:
			# TODO
			# return (Guid)Marshal.PtrToStructure(union.puuid, typeof(Guid))
			return
		else:
			return "%s:?" % (vt)

	def clear(self):
		windll.ole32.PropVariantClear(byref(self))


class PROPERTYKEY(Structure):
	_fields_ = [
		("fmtid", GUID),
		("pid", DWORD),
	]

	def __str__(self):
		return "%s %s" % (self.fmtid, self.pid)



