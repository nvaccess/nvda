# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited

"""Unit tests for speech/manger module
"""
import unittest
import config
from .speechManagerTestHarness import (
	ExpectedIndex,
	SpeechManagerInteractions,
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
