# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2024 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the textUtils module."""

import unittest

from textUtils import UnicodeNormalizationOffsetConverter, WideStringOffsetConverter

FACE_PALM = "\U0001f926"  # 🤦
SMILE = "\U0001f60a"  # 😊
THUMBS_UP = "\U0001f44d"  # 👍


class TestStrToWideOffsets(unittest.TestCase):
	"""
	Tests that ensure that offsets in a string are properly converted to wide string offsets.
	Every string offset for 32-bit unicode characters (e.g. emoji) take two offsets in a wide string representation.
	"""

	def test_nonSurrogate(self):
		converter = WideStringOffsetConverter(text="abc")
		self.assertEqual(converter.wideStringLength, 3)
		self.assertEqual(converter.strToWideOffsets(0, 0), (0, 0))
		self.assertEqual(converter.strToWideOffsets(0, 1), (0, 1))
		self.assertEqual(converter.strToWideOffsets(0, 2), (0, 2))
		self.assertEqual(converter.strToWideOffsets(0, 3), (0, 3))
		self.assertEqual(converter.strToWideOffsets(1, 1), (1, 1))
		self.assertEqual(converter.strToWideOffsets(1, 2), (1, 2))
		self.assertEqual(converter.strToWideOffsets(1, 3), (1, 3))
		self.assertEqual(converter.strToWideOffsets(2, 2), (2, 2))
		self.assertEqual(converter.strToWideOffsets(2, 3), (2, 3))
		self.assertEqual(converter.strToWideOffsets(3, 3), (3, 3))

	def test_surrogatePairs(self):
		converter = WideStringOffsetConverter(text=FACE_PALM + SMILE + THUMBS_UP)
		self.assertEqual(converter.wideStringLength, 6)
		self.assertEqual(converter.strToWideOffsets(0, 0), (0, 0))
		self.assertEqual(converter.strToWideOffsets(0, 1), (0, 2))
		self.assertEqual(converter.strToWideOffsets(0, 2), (0, 4))
		self.assertEqual(converter.strToWideOffsets(0, 3), (0, 6))
		self.assertEqual(converter.strToWideOffsets(1, 1), (2, 2))
		self.assertEqual(converter.strToWideOffsets(1, 2), (2, 4))
		self.assertEqual(converter.strToWideOffsets(1, 3), (2, 6))
		self.assertEqual(converter.strToWideOffsets(2, 2), (4, 4))
		self.assertEqual(converter.strToWideOffsets(2, 3), (4, 6))
		self.assertEqual(converter.strToWideOffsets(3, 3), (6, 6))

	def test_mixedSurrogatePairsAndNonSurrogates(self):
		converter = WideStringOffsetConverter(text="a" + FACE_PALM + "b")  # a🤦b
		self.assertEqual(converter.wideStringLength, 4)
		self.assertEqual(converter.strToWideOffsets(0, 0), (0, 0))
		self.assertEqual(converter.strToWideOffsets(0, 1), (0, 1))
		self.assertEqual(converter.strToWideOffsets(0, 2), (0, 3))
		self.assertEqual(converter.strToWideOffsets(0, 3), (0, 4))
		self.assertEqual(converter.strToWideOffsets(1, 1), (1, 1))
		self.assertEqual(converter.strToWideOffsets(1, 2), (1, 3))
		self.assertEqual(converter.strToWideOffsets(1, 3), (1, 4))
		self.assertEqual(converter.strToWideOffsets(2, 2), (3, 3))
		self.assertEqual(converter.strToWideOffsets(2, 3), (3, 4))
		self.assertEqual(converter.strToWideOffsets(3, 3), (4, 4))

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogates(self):
		"""
		Tests surrogate pairs, non surrogates as well as
		single surrogate characters (i.e. incomplete pairs)
		"""
		converter = WideStringOffsetConverter(text="a" + "\ud83e" + FACE_PALM + "\udd26" + "b")
		self.assertEqual(converter.wideStringLength, 6)
		self.assertEqual(converter.strToWideOffsets(0, 0), (0, 0))
		self.assertEqual(converter.strToWideOffsets(0, 1), (0, 1))
		self.assertEqual(converter.strToWideOffsets(0, 2), (0, 2))
		self.assertEqual(converter.strToWideOffsets(0, 3), (0, 4))
		self.assertEqual(converter.strToWideOffsets(0, 4), (0, 5))
		self.assertEqual(converter.strToWideOffsets(0, 5), (0, 6))
		self.assertEqual(converter.strToWideOffsets(1, 1), (1, 1))
		self.assertEqual(converter.strToWideOffsets(1, 2), (1, 2))
		self.assertEqual(converter.strToWideOffsets(1, 3), (1, 4))
		self.assertEqual(converter.strToWideOffsets(1, 4), (1, 5))
		self.assertEqual(converter.strToWideOffsets(1, 5), (1, 6))
		self.assertEqual(converter.strToWideOffsets(2, 2), (2, 2))
		self.assertEqual(converter.strToWideOffsets(2, 3), (2, 4))
		self.assertEqual(converter.strToWideOffsets(2, 4), (2, 5))
		self.assertEqual(converter.strToWideOffsets(2, 5), (2, 6))
		self.assertEqual(converter.strToWideOffsets(3, 3), (4, 4))
		self.assertEqual(converter.strToWideOffsets(3, 4), (4, 5))
		self.assertEqual(converter.strToWideOffsets(3, 5), (4, 6))
		self.assertEqual(converter.strToWideOffsets(4, 4), (5, 5))
		self.assertEqual(converter.strToWideOffsets(4, 5), (5, 6))
		self.assertEqual(converter.strToWideOffsets(5, 5), (6, 6))


class TestWideToStrOffsets(unittest.TestCase):
	"""
	Tests that ensure that offsets in a wide string are properly converted to str offsets.
	Every string offset for 32-bit unicode characters (e.g. emoji) take two offsets in a wide string representation.
	"""

	def test_nonSurrogate(self):
		converter = WideStringOffsetConverter(text="abc")
		self.assertEqual(converter.strLength, 3)
		self.assertEqual(converter.wideToStrOffsets(0, 0), (0, 0))
		self.assertEqual(converter.wideToStrOffsets(0, 1), (0, 1))
		self.assertEqual(converter.wideToStrOffsets(0, 2), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(0, 3), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(1, 1), (1, 1))
		self.assertEqual(converter.wideToStrOffsets(1, 2), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(1, 3), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(2, 2), (2, 2))
		self.assertEqual(converter.wideToStrOffsets(2, 3), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(3, 3), (3, 3))

	def test_surrogatePairs(self):
		converter = WideStringOffsetConverter(text=FACE_PALM + SMILE + THUMBS_UP)
		self.assertEqual(converter.strLength, 3)
		self.assertEqual(converter.wideToStrOffsets(0, 0), (0, 0))
		self.assertEqual(converter.wideToStrOffsets(0, 1), (0, 1))
		self.assertEqual(converter.wideToStrOffsets(0, 2), (0, 1))
		self.assertEqual(converter.wideToStrOffsets(0, 3), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(0, 4), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(0, 5), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(0, 6), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(1, 1), (0, 0))
		self.assertEqual(converter.wideToStrOffsets(1, 2), (0, 1))
		self.assertEqual(converter.wideToStrOffsets(1, 3), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(1, 4), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(1, 5), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(1, 6), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(2, 2), (1, 1))
		self.assertEqual(converter.wideToStrOffsets(2, 3), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(2, 4), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(2, 5), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(2, 6), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(3, 3), (1, 1))
		self.assertEqual(converter.wideToStrOffsets(3, 4), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(3, 5), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(3, 6), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(4, 4), (2, 2))
		self.assertEqual(converter.wideToStrOffsets(4, 5), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(4, 6), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(5, 5), (2, 2))
		self.assertEqual(converter.wideToStrOffsets(5, 6), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(6, 6), (3, 3))

	def test_mixedSurrogatePairsAndNonSurrogates(self):
		converter = WideStringOffsetConverter(text="a" + FACE_PALM + "b")  # a🤦b
		self.assertEqual(converter.strLength, 3)
		self.assertEqual(converter.wideToStrOffsets(0, 0), (0, 0))
		self.assertEqual(converter.wideToStrOffsets(0, 1), (0, 1))
		self.assertEqual(converter.wideToStrOffsets(0, 2), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(0, 3), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(0, 4), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(1, 1), (1, 1))
		self.assertEqual(converter.wideToStrOffsets(1, 2), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(1, 3), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(1, 4), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(2, 2), (1, 1))
		self.assertEqual(converter.wideToStrOffsets(2, 3), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(2, 4), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(3, 3), (2, 2))
		self.assertEqual(converter.wideToStrOffsets(3, 4), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(4, 4), (3, 3))

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogates(self):
		"""
		Tests surrogate pairs, non surrogates as well as
		single surrogate characters (i.e. incomplete pairs)
		"""
		converter = WideStringOffsetConverter(text="a" + "\ud83e" + FACE_PALM + "\udd26" + "b")
		self.assertEqual(converter.strLength, 5)
		self.assertEqual(converter.wideToStrOffsets(0, 0), (0, 0))
		self.assertEqual(converter.wideToStrOffsets(0, 1), (0, 1))
		self.assertEqual(converter.wideToStrOffsets(0, 2), (0, 2))
		self.assertEqual(converter.wideToStrOffsets(0, 3), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(0, 4), (0, 3))
		self.assertEqual(converter.wideToStrOffsets(0, 5), (0, 4))
		self.assertEqual(converter.wideToStrOffsets(0, 6), (0, 5))
		self.assertEqual(converter.wideToStrOffsets(1, 1), (1, 1))
		self.assertEqual(converter.wideToStrOffsets(1, 2), (1, 2))
		self.assertEqual(converter.wideToStrOffsets(1, 3), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(1, 4), (1, 3))
		self.assertEqual(converter.wideToStrOffsets(1, 5), (1, 4))
		self.assertEqual(converter.wideToStrOffsets(1, 6), (1, 5))
		self.assertEqual(converter.wideToStrOffsets(2, 2), (2, 2))
		self.assertEqual(converter.wideToStrOffsets(2, 3), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(2, 4), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(2, 5), (2, 4))
		self.assertEqual(converter.wideToStrOffsets(2, 6), (2, 5))
		self.assertEqual(converter.wideToStrOffsets(3, 3), (2, 2))
		self.assertEqual(converter.wideToStrOffsets(3, 4), (2, 3))
		self.assertEqual(converter.wideToStrOffsets(3, 5), (2, 4))
		self.assertEqual(converter.wideToStrOffsets(3, 6), (2, 5))
		self.assertEqual(converter.wideToStrOffsets(4, 4), (3, 3))
		self.assertEqual(converter.wideToStrOffsets(4, 5), (3, 4))
		self.assertEqual(converter.wideToStrOffsets(4, 6), (3, 5))
		self.assertEqual(converter.wideToStrOffsets(5, 5), (4, 4))
		self.assertEqual(converter.wideToStrOffsets(5, 6), (4, 5))
		self.assertEqual(converter.wideToStrOffsets(6, 6), (5, 5))


class TestEdgeCases(unittest.TestCase):
	"""
	Tests for edge cases, such as offsets out of range of a string,
	or end offsets less than start offsets.
	"""

	def test_wideToStrOffsets(self):
		converter = WideStringOffsetConverter(text="abc")
		self.assertEqual(converter.strLength, 3)
		self.assertEqual(
			converter.wideToStrOffsets(-1, 0, raiseOnError=False),
			(0, 0),
		)
		self.assertEqual(
			converter.wideToStrOffsets(0, 4, raiseOnError=False),
			(0, 3),
		)
		self.assertRaises(IndexError, converter.wideToStrOffsets, -1, 0, raiseOnError=True)
		self.assertRaises(IndexError, converter.wideToStrOffsets, 0, 4, raiseOnError=True)
		self.assertRaises(ValueError, converter.wideToStrOffsets, 1, 0)

	def test_strToWideOffsets(self):
		converter = WideStringOffsetConverter(text="abc")
		self.assertEqual(converter.wideStringLength, 3)
		self.assertEqual(
			converter.strToWideOffsets(-1, 0, raiseOnError=False),
			(0, 0),
		)
		self.assertEqual(
			converter.strToWideOffsets(0, 4, raiseOnError=False),
			(0, 3),
		)
		self.assertRaises(IndexError, converter.strToWideOffsets, -1, 0, raiseOnError=True)
		self.assertRaises(IndexError, converter.strToWideOffsets, 0, 4, raiseOnError=True)
		self.assertRaises(ValueError, converter.strToWideOffsets, 1, 0)


class TestUnicodeNormalizationOffsetConverter(unittest.TestCase):
	"""Tests for unicode normalization using the UnicodeNormalizationOffsetConverter"""

	def test_normalizedOffsetsSentence(self):
		text = "Één eigenwĳze geïnteresseerde ĳsbeer"
		converter = UnicodeNormalizationOffsetConverter(text, "NFKC")
		expectedStrToEncoded = (
			0,
			0,
			1,
			1,
			2,
			3,  # Één
			4,
			5,
			6,
			7,
			8,
			9,
			10,
			12,
			13,
			14,  # eigenwijze
			15,
			16,
			17,
			17,
			18,
			19,
			20,
			21,
			22,
			23,
			24,
			25,
			26,
			27,
			28,
			29,
			30,  # geïnteresseerde
			31,
			33,
			34,
			35,
			36,
			37,  # ijsbeer
		)
		self.assertSequenceEqual(converter.computedStrToEncodedOffsets, expectedStrToEncoded)
		expectedEncodedToStr = (
			0,
			2,
			4,
			5,  # Één
			6,
			7,
			8,
			9,
			10,
			11,
			12,
			12,
			13,
			14,
			15,  # eigenwijze
			16,
			17,
			18,
			20,
			21,
			22,
			23,
			24,
			25,
			26,
			27,
			28,
			29,
			30,
			31,
			32,  # geïnteresseerde
			33,
			33,
			34,
			35,
			36,
			37,
			38,  # ijsbeer
		)
		self.assertSequenceEqual(converter.computedEncodedToStrOffsets, expectedEncodedToStr)

	def test_normalizedOffsetsMixed(self):
		text = "Ééĳo\xa0 "
		converter = UnicodeNormalizationOffsetConverter(text, "NFKC")
		expectedStrToEncoded = (0, 0, 1, 1, 2, 4, 5, 6)
		self.assertSequenceEqual(converter.computedStrToEncodedOffsets, expectedStrToEncoded)
		expectedEncodedToStr = (0, 2, 4, 4, 5, 6, 7)
		self.assertSequenceEqual(converter.computedEncodedToStrOffsets, expectedEncodedToStr)

	def test_normalizedOffsetsDifferentOrder(self):
		text = "בְּרֵאשִׁית"
		converter = UnicodeNormalizationOffsetConverter(text, "NFKC")
		expectedStrToEncoded = (0, 2, 1, 3, 4, 5, 6, 8, 7, 9, 10)
		self.assertSequenceEqual(converter.computedStrToEncodedOffsets, expectedStrToEncoded)
		expectedEncodedToStr = (0, 2, 1, 3, 4, 5, 6, 8, 7, 9, 10)
		self.assertSequenceEqual(converter.computedEncodedToStrOffsets, expectedEncodedToStr)

	def test_normalizedOffsetsMixedSpaces(self):
		text = "\xa0 \xa0 \xa0"
		converter = UnicodeNormalizationOffsetConverter(text, "NFKC")
		expectedStrToEncoded = (0, 1, 2, 3, 4)
		self.assertSequenceEqual(converter.computedStrToEncodedOffsets, expectedStrToEncoded)
		expectedEncodedToStr = (0, 1, 2, 3, 4)
		self.assertSequenceEqual(converter.computedEncodedToStrOffsets, expectedEncodedToStr)

	def test_normalizedOffsetsMixedIJ(self):
		text = "ĳijĳijĳ"
		converter = UnicodeNormalizationOffsetConverter(text, "NFKC")
		expectedStrToEncoded = (0, 2, 3, 4, 6, 7, 8)
		self.assertSequenceEqual(converter.computedStrToEncodedOffsets, expectedStrToEncoded)
		expectedEncodedToStr = (0, 0, 1, 2, 3, 3, 4, 5, 6, 6)
		self.assertSequenceEqual(converter.computedEncodedToStrOffsets, expectedEncodedToStr)
