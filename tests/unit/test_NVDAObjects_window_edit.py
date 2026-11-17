# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for text with fields from rich edit controls, read through the Text Object Model."""

import ctypes
import dataclasses
import unittest
from typing import Any
from unittest.mock import patch

import comtypes.client.dynamic
from comInterfaces import tom
from controlTypes import Role, TextAlign
from NVDAObjects.window.edit import ITextDocumentTextInfo

_FORMAT_CONFIG: dict[str, bool | int] = {
	"detectFormatAfterCursor": True,
	"reportAlignment": False,
	"reportHeadings": False,
	"reportLists": False,
	"reportLineNumber": False,
	"reportFontName": False,
	"reportFontSize": False,
	"fontAttributeReporting": 0,
	"reportSuperscriptsAndSubscripts": False,
	"reportLinks": False,
	"reportColor": False,
}
"""Document formatting with every option off, apart from detecting formatting after the cursor."""


class _CaseInsensitiveAttrsObject:
	"""Falls back to the attribute whose name starts with a lowercase letter.

	For example, ``Duplicate`` falls back to ``duplicate``.
	"""

	def __getattr__(self, name: str) -> Any:
		lowerName = name[:1].lower() + name[1:]
		if lowerName == name:
			raise AttributeError(name)
		return getattr(self, lowerName)


@dataclasses.dataclass
class _Run(_CaseInsensitiveAttrsObject):
	"""A run of text in one font, which also serves as its ``ITextFont``."""

	text: str
	name: str = "Calibri"
	languageID: int = 0


@dataclasses.dataclass
class _Paragraph(_CaseInsensitiveAttrsObject):
	"""A paragraph, which also serves as its ``ITextPara``."""

	runs: list[_Run]
	style: int = tom.tomParaStyleNormal
	alignment: int = tom.tomAlignLeft
	listType: int = tom.tomListNone
	listLevelIndex: int = 0
	numbering: str = ""
	"""The text that ``GetText2`` with ``tomIncludeNumbering`` puts before the paragraph."""


def _paragraph(*runs: str | _Run, **attributes: Any) -> _Paragraph:
	"""A paragraph made of ``runs``, where a string is a run in the default font."""
	return _Paragraph([run if isinstance(run, _Run) else _Run(run) for run in runs], **attributes)


def _spanAt[T](spans: list[tuple[int, int, T]], offset: int) -> tuple[int, int, T]:
	"""The span that contains ``offset``, or the last span when ``offset`` is at the end of the document."""
	for span in spans:
		if span[0] <= offset < span[1]:
			return span
	return spans[-1]


class _Document:
	"""A rich edit document, which serves as its ``ITextDocument``."""

	def __init__(self, *paragraphs: _Paragraph):
		self.text = ""
		self.paragraphSpans: list[tuple[int, int, _Paragraph]] = []
		self.formatSpans: list[tuple[int, int, _Run]] = []
		"""Runs of identical character formatting, which may cross paragraph ends."""
		for paragraph in paragraphs:
			paragraphStart = len(self.text)
			for run in paragraph.runs:
				runStart = len(self.text)
				self.text += run.text
				if self.formatSpans and (previous := self.formatSpans[-1][2]).name == run.name:
					self.formatSpans[-1] = (self.formatSpans[-1][0], len(self.text), previous)
				else:
					self.formatSpans.append((runStart, len(self.text), run))
			self.paragraphSpans.append((paragraphStart, len(self.text), paragraph))

	def range(self, start: int, end: int) -> "_Range":
		return _Range(self, start, end)


class _Range(_CaseInsensitiveAttrsObject):
	"""An ``ITextRange`` over a :class:`_Document`, where lines are paragraphs."""

	def __init__(self, document: _Document, start: int, end: int):
		self._document = document
		self._start = start
		self._end = end

	@property
	def start(self) -> int:
		return self._start

	@start.setter
	def start(self, value: int) -> None:
		self._start = min(max(value, 0), len(self._document.text))
		self._end = max(self._end, self._start)

	@property
	def end(self) -> int:
		return self._end

	@end.setter
	def end(self, value: int) -> None:
		self._end = min(max(value, 0), len(self._document.text))
		self._start = min(self._start, self._end)

	@property
	def duplicate(self) -> "_Range":
		return _Range(self._document, self._start, self._end)

	@property
	def text(self) -> str:
		return self._document.text[self._start : self._end]

	@property
	def para(self) -> _Paragraph:
		return _spanAt(self._document.paragraphSpans, self._start)[2]

	@property
	def font(self) -> _Run:
		return _spanAt(self._document.formatSpans, self._start)[2]

	def collapse(self, bStart: int) -> None:
		if bStart:
			self._end = self._start
		else:
			self._start = self._end

	def expand(self, unit: int) -> int:
		start, end = self._start, self._end
		if unit == tom.tomCharacter:
			if start == end < len(self._document.text):
				self._end += 1
		elif unit == tom.tomStory:
			self._start, self._end = 0, len(self._document.text)
		else:
			spans = self._document.formatSpans if unit == tom.tomCharFormat else self._document.paragraphSpans
			self._start = _spanAt(spans, start)[0]
			self._end = _spanAt(spans, max(end - 1, start))[1]
		return (self._end - self._start) - (end - start)

	def getIndex(self, unit: int) -> int:
		if unit != tom.tomLine:
			raise NotImplementedError(unit)
		for index, (spanStart, spanEnd, _) in enumerate(self._document.paragraphSpans, start=1):
			if spanStart <= self._start < spanEnd:
				return index
		return len(self._document.paragraphSpans)

	def getText2(self, flags: int, text: "ctypes._CArgObject") -> None:
		"""Writes the paragraph's numbering and the text of this range to ``text``."""
		if flags != tom.tomIncludeNumbering:
			raise NotImplementedError(flags)
		text._obj.value = self.para.numbering + self.text


class _RichEdit:
	"""The NVDAObject that owns a :class:`_Document`."""

	def __init__(self, document: _Document):
		self.ITextDocumentObject = document
		self.states: set[Any] = set()


type _Command = str | tuple[str, dict[str, Any] | None]


def _getTextWithFields(
	document: _Document,
	start: int = 0,
	end: int | None = None,
	**formatConfig: bool,
) -> list[_Command]:
	"""Text with fields of ``document`` from ``start`` to ``end``, with each field command as a tuple.

	:param formatConfig: Formatting options to turn on or off, on top of :data:`_FORMAT_CONFIG`.
	"""
	obj = _RichEdit(document)
	if end is None:
		end = len(document.text)
	info = ITextDocumentTextInfo(obj, None, _rangeObj=document.range(start, end))
	# The fake range provides GetText2 itself.
	with patch.object(comtypes.client.dynamic, "Dispatch", new=lambda rangeObj: rangeObj):
		commands = info.getTextWithFields({**_FORMAT_CONFIG, **formatConfig})
	return [
		item if isinstance(item, str) else (item.command, None if item.field is None else dict(item.field))
		for item in commands
	]


def _listItem(level: int, startOffset: int, startOfNode: bool = True) -> _Command:
	return (
		"controlStart",
		{
			"role": Role.LISTITEM,
			"level": level,
			"startOffset": startOffset,
			"_startOfNode": startOfNode,
			"_endOfNode": True,
		},
	)


_LIST_ITEM_END: _Command = ("controlEnd", None)


def _linePrefix(marker: str) -> _Command:
	return ("formatChange", {"line-prefix": marker, "line-prefix_speakAlways": True})


class TestTextWithFields(unittest.TestCase):
	"""Text without headings or lists."""

	def test_formatDetectionOff(self):
		document = _Document(
			_paragraph(_Run("Plain ", "Arial"), _Run("bold\r", "Verdana")),
			_paragraph("Next\r"),
		)
		self.assertEqual(
			_getTextWithFields(document, detectFormatAfterCursor=False, reportFontName=True),
			[("formatChange", {"font-name": "Arial"}), "Plain bold\rNext\r"],
		)

	def test_formatRunsSplitAtParagraphEnds(self):
		document = _Document(
			_paragraph(_Run("Plain ", "Arial"), _Run("bold\r", "Verdana")),
			_paragraph(_Run("Next\r", "Verdana")),
		)
		self.assertEqual(
			_getTextWithFields(document, reportFontName=True),
			[
				("formatChange", {"font-name": "Arial"}),
				"Plain ",
				("formatChange", {"font-name": "Verdana"}),
				"bold\r",
				("formatChange", {"font-name": "Verdana"}),
				"Next\r",
			],
		)

	def test_lineNumbers(self):
		document = _Document(_paragraph("First\r"), _paragraph("Second\r"))
		self.assertEqual(
			_getTextWithFields(document, reportLineNumber=True),
			[
				("formatChange", {"line-number": 1}),
				"First\r",
				("formatChange", {"line-number": 2}),
				"Second\r",
			],
		)

	def test_alignment(self):
		document = _Document(_paragraph("Left\r"), _paragraph("Centered\r", alignment=tom.tomAlignCenter))
		self.assertEqual(
			_getTextWithFields(document, reportAlignment=True),
			[
				("formatChange", {"text-align": TextAlign.LEFT}),
				"Left\r",
				("formatChange", {"text-align": TextAlign.CENTER}),
				"Centered\r",
			],
		)

	def test_collapsedRange(self):
		document = _Document(_paragraph("Text\r"))
		self.assertEqual(_getTextWithFields(document, start=2, end=2), [])

	def test_rangeFromInsideRunToDocumentEnd(self):
		document = _Document(_paragraph(_Run("Plain ", "Arial"), _Run("bold\r", "Verdana")))
		self.assertEqual(
			_getTextWithFields(document, start=2, reportFontName=True),
			[
				("formatChange", {"font-name": "Arial"}),
				"ain ",
				("formatChange", {"font-name": "Verdana"}),
				"bold\r",
			],
		)


class TestHeadingsAndLists(unittest.TestCase):
	def test_headingLevels(self):
		document = _Document(
			_paragraph("Title\r", style=tom.tomParaStyleHeading1),
			_paragraph("Deep\r", style=tom.tomParaStyleHeading9),
			_paragraph("Body\r"),
		)
		self.assertEqual(
			_getTextWithFields(document, reportHeadings=True),
			[
				("formatChange", {"heading-level": 1}),
				"Title\r",
				("formatChange", {"heading-level": 9}),
				"Deep\r",
				("formatChange", {}),
				"Body\r",
			],
		)

	def test_bulletedItems(self):
		document = _Document(
			_paragraph("Intro\r"),
			_paragraph("One ", _Run("two\r", "Arial"), listType=tom.tomListBullet),
			_paragraph("Nested\r", listType=tom.tomListBullet, listLevelIndex=1),
		)
		self.assertEqual(
			_getTextWithFields(document, reportLists=True),
			[
				("formatChange", {}),
				"Intro\r",
				_listItem(level=1, startOffset=6),
				_linePrefix("\u2022"),
				"One ",
				("formatChange", {}),
				"two\r",
				_LIST_ITEM_END,
				_listItem(level=2, startOffset=14),
				_linePrefix("\u2022"),
				"Nested\r",
				_LIST_ITEM_END,
			],
		)

	def test_numberedItem(self):
		document = _Document(
			_paragraph("First\r", listType=tom.tomListNumberAsArabic | tom.tomListPeriod, numbering="1.\t"),
		)
		self.assertEqual(
			_getTextWithFields(document, reportLists=True),
			[_listItem(level=1, startOffset=0), _linePrefix("1."), "First\r", _LIST_ITEM_END],
		)

	def test_characterBullet(self):
		arrowhead = "\u27a2"
		document = _Document(_paragraph("Arrow\r", listType=ord(arrowhead)))
		self.assertEqual(
			_getTextWithFields(document, reportLists=True),
			[_listItem(level=1, startOffset=0), _linePrefix(arrowhead), "Arrow\r", _LIST_ITEM_END],
		)

	def test_itemWithoutNumber(self):
		document = _Document(_paragraph("Item\r", listType=tom.tomListBullet | tom.tomListNoNumber))
		self.assertEqual(
			_getTextWithFields(document, reportLists=True),
			[_listItem(level=1, startOffset=0), ("formatChange", {}), "Item\r", _LIST_ITEM_END],
		)

	def test_rangeStartingInsideItem(self):
		document = _Document(_paragraph("One two\r", listType=tom.tomListBullet))
		self.assertEqual(
			_getTextWithFields(document, start=4, reportLists=True),
			[
				_listItem(level=1, startOffset=0, startOfNode=False),
				("formatChange", {}),
				"two\r",
				_LIST_ITEM_END,
			],
		)

	def test_listReportingOff(self):
		document = _Document(_paragraph("Item\r", listType=tom.tomListBullet))
		self.assertEqual(
			_getTextWithFields(document),
			[_linePrefix("\u2022"), "Item\r"],
		)

	def test_formatDetectionOffInItem(self):
		document = _Document(_paragraph("One ", _Run("two\r", "Arial"), listType=tom.tomListBullet))
		self.assertEqual(
			_getTextWithFields(document, detectFormatAfterCursor=False, reportLists=True),
			[_listItem(level=1, startOffset=0), _linePrefix("\u2022"), "One two\r", _LIST_ITEM_END],
		)

	def test_formatDetectionOffFromItemIntoLaterParagraphs(self):
		document = _Document(_paragraph("Item\r", listType=tom.tomListBullet), _paragraph("After\r"))
		self.assertEqual(
			_getTextWithFields(document, detectFormatAfterCursor=False, reportLists=True),
			[_listItem(level=1, startOffset=0), _linePrefix("\u2022"), "Item\rAfter\r", _LIST_ITEM_END],
		)
