# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
import re

from logHandler import log

from ..segFlag import WordSegFlag
from . import wordSegStrategy
from winBindings.icu import ICU_AVAILABLE as _ICU_AVAILABLE


_GET_SEGMENT_RECOVERABLE_EXCEPTIONS = (
	OSError,
	ValueError,
	TypeError,
	IndexError,
	ctypes.ArgumentError,
)


class WordSegmenter:
	"""Selects appropriate segmentation strategy and segments text."""

	# Chinese characters and Japanese kanji (CJK Unified Ideographs U+4E00 - U+9FFF)
	_CHINESE_CHARACTER_AND_JAPANESE_KANJI: re.Pattern[str] = re.compile(r"[\u4E00-\u9FFF]")
	# Japanese kana (Hiragana U+3040 - U+309F, Katakana U+30A0 - U+30FF)
	_KANA: re.Pattern[str] = re.compile(r"[\u3040-\u309F\u30A0-\u30FF]")

	def __init__(
		self,
		text: str,
		encoding: str | None = "UTF-8",
		wordSegFlag: WordSegFlag = WordSegFlag.AUTO,
	) -> None:
		self.text: str = text
		self.encoding: str | None = encoding
		self.wordSegFlag: WordSegFlag = wordSegFlag
		self.strategy: wordSegStrategy.WordSegmentationStrategy = self._chooseStrategy()

	def _chooseStrategy(
		self,
	) -> wordSegStrategy.WordSegmentationStrategy:
		"""Choose the segmentation strategy, falling back Chinese -> ICU -> Uniscribe.

		The CHINESE flag always uses the Chinese strategy when cppjieba is loaded; under
		AUTO the Chinese strategy is used only for Chinese (non-kana) text.  ICU is used
		for AUTO and ICU, and as the fallback when cppjieba is unavailable: it follows
		UAX#29 plus script-driven dictionary segmentation, handling complex scripts that
		Uniscribe breaks poorly.  Uniscribe is the final fallback and the only strategy
		for the UNISCRIBE flag (it stays pinned where it is strictly required, e.g.
		EditTextInfo, to match the Windows edit control / Notepad).
		"""
		flag = self.wordSegFlag
		# Chinese: always for the CHINESE flag, or under AUTO for Chinese (non-kana) text.
		if (
			flag in (WordSegFlag.AUTO, WordSegFlag.CHINESE)
			and wordSegStrategy.ChineseWordSegmentationStrategy._lib
		):
			if flag == WordSegFlag.CHINESE or (
				WordSegmenter._CHINESE_CHARACTER_AND_JAPANESE_KANJI.search(self.text)
				and not WordSegmenter._KANA.search(self.text)
			):
				return wordSegStrategy.ChineseWordSegmentationStrategy(self.text, self.encoding)
		elif flag == WordSegFlag.CHINESE:
			log.debugWarning("Chinese word segmenter is unavailable. Falling back to ICU/Uniscribe.")
		# ICU for everything except the explicit UNISCRIBE flag.
		if flag != WordSegFlag.UNISCRIBE and _ICU_AVAILABLE:
			return wordSegStrategy.IcuWordSegmentationStrategy(self.text, self.encoding)
		elif flag == WordSegFlag.ICU:
			log.debugWarning("ICU word segmenter is unavailable. Falling back to Uniscribe.")
		return wordSegStrategy.UniscribeWordSegmentationStrategy(self.text, self.encoding)

	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:
		"""Get the segment containing the given offset."""
		try:
			return self.strategy.getSegmentForOffset(offset)
		except _GET_SEGMENT_RECOVERABLE_EXCEPTIONS as e:
			log.debugWarning(
				f"WordSegmenter.getSegmentForOffset failed: {e}  "
				f"text: {self.text!r} offset: {offset}  segmentation strategy: {self.strategy}",
			)
			return None

	def segmentedText(self, sep: str = " ", newSepIndex: list[int] | None = None) -> str:
		return self.strategy.segmentedText(sep, newSepIndex)
