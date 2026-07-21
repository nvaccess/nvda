# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from ctypes import (
	ArgumentError,
	CDLL,
	c_bool,
	c_char_p,
	c_int,
	create_string_buffer,
	cdll,
	POINTER,
	byref,
)
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from typing import Any, ParamSpec, TypeVar
import re
import unicodedata

import brailleTables
import config
import languageHandler
import NVDAHelper
import textUtils
from NVDAState import ReadPaths
from logHandler import log


_P = ParamSpec("_P")
_R = TypeVar("_R")
_InitializerEntry = tuple[str, str, Callable[..., Any], tuple[Any, ...], dict[str, Any]]
_initializerList: list[_InitializerEntry] = []
_CPPJIEBA_LOAD_EXCEPTIONS = (
	AttributeError,
	OSError,
	TypeError,
	ValueError,
)
_CPPJIEBA_CALL_EXCEPTIONS = (
	ArgumentError,
	OSError,
	TypeError,
	ValueError,
)


def iterInitializers() -> Iterator[_InitializerEntry]:
	"""Iterate over registered initializer entries."""
	return iter(_initializerList)


def initializerRegistry(func: Callable[_P, _R]) -> Callable[_P, _R]:
	"""
	A decorator to register an initializer function.
	We save (func.__module__, func.__qualname__, func) so that during package initialize()
	we can dynamically resolve the callable from the module.
	This handles classmethod/staticmethod ordering issues.
	"""
	_initializerList.append((func.__module__, func.__qualname__, func, (), {}))
	return func


def _loadCppJiebaLib() -> CDLL:
	lib = cdll.LoadLibrary(ReadPaths.cppjiebaDll)

	# bool initJieba(const char* dictDir)
	lib.initJieba.restype = c_bool
	lib.initJieba.argtypes = [c_char_p]

	# bool calculateWordOffsets(const char* text, int** wordEndOffsets, int* outLen)
	lib.calculateWordOffsets.restype = c_bool
	lib.calculateWordOffsets.argtypes = [c_char_p, POINTER(POINTER(c_int)), POINTER(c_int)]

	# bool insertUserWord(const char* word, int freq, const char* tag)
	lib.insertUserWord.restype = c_bool
	lib.insertUserWord.argtypes = [c_char_p, c_int, c_char_p]

	# bool deleteUserWord(const char* word, const char* tag)
	lib.deleteUserWord.restype = c_bool
	lib.deleteUserWord.argtypes = [c_char_p, c_char_p]

	# bool find(const char* word)
	lib.find.restype = c_bool
	lib.find.argtypes = [c_char_p]

	# void freeOffsets(int* offsets)
	lib.freeOffsets.restype = None
	lib.freeOffsets.argtypes = [POINTER(c_int)]

	return lib


def _getConfiguredBrailleOutputTable() -> str:
	tableName = config.conf["braille"]["translationTable"]
	if tableName == "auto":
		return brailleTables.getDefaultTableForCurLang(brailleTables.TableType.OUTPUT)
	return tableName


def _freeCppJiebaOffsets(lib: CDLL, charPtr: POINTER(c_int)) -> None:
	if not bool(charPtr):
		return
	try:
		lib.freeOffsets(charPtr)
	except _CPPJIEBA_CALL_EXCEPTIONS:
		log.exception("Failed to free cppjieba offsets")


def _callCppJiebaLib(lib: CDLL, textUtf8: bytes) -> list[int]:
	charPtr = POINTER(c_int)()
	outLen = c_int(0)
	try:
		success: bool = lib.calculateWordOffsets(textUtf8, byref(charPtr), byref(outLen))
	except _CPPJIEBA_CALL_EXCEPTIONS:
		log.exception("Exception calling cppjieba")
		_freeCppJiebaOffsets(lib, charPtr)
		return []

	if not success or not bool(charPtr) or outLen.value <= 0:
		_freeCppJiebaOffsets(lib, charPtr)
		return []

	try:
		return [charPtr[i] for i in range(outLen.value)]
	finally:
		_freeCppJiebaOffsets(lib, charPtr)


class WordSegmentationStrategy(ABC):
	"""Abstract base class for word segmentation strategies."""

	def __init__(self, text: str, encoding: str | None = None) -> None:
		self.text: str = text
		self.encoding: str | None = encoding
		self.wordEnds: list[int] = []

	@abstractmethod
	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:
		"""Return (start inclusive, end exclusive) or None. Offsets are str offsets relative to self.text."""
		pass

	def segmentedText(self, sep: str = " ", newSepIndex: list[int] | None = None) -> str:
		"""Segmented result with separators.

		The default returns the text unchanged; only strategies that insert separators
		for braille output (e.g. Chinese) override this.
		"""
		return self.text

	def getWordOffsetRange(
		self,
		offset: int,
	) -> tuple[int, int] | None:
		"""Helper to get word offset range from a list of word end offsets."""
		if not self.wordEnds:
			return None
		index = next((i for i, end in enumerate(self.wordEnds) if end > offset), len(self.wordEnds) - 1)
		start = 0 if index == 0 else self.wordEnds[index - 1]
		end = self.wordEnds[index]
		return (start, end)

	@classmethod
	def isUsingRelatedLanguage(cls) -> bool:
		"""Returns True if this strategy is for the current language."""

		if not hasattr(cls, "_LANGUAGE_PATTERN"):
			return False

		return any(
			re.match(cls._LANGUAGE_PATTERN, language)  # ty: ignore[no-matching-overload]
			for language in (
				languageHandler.getWindowsLanguage(),
				languageHandler.getLanguage(),
				_getConfiguredBrailleOutputTable(),
			)
		)


class UniscribeWordSegmentationStrategy(WordSegmentationStrategy):
	"""Windows Uniscribe-based segmentation (calls NVDAHelper.localLib.calculateWordOffsets)."""

	# Copied from OffsetsTextInfo to preserve existing Uniscribe behavior.
	def _calculateUniscribeOffsets(
		self,
		lineText: str,
		relOffset: int,
	) -> tuple[int, int] | None:
		"""
		Calculates the bounds of a unit at an offset within a given string of text
		using the Windows uniscribe  library, also used in Notepad, for example.
		Units supported are character and word.
		:param lineText: the text string to analyze
		:param relOffset: the character offset within the text string at which to calculate the bounds.
		"""

		helperFunc = NVDAHelper.localLib.calculateWordOffsets

		relStart = c_int()
		relEnd = c_int()
		# uniscribe does some strange things
		# when you give it a string  with not more than two alphanumeric chars in a row.
		# Inject two alphanumeric characters at the end to fix this
		uniscribeLineText = lineText + "xx"
		# We can't rely on len(lineText) to calculate the length of the line.
		offsetConverter = textUtils.WideStringOffsetConverter(lineText)
		lineLength = offsetConverter.encodedStringLength
		if self.encoding != textUtils.WCHAR_ENCODING:
			# We need to convert the str based line offsets to wide string offsets.
			relOffset = offsetConverter.strToEncodedOffsets(relOffset, relOffset)[0]
		uniscribeLineLength = lineLength + 2
		if helperFunc(
			uniscribeLineText,
			uniscribeLineLength,
			relOffset,
			byref(relStart),
			byref(relEnd),
		):
			relStart = relStart.value
			relEnd = min(lineLength, relEnd.value)
			if self.encoding != textUtils.WCHAR_ENCODING:
				# We need to convert the uniscribe based offsets to str offsets.
				relStart, relEnd = offsetConverter.encodedToStrOffsets(relStart, relEnd)
			return (relStart, relEnd)
		return None

	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:
		return self._calculateUniscribeOffsets(self.text, offset)


class ChineseWordSegmentationStrategy(WordSegmentationStrategy):
	_lib: CDLL | None = None
	_LANGUAGE_PATTERN: re.Pattern[str] = re.compile(r"^zh", re.IGNORECASE)
	_PUNCTUATION_CATEGORY_PREFIXES: str = "pP"
	_OTHER_PATTERN_CATEGORY: str = "So"

	@classmethod
	@initializerRegistry
	def _initCppJieba(
		cls,
		forceInit: bool = False,
	) -> None:
		"""
		Class-level initializer: attempts to load the versioned cppjieba library and
		set up ctypes signatures.
		"""
		if cls._lib:
			return

		if not forceInit:
			documentNavigationConf = config.conf["documentNavigation"]
			shouldInit = (
				documentNavigationConf["wordSegmentationStandard"].calculated()
				== config.featureFlagEnums.WordNavigationUnitFlag.CHINESE
				or cls.isUsingRelatedLanguage()
				or documentNavigationConf["initWordSegForUnusedLang"]
			)
			if not shouldInit:
				return
		try:
			lib = _loadCppJiebaLib()
		except _CPPJIEBA_LOAD_EXCEPTIONS:
			log.exception("Failed to load cppjieba library")
			cls._lib = None
			return

		dictsDir = ReadPaths.cppjiebaDictsDir
		try:
			dictsDirBytes = dictsDir.encode("utf-8")
			dictDir = create_string_buffer(dictsDirBytes)
			initialized = lib.initJieba(dictDir)
		except _CPPJIEBA_CALL_EXCEPTIONS:
			log.exception(f"Failed to initialize cppjieba library with dictionary path: {dictsDir}")
			cls._lib = None
			return
		if not initialized:
			log.debugWarning(f"Failed to initialize cppjieba library with dictionary path: {dictsDir}")
			cls._lib = None
			return
		cls._lib = lib

	def _callCppJieba(self) -> list[int]:
		"""
		Instance method: encode self.text and call cppjieba.
		Returns list[int] on success, or an empty list on failure.
		"""
		try:
			data = self.text.encode("utf-8")
		except UnicodeEncodeError:
			log.exception("Failed to encode text for cppjieba")
			return []

		if self._lib is None:
			return []
		return _callCppJiebaLib(self._lib, data)

	def segmentedText(self, sep: str = " ", newSepIndex: list[int] | None = None) -> str:
		"""Segments the text using the word end indices."""

		if len(self.wordEnds) <= 1:
			return self.text

		result = ""
		for sepIndex in range(len(self.wordEnds) - 1):
			preIndex = 0 if sepIndex == 0 else self.wordEnds[sepIndex - 1]
			curIndex = self.wordEnds[sepIndex]
			postIndex = self.wordEnds[sepIndex + 1]

			# append the token before the potential separator position
			result += self.text[preIndex:curIndex]

			# quick checks: avoid adding duplicate separator if already present
			if result.endswith(sep) or self.text[curIndex:postIndex].startswith(sep):
				# separator already present at either side, skip adding
				continue

			# Determine whether any punctuation forbids a separator
			noSep = (
				unicodedata.category(self.text[curIndex - 1])[0] in self._PUNCTUATION_CATEGORY_PREFIXES
				or unicodedata.category(self.text[curIndex - 1]) == self._OTHER_PATTERN_CATEGORY
				or unicodedata.category(self.text[curIndex])[0] in self._PUNCTUATION_CATEGORY_PREFIXES
				or unicodedata.category(self.text[curIndex]) == self._OTHER_PATTERN_CATEGORY
			)

			if not noSep:
				# If neither side forbids the separator, add it
				result += sep
				if newSepIndex is not None:
					newSepIndex.append(len(result) - len(sep))
		# append the final trailing token after the loop
		result += self.text[curIndex:postIndex]

		return result

	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:
		if self.encoding == textUtils.WCHAR_ENCODING:
			offsetConverter = textUtils.WideStringOffsetConverter(self.text)
			strOffset = offsetConverter.encodedToStrOffsets(offset, offset)[0]
			offsets = self.getWordOffsetRange(strOffset)
			if offsets is None:
				return None
			return offsetConverter.strToEncodedOffsets(*offsets)
		return self.getWordOffsetRange(offset)

	def __init__(self, text: str, encoding: str | None = None) -> None:
		super().__init__(text, encoding)
		self.wordEnds = self._callCppJieba()


class IcuWordSegmentationStrategy(WordSegmentationStrategy):
	"""ICU-based word segmentation (Windows built-in ICU library).

	Word boundaries follow Unicode Standard Annex #29 default rules plus automatic
	dictionary-based segmentation selected by the script of the text.
	SegmentedText returns the text unchanged (no braille separator insertion).
	"""

	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:
		from textUtils import icu

		if self.encoding == textUtils.WCHAR_ENCODING:
			return icu.calculateWordOffsets(self.text, offset)
		# Convert the str offset to a UTF-16 offset for ICU, then convert the result back.
		offsetConverter = textUtils.WideStringOffsetConverter(self.text)
		wideOffset = offsetConverter.strToEncodedOffsets(offset, offset)[0]
		result = icu.calculateWordOffsets(self.text, wideOffset)
		if result is None:
			return None
		return offsetConverter.encodedToStrOffsets(*result)
