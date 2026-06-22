# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for ICU word segmentation strategy."""

import unittest
from unittest.mock import patch

from textUtils._wordSeg import wordSegStrategy


class TestIcuStrategy(unittest.TestCase):
	def test_icu_strategy_getSegmentForOffset_calls_primitive(self):
		text = "hello world"
		with patch("textUtils.icu.calculateWordOffsets", return_value=(0, 6)) as mockCalc:
			strat = wordSegStrategy.IcuWordSegmentationStrategy(text, None)
			result = strat.getSegmentForOffset(2)
		mockCalc.assert_called_once_with(text, 2)
		self.assertEqual(result, (0, 6))

	def test_icu_segmentedText_returns_text_unchanged(self):
		strat = wordSegStrategy.IcuWordSegmentationStrategy("hello", None)
		self.assertEqual(strat.segmentedText(), "hello")

	def test_explicit_icu_flag_selects_icu_when_available(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with patch.object(wordSegmenter, "_ICU_AVAILABLE", True):
			seg = wordSegmenter.WordSegmenter("hello", None, WordSegFlag.ICU)
		self.assertIsInstance(seg.strategy, wordSegStrategy.IcuWordSegmentationStrategy)

	def test_explicit_icu_flag_falls_back_when_unavailable(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with patch.object(wordSegmenter, "_ICU_AVAILABLE", False):
			seg = wordSegmenter.WordSegmenter("hello", None, WordSegFlag.ICU)
		self.assertIsInstance(seg.strategy, wordSegStrategy.UniscribeWordSegmentationStrategy)

	def test_auto_prefers_icu_for_latin_when_available(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with (
			patch.object(wordSegmenter, "_ICU_AVAILABLE", True),
			patch.object(
				wordSegStrategy.ChineseWordSegmentationStrategy,
				"_lib",
				None,
			),
		):
			seg = wordSegmenter.WordSegmenter("hello world", None, WordSegFlag.AUTO)
		self.assertIsInstance(seg.strategy, wordSegStrategy.IcuWordSegmentationStrategy)

	def test_auto_falls_back_to_uniscribe_when_icu_unavailable(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with (
			patch.object(wordSegmenter, "_ICU_AVAILABLE", False),
			patch.object(
				wordSegStrategy.ChineseWordSegmentationStrategy,
				"_lib",
				None,
			),
		):
			seg = wordSegmenter.WordSegmenter("hello world", None, WordSegFlag.AUTO)
		self.assertIsInstance(seg.strategy, wordSegStrategy.UniscribeWordSegmentationStrategy)
