# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Definitions for the (Windows API) WTS Api32
Reference:
https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/WtsApi32.h

This file refers to this header with the convention `WtsApi32.h#L36` meaning line 36 of the above link.
"""

from enum import (
	IntEnum,
)
from typing import Callable
import ctypes  # Use for ctypes.Union to prevent name collision with typing.Union
from ctypes import (
	windll,
	c_void_p,
	c_wchar,
	c_int,
	POINTER,
)
from ctypes.wintypes import (
	HANDLE,
	DWORD,
	ULONG,
	LONG,
	LARGE_INTEGER,
	LPWSTR,
	BOOL,
)


WTS_CURRENT_SERVER_HANDLE = HANDLE(0)
""" WTS_CURRENT_SERVER_HANDLE WtsApi32.h#L36
"""

WTS_CURRENT_SESSION = DWORD(-1)
""" WTS_CURRENT_SESSION WtsApi32.h#L42
"""


# WTSFreeMemory Definition
WTSFreeMemoryT = Callable[[c_void_p], None]
WTSFreeMemory: WTSFreeMemoryT = windll.wtsapi32.WTSFreeMemory
"""WtsApi32.h#L1245"""
WTSFreeMemory.argtypes = (
	c_void_p,  # [in] PVOID pMemory
)
WTSFreeMemory.restype = None


class WTS_INFO_CLASS(IntEnum):
	"""WtsApi32.h#L322
	"""
	WTSInitialProgram = 0
	WTSApplicationName = 1
	WTSWorkingDirectory = 2
	WTSOEMId = 3
	WTSSessionId = 4
	WTSUserName = 5
	WTSWinStationName = 6
	WTSDomainName = 7
	WTSConnectState = 8
	WTSClientBuildNumber = 9
	WTSClientName = 10
	WTSClientDirectory = 11
	WTSClientProductId = 12
	WTSClientHardwareId = 13
	WTSClientAddress = 14
	WTSClientDisplay = 15
	WTSClientProtocolType = 16
	WTSIdleTime = 17
	WTSLogonTime = 18
	WTSIncomingBytes = 19
	WTSOutgoingBytes = 20
	WTSIncomingFrames = 21
	WTSOutgoingFrames = 22
	WTSClientInfo = 23
	WTSSessionInfo = 24
	WTSSessionInfoEx = 25
	WTSConfigInfo = 26
	WTSValidationInfo = 27  # Info Class value used to fetch Validation Information
	# through the WTSQuerySessionInformation
	WTSSessionAddressV4 = 28
	WTSIsRemoteSession = 29


WTS_CONNECTSTATE_CLASS = c_int
""" A value of the WTS_CONNECTSTATE_CLASS enumeration type that specifies the connection state of a Remote
Desktop Services session.
"""

WINSTATIONNAME_LENGTH = 32
"""WtsApi32.h#L81"""

DOMAIN_LENGTH = 17
"""WtsApi32.h#L82"""

USERNAME_LENGTH = 20
"""WtsApi32.h#L60"""


class WTSINFOEX_LEVEL1_W(ctypes.Structure):
	""" WtsApi32.h#L443
	https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/ns-wtsapi32-wtsinfoex_level1_w
	"""
	_fields_ = (
		("SessionId", ULONG),
		("SessionState", WTS_CONNECTSTATE_CLASS),
		("SessionFlags", LONG),
		("WinStationName", c_wchar * (WINSTATIONNAME_LENGTH + 1)),
		("UserName", c_wchar * (USERNAME_LENGTH + 1)),
		("DomainName", c_wchar * (DOMAIN_LENGTH + 1)),
		("LogonTime", LARGE_INTEGER),
		("ConnectTime", LARGE_INTEGER),
		("DisconnectTime", LARGE_INTEGER),
		("LastInputTime", LARGE_INTEGER),
		("CurrentTime", LARGE_INTEGER),
		("IncomingBytes", DWORD),
		("OutgoingBytes", DWORD),
		("IncomingFrames", DWORD),
		("OutgoingFrames", DWORD),
		("IncomingCompressedBytes", DWORD),
		("OutgoingCompressedBytes", DWORD),
	)

	SessionFlags: LONG


class WTSINFOEX_LEVEL_W(ctypes.Union):
	""" WtsApi32.h#L483
	https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/ns-wtsapi32-wtsinfoex_level_w
	"""
	_fields_ = (
		("WTSInfoExLevel1", WTSINFOEX_LEVEL1_W),
	)

	WTSInfoExLevel1: WTSINFOEX_LEVEL1_W


class WTSINFOEXW(ctypes.Structure):
	"""WtsApi32.h#L491
	https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/ns-wtsapi32-wtsinfoexw
	"""
	_fields_ = (
		('Level', DWORD),
		('Data', WTSINFOEX_LEVEL_W),
	)

	Level: DWORD
	Data: WTSINFOEX_LEVEL_W


# WTSQuerySessionInformationW Definition
# WtsApi32.h#L1011
# https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsquerysessioninformationw
WTSQuerySessionInformationT = Callable[
	[
		HANDLE,  # [in] HANDLE hServer
		DWORD,  # [ in] DWORD SessionId
		WTS_INFO_CLASS,  # [ in]  WTS_INFO_CLASS WTSInfoClass,
		POINTER(LPWSTR),  # [out] LPWSTR * ppBuffer. Holds WTSINFOEXW, use ctypes.cast
		POINTER(DWORD),  # [out] DWORD * pBytesReturned
	],
	bool
]
WTSQuerySessionInformation: WTSQuerySessionInformationT = windll.wtsapi32.WTSQuerySessionInformationW
WTSQuerySessionInformation.argtypes = (
	HANDLE,  # [in] HANDLE hServer
	DWORD,  # [ in] DWORD SessionId
	c_int,  # [ in]  WTS_INFO_CLASS WTSInfoClass,
	POINTER(LPWSTR),  # [out] LPWSTR * ppBuffer,
	POINTER(DWORD)  # [out] DWORD * pBytesReturned
)
WTSQuerySessionInformation.restype = BOOL  # On Failure, the return value is zero.


class _WTS_LockState(IntEnum):
	"""
	WtsApi32.h#L437
	"""
	WTS_SESSIONSTATE_UNKNOWN = 0xFFFFFFFF  # dec(4294967295)
	"""The session state is not known."""

	WTS_SESSIONSTATE_LOCK = 0x0
	"""The session is locked."""

	WTS_SESSIONSTATE_UNLOCK = 0x1
	"""The session is unlocked."""


class _WTS_LockState_Win7(IntEnum):
	""" Provide consistent interface to work around defect in Windows Server 2008 R2 and Windows 7.
	Due to a code defect in Windows 7/Server 2008 the values are reversed.
	That is:
	- _WTS_LockState.WTS_SESSIONSTATE_LOCK (0x0) indicates that the session is unlocked
	- _WTS_LockState.WTS_SESSIONSTATE_UNLOCK (0x1) indicates the session is locked.
	"""
	WTS_SESSIONSTATE_UNKNOWN = _WTS_LockState.WTS_SESSIONSTATE_UNKNOWN.value
	"""The session state is not known."""

	WTS_SESSIONSTATE_LOCK = _WTS_LockState.WTS_SESSIONSTATE_UNLOCK.value
	"""The session is locked."""

	WTS_SESSIONSTATE_UNLOCK = _WTS_LockState.WTS_SESSIONSTATE_LOCK.value
	"""The session is unlocked."""


def _setWTS_LockState() -> _WTS_LockState:
	""" Ensure that the correct values for WTS_SESSIONSTATE_LOCK are used based on the platform.
	"""
	return _WTS_LockState


WTS_LockState: _WTS_LockState = _setWTS_LockState()
"""
Set of known session states that NVDA can handle.
These values are different on different versions of Windows.

In some cases, other states such as -0x1 are returned when queried (#14379).
Generally, WTSINFOEX_LEVEL1_W.SessionFlags returns a flag state.
This means that the following is a valid state according to the winAPI:
WTS_SESSIONSTATE_UNKNOWN | WTS_SESSIONSTATE_LOCK | WTS_SESSIONSTATE_UNLOCK.
As mixed states imply an unknown state,
_WTS_LockStateT is an IntEnum rather than an IntFlag and mixed state flags are unexpected enum values.
"""
