#tests/unit/contentRecog/test_contentRecog.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the contentRecog module.
"""

import unittest
import contentRecog
import textInfos
from locationHelper import RectLTWH

class TestRecogImageInfo(unittest.TestCase):

	def test_noOffsetNoResize(self):
		info = contentRecog.RecogImageInfo(0, 0, 1000, 2000, 1)
		self.assertEqual(info.recogWidth, 1000)
		self.assertEqual(info.recogHeight, 2000)
		self.assertEqual(info.convertXToScreen(100), 100)
		self.assertEqual(info.convertYToScreen(200), 200)
		self.assertEqual(info.convertWidthToScreen(100), 100)
		self.assertEqual(info.convertHeightToScreen(200), 200)

	def test_withOffsetNoResize(self):
		info = contentRecog.RecogImageInfo(10, 20, 1000, 2000, 1)
		self.assertEqual(info.recogWidth, 1000)
		self.assertEqual(info.recogHeight, 2000)
		self.assertEqual(info.convertXToScreen(100), 110)
		self.assertEqual(info.convertYToScreen(200), 220)
		self.assertEqual(info.convertWidthToScreen(100), 100)
		self.assertEqual(info.convertHeightToScreen(200), 200)

	def test_noOffsetWithResize(self):
		info = contentRecog.RecogImageInfo(0, 0, 1000, 2000, 2)
		self.assertEqual(info.recogWidth, 2000)
		self.assertEqual(info.recogHeight, 4000)
		self.assertEqual(info.convertXToScreen(200), 100)
		self.assertEqual(info.convertYToScreen(400), 200)
		self.assertEqual(info.convertWidthToScreen(200), 100)
		self.assertEqual(info.convertHeightToScreen(400), 200)

	def test_withOffsetWithResize(self):
		info = contentRecog.RecogImageInfo(10, 20, 1000, 2000, 2)
		self.assertEqual(info.recogWidth, 2000)
		self.assertEqual(info.recogHeight, 4000)
		self.assertEqual(info.convertXToScreen(200), 110)
		self.assertEqual(info.convertYToScreen(400), 220)
		self.assertEqual(info.convertWidthToScreen(200), 100)
		self.assertEqual(info.convertHeightToScreen(400), 200)

class FakeNVDAObject(object):
	pass

class TestLinesWordsResult(unittest.TestCase):
	"""Tests that contentRecog.LinesWordsResult and contentRecog.LwrTextInfo
	correctly parse and process the JSON from a recognizer.
	"""
	DATA = [
		[
			{"x": 100, "y": 200, "width": 10, "height": 20, "text": "word1"},
			{"x": 110, "y": 200, "width": 10, "height": 20, "text": "word2"}
		],
		[
			{"x": 100, "y": 220, "width": 10, "height": 20, "text": "word3"},
			{"x": 110, "y": 220, "width": 10, "height": 20, "text": "word4"}
		]
	]
	TOP = 0
	BOTTOM = 23
	WORD1_OFFSETS = (0, 6)
	WORD1_SECOND = 1
	WORD1_LAST = 5
	WORD1_RECT = RectLTWH(100, 200, 10, 20)
	WORD2_START = 6
	WORD2_OFFSETS = (6, 12)
	WORD2_RECT = RectLTWH(110, 200, 10, 20)
	WORD3_OFFSETS = (12, 18)
	WORD3_START = 12
	WORD3_RECT = RectLTWH(100, 220, 10, 20)
	WORD4_OFFSETS = (18, 24)
	WORD4_RECT = RectLTWH(110, 220, 10, 20)
	LINE1_OFFSETS = (0, 12)
	LINE1_SECOND = 1
	LINE1_LAST = 11
	LINE2_OFFSETS = (12, 24)
	LINE2_START = 12

	def setUp(self):
		info = contentRecog.RecogImageInfo(0, 0, 1000, 2000, 1)
		self.result = contentRecog.LinesWordsResult(self.DATA, info)
		self.fakeObj = FakeNVDAObject()
		self.textInfo = self.result.makeTextInfo(self.fakeObj, textInfos.POSITION_FIRST)

	def test_text(self):
		self.assertEqual(self.result.text, "word1 word2\nword3 word4\n")

	def test_textLen(self):
		self.assertEqual(self.result.textLen, len(self.result.text))

	def test_wordOffsetsAtTop(self):
		actual = self.textInfo._getWordOffsets(self.TOP)
		self.assertEqual(actual, self.WORD1_OFFSETS)

	def test_wordOffsetsAtWord1SecondChar(self):
		actual = self.textInfo._getWordOffsets(self.WORD1_SECOND)
		self.assertEqual(actual, self.WORD1_OFFSETS)

	def test_wordOffsetsAtWord1LastChar(self):
		actual = self.textInfo._getWordOffsets(self.WORD1_LAST)
		self.assertEqual(actual, self.WORD1_OFFSETS)

	def test_wordOffsetsAtWord2Start(self):
		actual = self.textInfo._getWordOffsets(self.WORD2_START)
		self.assertEqual(actual, self.WORD2_OFFSETS)

	def test_wordOffsetsAtLine2Start(self):
		actual = self.textInfo._getWordOffsets(self.LINE2_START)
		self.assertEqual(actual, self.WORD3_OFFSETS)

	def test_wordOffsetsAtBottom(self):
		actual = self.textInfo._getWordOffsets(self.BOTTOM)
		self.assertEqual(actual, self.WORD4_OFFSETS)

	def test_lineOffsetsAtTop(self):
		actual = self.textInfo._getLineOffsets(self.TOP)
		self.assertEqual(actual, self.LINE1_OFFSETS)

	def test_lineOffsetsAtLine1SecondChar(self):
		actual = self.textInfo._getLineOffsets(self.LINE1_SECOND)
		self.assertEqual(actual, self.LINE1_OFFSETS)

	def test_lineOffsetsAtLine1LastChar(self):
		actual = self.textInfo._getLineOffsets(self.LINE1_LAST)
		self.assertEqual(actual, self.LINE1_OFFSETS)

	def test_lineOffsetsAtLine2Start(self):
		actual = self.textInfo._getLineOffsets(self.LINE2_START)
		self.assertEqual(actual, self.LINE2_OFFSETS)

	def test_lineOffsetsAtBottom(self):
		actual = self.textInfo._getLineOffsets(self.BOTTOM)
		self.assertEqual(actual, self.LINE2_OFFSETS)

	def test_boundingRectFromOffsetAtTop(self):
		actual = self.textInfo._getBoundingRectFromOffset(self.TOP)
		self.assertEqual(actual, self.WORD1_RECT)

	def test_boundingRectFromOffsetAtWord1SecondChar(self):
		actual = self.textInfo._getBoundingRectFromOffset(self.WORD1_SECOND)
		self.assertEqual(actual, self.WORD1_RECT)

	def test_boundingRectFromOffsetAtWord1LastChar(self):
		actual = self.textInfo._getBoundingRectFromOffset(self.WORD1_LAST)
		self.assertEqual(actual, self.WORD1_RECT)

	def test_boundingRectFromOffsetAtWord2Start(self):
		actual = self.textInfo._getBoundingRectFromOffset(self.WORD2_START)
		self.assertEqual(actual, self.WORD2_RECT)

	def test_boundingRectFromOffsetAtLine2Start(self):
		actual = self.textInfo._getBoundingRectFromOffset(self.LINE2_START)
		self.assertEqual(actual, self.WORD3_RECT)

	def test_boundingRectFromOffsetAtBottom(self):
		actual = self.textInfo._getBoundingRectFromOffset(self.BOTTOM)
		self.assertEqual(actual, self.WORD4_RECT)

	def test_copyTextInfo(self):
		copy = self.textInfo.copy()
		self.assertEqual(copy, self.textInfo)
