# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ICU-based text boundary utilities using the Windows built-in ICU library.

Requires Windows 10 version 1703 (Creators Update) or later.
"""

import ctypes
from contextlib import contextmanager

import winBindings.icu as _icu
from logHandler import log

_ROOT_LOCALE: bytes = b""
"""ICU root locale. Word and character segmentation are script-driven, not
locale-driven (see calculateWordOffsets), so the root locale is always used.
"""


@contextmanager
def _breakIterator(kind: int, locale: bytes, text: str):
	"""Context manager that opens an ICU BreakIterator, yields it, then closes it.

	The ctypes buffer is kept alive for the duration of the block, satisfying
	ICU's requirement that the text pointer remains valid while the iterator is in use.

	:param kind: One of the UBRK_* constants from winBindings.icu.
	:param locale: ICU locale byte string (the root locale, _ROOT_LOCALE).
	:param text: Python str to analyze.
	:raises RuntimeError: If ICU reports an error opening the iterator.
	"""
	buf = ctypes.create_unicode_buffer(text)
	textLength = len(buf) - 1
	status = _icu.UErrorCode(0)
	bi = _icu.ubrk_open(kind, locale, buf, textLength, ctypes.byref(status))
	if _icu.U_FAILURE(status.value) or not bi:
		raise RuntimeError(f"ubrk_open failed with status {status.value}")
	try:
		yield bi
	finally:
		_icu.ubrk_close(bi)


def calculateWordOffsets(
	text: str,
	offset: int,
) -> tuple[int, int] | None:
	"""Calculate the UTF-16 start and end offsets of the word at the given offset.

	Word boundaries follow Unicode Standard Annex #29 default rules plus automatic
	dictionary-based segmentation for scripts such as Thai, Lao, Khmer, and CJK
	ideographs.  ICU selects the dictionary by the script of the characters, not by
	the locale, so no language is passed: any locale (including unrecognised codes)
	would yield identical word boundaries and ICU never errors on an unknown locale
	(it silently falls back to the root locale).  The root locale is therefore used
	unconditionally.  (Locale-sensitive break types such as line and sentence
	breaking would need a locale, but those are not used here.)

	Trailing whitespace is included in the preceding word segment, matching the
	behaviour of NVDA's Uniscribe implementation (textUtils.cpp).  When the offset
	falls inside a whitespace run, the returned segment is the preceding word plus
	the whitespace.

	Note: ICU coalesces a run of identical whitespace into one segment but splits
	mixed whitespace (e.g. space + tab) into separate segments, so a mixed run is
	not merged into a single word.  This is not worth special-casing: the legacy
	Uniscribe/Notepad behaviour for mixed whitespace runs is itself inconsistent.

	:param text: The line text as a Python str.
	:param offset: UTF-16 code unit offset within text at which to find the boundary.
	:return: (startOffset, endOffset) as UTF-16 code unit indices (endOffset exclusive),
	    or None if the ICU call failed.
	"""
	utf16_bytes = text.encode("utf-16-le", errors="surrogatepass")
	textLength = len(utf16_bytes) // 2
	if offset >= textLength:
		return (offset, offset + 1)
	locale = _ROOT_LOCALE

	def _segText(segStart: int, segEnd: int) -> str:
		return utf16_bytes[segStart * 2 : segEnd * 2].decode("utf-16-le", errors="surrogatepass")

	try:
		with _breakIterator(_icu.UBRK_WORD, locale, text) as bi:
			# Find [start, end) — the ICU segment containing offset.
			# ICU offsets are code-point indexed, so anchor on the boundary following
			# offset and take the boundary preceding that. (ubrk_preceding(offset + 1)
			# would snap back for multi-unit segments.)
			end = _icu.ubrk_following(bi, offset)
			if end == _icu.UBRK_DONE:
				end = textLength
			start = _icu.ubrk_preceding(bi, end)
			if start == _icu.UBRK_DONE:
				start = 0

			if _segText(start, end).isspace():
				# Offset is inside a whitespace run.  Attach this run to the
				# preceding segment (mirroring the Uniscribe trailing-space rule).
				if start > 0:
					wordStart = _icu.ubrk_preceding(bi, start)
					if wordStart == _icu.UBRK_DONE:
						wordStart = 0
					return (wordStart, end)
			else:
				# Offset is inside a word/punctuation segment.  Extend the end
				# through any immediately following whitespace run.
				nextEnd = _icu.ubrk_following(bi, end)
				if nextEnd != _icu.UBRK_DONE and _segText(end, nextEnd).isspace():
					return (start, nextEnd)

			return (start, end)
	except RuntimeError:
		log.debugWarning("ICU word break iterator failed", exc_info=True)
		return None
