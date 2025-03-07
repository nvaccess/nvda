# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.plaintext

"""This module provides the NotepadLib Robot Framework Library which allows system tests to start
Windows Notepad with a text sample and assert NVDA interacts with it in the expected way.
"""

# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from os.path import join as _pJoin
import datetime as _datetime
import tempfile as _tempfile
from typing import Optional as _Optional
from SystemTestSpy import (
	_blockUntilConditionMet,
	_getLib,
)
from SystemTestSpy.windows import (
	GetForegroundWindowTitle,
	GetVisibleWindowTitles,
	GetForegroundHwnd as _getForegroundHwnd,
	GetWindowWithTitle,
	Window as _Window,
)
import re
from robot.libraries.BuiltIn import BuiltIn

# Imported for type information
from robot.libraries.OperatingSystem import OperatingSystem as _OpSysLib
from robot.libraries.Process import Process as _ProcessLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib
import WindowsLib as _WindowsLib

builtIn: BuiltIn = BuiltIn()
opSys: _OpSysLib = _getLib("OperatingSystem")
process: _ProcessLib = _getLib("Process")
assertsLib: _AssertsLib = _getLib("AssertsLib")
windowsLib: _WindowsLib = _getLib("WindowsLib")


# In Robot libraries, class name must match the name of the module. Use caps for both.
class NotepadLib:
	_testFileStagingPath = _tempfile.mkdtemp()
	_testCaseTitle = "test"

	# Use class variables for state that should be tied to the RF library instance.
	# These variables will be available in the teardown
	notepadWindow: _Optional[_Window] = None
	processRFHandleForStart: _Optional[int] = None

	@staticmethod
	def _getTestCasePath(filename):
		return _pJoin(NotepadLib._testFileStagingPath, filename)

	def exit_notepad(self):
		builtIn.log(
			# True is expected due to /wait argument.
			"Is Start process still running (True expected): "
			f"{process.is_process_running(NotepadLib.processRFHandleForStart)}",
		)
		spy = _NvdaLib.getSpyLib()
		if _getForegroundHwnd() == NotepadLib.notepadWindow.hwndVal:
			builtIn.log("Test case in foreground, trying to close")
			spy.emulateKeyPress("alt+f4")
			process.wait_for_process(
				NotepadLib.processRFHandleForStart,
				timeout="10 seconds",
				on_timeout="continue",
			)
		else:
			builtIn.log("Test case not in foreground, can't close it.")
		builtIn.log(
			# False is expected, notepad should have allowed "Start" to exit.
			"Is Start process still running (False expected): "
			f"{process.is_process_running(NotepadLib.processRFHandleForStart)}",
		)

	def start_notepad(self, filePath: str, expectedTitlePattern: re.Pattern) -> _Window:
		builtIn.log(f"starting notepad: {filePath}")
		NotepadLib.processRFHandleForStart = process.start_process(
			"start"  # windows utility to start a process
			# https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/start
			" /wait"  # Starts an application and waits for it to end.
			" notepad"
			f' "{filePath}"',
			shell=True,
			alias="NotepadAlias",
		)
		process.process_should_be_running(NotepadLib.processRFHandleForStart)

		success, NotepadLib.notepadWindow = _blockUntilConditionMet(
			getValue=lambda: GetWindowWithTitle(
				expectedTitlePattern,
				lambda message: builtIn.log(message, "DEBUG"),
			),
			giveUpAfterSeconds=3,
			shouldStopEvaluator=lambda _window: _window is not None,
			intervalBetweenSeconds=0.5,
			errorMessage="Unable to get notepad window",
		)

		if not success or NotepadLib.notepadWindow is None:
			builtIn.fatal_error("Unable to get notepad window")
		return NotepadLib.notepadWindow

	@staticmethod
	def getUniqueTestCaseTitle(testCaseHash: int) -> str:
		return f"{NotepadLib._testCaseTitle} ({abs(testCaseHash)}).txt"

	@staticmethod
	def getUniqueTestCaseTitleRegex(testCaseHash: int) -> re.Pattern:
		return re.compile(f"^{NotepadLib._testCaseTitle} \\({abs(testCaseHash)}\\)")

	@staticmethod
	def _writeTestFile(testCase: str, filename: str) -> str:
		"""
		Creates a file for a plaintext test case.
		@param testCase:  The plaintext sample that is to be tested.
		@return: path to the plaintext file.
		"""
		filePath = NotepadLib._getTestCasePath(filename)
		with open(file=filePath, mode="w", encoding="UTF-8") as f:
			f.write(testCase)
		return filePath

	def _waitForNotepadFocus(self, startsWithTestCaseTitle: re.Pattern):
		"""Wait for Notepad to come into focus."""

		def _isNotepadInForeground() -> bool:
			notepadWindow = GetWindowWithTitle(startsWithTestCaseTitle, builtIn.log)
			if notepadWindow is None:
				return False
			return notepadWindow.hwndVal == _getForegroundHwnd()

		success, _success = _blockUntilConditionMet(
			getValue=_isNotepadInForeground,
			giveUpAfterSeconds=3,
			intervalBetweenSeconds=0.5,
		)
		if success:
			return
		windowInformation = ""
		try:
			windowInformation = f"Foreground Window: {GetForegroundWindowTitle()}.\n"
			windowInformation += f"Open Windows: {GetVisibleWindowTitles()}"
		except OSError as e:
			builtIn.log(f"Couldn't retrieve active window information.\nException: {e}")
		raise AssertionError(
			f"Unable to focus Notepad.\n{windowInformation}",
		)

	def canNotepadTitleBeReported(self, notepadTitleSpeechPattern: re.Pattern) -> bool:
		titleSpeech = _NvdaLib.getSpeechAfterKey("NVDA+t")
		return bool(
			notepadTitleSpeechPattern.search(titleSpeech),
		)

	def prepareNotepad(self, testCase: str) -> None:
		"""
		Starts Notepad opening a file containing the plaintext sample.
		Different versions of notepad/windows have variations in how the title is presented.
		This may mean that there is a file extension in the title.
		E.G. "test.txt - Notepad" or "test – Notepad".
		@param testCase - The plaintext sample to test.
		"""
		spy = _NvdaLib.getSpyLib()
		_testCaseHash = hash(testCase + _datetime.datetime.now().isoformat())
		uniqueTitleRegex = NotepadLib.getUniqueTestCaseTitleRegex(_testCaseHash)
		path = self._writeTestFile(testCase, self.getUniqueTestCaseTitle(_testCaseHash))

		spy.wait_for_speech_to_finish()
		self.start_notepad(path, expectedTitlePattern=uniqueTitleRegex)

		windowsLib.logForegroundWindowTitle()
		testCaseNotepadTitleSpeech = re.compile(
			# Unlike getUniqueTestCaseTitleRegex, this speech does not have to be at the start of the string.
			f"{NotepadLib._testCaseTitle} \\({abs(_testCaseHash)}\\)",
		)
		if not self.canNotepadTitleBeReported(notepadTitleSpeechPattern=testCaseNotepadTitleSpeech):
			builtIn.log("Trying to switch to notepad Window")
			windowsLib.taskSwitchToItemMatching(targetWindowNamePattern=testCaseNotepadTitleSpeech)
			windowsLib.logForegroundWindowTitle()

		self._waitForNotepadFocus(uniqueTitleRegex)
		windowsLib.logForegroundWindowTitle()
		# Move to the start of file
		_NvdaLib.getSpeechAfterKey("home")
