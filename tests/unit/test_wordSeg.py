# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong

"""Unit tests for word segmentation utilities."""

import unittest
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, patch

import config
from config.featureFlag import FeatureFlag
from config.featureFlagEnums import WordNavigationUnitFlag
from textUtils import wordSeg
from textUtils.segFlag import WordSegFlag
from textUtils.wordSeg import wordSegStrategy
from textUtils.wordSeg.wordSegmenter import WordSegmenter
from textUtils.wordSeg.wordSegStrategy import ChineseWordSegmentationStrategy
from textUtils.wordSeg.wordSegUtils import WordSegWithSeparatorOffsetConverter


class TestChineseWordSegmentationInitialization(unittest.TestCase):
	def _makeMockJiebaDll(self) -> SimpleNamespace:
		return SimpleNamespace(
			initJieba=Mock(return_value=True),
			calculateWordOffsets=Mock(),
			insertUserWord=Mock(),
			deleteUserWord=Mock(),
			find=Mock(),
			freeOffsets=Mock(),
		)

	def _setWordSegConfig(self, *, initForUnusedLang: bool) -> Callable[[], None]:
		originalInitForUnusedLang = config.conf["documentNavigation"]["initWordSegForUnusedLang"]
		originalWordSegmentationStandard = config.conf["documentNavigation"]["wordSegmentationStandard"]
		config.conf["documentNavigation"]["initWordSegForUnusedLang"] = initForUnusedLang
		config.conf["documentNavigation"]["wordSegmentationStandard"] = FeatureFlag(
			WordNavigationUnitFlag.AUTO,
			behaviorOfDefault=WordNavigationUnitFlag.AUTO,
		)

		def restoreConfig() -> None:
			config.conf["documentNavigation"]["initWordSegForUnusedLang"] = originalInitForUnusedLang
			config.conf["documentNavigation"]["wordSegmentationStandard"] = originalWordSegmentationStandard

		return restoreConfig

	def test_doesNotInitializeForUnusedLanguageByDefault(self) -> None:
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

	def test_initializesForUnusedLanguageWhenConfigured(self) -> None:
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

	def test_forceInitStillInitializesForUnusedLanguage(self) -> None:
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

	def test_initFailureDisablesCppJieba(self) -> None:
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

	def test_basicLatin(self) -> None:
		text = "hello world"
		segmenter = WordSegmenter(text, wordSegFlag=WordSegFlag.UNISCRIBE)
		self.assertEqual(segmenter.getSegmentForOffset(0), (0, 6))
		self.assertEqual(segmenter.getSegmentForOffset(5), (0, 6))
		self.assertEqual(segmenter.getSegmentForOffset(6), (6, 11))
		self.assertEqual(segmenter.getSegmentForOffset(11), (6, 11))

	def test_chinese(self) -> None:
		text = "你好世界"

		with (
			patch.object(ChineseWordSegmentationStrategy, "_lib", object()),
			patch.object(ChineseWordSegmentationStrategy, "_callCppJieba", return_value=[2, 4]),
		):
			segmenter = WordSegmenter(text, wordSegFlag=WordSegFlag.CHINESE)
		self.assertEqual(segmenter.getSegmentForOffset(0), (0, 2))
		self.assertEqual(segmenter.getSegmentForOffset(1), (0, 2))
		self.assertEqual(segmenter.getSegmentForOffset(2), (2, 4))
		self.assertEqual(segmenter.getSegmentForOffset(3), (2, 4))
		self.assertEqual(segmenter.getSegmentForOffset(4), (2, 4))

	def test_chineseSegmentationFailureStoresEmptyWordEnds(self) -> None:
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

	def test_getSegmentForOffsetReturnsNoneForRecoverableError(self) -> None:
		segmenter = WordSegmenter("hello world", wordSegFlag=WordSegFlag.UNISCRIBE)
		with (
			patch.object(segmenter.strategy, "getSegmentForOffset", side_effect=IndexError("bad offset")),
			patch("textUtils.wordSeg.wordSegmenter.log.debugWarning") as debugWarning,
		):
			self.assertIsNone(segmenter.getSegmentForOffset(0))

		debugWarning.assert_called_once()

	def test_getSegmentForOffsetPropagatesUnexpectedError(self) -> None:
		segmenter = WordSegmenter("hello world", wordSegFlag=WordSegFlag.UNISCRIBE)
		with patch.object(segmenter.strategy, "getSegmentForOffset", side_effect=RuntimeError("unexpected")):
			with self.assertRaises(RuntimeError):
				segmenter.getSegmentForOffset(0)


class TestWordSegInitialize(unittest.TestCase):
	def test_runsAllRegisteredInitializers(self) -> None:
		calls: list[str] = []

		def firstInitializer() -> None:
			calls.append("first")

		def secondInitializer() -> None:
			calls.append("second")

		class ImmediateThread:
			def __init__(
				self,
				target: Callable[..., Any],
				args: tuple[Any, ...] | None = None,
				kwargs: dict[str, Any] | None = None,
				daemon: bool = False,
				name: str | None = None,
			) -> None:
				self.target: Callable[..., Any] = target
				self.args: tuple[Any, ...] = () if args is None else args
				self.kwargs: dict[str, Any] = {} if kwargs is None else kwargs
				self.daemon: bool = daemon
				self.name: str | None = name

			def start(self) -> None:
				self.target(*self.args, **self.kwargs)

		initializerList: list[tuple[str, str, Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = [
			("missingModule", "firstInitializer", firstInitializer, (), {}),
			("missingModule", "secondInitializer", secondInitializer, (), {}),
		]
		with (
			patch.object(wordSegStrategy, "_initializerList", initializerList),
			patch("threading.Thread", ImmediateThread),
		):
			wordSeg.initialize()

		self.assertEqual(calls, ["first", "second"])


class TestWordSegWithSeparatorOffsetConverter(unittest.TestCase):
	def _makeConverter(self) -> WordSegWithSeparatorOffsetConverter:
		def segmentedText(sep: str, newSepIndex: list[int]) -> str:
			newSepIndex.append(2)
			return "ab cd"

		with patch(
			"textUtils.wordSeg.wordSegUtils.WordSegmenter",
			return_value=SimpleNamespace(segmentedText=segmentedText),
		):
			return WordSegWithSeparatorOffsetConverter("abcd")

	def test_strToEncodedOffsetsMapsEndAndClampsOutOfRange(self) -> None:
		converter = self._makeConverter()

		self.assertEqual(converter.strToEncodedOffsets(-1), 0)
		self.assertEqual(converter.strToEncodedOffsets(2, 4), (3, 5))
		self.assertEqual(converter.strToEncodedOffsets(4), 5)
		self.assertEqual(converter.strToEncodedOffsets(5, 6), (5, 5))

	def test_strToEncodedOffsetsRaisesOnOutOfRangeWhenRequested(self) -> None:
		converter = self._makeConverter()

		with self.assertRaises(IndexError):
			converter.strToEncodedOffsets(5, raiseOnError=True)

	def test_encodedToStrOffsetsMapsEndAndClampsOutOfRange(self) -> None:
		converter = self._makeConverter()

		self.assertEqual(converter.encodedToStrOffsets(-1), 0)
		self.assertEqual(converter.encodedToStrOffsets(2), 2)
		self.assertEqual(converter.encodedToStrOffsets(2, 3), (2, 2))
		self.assertEqual(converter.encodedToStrOffsets(5), 4)
		self.assertEqual(converter.encodedToStrOffsets(6, 7), (4, 4))

	def test_encodedToStrOffsetsRaisesOnOutOfRangeWhenRequested(self) -> None:
		converter = self._makeConverter()

		with self.assertRaises(IndexError):
			converter.encodedToStrOffsets(6, raiseOnError=True)
