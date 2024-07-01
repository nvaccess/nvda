# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2024 NV Access Limited, Babbage B.V., Łukasz Golonka

"""
Classes and utilities to deal with offsets variable width encodings, particularly utf_16.
"""

import ctypes
import encodings
import locale
import unicodedata
from abc import ABCMeta, abstractmethod, abstractproperty
from functools import cached_property
from typing import Generator, Optional, Tuple, Type

from logHandler import log

from .uniscribe import splitAtCharacterBoundaries

WCHAR_ENCODING = "utf_16_le"
UTF8_ENCODING = "utf-8"
USER_ANSI_CODE_PAGE = locale.getpreferredencoding()


class OffsetConverter(metaclass=ABCMeta):
	decoded: str

	def __init__(self, text: str):
		if not isinstance(text, str):
			raise TypeError("Value must be of type str")
		self.decoded: str = text

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.decoded)})"

	@abstractproperty
	def encodedStringLength(self) -> int:
		"""Returns the length of the string in itssubclass-specific encoded representation."""
		raise NotImplementedError

	@property
	def strLength(self) -> int:
		"""Returns the length of the string in its pythonic string representation."""
		return len(self.decoded)

	@abstractmethod
	def strToEncodedOffsets(
			self,
			strStart: int,
			strEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		"""
		This method takes two offsets from the str representation
		of the string the object is initialized with, and converts them to subclass-specific encoded string offsets.
		@param strStart: The start offset in the str representation of the string.
		@param strEnd: The end offset in the str representation of the string.
			This offset is exclusive.
		@param raiseOnError: Raises an IndexError when one of the given offsets
			exceeds L{strLength} or is lower than zero.
			If C{False}, the out of range offset will be bounded to the range of the string.
		@raise ValueError: if strEnd < strStart
		"""
		if strEnd is not None and strEnd < strStart:
			raise ValueError(
				"strEnd=%d must be greater than or equal to strStart=%d"
				% (strEnd, strStart)
			)
		if strStart < 0 or strStart > self.strLength:
			if raiseOnError:
				raise IndexError("str start index out of range")
		if strEnd is not None and (strEnd < 0 or strEnd > self.strLength):
			if raiseOnError:
				raise IndexError("str end index out of range")

	@abstractmethod
	def encodedToStrOffsets(
			self,
			encodedStart: int,
			encodedEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		r"""
		This method takes two offsets from subclass-specific encoded string representation
		of the string the object is initialized with, and converts them to str offsets.
		@param encodedStart: The start offset in the wide character representation of the string.
		@param encodedEnd: The end offset in the wide character representation of the string.
			This offset is exclusive.
		@param raiseOnError: Raises an IndexError when one of the given offsets
			exceeds L{encodedStringLength} or is lower than zero.
			If C{False}, the out of range offset will be bounded to the range of the string.
		@raise ValueError: if wideStringEnd < wideStringStart
		"""
		if encodedEnd is not None and encodedEnd < encodedStart:
			raise ValueError(
				f"{encodedEnd=} must be greater than or equal to {encodedStart=}"
			)
		if encodedStart < 0 or encodedStart > self.encodedStringLength:
			if raiseOnError:
				raise IndexError("Wide string start index out of range")
		if encodedEnd is not None and (encodedEnd < 0 or encodedEnd > self.encodedStringLength):
			if raiseOnError:
				raise IndexError("Wide string end index out of range")


class WideStringOffsetConverter(OffsetConverter):
	R"""
	Object that holds a string in both its decoded and its UTF-16 encoded form.
	The object allows for easy conversion between offsets in str type strings,
	and offsets in wide character (UTF-16) strings (that are aware of surrogate characters).
	This representation is used by all wide character strings in Windows (i.e. with characters of type L{ctypes.c_wchar}).

	In Python 3 strings, every offset in a string corresponds with one unicode codepoint.
	In UTF-16 encoded strings, 32-bit unicode characters (such as emoji)
	are encoded as one high surrogate and one low surrogate character.
	Therefore, they take not one, but two offsets in such a string.
	This behavior is equivalent to how Python 2 unicode strings behave,
	which are internally encoded as UTF-16.

	For example: 😂 takes one offset in a Python 3 string.
	However, in a Python 2 string or UTF-16 encoded wide string,
	this character internally consists of two characters: \ud83d and \ude02.
	"""

	_encoding: str = WCHAR_ENCODING
	_bytesPerIndex: int = ctypes.sizeof(ctypes.c_wchar)

	def __init__(self, text: str):
		super().__init__(text)
		self.encoded: bytes = text.encode(self._encoding, errors="surrogatepass")

	@property
	def encodedStringLength(self) -> int:
		"""Returns the length of the string in its wide character (UTF-16) representation."""
		return len(self.encoded) // self._bytesPerIndex

	def strToEncodedOffsets(
			self,
			strStart: int,
			strEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		"""
		This method takes two offsets from the str representation
		of the string the object is initialized with, and converts them to wide character string offsets.
		@param strStart: The start offset in the str representation of the string.
		@param strEnd: The end offset in the str representation of the string.
			This offset is exclusive.
		@param raiseOnError: Raises an IndexError when one of the given offsets
			exceeds L{strLength} or is lower than zero.
			If C{False}, the out of range offset will be bounded to the range of the string.
		@raise ValueError: if strEnd < strStart
		"""
		super().strToEncodedOffsets(strStart, strEnd, raiseOnError)
		strStart = max(0, min(strStart, self.strLength))
		# Optimisation, don't do anything special if offsets are collapsed at the start.
		if 0 == strEnd == strStart:
			return (0, 0)
		# If the original string contains surrogate characters, we want to preserve them
		if strStart == 0:
			wideStringStart: int = 0
		else:
			precedingBytes: bytes = self.decoded[:strStart].encode(self._encoding, errors="surrogatepass")
			wideStringStart= len(precedingBytes) // self._bytesPerIndex
		if strEnd is None:
			return wideStringStart
		strEnd = max(0, min(strEnd, self.strLength))
		if strStart == strEnd:
			return (wideStringStart, wideStringStart)
		encodedRange: bytes = self.decoded[strStart:strEnd].encode(self._encoding, errors="surrogatepass")
		wideStringEnd: int = wideStringStart + (len(encodedRange) // self._bytesPerIndex)
		return (wideStringStart, wideStringEnd)

	def encodedToStrOffsets(
			self,
			encodedStart: int,
			encodedEnd: int,
			raiseOnError: bool = False,
	) -> Tuple[int, int]:
		r"""
		This method takes two offsets from the wide character representation
		of the string the object is initialized with, and converts them to str offsets.
		encodedEnd is considered an exclusive offset.
		If either encodedStart or encodedEnd corresponds with an offset
		in the middel of a surrogate pair, it is yet counted as one offset in the string.
		For example, when L{decoded} is "😂", which is one offset in the str representation,
		this method returns (0, 1) in all of the following cases:
			* encodedStart=0, encodedEnd=1
			* encodedStart=0, encodedEnd=2
			* encodedStart=1, encodedEnd=2
		However, encodedStart=1, encodedEnd=1 results in (0, 0)
		@param encodedStart: The start offset in the wide character representation of the string.
		@param encodedEnd: The end offset in the wide character representation of the string.
			This offset is exclusive.
		@param raiseOnError: Raises an IndexError when one of the given offsets
			exceeds L{encodedStringLength} or is lower than zero.
			If C{False}, the out of range offset will be bounded to the range of the string.
		@raise ValueError: if encodedEnd < encodedStart
		"""
		# Optimisation, don't do anything special if offsets are collapsed at the start.
		if 0 == encodedEnd == encodedStart:
			return (0, 0)
		if encodedEnd is None:
			return self.encodedToStrOffsets(encodedStart, encodedStart, raiseOnError)[0]
		super().encodedToStrOffsets(encodedStart, encodedEnd, raiseOnError)
		encodedStart = max(0, min(encodedStart, self.encodedStringLength))
		encodedEnd = max(0, min(encodedEnd, self.encodedStringLength))
		bytesStart: int = encodedStart * self._bytesPerIndex
		bytesEnd: int = encodedEnd * self._bytesPerIndex
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
			and isHighSurrogate(precedingStr[-1])
			and decodedRange
			and isLowSurrogate(decodedRange[0])
		):
			strStart -= 1
			strEnd -= 1
		if correctedBytesEnd > bytesEnd:
			# Compensate for the case where we stretched our offsets earlier
			strEnd -= (correctedBytesEnd - bytesEnd) // self._bytesPerIndex
		return (strStart, strEnd)
	
	wideStringLength = encodedStringLength
	strToWideOffsets = strToEncodedOffsets
	wideToStrOffsets = encodedToStrOffsets


def getTextFromRawBytes(
	buf: bytes,
	numChars: int,
	encoding: Optional[str] = None,
	errorsFallback: str = "replace"
):
	"""
	Gets a string from a raw bytes object, decoded using the specified L{encoding}.
	In most cases, the bytes object is fetched by passing the raw attribute of a ctypes.c_char-Array to this function.
	If L{encoding} is C{None}, the bytes object is inspected on whether it contains single byte or multi byte characters.
	As a first attempt, the bytes are encoded using the surrogatepass error handler.
	This handler behaves like strict for all encodings without surrogates,
	while making sure that surrogates are properly decoded when using UTF-16.
	If that fails, the exception is logged and the bytes are decoded
	according to the L{errorsFallback} error handler.
	"""
	if encoding is None:
		# If the buffer we got contains any non null characters from numChars to the buffer's end,
		# the buffer most likely contains multibyte characters.
		# Note that in theory, it could also be a multibyte character string
		# with nulls taking up the second half of the string.
		# Unfortunately, there isn't a good way to detect those cases.
		if numChars > 1 and any(buf[numChars:]):
			encoding = WCHAR_ENCODING
		else:
			encoding = USER_ANSI_CODE_PAGE
	else:
		encoding = encodings.normalize_encoding(encoding).lower()
	if encoding.startswith("utf_16"):
		numBytes = numChars * 2
	elif encoding.startswith("utf_32"):
		numBytes = numChars * 4
	else: # All other encodings are single byte.
		numBytes = numChars
	rawText: bytes = buf[:numBytes]
	if not any(rawText):
		# rawText is empty or only contains null characters.
		# If this is a range with only null characters in it, there's not much we can do about this.
		return ""
	try:
		text = rawText.decode(encoding, errors="surrogatepass")
	except UnicodeDecodeError:
		log.debugWarning("Error decoding text in %r, probably wrong encoding assumed or incomplete data" % buf)
		text = rawText.decode(encoding, errors=errorsFallback)
	return text

HIGH_SURROGATE_FIRST = u"\uD800"
HIGH_SURROGATE_LAST = u"\uDBFF"

def isHighSurrogate(ch: str) -> bool:
	"""Returns if the given character is a high surrogate UTF-16 character."""
	return HIGH_SURROGATE_FIRST <= ch <= HIGH_SURROGATE_LAST

LOW_SURROGATE_FIRST = u"\uDC00"
LOW_SURROGATE_LAST = u"\uDFFF"

def isLowSurrogate(ch: str) -> bool:
	"""Returns if the given character is a low surrogate UTF-16 character."""
	return LOW_SURROGATE_FIRST <= ch <= LOW_SURROGATE_LAST


#: ￼ OBJECT REPLACEMENT CHARACTER,
# placeholder in the text for another unspecified object, for example in a compound document.
# https://en.wikipedia.org/wiki/Specials_(Unicode_block)
OBJ_REPLACEMENT_CHAR = u"\uFFFC"

#: � REPLACEMENT CHARACTER,
# used to replace an unknown, unrecognized, or unrepresentable character.
# https://en.wikipedia.org/wiki/Specials_(Unicode_block)
REPLACEMENT_CHAR = u"\uFFFD"


class UTF8OffsetConverter(OffsetConverter):
	R"""
	Object that holds a string in both its decoded and its UTF-8 encoded form.
	The object allows for easy conversion between offsets in str type strings,
	and offsets in UTF-8 encoded strings.

	A single character in UTF-8 encoding might take 1, 2, or 4 bytes.
	Examples of applications using UTF-8 encoding are all Scintilla-based text editors,
	including Notepad++.
	"""

	_encoding: str = UTF8_ENCODING

	def __init__(self, text: str):
		super().__init__(text)
		self.encoded: bytes = text.encode(self._encoding)

	@property
	def encodedStringLength(self) -> int:
		"""Returns the length of the string in its UTF-8 representation."""
		return len(self.encoded)

	def strToEncodedOffsets(
			self,
			strStart: int,
			strEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		super().strToEncodedOffsets(strStart, strEnd, raiseOnError)
		if strStart == 0:
			resultStart = 0
		else:
			resultStart = len(self.decoded[:strStart].encode(self._encoding))
		if strEnd is None:
			return resultStart
		elif strStart == strEnd:
			return (resultStart, resultStart)
		else:
			resultEnd = resultStart + len(self.decoded[strStart:strEnd].encode(self._encoding))
			return (resultStart, resultEnd)

	def encodedToStrOffsets(
			self,
			encodedStart: int,
			encodedEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		r"""
			This method takes two offsets from UTF-8 representation
			of the string the object is initialized with, and converts them to str offsets.
			This implementation ignores raiseOnError argument and
			it will allways raise UnicodeDecodeError if indices are invalid.
		"""
		# Optimisation, don't do anything special if offsets are collapsed at the start.
		if 0 == encodedEnd == encodedStart:
			return (0, 0)
		super().encodedToStrOffsets(encodedStart, encodedEnd, raiseOnError)
		if encodedStart == 0:
			resultStart = 0
		else:
			resultStart = len(self.encoded[:encodedStart].decode(self._encoding))
		if encodedEnd is None:
			return resultStart
		elif encodedEnd == encodedStart:
			return (resultStart, resultStart)
		else:
			resultEnd = resultStart + len(self.encoded[encodedStart:encodedEnd].decode(self._encoding))
			return (resultStart, resultEnd)


class IdentityOffsetConverter(OffsetConverter):
	R"""
		This is a dummy converter that assumes 1:1 correspondence between encoded and decoded characters.
	"""

	def __init__(self, text: str):
		super().__init__(text)

	@property
	def encodedStringLength(self) -> int:
		return self.strLength

	def strToEncodedOffsets(
			self,
			strStart: int,
			strEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		super().strToEncodedOffsets(strStart, strEnd, raiseOnError)
		if strEnd is None:
			return strStart
		return (strStart, strEnd)

	def encodedToStrOffsets(
			self,
			encodedStart: int,
			encodedEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int, int]:
		super().encodedToStrOffsets(encodedStart, encodedEnd, raiseOnError)
		if encodedEnd is None:
			return encodedStart
		return (encodedStart, encodedEnd)


DEFAULT_UNICODE_NORMALIZATION_ALGORITHM = "NFKC"


class UnicodeNormalizationOffsetConverter(OffsetConverter):
	"""
	Object that holds a string in both its decoded and its unicode normalized form.
	The object allows for easy conversion between offsets in strings which may or may not be normalized,

	For example, when using the NFKC algorithm, the "ĳ" ligature normalizes to "ij",
	which takes two characters instead of one.
	"""
	normalizationForm: str
	computedStrToEncodedOffsets: list[int]
	computedEncodedToStrOffsets: list[int]

	def __init__(self, text: str, normalizationForm: str = DEFAULT_UNICODE_NORMALIZATION_ALGORITHM):
		super().__init__(text)
		self.normalizationForm = normalizationForm
		self.computedStrToEncodedOffsets = computedStrToEncodedOffsets = []
		self.computedEncodedToStrOffsets = computedEncodedToStrOffsets = []
		origOffset = normOffset = 0
		normalized = ""
		for origPart in splitAtCharacterBoundaries(text):
			normPart = unicodedata.normalize(normalizationForm, origPart)
			normalized += normPart
			isReorder = all(c in normPart for c in origPart)
			if origPart == normPart:
				computedStrToEncodedOffsets.extend(normOffset + i for i in range(len(origPart)))
				computedEncodedToStrOffsets.extend(origOffset + i for i in range(len(normPart)))
			elif isReorder:
				computedStrToEncodedOffsets.extend(normOffset + i for i in self._processReordered(origPart, normPart))
				computedEncodedToStrOffsets.extend(origOffset + i for i in self._processReordered(normPart, origPart))
			else:
				computedStrToEncodedOffsets.extend(normOffset for origChar in origPart)
				computedEncodedToStrOffsets.extend(origOffset for normChar in normPart)
			origOffset += len(origPart)
			normOffset += len(normPart)
		self.encoded = normalized

	def _processReordered(self, a: str, b: str) -> Generator[int, None, None]:
		""""Yields the offset in b of every character in a"""
		for char in a:
			index = b.find(char)
			yield index
			b = f"{b[:index]}\0{b[index + 1 :]}"

	@cached_property
	def encodedStringLength(self) -> int:
		"""Returns the length of the string in its normalized representation."""
		return len(self.encoded)

	def strToEncodedOffsets(
			self,
			strStart: int,
			strEnd: int | None = None,
			raiseOnError: bool = False,
	) -> int | Tuple[int]:
		super().strToEncodedOffsets(strStart, strEnd, raiseOnError)
		if strStart == 0:
			resultStart = 0
		else:
			resultStart = self.computedStrToEncodedOffsets[strStart]
		if strEnd is None:
			return resultStart
		elif strStart == strEnd:
			return (resultStart, resultStart)
		else:
			resultEnd = self.computedStrToEncodedOffsets[strEnd]
			return (resultStart, resultEnd)

	def encodedToStrOffsets(
			self,
			encodedStart: int,
			encodedEnd: int | None = None,
			raiseOnError: bool = False
	) -> int | Tuple[int]:
		super().encodedToStrOffsets(encodedStart, encodedEnd, raiseOnError)
		if encodedStart == 0:
			resultStart = 0
		else:
			resultStart = self.computedEncodedToStrOffsets[encodedStart]
		if encodedEnd is None:
			return resultStart
		elif encodedStart == encodedEnd:
			return (resultStart, resultStart)
		else:
			resultEnd = self.computedEncodedToStrOffsets[encodedEnd]
			return (resultStart, resultEnd)


def isUnicodeNormalized(text: str, normalizationForm: str = DEFAULT_UNICODE_NORMALIZATION_ALGORITHM) -> bool:
	"""Convenience function to wrap unicodedata.is_normalized with a default normalization form."""
	return unicodedata.is_normalized(normalizationForm, text)


def unicodeNormalize(text: str, normalizationForm: str = DEFAULT_UNICODE_NORMALIZATION_ALGORITHM) -> str:
	"""Convenience function to wrap unicodedata.normalize with a default normalization form."""
	return unicodedata.normalize(normalizationForm, text)


ENCODINGS_TO_CONVERTERS: dict[str, Type[OffsetConverter]] = {
	WCHAR_ENCODING: WideStringOffsetConverter,
	UTF8_ENCODING: UTF8OffsetConverter,
	"utf_32_le": IdentityOffsetConverter,
	USER_ANSI_CODE_PAGE: IdentityOffsetConverter,
	None: IdentityOffsetConverter,
}


def getOffsetConverter(encoding: str) -> Type[OffsetConverter]:
	try:
		return ENCODINGS_TO_CONVERTERS[encoding]
	except IndexError as e:
		raise LookupError(f"Don't know how to deal with encoding '{encoding}'", e)
