# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter, Wang Chong

"""Unit tests for the textUtils module."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from textUtils import UnicodeNormalizationOffsetConverter, WideStringOffsetConverter, WordSegmenter
from textUtils.uniscribe import splitAtCharacterBoundaries
from textUtils.segFlag import WordSegFlag

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


class TestUniscribeSplitAtCharacterBoundaries(unittest.TestCase):
	"""Several tests for the splitAtCharacterBoundaries function."""

	def _testHelper(self, input: str, expected: list[str]) -> None:
		self.assertSequenceEqual(list(splitAtCharacterBoundaries(input)), expected)

	def test_emptyString(self):
		self._testHelper("", [])

	def test_singleBasicCharacter(self):
		self._testHelper("a", ["a"])

	def test_multipleBasicCharacters(self):
		text = "Hello"
		self._testHelper(text, list(text))

	def test_longSentence(self):
		text = "This is a longer sentence, with punctuation!"
		self._testHelper(text, list(text))

	def test_emojis(self):
		text = "😊🤦👍"
		self._testHelper(text, list(text))

	def test_compositeCharacters(self):
		self._testHelper("áéĳ", ["á", "é", "ĳ"])

	def test_singleAcute(self):
		self._testHelper("\u0301", ["\u0301"])

	def test_acuteWithSpaceBefore(self):
		# The acute is bound to the space
		self._testHelper(" \u0301", [" \u0301"])

	def test_acuteWithSpaceAfter(self):
		self._testHelper("\u0301 ", ["\u0301", " "])

	def test_sentenceWithComposites(self):
		text = "Één eigenwĳze geïnteresseerde ĳsbeer"
		expected = [
			"É",
			"é",
			"n",
			" ",
			"e",
			"i",
			"g",
			"e",
			"n",
			"w",
			"ĳ",
			"z",
			"e",
			" ",
			"g",
			"e",
			"ï",
			"n",
			"t",
			"e",
			"r",
			"e",
			"s",
			"s",
			"e",
			"e",
			"r",
			"d",
			"e",
			" ",
			"ĳ",
			"s",
			"b",
			"e",
			"e",
			"r",
		]
		self._testHelper(text, expected)

	def test_hebrew(self):
		self._testHelper("בְּרֵאשִׁית", ["בְּ", "רֵ", "א", "שִׁ", "י", "ת"])


class TestChineseWordSegmentationInitialization(unittest.TestCase):
	def _makeMockJiebaDll(self):
		return SimpleNamespace(
			initJieba=Mock(return_value=True),
			calculateWordOffsets=Mock(),
			insertUserWord=Mock(),
			deleteUserWord=Mock(),
			find=Mock(),
			freeOffsets=Mock(),
		)

	def _setWordSegConfig(self, *, initForUnusedLang: bool):
		import config
		from config.featureFlag import FeatureFlag
		from config.featureFlagEnums import WordNavigationUnitFlag

		originalInitForUnusedLang = config.conf["documentNavigation"]["initWordSegForUnusedLang"]
		originalWordSegmentationStandard = config.conf["documentNavigation"]["wordSegmentationStandard"]
		config.conf["documentNavigation"]["initWordSegForUnusedLang"] = initForUnusedLang
		config.conf["documentNavigation"]["wordSegmentationStandard"] = FeatureFlag(
			WordNavigationUnitFlag.AUTO,
			behaviorOfDefault=WordNavigationUnitFlag.AUTO,
		)

		def restoreConfig():
			config.conf["documentNavigation"]["initWordSegForUnusedLang"] = originalInitForUnusedLang
			config.conf["documentNavigation"]["wordSegmentationStandard"] = originalWordSegmentationStandard

		return restoreConfig

	def test_doesNotInitializeForUnusedLanguageByDefault(self):
		from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy

		originalLib = ChineseWordSegmentationStrategy._lib
		restoreConfig = self._setWordSegConfig(initForUnusedLang=False)
		ChineseWordSegmentationStrategy._lib = None
		try:
			with (
				patch.object(ChineseWordSegmentationStrategy, "isUsingRelatedLanguage", return_value=False),
				patch("textUtils.wordSeg.wordSegStrategy.cdll.LoadLibrary") as loadLibrary,
			):
				ChineseWordSegmentationStrategy._initCppJieba()

			loadLibrary.assert_not_called()
		finally:
			ChineseWordSegmentationStrategy._lib = originalLib
			restoreConfig()

	def test_initializesForUnusedLanguageWhenConfigured(self):
		from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy

		mockDll = self._makeMockJiebaDll()
		originalLib = ChineseWordSegmentationStrategy._lib
		restoreConfig = self._setWordSegConfig(initForUnusedLang=True)
		ChineseWordSegmentationStrategy._lib = None
		try:
			with (
				patch.object(ChineseWordSegmentationStrategy, "isUsingRelatedLanguage", return_value=False),
				patch(
					"textUtils.wordSeg.wordSegStrategy.cdll.LoadLibrary",
					return_value=mockDll,
				) as loadLibrary,
			):
				ChineseWordSegmentationStrategy._initCppJieba()

			loadLibrary.assert_called_once()
			mockDll.initJieba.assert_called_once()
		finally:
			ChineseWordSegmentationStrategy._lib = originalLib
			restoreConfig()

	def test_forceInitStillInitializesForUnusedLanguage(self):
		from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy

		mockDll = self._makeMockJiebaDll()
		originalLib = ChineseWordSegmentationStrategy._lib
		restoreConfig = self._setWordSegConfig(initForUnusedLang=False)
		ChineseWordSegmentationStrategy._lib = None
		try:
			with (
				patch.object(ChineseWordSegmentationStrategy, "isUsingRelatedLanguage", return_value=False),
				patch(
					"textUtils.wordSeg.wordSegStrategy.cdll.LoadLibrary",
					return_value=mockDll,
				) as loadLibrary,
			):
				ChineseWordSegmentationStrategy._initCppJieba(forceInit=True)

			loadLibrary.assert_called_once()
			mockDll.initJieba.assert_called_once()
		finally:
			ChineseWordSegmentationStrategy._lib = originalLib
			restoreConfig()

	def test_initFailureDisablesCppJieba(self):
		from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy

		mockDll = self._makeMockJiebaDll()
		mockDll.initJieba.return_value = False
		originalLib = ChineseWordSegmentationStrategy._lib
		restoreConfig = self._setWordSegConfig(initForUnusedLang=False)
		ChineseWordSegmentationStrategy._lib = None
		try:
			with (
				patch.object(ChineseWordSegmentationStrategy, "isUsingRelatedLanguage", return_value=False),
				patch(
					"textUtils.wordSeg.wordSegStrategy.cdll.LoadLibrary",
					return_value=mockDll,
				) as loadLibrary,
				patch("textUtils.wordSeg.wordSegStrategy.log.debugWarning") as debugWarning,
			):
				ChineseWordSegmentationStrategy._initCppJieba(forceInit=True)

			loadLibrary.assert_called_once()
			mockDll.initJieba.assert_called_once()
			self.assertIsNone(ChineseWordSegmentationStrategy._lib)
			debugWarning.assert_called_once()
			self.assertIn("Failed to initialize cppjieba", debugWarning.call_args.args[0])
		finally:
			ChineseWordSegmentationStrategy._lib = originalLib
			restoreConfig()


class TestWordSegmenter(unittest.TestCase):
	"""Tests for the WordSegmenter class."""

	def test_basicLatin(self):
		text = "hello world"
		segmenter = WordSegmenter(text, wordSegFlag=WordSegFlag.UNISCRIBE)
		self.assertEqual(segmenter.getSegmentForOffset(0), (0, 6))
		self.assertEqual(segmenter.getSegmentForOffset(5), (0, 6))
		self.assertEqual(segmenter.getSegmentForOffset(6), (6, 11))
		self.assertEqual(segmenter.getSegmentForOffset(11), (6, 11))

	def test_chinese(self):
		text = "你好世界"

		from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy

		ChineseWordSegmentationStrategy._initCppJieba(forceInit=True)
		segmenter = WordSegmenter(text, wordSegFlag=WordSegFlag.CHINESE)
		self.assertEqual(segmenter.getSegmentForOffset(0), (0, 2))
		self.assertEqual(segmenter.getSegmentForOffset(1), (0, 2))
		self.assertEqual(segmenter.getSegmentForOffset(2), (2, 4))
		self.assertEqual(segmenter.getSegmentForOffset(3), (2, 4))
		self.assertEqual(segmenter.getSegmentForOffset(4), (2, 4))

	def test_chineseSegmentationFailureStoresEmptyWordEnds(self):
		from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy

		mockDll = SimpleNamespace(
			calculateWordOffsets=Mock(return_value=False),
			freeOffsets=Mock(),
		)
		originalLib = ChineseWordSegmentationStrategy._lib
		ChineseWordSegmentationStrategy._lib = mockDll
		try:
			strategy = ChineseWordSegmentationStrategy("你好世界")
			self.assertEqual(strategy.wordEnds, [])
			self.assertEqual(strategy.segmentedText(), "你好世界")
		finally:
			ChineseWordSegmentationStrategy._lib = originalLib


class TestWordSegInitialize(unittest.TestCase):
	def test_runsAllRegisteredInitializers(self):
		from textUtils import wordSeg
		from textUtils.wordSeg import wordSegStrategy

		calls = []

		def firstInitializer():
			calls.append("first")

		def secondInitializer():
			calls.append("second")

		class ImmediateThread:
			def __init__(self, target, args=None, kwargs=None, daemon=False):
				self.target = target
				self.args = () if args is None else args
				self.kwargs = {} if kwargs is None else kwargs
				self.daemon = daemon

			def start(self):
				self.target(*self.args, **self.kwargs)

		initializerList = [
			("missingModule", "firstInitializer", firstInitializer, (), {}),
			("missingModule", "secondInitializer", secondInitializer, (), {}),
		]
		with (
			patch.object(wordSegStrategy, "initializerList", initializerList),
			patch("threading.Thread", ImmediateThread),
		):
			wordSeg.initialize()

		self.assertEqual(calls, ["first", "second"])


class TestWordSegWithSeparatorOffsetConverter(unittest.TestCase):
	def _makeConverter(self):
		from textUtils.wordSeg.wordSegUtils import WordSegWithSeparatorOffsetConverter

		def segmentedText(sep, newSepIndex):
			newSepIndex.append(2)
			return "ab cd"

		with patch(
			"textUtils.wordSeg.wordSegUtils.WordSegmenter",
			return_value=SimpleNamespace(segmentedText=segmentedText),
		):
			return WordSegWithSeparatorOffsetConverter("abcd")

	def test_strToEncodedOffsetsMapsEndAndClampsOutOfRange(self):
		converter = self._makeConverter()

		self.assertEqual(converter.strToEncodedOffsets(-1), 0)
		self.assertEqual(converter.strToEncodedOffsets(2, 4), (3, 5))
		self.assertEqual(converter.strToEncodedOffsets(4), 5)
		self.assertEqual(converter.strToEncodedOffsets(5, 6), (5, 5))

	def test_strToEncodedOffsetsRaisesOnOutOfRangeWhenRequested(self):
		converter = self._makeConverter()

		with self.assertRaises(IndexError):
			converter.strToEncodedOffsets(5, raiseOnError=True)

	def test_encodedToStrOffsetsMapsEndAndClampsOutOfRange(self):
		converter = self._makeConverter()

		self.assertEqual(converter.encodedToStrOffsets(-1), 0)
		self.assertEqual(converter.encodedToStrOffsets(2), 2)
		self.assertEqual(converter.encodedToStrOffsets(2, 3), (2, 2))
		self.assertEqual(converter.encodedToStrOffsets(5), 4)
		self.assertEqual(converter.encodedToStrOffsets(6, 7), (4, 4))

	def test_encodedToStrOffsetsRaisesOnOutOfRangeWhenRequested(self):
		converter = self._makeConverter()

		with self.assertRaises(IndexError):
			converter.encodedToStrOffsets(6, raiseOnError=True)
