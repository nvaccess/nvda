# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Serotek Corporation
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import (
	cast,
	c_int,
	c_uint,
	c_ulong,
	c_ulonglong,
	c_wchar,
	c_wchar_p,
	c_void_p,
	HRESULT,
	POINTER,
	sizeof,
	Structure,
)
from ctypes.wintypes import BOOL, BYTE, DWORD, FILETIME, LPCWSTR, WORD
from enum import IntEnum
from comtypes import GUID, IUnknown, STDMETHOD, COMMETHOD

import winKernel

S_OK = 0

###comtypes class definitions

SVFN_LEN = 262
LANG_LEN = 64
TTSDATAFLAG_TAGGED = 1
TTSI_NAMELEN = SVFN_LEN
TTSI_STYLELEN = SVFN_LEN
TTSATTR_MINPITCH = 0
TTSATTR_MAXPITCH = 0xFFFF
TTSATTR_MINSPEED = 0
TTSATTR_MAXSPEED = 0xFFFFFFFF
TTSATTR_MINVOLUME = 0
TTSATTR_MAXVOLUME = 0xFFFFFFFF
TTSFEATURE_VOLUME = 2
TTSFEATURE_SPEED = 4
TTSFEATURE_PITCH = 8
TTSFEATURE_FIXEDAUDIO = 1024

# Audio related error codes
AUDERR_BADDEVICEID = -2147220735
AUDERR_NEEDWAVEFORMAT = -2147220734
AUDERR_NOTSUPPORTED = -2147467263  # E_NOTIMPL
AUDERR_NOTENOUGHDATA = -2147220991
AUDERR_NOTPLAYING = -2147220730
AUDERR_WAVEFORMATNOTSUPPORTED = -2147220990
AUDERR_WAVEDEVICEBUSY = -2147220989
AUDERR_WAVEDEVNOTSUPPORTED = -2147220718
AUDERR_NOTRECORDING = -2147220717
AUDERR_INVALIDFLAG = -2147220988
AUDERR_NODRIVER = -2147220713
AUDERR_HANDLEBUSY = -2147220712
AUDERR_INVALIDNOTIFYSINK = -2147220711
AUDERR_WAVENOTENABLED = -2147220710
AUDERR_ALREADYCLAIMED = -2147220707
AUDERR_NOTCLAIMED = -2147220706
AUDERR_STILLPLAYING = -2147220705
AUDERR_ALREADYSTARTED = -2147220704
AUDERR_SYNCNOTALLOWED = -2147220703

LANGID = WORD
QWORD = c_ulonglong


class VOICECHARSET(c_int):
	CHARSET_TEXT = 0
	CHARSET_IPAPHONETIC = 1
	CHARSET_ENGINEPHONETIC = 2


class LANGUAGEW(Structure):
	_fields_ = [
		("LanguageID", LANGID),
		("szDialect", c_wchar * LANG_LEN),
	]


LANGUAGE = LANGUAGEW


class TTSMODEINFOW(Structure):
	_fields_ = [
		("gEngine", GUID),
		("szMfgName", c_wchar * TTSI_NAMELEN),
		("szProductName", c_wchar * TTSI_NAMELEN),
		("gModeID", GUID),
		("szModeName", c_wchar * TTSI_NAMELEN),
		("language", LANGUAGEW),
		("szSpeaker", c_wchar * TTSI_NAMELEN),
		("szStyle", c_wchar * TTSI_STYLELEN),
		("wGender", WORD),
		("wAge", WORD),
		("dwFeatures", DWORD),
		("dwInterfaces", DWORD),
		("dwEngineFeatures", DWORD),
	]


TTSMODEINFO = TTSMODEINFOW


class SDATA(Structure):
	_fields_ = [("pData", c_void_p), ("dwSize", DWORD)]


class TTSMOUTH(Structure):
	_fields_ = [
		("bMouthHeight", BYTE),
		("bMouthWidth", BYTE),
		("bMouthUpturn", BYTE),
		("bJawOpen", BYTE),
		("bTeethUpperVisible", BYTE),
		("bTeethLowerVisible", BYTE),
		("bTonguePosn", BYTE),
		("bLipTension", BYTE),
	]


def TextSDATA(text):
	d = SDATA()
	d.pData = cast(c_wchar_p(text), c_void_p)
	d.dwSize = (len(text) + 1) * sizeof(c_wchar)
	return d


class ITTSAttributesW(IUnknown):
	_iid_ = GUID("{1287A280-4A47-101B-931A-00AA0047BA4F}")


ITTSAttributesW._methods_ = [
	STDMETHOD(HRESULT, "PitchGet", [POINTER(WORD)]),
	STDMETHOD(HRESULT, "PitchSet", [WORD]),
	STDMETHOD(HRESULT, "RealTimeGet", [POINTER(DWORD)]),
	STDMETHOD(HRESULT, "RealTimeSet", [DWORD]),
	STDMETHOD(HRESULT, "SpeedGet", [POINTER(DWORD)]),
	STDMETHOD(HRESULT, "SpeedSet", [DWORD]),
	STDMETHOD(HRESULT, "VolumeGet", [POINTER(DWORD)]),
	STDMETHOD(HRESULT, "VolumeSet", [DWORD]),
]

ITTSAttributes = ITTSAttributesW


class ITTSBufNotifySink(IUnknown):
	_iid_ = GUID("{E4963D40-C743-11cd-80E5-00AA003E4B50}")


ITTSBufNotifySink._methods_ = [
	STDMETHOD(HRESULT, "TextDataDone", [QWORD, DWORD]),
	STDMETHOD(HRESULT, "TextDataStarted", [QWORD]),
	STDMETHOD(HRESULT, "BookMark", [QWORD, DWORD]),
	STDMETHOD(HRESULT, "WordPosition", [QWORD, DWORD]),
]


class ITTSCentralW(IUnknown):
	_iid_ = GUID("{28016060-4A47-101B-931A-00AA0047BA4F}")


ITTSCentralW._methods_ = [
	STDMETHOD(HRESULT, "Inject", [LPCWSTR]),
	STDMETHOD(HRESULT, "ModeGet", [POINTER(TTSMODEINFOW)]),
	STDMETHOD(HRESULT, "Phoneme", [VOICECHARSET, DWORD, SDATA, POINTER(SDATA)]),
	STDMETHOD(HRESULT, "PosnGet", [POINTER(QWORD)]),
	STDMETHOD(HRESULT, "TextData", [VOICECHARSET, DWORD, SDATA, c_void_p, GUID]),
	STDMETHOD(HRESULT, "ToFileTime", [POINTER(QWORD), POINTER(winKernel.FILETIME)]),
	STDMETHOD(HRESULT, "AudioPause"),
	STDMETHOD(HRESULT, "AudioResume"),
	STDMETHOD(HRESULT, "AudioReset"),
	STDMETHOD(HRESULT, "Register", [c_void_p, GUID, POINTER(DWORD)]),
	STDMETHOD(HRESULT, "UnRegister", [DWORD]),
]

ITTSCentral = ITTSCentralW


class IAudioMultiMediaDevice(IUnknown):
	_iid_ = GUID("{B68AD320-C743-11cd-80E5-00AA003E4B50}")


IAudioMultiMediaDevice._methods_ = [
	STDMETHOD(HRESULT, "CustomMessage", [c_uint, SDATA]),
	STDMETHOD(HRESULT, "DeviceNumGet", [POINTER(DWORD)]),
	STDMETHOD(HRESULT, "DeviceNumSet", [DWORD]),
]


class ITTSEnumW(IUnknown):
	_iid_ = GUID("{6B837B20-4A47-101B-931A-00AA0047BA4F}")


ITTSEnumW._methods_ = [
	STDMETHOD(
		HRESULT,
		"Next",
		[
			c_ulong,
			POINTER(TTSMODEINFOW),
			POINTER(c_ulong),
		],
	),
	STDMETHOD(HRESULT, "Skip", [c_ulong]),
	STDMETHOD(HRESULT, "Reset"),
	STDMETHOD(HRESULT, "Clone", [POINTER(POINTER(ITTSEnumW))]),
	STDMETHOD(
		HRESULT,
		"Select",
		[
			GUID,
			POINTER(POINTER(ITTSCentralW)),
			POINTER(IUnknown),
		],
	),
]

ITTSEnum = ITTSEnumW


class ITTSNotifySinkW(IUnknown):
	_iid_ = GUID("{C0FA8F40-4A46-101B-931A-00AA0047BA4F}")


ITTSNotifySinkW._methods_ = [
	STDMETHOD(HRESULT, "AttribChanged", [DWORD]),
	STDMETHOD(HRESULT, "AudioStart", [QWORD]),
	STDMETHOD(HRESULT, "AudioStop", [QWORD]),
	STDMETHOD(
		HRESULT,
		"Visual",
		[
			QWORD,
			c_wchar,
			c_wchar,
			DWORD,
			POINTER(TTSMOUTH),
		],
	),
]

ITTSNotifySink = ITTSNotifySinkW


class IAudio(IUnknown):
	_iid_ = GUID("{F546B340-C743-11cd-80E5-00AA003E4B50}")


IAudio._methods_ = [
	COMMETHOD([], HRESULT, "Flush"),
	COMMETHOD([], HRESULT, "LevelGet", (["out"], POINTER(DWORD), "pdwLevel")),
	COMMETHOD([], HRESULT, "LevelSet", (["in"], DWORD, "dwLevel")),
	COMMETHOD(
		[],
		HRESULT,
		"PassNotify",
		(["in"], c_void_p, "pNotifyInterface"),
		(["in"], GUID, "IIDNotifyInterface"),
	),
	COMMETHOD([], HRESULT, "PosnGet", (["out"], POINTER(QWORD), "pqwTimeStamp")),
	COMMETHOD([], HRESULT, "Claim"),
	COMMETHOD([], HRESULT, "UnClaim"),
	COMMETHOD([], HRESULT, "Start"),
	COMMETHOD([], HRESULT, "Stop"),
	COMMETHOD([], HRESULT, "TotalGet", (["out"], POINTER(QWORD), "pqWord")),
	COMMETHOD(
		[],
		HRESULT,
		"ToFileTime",
		(["in"], POINTER(QWORD), "pqWord"),
		(["out"], POINTER(FILETIME), "pFT"),
	),
	COMMETHOD([], HRESULT, "WaveFormatGet", (["out"], POINTER(SDATA), "pdWFEX")),
	COMMETHOD([], HRESULT, "WaveFormatSet", (["in"], SDATA, "dWFEX")),
]


class IAudioDest(IUnknown):
	_iid_ = GUID("{2EC34DA0-C743-11cd-80E5-00AA003E4B50}")


IAudioDest._methods_ = [
	COMMETHOD(
		[],
		HRESULT,
		"FreeSpace",
		(["out"], POINTER(DWORD), "pdwBytes"),
		(["out"], POINTER(BOOL), "pfEOF"),
	),
	COMMETHOD([], HRESULT, "DataSet", (["in"], c_void_p, "pBuffer"), (["in"], DWORD, "dwSize")),
	COMMETHOD([], HRESULT, "BookMark", (["in"], DWORD, "dwMarkID")),
]


class IAudioDestNotifySink(IUnknown):
	_iid_ = GUID("{ACB08C00-C743-11cd-80E5-00AA003E4B50}")


IAudioDestNotifySink._methods_ = [
	STDMETHOD(HRESULT, "AudioStop", [WORD]),
	STDMETHOD(HRESULT, "AudioStart"),
	STDMETHOD(HRESULT, "FreeSpace", [DWORD, BOOL]),
	STDMETHOD(HRESULT, "BookMark", [DWORD, BOOL]),
]


CLSID_MMAudioDest = GUID("{CB96B400-C743-11cd-80E5-00AA003E4B50}")
CLSID_TTSEnumerator = GUID("{D67C0280-C743-11cd-80E5-00AA003E4B50}")


# Defined in mmsyscom.h
MMSYSERR_NOERROR = 0


class DriverMessage(IntEnum):
	"""WaveOutMessage message codes
	Defined in mmddk.h
	"""

	QUERY_INSTANCE_ID = 2065
	"""DRV_QUERYFUNCTIONINSTANCEID """

	QUERY_INSTANCE_ID_SIZE = 2066
	"""DRV_QUERYFUNCTIONINSTANCEIDSIZE """
