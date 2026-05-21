# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from functools import cached_property
from textUtils import OffsetConverter, WordSegmenter


class WordSegWithSeparatorOffsetConverter(OffsetConverter):
	"""An offset converter for text with word segmentation separator."""

	sep: str = " "
	computedStrToEncodedOffsets: list[int]
	computedEncodedToStrOffsets: list[int]

	def __init__(self, text: str) -> None:
		super().__init__(text)
		self.newSepIndex: list[int] = []
		self.encoded: str = WordSegmenter(text).segmentedText(sep=self.sep, newSepIndex=self.newSepIndex)

	@cached_property
	def _separatorFlag(self) -> list[bool]:
		isSep = [False] * self.encodedStringLength
		for pos in self.newSepIndex:
			isSep[pos] = True
		return isSep

	@cached_property
	def computedStrToEncodedOffsets(self) -> list[int]:
		"""
		We build an explicit mapping from original string indices to encoded indices
		by marking separator positions in the encoded string and then assigning
		each non-separator encoded slot to the next original-character index.
		The returned list contains the absolute encoded index for each original
		character index.
		"""
		strLen = self.strLength

		# build explicit str -> encoded mapping
		strToEncoded: list[int] = [0] * strLen
		nextStrIndex = 0
		for encodedIndex in range(self.encodedStringLength):
			if not self._separatorFlag[encodedIndex]:
				# assign the current original-char index to this encoded slot
				# then advance to the next original index
				if nextStrIndex >= strLen:
					# defensive: there should not be more non-sep encoded slots than strLen
					# but handle gracefully
					break
				strToEncoded[nextStrIndex] = encodedIndex
				nextStrIndex += 1

		return strToEncoded

	@cached_property
	def computedEncodedToStrOffsets(self) -> list[int]:
		# build explicit encoded -> str mapping
		# semantics: separator positions and the following encoded character
		# both map to the same upcoming original str index (insertion point semantics).
		encodedToStr: list[int] = [0] * self.encodedStringLength
		nextStrIndex = 0
		for encodedIndex in range(self.encodedStringLength):
			if self._separatorFlag[encodedIndex]:
				# map separator to the next original character index (insertion point)
				encodedToStr[encodedIndex] = nextStrIndex
			else:
				# map this encoded character to the current original index,
				# then advance the original index for subsequent positions
				encodedToStr[encodedIndex] = nextStrIndex
				nextStrIndex += 1

		return encodedToStr

	@cached_property
	def encodedStringLength(self) -> int:
		"""Returns the length of the string in its subclass-specific encoded representation."""
		return len(self.encoded)

	def _strOffsetToEncodedOffset(self, offset: int) -> int:
		if offset == self.strLength:
			return self.encodedStringLength
		return self.computedStrToEncodedOffsets[offset]

	def _encodedOffsetToStrOffset(self, offset: int) -> int:
		if offset == self.encodedStringLength:
			return self.strLength
		return self.computedEncodedToStrOffsets[offset]

	def strToEncodedOffsets(
		self,
		strStart: int,
		strEnd: int | None = None,
		raiseOnError: bool = False,
	) -> int | tuple[int, int]:
		super().strToEncodedOffsets(strStart, strEnd, raiseOnError)
		strStart = max(0, min(strStart, self.strLength))
		resultStart = self._strOffsetToEncodedOffset(strStart)
		if strEnd is None:
			return resultStart
		strEnd = max(0, min(strEnd, self.strLength))
		if strStart == strEnd:
			return (resultStart, resultStart)
		resultEnd = self._strOffsetToEncodedOffset(strEnd)
		return (resultStart, resultEnd)

	def encodedToStrOffsets(
		self,
		encodedStart: int,
		encodedEnd: int | None = None,
		raiseOnError: bool = False,
	) -> int | tuple[int, int]:
		super().encodedToStrOffsets(encodedStart, encodedEnd, raiseOnError)
		encodedStart = max(0, min(encodedStart, self.encodedStringLength))
		resultStart = self._encodedOffsetToStrOffset(encodedStart)
		if encodedEnd is None:
			return resultStart
		encodedEnd = max(0, min(encodedEnd, self.encodedStringLength))
		if encodedStart == encodedEnd:
			return (resultStart, resultStart)
		resultEnd = self._encodedOffsetToStrOffset(encodedEnd)
		return (resultStart, resultEnd)
