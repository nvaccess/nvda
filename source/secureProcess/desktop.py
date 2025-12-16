# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import contextlib
import uuid
import ctypes
from ctypes.wintypes import (
	HANDLE,
)
import win32service
import win32con
from winBindings.user32 import (
	CreateDesktopEx,
	CloseDesktop,
	DESKTOP_ALL_ACCESS,
)
from .raiiUtils import makeAutoFree
from logHandler import log


def createTempWindowStation(securityAttribs=None) -> tuple[str, HANDLE]:
	"""Create a temporary window station and return its name and handle.

	This function creates a uniquely named window station. The new window
	station is created with GENERIC_ALL access by default. Callers are
	responsible for closing or releasing the returned handle when it is
	no longer needed.

	:param securityAttribs: Optional pywin32 security attributes to apply when
		creating the window station.
	:returns: A tuple containing the name of the created window station and
		a handle to the window station.
	"""
	windowStationName = f"nvWinSta-{uuid.uuid4()}"
	winStationAccess = win32con.GENERIC_ALL
	log.debug("Calling CreateWindowStation...")
	winStationHandle = win32service.CreateWindowStation(
		windowStationName,
		0,
		winStationAccess,
		securityAttribs,
	)
	return windowStationName, winStationHandle

def createTempDesktop(securityAttribs=None) -> tuple[str, HANDLE]:
	"""Create a temporary desktop and return its name and handle.

	This function creates a uniquely named desktop and attempts to create it
	with DESKTOP_ALL_ACCESS by default. The returned value is a tuple of the
	desktop name and a handle object that represents the created desktop.

	:param securityAttribs: Optional pywin32 security attributes to apply when
		creating the desktop.
	:returns: A tuple containing the name of the created desktop and a handle
		to the desktop.
	:raises RuntimeError: If the underlying desktop creation fails.
	"""

	desktopName = f"nvDesktop-{uuid.uuid4()}"
	desktopAccess =  DESKTOP_ALL_ACCESS
	log.debug("Calling CreateDesktop...")
	desktopHandle = win32service.CreateDesktop(desktopName, 0, desktopAccess, securityAttribs)
	return desktopName, desktopHandle


@contextlib.contextmanager
def temporarilySwitchWindowStation(newWinStationHandle):
	"""Temporarily switch the current process window station.

	This context manager sets the process window station to the provided
	handle for the duration of the with-block and restores the original
	window station on exit, even if an exception is raised.

	:param newWinStationHandle: Handle to the window station to switch to.

	:yield: None. Execution resumes inside the with-block while the new
		window station is active.

	:raises: Any exception raised within the with-block is propagated after
		the original window station has been restored.

	"""

	oldWinStationHandle = win32service.GetProcessWindowStation()
	log.debug("Switching to temporary window station...")
	newWinStationHandle.SetProcessWindowStation()
	try:
		yield
	finally:
		log.debug("Restoring original window station...")
		oldWinStationHandle.SetProcessWindowStation()
