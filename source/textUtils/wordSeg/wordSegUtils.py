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
		self.computedStrToEncodedOffsets = list(range(self.strLength))
		for i in range(len(self.computedStrToEncodedOffsets)):
			self.computedStrToEncodedOffsets[i] += self._relevantStrToEncodedOffsets[i]
		self.computedEncodedToStrOffsets = list(range(self.encodedStringLength))
		for j in range(len(self.computedEncodedToStrOffsets)):
			self.computedEncodedToStrOffsets[j] += self._relevantEncodedToStrOffsets[j]

	@property
	def _relevantStrToEncodedOffsets(self) -> list[int]:
		relevantIndex: list[int] = [0 for _ in range(self.strLength)]
		j = 0
		m = len(self.newSepIndex)
		for i in range(self.strLength):
			while j < m and self.newSepIndex[j] <= i + j:
				j += 1
			relevantIndex[i] = j
		return relevantIndex

	@property
	def _relevantEncodedToStrOffsets(self) -> list[int]:
		relevantIndex: list[int] = [0 for _ in range(self.encodedStringLength)]
		j = 0
		m = len(self.newSepIndex)
		for i in range(self.encodedStringLength):
			while j < m and self.newSepIndex[j] < i + j:
				j += 1
			relevantIndex[i] = -j
		return relevantIndex

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
