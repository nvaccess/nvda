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
from KeyInputLib import KeyInputLib as _KeyInputLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

builtIn: BuiltIn = BuiltIn()
opSys: _OpSysLib = _getLib('OperatingSystem')
process: _ProcessLib = _getLib('Process')
keyInputLib: _KeyInputLib = _getLib('KeyInputLib')
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
			f"start chrome \"{filePath}\"",
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
				<button>{ChromeLib._beforeMarker}</button>
				{testCase}
				<button>{ChromeLib._afterMarker}</button>
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
		applicationTitle = f"{self._testCaseTitle}"
		spy.wait_for_specific_speech(applicationTitle)
		# Different versions of chrome have small variations in the separator between document name and
		# application name. E.G. "htmlTest   Google Chrome", "html – Google Chrome"
		# Rather than try to get the separator right, wait for the doc title, then wait for the 'Google Chrome'
		# part. Note: this also works with "Chrome Canary"
		spy.wait_for_specific_speech("Google Chrome")
		# Read all is configured, but just test interacting with the sample.
		spy.wait_for_speech_to_finish()

		# move to start marker
		for i in range(10):  # set a limit on the number of tries.
			# Small changes in Chrome mean the number of tab presses to get into the document can vary.
			builtIn.sleep(0.5)  # ensure application has time to receive input
			actualSpeech = self.getSpeechAfterTab()
			if actualSpeech == f"{ChromeLib._beforeMarker}  button":
				break
			if actualSpeech == f"{ChromeLib._afterMarker}  button":
				# somehow missed the start marker!
				builtIn.fail(
					"Unable to tab to 'before sample' marker, reached 'after sample' marker first."
					f" Looking for '{ChromeLib._beforeMarker}  button'"
					" See NVDA log for full speech."
				)
				spy.dump_speech_to_log()
		else:  # Exceeded the number of tries
			builtIn.fail(
				"Unable to tab to 'before sample' marker."
				f" Too many attempts looking for '{ChromeLib._beforeMarker}  button'"
				" See NVDA log for full speech."
			)
			spy.dump_speech_to_log()

	@staticmethod
	def getSpeechAfterTab() -> str:
		"""Press tab, and get speech until it stops.
		@return: The speech after tab.
		"""
		spy = _NvdaLib.getSpyLib()
		spy.wait_for_speech_to_finish()
		nextSpeechIndex = spy.get_next_speech_index()
		keyInputLib.send('\t')
		spy.wait_for_speech_to_finish()
		speech = spy.get_speech_at_index_until_now(nextSpeechIndex)
		return speech
