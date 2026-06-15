# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ctypes bindings for the Windows built-in ICU library.

ICU has been built into Windows since Windows 10 version 1703 (Creators Update).
The combined icu.dll is available from Windows 10 version 1903 (May 2019 Update).
Only the C APIs are exposed; no C++ APIs are available due to ABI instability.

See: https://learn.microsoft.com/windows/win32/intl/international-components-for-unicode--icu-
"""

import ctypes
from ctypes import c_int32, c_void_p, c_char_p, c_wchar_p, POINTER

# Try the combined icu.dll (Windows 10 1903+) first, then icuuc.dll (Windows 10 1703+).
# ubrk_* functions are part of the "common" library, present in both.
_lib: ctypes.WinDLL | None = None
for _dllName in ("icu.dll", "icuuc.dll"):
	try:
		_lib = ctypes.WinDLL(_dllName)
		break
	except OSError:
		pass

ICU_AVAILABLE: bool = _lib is not None
"""True if an ICU library was successfully loaded."""

UBRK_CHARACTER: int = 0
"""Break iterator type for character boundaries."""
UBRK_WORD: int = 1
"""Break iterator type for word boundaries."""
UBRK_LINE: int = 2
"""Break iterator type for line-break boundaries."""
UBRK_SENTENCE: int = 3
"""Break iterator type for sentence boundaries."""

UBRK_WORD_NONE: int = 0
"""Rule status tag: start of non-word boundary range (whitespace or punctuation between words)."""
UBRK_WORD_NONE_LIMIT: int = 100
"""Rule status tag: exclusive end of non-word boundary range."""
UBRK_WORD_NUMBER: int = 100
"""Rule status tag: start of number boundary range."""
UBRK_WORD_NUMBER_LIMIT: int = 200
"""Rule status tag: exclusive end of number boundary range."""
UBRK_WORD_LETTER: int = 200
"""Rule status tag: start of letter boundary range; values >= this are actual word boundaries."""
UBRK_WORD_LETTER_LIMIT: int = 300
"""Rule status tag: exclusive end of letter boundary range."""
UBRK_WORD_KANA: int = 300
"""Rule status tag: start of kana boundary range."""
UBRK_WORD_KANA_LIMIT: int = 400
"""Rule status tag: exclusive end of kana boundary range."""
UBRK_WORD_IDEO: int = 400
"""Rule status tag: start of ideograph boundary range."""
UBRK_WORD_IDEO_LIMIT: int = 500
"""Rule status tag: exclusive end of ideograph boundary range."""

UBRK_DONE: int = -1
"""Returned by iterator functions when there are no more boundaries."""

UErrorCode = c_int32
"""Signed 32-bit integer error code. U_ZERO_ERROR = 0; positive values indicate errors."""


def U_FAILURE(code: int) -> bool:
	"""Return True if the given UErrorCode indicates an error."""
	return code > 0


if ICU_AVAILABLE:
	assert _lib is not None

	ubrk_open = _lib.ubrk_open
	"""Create a new break iterator.

	:param kind: UBreakIteratorType (one of the UBRK_* constants).
	:param locale: Null-terminated UTF-8 locale ID, or NULL/empty for the root locale.
	:param text: UTF-16 text to analyze.
	:param textLength: Number of UTF-16 code units, or -1 for NUL-terminated.
	:param status: In/out UErrorCode; pass a pointer to a zero-initialised value.
	:return: Opaque UBreakIterator* handle; must be freed with ubrk_close.
	"""
	ubrk_open.restype = c_void_p
	ubrk_open.argtypes = (
		c_int32,              # kind: UBreakIteratorType
		c_char_p,             # locale: UTF-8 locale ID or NULL
		c_wchar_p,            # text: UTF-16 text to analyze
		c_int32,              # textLength: code units, or -1 for NUL-terminated
		POINTER(UErrorCode),  # status: in/out error code
	)

	ubrk_close = _lib.ubrk_close
	"""Free a break iterator created by ubrk_open."""
	ubrk_close.restype = None
	ubrk_close.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle to free
	)

	ubrk_setText = _lib.ubrk_setText
	"""Rebind an existing iterator to new text without reallocating.

	ICU holds a reference to the text buffer; the caller must keep it alive for the
	lifetime of the iterator.
	"""
	ubrk_setText.restype = None
	ubrk_setText.argtypes = (
		c_void_p,             # bi: UBreakIterator* handle
		c_wchar_p,            # text: new UTF-16 text buffer
		c_int32,              # textLength: code units, or -1 for NUL-terminated
		POINTER(UErrorCode),  # status: in/out error code
	)

	ubrk_first = _lib.ubrk_first
	"""Move to the first boundary (start of text) and return its position."""
	ubrk_first.restype = c_int32
	ubrk_first.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
	)

	ubrk_next = _lib.ubrk_next
	"""Advance to the next boundary and return its position.

	Returns UBRK_DONE when past the end of the text.
	"""
	ubrk_next.restype = c_int32
	ubrk_next.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
	)

	ubrk_preceding = _lib.ubrk_preceding
	"""Return the largest boundary position strictly less than offset.

	Sets the iterator to that position.
	"""
	ubrk_preceding.restype = c_int32
	ubrk_preceding.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
		c_int32,   # offset: position to search before
	)

	ubrk_following = _lib.ubrk_following
	"""Return the smallest boundary position strictly greater than offset.

	Sets the iterator to that position. Returns UBRK_DONE if past the end.
	"""
	ubrk_following.restype = c_int32
	ubrk_following.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
		c_int32,   # offset: position to search after
	)

	ubrk_getRuleStatus = _lib.ubrk_getRuleStatus
	"""Return the rule status tag for the most recently returned boundary.

	For UBRK_WORD iterators, values < UBRK_WORD_NONE_LIMIT indicate non-word boundaries
	(whitespace or punctuation); values >= UBRK_WORD_LETTER are actual word boundaries.
	"""
	ubrk_getRuleStatus.restype = c_int32
	ubrk_getRuleStatus.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
	)
