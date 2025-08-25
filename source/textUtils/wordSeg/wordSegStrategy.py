# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import ctypes
from ctypes import c_char_p, c_int, POINTER, byref
from abc import ABC, abstractmethod
from functools import lru_cache
from collections.abc import Callable
from typing import Any

from logHandler import log
import textUtils

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
	def getSegmentForOffset(self, text: str, offset: int) -> tuple[int, int] | None:  # TODO: optimize
		"""Return (start inclusive, end exclusive) or None. Offsets are str offsets relative to self.text."""
		pass


class ChineseWordSegmentationStrategy(WordSegmentationStrategy):
	_lib = None

	@classmethod
	@initializerRegistry
	def _ensureLibLoaded(cls):  # TODO: make cppjieba alternative
		"""
		Class-level initializer: attempts to load the versioned cppjieba library and
		set up ctypes signatures.
		"""
		if cls._lib is not None:
			return
		try:
			from NVDAHelper import versionedLibPath

			lib_path = os.path.join(versionedLibPath, "cppjieba.dll")
			cls._lib = ctypes.cdll.LoadLibrary(lib_path)

			# Setup function signatures
			# int initJieba()
			cls._lib.initJieba.restype = c_int
			cls._lib.initJieba.argtypes = []

			# int segmentOffsets(const char* utf8Text, int** outOffsets, int* outLen)
			cls._lib.segmentOffsets.restype = c_int
			cls._lib.segmentOffsets.argtypes = [c_char_p, POINTER(POINTER(c_int)), POINTER(c_int)]

			# void freeOffsets(int* offsets)
			cls._lib.freeOffsets.restype = None
			cls._lib.freeOffsets.argtypes = [POINTER(c_int)]

			cls._lib.initJieba()
		except Exception as e:
			log.debugWarning("Failed to load cppjieba library: %s", e)
			cls._lib = None

	@staticmethod
	@lru_cache(maxsize=256)
	def _callCppjiebaCached(text_utf8: bytes) -> list[int]:
		"""Module-level cached wrapper to call the C library given utf8 bytes."""
		if ChineseWordSegmentationStrategy._lib is None:
			return []
		lib = ChineseWordSegmentationStrategy._lib
		charPtr = POINTER(c_int)()
		outLen = c_int(0)
		try:
			res = lib.segmentOffsets(text_utf8, byref(charPtr), byref(outLen))
			if res != 0 or not bool(charPtr):
				return []
			n = outLen.value
			# read n ints
			offsets = [charPtr[i] for i in range(n)]
			# free memory allocated by C side
			lib.freeOffsets(charPtr)
			return offsets
		except Exception as e:
			log.debugWarning("Exception calling cppjieba: %s", e)
			try:
				if bool(charPtr):
					lib.freeOffsets(charPtr)
			except Exception:
				pass
			return []

	@lru_cache(maxsize=128)
	def _callCPPJieba(self, text: str) -> list[tuple[int, int]] | None:
		data = text.encode("utf-8")
		charPtr = POINTER(c_int)()
		outLen = c_int()
		result = self._lib.segmentOffsets(data, byref(charPtr), byref(outLen))
		if result != 0 or not charPtr:
			return [], []
		n = outLen.value
		char_offsets = [charPtr[i] for i in range(n)]
		self._lib.freeOffsets(charPtr)
		return char_offsets

	def getSegmentForOffset(self, text: str, offset: int) -> tuple[int, int] | None:
		wordEnds = self._callCPPJieba(text)
		if wordEnds is None or not wordEnds:
			return None
		index = next((i for i, end in enumerate(wordEnds) if end > offset))
		if index == 0:
			start = 0
		else:
			start = wordEnds[index - 1]
		end = wordEnds[index] if index < len(wordEnds) else len(text)
		return (start, end)


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

	def getSegmentForOffset(self, text: str, offset: int) -> tuple[int, int] | None:
		return self._calculateUniscribeOffsets(text, offset)
