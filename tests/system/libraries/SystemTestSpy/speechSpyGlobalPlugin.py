# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides an NVDA global plugin which creates a and robot library remote server.
It allows tests to get information out of NVDA.
It is copied into the (system test specific) NVDA profile directory. It becomes the '__init__.py' file as part
of a package.
"""
import gettext
import typing
from typing import Optional

import extensionPoints
import globalPluginHandler
import threading
from .blockUntilConditionMet import _blockUntilConditionMet
from logHandler import log
from time import perf_counter as _timer
from keyboardHandler import KeyboardInputGesture
import inputCore
import queueHandler
import watchdog

import ctypes
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


class BrailleViewerSpy:
	postBrailleUpdate = extensionPoints.Action()

	def __init__(self):
		self._last = ""

	def updateBrailleDisplayed(
			self,
			cells,  # ignored
			rawText,
			currentCellCount,  # ignored
	):
		rawText = rawText.strip()
		if rawText and rawText != self._last:
			self._last = rawText
			self.postBrailleUpdate.notify(rawText=rawText)

	isDestroyed: bool = False

	def saveInfoAndDestroy(self):
		if not self.isDestroyed:
			self.isDestroyed = True
			import brailleViewer
			brailleViewer._onGuiDestroyed()


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
		self._lastSpeechTime_requiresLock = _timer()
		#: Lock to protect members that are written to in _onNvdaSpeech.
		self._speechLock = threading.RLock()

		# braille raw text (not dots) cache is ordered temporally,
		# oldest at low indexes, most recent at highest index.
		self._nvdaBraille_requiresLock = [  # requires thread locking before read/write
			"",  # initialise with an empty string, this allows for access via [-1]. This is equiv to no braille.
		]
		#: Lock to protect members that are written to in _onNvdaBraille.
		self._brailleLock = threading.RLock()

		self._isNvdaStartupComplete = False
		self._allSpeechStartIndex = self.get_last_speech_index()
		self._allBrailleStartIndex = self.get_last_braille_index()
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

		self._brailleSpy = BrailleViewerSpy()
		self._brailleSpy.postBrailleUpdate.register(self._onNvdaBraille)

	def set_configValue(self, keyPath: typing.List[str], val: typing.Union[str, bool, int]):
		import config
		if not keyPath or len(keyPath) < 1:
			raise ValueError("Key path not provided")
		penultimateConf = config.conf
		for key in keyPath[:-1]:
			penultimateConf = penultimateConf[key]
		ultimateKey = keyPath[-1]
		penultimateConf[ultimateKey] = val

	fakeTranslations: typing.Optional[gettext.NullTranslations] = None

	def override_translationString(self, invariantString: str, replacementString: str):
		import languageHandler
		if not self.fakeTranslations:
			class Translation_Fake(gettext.NullTranslations):
				originalTranslationFunction: Optional
				translationResults: typing.Dict[str, str]

				def __init__(
						self,
						originalTranslationFunction: Optional
				):
					self.originalTranslationFunction = originalTranslationFunction
					self.translationResults = {}
					super().__init__()
					self.install()

				def gettext(self, msg: str) -> str:
					if msg in self.translationResults:
						return self.translationResults[msg]
					if self.originalTranslationFunction:
						return self.originalTranslationFunction.gettext(msg)
					return msg

				def restore(self) -> None:
					self.translationResults.clear()
					if self.originalTranslationFunction:
						self.originalTranslationFunction.install()

			self.fakeTranslations = Translation_Fake(
				languageHandler.installedTranslation() if languageHandler.installedTranslation else None
			)
		self.fakeTranslations.translationResults[invariantString] = replacementString

	def queueNVDAMainThreadCrash(self):
		from queueHandler import queueFunction, eventQueue
		queueFunction(eventQueue, _crashNVDA)

	def queueNVDABrailleThreadCrash(self):
		from braille import _BgThread
		_BgThread.queueApc(ctypes.windll.Kernel32.DebugBreak)

	def queueNVDAUIAHandlerThreadCrash(self):
		from UIAHandler import handler
		handler.MTAThreadQueue.put(_crashNVDA)

	# callbacks for extension points
	def _onNvdaStartupComplete(self):
		self._isNvdaStartupComplete = True
		import brailleViewer
		brailleViewer._brailleGui = self._brailleSpy
		self.setBrailleCellCount(120)
		brailleViewer.postBrailleViewerToolToggledAction.notify(created=True)

	def _onNvdaBraille(self, rawText: str):
		if not rawText:
			return
		if not isinstance(rawText, str):
			raise TypeError(f"rawText expected as str, got: {type(rawText)}, {rawText!r}")
		with self._brailleLock:
			self._nvdaBraille_requiresLock.append(rawText)

	def _onNvdaSpeech(self, speechSequence=None):
		if not speechSequence:
			return
		with self._speechLock:
			self._lastSpeechTime_requiresLock = _timer()
			self._nvdaSpeech_requiresLock.append(speechSequence)

	@staticmethod
	def _getJoinedBaseStringsFromCommands(speechCommandArray) -> str:
		baseStrings = [c for c in speechCommandArray if isinstance(c, str)]
		return ''.join(baseStrings).strip()

	def _getSpeechAtIndex(self, speechIndex):
		with self._speechLock:
			return self._getJoinedBaseStringsFromCommands(self._nvdaSpeech_requiresLock[speechIndex])

	def get_speech_at_index_until_now(self, speechIndex: int) -> str:
		""" All speech from (and including) the index until now.
		@param speechIndex:
		@return: The speech joined together, see L{_getJoinedBaseStringsFromCommands}
		"""
		with self._speechLock:
			speechCommands = [
				self._getJoinedBaseStringsFromCommands(x) for x in self._nvdaSpeech_requiresLock[speechIndex:]
			]
			return "\n".join(x for x in speechCommands if x and not x.isspace())

	def get_last_speech_index(self) -> int:
		with self._speechLock:
			return len(self._nvdaSpeech_requiresLock) - 1

	def _getIndexOfSpeech(self, speech, searchAfterIndex: Optional[int] = None):
		if searchAfterIndex is None:
			firstIndexToCheck = 0
		else:
			firstIndexToCheck = 1 + searchAfterIndex
		with self._speechLock:
			for index, commands in enumerate(self._nvdaSpeech_requiresLock[firstIndexToCheck:]):
				index = index + firstIndexToCheck
				baseStrings = [c.strip() for c in commands if isinstance(c, str)]
				if any(speech in x for x in baseStrings):
					return index
			return -1

	def _hasSpeechFinished(self, speechStartedIndex: Optional[int] = None):
		with self._speechLock:
			started = speechStartedIndex is None or speechStartedIndex < self.get_next_speech_index()
			finished = self.SPEECH_HAS_FINISHED_SECONDS < _timer() - self._lastSpeechTime_requiresLock
			return started and finished

	def setBrailleCellCount(self, brailleCellCount: int):
		import brailleViewer
		brailleViewer.DEFAULT_NUM_CELLS = brailleCellCount

	def _getBrailleAtIndex(self, brailleIndex: int) -> str:
		with self._brailleLock:
			return self._nvdaBraille_requiresLock[brailleIndex]

	def get_braille_at_index_until_now(self, brailleIndex: int) -> str:
		""" All raw braille text from (and including) the index until now.
		@param brailleIndex:
		@return: The raw text, each update on a new line
		"""
		with self._brailleLock:
			rangeOfInterest = self._nvdaBraille_requiresLock[brailleIndex:]
			return "\n".join(rangeOfInterest)

	def get_last_braille_index(self) -> int:
		with self._brailleLock:
			return len(self._nvdaBraille_requiresLock) - 1

	def _devInfoToLog(self):
		import api
		obj = api.getNavigatorObject()
		if hasattr(obj, "devInfo"):
			log.info("Developer info for navigator object:\n%s" % "\n".join(obj.devInfo))
		else:
			log.info("No developer info for navigator object")

	def dump_speech_to_log(self):
		log.debug("dump_speech_to_log.")
		with self._speechLock:
			try:
				self._devInfoToLog()
			except Exception:
				log.error("Unable to log dev info")
			try:
				log.debug(f"All speech:\n{repr(self._nvdaSpeech_requiresLock)}")
			except Exception:
				log.error("Unable to log speech")

	def dump_braille_to_log(self):
		log.debug("dump_braille_to_log.")
		with self._brailleLock:
			try:
				log.debug(f"All braille:\n{repr(self._nvdaBraille_requiresLock)}")
			except Exception:
				log.error("Unable to log braille")

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

	def wait_for_speech_to_finish(
			self,
			maxWaitSeconds=5.0,
			speechStartedIndex: Optional[int] = None
	):
		_blockUntilConditionMet(
			getValue=lambda: self._hasSpeechFinished(speechStartedIndex=speechStartedIndex),
			giveUpAfterSeconds=self._minTimeout(maxWaitSeconds),
			errorMessage="Speech did not finish before timeout"
		)

	def wait_for_braille_update(
			self,
			nextBrailleIndex: int,
			maxWaitSeconds=5.0,
	):
		"""Wait until there is at least a single update.
		@note there may be subsequent braille updates. This method does not confirm updates are finished.
		"""
		_blockUntilConditionMet(
			getValue=lambda: self.get_last_braille_index() == nextBrailleIndex,
			giveUpAfterSeconds=self._minTimeout(maxWaitSeconds),
			errorMessage=None
		)

	def get_last_braille(self) -> str:
		return self._getBrailleAtIndex(-1)

	def get_next_braille_index(self) -> int:
		""" @return: the next index that will be used.
		"""
		return self.get_last_braille_index() + 1

	def emulateKeyPress(self, kbIdentifier: str, blockUntilProcessed=True):
		"""
		Emulates a key press using NVDA's input gesture framework.
		The key press will either result in a script being executed, or the key being sent on to the OS.
		By default this method will block until any script resulting from this key has been executed,
		and the NVDA core has again gone back to sleep.
		@param kbIdentifier: an NVDA keyboard gesture identifier.
		0 or more modifier keys followed by a main key, all separated by a plus (+) symbol.
		E.g. control+shift+downArrow.
		See vkCodes.py in the NVDA source directory for valid key names.
		"""
		gesture = KeyboardInputGesture.fromName(kbIdentifier)
		inputCore.manager.emulateGesture(gesture)
		if blockUntilProcessed:
			# Emulating may have queued a script or events.
			# Insert our own function into the queue after, and wait for that to be also executed.
			queueProcessed = set()

			def _setQueueProcessed():
				nonlocal queueProcessed
				queueProcessed = True

			queueHandler.queueFunction(queueHandler.eventQueue, _setQueueProcessed)
			_blockUntilConditionMet(
				getValue=lambda: queueProcessed,
				giveUpAfterSeconds=self._minTimeout(5),
				errorMessage="Timed out waiting for key to be processed",
			)
			# We know that by now the core will have woken up and processed the scripts, events and our own function.
			# Wait for the core to go to sleep,
			# Which means there is no more things the core is currently processing.
			_blockUntilConditionMet(
				getValue=lambda: watchdog.isCoreAsleep(),
				giveUpAfterSeconds=self._minTimeout(5),
				errorMessage="Timed out waiting for core to sleep again",
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
		server_thread = threading.Thread(target=server.serve, name="RF Test Spy Thread")
		server_thread.start()

	def terminate(self):
		log.debug("Terminating the SystemTestSpyServer")
		self._server.stop()


def _crashNVDA():
	ctypes.windll.Kernel32.DebugBreak()


GlobalPlugin = SystemTestSpyServer
GlobalPlugin.__gestures = {
}
