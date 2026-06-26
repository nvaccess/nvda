# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ctypes bindings for the Windows built-in ICU library.

ICU has been built into Windows since Windows 10 version 1703 (Creators Update).
The combined icu.dll is available from Windows 10 version 1903 (May 2019 Update).
Only the C APIs are exposed; no C++ APIs are available due to ABI instability.

The ``ubrk_*`` function bindings are only defined when :data:`ICU_AVAILABLE` is True.

.. seealso::
	https://learn.microsoft.com/windows/win32/intl/international-components-for-unicode--icu-
"""

from ctypes import (
	WINFUNCTYPE,
	windll,
	c_int32,
	c_void_p,
	c_char_p,
	c_wchar_p,
	POINTER,
)
from enum import IntEnum

# Load the combined icu.dll (Windows 10 1903+) first, then icuuc.dll (Windows 10 1703+).
# ubrk_* functions are part of the "common" library, present in both.
try:
	dll = windll.icu
except OSError:
	try:
		dll = windll.icuuc
	except OSError:
		dll = None

ICU_AVAILABLE: bool = dll is not None
"""True if an ICU library was successfully loaded."""

UBRK_DONE: int = -1
"""Returned by iterator functions when there are no more boundaries."""

UErrorCode = c_int32
"""Signed 32-bit integer error code. U_ZERO_ERROR = 0; positive values indicate errors."""


class UBRK(IntEnum):
	"""The possible types of text boundaries (UBreakIteratorType)."""

	WORD = 1
	"""Word breaks."""


def U_FAILURE(code: int) -> bool:
	"""Return True if the given UErrorCode indicates an error."""
	return code > 0


if ICU_AVAILABLE:
	ubrk_open = WINFUNCTYPE(None)(("ubrk_open", dll))
	"""Create a new break iterator.

	:param kind: UBreakIteratorType (one of the UBRK members).
	:param locale: Null-terminated UTF-8 locale ID, or NULL/empty for the root locale.
	:param text: UTF-16 text to analyze.
	:param textLength: Number of UTF-16 code units, or -1 for NUL-terminated.
	:param status: In/out UErrorCode; pass a pointer to a zero-initialised value.
	:return: Opaque UBreakIterator* handle; must be freed with ubrk_close.
	"""
	ubrk_open.argtypes = (
		c_int32,  # kind: UBreakIteratorType
		c_char_p,  # locale: UTF-8 locale ID or NULL
		c_wchar_p,  # text: UTF-16 text to analyze
		c_int32,  # textLength: code units, or -1 for NUL-terminated
		POINTER(UErrorCode),  # status: in/out error code
	)
	ubrk_open.restype = c_void_p

	ubrk_close = WINFUNCTYPE(None)(("ubrk_close", dll))
	"""Free a break iterator created by ubrk_open."""
	ubrk_close.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle to free
	)
	ubrk_close.restype = None

	ubrk_preceding = WINFUNCTYPE(None)(("ubrk_preceding", dll))
	"""Return the largest boundary position strictly less than offset.

	Sets the iterator to that position.
	"""
	ubrk_preceding.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
		c_int32,  # offset: position to search before
	)
	ubrk_preceding.restype = c_int32

	ubrk_following = WINFUNCTYPE(None)(("ubrk_following", dll))
	"""Return the smallest boundary position strictly greater than offset.

	Sets the iterator to that position. Returns UBRK_DONE if past the end.
	"""
	ubrk_following.argtypes = (
		c_void_p,  # bi: UBreakIterator* handle
		c_int32,  # offset: position to search after
	)
	ubrk_following.restype = c_int32
