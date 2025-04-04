# -*- coding: UTF-8 -*-
# tests/unit/test_textInfos.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the textInfos module, its submodules and classes."""

import unittest
from .textProvider import BasicTextProvider, MockBlackBoxTextInfo
import textInfos
from textInfos.offsets import Offsets
import textUtils


class TestCharacterOffsets(unittest.TestCase):
	"""
	Tests for textInfos.offsets.OffsetsTextInfo for its ability to deal with
	UTF-16 surrogate characters (i.e. whether a surrogate pair is treated as one character).
	These tests are also implicit tests for the textUtils module,
	as its logic is used for character offset calculation in wide character strings.
	"""

	def test_nonSurrogateForward(self):
		obj = BasicTextProvider(text="abc")
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at a
		self.assertEqual(ti.offsets, (0, 1))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at b
		self.assertEqual(ti.offsets, (1, 2))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at c
		self.assertEqual(ti.offsets, (2, 3))  # One offset

	def test_nonSurrogateBackward(self):
		obj = BasicTextProvider(text="abc")
		ti = obj.makeTextInfo(Offsets(2, 2))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at c
		self.assertEqual(ti.offsets, (2, 3))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at b
		self.assertEqual(ti.offsets, (1, 2))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at a
		self.assertEqual(ti.offsets, (0, 1))  # One offset

	def test_surrogatePairsForward(self):
		obj = BasicTextProvider(text="\U0001f926\U0001f60a\U0001f44d")  # 🤦😊👍
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🤦
		self.assertEqual(ti.offsets, (0, 2))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 😊
		self.assertEqual(ti.offsets, (2, 4))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 👍
		self.assertEqual(ti.offsets, (4, 6))  # Two offsets

	def test_surrogatePairsBackward(self):
		obj = BasicTextProvider(text="\U0001f926\U0001f60a\U0001f44d")  # 🤦😊👍
		ti = obj.makeTextInfo(Offsets(5, 5))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 👍
		self.assertEqual(ti.offsets, (4, 6))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 😊
		self.assertEqual(ti.offsets, (2, 4))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🤦
		self.assertEqual(ti.offsets, (0, 2))  # Two offsets

	def test_mixedSurrogatePairsAndNonSurrogatesForward(self):
		obj = BasicTextProvider(text="a\U0001f926b")  # a🤦b
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at a
		self.assertEqual(ti.offsets, (0, 1))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🤦
		self.assertEqual(ti.offsets, (1, 3))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at c
		self.assertEqual(ti.offsets, (3, 4))  # One offset

	def test_mixedSurrogatePairsAndNonSurrogatesBackward(self):
		obj = BasicTextProvider(text="a\U0001f926b")  # a🤦b
		ti = obj.makeTextInfo(Offsets(3, 3))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at c
		self.assertEqual(ti.offsets, (3, 4))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🤦
		self.assertEqual(ti.offsets, (1, 3))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at a
		self.assertEqual(ti.offsets, (0, 1))  # One offset

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogatesForward(self):
		"""
		Tests surrogate pairs, non surrogates as well as
		single surrogate characters (i.e. incomplete pairs)
		"""
		obj = BasicTextProvider(text="a\ud83e\U0001f926\udd26b")
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at a
		self.assertEqual(ti.offsets, (0, 1))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🠀
		self.assertEqual(ti.offsets, (1, 2))  # Leading surrogate without a trailing surrogate
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🤦
		self.assertEqual(ti.offsets, (2, 4))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 񙠀
		self.assertEqual(ti.offsets, (4, 5))  # Trailing surrogate without a leading surrogate.
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at c
		self.assertEqual(ti.offsets, (5, 6))  # One offset

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogatesBackward(self):
		obj = BasicTextProvider(text="a\ud83e\U0001f926\udd26b")
		ti = obj.makeTextInfo(Offsets(5, 5))
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at c
		self.assertEqual(ti.offsets, (5, 6))  # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 񙠀
		self.assertEqual(ti.offsets, (4, 5))  # Trailing surrogate without a leading surrogate.
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🤦
		self.assertEqual(ti.offsets, (2, 4))  # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at 🠀
		self.assertEqual(ti.offsets, (1, 2))  # Leading surrogate without a trailing surrogate
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER)  # Range at a
		self.assertEqual(ti.offsets, (0, 1))  # One offset


class TestEndpoints(unittest.TestCase):
	def test_TextInfoEndpoint_largerAndSmaller(self):
		obj = BasicTextProvider(text="abcdef")
		ti = obj.makeTextInfo(Offsets(0, 2))
		smaller = ti.start
		larger = ti.end
		self.assertTrue(smaller < larger)
		self.assertFalse(larger < smaller)
		self.assertTrue(smaller <= larger)
		self.assertFalse(larger <= smaller)
		self.assertFalse(smaller >= larger)
		self.assertTrue(larger >= smaller)
		self.assertFalse(smaller > larger)
		self.assertTrue(larger > smaller)
		self.assertTrue(smaller != larger)
		self.assertTrue(larger != smaller)

	def test_TextInfoEndpoint_equal(self):
		obj = BasicTextProvider(text="abcdef")
		ti = obj.makeTextInfo(Offsets(1, 1))
		self.assertTrue(ti.start == ti.end)
		self.assertFalse(ti.start != ti.end)
		self.assertFalse(ti.start < ti.end)
		self.assertTrue(ti.start <= ti.end)
		self.assertTrue(ti.start >= ti.end)
		self.assertFalse(ti.start > ti.end)

	def test_setEndpoint(self):
		obj = BasicTextProvider(text="abcdef")
		ti1 = obj.makeTextInfo(Offsets(0, 2))
		ti2 = obj.makeTextInfo(Offsets(3, 5))
		ti1.end = ti2.end
		self.assertEqual((ti1._startOffset, ti1._endOffset), (0, 5))
		ti1.start = ti2.start
		self.assertEqual((ti1._startOffset, ti1._endOffset), (3, 5))
		ti1.end = ti2.start
		self.assertEqual((ti1._startOffset, ti1._endOffset), (3, 3))
		ti1.start = ti2.end
		self.assertEqual((ti1._startOffset, ti1._endOffset), (5, 5))


class TestMoveToCodepointOffsetInBlackBoxTextInfo(unittest.TestCase):
	THREE_CHARS = "012"
	TEN_CHARS = "0123456789"
	TWELVE_CHARS = "0123456789AB"
	LETTERS = "ABCDEFGHIJ"

	def runTestImpl(self, tokens: list[str], target: str):
		info = MockBlackBoxTextInfo(tokens)
		s = info.text
		i = s.index(target)
		j = i + len(target)
		startInfo = info.moveToCodepointOffset(i)
		endInfo = info.moveToCodepointOffset(j)
		resultInfo = startInfo.copy()
		resultInfo.setEndPoint(endInfo, "endToEnd")
		self.assertEqual(resultInfo.text, target)

	def test_simple(self):
		self.runTestImpl(list("Hello, world!"), "world")

	def test_tenCharactersLeft(self):
		self.runTestImpl([self.TEN_CHARS, "a", "b"], "a")

	def test_tenCharactersLeftRight(self):
		self.runTestImpl([self.TEN_CHARS, "a", self.TEN_CHARS], "a")

	def test_tenTwelveCharacters(self):
		self.runTestImpl([self.TEN_CHARS, "a", self.TWELVE_CHARS], "a")

	def test_TwelveTenCharacters(self):
		self.runTestImpl([self.TWELVE_CHARS, "a", self.TEN_CHARS], "a")

	def test_doubleLeftRecursion(self):
		self.runTestImpl([self.THREE_CHARS, "a", self.THREE_CHARS, self.THREE_CHARS], "a")

	def test_doubleRightRecursion(self):
		self.runTestImpl([self.THREE_CHARS, self.THREE_CHARS, self.THREE_CHARS, "a", self.THREE_CHARS], "a")

	def test_emptyCharacter(self):
		for c in self.LETTERS:
			self.runTestImpl(list(self.LETTERS) + [""], c)

	def test_emptyCharacterAtStart(self):
		for c in self.LETTERS:
			self.runTestImpl([""] + list(self.LETTERS), c)


class TestMoveToCodepointOffsetInOffsetsTextInfo(unittest.TestCase):
	encodings = [
		textUtils.UTF8_ENCODING,
		textUtils.WCHAR_ENCODING,
		"utf_32_le",
	]

	prefixes = [
		"",
		"a\n",
		"0123456789",
		"\r\n\r\n",
		"Привет ",
		"🤦😊👍",
	]

	def runTestImpl(self, prefix: str, text: str, target: str, encoding: str):
		self.assertTrue(target in text, "Invalid test case")
		prefixOffset = textUtils.getOffsetConverter(encoding)(prefix).encodedStringLength
		obj = BasicTextProvider(text=prefix + text, encoding=encoding)
		info = obj.makeTextInfo(Offsets(0, 0))
		info._startOffset = info._endOffset = prefixOffset
		storyInfo = info.copy()
		storyInfo.expand(textInfos.UNIT_STORY)
		info.setEndPoint(storyInfo, "endToEnd")
		s = info.text
		self.assertEqual(text, s)
		i = s.index(target)
		j = i + len(target)
		startInfo = info.moveToCodepointOffset(i)
		endInfo = info.moveToCodepointOffset(j)
		resultInfo = startInfo.copy()
		resultInfo.setEndPoint(endInfo, "endToEnd")
		self.assertEqual(resultInfo.text, target)

	def runTestAllEncodingsAllPrefixes(self, text: str, target: str):
		for encoding in self.encodings:
			for prefix in self.prefixes:
				self.runTestImpl(prefix, text, target, encoding)

	def test_simple(self):
		self.runTestAllEncodingsAllPrefixes("Hello, world!", "world")

	def test_russian(self):
		self.runTestAllEncodingsAllPrefixes("Привет, мир!", "мир")

	def test_chinese(self):
		self.runTestAllEncodingsAllPrefixes("前往另一种语言写成的文章。", "文")

	def test_smileyFace(self):
		self.runTestAllEncodingsAllPrefixes("😂0😂", "0")
