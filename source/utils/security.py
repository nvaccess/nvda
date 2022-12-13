# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import typing
from typing import (
	Set,
)

import extensionPoints
from logHandler import log
from winAPI.sessionTracking import isWindowsLocked
import winUser

if typing.TYPE_CHECKING:
	import appModuleHandler
	import scriptHandler  # noqa: F401, use for typing
	import NVDAObjects


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
		# Mouse click events are harmless.
		# Mouse clicks are already exposed by Windows, and these scripts emulate those mouse clicks,
		# rather than passing a click event to an NVDAObject / HWND.
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


def objectBelowLockScreenAndWindowsIsLocked(
		obj: "NVDAObjects.NVDAObject",
		shouldLog: bool = True,
) -> bool:
	"""
	While Windows is locked, the current user session is still running, and below the lockscreen
	exists the current user's desktop.

	Windows 10 and 11 doesn't prevent object navigation below the lockscreen.

	If an object is above the lockscreen, it is accessible and visible to the user
	through the Windows UX while Windows is locked.
	An object below the lockscreen should only be accessible when Windows is unlocked,
	as it may contain sensitive information.

	As such, NVDA must prevent accessing and reading objects below the lockscreen when Windows is locked.
	@return: C{True} if the Windows 10/11 lockscreen is active and C{obj} is below the lock screen.
	"""
	if isWindowsLocked() and not isObjectAboveLockScreen(obj):
		if shouldLog and log.isEnabledFor(log.DEBUG):
			devInfo = '\n'.join(obj.devInfo)
			log.debug(f"Attempt at navigating to a secure object: {devInfo}")
		return True

	return False


def isObjectAboveLockScreen(obj: "NVDAObjects.NVDAObject") -> bool:
	"""
	While Windows is locked, the current user session is still running, and below the lockscreen
	exists the current user's desktop.

	When Windows is locked, the foreground Window is usually LockApp,
	but other Windows can be focused (e.g. Windows Magnifier).

	If an object is above the lockscreen, it is accessible and visible to the user
	through the Windows UX while Windows is locked.
	An object below the lockscreen should only be accessible when Windows is unlocked,
	as it may contain sensitive information.
	"""
	import appModuleHandler
	from IAccessibleHandler import SecureDesktopNVDAObject
	from NVDAObjects.IAccessible import TaskListIcon

	foregroundWindow = winUser.getForegroundWindow()
	foregroundProcessID, _foregroundThreadID = winUser.getWindowThreadProcessID(foregroundWindow)

	if obj.processID == foregroundProcessID:
		return True

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
		return True

	runningAppModules = appModuleHandler.runningTable.values()
	lockAppModule = next(filter(_isLockAppAndAlive, runningAppModules), None)

	if lockAppModule is None:
		# lockAppModule not running/registered by NVDA yet
		log.debugWarning(
			"lockAppModule not detected when Windows is locked. "
			"Cannot detect if object is in lock app, considering object as insecure. "
		)
	elif lockAppModule is not None and obj.processID == lockAppModule.processID:
		return True

	return False


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
