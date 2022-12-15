# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import typing
from typing import (
	Callable,
	List,
	Optional,
	Set,
)

import extensionPoints
from logHandler import log
from winAPI.sessionTracking import _isLockScreenModeActive
import winUser

if typing.TYPE_CHECKING:
	import appModuleHandler  # noqa: F401, use for typing
	import scriptHandler  # noqa: F401, use for typing
	import NVDAObjects  # noqa: F401, use for typing


postSessionLockStateChanged = extensionPoints.Action()
"""
Notifies when a session lock or unlock event occurs.

Usage:
```
def onSessionLockStateChange(isNowLocked: bool):
	'''
	@param isNowLocked: True if new state is locked, False if new state is unlocked
	'''
	pass

postSessionLockStateChanged.register(onSessionLockStateChange)
postSessionLockStateChanged.notify(isNowLocked=False)
postSessionLockStateChanged.unregister(onSessionLockStateChange)
```
"""


def getSafeScripts() -> Set["scriptHandler._ScriptFunctionT"]:
	"""
	Returns scripts which are safe to use on the Windows lockscreen.
	Not to be confused with the Windows sign-in screen, a secure screen.
	"""
	# Import late to avoid circular import.
	# We need to import this here because this might be the first import of this module
	# and it might be needed by global maps.
	from globalCommands import commands
	return {
		# The focus object should not cache secure content
		# due to handling in `api.setFocusObject`.
		commands.script_reportCurrentFocus,
		
		# Reports the foreground window.
		# The foreground object should not cache secure content
		# due to handling in `api.setForegroundObject`.
		commands.script_title,
		
		# Reports system information that should be accessible from the lock screen.
		commands.script_dateTime,
		commands.script_say_battery_status,
		
		# Mouse navigation is required to ensure controls
		# on the lock screen are accessible.
		# Preventing mouse navigation outside the lock screen
		# is handled using `api.setMouseObject` and `api.setNavigatorObject`.
		commands.script_moveMouseToNavigatorObject,
		commands.script_moveNavigatorObjectToMouse,
		commands.script_leftMouseClick,
		commands.script_rightMouseClick,
		
		# Braille commands are safe, and required to interact
		# on the lock screen using braille.
		commands.script_braille_scrollBack,
		commands.script_braille_scrollForward,
		commands.script_braille_routeTo,
		commands.script_braille_previousLine,
		commands.script_braille_nextLine,
		
		# Object navigation is required to ensure controls
		# on the lock screen are accessible.
		# Preventing object navigation outside the lock screen
		# is handled in `api.setNavigatorObject` and by applying `LockScreenObject`.
		commands.script_navigatorObject_current,
		commands.script_navigatorObject_currentDimensions,
		commands.script_navigatorObject_toFocus,
		commands.script_navigatorObject_moveFocus,
		commands.script_navigatorObject_parent,
		commands.script_navigatorObject_next,
		commands.script_navigatorObject_previous,
		commands.script_navigatorObject_firstChild,
		commands.script_navigatorObject_nextInFlow,
		commands.script_navigatorObject_previousInFlow,
		
		# Moving the review cursor is required to ensure controls
		# on the lock screen are accessible.
		# Preventing review cursor navigation outside the lock screen
		# is handled in `api.setReviewPosition`.
		commands.script_review_activate,
		commands.script_review_top,
		commands.script_review_previousLine,
		commands.script_review_currentLine,
		commands.script_review_nextLine,
		commands.script_review_bottom,
		commands.script_review_previousWord,
		commands.script_review_currentWord,
		commands.script_review_nextWord,
		commands.script_review_startOfLine,
		commands.script_review_previousCharacter,
		commands.script_review_currentCharacter,
		commands.script_review_nextCharacter,
		commands.script_review_endOfLine,
		commands.script_review_sayAll,
		
		# Using the touch screen is required to ensure controls
		# on the lock screen are accessible.
		# Preventing touch navigation outside the lock screen
		# is handled in `screenExplorer.ScreenExplorer.moveTo`.
		commands.script_touch_changeMode,  # cycles through available touch screen modes
		commands.script_touch_newExplore,  # tap gesture, reports content under the finger
		commands.script_touch_explore,  # hover gesture, reports content changes under the finger
		commands.script_touch_hoverUp,  # hover up gesture, fixes a situation with touch typing
		# commands.script_touch_rightClick, TODO: consider adding, was this missed previously?
	}


def _isLockAppAndAlive(appModule: "appModuleHandler.AppModule") -> bool:
	return appModule.appName == "lockapp" and appModule.isAlive


# TODO: Consider renaming to _objectBelowLockScreenAndWindowsIsLocked.
def _isSecureObjectWhileLockScreenActivated(
		obj: "NVDAObjects.NVDAObject",
		shouldLog: bool = True,
) -> bool:
	"""
	While Windows is locked, Windows 10 and 11 doesn't prevent object navigation outside of the lockscreen.
	As such, NVDA must prevent accessing and reading objects outside of the lockscreen when Windows is locked.
	@return: C{True} if the Windows 10/11 lockscreen is active and C{obj} is below the lock screen.
	"""
	try:
		isObjectBelowLockScreen = _isLockScreenModeActive() and obj.isBelowLockScreen
	except Exception:
		log.exception()
		return False

	if isObjectBelowLockScreen:
		if shouldLog and log.isEnabledFor(log.DEBUG):
			devInfo = '\n'.join(obj.devInfo)
			log.debug(f"Attempt at navigating to an object below the lock screen: {devInfo}")
		return True

	return False


def isObjectAboveLockScreen(obj: "NVDAObjects.NVDAObject") -> bool:
	# TODO: improve deprecation practice on beta/master merges
	log.error(
		"This function is deprecated. "
		"Instead use obj.isBelowLockScreen. "
	)
	return not obj.isBelowLockScreen


def _findLockAppModule() -> Optional["appModuleHandler.AppModule"]:
	import appModuleHandler
	runningAppModules = appModuleHandler.runningTable.values()
	return next(filter(_isLockAppAndAlive, runningAppModules), None)


def _searchForLockAppModule():
	from appModuleHandler import _checkWindowsForAppModules
	if _isLockScreenModeActive():
		lockAppModule = _findLockAppModule()
		if lockAppModule is None:
			_checkWindowsForAppModules()


def _isObjectBelowLockScreen(obj: "NVDAObjects.NVDAObject") -> bool:
	"""
	When Windows is locked, the foreground Window is usually LockApp,
	but other Windows can be focused (e.g. Windows Magnifier, reset PIN workflow).
	"""
	from IAccessibleHandler import SecureDesktopNVDAObject
	from NVDAObjects.IAccessible import TaskListIcon

	foregroundWindow = winUser.getForegroundWindow()
	foregroundProcessID, _foregroundThreadID = winUser.getWindowThreadProcessID(foregroundWindow)

	if obj.processID == foregroundProcessID:
		return False

	if (
		# alt+tab task switcher item.
		# The task switcher window does not become the foreground process on the lock screen,
		# so we must whitelist it explicitly.
		isinstance(obj, TaskListIcon)
		# Secure Desktop Object.
		# Used to indicate to the user and to API consumers (including NVDA remote) via gainFocus,
		# that the user has switched to a secure desktop.
		or isinstance(obj, SecureDesktopNVDAObject)
	):
		return False

	lockAppModule = _findLockAppModule()
	if lockAppModule is None:
		# lockAppModule not running/registered by NVDA yet.
		# This is not an expected state.
		log.error(
			"lockAppModule not detected when Windows is locked. "
			"Cannot detect if object is below lock app, considering object as safe. "
		)
		return False

	from NVDAObjects.window import Window
	if not isinstance(obj, Window):
		log.debug(
			"Cannot detect if object is below lock app, considering object as safe. "
		)
		# Must be a window instance to get the HWNDVal, other NVDAObjects do not support this.
		return False

	topLevelWindowHandle = winUser.getAncestor(obj.windowHandle, winUser.GA_ROOT)
	return _isObjectBelowLockScreenCheckZOrder(topLevelWindowHandle, lockAppModule.processID)


def _isObjectBelowLockScreenCheckZOrder(objWindowHandle: int, lockAppModuleProcessId: int) -> bool:
	"""
	This is a risky hack.
	If the order is incorrectly detected,
	secure information may become accessible.

	If these functions fail, where possible,
	NVDA should make NVDA objects accessible.
	"""

	def _isWindowLockApp(hwnd: winUser.HWNDVal) -> bool:
		windowProcessId, _threadId = winUser.getWindowThreadProcessID(hwnd)
		return windowProcessId == lockAppModuleProcessId

	try:
		return _isWindowBelowWindowMatchesCond(objWindowHandle, _isWindowLockApp)
	except _UnexpectedWindowCountError:
		log.debugWarning("Couldn't find lock screen")
		return False


class _UnexpectedWindowCountError(Exception):
	"""
	Raised when a window which matches the expected condition
	is not found by _isWindowBelowWindowMatchesCond
	"""
	pass


def _isWindowBelowWindowMatchesCond(
		window: winUser.HWNDVal,
		matchCond: Callable[[winUser.HWNDVal], bool]
) -> bool:
	"""
	This is a risky hack.
	The order may be incorrectly detected.

	@returns: True if window is below a window that matches matchCond.
	If the first window is not found, but the second window is,
	it is assumed that the first window is below the second window.

	In the context of _isObjectBelowLockScreenCheckZOrder, NVDA starts at the lowest window,
	and searches up towards the closest/lowest lock screen window.
	If the lock screen window is found before the NVDAobject, the object should be made accessible.
	This is because if the NVDAObject is not present, we want to make it accessible by default.
	If the lock screen window is not present, we also want to make the NVDAObject accessible,
	so the lock screen window must be comprehensively searched for.
	If the NVDAObject is found, and then a lock screen window,
	the object is not made accessible as it is below the lock screen.
	Edge cases and failures should be handled by making the object accessible.

	Refer to test_security for testing cases which demonstrate this behaviour.
	"""
	desktopWindow = winUser.getDesktopWindow()
	topLevelWindow = winUser.getTopWindow(desktopWindow)
	bottomWindow = winUser.getWindow(topLevelWindow, winUser.GW_HWNDLAST)
	currentWindow = bottomWindow
	currentIndex = 0  # 0 is the last/lowest window
	window1Indexes: List[int] = []
	window2Index: Optional[int] = None
	while currentWindow != winUser.GW_RESULT_NOT_FOUND:
		if currentWindow == window:
			window1Indexes.append(currentIndex)
		if matchCond(currentWindow):
			if not window1Indexes:
				return False
			window2Index = currentIndex
			break
		currentWindow = winUser.getWindow(currentWindow, winUser.GW_HWNDPREV)
		currentIndex += 1
	if len(window1Indexes) != 1 or window2Index is None:
		raise _UnexpectedWindowCountError(
			"Windows found\n"
			f" - window 1 indexes: {window1Indexes} (expects len 1)\n"
			f" - window 2 index: {window2Index}\n"
		)
	if window1Indexes[0] >= window2Index:
		return False
	else:
		return True


_hasSessionLockStateUnknownWarningBeenGiven = False
"""Track whether the user has been notified.
"""


def warnSessionLockStateUnknown() -> None:
	""" Warn the user that the lock state of the computer can not be determined.
	NVDA will not be able to determine if Windows is on the lock screen
	(LockApp on Windows 10/11), and will not be able to ensure privacy/security
	of the signed-in user against unauthenticated users.
	@note Only warn the user once.
	"""
	global _hasSessionLockStateUnknownWarningBeenGiven
	if _hasSessionLockStateUnknownWarningBeenGiven:
		return
	_hasSessionLockStateUnknownWarningBeenGiven = True

	log.warning(
		"NVDA is unable to determine if Windows is locked."
		" While this instance of NVDA is running,"
		" your desktop will not be secure when Windows is locked."
		" Restarting Windows may address this."
		" If this error is ongoing then disabling the Windows lock screen is recommended."
	)

	unableToDetermineSessionLockStateMsg = _(
		# Translators: This is the message for a warning shown if NVDA cannot determine if
		# Windows is locked.
		"NVDA is unable to determine if Windows is locked."
		" While this instance of NVDA is running,"
		" your desktop will not be secure when Windows is locked."
		" Restarting Windows may address this."
		" If this error is ongoing then disabling the Windows lock screen is recommended."
	)

	import wx  # Late import to prevent circular dependency.
	import gui  # Late import to prevent circular dependency.
	log.debug("Presenting session lock tracking failure warning.")
	gui.messageBox(
		unableToDetermineSessionLockStateMsg,
		# Translators: This is the title for a warning dialog, shown if NVDA cannot determine if
		# Windows is locked.
		caption=_("Lock screen not secure while using NVDA"),
		style=wx.ICON_ERROR | wx.OK,
	)
