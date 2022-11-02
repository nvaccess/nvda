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
)
import enum
from threading import Lock
from typing import (
	Dict,
	Set,
	Optional,
)

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

from .types import HWNDValT


_updateSessionStateLock = Lock()
"""Used to protect updates to _currentSessionStates"""
_currentSessionStates: Set["WindowsTrackedSession"] = set()
"""
Current state of the Windows session associated with this instance of NVDA.
Maintained via receiving session notifications via the NVDA MessageWindow.
Initial state will be set by querying the current status.
Actions which involve updating this state this should be protected by _updateSessionStateLock.
"""

_sessionQueryLockStateHasBeenUnknown = False
"""
Track if any 'Unknown' Value when querying the Session Lock status has been encountered.
"""

_isSessionTrackingRegistered = False
"""
Session tracking is required for NVDA to be notified of lock state changes for security purposes.
"""

RPC_S_INVALID_BINDING = 0x6A6
"""
Error which occurs when Windows is not ready to register session notification tracking.
This error can be prevented by waiting for the event: 'Global\\TermSrvReadyEvent.'

https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--1700-3999-
"""

NOTIFY_FOR_THIS_SESSION = 0
"""
The alternative to NOTIFY_FOR_THIS_SESSION is to be notified for all user sessions.
NOTIFY_FOR_ALL_SESSIONS is not required as NVDA runs on separate user profiles, including the system profile.
"""

SYNCHRONIZE = 0x00100000
"""
Parameter for OpenEventW, blocks thread until event is registered.
https://docs.microsoft.com/en-us/windows/win32/sync/synchronization-object-security-and-access-rights
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


_toggleWindowsSessionStatePair: Dict[WindowsTrackedSession, WindowsTrackedSession] = {
	WindowsTrackedSession.CONSOLE_CONNECT: WindowsTrackedSession.CONSOLE_DISCONNECT,
	WindowsTrackedSession.CONSOLE_DISCONNECT: WindowsTrackedSession.CONSOLE_CONNECT,
	WindowsTrackedSession.REMOTE_CONNECT: WindowsTrackedSession.REMOTE_DISCONNECT,
	WindowsTrackedSession.REMOTE_DISCONNECT: WindowsTrackedSession.REMOTE_CONNECT,
	WindowsTrackedSession.SESSION_LOGON: WindowsTrackedSession.SESSION_LOGOFF,
	WindowsTrackedSession.SESSION_LOGOFF: WindowsTrackedSession.SESSION_LOGON,
	WindowsTrackedSession.SESSION_LOCK: WindowsTrackedSession.SESSION_UNLOCK,
	WindowsTrackedSession.SESSION_UNLOCK: WindowsTrackedSession.SESSION_LOCK,
	WindowsTrackedSession.SESSION_CREATE: WindowsTrackedSession.SESSION_TERMINATE,
	WindowsTrackedSession.SESSION_TERMINATE: WindowsTrackedSession.SESSION_CREATE,
}
"""
Pair of WindowsTrackedSession, where each key has a value of the opposite state.
e.g. SESSION_LOCK/SESSION_UNLOCK.
"""


def _hasLockStateBeenTracked() -> bool:
	"""
	Checks if NVDA is aware of a session lock state change since NVDA started.
	"""
	return bool(_currentSessionStates.intersection({
		WindowsTrackedSession.SESSION_LOCK,
		WindowsTrackedSession.SESSION_UNLOCK
	}))


def _recordLockStateTrackingFailure(error: Optional[Exception] = None):
	log.error(
		"Unknown lock state, unexpected, potential security issue, please report.",
		exc_info=error
	)  # Report error repeatedly, attention is required.
	##
	# For security it would be best to treat unknown as locked.
	# However, this would make NVDA unusable.
	# Instead, the user should be warned, and allowed to mitigate the impact themselves.
	# Reporting is achieved via _sessionQueryLockStateHasBeenUnknown exposed with
	# L{hasLockStateBeenUnknown}.
	global _sessionQueryLockStateHasBeenUnknown
	_sessionQueryLockStateHasBeenUnknown = True


def isWindowsLocked() -> bool:
	"""
	Checks if the Window lockscreen is active.
	Not to be confused with the Windows sign-in screen, a secure screen.
	"""
	if _isSecureDesktop():
		# If this is the Secure Desktop,
		# we are in secure mode and on a secure screen,
		# e.g. on the sign-in screen.
		# _isSecureDesktop may also return True on the lock screen before a user has signed in.

		# For more information, refer to devDocs/technicalDesignOverview.md 'Logging in secure mode'
		# and the following userGuide sections:
		# - SystemWideParameters (information on the serviceDebug parameter)
		# - SecureMode and SecureScreens
		return False
	lockStateTracked = _hasLockStateBeenTracked()
	if lockStateTracked:
		return WindowsTrackedSession.SESSION_LOCK in _currentSessionStates
	else:
		_recordLockStateTrackingFailure()  # Report error repeatedly, attention is required.
		##
		# For security it would be best to treat unknown as locked.
		# However, this would make NVDA unusable.
		# Instead, the user should be warned via UI, and allowed to mitigate the impact themselves.
		# See usage of L{hasLockStateBeenUnknown}.
		return False  # return False, indicating unlocked, to allow NVDA to be used


def _setInitialWindowLockState() -> None:
	"""
	Ensure that session tracking state is initialized.
	If NVDA has started on a lockScreen, it needs to be aware of this.
	As NVDA has already registered for session tracking notifications,
	a lock is used to prevent conflicts.
	"""
	with _updateSessionStateLock:
		lockStateTracked = _hasLockStateBeenTracked()
		if lockStateTracked:
			log.debugWarning(
				"Initial state already set."
				" NVDA may have received a session change notification before initialising"
			)
		# Fall back to explicit query
		try:
			isLocked = _isWindowsLocked_checkViaSessionQuery()
			_currentSessionStates.add(
				WindowsTrackedSession.SESSION_LOCK
				if isLocked
				else WindowsTrackedSession.SESSION_UNLOCK
			)
		except RuntimeError as error:
			_recordLockStateTrackingFailure(error)


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
	return (
		not _sessionQueryLockStateHasBeenUnknown
		or not _isSessionTrackingRegistered
	)


def register(handle: HWNDValT) -> bool:
	"""
	@param handle: handle for NVDA message window.
	When registered, Windows Messages related to session event changes will be
	sent to the message window.
	@returns: True is session tracking is successfully registered.

	Blocks until Windows accepts session tracking registration.

	Every call to this function must be paired with a call to unregister.

	If registration fails, NVDA may not work properly until the session can be registered in a new instance.
	NVDA will not know when the lock screen is activated, which means it becomes a security risk.
	NVDA should warn the user if registering the session notification fails.

	https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsregistersessionnotification
	"""

	# OpenEvent handle must be closed with CloseHandle.
	eventObjectHandle: HANDLE = ctypes.windll.kernel32.OpenEventW(
		# Blocks until WTS session tracking can be registered.
		# Windows needs time for the WTS session tracking service to initialize.
		# NVDA must ensure that the WTS session tracking service is ready before trying to register
		SYNCHRONIZE,  # DWORD dwDesiredAccess
		False,  # BOOL bInheritHandle - NVDA sub-processes do not need to inherit this handle
		# According to the docs, when the Global\TermSrvReadyEvent global event is set,
		# all dependent services have started and WTSRegisterSessionNotification can be successfully called.
		# https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsregistersessionnotification#remarks
		"Global\\TermSrvReadyEvent"  # LPCWSTR lpName - The name of the event object.
	)
	if not eventObjectHandle:
		error = ctypes.WinError()
		log.error("Unexpected error waiting to register session tracking.", exc_info=error)
		return False

	registrationSuccess = ctypes.windll.wtsapi32.WTSRegisterSessionNotification(handle, NOTIFY_FOR_THIS_SESSION)
	ctypes.windll.kernel32.CloseHandle(eventObjectHandle)

	if registrationSuccess:
		log.debug("Registered session tracking")
		# Ensure that an initial state is set.
		# Do this only when session tracking has been registered,
		# so that any changes to the state are not missed via a race condition with session tracking registration.
		# As this occurs after NVDA hs registered for session tracking,
		# it is possible NVDA is expected to handle a session change notification
		# at the same time as initialisation.
		# _updateSessionStateLock is used to prevent received session notifications from being handled at the
		# same time as initialisation.
		_setInitialWindowLockState()
	else:
		error = ctypes.WinError()
		if error.errno == RPC_S_INVALID_BINDING:
			log.error(
				"WTS registration failed. "
				"NVDA waited successfully on TermSrvReadyEvent to ensure that WTS is ready to allow registration. "
				"Cause of failure unknown. "
			)
		else:
			log.error("Unexpected error registering session tracking.", exc_info=error)

	global _isSessionTrackingRegistered
	_isSessionTrackingRegistered = registrationSuccess
	return isLockStateSuccessfullyTracked()


def unregister(handle: HWNDValT) -> None:
	"""
	This function must be called once for every call to register.
	If unregistration fails, NVDA may not work properly until the session can be unregistered in a new instance.

	https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsunregistersessionnotification
	"""
	if not _isSessionTrackingRegistered:
		log.info("Not unregistered session tracking, it was not registered.")
		return
	if ctypes.windll.wtsapi32.WTSUnRegisterSessionNotification(handle):
		log.debug("Unregistered session tracking")
	else:
		error = ctypes.WinError()
		log.error("Unexpected error unregistering session tracking.", exc_info=error)


def handleSessionChange(newState: WindowsTrackedSession, sessionId: int) -> None:
	"""
	Keeps track of the Windows session state.
	When a session change event occurs, the new state is added and the opposite state
	is removed.

	For example a "SESSION_LOCK" event removes the "SESSION_UNLOCK" state.

	This does not track SESSION_REMOTE_CONTROL, which isn't part of a logical pair of states.
	Managing the state of this is more complex, and NVDA does not need to track this status.

	https://docs.microsoft.com/en-us/windows/win32/termserv/wm-wtssession-change
	"""
	with _updateSessionStateLock:
		stateChanged = False

		log.debug(f"Windows Session state notification received: {newState.name}")

		if not _isSessionTrackingRegistered:
			log.debugWarning("Session tracking not registered, unexpected session change message")

		if newState not in _toggleWindowsSessionStatePair:
			log.debug(f"Ignoring {newState} event as tracking is not required.")
			return

		oppositeState = _toggleWindowsSessionStatePair[newState]
		if newState in _currentSessionStates:
			log.error(
				f"NVDA expects Windows to be in {newState} already. "
				f"NVDA may have dropped a {oppositeState} event. "
				f"Dropping this {newState} event. "
			)
		else:
			_currentSessionStates.add(newState)
			stateChanged = True

		if oppositeState in _currentSessionStates:
			_currentSessionStates.remove(oppositeState)
		else:
			log.debugWarning(
				f"NVDA expects Windows to be in {newState} already. "
				f"NVDA may have dropped a {oppositeState} event. "
			)

		log.debug(f"New Windows Session state: {_currentSessionStates}")
		if (
			stateChanged
			and newState in {WindowsTrackedSession.SESSION_LOCK, WindowsTrackedSession.SESSION_UNLOCK}
		):
			from utils.security import postSessionLockStateChanged
			postSessionLockStateChanged.notify(isNowLocked=newState == WindowsTrackedSession.SESSION_LOCK)


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
