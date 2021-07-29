# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.plaintext

""" This module provides the NotepadLib Robot Framework Library which allows system tests to start
Windows Notepad with a text sample and assert NVDA interacts with it in the expected way.
"""

# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from os.path import join as _pJoin
import tempfile as _tempfile
from typing import Optional as _Optional
from SystemTestSpy import (
	_blockUntilConditionMet,
	_getLib,
)
from SystemTestSpy.windows import (
	GetForegroundWindowTitle,
	GetVisibleWindowTitles,
	SetForegroundWindow,
)
import re
from robot.libraries.BuiltIn import BuiltIn

# Imported for type information
from robot.libraries.OperatingSystem import OperatingSystem as _OpSysLib
from robot.libraries.Process import Process as _ProcessLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

builtIn: BuiltIn = BuiltIn()
opSys: _OpSysLib = _getLib('OperatingSystem')
process: _ProcessLib = _getLib('Process')
assertsLib: _AssertsLib = _getLib('AssertsLib')


# In Robot libraries, class name must match the name of the module. Use caps for both.
class NotepadLib:
	_testFileStagingPath = _tempfile.mkdtemp()
	_testCaseTitle = "test"

	def __init__(self):
		self.notepadHandle: _Optional[int] = None

	@staticmethod
	def _getTestCasePath(filename):
		return _pJoin(NotepadLib._testFileStagingPath, filename)

	def exit_notepad(self):
		spy = _NvdaLib.getSpyLib()
		spy.emulateKeyPress('alt+f4')
		process.wait_for_process(self.notepadHandle, timeout="1 minute", on_timeout="continue")

	def start_notepad(self, filePath):
		builtIn.log(f"starting notepad: {filePath}")
		self.notepadHandle = process.start_process(
			"start notepad"
			f' "{filePath}"',
			shell=True,
			alias='NotepadAlias',
		)
		process.process_should_be_running(self.notepadHandle)
		return self.notepadHandle

	@staticmethod
	def getUniqueTestCaseTitle(testCase: str) -> str:
		return f"{NotepadLib._testCaseTitle} ({abs(hash(testCase))}).txt"

	@staticmethod
	def getUniqueTestCaseTitleRegex(testCase: str) -> re.Pattern:
		return re.compile(f"^{NotepadLib._testCaseTitle} \\({abs(hash(testCase))}\\)")

	@staticmethod
	def _writeTestFile(testCase) -> str:
		"""
		Creates a file for a plaintext test case.
		@param testCase:  The plaintext sample that is to be tested.
		@return: path to the plaintext file.
		"""
		filePath = NotepadLib._getTestCasePath(NotepadLib.getUniqueTestCaseTitle(testCase))
		with open(file=filePath, mode='w', encoding='UTF-8') as f:
			f.write(testCase)
		return filePath

	def _focusNotepad(self, startsWithTestCaseTitle: re.Pattern):
		""" Ensure Notepad started and is focused.
		"""
		success, _success = _blockUntilConditionMet(
			getValue=lambda: SetForegroundWindow(startsWithTestCaseTitle, builtIn.log),
			giveUpAfterSeconds=3,
			intervalBetweenSeconds=0.5
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
			"Unable to focus Notepad.\n"
			f"{windowInformation}"
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
		path = self._writeTestFile(testCase)

		spy.wait_for_speech_to_finish()
		self.start_notepad(path)
		self._focusNotepad(NotepadLib.getUniqueTestCaseTitleRegex(testCase))
		# Move to the start of file
		spy.emulateKeyPress('home')
		spy.wait_for_speech_to_finish()
