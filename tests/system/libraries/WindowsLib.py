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
)

if _typing.TYPE_CHECKING:
	#  F401 used for type checking only
	from SystemTestSpy.speechSpyGlobalPlugin import SpeechIndexT as _SpeechIndexT  # noqa: F401
	from SystemTestSpy.speechSpyGlobalPlugin import NVDASpyLib as _NVDASpyLib


builtIn: _BuiltInLib = _BuiltInLib()
opSys: _OpSysLib = _getLib('OperatingSystem')
process: _ProcessLib = _getLib('Process')
assertsLib: _AssertsLib = _getLib('AssertsLib')

# This library doesn't rely on state, so it is not a class.
# However, if converting to a class note that in Robot libraries, the class name must match the name
# of the module.
# Use caps for both.


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
	startOfTaskSwitcherSpeech = _tryOpenTaskSwitcher(spy)
	if startOfTaskSwitcherSpeech is None:
		# Try opening the task switcher again
		spy.emulateKeyPress('escape')
		# Hack: using 'sleep' is error-prone.
		# Given that opening the task switcher failed, or was too slow, the intention is to dismiss it
		# and give the system time to recover before trying again.
		builtIn.sleep(3)

		startOfTaskSwitcherSpeech = _tryOpenTaskSwitcher(spy)
		if startOfTaskSwitcherSpeech is None:
			raise AssertionError("Tried twice to open task switcher and failed.")

	spy.wait_for_speech_to_finish(speechStartedIndex=startOfTaskSwitcherSpeech)
	speech = spy.get_speech_at_index_until_now(startOfTaskSwitcherSpeech)
	# if there is only one application open, it will already be selected:
	firstItemPattern = _re.compile(r"row 1\s+column 1")
	atFirstItemAlready = bool(firstItemPattern.search(speech))

	if not atFirstItemAlready:
		# The second item (in the task switcher) is normally selected initially (when there are multiple windows),
		# the nominal case is that the first item is the required target.
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress('leftArrow')  # So move back to the first.
		spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
		speech = spy.get_speech_at_index_until_now(nextIndex)
		builtIn.log(f"First window: {speech}", level="DEBUG")

		# ensure this is now the first item
		if not firstItemPattern.search(speech):
			raise AssertionError("Didn't return to the first item with left arrow")

	found = False
	if targetWindowNamePattern.search(speech):
		found = True

	speech = ""
	windowsTested = 1
	while (
		not found
		and not firstItemPattern.search(speech)
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
		builtIn.log(f"next window: {speech}", level="DEBUG")
		if targetWindowNamePattern.search(speech):
			found = True
		windowsTested += 1

	if not found:
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress("escape")
		spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
		raise AssertionError(
			f"Unable to find Window in task switcher matching: {targetWindowNamePattern}\n"
			"See NVDA log for dump of all speech."
		)
	else:
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress("enter")
		if not spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex, errorMessage=None):
			AssertionError(
				f"Expected some speech after enter press."
				f" Speech at index: {nextIndex}"
				f", nextIndex: {spy.get_next_speech_index()}"
				f", speech in range: {spy.get_speech_at_index_until_now(nextIndex)}"
			)


def _tryOpenTaskSwitcher(spy: "_NVDASpyLib") -> _Optional["_SpeechIndexT"]:
	"""
	@param spy: The NVDA spy lib to be used.
	@return: If the task switcher 'row 1' was spoken, the speech index for the start of the task switcher
	speech.
	"""
	expectedStartOfKeypressSpeechIndex = spy.get_next_speech_index()
	spy.emulateKeyPress('control+alt+tab')  # opens the task switcher until enter or escape is pressed.
	# each item has "row 1 column 1" appended, ensure that the task switcher has opened.
	firstRow = "row 1"
	indexOfSpeech: _Optional[int] = spy.wait_for_specific_speech_no_raise(
		firstRow,
		afterIndex=expectedStartOfKeypressSpeechIndex - 1,
		maxWaitSeconds=5,
		intervalBetweenSeconds=0.2
	)
	builtIn.log(f"indexOfSpeech '{firstRow}': {indexOfSpeech}", level="DEBUG")
	if indexOfSpeech:
		return expectedStartOfKeypressSpeechIndex
	return None
