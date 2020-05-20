# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited

"""A test harness for interacting with the SpeechManager class."""
import typing
import unittest
from contextlib import contextmanager
from typing import (
	Callable,
	Tuple,
	Union,
	Optional,
	List,
)
from unittest import mock
from unittest.mock import (
	MagicMock,
)

from dataclasses import dataclass

import queueHandler
import speech.manager
from speech import (
	IndexCommand,
	CallbackCommand,
	SpeechSequence,
)
from speech.types import _IndexT

_SentSequenceIndex = int


@dataclass
class ExpectedIndex:
	expectedIndexCommandIndex: int

	def __eq__(self, other):
		if isinstance(other, IndexCommand):
			return other.index == self.expectedIndexCommandIndex
		elif isinstance(other, ExpectedIndex):
			return other.expectedIndexCommandIndex == self.expectedIndexCommandIndex
		return False


class SpeechManagerInteractions:
	""" Track expected state and interactions with the speechManager.
	SpeechManager has the following functions that external code interacts with.
	Inputs:
	- SpeechManager.speak()
	- SpeechManager.cancel()
	- SpeechManager.removeCancelledSpeechCommands: Normally via eventHandler.executeEvent
	- SpeechManager._onSynthIndexReached(): Normally via synthDriverHandler.synthIndexReached extensionPoint
	- SpeechManager._onSynthDoneSpeaking(): Normally via synthDriverHandler.synthDoneSpeaking extensionPoint
	- queueHandler.pumpAll(): handles all pending _onSynthIndexReached and _onSynthDoneSpeaking calls.
	Outputs:
	- synthDriverHandler.getSynth().speak(): Send speech to the synth.
	- synthDriverHandler.getSynth().cancel(): Cancel current speech.
	- CallbackCommand: Converted into index commands. When the index is reached (by the synth) the callback is
			called after queueHandler.pumpAll is called.
	"""
	def __init__(self, testCase: unittest.TestCase):
		"""
		@param testCase: Used to run asserts
		"""
		self._testCase = testCase
		import synthDriverHandler

		#: speechManager needs to call to the synth
		self.synthMock = MagicMock()
		self.synthMock.speak.side_effect = self._sideEffect_synth_speak
		self.synthMock.cancel.side_effect = self._sideEffect_synth_cancel

		#: Used by CallbackCommands, called when their associated index is reached. Records the indexes.
		self._indexReachedCallback = MagicMock()
		self._indexReachedCallback.side_effect = self._sideEffect_callbackCommand

		#: SequenceIndexes we are awaiting to be sent to the synth
		self._awaitingSpeakCalls: List[_SentSequenceIndex] = []
		#: Number of cancel calls we are waiting for
		self._awaitingCancelCalls: int = 0
		#: Index and Callbacks for callback commands
		self._awaitingCallbackForIndex: List[Tuple[_IndexT, Optional[Callable[[], None]]]] = []

		#: All sequence indexes already expected to be sent to the synth
		self.expectedState_speak: List[_SentSequenceIndex] = []
		#: Number of calls to cancel
		self.expectedState_cancelCallCount: int = 0
		#: Indexes that have been reached
		self.expectedState_indexReached: List[_IndexT] = []

		self._inExpectBlock = False

		# Install the mock synth
		synthDriverHandler._curSynth = self.synthMock
		#: Sequences sent to the speechManager so far.
		self._sentSequences = []

		self._indexCommandIndexes = iter(range(1, 1000))
		self._lastCommandIndex = 0
		self._testDebug_IndexReached: List[int] = []

		self.sManager = speech.manager.SpeechManager()

	def _sideEffect_synth_speak(self, sequence):
		if not self._inExpectBlock:  # an ExpectBlock will verify state on exit
			self._testCase.assertTrue(self._awaitingSpeakCalls)
			self._updateExpectedStateFromAwaiting_speak()
			self._verifyCurrentState()

	def _sideEffect_synth_cancel(self):
		if not self._inExpectBlock:  # an ExpectBlock will verify state on exit
			self._testCase.assertTrue(self._awaitingCancelCalls)
			self._updateExpectedStateFromAwaiting_cancel()
			self._verifyCurrentState()

	def _sideEffect_callbackCommand(self, index):
		"""Callback commands must be expected, so they can deliver new speech.
		Asserts can not be run inside callback commands, the exceptions they raise on failure are caught by
		speechManager.
		"""
		# pop used because there may be multiple callbacks for a given operation.
		# We wish to verify the order of the callbacks.
		expectedIndex, sideEffect = self._awaitingCallbackForIndex[-1]
		if expectedIndex != index:
			return
		if sideEffect:
			sideEffect()
		self.expectedState_indexReached.append(expectedIndex)
		self._awaitingCallbackForIndex.pop()

	@contextmanager
	def expectation(self):
		"""Used to ensure that the next command results in an expected change."""
		self._testCase.assertFalse(self._inExpectBlock, msg="This is likely a logic error in the test.")
		self._inExpectBlock = True
		self._verifyCurrentState()
		yield
		self.assertExpectedStateNowMet()
		self._inExpectBlock = False

	def assertExpectedStateNowMet(self):
		self._updateExpectedStateFromAwaiting_speak()
		self._updateExpectedStateFromAwaiting_cancel()
		self._updateExpectedStateFromAwaiting_callbacks()
		self._verifyCurrentState()

	def _verifyCurrentState(self):
		# Sequences sent to synth?
		self._assertCurrentSpeechCallState()
		self._assertIndexCallbackState()
		self._assertCancelState()
		pass

	def speak(self, seq: SpeechSequence, priority=speech.Spri.NORMAL) -> _SentSequenceIndex:
		nextSentSequenceNumber = len(self._sentSequences)
		self._sentSequences.append(seq)
		filteredSpeech = [
			x for x in self._sentSequences[nextSentSequenceNumber]
			if not isinstance(x, ExpectedIndex)  # don't send types used for behaviour tracking.
		]
		self.sManager.speak(filteredSpeech, priority)
		return nextSentSequenceNumber

	def cancel(self):
		self.sManager.cancel()

	def removeCancelledSpeechCommands(self):
		"""Call SpeechManager.removeCancelledSpeechCommands"""
		self.sManager.removeCancelledSpeechCommands()

	def indexReached(self, index: _IndexT):
		self._assertSpeechManagerKnowsAboutIndex(index)
		self._testDebug_IndexReached.append(index)
		self.sManager._onSynthIndexReached(self.synthMock, index)

	def doneSpeaking(self):
		self.sManager._onSynthDoneSpeaking(self.synthMock)

	def pumpAll(self):
		queueHandler.pumpAll()

	def create_CallBackCommand(self, expectedToBecomeIndex):
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		cb = CallbackCommand(
			lambda i=expectedToBecomeIndex: self._indexReachedCallback(i),
			name=f"indexCommandIndex: {expectedToBecomeIndex}"
		)
		cb.expectedIndexCommandIndex = expectedToBecomeIndex
		return cb

	def create_ExpectedIndex(self, expectedToBecomeIndex):
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		return ExpectedIndex(expectedToBecomeIndex)

	def expect_indexReachedCallback(
			self,
			forIndex: _IndexT,
			sideEffect: Optional[Callable[[], None]] = None
	):
		if not self._inExpectBlock:
			self._testCase.fail("Expectations should be set in a with expectation() block")
		if not (self._lastCommandIndex >= forIndex > 0):
			self._testCase.fail(
				f"Test Case error. Index {forIndex} not sent to synth yet,"
				f" ensure SpeechManagerInteractions.speak has already been called."
			)
		self._awaitingCallbackForIndex.append((forIndex, sideEffect))

		if forIndex not in self._testDebug_IndexReached:
			self._testCase.fail(
				f"IndexReached not yet called for {forIndex}."
				f" Check test for smi.indexReached({forIndex})"
				f" IndexReach called for the following: {self._testDebug_IndexReached!r}"
			)
		self._assertSpeechManagerKnowsAboutIndex(forIndex)

	def _assertSpeechManagerKnowsAboutIndex(self, index):
		indexCommands = [
			(seqNumber, speechItem)
			for seqNumber, seq in enumerate(self._sentSequences)
			for speechItem in seq
			if isinstance(speechItem, (CallbackCommand, ExpectedIndex))
			and speechItem.expectedIndexCommandIndex == index
		]
		if len(indexCommands) != 1:
			self._testCase.fail(f"Index {index} is not one of the index commands sent to speech manager.")
		seqNumber, speechItem = indexCommands[0]
		if seqNumber not in self.expectedState_speak:  # ensure the index has been sent to the synth
			self._testCase.fail(f"Index {index} not yet sent to the synth")

	def expect_synthCancel(self):
		if not self._inExpectBlock:
			self._testCase.fail("Expectations should be set in a with expectation() block")
		self._awaitingCancelCalls = 1 + self._awaitingCancelCalls

	def expect_synthSpeak(self, sequenceNumbers: Union[int, typing.Iterable[int]]):
		if isinstance(sequenceNumbers, int):
			if not self._inExpectBlock:
				self._testCase.fail("Expectations should be set in a with expectation() block")

			self._testCase.assertLess(
				sequenceNumbers,
				len(self._sentSequences),
				msg=f"Less than {sequenceNumbers} sequences have been sent to the synth (see calls to speak)"
			)
			self._awaitingSpeakCalls.append(sequenceNumbers)
		else:
			for i in sequenceNumbers:
				if isinstance(i, int):
					self.expect_synthSpeak(i)
				else:
					self._testCase.fail(
						f"sequenceNumbers should be int or Iterable[int]. ArgType: {type(sequenceNumbers)}"
					)

	def _updateExpectedStateFromAwaiting_speak(self):
		self.expectedState_speak.extend(self._awaitingSpeakCalls)
		self._awaitingSpeakCalls.clear()

	def _updateExpectedStateFromAwaiting_cancel(self):
		self.expectedState_cancelCallCount = self.expectedState_cancelCallCount + self._awaitingCancelCalls
		self._awaitingCancelCalls = 0

	def _updateExpectedStateFromAwaiting_callbacks(self):
		self.expectedState_indexReached.extend(
			index for index, c in self._awaitingCallbackForIndex
		)
		self._awaitingCallbackForIndex.clear()

	def _assertIndexCallbackState(self):
		expectedCalls = [mock.call(i) for i in self.expectedState_indexReached]
		self._indexReachedCallback.assert_has_calls(expectedCalls)

	def _assertCancelState(self):
		expectedCancelCallCount = self.expectedState_cancelCallCount
		self._testCase.assertEqual(
			expectedCancelCallCount,
			self.synthMock.cancel.call_count,
			msg=f"The number of calls to synth.cancel was not as expected. Expected {expectedCancelCallCount}"
		)

	def _assertCurrentSpeechCallState(self):
		expectedSeqIndexes = self.expectedState_speak
		mockSpeak = self.synthMock.speak
		actualCallCount = mockSpeak.call_count
		self._testCase.assertEqual(
			len(expectedSeqIndexes),
			actualCallCount,
			msg=(
				f"Number of sequences sent to synth not as expected."
				f"\nExpected a total of {len(expectedSeqIndexes)}"
				f"\nThe index(es) of the expected sequences: {expectedSeqIndexes}"
				f"\nActual calls: {mockSpeak.call_args_list}"
			)
		)
		# Build (total) expected call list
		expectedCalls = []
		for s in expectedSeqIndexes:
			expectedSpeech = self._sentSequences[s]
			expectedSpeech = [
				x if not isinstance(x, CallbackCommand) else ExpectedIndex(x.expectedIndexCommandIndex)
				for x in expectedSpeech
			]
			expectedCalls.append(mock.call(expectedSpeech))

		if expectedCalls:
			mockSpeak.assert_has_calls(expectedCalls)

	def pumpAllAndSendSpeechOnCallback(
			self,
			expectCallbackForIndex: int,
			expectedSendSequenceNumber: int,
			seq,
	):
		"""Must be called in an 'expectation' block. """
		def _lineReachedSideEffect():
			actualSendSequenceNumber = self.speak(seq=seq)
			self._testCase.assertEqual(expectedSendSequenceNumber, actualSendSequenceNumber)

		self.expect_indexReachedCallback(expectCallbackForIndex, _lineReachedSideEffect)
		self.pumpAll()
		self._assertIndexCallbackState()

	def _assertStrictIndexOrder(self, expectedToBecomeIndex):
		indexCommandIndex = next(self._indexCommandIndexes)
		self._lastCommandIndex = indexCommandIndex
		self._testCase.assertEqual(
			expectedToBecomeIndex,
			indexCommandIndex,
			msg=f"Did you forget to update the 'expectedToBecomeIndex' argument?"
		)
