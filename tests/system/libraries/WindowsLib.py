# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" This module provides the WindowsLib Robot Framework Library which allows interacting with Windows GUI
features.
"""

# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from typing import Optional as _Optional
from SystemTestSpy import (
	_getLib,
)
import re
from robot.libraries.BuiltIn import BuiltIn

# Imported for type information
from robot.libraries.OperatingSystem import OperatingSystem as _OpSysLib
from robot.libraries.Process import Process as _ProcessLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

from SystemTestSpy.windows import (
	GetForegroundWindowTitle as _getForegroundWindowTitle,
)

builtIn: BuiltIn = BuiltIn()
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


def taskSwitchToItemMatching(pattern: re.Pattern, maxWindowsToTest: int = 10) -> None:
	"""Opens the task switcher, rightArrows through the items trying to search the for the pattern in the
	speech for each item.
	Raises AssertionError if not found.
	If found "enter" is pressed to select and exit the task switcher, waits for speech to finish after this.
	If not found "escape" is pressed to exit the task switcher, waits for speech to finish after this.
	"""
	spy = _NvdaLib.getSpyLib()
	spy.wait_for_speech_to_finish()

	nextIndex = spy.get_next_speech_index()
	builtIn.log(f"Looking for window: {pattern}", level="DEBUG")
	spy.emulateKeyPress('control+alt+tab')  # opens the task switcher until enter or escape is pressed.
	# each item has "row 1 column 1" appended, ensure that the task switcher has opened.
	indexOfSpeech: _Optional[int] = spy.wait_for_specific_speech_no_raise(
		"row 1",
		afterIndex=nextIndex - 1,
		maxWaitSeconds=5,
		intervalBetweenSeconds=0.2
	)
	if indexOfSpeech is None:
		spy.emulateKeyPress('escape')
		builtIn.sleep(3)

		nextIndex = spy.get_next_speech_index()
		builtIn.log(f"Looking for window: {pattern}", level="DEBUG")
		spy.emulateKeyPress('control+alt+tab')  # opens the task switcher until enter or escape is pressed.
		# each item has "row 1 column 1" appended, ensure that the task switcher has opened.
		indexOfSpeech: _Optional[int] = spy.wait_for_specific_speech_no_raise(
			"row 1",
			afterIndex=nextIndex - 1,
			maxWaitSeconds=5,
			intervalBetweenSeconds=0.2
		)
		if indexOfSpeech is None:
			builtIn.log(f"indexOfSpeech 'row 1': {indexOfSpeech}")
			raise AssertionError("tried twice to open task switcher and failed")

	builtIn.log(f"indexOfSpeech 'row 1': {indexOfSpeech}")

	spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
	speech = spy.get_speech_at_index_until_now(nextIndex)
	# if there is only one application open, it will already be selected:
	firstItemPattern = re.compile(r"row 1\s+column 1")
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
	if pattern.search(speech):
		found = True

	speech = ""
	windowsTested = 1
	while (
		not found
		and not firstItemPattern.search(speech)
		and windowsTested < maxWindowsToTest
	):
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress('rightArrow')  # move to the next task switcher item
		spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
		speech = spy.get_speech_at_index_until_now(nextIndex)
		builtIn.log(f"next window: {speech}", level="DEBUG")
		if pattern.search(speech):
			found = True
		windowsTested += 1

	if not found:
		nextIndex = spy.get_next_speech_index()
		spy.emulateKeyPress("escape")
		spy.wait_for_speech_to_finish(speechStartedIndex=nextIndex)
		raise AssertionError(
			f"Unable to find Window in task switcher matching: {pattern}\n"
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
