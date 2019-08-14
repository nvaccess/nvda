# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides spy and robot library behaviour for NVDA system tests.
It is copied into the (system test specific) NVDA profile directory. It becomes the '__init__.py' file as part of a
package. This allows us to share utility methods between the global plugin and the nvdaRobotLib library.
"""
import globalPluginHandler
import threading
from .systemTestUtils import _blockUntilConditionMet
from logHandler import log
from time import clock as _timer

import sys
import os
log.debug("before pathmod: {}".format(sys.path))
# Get the path to the top of the package
TOP_DIR = os.path.abspath(os.path.dirname(__file__))
# imports that require libraries not distributed with an install of NVDA
sys.path.append( os.path.join(TOP_DIR, "libs"))
log.debug("after pathmod: {}".format(sys.path))
from robotremoteserver import RobotRemoteServer

whitespaceMinusSlashN = '\t\x0b\x0c\r '


class SystemTestSpy(object):
	SPEECH_HAS_FINISHED_SECONDS = 0.5

	def __init__(self):
		self._nvdaSpeech = [
			[""],  # initialise with an empty string, this allows for access via [-1]. This is equiv to no speech.
		]
		self._allSpeechStartIndex = 0
		self._speechOccurred = False
		self.isNvdaStartupComplete = False
		self.lastSpeechTime = _timer()
		self._registerWithExtensionPoints()

	def _registerWithExtensionPoints(self):
		from core import postNvdaStartup
		postNvdaStartup.register(self._onNvdaStartupComplete)

		from synthDrivers.speechSpy import post_speech
		post_speech.register(self._onNvdaSpeech)

	# callbacks for extension points
	def _onNvdaStartupComplete(self):
		self.isNvdaStartupComplete = True

	def _onNvdaSpeech(self, speechSequence=None):
		if not speechSequence: return
		with threading.Lock():
			self._speechOccurred = True
			self.lastSpeechTime = _timer()
			self._nvdaSpeech.append(speechSequence)

	# Private helper methods
	def _flattenCommandsSeparatingWithNewline(self, commandArray):
		f = [c for commands in commandArray for newlineJoined in [commands, [u"\n"]] for c in newlineJoined]
		return f

	def _getJoinedBaseStringsFromCommands(self, speechCommandArray):
		wsChars = whitespaceMinusSlashN
		baseStrings = [c.strip(wsChars) for c in speechCommandArray if isinstance(c, str)]
		return ''.join(baseStrings).strip()

	# Public methods
	def checkIfSpeechOccurredAndReset(self):
		# don't let _speechOccurred get updated and overwritten with False
		with threading.Lock():
			speechOccurred = self._speechOccurred
			self._speechOccurred = False
		return speechOccurred

	def getSpeechAtIndex(self, speechIndex):
		with threading.Lock():
			return self._getJoinedBaseStringsFromCommands(self._nvdaSpeech[speechIndex])

	def getSpeechSinceIndex(self, speechIndex):
		with threading.Lock():
			speechCommands = self._flattenCommandsSeparatingWithNewline(
				self._nvdaSpeech[speechIndex:]
			)
			joined = self._getJoinedBaseStringsFromCommands(speechCommands)
			return joined

	def getIndexOfLastSpeech(self):
		with threading.Lock():
			return len(self._nvdaSpeech) - 1

	def getIndexOfSpeech(self, speech, startFromIndex=0):
		with threading.Lock():
			for index, commands in enumerate(self._nvdaSpeech[startFromIndex:]):
				index = index + startFromIndex
				baseStrings = [c.strip() for c in commands if isinstance(c, str)]
				if any(speech in x for x in baseStrings):
					return index
			return -1

	def hasSpeechFinished(self):
		return self.SPEECH_HAS_FINISHED_SECONDS < _timer() - self.lastSpeechTime

	def dumpSpeechToLog(self):
		log.debug("All speech:\n{}".format(repr(self._nvdaSpeech)))

class NvdaSpyLib(object):
	_spy = None  # type: SystemTestSpy

	def __init__(self, systemTestSpy):
		self._spy = systemTestSpy
		self._allSpeechStartIndex = self._spy.getIndexOfLastSpeech()
		self._maxKeywordDuration=30

	def _minTimeout(self, timeout):
		"""Helper to get the minimum value, the timeout passed in, or self._maxKeywordDuration"""
		return min(timeout, self._maxKeywordDuration)

	# Start of Robot library API

	def set_max_keyword_duration(self, maxSeconds):
		"""This should only be called after importing the library, and should match the 'timeout' value given to the
		robot.libraries.Remote instance"""
		self._maxKeywordDuration = maxSeconds-1

	def wait_for_NVDA_startup_to_complete(self):
		_blockUntilConditionMet(
			getValue=lambda: self._spy.isNvdaStartupComplete,
			giveUpAfterSeconds=self._minTimeout(10),
			errorMessage="Unable to connect to nvdaSpy",
		)
		if self._spy.isNvdaStartupComplete:
			self.reset_all_speech_index()

	def get_last_speech(self):
		return self._spy.getSpeechAtIndex(-1)

	def get_all_speech(self):
		return self._spy.getSpeechSinceIndex(self._allSpeechStartIndex)

	def get_speech_from_index_until_now(self, speechIndex):
		return self._spy.getSpeechSinceIndex(speechIndex)

	def reset_all_speech_index(self):
		self._allSpeechStartIndex = self._spy.getIndexOfLastSpeech()
		return self._allSpeechStartIndex

	def get_last_speech_index(self):
		return self._spy.getIndexOfLastSpeech()

	def wait_for_specific_speech(self, speech, sinceIndex=None, maxWaitSeconds=5):
		sinceIndex = 0 if not sinceIndex else sinceIndex
		success, speechIndex = _blockUntilConditionMet(
			getValue=lambda: self._spy.getIndexOfSpeech(speech, sinceIndex),
			giveUpAfterSeconds=self._minTimeout(maxWaitSeconds),
			shouldStopEvaluator=lambda speechIndex: speechIndex >= 0,
			intervalBetweenSeconds=0.1,
			errorMessage=None
		)
		if not success:
			self._spy.dumpSpeechToLog()
			raise AssertionError(
				"Specific speech did not occur before timeout: {}\n"
				"See NVDA log for dump of all speech.".format(speech)
			)
		return speechIndex

	def wait_for_speech_to_finish(self, maxWaitSeconds=5.0):
		_blockUntilConditionMet(
			getValue=self._spy.hasSpeechFinished,
			giveUpAfterSeconds=self._minTimeout(maxWaitSeconds),
			errorMessage="Speech did not finish before timeout"
		)

class SystemTestSpyServer(object):
	def __init__(self):
		self._server = None

	def start(self):
		log.debug("TestSpyPlugin started")
		spy = SystemTestSpy()  # spies on NVDA
		server = self._server = RobotRemoteServer(
			NvdaSpyLib(spy),  # provides library behaviour
			port=8270,  # default:8270 is `registered by IANA` for remote server usage. Two ASCII values, RF.
			serve=False  # we want to start this serving on another thread so as not to block.
		)
		log.debug("Server address: {}".format(server.server_address))
		server_thread = threading.Thread(target=server.serve)
		server_thread.start()

	def stop(self):
		log.debug("Stop SystemTestSpyServer called")
		self._server.stop()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self._testSpy = SystemTestSpyServer()
		self._testSpy.start()

	def terminate(self):
		log.debug("Terminating the systemTestSpy")
		self._testSpy.stop()

	__gestures = {
	}