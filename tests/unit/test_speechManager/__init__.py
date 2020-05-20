# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited

"""Unit tests for speech/manger module
"""
import unittest
import config
import speech
from .speechManagerTestHarness import (
	_IndexT,
	ExpectedIndex,
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

		# First sayAllHandler queues up a number of utterances.
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
			# no side effect, sayAllHandler does not send more speech until the final callback index is hit.
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
			# Todo: Fix SpeechManager. Should not be double speaking!
			smi.expect_synthSpeak([3, 3])  # smi.expect_synthSpeak(1) expected here

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
			# Todo: Fix SpeechManager. Should not be double speaking!
			smi.expect_synthSpeak([1, 1])  # smi.expect_synthSpeak(1) expected here


class SayAllEmulatedTests_withCancellableSpeechEnabled(SayAllEmulatedTests):
	"""Note, while cancellable speech is configurable test with and without it enabled."""
	def setUp(self):
		super().setUp()
		config.conf['featureFlag']['cancelExpiredFocusSpeech'] = 1  # yes
