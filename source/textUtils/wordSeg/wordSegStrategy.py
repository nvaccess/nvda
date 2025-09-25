# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import ctypes
from ctypes import (
	c_bool,
	c_char_p,
	c_int,
	create_string_buffer,
	POINTER,
	byref,
)
from abc import ABC, abstractmethod
from functools import lru_cache
from collections.abc import Callable
from typing import Any

import textUtils
from logHandler import log


# Initializer registry (robust: saves module + qualname + original function + args/kwargs)
# Each entry: (module_name: str, qualname: str, func_obj: Callable, args: tuple, kwargs: dict)
initializerList: list[tuple[str, str, Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = []


def initializerRegistry(*decorator_args, **decorator_kwargs):
	"""
	A decorator to register an initializer function.
	Usage:
		@initializerRegistry
		def f(): ...
	or with arguments:
		@initializerRegistry(arg1, arg2, kw=val)
		def f(...): ...
	We save (func.__module__, func.__qualname__, func, args, kwargs) so that during
	package initialize() we can dynamically resolve the callable from the module
	(this handles classmethod/staticmethod ordering issues).
	"""
	if decorator_args and callable(decorator_args[0]) and len(decorator_args) == 1 and not decorator_kwargs:
		func = decorator_args[0]
		initializerList.append((func.__module__, func.__qualname__, func, (), {}))
		return func

	def _decorator(func: Callable[..., Any]):
		initializerList.append((func.__module__, func.__qualname__, func, decorator_args, decorator_kwargs))
		return func

	return _decorator


class WordSegmentationStrategy(ABC):
	"""Abstract base class for word segmentation strategies."""

	def __init__(self, text: str, encoding: str | None = None):
		self.text = text
		self.encoding = encoding

	@abstractmethod
	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:  # TODO: optimize
		"""Return (start inclusive, end exclusive) or None. Offsets are str offsets relative to self.text."""
		pass

	@abstractmethod
	def segmentedText(self, sep: str = " ", newSepIndex: list[int] | None = None) -> str:
		"""Segmented result with separators."""
		pass


class UniscribeWordSegmentationStrategy(WordSegmentationStrategy):
	"""Windows Uniscribe-based segmentation (calls NVDAHelper.localLib.calculateWordOffsets)."""

	# Copied from OffsetTextInfos. TODO: optimize
	def _calculateUniscribeOffsets(
		self,
		lineText: str,
		relOffset: int,
	) -> tuple[int, int] | None:
		"""
		Calculates the bounds of a unit at an offset within a given string of text
		using the Windows uniscribe  library, also used in Notepad, for example.
		Units supported are character and word.
		@param lineText: the text string to analyze
		@param relOffset: the character offset within the text string at which to calculate the bounds.
		"""

		import NVDAHelper

		helperFunc = NVDAHelper.localLib.calculateWordOffsets

		relStart = ctypes.c_int()
		relEnd = ctypes.c_int()
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
			ctypes.byref(relStart),
			ctypes.byref(relEnd),
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

	def segmentedText(self, sep: str = " ", newSepIndex: list[int] | None = None) -> str:
		return self.text


class ChineseWordSegmentationStrategy(WordSegmentationStrategy):
	_lib = None

	@classmethod
	@initializerRegistry
	def _initCppJieba(cls):  # TODO: make cppjieba alternative
		"""
		Class-level initializer: attempts to load the versioned cppjieba library and
		set up ctypes signatures.
		"""
		import config

		if not config.conf["general"]["language"].startswith("zh") or cls._lib is not None:
			return
		try:
			from NVDAState import ReadPaths

			lib_path = os.path.join(ReadPaths.coreArchLibPath, "cppjieba.dll")
			cls._lib = ctypes.cdll.LoadLibrary(lib_path)

			# Setup function signatures
			# bool initJieba(const char* dictDir)
			cls._lib.initJieba.restype = c_bool
			cls._lib.initJieba.argtypes = [c_char_p]

			# bool calculateWordOffsets(const char* text, int** wordEndOffsets, int* outLen)
			cls._lib.calculateWordOffsets.restype = c_bool
			cls._lib.calculateWordOffsets.argtypes = [c_char_p, POINTER(POINTER(c_int)), POINTER(c_int)]

			# bool insertUserWord(const char* word, int freq, const char* tag)
			cls._lib.insertUserWord.restype = c_bool
			cls._lib.insertUserWord.argtypes = [c_char_p, c_int, c_char_p]

			# bool deleteUserWord(const char* word, const char* tag)
			cls._lib.deleteUserWord.restype = c_bool
			cls._lib.deleteUserWord.argtypes = [c_char_p, c_char_p]

			# bool find(const char* word)
			cls._lib.find.restype = c_bool
			cls._lib.find.argtypes = [c_char_p]

			# void freeOffsets(int* offsets)
			cls._lib.freeOffsets.restype = None
			cls._lib.freeOffsets.argtypes = [POINTER(c_int)]

			# Initialize with dictionary path
			import globalVars

			DICTS_DIR = os.path.join(globalVars.appDir, "cppjieba", "dicts")
			DICTS_DIR_BYTES = DICTS_DIR.encode("utf-8")
			dictDir = create_string_buffer(DICTS_DIR_BYTES)
			cls._lib.initJieba(dictDir)
		except Exception as e:
			log.debugWarning("Failed to load cppjieba library: %s", e)
			cls._lib = None

	@lru_cache(maxsize=256)
	def _callCppjiebaCached(self, text_utf8: bytes) -> list[int] | None:
		if self._lib is None:
			return None

		charPtr = POINTER(c_int)()
		outLen = c_int(0)

		try:
			success: bool = self._lib.calculateWordOffsets(text_utf8, byref(charPtr), byref(outLen))
			if not success or not bool(charPtr) or outLen.value <= 0:
				return None

			try:
				n = outLen.value
				offsets = [charPtr[i] for i in range(n)]
				return offsets
			finally:
				self._lib.freeOffsets(charPtr)
		except Exception as e:
			log.debugWarning("Exception calling cppjieba: %s", e)
			try:
				if bool(charPtr):
					self._lib.freeOffsets(charPtr)
			except Exception:
				pass
			return None

	def _callCPPJieba(self) -> list[int] | None:
		"""
		Instance method: encode self.text and call cppjieba.
		Returns list[int] on success, None on failure.
		Uses LRU cache keyed by utf-8 bytes.
		"""
		data = self.text.encode("utf-8")

		if getattr(self, "_lib", None) is ChineseWordSegmentationStrategy._lib:
			return self._callCppjiebaCached(data)
		else:
			if self._lib is None:
				return None

			charPtr = POINTER(c_int)()
			outLen = c_int(0)
			try:
				success: bool = self._lib.calculateWordOffsets(data, byref(charPtr), byref(outLen))
				if not success or not bool(charPtr) or outLen.value <= 0:
					return None

				try:
					n = outLen.value
					return [charPtr[i] for i in range(n)]
				finally:
					self._lib.freeOffsets(charPtr)
			except Exception as e:
				log.debugWarning("Exception calling cppjieba: %s", e)
				try:
					if bool(charPtr):
						self._lib.freeOffsets(charPtr)
				except Exception:
					pass
				return None

	# Punctuation that should NOT have a separator BEFORE it (no space before these marks)
	NO_SEP_BEFORE = {
		# Common Chinese fullwidth punctuation
		"。",
		"，",
		"、",
		"；",
		"：",
		"？",
		"！",
		"…",
		"...",
		"—",
		"–",
		"——",
		"）",
		"】",
		"》",
		"〉",
		"」",
		"』",
		"”",
		"’",
		"％",
		"‰",
		"￥",
		# Common ASCII / halfwidth punctuation
		".",
		",",
		";",
		":",
		"?",
		"!",
		"%",
		".",
		")",
		"]",
		"}",
		">",
		'"',
		"'",
	}

	# Punctuation that should NOT have a separator AFTER it (no space after these marks)
	NO_SEP_AFTER = {
		# Common Chinese fullwidth opening/leading punctuation
		"（",
		"【",
		"《",
		"〈",
		"「",
		"『",
		"“",
		"‘",
		# Common ASCII / halfwidth opening/leading punctuation
		"(",
		"[",
		"{",
		"<",
		'"',
		"'",
		# Currency and prefix-like symbols that typically bind to the following token
		"$",
		"€",
		"£",
		"¥",
		"₹",
		# Social/identifier prefixes
		"@",
		"#",
		"&",
	}

	def segmentedText(self, sep: str = " ", newSepIndex: list[int] | None = None) -> str:
		"""Segments the text using the word end indices."""
		if len(self.wordEndIndex) <= 1:
			return self.text

		result = ""
		for sepIndex in range(len(self.wordEndIndex) - 1):
			preIndex = 0 if sepIndex == 0 else self.wordEndIndex[sepIndex - 1]
			curIndex = self.wordEndIndex[sepIndex]
			postIndex = self.wordEndIndex[sepIndex + 1]

			# append the token before the potential separator position
			result += self.text[preIndex:curIndex]

			# quick checks: avoid adding duplicate separator if already present
			if result.endswith(sep) or self.text[curIndex:postIndex].startswith(sep):
				# separator already present at either side -> skip adding
				continue

			# slice to check the next token (text between curIndex and postIndex)
			nextSlice = self.text[curIndex:postIndex]

			# Determine whether any punctuation forbids a separator BEFORE the next token
			noSepBefore = any(nextSlice.startswith(s) for s in self.NO_SEP_BEFORE)
			# Determine whether any punctuation forbids a separator AFTER the current result
			noSepAfter = any(result.endswith(s) for s in self.NO_SEP_AFTER)

			if not (noSepBefore or noSepAfter):
				# If neither side forbids the separator, add it
				result += sep
				if newSepIndex is not None:
					newSepIndex.append(len(result) - len(sep))
		else:
			# append the final trailing token after the loop
			result += self.text[curIndex:postIndex]

		return result

	def getSegmentForOffset(self, offset: int) -> tuple[int, int] | None:
		wordEnds = self._callCPPJieba()
		if wordEnds is None or not wordEnds:
			return
		index = next((i for i, end in enumerate(wordEnds) if end > offset))
		if index == 0:
			start = 0
		else:
			start = wordEnds[index - 1]
		end = wordEnds[index] if index < len(wordEnds) else len(self.text)
		return (start, end)

	def __init__(self, text, encoding=None):
		super().__init__(text, encoding)
		self.wordEndIndex = self._callCPPJieba()
