# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
import documentNavigation.sentenceHelper as sentenceHelper


class TestSentenceHelper(unittest.TestCase):
	def test_findEndOfSentence(self):
		westernSentences = (
			"Test sentence number one. "
			"Test sentence number two?       "
			"Test sentence number three!"
		)
		fullWidthSentences = (
			"Test sentence number one\u3002"
			"Test sentence number two\uff01"
			"Test sentence number three\uff1f"
		)
		notASentence = "not a terminated sentence"
		emptyString = ""
		res = sentenceHelper._findEndOfSentence(westernSentences, 0)
		self.assertEqual(res, 26)
		res = sentenceHelper._findEndOfSentence(westernSentences, res)  # find end of second sentence
		self.assertEqual(res, 58)
		res = sentenceHelper._findEndOfSentence(westernSentences, res)
		self.assertEqual(res, len(westernSentences))
		res = sentenceHelper._findEndOfSentence(fullWidthSentences, 0)
		self.assertEqual(res, 25)
		res = sentenceHelper._findEndOfSentence(fullWidthSentences, res)
		self.assertEqual(res, 50)
		res = sentenceHelper._findEndOfSentence(fullWidthSentences, res)
		self.assertEqual(res, len(fullWidthSentences))
		res = sentenceHelper._findEndOfSentence(notASentence, 0)
		self.assertIsNone(res)
		res = sentenceHelper._findEndOfSentence(emptyString, 0)
		self.assertIsNone(res)
