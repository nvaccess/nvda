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
from speech.commands import (
	IndexCommand,
	CallbackCommand,
	BeepCommand,
	WaveFileCommand,
	EndUtteranceCommand,
	BaseProsodyCommand,
	RateCommand,
	VolumeCommand,
	PitchCommand,
	ConfigProfileTriggerCommand,
)
from speech.types import _IndexT

_SentSequenceIndex = int


@dataclass
class ExpectedIndex:
	"""To simplify building tests (de-duplication of test data) , ExpectedIndexes are not sent to the speech
		manager, but represent indexes that is sent to the synth.
	"""
	expectedIndexCommandIndex: int

	def __eq__(self, other):
		if isinstance(other, IndexCommand):
			return other.index == self.expectedIndexCommandIndex
		elif isinstance(other, ExpectedIndex):
			return other.expectedIndexCommandIndex == self.expectedIndexCommandIndex
		return False


@dataclass
class ExpectedProsody:
	"""To simplify building (de-duplication of test data) tests, ExpectedProsody are not sent to the speech
	manager,
	but represent prosody
	commands that are sent to the synth. This may be as a result of resuming a previous utterance.
	"""
	expectedProsody: Union[
		PitchCommand,
		RateCommand,
		VolumeCommand
	]

	def __eq__(self, other):
		if type(self.expectedProsody) != type(other):
			return False
		if isinstance(other, BaseProsodyCommand):
			return repr(other) == repr(self.expectedProsody)
		return False


class SpeechManagerInteractions:
	""" Track expected state and interactions with the speechManager.
	SpeechManager has the following functions that external code interacts with. Currently only supports
	setting / checking expectations within an expectation block. See L{SpeechManagerInteractions.expectation}
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

	The expectation method should be used as a context manager to assert the pre/post conditions on interactions
	with the speech manager.
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
		#: Map of mocks to the number of times that we expect for them get called in this expect block.
		self._awaitingMockCalls: typing.Dict[MagicMock, int] = {}

		#: All sequence indexes already expected to be sent to the synth
		self.expectedState_speak: List[_SentSequenceIndex] = []
		#: Number of calls to cancel
		self.expectedState_cancelCallCount: int = 0
		#: Indexes that have been reached
		self.expectedState_indexReached: List[_IndexT] = []

		#: map mocks with the number of times we expect them to be called useful for extending this class
		self._expectedMockCallCount: typing.Dict[MagicMock, int] = {}

		self._unexpectedSideEffectFailureMessages = []

		self._inExpectBlock = False

		# Install the mock synth
		synthDriverHandler._curSynth = self.synthMock
		synthDriverHandler._getSynthDriver = lambda name: mock.Mock(return_value=self.synthMock)
		#: Sequences sent to the speechManager so far.
		self._knownSequences = []
		#: Map ExpectedIndexes (IndexCommand) to knownSequences index
		self._speechManagerIndexes = {}

		self._indexCommandIndexes = iter(range(1, 1000))
		self._lastCommandIndex = 0
		self._testDebug_IndexReached: List[int] = []

		self.sManager = speech.manager.SpeechManager()

	def _sideEffect_synth_speak(self, sequence):
		if not self._inExpectBlock:  # an ExpectBlock will verify state on exit
			failureMessage = (
				"Unexpected call to synth.speak. Calls should happen in an expect block."
			)
			# sometimes for code called by SpeechManager, exceptions caused by failed asserts are caught.
			# record them so that at any subsequent _verifyCurrentState calls they can be reported.
			self._unexpectedSideEffectFailureMessages.append(failureMessage)
			self._testCase.fail(failureMessage)

	def _sideEffect_synth_cancel(self):
		if not self._inExpectBlock:  # an ExpectBlock will verify state on exit
			failureMessage = (
				"Unexpected call to synth.cancel. Calls should happen in an expect block."
			)
			# sometimes for code called by SpeechManager, exceptions caused by failed asserts are caught.
			# record them so that at any subsequent _verifyCurrentState calls they can be reported.
			self._unexpectedSideEffectFailureMessages.append(failureMessage)
			self._testCase.fail(failureMessage)

	def _sideEffect_callbackCommand(self, index):
		"""Callback commands must be expected, so they can deliver new speech.
		Asserts can not be run inside callback commands, the exceptions they raise on failure are caught by
		speechManager.
		"""
		if not self._inExpectBlock:  # an ExpectBlock will verify state on exit
			failureMessage = "Unexpected call to callbackCommand. Calls should happen in an expect block."
			# sometimes for code called by SpeechManager, exceptions caused by failed asserts are caught.
			# record them so that at any subsequent _verifyCurrentState calls they can be reported.
			self._unexpectedSideEffectFailureMessages.append(failureMessage)
			self._testCase.fail(failureMessage)
		# pop used because there may be multiple callbacks for a given operation.
		# We wish to verify the order of the callbacks.
		expectedIndex, sideEffect = self._awaitingCallbackForIndex[-1]
		if expectedIndex != index:
			failureMessage = "Unexpected index for callbackCommand. Calls should happen in an expect block."
			self._unexpectedSideEffectFailureMessages.append(failureMessage)
			return  # by returning early intentionally allow later asserts to fail
		if sideEffect:
			sideEffect()
		self.expectedState_indexReached.append(expectedIndex)
		self._awaitingCallbackForIndex.pop()

	@contextmanager
	def expectation(self):
		"""Ensures the pre/post conditions are as expected when exercising the SpeechManager.
		"""
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
		self._updateExpectedStateFromAwaiting_mocks()
		self._verifyCurrentState()

	def _verifyCurrentState(self):
		if self._unexpectedSideEffectFailureMessages:
			self._testCase.fail(f"Unexpected calls: {self._unexpectedSideEffectFailureMessages!r}")
		self._assertCurrentSpeechCallState()
		self._assertIndexCallbackState()
		self._assertCancelState()
		self._assertMockCallsState()
		pass

	def _updateKnownSequences(self, seq) -> List[_SentSequenceIndex]:
		"""Handle EndUtteranceCommands
			Sequence gets split after the EndUtteranceCommand and two sequence numbers are returned.
		"""
		startOfUtteranceIndexes = set(
			i + 1 for i, item in enumerate(seq)
			if isinstance(item, EndUtteranceCommand)
		)
		startOfUtteranceIndexes.add(len(seq))  # ensure the last index is included
		start = 0
		seqNumbers = []
		for nextStart in startOfUtteranceIndexes:
			seqNumbers.append(len(self._knownSequences))
			self._knownSequences.append(seq[start:nextStart])
			start = nextStart
		# Keep track of which sequence each "expectedIndex" belongs to.
		# This allows us to verify that tests don't call "reached index" before the sequence it is part of
		# has been sent to the synth. Essentially to prevent bugs in the tests.
		for seqNumber in seqNumbers:
			indexNumbers = [
				speechItem.index
				if not hasattr(speechItem, 'expectedIndexCommandIndex')
				else speechItem.expectedIndexCommandIndex
				for speechItem in self._knownSequences[seqNumber]
				if hasattr(speechItem, 'expectedIndexCommandIndex')
				or isinstance(speechItem, IndexCommand)
			]
			for index in indexNumbers:
				self._speechManagerIndexes[index] = seqNumber
		return seqNumbers

	def speak(
			self,
			seq: List[Union[speech.types.SequenceItemT, ExpectedProsody, ExpectedIndex, EndUtteranceCommand]],
			priority=speech.Spri.NORMAL
	) -> Union[_SentSequenceIndex, List[_SentSequenceIndex]]:
		"""Call SpeechManager.speak and track sequences used."""
		sequenceNumbers = self._updateKnownSequences(seq)
		self._filterAndSendSpeech(seq, priority)
		return sequenceNumbers if len(sequenceNumbers) > 1 else sequenceNumbers[0]

	def cancel(self):
		"""Call SpeechManager.cancel"""
		self.sManager.cancel()

	def removeCancelledSpeechCommands(self):
		"""Call SpeechManager.removeCancelledSpeechCommands"""
		self.sManager.removeCancelledSpeechCommands()

	def indexReached(self, index: _IndexT):
		"""Call SpeechManager.indexReached
		@note SpeechManager requires a call to pumpAll for this to have any affect.
		"""
		self._assertSpeechManagerKnowsAboutIndex(index)
		self._testDebug_IndexReached.append(index)
		self.sManager._onSynthIndexReached(self.synthMock, index)

	def doneSpeaking(self):
		"""Call SpeechManager.doneSpeaking
		@note SpeechManager requires a call to pumpAll for this to have any affect
		"""
		self.sManager._onSynthDoneSpeaking(self.synthMock)

	def pumpAll(self):
		"""Call queueHandler.pumpAll
		@note This is required to process pending events (indexReached, doneSpeaking) for SpeechManager.
		"""
		queueHandler.pumpAll()

	def create_CallBackCommand(self, expectedToBecomeIndex):
		"""While a CallBackCommand could be created directly, this method augments it with the index number it
		is expected to be represented by when sent to the synth. This reduces the duplication of the test data.
		"""
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		cb = CallbackCommand(
			lambda i=expectedToBecomeIndex: self._indexReachedCallback(i),
			name=f"indexCommandIndex: {expectedToBecomeIndex}"
		)
		cb.expectedIndexCommandIndex = expectedToBecomeIndex
		return cb

	def create_ExpectedIndex(self, expectedToBecomeIndex):
		"""Creates a placeholder for an IndexCommand that should be created by SpeechManager.
		ExpectedIndexes are not passed to the SpeechManager. They act as a placeholder to verify what is sent
		to the synth. This is useful when you want to confirm that an index is created by speechManager
		"""
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		return ExpectedIndex(expectedToBecomeIndex)

	def create_ExpectedProsodyCommand(self, expectedProsody):
		"""ExpectedProsodyCommands are not passed to the speechManager. They act as a placeholder to verify
		what is sent to the synth. This is useful when you want to confirm that speechManager recreates prosody
		effectively.
		"""
		return ExpectedProsody(expectedProsody)

	def create_BeepCommand(self, hz, length, left=50, right=50, expectedToBecomeIndex=None):
		"""BeepCommands get converted into IndexCommands by speechManager. The expectedToBecomeIndex argument
		allow us to track that.
		@note: the expectedToBecomeIndex is tested to be ordered, contiguous, and unique with respect to other
		indexed commands to help to prevent errors in the tests.
		"""
		self._testCase.assertIsNotNone(
			expectedToBecomeIndex,
			"Did you forget to provide the 'expectedToBecomeIndex' argument?"
		)
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		b = BeepCommand(hz, length, left, right)
		b.expectedIndexCommandIndex = expectedToBecomeIndex
		return b

	def create_ConfigProfileTriggerCommand(self, trigger, enter=True, expectedToBecomeIndex=None):
		"""ConfigProfileTriggerCommands get converted into IndexCommands by speechManager. The
		expectedToBecomeIndex argument allows tracking that.
		@note: the expectedToBecomeIndex is tested to be ordered, contiguous, and unique with respect to other
		indexed commands to help to prevent errors in the tests.
		"""
		self._testCase.assertIsNotNone(
			expectedToBecomeIndex,
			"Did you forget to provide the 'expectedToBecomeIndex' argument?"
		)
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		t = ConfigProfileTriggerCommand(trigger, enter)
		t.expectedIndexCommandIndex = expectedToBecomeIndex
		return t

	def create_WaveFileCommand(self, filename, expectedToBecomeIndex=None):
		"""WaveFileCommands get converted into IndexCommands by speechManager. The expectedToBecomeIndex argument
		allows tracking that.
		@note: the expectedToBecomeIndex is tested to be ordered, contiguous, and unique with respect to other
		indexed commands to help to prevent errors in the tests.
		"""
		self._testCase.assertIsNotNone(
			expectedToBecomeIndex,
			"Did you forget to provide the 'expectedToBecomeIndex' argument?"
		)
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		w = WaveFileCommand(filename)
		w.expectedIndexCommandIndex = expectedToBecomeIndex
		return w

	def create_EndUtteranceCommand(self, expectedToBecomeIndex=None):
		"""EndUtteranceCommand get converted into IndexCommands by speechManager. The expectedToBecomeIndex argument
		allow tracking that.
		@note: the expectedToBecomeIndex is tested to be ordered, contiguous, and unique with respect to other
		indexed commands to help to prevent errors in the tests.
		"""
		self._testCase.assertIsNotNone(
			expectedToBecomeIndex,
			"Did you forget to provide the 'expectedToBecomeIndex' argument?"
		)
		self._assertStrictIndexOrder(expectedToBecomeIndex)
		e = EndUtteranceCommand()
		e.expectedIndexCommandIndex = expectedToBecomeIndex
		return e

	def expect_indexReachedCallback(
			self,
			forIndex: _IndexT,
			sideEffect: Optional[Callable[[], None]] = None
	):
		"""Expect that upon exiting the expectation block, forIndex will have been reached.
			If a side effect is required (such as speaking more text) this must be called before
			triggering the index reached code, in this case consider using pumpAllAndSendSpeechOnCallback.
		"""
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
		if index not in self._speechManagerIndexes.keys():
			self._testCase.fail(f"Index {index} is not one of the index commands sent to speech manager.")
		seqNumber = self._speechManagerIndexes[index]
		if seqNumber not in self.expectedState_speak:  # ensure the index has been sent to the synth
			self._testCase.fail(f"Index {index} not yet sent to the synth. This indicates an error in the test.")

	def expect_synthCancel(self):
		if not self._inExpectBlock:
			self._testCase.fail("Expectations should be set in a with expectation() block")
		self._awaitingCancelCalls = 1 + self._awaitingCancelCalls

	def addMockCallMonitoring(self, monitorMocks: typing.List[mock.Mock]):
		""" Allows the call count state for other arbitrary mock objects to be tracked.
		@param monitorMocks: Mock objects to track the number of calls to
		"""
		for m in monitorMocks:
			self._expectedMockCallCount[m] = 0

	def expect_mockCall(self, m: mock.Mock):
		""" Expect another call to the given Mock. The total number of expected calls to this mock is incremented.
		@param m: Mock object to expect another call on.
		"""
		if not self._inExpectBlock:
			self._testCase.fail("Expectations should be set in a with expectation() block")
		self._awaitingMockCalls[m] = 1 + self._awaitingMockCalls.get(m, 0)

	def expect_synthSpeak(
			self,
			sequenceNumbers: Optional[Union[int, typing.Iterable[int]]] = None,
			sequence: Optional[List[Union[speech.types.SequenceItemT, ExpectedProsody, ExpectedIndex]]] = None,
	):
		isSpeechSpecified = sequence is not None
		areNumbersSpecified = sequenceNumbers is not None
		if (isSpeechSpecified and areNumbersSpecified) or not (isSpeechSpecified or areNumbersSpecified):
			raise ValueError("Exactly one argument should be provided.")
		if isSpeechSpecified:
			sequenceNumbers = self._updateKnownSequences(sequence)

		if isinstance(sequenceNumbers, int):
			if not self._inExpectBlock:
				self._testCase.fail("Expectations should be set in a with expectation() block")

			self._testCase.assertLess(
				sequenceNumbers,
				len(self._knownSequences),
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

	def _updateExpectedStateFromAwaiting_mocks(self):
		for m, awaitCount in self._awaitingMockCalls.items():
			e = self._expectedMockCallCount.get(m, 0)
			self._expectedMockCallCount[m] = e + awaitCount
		self._awaitingMockCalls.clear()

	def _updateExpectedStateFromAwaiting_callbacks(self):
		self.expectedState_indexReached.extend(
			index for index, c in self._awaitingCallbackForIndex
		)
		self._awaitingCallbackForIndex.clear()

	def _assertIndexCallbackState(self):
		expectedCalls = [mock.call(i) for i in self.expectedState_indexReached]
		self._testCase.assertEqual(
			len(expectedCalls),
			self._indexReachedCallback.call_count,
			msg=(
				f"Number of CallbackCommand callbacks not as expected."
				f"\nExpected: {expectedCalls}"
				f"\nGot: {self._indexReachedCallback.call_args_list}"
			)
		)
		self._indexReachedCallback.assert_has_calls(expectedCalls)

	def _assertCancelState(self):
		expectedCancelCallCount = self.expectedState_cancelCallCount
		self._testCase.assertEqual(
			expectedCancelCallCount,
			self.synthMock.cancel.call_count,
			msg=f"The number of calls to synth.cancel was not as expected. Expected {expectedCancelCallCount}"
		)

	def _assertMockCallsState(self):
		for m, e in self._expectedMockCallCount.items():
			self._testCase.assertEqual(
				e,
				m.call_count,
				msg=f"The number of calls to {m} was not as expected. Expected {e}"
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
		replaceWithExpectedIndexTypes = (
			CallbackCommand,
			BeepCommand,
			WaveFileCommand,
			EndUtteranceCommand,
			ConfigProfileTriggerCommand,
		)
		expectedCalls = []
		for s in expectedSeqIndexes:
			expectedSpeech = self._knownSequences[s]
			expectedSpeech = [
				x if not isinstance(x, replaceWithExpectedIndexTypes)
				else ExpectedIndex(x.expectedIndexCommandIndex)
				for x in expectedSpeech
			]
			expectedCalls.append(mock.call(expectedSpeech))

		if expectedCalls:
			mockSpeak.assert_has_calls(expectedCalls)

	def pumpAllAndSendSpeechOnCallback(
			self,
			expectCallbackForIndex: int,
			expectedSendSequenceNumber: Union[int, List[int]],
			seq,
			priority=speech.Spri.NORMAL
	):
		"""Must be called in an 'expectation' block. """
		def _lineReachedSideEffect():
			self._filterAndSendSpeech(seq, priority)

		actualSequenceNumber = self._updateKnownSequences(seq)
		actualSequenceNumber = actualSequenceNumber if len(actualSequenceNumber) > 1 else actualSequenceNumber[0]
		self._testCase.assertEqual(expectedSendSequenceNumber, actualSequenceNumber)

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

	def _filterAndSendSpeech(self, seq, priority):
		filteredSpeech = [
			x for x in seq
			if not isinstance(x, (ExpectedIndex, ExpectedProsody))  # don't send types used for behaviour tracking.
		]
		self.sManager.speak(filteredSpeech, priority)
