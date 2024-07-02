# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" This module provides the WindowsLib Robot Framework Library which allows interacting with Windows GUI
features.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
import typing as _typing
from typing import (
	Optional as _Optional,
)
from SystemTestSpy import (
	_getLib,
)
import re as _re
from robot.libraries.BuiltIn import BuiltIn as _BuiltInLib

# Imported for type information
from robot.libraries.OperatingSystem import OperatingSystem as _OpSysLib
from robot.libraries.Process import Process as _ProcessLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

from SystemTestSpy.windows import (
	GetForegroundWindowTitle as _getForegroundWindowTitle,
	GetForegroundHwnd as _getForegroundHwnd,
	Window as _Window,
)

if _typing.TYPE_CHECKING:
	#  F401 used for type checking only
	from SystemTestSpy.speechSpyGlobalPlugin import SpeechIndexT as _SpeechIndexT  # noqa: F401


builtIn: _BuiltInLib = _BuiltInLib()
opSys: _OpSysLib = _getLib('OperatingSystem')
process: _ProcessLib = _getLib('Process')
assertsLib: _AssertsLib = _getLib('AssertsLib')

# This library doesn't rely on state, so it is not a class.
# However, if converting to a class note that in Robot libraries, the class name must match the name
# of the module.
# Use caps for both.


def isWindowInForeground(window: _Window) -> bool:
	return window.hwndVal == _getForegroundHwnd()


def logForegroundWindowTitle():
	"""Debugging helper, log the current foreground window title to the robot framework log.
	See log.html.
	"""
	windowTitle = _getForegroundWindowTitle()
	builtIn.log(f"Foreground window title: {windowTitle}")


def taskSwitchToItemMatching(targetWindowNamePattern: _re.Pattern, maxWindowsToTest: int = 10) -> None:
	"""Opens the task switcher, rightArrows through the items trying to search the for the pattern in the
	speech for each item.
	Raises AssertionError if not found.
	If found "enter" is pressed to select and exit the task switcher, waits for speech to finish after this.
	If not found "escape" is pressed to exit the task switcher, waits for speech to finish after this.
	"""
	spy = _NvdaLib.getSpyLib()
	spy.wait_for_speech_to_finish()

	builtIn.log(f"Looking for window: {targetWindowNamePattern}", level="DEBUG")
	startOfTaskSwitcherSpeech = _tryOpenTaskSwitcher()
	if startOfTaskSwitcherSpeech is None:
		builtIn.log("No speech for opening the task switcher, trying again", level="DEBUG")
		# Try opening the task switcher again
		spy.emulateKeyPress('escape')
		# Hack: using 'sleep' is error-prone.
		# Given that opening the task switcher failed, or was too slow, the intention is to dismiss it
		# and give the system time to recover before trying again.
		builtIn.sleep(3)

		startOfTaskSwitcherSpeech = _tryOpenTaskSwitcher()
		if startOfTaskSwitcherSpeech is None:
			builtIn.log("No speech for opening the task switcher again", level="DEBUG")
			spy.emulateKeyPress('escape')
			raise AssertionError("Tried twice to open task switcher and failed.")

	spy.wait_for_speech_to_finish(speechStartedIndex=startOfTaskSwitcherSpeech)
	speech = spy.get_speech_at_index_until_now(startOfTaskSwitcherSpeech)
	builtIn.log(f"Open task switch speech: '{speech}'", level="DEBUG")
	# If there is only one application open, it will already be selected:
	# Match "row 1  column 1" not "row 2  column 1" and not "column 1"
	firstRowColPattern = _re.compile(r"row 1\s\scolumn 1")
	atFirstItemAlready = bool(firstRowColPattern.search(speech))

	# Match only "column 1" not "row 1  column 1" and not "row 2  column 1"
	firstColPattern = _re.compile(r"(?<!row \d\s\s)column 1")
	# For a single row of items, returning to the first item will not report the row again.
	returnToFirstItemPattern = firstColPattern
	# When there are many items, cycling through items will result in row changes.
	# Match "row 2  column 1" but not "row 1  column 1" and not "column 1"
	rowChangedPattern = _re.compile(r"row [2-9]\s\scolumn 1")

	found = False
	if targetWindowNamePattern.search(speech):
		builtIn.log("Found target window in first item.", level="DEBUG")
		found = True

	speech = ""
	windowsTested = 1
	while (
		not found
		and not atFirstItemAlready  # no point navigating through items if there is only one.
		and not returnToFirstItemPattern.search(speech)
		# In most cases it is expected that the target Window is close to the top of the z-order.
		# On CI there should not be many windows open.
		# A sanity check on the max windows to test ensures the test does not get stuck cycling through the
		# available windows if the other tests fail for some reason.
		and windowsTested < maxWindowsToTest
	):
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress('rightArrow')  # move to the next task switcher item
		spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
		speech = spy.get_speech_at_index_until_now(nextIndex)
		builtIn.log(f"next window: '{speech}'", level="DEBUG")
		if targetWindowNamePattern.search(speech):
			builtIn.log(f"Found target window at item {windowsTested}", level="DEBUG")
			found = True
		elif rowChangedPattern.search(speech):
			builtIn.log("Multiple task switch rows detected.", level="DEBUG")
			# Once in a row > 1, row and column will be reported when returning to the first row.
			returnToFirstItemPattern = firstRowColPattern
		windowsTested += 1

	if not found:
		builtIn.log("Not found, attempting to close task switcher.", level="DEBUG")
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress("escape")
		spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
		raise AssertionError(
			f"Unable to find Window in task switcher matching: {targetWindowNamePattern}\n"
			"See NVDA log for dump of all speech."
		)
	else:
		builtIn.log("Found, attempting to select.", level="DEBUG")
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress("enter")
		if not spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex, errorMessage=None):
			AssertionError(
				"Expected some speech after enter press."
				f" Speech at index: {nextIndex}"
				f", nextIndex: {spy.get_next_speech_index()}"
				f", speech in range: {spy.get_speech_at_index_until_now(nextIndex)}"
			)


def _tryOpenTaskSwitcher() -> _Optional["_SpeechIndexT"]:
	"""
	@return: If the task switcher 'row 1' was spoken, the speech index for the start of the task switcher
	speech.
	"""
	spy = _NvdaLib.getSpyLib()
	expectedStartOfKeypressSpeechIndex = spy.get_next_speech_index()
	spy.emulateKeyPress('control+alt+tab')  # opens the task switcher until enter or escape is pressed.
	# each item has "row 1 column 1" appended, ensure that the task switcher has opened.
	firstRow = "row 1"
	indexOfSpeech: _Optional[int] = spy.wait_for_specific_speech_no_raise(
		firstRow,
		afterIndex=expectedStartOfKeypressSpeechIndex - 1,
		maxWaitSeconds=5,
		intervalBetweenSeconds=0.3
	)
	builtIn.log(f"indexOfSpeech '{firstRow}': {indexOfSpeech}", level="DEBUG")
	if indexOfSpeech:
		return expectedStartOfKeypressSpeechIndex
	return None
