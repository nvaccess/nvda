# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" This module provides the ChromeLib Robot Framework Library which allows system tests to start
Google Chrome with a HTML sample and assert NVDA interacts with it in the expected way.
"""

# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from os.path import join as _pJoin
import os
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
	_mainChromeAlias = 'mainChromeWindow'
	_testFileStagingPath = _tempfile.mkdtemp()

	def __init__(self):
		self._original_chrome_log = os.environ.get('CHROME_LOG_FILE', None)
		self.chromeHandle: _Optional[int] = None
		self.chromeAlias: _Optional[str] = None

	@staticmethod
	def _getTestCasePath(filename):
		return _pJoin(ChromeLib._testFileStagingPath, filename)

	def exit_chrome(self, isMainChromeProcess: bool = False):
		spy = _NvdaLib.getSpyLib()
		spy.emulateKeyPress('control+w')
		chromeAlias = self._mainChromeAlias if isMainChromeProcess else self.chromeAlias
		process.wait_for_process(chromeAlias, timeout="1 minute", on_timeout="terminate")
		process.process_should_be_stopped(chromeAlias)
		if self._original_chrome_log is not None:
			os.environ['CHROME_LOG_FILE'] = self._original_chrome_log
		else:
			del os.environ['CHROME_LOG_FILE']

	def start_chrome(self, filePath: _Optional[str] = None):
		self.chromeAlias = self._mainChromeAlias if filePath is None else filePath
		builtIn.log(f"starting chrome: {self.chromeAlias}")
		os.environ['CHROME_LOG_FILE'] = _NvdaLib.NvdaLib.createLogsFullTestIdPath("chrome.log")
		self.chromeHandle = process.start_process(
			"start chrome"
			" --force-renderer-accessibility"
			" --suppress-message-center-popups"
			" --disable-notifications"
			" -kiosk"
			f' --enable-logging --v=1'
			f' {f"{filePath}" if filePath is not None else ""}',
			shell=True,
			alias=self.chromeAlias,
		)
		process.process_should_be_running(self.chromeHandle)
		return self.chromeHandle

	_testCaseTitle = "NVDA Browser Test Case"
	_beforeMarker = "Before Test Case Marker"
	_afterMarker = "After Test Case Marker"
	_loadCompleteString = "Test page load complete"

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
			<body onload="document.getElementById('loadStatus').innerHTML='{ChromeLib._loadCompleteString}'">
				<p>{ChromeLib._beforeMarker}</p>
				<p id="loadStatus">Loading...</p>
				{testCase}
				<p>{ChromeLib._afterMarker}</p>
			</body>
		""")
		with open(file=filePath, mode='w', encoding='UTF-8') as f:
			f.write(fileContents)
		return filePath

	def _wasStartMarkerSpoken(self, speech: str):
		if "document" not in speech:
			return False
		documentIndex = speech.index("document")
		marker = ChromeLib._beforeMarker
		return marker in speech and documentIndex < speech.index(marker)

	def _waitForStartMarker(self, spy, lastSpeechIndex):
		""" Wait until the page loads and NVDA reads the start marker.
		@param spy:
		@type spy: SystemTestSpy.speechSpyGlobalPlugin.NVDASpyLib
		@return: None
		"""
		for i in range(10):  # set a limit on the number of tries.
			builtIn.sleep("0.5 seconds")  # ensure application has time to receive input
			spy.wait_for_speech_to_finish()
			actualSpeech = spy.get_speech_at_index_until_now(lastSpeechIndex)
			if self._wasStartMarkerSpoken(actualSpeech):
				break
			lastSpeechIndex = spy.get_last_speech_index()
		else:  # Exceeded the number of tries
			spy.dump_speech_to_log()
			builtIn.fail(
				"Unable to locate 'before sample' marker."
				f" Too many attempts looking for '{ChromeLib._beforeMarker}'"
				" See NVDA log for full speech."
			)

	def prepareChrome(self, testCase: str) -> None:
		"""
		Starts Chrome opening a file containing the HTML sample
		@param testCase - The HTML sample to test.
		"""
		spy = _NvdaLib.getSpyLib()
		path = self._writeTestFile(testCase)

		spy.wait_for_speech_to_finish()
		lastSpeechIndex = spy.get_last_speech_index()
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
		appTitleIndex = spy.wait_for_specific_speech(applicationTitle, afterIndex=lastSpeechIndex)
		self._waitForStartMarker(spy, appTitleIndex)
		# Move to the loading status line, and wait fore it to become complete
		# the page has fully loaded.
		spy.emulateKeyPress('downArrow')
		for x in range(10):
			builtIn.sleep("0.1 seconds")
			actualSpeech = ChromeLib.getSpeechAfterKey('NVDA+UpArrow')
			if actualSpeech == self._loadCompleteString:
				break
			spy.emulateKeyPress('alt+shift+escape')  # switches to the previous open window
		else:  # Exceeded the number of tries
			spy.dump_speech_to_log()
			builtIn.fail(
				"Failed to wait for Test page load complete."
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
		spy.wait_for_speech_to_finish(speechStartedIndex=nextSpeechIndex)
		speech = spy.get_speech_at_index_until_now(nextSpeechIndex)
		return speech

	@staticmethod
	def getSpeechAfterTab() -> str:
		"""Ensure speech has stopped, press tab, and get speech until it stops.
		@return: The speech after tab.
		"""
		return ChromeLib.getSpeechAfterKey('tab')
