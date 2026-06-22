# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Comparison tests between the Uniscribe and ICU word boundary backends.

These tests document where the two backends agree and where they diverge,
using the same inputs on both sides.  Tests that require ICU are skipped
when the ICU library is not present on the system.

Word-offset comparisons are done by constructing a WordSegmenter with the
appropriate WordSegFlag and calling getSegmentForOffset.
"""

import unittest

import textUtils
from winBindings.icu import ICU_AVAILABLE
from textUtils._wordSeg.wordSegmenter import WordSegmenter
from textUtils.segFlag import WordSegFlag


skipIfNoICU = unittest.skipUnless(ICU_AVAILABLE, "ICU library not available on this system")

# Encoding used for all WordSegmenter calls — matches what NVDA uses internally.
_ENCODING = textUtils.WCHAR_ENCODING


def _icuWordOffsets(text: str, offset: int) -> tuple[int, int] | None:
	"""Get word offsets via the ICU backend (UTF-16 offsets)."""
	return WordSegmenter(text, _ENCODING, WordSegFlag.ICU).getSegmentForOffset(offset)


def _uniscribeWordOffsets(text: str, offset: int) -> tuple[int, int] | None:
	"""Get word offsets via the Uniscribe backend (UTF-16 offsets)."""
	return WordSegmenter(text, _ENCODING, WordSegFlag.UNISCRIBE).getSegmentForOffset(offset)


class _WordOffsetsParityTest(unittest.TestCase):
	"""Base for per-script word offset parity tests.

	Subclasses set TEXT and add test_* methods that assert the exact span via
	_assertSameWordOffsets.  Has no test methods of its own, so the loader runs nothing.
	"""

	TEXT: str

	def _assertSameWordOffsets(self, offset: int) -> tuple[int, int] | None:
		"""Assert both backends return the same word offsets for self.TEXT at offset.

		:param offset: UTF-16 code unit offset within self.TEXT to query.
		:return: The (start, end) offsets, so callers can additionally assert the exact span.
		:raises AssertionError: If the ICU and Uniscribe backends disagree.
		"""
		icu_result = _icuWordOffsets(self.TEXT, offset)
		uni_result = _uniscribeWordOffsets(self.TEXT, offset)
		self.assertEqual(
			icu_result,
			uni_result,
			f"Backends disagree on word offsets for {self.TEXT!r} at offset {offset}: "
			f"ICU={icu_result!r} Uniscribe={uni_result!r}",
		)
		return icu_result


@skipIfNoICU
class TestWordOffsetsEnglish(_WordOffsetsParityTest):
	"""Word offset comparison for English text.

	Both backends include trailing whitespace as part of the preceding word.
	NVDA's Uniscribe implementation (textUtils.cpp) does this natively;
	the ICU implementation mirrors that behaviour explicitly.
	"""

	TEXT = "hello world"

	def test_first_word(self):
		"""Both backends: "hello " — trailing space included."""
		result = self._assertSameWordOffsets(0)
		self.assertEqual(result, (0, 6))

	def test_mid_first_word(self):
		result = self._assertSameWordOffsets(2)
		self.assertEqual(result, (0, 6))

	def test_space(self):
		"""Both backends: querying at the space returns the preceding word+space."""
		result = self._assertSameWordOffsets(5)
		self.assertEqual(result, (0, 6))

	def test_second_word(self):
		"""Both backends: "world" — no trailing space at end of string."""
		result = self._assertSameWordOffsets(6)
		self.assertEqual(result, (6, 11))

	def test_mid_second_word(self):
		result = self._assertSameWordOffsets(8)
		self.assertEqual(result, (6, 11))


@skipIfNoICU
class TestWordOffsetsHebrew(_WordOffsetsParityTest):
	"""Word offset comparison for vocalized (Biblical) Hebrew — שָׁלוֹם עוֹלָם (peace, world).

	The niqqud (combining vowel and shin points) attach to their base letters, so each
	word stays a single segment: שָׁלוֹם is 7 UTF-16 code units, עוֹלָם is 6.
	"""

	TEXT = "שָׁלוֹם עוֹלָם"

	def test_first_word(self):
		"""Both backends: "שָׁלוֹם " — trailing space included, offsets (0, 8)."""
		result = self._assertSameWordOffsets(0)
		self.assertEqual(result, (0, 8))

	def test_mid_first_word(self):
		result = self._assertSameWordOffsets(2)
		self.assertEqual(result, (0, 8))

	def test_space(self):
		"""Both backends: querying at offset 7 (space) returns the preceding word+space."""
		result = self._assertSameWordOffsets(7)
		self.assertEqual(result, (0, 8))

	def test_second_word(self):
		"""Both backends: "עוֹלָם" — no trailing space."""
		result = self._assertSameWordOffsets(8)
		self.assertEqual(result, (8, 14))


@skipIfNoICU
class TestWordOffsetsComplexScriptDivergence(unittest.TestCase):
	"""Japanese and Khmer: Uniscribe falls back to character/cluster level; ICU groups words."""

	def test_japanese_uniscribe_is_character_level(self):
		"""Japanese "これは日本語です": Uniscribe returns single code points; ICU groups words."""
		text = "これは日本語です"
		# Offset 0 ("こ"): ICU groups "これ"; Uniscribe returns just "こ".
		icu_result = _icuWordOffsets(text, 0)
		uni_result = _uniscribeWordOffsets(text, 0)
		self.assertNotEqual(icu_result, uni_result)
		# Uniscribe is character-level here (single code point).
		self.assertEqual(uni_result[1] - uni_result[0], 1)
		# ICU groups more than one code point into a word.
		self.assertGreater(icu_result[1] - icu_result[0], 1)

	def test_khmer_uniscribe_breaks_clusters(self):
		"""Khmer "ខ្ញុំស្រលាញ់": Uniscribe breaks the second word into syllable clusters; ICU keeps it whole."""
		text = "ខ្ញុំស្រលាញ់"
		# Offset 5 is the start of the second Khmer word "ស្រលាញ់".
		icu_result = _icuWordOffsets(text, 5)
		uni_result = _uniscribeWordOffsets(text, 5)
		self.assertNotEqual(icu_result, uni_result)
		# ICU spans the whole word; Uniscribe returns a shorter cluster.
		self.assertGreater(icu_result[1] - icu_result[0], uni_result[1] - uni_result[0])


@skipIfNoICU
class TestWordOffsetsEmojiZwjSequence(unittest.TestCase):
	"""Multi-person emoji ZWJ sequence with skin-tone modifiers.

	"👩🏻‍👧🏻‍👦🏻" (woman + girl + boy family, each with a light skin-tone modifier,
	joined by ZERO WIDTH JOINER) is a single UAX#29 word.  ICU treats the whole
	sequence as one segment; Uniscribe falls back to grapheme/surrogate-level
	boundaries and returns only the leading part.

	The sequence is 14 UTF-16 code units:
	👩 (2) 🏻 (2) ZWJ (1) 👧 (2) 🏻 (2) ZWJ (1) 👦 (2) 🏻 (2).
	"""

	TEXT = "👩🏻‍👧🏻‍👦🏻"
	# UTF-16 code-unit length of the whole sequence.
	LENGTH = len(TEXT.encode("utf-16-le")) // 2

	def test_length_is_as_expected(self):
		"""Guard the constant the assertions below rely on."""
		self.assertEqual(self.LENGTH, 14)

	def test_icu_groups_whole_sequence(self):
		"""ICU returns the entire ZWJ sequence as one word from offset 0."""
		self.assertEqual(_icuWordOffsets(self.TEXT, 0), (0, self.LENGTH))

	def test_backends_diverge(self):
		"""Uniscribe does not group the whole sequence; ICU does."""
		icu_result = _icuWordOffsets(self.TEXT, 0)
		uni_result = _uniscribeWordOffsets(self.TEXT, 0)
		self.assertNotEqual(icu_result, uni_result)
		# ICU spans the full sequence; Uniscribe returns a shorter leading run.
		self.assertEqual(icu_result, (0, self.LENGTH))
		self.assertLess(uni_result[1] - uni_result[0], self.LENGTH)
