# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Babbage B.V., Bill Dengler,
# Julien Cochuyt

from abc import ABCMeta, abstractmethod
from enum import IntEnum
from typing import Callable, TYPE_CHECKING, Optional
import weakref
import garbageHandler
from logHandler import log
import config
import controlTypes
import api
import textInfos
import queueHandler
import winKernel
from utils.security import objectBelowLockScreenAndWindowsIsLocked

from .commands import CallbackCommand, EndUtteranceCommand
from .speechWithoutPauses import SpeechWithoutPauses

from .types import (
	SpeechSequence,
	_flattenNestedSequences,
)

if TYPE_CHECKING:
	import NVDAObjects
	from .speech import (
		getTextInfoSpeech,
		SpeakTextInfoState,
		speakObject,
	)


class CURSOR(IntEnum):
	CARET = 0
	REVIEW = 1
	TABLE = 2


SayAllHandler = None


def initialize(
		speakFunc: Callable[[SpeechSequence], None],
		speakObject: 'speakObject',
		getTextInfoSpeech: 'getTextInfoSpeech',
		SpeakTextInfoState: 'SpeakTextInfoState',
):
	log.debug("Initializing sayAllHandler")
	global SayAllHandler
	SayAllHandler = _SayAllHandler(
		SpeechWithoutPauses(speakFunc=speakFunc),
		speakObject,
		getTextInfoSpeech,
		SpeakTextInfoState,
	)


class _SayAllHandler:
	def __init__(
			self,
			speechWithoutPausesInstance: SpeechWithoutPauses,
			speakObject: 'speakObject',
			getTextInfoSpeech: 'getTextInfoSpeech',
			SpeakTextInfoState: 'SpeakTextInfoState',
	):
		self.lastSayAllMode = None
		self.speechWithoutPausesInstance = speechWithoutPausesInstance
		#: The active say all manager.
		#: This is a weakref because the manager should be allowed to die once say all is complete.
		self._getActiveSayAll = lambda: None  # noqa: Return None when called like a dead weakref.
		self._speakObject = speakObject
		self._getTextInfoSpeech = getTextInfoSpeech
		self._makeSpeakTextInfoState = SpeakTextInfoState

	def stop(self):
		'''
		Stops any active objects reader and resets the SayAllHandler's SpeechWithoutPauses instance
		'''
		active = self._getActiveSayAll()
		if active:
			active.stop()
		self.speechWithoutPausesInstance.reset()

	def isRunning(self):
		"""Determine whether say all is currently running.
		@return: C{True} if say all is currently running, C{False} if not.
		@rtype: bool
		"""
		return bool(self._getActiveSayAll())

	def readObjects(self, obj: 'NVDAObjects.NVDAObject'):
		reader = _ObjectsReader(self, obj)
		self._getActiveSayAll = weakref.ref(reader)
		reader.next()

	def readText(
			self,
			cursor: CURSOR,
			startPos: Optional[textInfos.TextInfo] = None,
			nextLineFunc: Optional[Callable[[textInfos.TextInfo], textInfos.TextInfo]] = None,
			shouldUpdateCaret: bool = True,
	) -> None:
		self.lastSayAllMode = cursor
		try:
			if cursor == CURSOR.CARET:
				reader = _CaretTextReader(self)
			elif cursor == CURSOR.REVIEW:
				reader = _ReviewTextReader(self)
			elif cursor == CURSOR.TABLE:
				reader = _TableTextReader(self, startPos, nextLineFunc, shouldUpdateCaret)
			else:
				raise RuntimeError(f"Unknown cursor {cursor}")
		except NotImplementedError:
			log.debugWarning("Unable to make reader", exc_info=True)
			return
		self._getActiveSayAll = weakref.ref(reader)
		reader.nextLine()


class _ObjectsReader(garbageHandler.TrackedObject):

	def __init__(self, handler: _SayAllHandler, root: 'NVDAObjects.NVDAObject'):
		self.handler = handler
		self.walker = self.walk(root)
		self.prevObj = None

	def walk(self, obj: 'NVDAObjects.NVDAObject'):
		yield obj
		child=obj.simpleFirstChild
		while child:
			for descendant in self.walk(child):
				yield descendant
			child=child.simpleNext

	def next(self):
		if not self.walker:
			# We were stopped.
			return
		if self.prevObj:
			# We just started speaking this object, so move the navigator to it.
			if not api.setNavigatorObject(
				self.prevObj,
				isFocus=self.handler.lastSayAllMode == CURSOR.CARET
			):
				return
			winKernel.SetThreadExecutionState(winKernel.ES_SYSTEM_REQUIRED)
		# Move onto the next object.
		self.prevObj = obj = next(self.walker, None)
		if not obj:
			return
		# Call this method again when we start speaking this object.
		callbackCommand = CallbackCommand(self.next, name="say-all:next")
		SayAllHandler._speakObject(
			obj,
			reason=controlTypes.OutputReason.SAYALL,
			_prefixSpeechCommand=callbackCommand
		)

	def stop(self):
		self.walker = None


class _TextReader(garbageHandler.TrackedObject, metaclass=ABCMeta):
	"""Manages continuous reading of text.
	This is intended for internal use only.

	The high level flow of control is as follows:
	1. The constructor sets things up.
	2. L{nextLine} is called to read the first line.
	3. When it speaks a line, L{nextLine} request that L{lineReached} be called
		when we start speaking this line, providing the position and state at this point.
	4. When we start speaking a line, L{lineReached} is called
		and moves the cursor to that line.
	5. L{lineReached} calls L{nextLine}.
	6. If there are more lines, L{nextLine} works as per steps 3 and 4.
	7. Otherwise, if the object doesn't support page turns, we're finished.
	8. If the object does support page turns,
		we request that L{turnPage} be called when speech is finished.
	9. L{turnPage} tries to turn the page.
	10. If there are no more pages, we're finished.
	11. If there is another page, L{turnPage} calls L{nextLine}.
	"""
	MAX_BUFFERED_LINES = 10

	def __init__(self, handler: _SayAllHandler):
		self.reader = None
		self.handler = handler
		self.trigger = SayAllProfileTrigger()
		self.reader = self.getInitialTextInfo()
		# #10899: SayAll profile can't be activated earlier because they may not be anything to read
		self.trigger.enter()
		self.speakTextInfoState = SayAllHandler._makeSpeakTextInfoState(self.reader.obj)
		self.numBufferedLines = 0
		self.initialIteration = True

	@abstractmethod
	def getInitialTextInfo(self) -> textInfos.TextInfo:
		...

	@abstractmethod
	def updateCaret(self, updater: textInfos.TextInfo) -> None:
		...

	def shouldReadInitialPosition(self) -> bool:
		return False

	def nextLineImpl(self) -> bool:
		"""
		Advances cursor to the next reading chunk (e.g. paragraph).
		@return: C{True} if advanced successfully, C{False} otherwise.
		"""
		# Expand to the current line.
		# We use move end rather than expand
		# because the user might start in the middle of a line
		# and we don't want to read from the start of the line in that case.
		# For lines after the first, it's also more efficient because
		# we're already at the start of the line, so there's no need to search backwards.
		delta = self.reader.move(textInfos.UNIT_READINGCHUNK, 1, endPoint="end")
		if delta <= 0:
			# No more text.
			if isinstance(self.reader.obj, textInfos.DocumentWithPageTurns):
				# Once the last line finishes reading, try turning the page.
				cb = CallbackCommand(self.turnPage, name="say-all:turnPage")
				self.handler.speechWithoutPausesInstance.speakWithoutPauses([cb, EndUtteranceCommand()])
			else:
				self.finish()
			return False
		return True

	def collapseLineImpl(self) -> bool:
		"""
		Collapses to the end of this line, ready to read the next.
		@return: C{True} if collapsed successfully, C{False} otherwise.
		"""
		try:
			self.reader.collapse(end=True)
			return True
		except RuntimeError:
			# This occurs in Microsoft Word when the range covers the end of the document.
			# without this exception to indicate that further collapsing is not possible,
			# say all could enter an infinite loop.
			self.finish()
			return False

	def nextLine(self):
		if not self.reader:
			log.debug("no self.reader")
			# We were stopped.
			return

		if (
			# The object died, so we should too.
			not self.reader.obj
			# SayAll is available on the lock screen via getSafeScripts, as such
			# ensure the say all reader does not contain secure information
			# before continuing
			or objectBelowLockScreenAndWindowsIsLocked(self.reader.obj)
		):
			log.debug("no self.reader.obj")
			self.finish()
			return

		if not self.initialIteration or not self.shouldReadInitialPosition():
			if not self.nextLineImpl():
				return
		self.initialIteration = False
		bookmark = self.reader.bookmark
		# Copy the speakTextInfoState so that speak callbackCommand
		# and its associated callback are using a copy isolated to this specific line.
		state = self.speakTextInfoState.copy()
		# Call lineReached when we start speaking this line.
		# lineReached will move the cursor and trigger reading of the next line.

		def _onLineReached(obj=self.reader.obj, state=state):
			self.lineReached(obj, bookmark, state)

		cb = CallbackCommand(
			_onLineReached,
			name="say-all:lineReached"
		)

		# Generate the speech sequence for the reader textInfo
		# and insert the lineReached callback at the very beginning of the sequence.
		# _linePrefix on speakTextInfo cannot be used here
		# As it would be inserted in the sequence after all initial control starts which is too late.
		speechGen = SayAllHandler._getTextInfoSpeech(
			self.reader,
			unit=textInfos.UNIT_READINGCHUNK,
			reason=controlTypes.OutputReason.SAYALL,
			useCache=state
		)
		seq = list(_flattenNestedSequences(speechGen))
		seq.insert(0, cb)
		# Speak the speech sequence.
		spoke = self.handler.speechWithoutPausesInstance.speakWithoutPauses(seq)
		# Update the textInfo state ready for when speaking the next line.
		self.speakTextInfoState = state.copy()

		if not self.collapseLineImpl():
			return

		if not spoke:
			# This line didn't include a natural pause, so nothing was spoken.
			self.numBufferedLines += 1
			if self.numBufferedLines < self.MAX_BUFFERED_LINES:
				# Move on to the next line.
				# We queue this to allow the user a chance to stop say all.
				queueHandler.queueFunction(queueHandler.eventQueue, self.nextLine)
			else:
				# We don't want to buffer too much.
				# Force speech. lineReached will resume things when speech catches up.
				self.handler.speechWithoutPausesInstance.speakWithoutPauses(None)
				# The first buffered line has now started speaking.
				self.numBufferedLines -= 1

	def lineReached(self, obj, bookmark, state):
		# We've just started speaking this line, so move the cursor there.
		state.updateObj()
		updater = obj.makeTextInfo(bookmark)
		self.updateCaret(updater)
		winKernel.SetThreadExecutionState(winKernel.ES_SYSTEM_REQUIRED)
		if self.numBufferedLines == 0:
			# This was the last line spoken, so move on.
			self.nextLine()
		else:
			self.numBufferedLines -= 1

	def turnPage(self):
		try:
			self.reader.obj.turnPage()
		except RuntimeError:
			log.debug("No more pages")
			# No more pages.
			self.stop()
			return
		self.reader = self.reader.obj.makeTextInfo(textInfos.POSITION_FIRST)
		self.nextLine()

	def finish(self):
		# There is no more text.
		# Call stop to clean up, but only after speech completely finishes.
		# Otherwise, if a different synth is being used for say all,
		# we might switch synths too early and truncate the final speech.
		# We do this by putting a CallbackCommand at the start of a new utterance.
		cb = CallbackCommand(self.stop, name="say-all:stop")
		self.handler.speechWithoutPausesInstance.speakWithoutPauses([
			EndUtteranceCommand(),
			cb,
			EndUtteranceCommand()
		])

	def stop(self):
		if not self.reader:
			return
		self.reader = None
		self.trigger.exit()
		self.trigger = None

	def __del__(self):
		self.stop()


class _CaretTextReader(_TextReader):
	def getInitialTextInfo(self) -> textInfos.TextInfo:
		try:
			return api.getCaretObject().makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError) as e:
			raise NotImplementedError("Unable to make TextInfo: ", e)

	def updateCaret(self, updater: textInfos.TextInfo) -> None:
		updater.updateCaret()
		if config.conf["reviewCursor"]["followCaret"]:
			api.setReviewPosition(updater, isCaret=True)


class _ReviewTextReader(_TextReader):
	def getInitialTextInfo(self) -> textInfos.TextInfo:
		return api.getReviewPosition()

	def updateCaret(self, updater: textInfos.TextInfo) -> None:
		api.setReviewPosition(updater, isCaret=False)


class _TableTextReader(_CaretTextReader):
	def __init__(
			self,
			handler: _SayAllHandler,
			startPos: Optional[textInfos.TextInfo] = None,
			nextLineFunc: Optional[Callable[[textInfos.TextInfo], textInfos.TextInfo]] = None,
			shouldUpdateCaret: bool = True,
	):
		self.startPos = startPos
		self.nextLineFunc = nextLineFunc
		self.shouldUpdateCaret = shouldUpdateCaret
		super().__init__(handler)

	def getInitialTextInfo(self) -> textInfos.TextInfo:
		return self.startPos or super().getInitialTextInfo()

	def nextLineImpl(self) -> bool:
		try:
			self.reader = self.nextLineFunc(self.reader)
			return True
		except StopIteration:
			self.finish()
			return False

	def collapseLineImpl(self) -> bool:
		return True

	def shouldReadInitialPosition(self) -> bool:
		return True

	def updateCaret(self, updater: textInfos.TextInfo) -> None:
		if self.shouldUpdateCaret:
			return super().updateCaret(updater)


class SayAllProfileTrigger(config.ProfileTrigger):
	"""A configuration profile trigger for when say all is in progress.
	"""
	spec = "sayAll"
