# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import bisect
import collections

import brailleTables
import config
import languageHandler
import louis
import louisHelper
from textUtils import OffsetConverter, UnicodeNormalizationOffsetConverter, isUnicodeNormalized
from textUtils._braille import _applyOffsetConverter
from textUtils._wordSeg.wordSegUtils import WordSegWithSeparatorOffsetConverter

import braille

from ..constants import (
	SELECTION_SHAPE,
)

#: Named tuple for a region with start and end positions in a buffer
RegionWithPositions = collections.namedtuple("RegionWithPositions", ("region", "start", "end"))


class Region(object):
	"""A region of braille to be displayed.
	Each portion of braille to be displayed is represented by a region.
	The region is responsible for retrieving its text and the cursor and selection positions, translating it into braille cells and handling cursor routing requests relative to its braille cells.
	The :class:`BrailleBuffer` containing this region will call :meth:`update` and expect that :attr:`brailleCells`, :attr:`brailleCursorPos`, :attr:`brailleSelectionStart` and :attr:`brailleSelectionEnd` will be set appropriately.
	:meth:`routeTo` will be called to handle a cursor routing request.
	"""

	rawText: str = ""
	"""The original, raw text of this region."""
	cursorPos: int | None = None
	"""The position of the cursor in :attr:`rawText`, ``None`` if the cursor is not in this region."""
	selectionStart: int | None = None
	"""The start of the selection in :attr:`rawText` (inclusive), ``None`` if there is no selection in this region."""
	selectionEnd: int | None = None
	"""The end of the selection in :attr:`rawText` (exclusive), ``None`` if there is no selection in this region."""
	rawTextTypeforms: list[int] | None = None
	"""liblouis typeform flags for each character in :attr:`rawText`, ``None`` if no typeform info."""
	brailleCursorPos: int | None = None
	"""The position of the cursor in :attr:`brailleCells`, ``None`` if the cursor is not in this region."""
	brailleSelectionStart: int | None = None
	"""The position of the selection start in :attr:`brailleCells`, ``None`` if there is no selection in this region."""
	brailleSelectionEnd: int | None = None
	"""The position of the selection end in :attr:`brailleCells`, ``None`` if there is no selection in this region."""
	hidePreviousRegions: bool = False
	"""Whether to hide all previous regions."""
	focusToHardLeft: bool = False
	"""Whether this region should be positioned at the absolute left of the display when focused."""

	def __init__(self):
		self._languageIndexes: dict[int, str] = {0: self._getDefaultRegionLanguage()}
		"""Language indexes in :attr:`rawText`. The last language is assumed to be the final language in the region."""
		self.brailleCells: list[int] = []
		"""The translated braille representation of this region."""
		self.rawToBraillePos: list[int] = []
		"""A list mapping positions in :attr:`rawText` to positions in :attr:`brailleCells`."""
		self.brailleToRawPos: list[int] = []
		"""A list mapping positions in :attr:`brailleCells` to positions in :attr:`rawText`."""

	def _getDefaultRegionLanguage(self) -> str:
		"""Get the default language for a region."""
		return louisHelper.getTableLanguage(braille.handler.table.fileName) or languageHandler.getLanguage()

	def _getLanguageAtPos(self, pos: int) -> str:
		"""Get the language at a given position in :attr:`rawText` based on :attr:`_languageIndexes`."""
		keys = sorted(self._languageIndexes)
		i = bisect.bisect_right(keys, pos) - 1
		return self._languageIndexes[keys[i]]

	def update(self):
		"""Update this region.
		Subclasses should extend this to update L{rawText}, L{cursorPos}, L{selectionStart} and L{selectionEnd} if necessary.
		The base class method handles translation of L{rawText} into braille, placing the result in L{brailleCells}.
		Typeform information from L{rawTextTypeforms} is used, if any.
		L{rawToBraillePos} and L{brailleToRawPos} are updated according to the translation.
		L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} are similarly updated based on L{cursorPos}, L{selectionStart} and L{selectionEnd}, respectively.
		@postcondition: L{brailleCells}, L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} are updated and ready for rendering.
		"""
		mode = louis.dotsIO
		if config.conf["braille"]["expandAtCursor"] and self.cursorPos is not None:
			mode |= louis.compbrlAtCursor

		converters: list[OffsetConverter] = []
		textToTranslate = self.rawText
		textToTranslateTypeforms = self.rawTextTypeforms
		cursorPos = self.cursorPos

		translationTable = config.conf["braille"]["translationTable"].casefold()
		if translationTable == "auto":
			translationTable = brailleTables.getDefaultTableForCurLang(
				brailleTables.TableType.OUTPUT,
			).casefold()

		if translationTable.startswith("zh"):
			converter = WordSegWithSeparatorOffsetConverter(textToTranslate)
			textToTranslate, textToTranslateTypeforms, cursorPos = _applyOffsetConverter(
				converter,
				textToTranslateTypeforms,
				cursorPos,
			)
			converters.append(converter)
		if config.conf["braille"]["unicodeNormalization"] and not isUnicodeNormalized(textToTranslate):
			converter = UnicodeNormalizationOffsetConverter(textToTranslate)
			textToTranslate, textToTranslateTypeforms, cursorPos = _applyOffsetConverter(
				converter,
				textToTranslateTypeforms,
				cursorPos,
			)
			converters.append(converter)
		self.brailleCells, brailleToRawPos, rawToBraillePos, self.brailleCursorPos = louisHelper.translate(
			[braille.handler.table.fileName, "braille-patterns.cti"],
			textToTranslate,
			typeform=textToTranslateTypeforms,
			mode=mode,
			cursorPos=cursorPos,
		)

		for converter in reversed(converters):
			# Convert liblouis offsets from the most recently transformed text
			# back through each transformation to the original raw text.
			brailleToRawPos = [converter.encodedToStrOffsets(i) for i in brailleToRawPos]
			rawToBraillePos = [
				rawToBraillePos[converter.strToEncodedOffsets(i)] for i in range(converter.strLength)
			]
		self.brailleToRawPos = brailleToRawPos
		self.rawToBraillePos = rawToBraillePos

		if (
			self.selectionStart is not None
			and self.selectionEnd is not None
			and config.conf["braille"]["showSelection"]
		):
			try:
				# Mark the selection.
				self.brailleSelectionStart = self.rawToBraillePos[self.selectionStart]
				if self.selectionEnd >= len(self.rawText):
					self.brailleSelectionEnd = len(self.brailleCells)
				else:
					self.brailleSelectionEnd = self.rawToBraillePos[self.selectionEnd]
				for pos in range(self.brailleSelectionStart, self.brailleSelectionEnd):
					self.brailleCells[pos] |= SELECTION_SHAPE
			except IndexError:
				pass

	def routeTo(self, braillePos):
		"""Handle a cursor routing request.
		For example, this might activate an object or move the cursor to the requested position.
		@param braillePos: The routing position in L{brailleCells}.
		@type braillePos: int
		@note: If routing the cursor, L{brailleToRawPos} can be used to translate L{braillePos} into a position in L{rawText}.
		"""

	def nextLine(self):
		"""Move to the next line if possible."""

	def previousLine(self, start=False):
		"""Move to the previous line if possible.
		@param start: C{True} to move to the start of the line, C{False} to move to the end.
		@type start: bool
		"""

	def __repr__(self):
		return f"{self.__class__.__name__} ({self.rawText!r})"


class TextRegion(Region):
	"""A simple region containing a string of text."""

	def __init__(self, text):
		super(TextRegion, self).__init__()
		self.rawText = text


def rindex(seq, item, start, end):
	for index in range(end - 1, start - 1, -1):
		if seq[index] == item:
			return index
	raise ValueError("%r is not in sequence" % item)
