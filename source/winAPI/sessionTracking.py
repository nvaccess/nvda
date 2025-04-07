# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""
Session tracking was introduced so that NVDA has a mechanism to track activation of the Windows lock screen.
This is required to support the privacy and data integrity of the logged in user.
NVDA restricts access to NVDA settings and certain tools while the system is locked,
and prevents navigating beyond apps open on the lock screen (LockScreen.exe, Magnifier, some notifications).

Used to:
- only allow a whitelist of safe scripts to run
- ensure object navigation cannot occur outside of the lockscreen
"""

from __future__ import annotations
import ctypes
from contextlib import contextmanager
from ctypes.wintypes import (
	DWORD,
	LPWSTR,
)
import enum
from typing import (
	Generator,
	Optional,
)

from baseObject import AutoPropertyObject
from logHandler import log
from NVDAState import _TrackNVDAInitialization

from ._wtsApi32 import (
	WTSINFOEXW,
	WTSQuerySessionInformation,
	WTS_CURRENT_SERVER_HANDLE,
	WTS_CURRENT_SESSION,
	WTS_INFO_CLASS,
	WTSFreeMemory,
	WTS_LockState,
)

RPC_S_INVALID_BINDING = 0x6A6
"""
Error which occurs when Windows is not ready to register session notification tracking.
This error can be prevented by waiting for the event: 'Global\\TermSrvReadyEvent.'

Unused in NVDA core.
"""

NOTIFY_FOR_THIS_SESSION = 0
"""
The alternative to NOTIFY_FOR_THIS_SESSION is to be notified for all user sessions.
NOTIFY_FOR_ALL_SESSIONS is not required as NVDA runs on separate user profiles, including the system profile.

Unused in NVDA core.
"""

SYNCHRONIZE = 0x00100000
"""
Parameter for OpenEventW, blocks thread until event is registered.
https://docs.microsoft.com/en-us/windows/win32/sync/synchronization-object-security-and-access-rights

Unused in NVDA core, duplicate of winKernel.SYNCHRONIZE.
"""

_lockStateTracker: Optional["_WindowsLockedState"] = None
"""
Caches the Windows lock state as an auto property object.
"""
_wasLockedPreviousPumpAll = False
"""
Each core pump cycle, the Windows lock state is updated.
The previous value is tracked, so that changes to the lock state can be detected.
"""


class WindowsTrackedSession(enum.IntEnum):
	"""
	Windows Tracked Session notifications.
	Members are states which form logical pairs,
	except SESSION_REMOTE_CONTROL which requires more complex handling.
	Values from: https://learn.microsoft.com/en-us/windows/win32/termserv/wm-wtssession-change
	Context:
	https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsregistersessionnotification

	Unused in NVDA core.
	"""

	CONSOLE_CONNECT = 1
	CONSOLE_DISCONNECT = 2
	REMOTE_CONNECT = 3
	REMOTE_DISCONNECT = 4
	SESSION_LOGON = 5
	SESSION_LOGOFF = 6
	SESSION_LOCK = 7
	SESSION_UNLOCK = 8
	SESSION_REMOTE_CONTROL = 9
	SESSION_CREATE = 10
	SESSION_TERMINATE = 11


class _WindowsLockedState(AutoPropertyObject):
	"""
	Class to encapsulate caching the Windows lock state.
	"""

	# Refer to AutoPropertyObject for notes on caching
	_cache_isWindowsLocked = True

	# Typing information for auto-property _get_isWindowsLocked
	isWindowsLocked: bool

	def _get_isWindowsLocked(self) -> bool:
		from winAPI.sessionTracking import _isWindowsLocked_checkViaSessionQuery

		return _isWindowsLocked_checkViaSessionQuery()


def initialize():
	global _lockStateTracker
	_lockStateTracker = _WindowsLockedState()


def pumpAll():
	"""Used to track the session lock state every core cycle, and detect changes."""
	global _wasLockedPreviousPumpAll
	from utils.security import post_sessionLockStateChanged

	windowsIsNowLocked = _isWindowsLocked()
	# search for lock app module once lock state is known,
	# but before triggering callbacks via post_sessionLockStateChanged
	if windowsIsNowLocked != _wasLockedPreviousPumpAll:
		_wasLockedPreviousPumpAll = windowsIsNowLocked
		post_sessionLockStateChanged.notify(isNowLocked=windowsIsNowLocked)


def _isWindowsLocked() -> bool:
	if not _TrackNVDAInitialization.isInitializationComplete():
		# Wait until initialization is complete,
		# so NVDA and other consumers can register the lock state
		# via post_sessionLockStateChanged.
		return False
	if _lockStateTracker is None:
		log.error(
			"_TrackNVDAInitialization.markInitializationComplete was called "
			"before sessionTracking.initialize",
		)
		return False
	return _lockStateTracker.isWindowsLocked


def isLockScreenModeActive() -> bool:
	"""
	Checks if the Window lock screen is active.
	Not to be confused with the Windows sign-in screen, a secure screen.
	Includes temporary locked desktops,
	such as the PIN workflow reset and the Out Of Box Experience.
	"""
	from utils.security import isRunningOnSecureDesktop

	if isRunningOnSecureDesktop():
		# Use secure mode instead if on the secure desktop
		return False

	import winVersion

	if winVersion.getWinVer() < winVersion.WIN10:
		# On Windows 8 and Earlier, the lock screen runs on
		# the secure desktop.
		# Lock screen mode is not supported on these Windows versions.
		return False

	return _isWindowsLocked()


def _isWindowsLocked_checkViaSessionQuery() -> bool:
	"""Use a session query to check if the session is locked
	@returns: True is the session is locked.
	Also returns False if the lock state can not be determined via a Session Query.
	"""
	try:
		sessionQueryLockState = _getSessionLockedValue()
	except RuntimeError:
		log.exception("Failure querying session locked state")
		return False
	if sessionQueryLockState == WTS_LockState.WTS_SESSIONSTATE_UNKNOWN:
		log.error(
			f"Unable to determine lock state via Session Query. Lock state value: {sessionQueryLockState!r}",
		)
		return False
	return sessionQueryLockState == WTS_LockState.WTS_SESSIONSTATE_LOCK


_WTS_INFO_POINTER_T = ctypes.POINTER(WTSINFOEXW)


@contextmanager
def WTSCurrentSessionInfoEx() -> Generator[_WTS_INFO_POINTER_T, None, None]:
	"""Context manager to get the WTSINFOEXW for the current server/session or raises a RuntimeError.
	Handles freeing the memory when usage is complete.
	@raises RuntimeError: On failure
	"""
	info = _getCurrentSessionInfoEx()
	if info is None:
		return
	try:
		yield info
	finally:
		WTSFreeMemory(
			ctypes.cast(info, ctypes.c_void_p),
		)


def _getCurrentSessionInfoEx() -> Optional[_WTS_INFO_POINTER_T]:
	"""
	Gets the WTSINFOEXW for the current server/session or raises a RuntimeError
	on failure.
	On RuntimeError memory is first freed.
	In other cases use WTSFreeMemory.
	Ideally use the WTSCurrentSessionInfoEx context manager which will handle freeing the memory.
	@raises RuntimeError: On failure
	"""
	ppBuffer = LPWSTR(None)
	pBytesReturned = DWORD(0)
	info = None

	res = WTSQuerySessionInformation(
		WTS_CURRENT_SERVER_HANDLE,  # WTS_CURRENT_SERVER_HANDLE to indicate the RD Session Host server on
		# which the application is running.
		WTS_CURRENT_SESSION,  # To indicate the session in which the calling application is running
		# (or the current session) specify WTS_CURRENT_SESSION
		WTS_INFO_CLASS.WTSSessionInfoEx,  # Indicates the type of session information to retrieve
		# Fetch a WTSINFOEXW containing a WTSINFOEX_LEVEL1 structure.
		ctypes.byref(
			ppBuffer,
		),  # A pointer to a variable that receives a pointer to the requested information.
		# The format and contents of the data depend on the information class specified in the WTSInfoClass
		# parameter.
		# To free the returned buffer, call the WTSFreeMemory function.
		ctypes.byref(pBytesReturned),  # A pointer to a variable that receives the size, in bytes, of the data
		# returned in ppBuffer.
	)
	try:
		if not res:
			raise RuntimeError(f"Failure calling WTSQuerySessionInformationW: {res}")
		elif ctypes.sizeof(WTSINFOEXW) != pBytesReturned.value:
			raise RuntimeError(
				f"Returned data size failure, got {pBytesReturned.value}, expected {ctypes.sizeof(WTSINFOEXW)}",
			)
		info = ctypes.cast(
			ppBuffer,
			_WTS_INFO_POINTER_T,
		)
		if (
			not info.contents or info.contents.Level != 1
			##
			# Level value must be 1, see:
			# https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/ns-wtsapi32-wtsinfoexa
		):
			raise RuntimeError(
				f"Unexpected Level data, got {info.contents.Level}.",
			)
		return info
	except Exception as e:
		log.exception("Unexpected WTSQuerySessionInformation value:", exc_info=e)
		WTSFreeMemory(  # should this be moved to a finally block?
			ctypes.cast(ppBuffer, ctypes.c_void_p),
		)
		return None


def _getSessionLockedValue() -> WTS_LockState:
	"""Get the WTS_LockState for the current server/session.
	@raises RuntimeError: if fetching the session info fails.
	"""
	with WTSCurrentSessionInfoEx() as info:
		infoEx = info.contents.Data.WTSInfoExLevel1
		sessionFlags = infoEx.SessionFlags
		try:
			lockState = WTS_LockState(sessionFlags)
		except ValueError:
			# If an unexpected flag value is provided,
			# the WTS_LockState enum will not be constructed and will raise ValueError.
			# In some cases sessionFlags = -0x1 is returned (#14379).
			# Also, SessionFlags returns a flag state. This means that the following is a valid result:
			# sessionFlags = WTS_SESSIONSTATE_UNKNOWN | WTS_SESSIONSTATE_LOCK | WTS_SESSIONSTATE_UNLOCK.
			# As mixed states imply an unknown state,
			# WTS_LockState is an IntEnum rather than an IntFlag and mixed state flags are unexpected enum values.
			return WTS_LockState.WTS_SESSIONSTATE_UNKNOWN
		return lockState
