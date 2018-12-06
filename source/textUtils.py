#textUtils.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""
Classes and utilities to deal with offsets variable width encodings, particularly utf_16.
"""

import encodings
import sys
import ctypes
from collections.abc import ByteString # Python 3 import
from typing import Tuple

HIGH_SURROGATE_FIRST = u"\uD800"
HIGH_SURROGATE_LAST = u"\uDBFF"
LOW_SURROGATE_FIRST = u"\uDC00"
LOW_SURROGATE_LAST = u"\uDFFF"

class WideStringOffsetConverter:
	"""
	Object that holds a string in both its decoded and its UTF-16 encoded form.
	The object allows for easy convertion between offsets in str type strings,
	and offsets that are aware of surrogate characters in UTF-16.
	"""

	_encoding: str = "utf_16_le"
	_bytesPerIndex: int = ctypes.sizeof(ctypes.c_wchar)

	def __init__(self, strVal: str):
		super(WideStringOffsetConverter, self).__init__()
		if not isinstance(strVal, str):
			raise TypeError("Value must be of type str")
		self.decoded: str = strVal
		self.encoded: bytes = strVal.encode(self._encoding, errors="surrogatepass")

	def __repr__(self):
		return "{}({})".format(self.__class__.__name__, repr(self.decoded))

	@property
	def wideStringLength(self) -> int:
		return len(self.encoded) // self._bytesPerIndex

	@property
	def strLength(self) -> int:
		return len(self.decoded)

	def strToWideOffsets(
		self,
		strStart: int,
		strEnd: int,
		strict: bool =False
	) -> Tuple[int, int]:
		if strStart > self.strLength:
			if strict:
				raise IndexError("str start index out of range")
			strStart = min(strStart, self.strLength)
		if strEnd > self.strLength:
			if strict:
				raise IndexError("str end index out of range")
			strEnd = min(strEnd, self.strLength)
		# If the original string contains surrogate characters, we want to preserve them
		if strStart == 0:
			wideStringStart: int = 0
		else:
			precedingBytes: bytes = self.decoded[:strStart].encode(self._encoding, errors="surrogatepass")
			wideStringStart= len(precedingBytes) // self._bytesPerIndex
		if strStart == strEnd:
			return (wideStringStart, wideStringStart)
		encodedRange: bytes = self.decoded[strStart:strEnd].encode(self._encoding, errors="surrogatepass")
		wideStringEnd: int = wideStringStart + (len(encodedRange) // self._bytesPerIndex)
		return (wideStringStart, wideStringEnd)

	def wideToStrOffsets(
		self,
		wideStringStart: int,
		wideStringEnd: int,
		strict: bool = False
	) -> Tuple[int, int]:
		if wideStringStart > self.wideStringLength:
			if strict:
				raise IndexError("Encoding aware start index out of range")
			wideStringStart = min(wideStringStart, self.wideStringLength)
		if wideStringEnd > self.wideStringLength:
			if strict:
				raise IndexError("Encoding aware end index out of range")
			wideStringEnd = min(wideStringEnd, self.wideStringLength)
		bytesStart: int = wideStringStart * self._bytesPerIndex
		bytesEnd: int = wideStringEnd * self._bytesPerIndex
		if bytesStart == 0:
			precedingStr: str = ""
			strStart: int = 0
		else:
			precedingStr= self.encoded[:bytesStart].decode(self._encoding, errors="surrogatepass")
			strStart= len(precedingStr)
		if bytesStart == bytesEnd and bytesEnd <= (len(self.encoded) - self._bytesPerIndex):
			# Though we are trying to fetch str offsets for a single offset,
			# we need to make sure to avoid off by one errors caused by surrogates
			correctedBytesEnd = bytesEnd + self._bytesPerIndex
		else:
			correctedBytesEnd = bytesEnd
		decodedRange: str = self.encoded[bytesStart:correctedBytesEnd].decode(self._encoding, errors="surrogatepass")
		strEnd: int = strStart + len(decodedRange)
		# In the case where precedingStr ends with a high surrogate,
		# and decodedRange ends with a low surrogate character
		# They take one offset in the resulting string, so our offsets are off by one.
		if (
			precedingStr
			and HIGH_SURROGATE_FIRST <= precedingStr[-1] <= HIGH_SURROGATE_LAST
			and decodedRange
			and LOW_SURROGATE_FIRST <= decodedRange[0] <= LOW_SURROGATE_LAST
		):
			strStart -= 1
			strEnd -= 1
		if correctedBytesEnd > bytesEnd:
			# Compensate for the case where we stretched our offsets earlier
			strEnd -= (correctedBytesEnd - bytesEnd) // self._bytesPerIndex
		return (strStart, strEnd)
