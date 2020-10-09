# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" This module provides the ChromeLib Robot Framework Library which allows system tests to start
Google Chrome with a HTML sample and assert NVDA interacts with it in the expected way.
"""

# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from os.path import join as _pJoin
import tempfile as _tempfile
from typing import Optional as _Optional
from SystemTestSpy import (
	_getLib,
)
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
class ChromeLib:
	_testFileStagingPath = _tempfile.mkdtemp()

	def __init__(self):
		self.chromeHandle: _Optional[int] = None

	@staticmethod
	def _getTestCasePath(filename):
		return _pJoin(ChromeLib._testFileStagingPath, filename)

	def start_chrome(self, filePath):
		builtIn.log(f"starting chrome: {filePath}")
		self.chromeHandle = process.start_process(
			"start chrome"
			" --force-renderer-accessibility"
			" --suppress-message-center-popups"
			" --disable-notifications"
			f' "{filePath}"',
			shell=True,
			alias='chromeAlias',
		)
		process.process_should_be_running(self.chromeHandle)
		return self.chromeHandle

	_testCaseTitle = "NVDA Browser Test Case"
	_beforeMarker = "Before Test Case Marker"
	_afterMarker = "After Test Case Marker"

	@staticmethod
	def _writeTestFile(testCase) -> str:
		"""
		Creates a file for a HTML test case. The sample is written with a button before and after so that NVDA
		can tab to the sample from either direction.
		@param testCase:  The HTML sample that is to be tested.
		@return: path to the HTML file.
		"""
		filePath = ChromeLib._getTestCasePath("test.html")
		fileContents = (f"""
			<head>
				<title>{ChromeLib._testCaseTitle}</title>
			</head>
			<body>
				<p>{ChromeLib._beforeMarker}</p>
				{testCase}
				<p>{ChromeLib._afterMarker}</p>
			</body>
		""")
		with open(file=filePath, mode='w', encoding='UTF-8') as f:
			f.write(fileContents)
		return filePath

	def prepareChrome(self, testCase: str) -> None:
		"""
		Starts Chrome opening a file containing the HTML sample
		@param testCase - The HTML sample to test.
		"""
		spy = _NvdaLib.getSpyLib()
		path = self._writeTestFile(testCase)
		self.start_chrome(path)
		# Ensure chrome started
		# Different versions of chrome have variations in how the title is presented
		# This may mean that there is a separator between document name and
		# application name. E.G. "htmlTest   Google Chrome", "html – Google Chrome" or perhaps no applcation
		# name at all.
		# Rather than try to get this right, just wait for the doc title.
		# If this continues to be unreliable we could use solenium or similar to start chrome and inform us when
		# it is ready.
		applicationTitle = f"{self._testCaseTitle}"
		spy.wait_for_specific_speech(applicationTitle)
		# Read all is configured, but just test interacting with the sample.
		spy.wait_for_speech_to_finish()

		# move to start marker
		for i in range(10):  # set a limit on the number of tries.
			# Small changes in Chrome mean the number of tab presses to get into the document can vary.
			builtIn.sleep("0.5 seconds")  # ensure application has time to receive input
			actualSpeech = self.getSpeechAfterKey('f6')
			if ChromeLib._beforeMarker in actualSpeech:
				break
		else:  # Exceeded the number of tries
			spy.dump_speech_to_log()
			builtIn.fail(
				"Unable to tab to 'before sample' marker."
				f" Too many attempts looking for '{ChromeLib._beforeMarker}'"
				" See NVDA log for full speech."
			)

	@staticmethod
	def getSpeechAfterKey(key) -> str:
		"""Ensure speech has stopped, press key, and get speech until it stops.
		@return: The speech after key press.
		"""
		spy = _NvdaLib.getSpyLib()
		spy.wait_for_speech_to_finish()
		nextSpeechIndex = spy.get_next_speech_index()
		spy.emulateKeyPress(key)
		speech = spy.get_speech_at_index_until_now(nextSpeechIndex)
		return speech

	@staticmethod
	def getSpeechAfterTab() -> str:
		"""Ensure speech has stopped, press tab, and get speech until it stops.
		@return: The speech after tab.
		"""
		return ChromeLib.getSpeechAfterKey('tab')
