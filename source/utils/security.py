# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import hashlib
from typing import (
	Any,
	BinaryIO,
	Callable,
	List,
	Optional,
	Set,
	TYPE_CHECKING,
)

import extensionPoints
from logHandler import log
import systemUtils
from winAPI.sessionTracking import isLockScreenModeActive
import winUser

if TYPE_CHECKING:
	import scriptHandler  # noqa: F401, use for typing
	import NVDAObjects  # noqa: F401, use for typing


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	import NVDAState

	if NVDAState._allowDeprecatedAPI():
		if attrName == "isObjectAboveLockScreen":
			log.warning(
				"isObjectAboveLockScreen(obj) is deprecated. Instead use obj.isBelowLockScreen. ",
			)
			return _isObjectAboveLockScreen
		if attrName == "postSessionLockStateChanged":
			log.warning(
				"postSessionLockStateChanged is deprecated, use post_sessionLockStateChanged instead.",
			)
			return post_sessionLockStateChanged
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


post_sessionLockStateChanged = extensionPoints.Action()
"""
Notifies when a session lock or unlock event occurs.

Usage:
```
def onSessionLockStateChange(isNowLocked: bool):
	'''
	@param isNowLocked: True if new state is locked, False if new state is unlocked
	'''
	pass

post_sessionLockStateChanged.register(onSessionLockStateChange)
post_sessionLockStateChanged.notify(isNowLocked=False)
post_sessionLockStateChanged.unregister(onSessionLockStateChange)
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


def objectBelowLockScreenAndWindowsIsLocked(
	obj: "NVDAObjects.NVDAObject",
	shouldLog: bool = True,
) -> bool:
	"""
	While Windows is locked, the current user session is still running, and below the lock screen
	exists the current user's desktop.

	Windows 10 and 11 doesn't prevent object navigation below the lock screen.

	If an object is above the lock screen, it is accessible and visible to the user
	through the Windows UX while Windows is locked.
	An object below the lock screen should only be accessible when Windows is unlocked,
	as it may contain sensitive information.

	As such, NVDA must prevent accessing and reading objects below the lock screen when Windows is locked.
	@return: C{True} if the Windows 10/11 lockscreen is active and C{obj} is below the lock screen.
	"""
	try:
		isObjectBelowLockScreen = isLockScreenModeActive() and obj.isBelowLockScreen
	except Exception:
		log.exception()
		return False

	if isObjectBelowLockScreen:
		if shouldLog and log.isEnabledFor(log.DEBUG):
			devInfo = "\n".join(obj.devInfo)
			log.debug(f"Attempt at navigating to an object below the lock screen: {devInfo}")
		return True

	return False


def _isObjectAboveLockScreen(obj: "NVDAObjects.NVDAObject") -> bool:
	log.error(
		"This function is deprecated. Instead use obj.isBelowLockScreen. ",
	)
	return not obj.isBelowLockScreen


def _isObjectBelowLockScreen(obj: "NVDAObjects.NVDAObject") -> bool:
	"""
	While Windows is locked, the current user session is still running, and below the lockscreen
	exists the current user's desktop.

	When Windows is locked, the foreground Window is usually LockApp,
	but other Windows can be focused (e.g. Windows Magnifier, reset PIN workflow).

	If an object is above the lockscreen, it is accessible and visible to the user
	through the Windows UX while Windows is locked.
	An object below the lockscreen should only be accessible when Windows is unlocked,
	as it may contain sensitive information.
	"""
	from NVDAObjects.IAccessible import TaskListIcon
	import systemUtils

	if not systemUtils.hasUiAccess():
		# If NVDA does not have UIAccess, it cannot read below the lock screen
		return False

	foregroundWindow = winUser.getForegroundWindow()
	foregroundProcessID, _foregroundThreadID = winUser.getWindowThreadProcessID(foregroundWindow)

	if obj.processID == foregroundProcessID:
		return False

	if (
		# alt+tab task switcher item.
		# The task switcher window does not become the foreground process on the lock screen,
		# so we must whitelist it explicitly.
		isinstance(obj, TaskListIcon)
	):
		return False

	from NVDAObjects.window import Window

	if not isinstance(obj, Window):
		log.debug(
			"Cannot detect if object is below lock app, considering object as safe. ",
		)
		# Must be a window instance to get the HWNDVal, other NVDAObjects do not support this.
		return False

	topLevelWindowHandle = winUser.getAncestor(obj.windowHandle, winUser.GA_ROOT)
	return _isObjectBelowLockScreenCheckZOrder(topLevelWindowHandle)


def _isObjectBelowLockScreenCheckZOrder(objWindowHandle: int) -> bool:
	"""
	This is a risky hack.
	If the order is incorrectly detected,
	secure information may become accessible.

	If these functions fail, where possible,
	NVDA should make NVDA objects accessible.
	"""

	def _isWindowLockScreen(hwnd: winUser.HWNDVal) -> bool:
		"""
		This is a hack/risk, lock screen window class names may change in future.
		Unfortunately the lockApp appModule is not detected on "forgot my PIN" workflow screen.
		However, these lock screen windows are available.
		"""
		lockScreenWindowClasses = {
			"LockScreenInputOcclusionFrame",
			"LockScreenControllerProxyWindow",
			"LockScreenBackstopFrame",
		}

		return winUser.getClassName(hwnd) in lockScreenWindowClasses

	try:
		return _isWindowBelowWindowMatchesCond(objWindowHandle, _isWindowLockScreen)
	except _UnexpectedWindowCountError:
		log.debugWarning(
			"Couldn't determine lock screen and NVDA object relative z-order",
			exc_info=True,
		)
		return False


class _UnexpectedWindowCountError(Exception):
	"""
	Raised when a window which matches the expected condition
	is not found by _isWindowBelowWindowMatchesCond
	"""

	pass


def _isWindowBelowWindowMatchesCond(
	window: winUser.HWNDVal,
	matchCond: Callable[[winUser.HWNDVal], bool],
) -> bool:
	"""
	This is a risky hack.
	The order may be incorrectly detected.

	@returns: True if window is below a window that matches matchCond.
	If the first window is not found, but the second window is,
	it is assumed that the first window is above the second window.

	In the context of _isObjectBelowLockScreenCheckZOrder, NVDA starts at the lowest window,
	and searches up towards the closest/lowest lock screen window.
	If the lock screen window is found before the NVDAObject,
	then the NVDAObject is above the lock screen,
	or not present at all,
	and therefore the NVDAObject should be made accessible.
	This is because if the NVDAObject is not present, we want to make it accessible by default.
	If the lock screen window is not present at all, we also want to make the NVDAObject accessible,
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
			f" - window 2 index: {window2Index}\n",
		)
	if window1Indexes[0] >= window2Index:
		return False
	else:
		return True


_hasSessionLockStateUnknownWarningBeenGiven = False
"""Track whether the user has been notified.
"""


def warnSessionLockStateUnknown() -> None:
	"""Warn the user that the lock state of the computer can not be determined.
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
		" If this error is ongoing then disabling the Windows lock screen is recommended.",
	)

	unableToDetermineSessionLockStateMsg = _(
		# Translators: This is the message for a warning shown if NVDA cannot determine if
		# Windows is locked.
		"NVDA is unable to determine if Windows is locked."
		" While this instance of NVDA is running,"
		" your desktop will not be secure when Windows is locked."
		" Restarting Windows may address this."
		" If this error is ongoing then disabling the Windows lock screen is recommended.",
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


#: The read size for each chunk read from the file, prevents memory overuse with large files.
SHA_BLOCK_SIZE = 65536


def sha256_checksum(binaryReadModeFile: BinaryIO, blockSize: int = SHA_BLOCK_SIZE) -> str:
	"""
	@param binaryReadModeFile: An open file (mode=='rb'). Calculate its sha256 hash.
	@param blockSize: The size of each read.
	@returns: The sha256 hex digest.
	"""
	sha256sum = hashlib.sha256()
	assert binaryReadModeFile.readable() and binaryReadModeFile.mode == "rb"
	f = binaryReadModeFile
	for block in iter(lambda: f.read(blockSize), b""):
		sha256sum.update(block)
	return sha256sum.hexdigest()


def isRunningOnSecureDesktop() -> bool:
	"""
	When NVDA is running on a secure screen,
	it is running on the secure desktop.
	When the serviceDebug parameter is not set,
	NVDA should run in secure mode when on the secure desktop.
	globalVars.appArgs.secure being set to True means NVDA is running in secure mode.

	For more information, refer to projectDocs/design/technicalDesignOverview.md 'Logging in secure mode'
	and the following userGuide sections:
	 - SystemWideParameters (information on the serviceDebug parameter)
	 - SecureMode and SecureScreens
	"""
	return systemUtils._getDesktopName() == "Winlogon"
