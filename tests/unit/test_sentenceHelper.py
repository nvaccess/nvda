# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from documentNavigation import sentenceHelper


class TestSentenceHelper(unittest.TestCase):
	def test_westernPeriod(self):
		sentence = "Test sentence number one, ending with a period."
		res = sentenceHelper._findNextEndOfSentence(sentence, 0)
		self.assertEqual(res, len(sentence))

	def test_westernQuestionMark(self):
		sentence = "Test sentence number two, ending with a question mark?"
		res = sentenceHelper._findNextEndOfSentence(sentence, 0)
		self.assertEqual(res, len(sentence))

	def test_westernExclamationPoint(self):
		sentence = "Test sentence number three, ending with an exclamation point!"
		res = sentenceHelper._findNextEndOfSentence(sentence, 0)
		self.assertEqual(res, len(sentence))

	def test_multipleWesternSentences(self):
		# Prove that one or more space characters are both required and included as part of the sentence.
		first = "Test sentence number one, ending with a period."
		second = "Test sentence number two, ending with a question mark?"
		third = "Test sentence number three, ending with an exclamation point!"
		# one space between first and second, four spaces between second and third
		sentences = f"{first} {second}    {third}"
		secondOffset = len(first) + 1
		thirdOffset = secondOffset + len(second) + 4
		res = sentenceHelper._findNextEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)  # should return beginning of second sentence
		res = sentenceHelper._findNextEndOfSentence(sentences, secondOffset)
		self.assertEqual(res, thirdOffset)
		res = sentenceHelper._findNextEndOfSentence(sentences, thirdOffset)
		self.assertEqual(res, len(sentences))

	def test_westernPeriodNoSpace(self):
		# test that we are not tripped up by period with no following space
		first = "Test sentence number one, ending with a period."
		second = "Test sentence number two, ending with a question mark?"
		sentence = f"{first}{second}"
		res = sentenceHelper._findNextEndOfSentence(sentence, 0)
		self.assertEqual(res, len(sentence))

	def test_westernSentencesWithLineTerminators(self):
		# With western terminators,
		# one or more of \r, \n, or space are required after the sentence terminator.
		# Prove that \r and \n are included as part of the sentence when present.
		first = "Test sentence number one, ending with a period."
		second = "Test sentence number two, ending with a question mark?"
		sentences = f"{first}\r\n\n\r{second}"
		secondOffset = len(first) + 4
		res = sentenceHelper._findNextEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)

	def test_westernSentenceTrailingTabNotSupported(self):
		trailingTab = "Invalid sentence termination.\t"
		res = sentenceHelper._findNextEndOfSentence(trailingTab, 0)
		self.assertIsNone(res)

	def test_fullWidthPeriod(self):
		sentenceWithPeriod = "Test sentence number one with period\u3002"
		res = sentenceHelper._findNextEndOfSentence(sentenceWithPeriod, 0)
		self.assertEqual(res, len(sentenceWithPeriod))

	def test_fullWidthQuestionMark(self):
		sentenceWithQuestionMark = "Test sentence number two with question mark\uff01"
		res = sentenceHelper._findNextEndOfSentence(sentenceWithQuestionMark, 0)
		self.assertEqual(res, len(sentenceWithQuestionMark))

	def test_fullWidthExclmationPoint(self):
		sentenceWithExclamationPoint = "Test sentence number three with exclamation point\uff1f"
		res = sentenceHelper._findNextEndOfSentence(sentenceWithExclamationPoint, 0)
		self.assertEqual(res, len(sentenceWithExclamationPoint))

	def test_multipleFullWidthSentences(self):
		first = "Test sentence number one with period\u3002"
		second = "Test sentence number two with question mark\uff01"
		third = "Test sentence number three with exclamation point\uff1f"
		sentences = f"{first}{second}{third}"  # no spaces, following the rules of full widh terminators
		secondOffset = len(first)
		thirdOffset = secondOffset + len(second)
		res = sentenceHelper._findNextEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)
		res = sentenceHelper._findNextEndOfSentence(sentences, secondOffset)
		self.assertEqual(res, thirdOffset)
		res = sentenceHelper._findNextEndOfSentence(sentences, thirdOffset)
		self.assertEqual(res, len(sentences))

	def test_fullWidthNoIncludeSpace(self):
		# Test that if there are spaces between sentences,
		# the algorithm does not skip them as it does with western terminators.
		first = "Test sentence number one with period\u3002"
		second = "Test sentence number two with question mark\uff01"
		sentences = f"{first} {second}"
		res = sentenceHelper._findNextEndOfSentence(sentences, 0)
		self.assertEqual(res, len(first))
		res = sentenceHelper._findNextEndOfSentence(sentences, res)
		self.assertEqual(res, len(sentences))

	def test_fullWidthSentencesWithLineTerminators(self):
		# In the case of full width sentence terminators,
		# any number of \r and \n are included if present after the terminator
		# in case synthesizers use the line break as an indicator to flush buffers, etc.
		# This behavior also increases the chance of the next sentence starting on a word.
		# Prove that if \r, \n, or any combination follows a sentence,
		# these characters are included as part of the sentence.
		first = "Test sentence number one with period\u3002"
		second = "Test sentence number two with question mark\uff01"
		sentences = f"{first}\r\n\n\r{second}"
		secondOffset = len(first) + 4
		res = sentenceHelper._findNextEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)

	def test_mixedWesternAndFullWidthSentences(self):
		western = "Test sentence number one, ending with a period."
		fullWidth = "Test sentence number one with period\u3002"
		combined = f"{western} {fullWidth}"
		res = sentenceHelper._findNextEndOfSentence(combined, 0)
		self.assertEqual(res, len(western) + 1)
		combined = f"{fullWidth}{western}"
		res = sentenceHelper._findNextEndOfSentence(combined, 0)
		self.assertEqual(res, len(fullWidth))

	def test_notASentence(self):
		notASentence = "this is a string of words which is not a sentence"
		res = sentenceHelper._findNextEndOfSentence(notASentence, 0)
		self.assertIsNone(res)

	def test_emptyString(self):
		res = sentenceHelper._findNextEndOfSentence("", 0)
		self.assertIsNone(res)
