# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides an NVDA global plugin which creates a and robot library remote server.
It allows tests to get information out of NVDA.
It is copied into the (system test specific) NVDA profile directory. It becomes the '__init__.py' file as part
of a package.
"""
import typing
from typing import Optional

import globalPluginHandler
import threading
from .blockUntilConditionMet import _blockUntilConditionMet
from logHandler import log
from time import perf_counter as _timer

import sys
import os


def _importRobotRemoteServer() -> typing.Type:
	log.debug(f"before path mod: {sys.path}")
	# Get the path to the top of the package
	TOP_DIR = os.path.abspath(os.path.dirname(__file__))
	# imports that require libraries not distributed with an install of NVDA
	sys.path.append(os.path.join(TOP_DIR, "libs"))
	log.debug(f"after path mod: {sys.path}")
	from robotremoteserver import RobotRemoteServer
	return RobotRemoteServer


class NVDASpyLib:
	""" Robot Framework Library to spy on NVDA during system tests.
	Used to determine if NVDA has finished starting, and various ways of getting speech output.
	All public methods are part of the Robot Library
	"""
	SPEECH_HAS_FINISHED_SECONDS: float = 0.5

	def __init__(self):
		# speech cache is ordered temporally, oldest at low indexes, most recent at highest index.
		self._nvdaSpeech_requiresLock = [  # requires thread locking before read/write
			[""],  # initialise with an empty string, this allows for access via [-1]. This is equiv to no speech.
		]
		self._speechOccurred_requiresLock = False  # requires thread locking before read/write
		self._lastSpeechTime_requiresLock = _timer()
		self._isNvdaStartupComplete = False
		self._allSpeechStartIndex = self.get_last_speech_index()
		self._maxKeywordDuration = 30
		self._registerWithExtensionPoints()

	def _registerWithExtensionPoints(self):
		from core import postNvdaStartup
		postNvdaStartup.register(self._onNvdaStartupComplete)

		# This file (`speechSpyGlobalPlugin.py`) is moved to
		# "scratchpad/globalPlugins/speechSpyGlobalPlugin/__init__.py"
		# Import path must be valid after `speechSpySynthDriver.py` is moved to "scratchpad/synthDrivers/"
		from synthDrivers.speechSpySynthDriver import post_speech
		post_speech.register(self._onNvdaSpeech)

	# callbacks for extension points
	def _onNvdaStartupComplete(self):
		self._isNvdaStartupComplete = True

	def _onNvdaSpeech(self, speechSequence=None):
		if not speechSequence:
			return
		with threading.Lock():
			self._speechOccurred_requiresLock = True
			self._lastSpeechTime_requiresLock = _timer()
			self._nvdaSpeech_requiresLock.append(speechSequence)

	@staticmethod
	def _flattenCommandsSeparatingWithNewline(commandArray):
		"""
		Flatten many collections of speech sequences into a single speech sequence. Each original speech sequence
		is separated by a newline string.
		@param commandArray: is a collection of speechSequences
		@return: speechSequence
		"""
		f = [c for commands in commandArray for newlineJoined in [commands, [u"\n"]] for c in newlineJoined]
		return f

	@staticmethod
	def _getJoinedBaseStringsFromCommands(speechCommandArray) -> str:
		baseStrings = [c for c in speechCommandArray if isinstance(c, str)]
		return ''.join(baseStrings).strip()

	def _getSpeechAtIndex(self, speechIndex):
		with threading.Lock():
			return self._getJoinedBaseStringsFromCommands(self._nvdaSpeech_requiresLock[speechIndex])

	def get_speech_at_index_until_now(self, speechIndex: int) -> str:
		""" All speech from (and including) the index until now.
		@param speechIndex:
		@return: The speech joined together, see L{_getJoinedBaseStringsFromCommands}
		"""
		with threading.Lock():
			speechCommands = self._flattenCommandsSeparatingWithNewline(
				self._nvdaSpeech_requiresLock[speechIndex:]
			)
			joined = self._getJoinedBaseStringsFromCommands(speechCommands)
			return joined

	def get_last_speech_index(self) -> int:
		with threading.Lock():
			return len(self._nvdaSpeech_requiresLock) - 1

	def _getIndexOfSpeech(self, speech, searchAfterIndex: Optional[int] = None):
		if searchAfterIndex is None:
			firstIndexToCheck = 0
		else:
			firstIndexToCheck = 1 + searchAfterIndex
		with threading.Lock():
			for index, commands in enumerate(self._nvdaSpeech_requiresLock[firstIndexToCheck:]):
				index = index + firstIndexToCheck
				baseStrings = [c.strip() for c in commands if isinstance(c, str)]
				if any(speech in x for x in baseStrings):
					return index
			return -1

	def _hasSpeechFinished(self):
		with threading.Lock():
			return self.SPEECH_HAS_FINISHED_SECONDS < _timer() - self._lastSpeechTime_requiresLock

	def _devInfoToLog(self):
		import api
		obj = api.getNavigatorObject()
		if hasattr(obj, "devInfo"):
			log.info("Developer info for navigator object:\n%s" % "\n".join(obj.devInfo))
		else:
			log.info("No developer info for navigator object")

	def dump_speech_to_log(self):
		log.debug("dump_speech_to_log.")
		with threading.Lock():
			try:
				self._devInfoToLog()
			except Exception:
				log.error("Unable to log dev info")
			try:
				log.debug(f"All speech:\n{repr(self._nvdaSpeech_requiresLock)}")
			except Exception:
				log.error("Unable to log speech")

	def _minTimeout(self, timeout: float) -> float:
		"""Helper to get the minimum value, the timeout passed in, or self._maxKeywordDuration"""
		return min(timeout, self._maxKeywordDuration)

	def init_max_keyword_duration(self, maxSeconds: float):
		"""This should only be called once, immediately after importing the library.
		@param maxSeconds: Should match the 'timeout' value given to the `robot.libraries.Remote` instance. If
		this value is greater than the value for the `robot.libraries.Remote` instance it may mean that the test
		is failed, and NVDA is never exited, requiring manual intervention.
		Should be set to a large value like '30' (seconds).
		"""
		self._maxKeywordDuration = maxSeconds - 1

	def wait_for_NVDA_startup_to_complete(self):
		_blockUntilConditionMet(
			getValue=lambda: self._isNvdaStartupComplete,
			giveUpAfterSeconds=self._minTimeout(10),
			errorMessage="Unable to connect to nvdaSpy",
		)
		if self._isNvdaStartupComplete:
			self.reset_all_speech_index()

	def get_last_speech(self) -> str:
		return self._getSpeechAtIndex(-1)

	def get_all_speech(self) -> str:
		return self.get_speech_at_index_until_now(self._allSpeechStartIndex)

	def reset_all_speech_index(self) -> int:
		self._allSpeechStartIndex = self.get_last_speech_index()
		return self._allSpeechStartIndex

	def get_next_speech_index(self) -> int:
		""" @return: the next index that will be used.
		"""
		return self.get_last_speech_index() + 1

	def wait_for_specific_speech(
			self,
			speech: str,
			afterIndex: Optional[int] = None,
			maxWaitSeconds: int = 5,
	) -> int:
		"""
		@param speech: The speech to expect.
		@param afterIndex: The speech should come after this index. The index is exclusive.
		@param maxWaitSeconds: The amount of time to wait in seconds.
		@return: the index of the speech.
		"""
		success, speechIndex = _blockUntilConditionMet(
			getValue=lambda: self._getIndexOfSpeech(speech, afterIndex),
			giveUpAfterSeconds=self._minTimeout(maxWaitSeconds),
			shouldStopEvaluator=lambda indexFound: indexFound >= (afterIndex if afterIndex else 0),
			intervalBetweenSeconds=0.1,
			errorMessage=None
		)
		if not success:
			self.dump_speech_to_log()
			raise AssertionError(
				"Specific speech did not occur before timeout: {}\n"
				"See NVDA log for dump of all speech.".format(speech)
			)
		return speechIndex

	def wait_for_speech_to_finish(self, maxWaitSeconds=5.0):
		_blockUntilConditionMet(
			getValue=self._hasSpeechFinished,
			giveUpAfterSeconds=self._minTimeout(maxWaitSeconds),
			errorMessage="Speech did not finish before timeout"
		)


class SystemTestSpyServer(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		self._server = None
		self._start()

	def _start(self):
		log.debug("SystemTestSpyServer started")
		spyLibrary = NVDASpyLib()  # spies on NVDA
		RobotRemoteServer = _importRobotRemoteServer()
		server = self._server = RobotRemoteServer(
			spyLibrary,  # provides library behaviour
			port=8270,  # default:8270 is `registered by IANA` for remote server usage. Two ASCII values, RF.
			serve=False  # we want to start this serving on another thread so as not to block.
		)
		log.debug("Server address: {}".format(server.server_address))
		server_thread = threading.Thread(target=server.serve)
		server_thread.start()

	def terminate(self):
		log.debug("Terminating the SystemTestSpyServer")
		self._server.stop()


GlobalPlugin = SystemTestSpyServer
GlobalPlugin.__gestures = {
}
