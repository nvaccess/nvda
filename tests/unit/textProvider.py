# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2023 NV Access Limited, Leonard de Ruijter


"""Fake text provider implementation for testing of code which uses TextInfos.
See the L{BasicTextProvider} class.
"""

from NVDAObjects import NVDAObjectTextInfo
from .objectProvider import PlaceholderNVDAObject
import textInfos
from textInfos.offsets import Offsets
import textUtils
import cursorManager
from typing import Tuple


class BasicTextInfo(NVDAObjectTextInfo):
	# Most of our code use UTF-16 as internal encoding.
	# Mimic this behavior, so we can also implicitly test textUtils module code
	encoding = textUtils.WCHAR_ENCODING

	def __repr__(self):
		return f"{self.__class__.__name__} {self._get_offsets()!r}"

	def _getStoryLength(self):
		# NVDAObjectTextInfo will just return the str length of the story text,.
		# As we are using a custom encoding for this TextInfo, this is incorrect.
		return textUtils.getOffsetConverter(self.encoding)(self._getStoryText()).encodedStringLength

	def _get_offsets(self):
		return (self._startOffset, self._endOffset)

	def updateCaret(self):
		self.obj.selectionOffsets = (self._startOffset, self._startOffset)

	def updateSelection(self):
		self.obj.selectionOffsets = self.offsets

	def _getTextRange(self, start: int, end: int):
		storyText = self._getStoryText()
		converter = textUtils.getOffsetConverter(self.encoding)(storyText)
		strStart, strEnd = converter.encodedToStrOffsets(start, end)
		return storyText[strStart:strEnd]

	def copy(self):
		obj = super().copy()
		obj.encoding = self.encoding
		return obj


class BasicTextProvider(PlaceholderNVDAObject):
	"""An NVDAObject which makes TextInfos based on a provided string of text.
	Example usage:
	>>> obj = BasicTextProvider(text="abcd")
	>>> ti = obj.makeTextInfo(textInfos.POSITION_CARET)
	>>> ti.offsets
	(0, 0)
	>>> ti.expand(textInfos.UNIT_CHARACTER)
	>>> ti.text
	"a"
	>>> ti.offsets
	(0, 1)
	>>> ti.updateSelection()
	>>> obj.selectionOffsets
	(0, 1)
	"""

	TextInfo = BasicTextInfo
	selectionOffsets: Tuple[int, int]

	def __init__(
		self,
		text: str = "",
		selection: Tuple[int, int] = (0, 0),
		encoding: str = textUtils.WCHAR_ENCODING,
	):
		"""
		@param text: The text to provide via TextInfos.
		@param selection: The start and end offsets of the initial selection;
			same start and end is caret with no selection.
		"""
		super().__init__()
		self.basicText = text
		self.selectionOffsets = selection
		self.encoding = encoding

	def __repr__(self):
		return f"{self.__class__.__name__} {self.selectionOffsets!r}"

	def makeTextInfo(self, position):
		if position in (textInfos.POSITION_CARET, textInfos.POSITION_SELECTION):
			start, end = self.selectionOffsets
			position = Offsets(start, end)
		result = super(BasicTextProvider, self).makeTextInfo(position)
		result.encoding = self.encoding
		return result


class CursorManager(cursorManager.CursorManager, BasicTextProvider):
	"""CursorManager which navigates within a provided string of text."""


class MockBlackBoxTextInfo(textInfos.TextInfo):
	"""
	This class mocks a textInfo implementation with hidden internal state. Each character of its internal
	representation maps to one or more characters of python codepoint string,
	and we assume we don't have access to this mapping. We also assume tests don't make use of _startOffset and
	_endOffset fields.
	"""

	_abstract_text = False

	def __init__(self, characters: list[str]):
		self.characters = characters
		self.n = len(characters)
		self._startOffset = 0
		self._endOffset = self.n

	def move(self, unit: str, direction: int, endPoint: str | None = None) -> int:
		if unit != textInfos.UNIT_CHARACTER:
			raise NotImplementedError("This mock TextInfo only supports move by character")
		if self._startOffset != self._endOffset and endPoint is None:
			raise RuntimeError("For non-collapsed textInfo endPoint must be specified.")
		oldOffset = self._endOffset if endPoint == "end" else self._startOffset
		newOffset = oldOffset + direction
		newOffset = min(self.n, max(0, newOffset))
		match endPoint:
			case "start":
				newOffset = min(newOffset, self._endOffset)
				self._startOffset = newOffset
			case "end":
				newOffset = max(newOffset, self._startOffset)
				self._endOffset = newOffset
			case None:
				self._startOffset = self._endOffset = newOffset
			case _:
				raise RuntimeError
		actualMoved = newOffset - oldOffset
		return actualMoved

	def collapse(self, end: bool = False):
		if end:
			self._startOffset = self._endOffset
		else:
			self._endOffset = self._startOffset

	def expand(self, unit: str):
		if unit != textInfos.UNIT_CHARACTER:
			raise NotImplementedError("This mock TextInfo only supports expand by character")
		if self._startOffset != self._endOffset:
			raise RuntimeError("expand() can be called on collapsed textInfo only.")
		self.move(textInfos.UNIT_CHARACTER, 1, "end")

	def compareEndPoints(self, other: textInfos.TextInfo, which: str):
		if not isinstance(other, self.__class__):
			raise NotImplementedError("UMad!")
		tokens = which.split("To")
		if len(tokens) != 2:
			raise ValueError(f"Bad value {which=}")
		firstOffset = self._startOffset if tokens[0] == "start" else self._endOffset
		secondOffset = other._startOffset if tokens[0] == "Start" else other._endOffset
		if firstOffset > secondOffset:
			return 1
		elif firstOffset < secondOffset:
			return -1
		else:
			return 0

	def setEndPoint(self, other: textInfos.TextInfo, which: str):
		if not isinstance(other, self.__class__):
			raise NotImplementedError("UMad!")
		tokens = which.split("To")
		if len(tokens) != 2:
			raise ValueError(f"Bad value {which=}")
		offset = other._startOffset if tokens[0] == "start" else other._endOffset
		if tokens[1] == "Start":
			self._startOffset = offset
			self._endOffset = max(self._endOffset, self._startOffset)
		else:
			self._endOffset = offset
			self._startOffset = min(self._endOffset, self._startOffset)

	def copy(self):
		other = MockBlackBoxTextInfo(self.characters)
		other._startOffset = self._startOffset
		other._endOffset = self._endOffset
		return other

	def _get_text(self) -> str:
		return "".join(self.characters[self._startOffset : self._endOffset])

	def _get_bookmark(self):
		raise NotImplementedError
