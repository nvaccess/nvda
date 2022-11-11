# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from documentNavigation import sentenceHelper


class TestSentenceHelper(unittest.TestCase):
	def test_westernSentenceEndings(self):
		first = "Test sentence number one, ending with a period."
		second = "Test sentence number two, ending with a question mark?"
		third = "Test sentence number three, ending with an exclamation point!"
		res = sentenceHelper._findEndOfSentence(first, 0)
		self.assertEqual(res, len(first))
		res = sentenceHelper._findEndOfSentence(second, 0)
		self.assertEqual(res, len(second))
		res = sentenceHelper._findEndOfSentence(third, 0)
		self.assertEqual(res, len(third))
		# test multiple sentences
		# one space between first and second, four spaces between second and third
		sentences = f"{first} {second}    {third}"
		secondOffset = len(first) + 1
		thirdOffset = secondOffset + len(second) + 4
		res = sentenceHelper._findEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)  # should return beginning of second sentence
		res = sentenceHelper._findEndOfSentence(sentences, secondOffset)
		self.assertEqual(res, thirdOffset)
		res = sentenceHelper._findEndOfSentence(sentences, thirdOffset)
		self.assertEqual(res, len(sentences))
		# test that we are not tripped up by period with no following space
		sentence = f"{first}{second}"
		res = sentenceHelper._findEndOfSentence(sentence, 0)
		self.assertEqual(res, len(sentence))
		# test that any combination of \r and \n after a sentence terminator is included as part of the sentence
		sentences = f"{first}\r\n\n\r{second}"
		secondOffset = len(first) + 4
		res = sentenceHelper._findEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)
		# test that tab(s) after sentence terminator is not supported
		trailingTab = "Invalid sentence termination.\t"
		res = sentenceHelper._findEndOfSentence(trailingTab, 0)
		self.assertIsNone(res)

	def test_FullWidthSentenceEndings(self):
		first = "Test sentence number one with period\u3002"
		second = "Test sentence number two with question mark\uff01"
		third = "Test sentence number three with exclamation point\uff1f"
		res = sentenceHelper._findEndOfSentence(first, 0)
		self.assertEqual(res, len(first))
		res = sentenceHelper._findEndOfSentence(second, 0)
		self.assertEqual(res, len(second))
		res = sentenceHelper._findEndOfSentence(third, 0)
		self.assertEqual(res, len(third))
		# test multiple sentences
		sentences = f"{first}{second}{third}"  # no spaces, following the rules of full widh terminators
		secondOffset = len(first)
		thirdOffset = secondOffset + len(second)
		res = sentenceHelper._findEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)
		res = sentenceHelper._findEndOfSentence(sentences, secondOffset)
		self.assertEqual(res, thirdOffset)
		res = sentenceHelper._findEndOfSentence(sentences, thirdOffset)
		self.assertEqual(res, len(sentences))
		# test that if there are spaces between sentences,
		# algorithm does not skip them as it does with western terminators
		sentences = f"{first} {second}"
		res = sentenceHelper._findEndOfSentence(sentences, 0)
		self.assertEqual(res, len(first))
		# test that if \r, \n, or any combination follows a sentence, these characters are included
		sentences = f"{first}\r\n\n\r{second}"
		secondOffset = len(first) + 4
		res = sentenceHelper._findEndOfSentence(sentences, 0)
		self.assertEqual(res, secondOffset)

	def test_notASentence(self):
		notASentence = "this is a string of words which is not a sentence"
		res = sentenceHelper._findEndOfSentence(notASentence, 0)
		self.assertIsNone(res)

	def test_emptyString(self):
		res = sentenceHelper._findEndOfSentence("", 0)
		self.assertIsNone(res)
