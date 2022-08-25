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

import ctypes
from ctypes.wintypes import (
	HANDLE,
)
import enum
from typing import (
	Dict,
	Set,
)

from logHandler import log

from .types import HWNDValT


_currentSessionStates: Set["WindowsTrackedSession"] = set()
"""
Current state of the Windows session associated with this instance of NVDA.
Maintained via receiving session notifications via the NVDA MessageWindow.
"""


RPC_S_INVALID_BINDING = 0x6A6
"""
Error which occurs when Windows is not ready to register session notification tracking.
This error can be prevented by waiting for the event: 'Global\\TermSrvReadyEvent.'
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


def isWindowsLocked() -> bool:
	"""
	Checks if the Window lockscreen is active.

	Not to be confused with the Windows sign-in screen, a secure screen.
	"""
	return WindowsTrackedSession.SESSION_LOCK in _currentSessionStates


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

	return registrationSuccess


def unregister(handle: HWNDValT) -> None:
	"""
	This function must be called once for every call to register.
	If unregistration fails, NVDA may not work properly until the session can be unregistered in a new instance.

	https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsunregistersessionnotification
	"""
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

	log.debug(f"Windows Session state notification received: {newState.name}")

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

	if oppositeState in _currentSessionStates:
		_currentSessionStates.remove(oppositeState)
	else:
		log.debug(f"NVDA started in state {oppositeState.name} or dropped a state change event")

	log.debug(f"New Windows Session state: {_currentSessionStates}")
