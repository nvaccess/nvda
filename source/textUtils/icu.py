# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ICU-based text boundary utilities using the Windows built-in ICU library.

Requires Windows 10 version 1703 (Creators Update) or later.
"""

import ctypes
from contextlib import contextmanager

import winBindings.icu as icu
from logHandler import log

_ROOT_LOCALE: bytes = b""
"""ICU root locale. Word and character segmentation are script-driven, not
locale-driven (see calculateWordOffsets), so the root locale is always used.
"""


@contextmanager
def _breakIterator(kind: int, locale: bytes, buf: ctypes.Array[ctypes.c_wchar]):
	"""Context manager that opens an ICU BreakIterator, yields it, then closes it.

	The caller owns the text buffer and must keep it alive for the duration of the
	block, satisfying ICU's requirement that the text pointer remains valid while
	the iterator is in use.

	:param kind: One of the UBRK members from winBindings.icu.
	:param locale: ICU locale byte string (the root locale, _ROOT_LOCALE).
	:param buf: NUL-terminated UTF-16 buffer (ctypes.create_unicode_buffer) to analyze.
	:raises RuntimeError: If ICU reports an error opening the iterator.
	"""
	textLength = len(buf) - 1
	status = icu.UErrorCode(0)
	bi = icu.ubrk_open(kind, locale, buf, textLength, ctypes.byref(status))
	if icu.U_FAILURE(status.value) or not bi:
		raise RuntimeError(f"ubrk_open failed with status {status.value}")
	try:
		yield bi
	finally:
		icu.ubrk_close(bi)


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
	# A c_wchar buffer is UTF-16 code-unit indexed on Windows, so buf[a:b] is exactly
	# the segment ICU's offsets refer to (lone surrogates decode as non-space).
	buf = ctypes.create_unicode_buffer(text)
	textLength = len(buf) - 1
	if offset >= textLength:
		return (offset, offset + 1)

	try:
		with _breakIterator(icu.UBRK.WORD, _ROOT_LOCALE, buf) as bi:
			# Find [start, end) — the ICU segment containing offset.
			# ICU offsets are UTF-16 code-unit indexed, so anchor on the boundary following
			# offset and take the boundary preceding that. (ubrk_preceding(offset + 1)
			# would snap back for multi-unit segments.)
			end = icu.ubrk_following(bi, offset)
			if end == icu.UBRK_DONE:
				end = textLength
			start = icu.ubrk_preceding(bi, end)
			if start == icu.UBRK_DONE:
				start = 0

			if buf[start:end].isspace():
				# Offset is inside a whitespace run.  Attach this run to the
				# preceding segment (mirroring the Uniscribe trailing-space rule).
				if start > 0:
					wordStart = icu.ubrk_preceding(bi, start)
					if wordStart == icu.UBRK_DONE:
						wordStart = 0
					return (wordStart, end)
			else:
				# Offset is inside a word/punctuation segment.  Extend the end
				# through any immediately following whitespace run.
				nextEnd = icu.ubrk_following(bi, end)
				if nextEnd != icu.UBRK_DONE and buf[end:nextEnd].isspace():
					return (start, nextEnd)

			return (start, end)
	except RuntimeError:
		log.debugWarning("ICU word break iterator failed", exc_info=True)
		return None
