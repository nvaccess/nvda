# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import typing
from typing import (
	Set,
)

from logHandler import log
from winAPI.sessionTracking import isWindowsLocked
import winUser

if typing.TYPE_CHECKING:
	import appModuleHandler
	import scriptHandler  # noqa: F401, use for typing
	import NVDAObjects


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
		commands.script_reportCurrentFocus,
		commands.script_title,
		commands.script_dateTime,
		commands.script_say_battery_status,
		commands.script_navigatorObject_current,
		commands.script_navigatorObject_currentDimensions,
		commands.script_navigatorObject_toFocus,
		commands.script_navigatorObject_moveFocus,
		commands.script_navigatorObject_parent,
		commands.script_navigatorObject_next,
		commands.script_navigatorObject_previous,
		commands.script_navigatorObject_firstChild,
		commands.script_navigatorObject_devInfo,
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
		commands.script_braille_scrollBack,
		commands.script_braille_scrollForward,
		commands.script_braille_routeTo,
		commands.script_braille_previousLine,
		commands.script_braille_nextLine,
		commands.script_navigatorObject_nextInFlow,
		commands.script_navigatorObject_previousInFlow,
		commands.script_touch_changeMode,
		commands.script_touch_newExplore,
		commands.script_touch_explore,
		commands.script_touch_hoverUp,
		commands.script_moveMouseToNavigatorObject,
		commands.script_moveNavigatorObjectToMouse,
		commands.script_leftMouseClick,
		commands.script_rightMouseClick,
	}


def _isLockAppAndAlive(appModule: "appModuleHandler.AppModule") -> bool:
	return appModule.appName == "lockapp" and appModule.isAlive


# TODO: mark this API as public when it becomes stable (i.e. remove the underscore).
# Add-on authors may require this function to make their code secure.
# Consider renaming (e.g. objectOutsideOfLockScreenAndWindowsIsLocked).
def _isSecureObjectWhileLockScreenActivated(
		obj: "NVDAObjects.NVDAObject",
		shouldLog: bool = True,
) -> bool:
	"""
	While Windows is locked, Windows 10 and 11 doesn't prevent object navigation outside of the lockscreen.
	As such, NVDA must prevent accessing and reading objects outside of the lockscreen when Windows is locked.
	@return: C{True} if the Windows 10/11 lockscreen is active and C{obj} is outside of the lock screen.
	"""
	if isWindowsLocked() and not isObjectAboveLockScreen(obj):
		if shouldLog and log.isEnabledFor(log.DEBUG):
			devInfo = '\n'.join(obj.devInfo)
			log.debug(f"Attempt at navigating to a secure object: {devInfo}")
		return True

	return False


def isObjectAboveLockScreen(obj: "NVDAObjects.NVDAObject") -> bool:
	"""
	When Windows is locked, the foreground Window is usually LockApp,
	but other Windows can be focused (e.g. Windows Magnifier).
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
