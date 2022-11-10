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

https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsregistersessionnotification
"""

from __future__ import annotations
import contextlib
import ctypes
from contextlib import contextmanager
from ctypes.wintypes import (
	HANDLE,
	HWND,
)
import enum
from typing import (
	Optional,
)

from baseObject import AutoPropertyObject
from systemUtils import _isSecureDesktop
from winAPI.wtsApi32 import (
	WTSINFOEXW,
	WTSQuerySessionInformation,
	WTS_CURRENT_SERVER_HANDLE,
	WTS_CURRENT_SESSION,
	WTS_INFO_CLASS,
	WTSFreeMemory,
	WTS_LockState,
	WTSINFOEX_LEVEL1_W,
)
from logHandler import log

_currentSessionState: Optional["_CurrentSessionState"] = None

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


class WindowsTrackedSession(enum.IntEnum):
	"""
	Windows Tracked Session notifications.
	Members are states which form logical pairs,
	except SESSION_REMOTE_CONTROL which requires more complex handling.
	Values from: https://learn.microsoft.com/en-us/windows/win32/termserv/wm-wtssession-change
	Context:
	https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsregistersessionnotification
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


class _CurrentSessionState(AutoPropertyObject):

	def __init__(self) -> None:
		self._windowsLockStateIsUnknown = False
		"""
		Track if any 'Unknown' Value when querying the Session Lock status has been encountered.
		Resets when a successful Windows lock state query completes.
		"""
		self._prev_isWindowsLockedValue = False
		"""Before NVDA initialization, assume Windows is unlocked.
		This means if Windows is locked, NVDA processes the state change correctly.
		"""
		super().__init__()

	_cache_isWindowsLocked = True

	# typing information for auto property _get_isWindowsLocked
	isWindowsLocked: bool

	def _get_isWindowsLocked(self) -> bool:
		# Reset this at the start of every cache cycle.
		self._windowsLockStateIsUnknown = False
		if _isSecureDesktop():
			# If this is the Secure Desktop,
			# we are in secure mode and on a secure screen,
			# e.g. on the sign-in screen.
			# _isSecureDesktop may also return True on the lock screen before a user has signed in.
			# For more information, refer to devDocs/technicalDesignOverview.md 'Logging in secure mode'
			# and the following userGuide sections:
			# - SystemWideParameters (information on the serviceDebug parameter)
			# - SecureMode and SecureScreens
			isWindowsLocked = False
		else:
			try:
				isWindowsLocked = _isWindowsLocked_checkViaSessionQuery()
			except Exception as e:
				self._recordLockStateTrackingFailure(e)  # Report error repeatedly, attention is required.
				##
				# For security it would be best to treat unknown as locked.
				# However, this would make NVDA unusable.
				# Instead, the user should be warned via UI, and allowed to mitigate the impact themselves.
				# See usage of L{warnSessionLockStateUnknown}.
				isWindowsLocked = False

		if self._prev_isWindowsLockedValue != isWindowsLocked:
			from utils.security import postSessionLockStateChanged
			postSessionLockStateChanged.notify(isNowLocked=isWindowsLocked)

		# set prev value for comparison during the next cache cycle
		self._prev_isWindowsLockedValue = isWindowsLocked
		return isWindowsLocked

	def _recordLockStateTrackingFailure(self, error: Optional[Exception] = None):
		log.error(
			"Unknown lock state, unexpected, potential security issue, please report.",
			exc_info=error
		)  # Report error repeatedly, attention is required.
		##
		# For security it would be best to treat unknown as locked.
		# However, this would make NVDA unusable.
		# Instead, the user should be warned, and allowed to mitigate the impact themselves.
		# See usage of L{warnSessionLockStateUnknown}.
		self._windowsLockStateIsUnknown = True


def initialize() -> None:
	"""
	This function must be called late during NVDA initialization.

	During NVDA initialization,
	core._initializeObjectCaches needs to cache the desktop object,
	regardless of lock state.
	Security checks may cause the desktop object to not be set if NVDA starts on the lock screen.
	As such, during initialization, NVDA should behave as if Windows is unlocked.
	sessionTracking.initialize is called when NVDA initialization is complete, which sets _currentSessionState
	"""
	global _currentSessionState
	log.debug("initializing session tracking")
	_currentSessionState = _CurrentSessionState()


def isWindowsLocked() -> bool:
	"""
	Checks if the Window lockscreen is active.
	Not to be confused with the Windows sign-in screen, a secure screen.
	"""
	if _currentSessionState is None:
		# During NVDA initialization,
		# core._initializeObjectCaches needs to cache the desktop object,
		# regardless of lock state.
		# Security checks may cause the desktop object to not be set if NVDA starts on the lock screen.
		# As such, during initialization, NVDA should behave as if Windows is unlocked.
		# sessionTracking.initialize is called when NVDA initialization is complete, which sets _currentSessionState
		return False
	if _currentSessionState._windowsLockStateIsUnknown:
		from utils.security import warnSessionLockStateUnknown
		import wx
		wx.CallAfter(warnSessionLockStateUnknown)
	return _currentSessionState.isWindowsLocked


def _isWindowsLocked_checkViaSessionQuery() -> bool:
	""" Use a session query to check if the session is locked
	@return: True is the session is locked.
	@raise: Runtime error if the lock state can not be determined via a Session Query.
	"""
	sessionQueryLockState = _getSessionLockedValue()
	if sessionQueryLockState == WTS_LockState.WTS_SESSIONSTATE_UNKNOWN:
		raise RuntimeError(
			"Unable to determine lock state via Session Query."
			f" Lock state value: {sessionQueryLockState!r}"
		)
	return sessionQueryLockState == WTS_LockState.WTS_SESSIONSTATE_LOCK


def isLockStateSuccessfullyTracked() -> bool:
	"""Check if the lock state is successfully tracked.
	I.E. Registered for session tracking AND initial value set correctly.
	@return: True when successfully tracked.
	"""
	# TODO: improve deprecation practice on beta/master merges
	log.error(
		"NVDA no longer registers session tracking notifications. "
		"This function is deprecated, for removal in 2023.1. "
		"It was never expected that add-on authors would use this function"
	)
	return _currentSessionState and not _currentSessionState._windowsLockStateIsUnknown


def register(handle: int) -> bool:
	# TODO: improve deprecation practice on beta/master merges
	log.error(
		"NVDA no longer registers session tracking notifications. "
		"This function is deprecated, for removal in 2023.1. "
		"It was never expected that add-on authors would use this function"
	)
	return True


def unregister(handle: HWND) -> None:
	# TODO: improve deprecation practice on beta/master merges
	log.error(
		"NVDA no longer registers session tracking notifications. "
		"This function is deprecated, for removal in 2023.1. "
		"It was never expected that add-on authors would use this function"
	)


def handleSessionChange(newState: WindowsTrackedSession, sessionId: Optional[int] = None) -> None:
	# TODO: improve deprecation practice on beta/master merges
	log.error(
		"NVDA no longer registers session tracking notifications. "
		"This function is deprecated, for removal in 2023.1. "
		"It was never expected that add-on authors would use this function"
	)


@contextmanager
def WTSCurrentSessionInfoEx() -> contextlib.AbstractContextManager[ctypes.pointer[WTSINFOEXW]]:
	"""Context manager to get the WTSINFOEXW for the current server/session or raises a RuntimeError.
	Handles freeing the memory when usage is complete.
	"""
	info = _getCurrentSessionInfoEx()
	try:
		yield info
	finally:
		WTSFreeMemory(
			ctypes.cast(info, ctypes.c_void_p),
		)


def _getCurrentSessionInfoEx() -> ctypes.POINTER(WTSINFOEXW):
	""" Gets the WTSINFOEXW for the current server/session or raises a RuntimeError
	on failure.
	On RuntimeError memory is first freed.
	In other cases use WTSFreeMemory.
	Ideally use the WTSCurrentSessionInfoEx context manager which will handle freeing the memory.
	"""
	ppBuffer = ctypes.wintypes.LPWSTR(None)
	pBytesReturned = ctypes.wintypes.DWORD(0)

	res = WTSQuerySessionInformation(
		WTS_CURRENT_SERVER_HANDLE,  # WTS_CURRENT_SERVER_HANDLE to indicate the RD Session Host server on
		# which the application is running.
		WTS_CURRENT_SESSION,  # To indicate the session in which the calling application is running
		# (or the current session) specify WTS_CURRENT_SESSION
		WTS_INFO_CLASS.WTSSessionInfoEx,  # Indicates the type of session information to retrieve
		# Fetch a WTSINFOEXW containing a WTSINFOEX_LEVEL1 structure.
		ctypes.pointer(ppBuffer),  # A pointer to a variable that receives a pointer to the requested information.
		# The format and contents of the data depend on the information class specified in the WTSInfoClass
		# parameter.
		# To free the returned buffer, call the WTSFreeMemory function.
		ctypes.pointer(pBytesReturned),  # A pointer to a variable that receives the size, in bytes, of the data
		# returned in ppBuffer.
	)
	try:
		if not res:
			raise RuntimeError(f"Failure calling WTSQuerySessionInformationW: {res}")
		elif ctypes.sizeof(WTSINFOEXW) != pBytesReturned.value:
			raise RuntimeError(
				f"Returned data size failure, got {pBytesReturned.value}, expected {ctypes.sizeof(WTSINFOEXW)}"
			)
		info = ctypes.cast(
			ppBuffer,
			ctypes.POINTER(WTSINFOEXW)
		)
		if (
			not info.contents
			or info.contents.Level != 1
			##
			# Level value must be 1, see:
			# https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/ns-wtsapi32-wtsinfoexa
		):
			raise RuntimeError(
				f"Unexpected Level data, got {info.contents.Level}."
			)
		return info
	except Exception as e:
		log.exception("Unexpected WTSQuerySessionInformation value:", exc_info=e)
		WTSFreeMemory(
			ctypes.cast(ppBuffer, ctypes.c_void_p),
		)


def _getSessionLockedValue() -> WTS_LockState:
	"""Get the WTS_LockState for the current server/session or raises a RuntimeError
	"""
	with WTSCurrentSessionInfoEx() as info:
		infoEx: WTSINFOEX_LEVEL1_W = info.contents.Data.WTSInfoExLevel1
		sessionFlags: ctypes.wintypes.LONG = infoEx.SessionFlags
		lockState = WTS_LockState(sessionFlags)
		log.debug(f"Query Lock state result: {lockState!r}")
		return lockState
