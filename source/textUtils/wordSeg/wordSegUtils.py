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

	def __init__(self, text: str):
		super().__init__(text)
		self.newSepIndex: list[int] = []
		self.encoded = WordSegmenter(text).segmentedText(sep=self.sep, newSepIndex=self.newSepIndex)

	@property
	def computedStrToEncodedOffsets(self) -> list[int]:
		"""
		Compute a list of offsets so that:
			encodedIndex = strIndex + relevantStrToEncodedOffsets[strIndex]

		We build an explicit mapping from original string indices to encoded indices
		by marking separator positions in the encoded string and then assigning
		each non-separator encoded slot to the next original-character index.
		The returned list contains the delta (encodedIndex - strIndex) for each
		original index.
		"""
		strLen = self.strLength
		encodedLen = self.encodedStringLength

		# validate separator positions (optional but makes bugs obvious)
		for pos in self.newSepIndex:
			if pos < 0 or pos >= encodedLen:
				raise ValueError(f"separator position {pos} out of range for encoded length {encodedLen}")

		# mark which encoded positions are separators
		isSep = [False] * encodedLen
		for pos in self.newSepIndex:
			isSep[pos] = True

		# build explicit str -> encoded mapping
		strToEncoded: list[int] = [0] * strLen
		nextStrIndex = 0
		for encodedIndex in range(encodedLen):
			if not isSep[encodedIndex]:
				# assign the current original-char index to this encoded slot
				# then advance to the next original index
				if nextStrIndex >= strLen:
					# defensive: there should not be more non-sep encoded slots than strLen
					# but handle gracefully
					break
				strToEncoded[nextStrIndex] = encodedIndex
				nextStrIndex += 1

		return strToEncoded

	@property
	def computedEncodedToStrOffsets(self) -> list[int]:
		encodedLen = self.encodedStringLength

		# validate separator positions
		for pos in self.newSepIndex:
			if pos < 0 or pos >= encodedLen:
				raise ValueError(f"separator position {pos} out of range for encoded length {encodedLen}")

		# mark which encoded positions are separators
		isSep = [False] * encodedLen
		for pos in self.newSepIndex:
			isSep[pos] = True

		# build explicit encoded -> str mapping
		# semantics: separator positions and the following encoded character
		# both map to the same upcoming original str index (insertion point semantics).
		encodedToStr: list[int] = [0] * encodedLen
		nextStrIndex = 0
		for encodedIndex in range(encodedLen):
			if isSep[encodedIndex]:
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

	def strToEncodedOffsets(
		self,
		strStart: int,
		strEnd: int | None = None,
		raiseOnError: bool = False,
	) -> int | tuple[int, int]:
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
		raiseOnError: bool = False,
	) -> int | tuple[int]:
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
