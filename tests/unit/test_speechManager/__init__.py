# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited

"""Unit tests for speech/manager module
"""
import unittest
from typing import Optional, Callable

import config
import speech
from unittest import mock
from unittest.mock import (
	patch,
)
import speech.manager
from speech.commands import (
	BeepCommand,
	WaveFileCommand,
	PitchCommand,
	ConfigProfileTriggerCommand,
	_CancellableSpeechCommand,
	CharacterModeCommand,
	EndUtteranceCommand,
)
from .speechManagerTestHarness import (
	_IndexT,
	ExpectedIndex,
	ExpectedProsody,
	SpeechManagerInteractions,
)

#: Enable logging used to aid in the development of unit
# Hard coding this to True where it is defined makes creating new unit tests easier, since all interactions
# can be tracked.
speech.manager.IS_UNIT_TEST_LOG_ENABLED = True

_isIndexABeforeIndexB = speech.manager.SpeechManager._isIndexABeforeIndexB
MAX_INDEX = speech.manager.SpeechManager.MAX_INDEX
WRAPPED_INDEX_MAGNITUDE = speech.manager.SpeechManager._WRAPPED_INDEX_MAGNITUDE


class TestSpeechIndexComparison(unittest.TestCase):
	"""Speech indexes wrap around after a limit which must be considered when comparing relative positions of
	indexes
	"""

	def testSimple_before(self):
		self.assertTrue(_isIndexABeforeIndexB(2, 3))

	def testSimple_equal(self):
		self.assertFalse(_isIndexABeforeIndexB(2, 2))

	def testSimple_after(self):
		self.assertFalse(_isIndexABeforeIndexB(3, 2))

	def testWrapped_beforeAfter(self):
		lastIndex = MAX_INDEX  # last index
		firstIndex: _IndexT = 1  # first index after wrapping.
		self.assertTrue(_isIndexABeforeIndexB(lastIndex, firstIndex))
		self.assertFalse(_isIndexABeforeIndexB(firstIndex, lastIndex))

	def testExtents_relativeToFirstIndex(self):
		"""How far ahead of the first index can b get before a is no longer considered before
		"""
		firstIndex: _IndexT = 1
		boundaryAfterFirstIndex = WRAPPED_INDEX_MAGNITUDE + 1
		boundaryBeforeFirstIndex = boundaryAfterFirstIndex + 1
		# Relative to firstIndex
		self.assertTrue(_isIndexABeforeIndexB(firstIndex, boundaryAfterFirstIndex))
		self.assertFalse(_isIndexABeforeIndexB(firstIndex, boundaryBeforeFirstIndex))
		# And ensure symmetry
		self.assertTrue(_isIndexABeforeIndexB(boundaryBeforeFirstIndex, firstIndex))
		self.assertFalse(_isIndexABeforeIndexB(boundaryAfterFirstIndex, firstIndex))

	def testExtents_relativeToLastIndex(self):
		"""How far ahead of the "last index" can b get before a is no longer considered before
		"""
		lastIndex = MAX_INDEX

		boundaryAfterLastIndex = WRAPPED_INDEX_MAGNITUDE
		boundaryBeforeLastIndex = boundaryAfterLastIndex + 1

		self.assertTrue(_isIndexABeforeIndexB(lastIndex, boundaryAfterLastIndex))
		self.assertFalse(_isIndexABeforeIndexB(lastIndex, boundaryBeforeLastIndex))
		# And ensure symmetry
		self.assertFalse(_isIndexABeforeIndexB(boundaryAfterLastIndex, lastIndex))
		self.assertTrue(_isIndexABeforeIndexB(boundaryBeforeLastIndex, lastIndex))

	def testExtents_relativeToMidPoint(self):
		""" Despite the largest possible index being odd, there is an even number of possible indexes since
		zero is not used as an index. For a given A value there will be a B value (in a space of 9998
		values) that is equal, leaving 9997 values which can not be split evenly into before / after.
		"""
		lastIndex = MAX_INDEX
		firstIndex: _IndexT = 1

		self.assertTrue(_isIndexABeforeIndexB(firstIndex, WRAPPED_INDEX_MAGNITUDE))
		self.assertTrue(_isIndexABeforeIndexB(WRAPPED_INDEX_MAGNITUDE + 1, lastIndex))
		# And ensure symmetry
		self.assertFalse(_isIndexABeforeIndexB(lastIndex, WRAPPED_INDEX_MAGNITUDE + 1))
		self.assertFalse(_isIndexABeforeIndexB(WRAPPED_INDEX_MAGNITUDE, firstIndex))

	def testAllValuesHaveSymmetry(self):
		"""Test all B values for a given A value.
		Confirm the number of equivalent, A-before, B-before, and assert no B values are both before and after!
		"""
		stationary: _IndexT = WRAPPED_INDEX_MAGNITUDE
		stationaryBeforeCount = 0
		movingBeforeCount = 0
		bothBefore = []  # a before b and b before a should never happen
		indexesWithEquivalence = []
		for moving in range(1, MAX_INDEX):
			isStationaryBefore = _isIndexABeforeIndexB(stationary, moving)
			isMovingBefore = _isIndexABeforeIndexB(moving, stationary)
			if isMovingBefore and isStationaryBefore:
				bothBefore.append((stationary, moving))
			elif isStationaryBefore:
				stationaryBeforeCount = stationaryBeforeCount + 1
			elif isMovingBefore:
				movingBeforeCount = movingBeforeCount + 1
			else:
				indexesWithEquivalence.append((stationary, moving))

		# There should only be one pair with equivalence (the equal pair)
		self.assertEqual(
			len(indexesWithEquivalence), 1,
			msg=f"Indexes with neither true: {indexesWithEquivalence!r}"
		)
		# Ensure equivalent indexes really are equal
		self.assertEqual(indexesWithEquivalence[0][0], indexesWithEquivalence[0][1])

		# None should be: A < B < A
		self.assertEqual(
			len(bothBefore), 0,
			msg=f"Indexes with both true: {bothBefore!r}"
		)
		# Check that the number of B values before and after is as expected.
		self.assertAlmostEqual(
			stationaryBeforeCount,
			movingBeforeCount,
			delta=1  # Odd number of available indexes since 0 is excluded and one pair is equivalent.
		)


class TestExpectedClasses(unittest.TestCase):
	def test_expectedProsodyEqualsMatching(self):
		p = PitchCommand(offset=2)
		e = ExpectedProsody(PitchCommand(offset=2))
		self.assertEqual(p, e)

	def test_expectedProsodyNotMatching(self):
		p = PitchCommand(offset=2)
		e = ExpectedProsody(PitchCommand(offset=5))
		self.assertNotEqual(p, e)


class _CancellableSpeechCommand_withLamda(_CancellableSpeechCommand):
	"""
	A test helper to control when speech gets cancelled.
	"""

	def _getDevInfo(self):
		return ""

	def _checkIfValid(self):
		return True

	def __init__(
			self,
			checkIfValid: Optional[Callable[[], bool]] = None,
			getDevInfo: Optional[Callable[[], str]] = None,
	):
		if checkIfValid is not None:
			self._checkIfValid = checkIfValid
		if getDevInfo is not None:
			self._getDevInfo = getDevInfo
		super().__init__(reportDevInfo=True)


class CancellableSpeechTests(unittest.TestCase):
	"""Tests behaviour related to CancellableSpeech"""

	def setUp(self):
		import speechDictHandler
		speechDictHandler.initialize()  # setting the synth depends on dictionary["voice"]
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 1  # yes

	def test_validSpeechSpoken(self):
		"""Tests the outcome when speech stays valid. It should not be cancelled."""
		smi = SpeechManagerInteractions(self)

		with smi.expectation():
			text = "This stays valid"
			smi.speak([text, _CancellableSpeechCommand_withLamda(lambda: True)])
			smi.expect_synthSpeak(sequence=[text, smi.create_ExpectedIndex(expectedToBecomeIndex=1)])

	def test_invalidSpeechNotSpoken(self):
		"""Ensure that invalid speech is not sent to the synth"""
		smi = SpeechManagerInteractions(self)

		with smi.expectation():
			text = "This stays invalid"
			smi.speak([text, _CancellableSpeechCommand_withLamda(lambda: False)])

	def test_invalidated_indexHit(self):
		"""Hitting an index should cause a cancellation of speech that has become
			invalid after being sent to the synth.
			For particularly long utterances with many indexes, the speech can be
			stopped sooner.
		"""
		smi = SpeechManagerInteractions(self)
		isSpeechNumberValid = {}

		def _checkIfValid(speechNumber):
			return isSpeechNumberValid.get(speechNumber, False)

		with smi.expectation():
			initiallyValidSequence = [
				"text 1",
				smi.create_CallBackCommand(expectedToBecomeIndex=1),
				"text 2",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2),
				_CancellableSpeechCommand_withLamda(lambda: _checkIfValid(1)),
			]
			isSpeechNumberValid[1] = True  # initially valid
			smi.speak(initiallyValidSequence)
			smi.expect_synthSpeak(sequence=initiallyValidSequence[:4])

		with smi.expectation():
			isSpeechNumberValid[1] = False  # becomes invalid
			smi.indexReached(1)
			smi.expect_indexReachedCallback(forIndex=1)
			smi.pumpAll()
			smi.expect_synthCancel()

	def test_invalidated_newSpeech(self):
		"""New speech should cause a cancellation of speech that has become
			invalid after being sent to the synth.
			Ensure that new speech can be started as soon as possible to reduce
			the stammering of the synth.
		"""
		smi = SpeechManagerInteractions(self)
		isSpeechNumberValid = {}

		def _checkIfValid(speechNumber):
			return isSpeechNumberValid.get(speechNumber, False)

		with smi.expectation():
			initiallyValidSequence = [
				"text 1",
				smi.create_CallBackCommand(expectedToBecomeIndex=1),
				"text 2",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2),
				_CancellableSpeechCommand_withLamda(lambda: _checkIfValid(1)),
			]
			isSpeechNumberValid[1] = True  # initially valid
			smi.speak(initiallyValidSequence)
			smi.expect_synthSpeak(sequence=initiallyValidSequence[:4])

		isSpeechNumberValid[1] = False
		with smi.expectation():
			newSequence = [
				"text 3",
				smi.create_CallBackCommand(expectedToBecomeIndex=3),
				"text 4",
				smi.create_ExpectedIndex(expectedToBecomeIndex=4),
			]
			smi.speak(newSequence)
			smi.expect_synthCancel()
			smi.expect_synthSpeak(sequence=newSequence[:4])

	def test_invalidated_newSpeechWithCancellable(self):
		"""New speech that contains a cancellableSpeechCommand should cause a
			cancellation of speech that has become invalid after being sent to the
			synth.
			Similar to test_invalidated_newSpeech, but ensure that the
			cancellableSpeechCommand does not affect the behaviour.
			"""
		smi = SpeechManagerInteractions(self)
		isSpeechNumberValid = {}

		def _checkIfValid(speechNumber):
			return isSpeechNumberValid.get(speechNumber, False)

		with smi.expectation():
			initiallyValidSequence = [
				"text 1",
				smi.create_CallBackCommand(expectedToBecomeIndex=1),
				"text 2",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2),
				_CancellableSpeechCommand_withLamda(lambda: _checkIfValid(1)),
			]
			isSpeechNumberValid[1] = True  # initially valid
			smi.speak(initiallyValidSequence)
			smi.expect_synthSpeak(sequence=initiallyValidSequence[:4])

		isSpeechNumberValid[1] = False
		isSpeechNumberValid[2] = True
		with smi.expectation():
			newValidSequence = [
				"text 3",
				smi.create_CallBackCommand(expectedToBecomeIndex=3),
				"text 4",
				smi.create_ExpectedIndex(expectedToBecomeIndex=4),
				_CancellableSpeechCommand_withLamda(lambda: _checkIfValid(2)),
			]
			smi.speak(newValidSequence)
			smi.expect_synthCancel()
			smi.expect_synthSpeak(sequence=newValidSequence[:4])

	def test_validSpeechAfterInvalid(self):
		"""Tests that calling speak with invalid speech will not lock up the SpeechManager.
		Under certain circumstances this resulted in NVDA going silent when more speech was in the queue.
		"""
		smi = SpeechManagerInteractions(self)

		with smi.expectation():
			smi.speak([
				"Stays invalid",
				_CancellableSpeechCommand_withLamda(lambda: False),
				smi.create_ExpectedIndex(expectedToBecomeIndex=1)
			])

		with smi.expectation():
			smi.speak(["Stays valid", _CancellableSpeechCommand_withLamda(lambda: True)])
			smi.expect_synthSpeak(sequence=[
				"Stays valid", smi.create_ExpectedIndex(expectedToBecomeIndex=2)
			])


class SayAllEmulatedTests(unittest.TestCase):
	"""Tests for speechManager operations."""

	def setUp(self):
		import speechDictHandler
		speechDictHandler.initialize()  # setting the synth depends on dictionary["voice"]
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 2  # no

	def test_simpleSpeech(self):
		smi = SpeechManagerInteractions(self)
		with smi.expectation():
			seqIndex = smi.speak(["hello ", "world", ExpectedIndex(1)])
			smi.expect_synthSpeak(seqIndex)

	def test_moreSpeechOnIndexReached(self):
		smi = SpeechManagerInteractions(self)
		with smi.expectation():
			seqIndex1 = smi.speak(["hello ", "world", ExpectedIndex(1)])
			seqIndex2 = smi.speak(["goodBye ", "earth", ExpectedIndex(2)])
			smi.expect_synthSpeak(seqIndex1)

		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_synthSpeak(seqIndex2)

	def test_standardSayAll(self):
		"""See #11144: Mimic behaviour that caused repeated speech during say-all - Full example.
		"""
		smi = SpeechManagerInteractions(self)
		callBack = smi.create_CallBackCommand
		expectIndex = smi.create_ExpectedIndex

		# First sayAll queues up a number of utterances.
		with smi.expectation():
			seqNum = smi.speak([
				callBack(expectedToBecomeIndex=1),
				'sequence 0  ',
				callBack(expectedToBecomeIndex=2)
			])
			self.assertEqual(seqNum, 0)
			# Speech manager is expected to get started immediately
			smi.expect_synthSpeak(seqNum)

		seqNum = smi.speak([
			'sequence 1 before call back  ',
			callBack(expectedToBecomeIndex=3),
			'sequence 1 after call back  ',
			callBack(expectedToBecomeIndex=4)
		])
		self.assertEqual(seqNum, 1)

		# Synth has already reached the first index, callback shouldn't be called until
		# pump all is called.
		smi.indexReached(1)  # start of sequenceNumber 0

		seqNum = smi.speak([
			'sequence 2  ',
			callBack(expectedToBecomeIndex=5)
		])
		self.assertEqual(seqNum, 2)

		seqNum = smi.speak([
			# for some reason say-all handler does not give this sequence callback commands
			'sequence 3  ',
			expectIndex(expectedToBecomeIndex=6)
		])
		self.assertEqual(seqNum, 3)

		with smi.expectation():
			smi.pumpAll()
			# no side effect, sayAll does not send more speech until the final callback index is hit.
			smi.expect_indexReachedCallback(forIndex=1, sideEffect=None)

		with smi.expectation():
			smi.indexReached(2)  # end of sequenceNumber 0
			smi.pumpAll()
			smi.expect_indexReachedCallback(forIndex=2, sideEffect=None)
			smi.expect_synthSpeak(1)  # new speech expected after reaching endOfUtterance

		with smi.expectation():
			smi.indexReached(3)  # in sequenceNumber 1
			smi.pumpAll()
			smi.expect_indexReachedCallback(forIndex=3, sideEffect=None)
			# Don't expect new speech to be sent to the synth, index is not at the end of the utterance.

		with smi.expectation():
			smi.indexReached(4)  # in sequenceNumber 1
			smi.pumpAll()
			smi.expect_indexReachedCallback(forIndex=4, sideEffect=None)
			smi.expect_synthSpeak(2)

		with smi.expectation():
			smi.indexReached(5)  # in sequenceNumber 2
			# Only 1 pending speech sequence from say all, this results in new speech being sent during the
			# callback which triggers the duplicate speech.
			smi.pumpAllAndSendSpeechOnCallback(
				expectCallbackForIndex=5,
				expectedSendSequenceNumber=4,
				seq=[
					callBack(expectedToBecomeIndex=7),
					'sequence 4  ', expectIndex(expectedToBecomeIndex=8)
				]
			)
			# Now ensure there is no double speaking!
			smi.expect_synthSpeak(3)

		smi.indexReached(6)  # in sequenceNumber 4, does not have a callback
		with smi.expectation():
			smi.pumpAll()  # No callback, so no handle index call
			smi.expect_synthSpeak(4)

	def test_speechNotRepeated(self):
		"""Minimal test for #11144: Repeated speech during say-all.
		Ensure that adding new speech during a callback does not result in double speaking.
		"""
		smi = SpeechManagerInteractions(self)
		callBack = smi.create_CallBackCommand
		expectIndex = smi.create_ExpectedIndex

		with smi.expectation():
			seq0 = smi.speak(['sequence 0  ', callBack(expectedToBecomeIndex=1)])
			seq1 = smi.speak(['sequence 1  ', callBack(expectedToBecomeIndex=2)])
			smi.expect_synthSpeak(seq0)

		with smi.expectation():
			smi.indexReached(1)  # in sequenceNumber 2
			# Only 1 pending speech sequence from say all, this results in new speech being sent during the
			# callback which triggers the duplicate speech.
			smi.pumpAllAndSendSpeechOnCallback(
				expectCallbackForIndex=1,
				expectedSendSequenceNumber=2,
				seq=[
					callBack(expectedToBecomeIndex=3),
					'sequence 2  ', expectIndex(expectedToBecomeIndex=4)
				]
			)
			# Now ensure there is no double speaking!
			smi.expect_synthSpeak(seq1)


class SayAllEmulatedTests_withCancellableSpeechEnabled(SayAllEmulatedTests):
	"""Note, while cancellable speech is configurable test with and without it enabled."""
	def setUp(self):
		super().setUp()
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 1  # yes


class InitialDevelopmentTests(unittest.TestCase):
	"""These tests were run manually during the initial development of speechManager.
		See PR #7599 for source of tests.
		Test numbers match order of tests defined on original PR, however they are grouped in this file based on
		the features they test.
		Manual test steps are kept in unit tests doc string, they can be run in the NVDA python console after
		the following imports:
			from speech import sayAll, appModuleHandler
	"""

	def setUp(self):
		import speechDictHandler
		speechDictHandler.initialize()  # setting the synth depends on dictionary["voice"]
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 2  # no

	@patch.object(WaveFileCommand, 'run')
	@patch.object(BeepCommand, 'run')
	def test_1(self, mock_BeepCommand_run, mock_WaveFileCommand_run):
		r"""Text, beep, beep, sound, text.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [
				u"This is some speech and then comes a", BeepCommand(440, 10),
				u"beep. If you liked that, let's ", BeepCommand(880, 10),
				u"beep again. I'll speak the rest of this in a ", PitchCommand(offset=50),
				u"higher pitch. And for the finale, let's ",
				WaveFileCommand(r"waves\browseMode.wav"), u"play a sound."
				])
		"""
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([mock_BeepCommand_run, mock_WaveFileCommand_run])
		_beepCommand = smi.create_BeepCommand
		_waveFileCommand = smi.create_WaveFileCommand
		sequence = [
			"This is some speech and then comes a",
			_beepCommand(440, 10, expectedToBecomeIndex=1),
			"beep. If you liked that, let's ",
			_beepCommand(880, 10, expectedToBecomeIndex=2),
			"beep again. I'll speak the rest of this in a ",
			PitchCommand(offset=50),
			"higher pitch. And for the finale, let's ",
			_waveFileCommand(r"waves\browseMode.wav", expectedToBecomeIndex=3),
			"play a sound.",
			smi.create_ExpectedIndex(expectedToBecomeIndex=4)
		]
		with smi.expectation():
			smi.speak(sequence)
			smi.expect_synthSpeak(0)

		for i in range(1, 5):
			with smi.expectation():
				smi.indexReached(i)
				smi.pumpAll()
				if i in [1, 2, ]:
					smi.expect_mockCall(mock_BeepCommand_run)
				if i in [3, ]:
					smi.expect_mockCall(mock_WaveFileCommand_run)

	def test2(self):
		"""Text, end utterance, text.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [
				u"This is the first utterance", EndUtteranceCommand(), u"And this is the second"
			])
		"""
		smi = SpeechManagerInteractions(self)
		sequence = [
			u"This is the first utterance",
			smi.create_EndUtteranceCommand(expectedToBecomeIndex=1),
			u"And this is the second",
			smi.create_ExpectedIndex(expectedToBecomeIndex=2),
		]
		with smi.expectation():
			smi.speak(sequence)
			smi.expect_synthSpeak(0)
		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_synthSpeak(1)

	def test3(self):
		"""Change pitch, text, end utterance, text.
			wx.CallLater(500, speech.speak, [
				PitchCommand(offset=50),
				u"This is the first utterance in a higher pitch",
				EndUtteranceCommand(), u"And this is the second"
			])
		Expected: All should be higher pitch.
		"""
		smi = SpeechManagerInteractions(self)
		sequence = [
			PitchCommand(offset=50),
			u"This is the first utterance in a higher pitch",
			# EndUtterance effectively splits the sequence, two sequence numbers are returned
			# from smi.speak for ease of adding expectations.
			smi.create_EndUtteranceCommand(expectedToBecomeIndex=1),
			smi.create_ExpectedProsodyCommand(PitchCommand(offset=50)),
			u"And this is the second",
			smi.create_ExpectedIndex(expectedToBecomeIndex=2),
		]
		with smi.expectation():
			smi.speak(sequence)
			smi.expect_synthSpeak(0)
		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_synthSpeak(1)

	def test_6_SPRI(self):
		"""Two utterances at SPRI_NORMAL in same sequence. Two separate sequences at SPRI_NEXT.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [
				u"1 2 3 ", u"4 5", EndUtteranceCommand(), u"16 17 18 19 20"
			])
			wx.CallLater(510, speech.speak, [u"6 7 8 9 10"], priority=speech.SPRI_NEXT)
			wx.CallLater(520, speech.speak, [u"11 12 13 14 15"], priority=speech.SPRI_NEXT)
		Expected result: numbers in order from 1 to 20.
		"""
		smi = SpeechManagerInteractions(self)
		with smi.expectation():
			first, last = smi.speak([
				"1 2 3 ", "4 5",
				# EndUtterance effectively splits the sequence, two sequence numbers are returned
				# for ease of adding expectations.
				smi.create_EndUtteranceCommand(expectedToBecomeIndex=1),
				"16 17 18 19 20",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2),
			])
			smi.expect_synthSpeak(first)

		interrupt1 = smi.speak(priority=speech.Spri.NEXT, seq=[
			"6 7 8 9 10",
			smi.create_ExpectedIndex(expectedToBecomeIndex=3)
		])
		interrupt2 = smi.speak(priority=speech.Spri.NEXT, seq=[
			"11 12 13 14 15",
			smi.create_ExpectedIndex(expectedToBecomeIndex=4)
		])

		with smi.expectation():
			smi.indexReached(1)  # endUtterance
			smi.pumpAll()
			smi.expect_synthSpeak(interrupt1)
		with smi.expectation():
			smi.indexReached(3)  # end of interrupt1
			smi.pumpAll()
			smi.expect_synthSpeak(interrupt2)
		with smi.expectation():
			smi.indexReached(4)  # end of interrupt2
			smi.pumpAll()
			smi.expect_synthSpeak(last)
		fin = smi.speak(["finally", smi.create_ExpectedIndex(expectedToBecomeIndex=5)])
		with smi.expectation():
			# End of second utterance in first speak call.
			# Note, indexes can be out of order because there are in different queues!
			smi.indexReached(2)
			smi.pumpAll()
			smi.expect_synthSpeak(fin)

	@patch.object(BeepCommand, 'run')
	def test_7_SPRI(self, mock_BeepCommand_run):
		"""Utterance at SPRI_NORMAL including a beep. Utterance at SPRI_NOW.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [
				u"Text before the beep ", BeepCommand(440, 10),
				u"text after the beep, text, text, text, text"
			])
			wx.CallLater(1500, speech.speak, [u"This is an interruption"], priority=speech.SPRI_NOW)
		Expected:
			Text before the beep, beep, Text after..., This is an interruption., Text after the beep, text...
		"""
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring(mock_BeepCommand_run)
		_beepCommand = smi.create_BeepCommand

		toBeInterrupted = [
			"Text before the beep ",
			_beepCommand(440, 10, expectedToBecomeIndex=1),
			"text after the beep, text, text, text, text",
			smi.create_ExpectedIndex(expectedToBecomeIndex=2)
		]
		postInterruption = toBeInterrupted[2:]
		with smi.expectation():
			first = smi.speak(toBeInterrupted)
			smi.expect_synthSpeak(first)

		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_mockCall(mock_BeepCommand_run)

		with smi.expectation():
			interrupt = smi.speak(
				priority=speech.Spri.NOW,
				seq=["This is an interruption", smi.create_ExpectedIndex(expectedToBecomeIndex=3)]
			)
			smi.expect_synthCancel()
			smi.expect_synthSpeak(interrupt)

		with smi.expectation():
			smi.indexReached(3)
			smi.pumpAll()
			smi.expect_synthSpeak(
				sequence=postInterruption
			)

	def test_8_SPRI(self):
		"""Utterance with two sequences at SPRI_NOW. Utterance at SPRI_NOW.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [u"First ", u"utterance"], priority=speech.SPRI_NOW)
			wx.CallLater(510, speech.speak, [u"Second ", u"utterance"], priority=speech.SPRI_NOW)
		Expected result: First utterance, second utterance
		"""
		smi = SpeechManagerInteractions(self)
		with smi.expectation():
			first = smi.speak(priority=speech.Spri.NOW, seq=[
				"First ", "utterance", smi.create_ExpectedIndex(expectedToBecomeIndex=1)
			])
			smi.expect_synthSpeak(first)
			smi.expect_synthCancel()

		with smi.expectation():
			second = smi.speak(priority=speech.Spri.NOW, seq=[
				"Second ", "utterance", smi.create_ExpectedIndex(expectedToBecomeIndex=2)
			])

		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_synthSpeak(second)

	def test_9_SPRI(self):
		"""Utterance with two sequences at SPRI_NOW. Utterance at SPRI_NEXT.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [u"First ", u"utterance"], priority=speech.SPRI_NOW)
			wx.CallLater(501, speech.speak, [u"Second ", u"utterance"], priority=speech.SPRI_NEXT)
		Expected result: First utterance, second utterance
		"""
		smi = SpeechManagerInteractions(self)
		with smi.expectation():
			first = smi.speak(priority=speech.Spri.NOW, seq=[
				"First ", "utterance", smi.create_ExpectedIndex(expectedToBecomeIndex=1)
			])
			smi.expect_synthSpeak(first)
			smi.expect_synthCancel()

		with smi.expectation():
			second = smi.speak(priority=speech.Spri.NEXT, seq=[
				"Second ", "utterance", smi.create_ExpectedIndex(expectedToBecomeIndex=2)
			])

		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_synthSpeak(second)

	@patch.object(BeepCommand, 'run')
	def test_13_SPRI_interruptBeforeIndexReached(self, mock_BeepCommand_run):
		"""The same as the other test_13, but the first index is not reached before the interruption.
		In this cases speech manager is expected to finish the first utterance before interrupting.
		"""
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([mock_BeepCommand_run])
		firstSeq = [
			PitchCommand(offset=100),
			"Text before the beep ",
			smi.create_BeepCommand(440, 10, expectedToBecomeIndex=1),
			"text after the beep, text, text, text, text",
			smi.create_ExpectedIndex(expectedToBecomeIndex=2),
		]
		with smi.expectation():
			first = smi.speak(priority=speech.Spri.NORMAL, seq=firstSeq)
			smi.expect_synthSpeak(first)

		with smi.expectation():
			interrupt = smi.speak(
				priority=speech.Spri.NOW,
				seq=[
					"This is an interruption",
					smi.create_ExpectedIndex(expectedToBecomeIndex=3)
				]
			)
			smi.expect_synthSpeak(interrupt)
			smi.expect_synthCancel()

		with smi.expectation():
			# the first sequence was canceled, after reaching the end of the interruption sequence expect to return
			# to the first sequence. Note that it speaks the whole first utterance again.
			smi.indexReached(3)
			smi.pumpAll()
			smi.expect_synthSpeak(first)

	@patch.object(BeepCommand, 'run')
	def test_13_SPRI_interruptAfterIndexReached(self, mock_BeepCommand_run):
		"""Utterance at SPRI_NORMAL including a pitch change and beep. Utterance at SPRI_NOW.
		Manual Test (in NVDA python console):
			wx.CallLater(500, speech.speak, [
			PitchCommand(offset=100),
			u"Text before the beep ",
			BeepCommand(440, 10),
			u"text after the beep, text, text, text, text"
			])
			wx.CallLater(1500, speech.speak, [u"This is an interruption"], priority=speech.SPRI_NOW)
		Expected: Text speaks with higher pitch, beep, text gets interrupted,
			interruption speaks with normal pitch, text after the beep speaks again with higher pitch
		"""
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([mock_BeepCommand_run])

		firstSeq = [
			PitchCommand(offset=100),
			"Text before the beep ",
			smi.create_BeepCommand(440, 10, expectedToBecomeIndex=1),
			"text after the beep, text, text, text, text",
			smi.create_ExpectedIndex(expectedToBecomeIndex=2),
		]
		with smi.expectation():
			first = smi.speak(priority=speech.Spri.NORMAL, seq=firstSeq)
			smi.expect_synthSpeak(first)

		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
			smi.expect_mockCall(mock_BeepCommand_run)

		with smi.expectation():
			interrupt = smi.speak(priority=speech.Spri.NOW, seq=[
				"This is an interruption",
				smi.create_ExpectedIndex(expectedToBecomeIndex=3)
			])
			smi.expect_synthSpeak(interrupt)
			smi.expect_synthCancel()

		with smi.expectation():
			smi.indexReached(3)
			smi.pumpAll()
			resume = [
				smi.create_ExpectedProsodyCommand(firstSeq[0]),
				*firstSeq[3:]
			]
			smi.expect_synthSpeak(sequence=resume)

	class FakeProfileTrigger(config.ProfileTrigger):
		spec = "fakeProfileTriggerSpec"

		def __init__(self, name):
			self.spec = f"{name} - {self.spec}"
			self.enter = mock.Mock(name=f"enter {self.spec}")
			self.exit = mock.Mock(name=f"exit {self.spec}")

		@property
		def hasProfile(self):
			return True

	def test_4_profiles(self):
		"""Text, pitch, text, enter profile1, enter profile2, text, exit profile1, text.
		Manual Test (in NVDA python console):
			from speech import sayAll, appModuleHandler
			t1 = sayAll.SayAllProfileTrigger()
			t2 = appModuleHandler.AppProfileTrigger("notepad")
			wx.CallLater(500, speech.speak, [
				u"Testing testing ", PitchCommand(offset=100), "1 2 3 4",
				ConfigProfileTriggerCommand(t1, True), ConfigProfileTriggerCommand(t2, True),
				u"5 6 7 8", ConfigProfileTriggerCommand(t1, False), u"9 10 11 12"
			])
		Expected:
			All text after 1 2 3 4 should be higher pitch.
			5 6 7 8 should have profile 1 and 2.
			9 10 11 12 should be just profile 2.
		"""
		t1 = InitialDevelopmentTests.FakeProfileTrigger("t1")
		t2 = InitialDevelopmentTests.FakeProfileTrigger("t2")
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([t1.enter, t1.exit, t2.enter, t2.exit])
		seq = [
			"Testing testing ",
			PitchCommand(offset=100),
			"1 2 3 4",
			smi.create_ExpectedIndex(1),
			# The preceeding index is expected,
			# as the following profile trigger commands will cause the utterance to be split here.
			ConfigProfileTriggerCommand(t1, True),
			ConfigProfileTriggerCommand(t2, True),
			"5 6 7 8",
			smi.create_ExpectedIndex(2),
			# The preceeding index is expected,
			# as the following profile trigger commands will cause the utterance to be split here.
			ConfigProfileTriggerCommand(t1, False),
			"9 10 11 12"
		]
		with smi.expectation():
			smi.speak(seq)
			smi.expect_synthSpeak(sequence=seq[:4])
		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_mockCall(t1.enter)
			smi.expect_synthCancel()
			smi.expect_mockCall(t2.enter)
			smi.expect_synthSpeak(sequence=[
				seq[1],  # PitchCommand
				'5 6 7 8',
				seq[7],  # IndexCommand index=2 (due to a  ConfigProfileTriggerCommand following it)
			])

		with smi.expectation():
			smi.indexReached(2)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_synthSpeak(sequence=[
				seq[1],  # PitchCommand
				'9 10 11 12',
				smi.create_ExpectedIndex(expectedToBecomeIndex=3)
			])
			smi.expect_mockCall(t1.exit)

		with smi.expectation():
			smi.indexReached(3)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_mockCall(t2.exit)

	def test_5_profiles(self):
		"""Enter profile, text, exit profile.
		Manual Test (in NVDA python console):
			from speech import sayAll
			trigger = sayAll.SayAllProfileTrigger()
			wx.CallLater(500, speech.speak, [
				ConfigProfileTriggerCommand(trigger, True), u"5 6 7 8",
				ConfigProfileTriggerCommand(trigger, False),
				u"9 10 11 12"
			])
		Expected: 5 6 7 8 in different profile, 9 10 11 12 with base config.
		"""
		t1 = InitialDevelopmentTests.FakeProfileTrigger("t1")
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([t1.enter, t1.exit])
		seq = [
			ConfigProfileTriggerCommand(t1, True),
			"5 6 7 8",
			smi.create_ConfigProfileTriggerCommand(t1, False, expectedToBecomeIndex=1),
			"9 10 11 12",
		]
		with smi.expectation():
			smi.speak(seq)
			smi.expect_synthSpeak(sequence=seq[1:3])
			smi.expect_synthCancel()
			smi.expect_mockCall(t1.enter)
		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthSpeak(sequence=['9 10 11 12', smi.create_ExpectedIndex(expectedToBecomeIndex=2)])
			smi.expect_synthCancel()
			smi.expect_mockCall(t1.exit)
		with smi.expectation():
			smi.indexReached(2)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()

	def test_10_SPRI_profiles(self):
		"""Utterance at SPRI_NORMAL. Utterance at SPRI_NOW with profile switch.
		Manual Test (in NVDA python console):
			from speech import sayAll;
			trigger = sayAll.SayAllProfileTrigger();
			wx.CallLater(500, speech.speak, [
				ConfigProfileTriggerCommand(trigger, True),
				u"This is a normal utterance with a different profile"
			])
			wx.CallLater(1000, speech.speak, [u"This is an interruption"], priority=speech.SPRI_NOW)
		Expected: Normal speaks but gets interrupted, interruption with different profile, normal speaks again
		"""
		t1 = InitialDevelopmentTests.FakeProfileTrigger("t1")
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([t1.enter, t1.exit])

		with smi.expectation():
			first = smi.speak([
				"This is a normal utterance, text, text,",
				smi.create_ExpectedIndex(expectedToBecomeIndex=1)
			])
			smi.expect_synthSpeak(first)

		# before the first utterance can finish, it is interrupted.
		with smi.expectation():
			interrupt = [
				ConfigProfileTriggerCommand(t1, True),
				"This is an interruption with a different profile",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2)
			]
			smi.speak(priority=speech.Spri.NOW, seq=interrupt)
			smi.expect_synthCancel()  # twice ??
			smi.expect_synthCancel()
			smi.expect_mockCall(t1.enter)
			smi.expect_synthSpeak(sequence=interrupt[1:])

		with smi.expectation():
			smi.indexReached(2)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_synthSpeak(first)
			smi.expect_mockCall(t1.exit)

	def test_11_SPRI_Profile(self):
		"""Utterance at SPRI_NORMAL with profile switch. Utterance at SPRI_NOW.
		Manual Test (in NVDA python console):
			from speech import sayAll
			trigger = sayAll.SayAllProfileTrigger()
			wx.CallLater(500, speech.speak, [
				ConfigProfileTriggerCommand(trigger, True),
				u"This is a normal utterance with a different profile"
				])
			wx.CallLater(1000, speech.speak, [u"This is an interruption"], priority=speech.SPRI_NOW)
		Expected:
			Normal speaks with different profile but gets interrupted, interruption speaks with base config,
			normal speaks again with different profile
		"""

		t1 = InitialDevelopmentTests.FakeProfileTrigger("t1")
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([t1.enter, t1.exit])
		with smi.expectation():
			first = [
				ConfigProfileTriggerCommand(t1, True),
				"This is a normal utterance with a different profile",
				smi.create_ExpectedIndex(expectedToBecomeIndex=1)
			]
			smi.speak(first)
			smi.expect_synthSpeak(sequence=first[1:])
			smi.expect_mockCall(t1.enter)
			smi.expect_synthCancel()

		# Before the first index is reached, there is an interruption
		with smi.expectation():
			interrupt = [
				"This is an interruption",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2)
			]
			interruptIndex = smi.speak(priority=speech.Spri.NOW, seq=interrupt)
			smi.expect_synthCancel()  # 2 calls ??
			smi.expect_synthCancel()
			smi.expect_synthSpeak(interruptIndex)
			smi.expect_mockCall(t1.exit)

		# Reach the end of the interruption speech sequence
		with smi.expectation():
			smi.indexReached(2)
			smi.pumpAll()
		# Once done speaking, expect to return to the lower priority speech, including swapping back to the
		# initial profile trigger.
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_synthSpeak(sequence=first[1:])
			smi.expect_mockCall(t1.enter)

		# Reach the end of the lower priority (initial) speech
		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_mockCall(t1.exit)

	def test_12_SPRI_profile(self):
		"""Utterance at SPRI_NORMAL with profile 1. Utterance at SPRI_NOW with profile 2.
		Manual Test (in NVDA python console):
			from speech import sayAll, appModuleHandler
			t1 = sayAll.SayAllProfileTrigger()
			t2 = appModuleHandler.AppProfileTrigger("notepad")
			wx.CallLater(500, speech.speak, [
				ConfigProfileTriggerCommand(t1, True),
				u"This is a normal utterance with profile 1"
			])
			wx.CallLater(1000, speech.speak, [
				ConfigProfileTriggerCommand(t2, True),
				u"This is an interruption with profile 2"
			], priority=speech.SPRI_NOW)
		Expected: Normal speaks with profile 1 but gets interrupted, interruption speaks with profile 2,
		normal speaks again with profile 1
		"""
		t1 = InitialDevelopmentTests.FakeProfileTrigger("t1")
		t2 = InitialDevelopmentTests.FakeProfileTrigger("t2")
		smi = SpeechManagerInteractions(self)
		smi.addMockCallMonitoring([t1.enter, t1.exit, t2.enter, t2.exit])
		with smi.expectation():
			first = [
				ConfigProfileTriggerCommand(t1, True),
				"This is a normal utterance with profile 1",
				smi.create_ExpectedIndex(expectedToBecomeIndex=1)
			]
			smi.speak(first)
			smi.expect_synthSpeak(sequence=first[1:])
			smi.expect_mockCall(t1.enter)
			smi.expect_synthCancel()

		# Before the first index is reached, there is an interruption
		with smi.expectation():
			interrupt = [
				ConfigProfileTriggerCommand(t2, True),
				"This is an interruption with profile 2",
				smi.create_ExpectedIndex(expectedToBecomeIndex=2)
			]
			smi.speak(priority=speech.Spri.NOW, seq=interrupt)
			smi.expect_synthCancel()  # 3 calls ??
			smi.expect_synthCancel()
			smi.expect_synthCancel()
			smi.expect_synthSpeak(sequence=interrupt[1:])
			smi.expect_mockCall(t1.exit)
			smi.expect_mockCall(t2.enter)

		# Reach the end of the interruption speech sequence
		with smi.expectation():
			smi.indexReached(2)
			smi.pumpAll()
		# Once done speaking, expect to return to the lower priority speech, including swapping back to the
		# initial profile trigger.
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_synthCancel()
			smi.expect_synthSpeak(sequence=first[1:])
			smi.expect_mockCall(t2.exit)
			smi.expect_mockCall(t1.enter)

		# Reach the end of the lower priority (initial) speech
		with smi.expectation():
			smi.indexReached(1)
			smi.pumpAll()
		with smi.expectation():
			smi.doneSpeaking()
			smi.pumpAll()
			smi.expect_synthCancel()
			smi.expect_mockCall(t1.exit)


class InitialDevelopmentTests_withCancellableSpeechEnabled(InitialDevelopmentTests):
	"""Note, while cancellable speech is configurable test with and without it enabled."""
	def setUp(self):
		super().setUp()
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 1  # yes


class RegressionTests(unittest.TestCase):
	"""Tests to prevent regressions after issues are fixed.
	"""

	def test_redundantSequenceAfterEndUtterance(self):
		"""
		Tests that redundant param change and index commands are not emitted as an extra utterance
		when the preceeding utterance contained param change commands and an EndUtterance command.
		See PR #11651
		E.g. speaking a character.
		"""
		smi = SpeechManagerInteractions(self)
		seq = [
			CharacterModeCommand(True),
			"a",
			smi.create_ExpectedIndex(1),
			EndUtteranceCommand(),
		]
		with smi.expectation():
			smi.speak(seq)
			# synth should receive the characterMode, the letter 'a' and an index command.
			smi.expect_synthSpeak(sequence=seq[:-1])
		with smi.expectation():
			# Previously, this would result in synth.speak receiving
			# a call with sequence:
			# [CharacterModeCommand(True), IndexCommand(2)]
			# This is a problem because it includes an index command but no speech.
			# This is inefficient, and also some SAPI5 synths such as Ivona will not
			# notify of this bookmark.
			smi.indexReached(1)
			smi.doneSpeaking()
			smi.pumpAll()

	def test_nonSpokenCharacter(self):
		"""Test for fix to GH#11752 - NVDA Freeze with unicode value U+000B
		Actually, the speech manager receives an empty string for the character U+000B. NVDA
		does not have a mapping for this character.
		It is questionable whether we should send anything to the synth when there is no content, however
		what constitutes 'content' is currently not easy to define.
		"""
		smi = SpeechManagerInteractions(self)

		speechSequence = [
			CharacterModeCommand(True),
			'',
			smi.create_EndUtteranceCommand(expectedToBecomeIndex=1)
		]
		with smi.expectation():
			seqIndexes = smi.speak(speechSequence)
			smi.expect_synthSpeak(seqIndexes)


class RegressionTests_withCancellableSpeechEnabled(RegressionTests):
	"""Note, while cancellable speech is configurable test with and without it enabled."""
	def setUp(self):
		super().setUp()
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 1  # yes
