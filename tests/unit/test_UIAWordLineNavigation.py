# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Word line navigation with a UIA provider that wraps when expanding at document end."""

import unittest
from unittest.mock import Mock, patch

import cursorManager
import textInfos
import UIAHandler
from NVDAObjects.UIA.wordDocument import WordDocumentTextInfo


class _LineRange:
	"""Simulate only the UIA range operations used by Word line navigation.

	Collapsed ranges can move to the final insertion point, where line expansion
	wraps to the first line. This models the provider behavior behind the regression.
	"""

	def __init__(self, text: str, start: int, end: int) -> None:
		"""Create a range using explicit line breaks as the simulated visual layout."""
		self.text: str = text
		self.start: int = start
		self.end: int = end
		self.lines: list[tuple[int, int]] = []
		"""Start and end offsets for each simulated line."""
		startOffset: int = 0
		for line in text.splitlines(keepends=True):
			self.lines.append((startOffset, startOffset + len(line)))
			startOffset += len(line)

	def clone(self) -> "_LineRange":
		"""Return an independent range with the same endpoints."""
		return _LineRange(self.text, self.start, self.end)

	def CompareEndpoints(self, endpoint: int, other: "_LineRange", otherEndpoint: int) -> int:
		"""Compare endpoint offsets using the UIA method's naming and semantics."""
		return self._getEndpoint(endpoint) - other._getEndpoint(otherEndpoint)

	def _getEndpoint(self, endpoint: int) -> int:
		return self.start if endpoint == UIAHandler.TextPatternRangeEndpoint_Start else self.end

	def MoveEndpointByRange(self, endpoint: int, other: "_LineRange", otherEndpoint: int) -> None:
		"""Set an endpoint, collapsing the range if the endpoints would cross."""
		value: int = other._getEndpoint(otherEndpoint)
		if endpoint == UIAHandler.TextPatternRangeEndpoint_Start:
			self.start = value
			self.end = max(self.end, value)
		else:
			self.end = value
			self.start = min(self.start, value)

	def _lineIndex(self) -> int:
		return next(i for i, (_, end) in enumerate(self.lines) if self.start < end)

	def ExpandToEnclosingUnit(self, unit: int) -> None:
		"""Expand to a character or line, reproducing line wraparound at document end."""
		if unit == UIAHandler.TextUnit_Character:
			self.end = min(self.start + 1, len(self.text))
			return
		assert unit == UIAHandler.TextUnit_Line
		# Model the suspected Word/Outlook provider bug, not an NVDA fallback.
		if self.start == len(self.text):
			self.start, self.end = self.lines[0]
		else:
			self.start, self.end = self.lines[self._lineIndex()]

	def Move(self, unit: int, count: int) -> int:
		"""Move by characters or lines, including the collapsed-range boundary behavior."""
		if unit == UIAHandler.TextUnit_Character:
			assert self.start == self.end
			oldStart: int = self.start
			self.start = self.end = max(0, min(self.start + count, len(self.text)))
			return self.start - oldStart
		assert unit == UIAHandler.TextUnit_Line
		index: int = self._lineIndex()
		isCollapsed: bool = self.start == self.end
		# UIA permits a collapsed range to move to the document's final insertion point.
		if isCollapsed and count > 0 and index == len(self.lines) - 1:
			self.start = self.end = len(self.text)
			return 1
		target: int = max(0, min(index + count, len(self.lines) - 1))
		if target == index:
			return 0
		self.start, self.end = self.lines[target]
		if isCollapsed:
			self.end = self.start
		return target - index

	def getText(self, length: int) -> str:
		"""Return range text, treating a negative length as unlimited."""
		text: str = self.text[self.start : self.end]
		return text if length < 0 else text[:length]


class TestWordLineNavigation(unittest.TestCase):
	"""Check Word's boundary workarounds against a provider with end-of-document wraparound."""

	def test_expandLineAtDocumentEnd(self) -> None:
		"""Read the final line, including a blank final paragraph, from the end position."""
		testCases: tuple[tuple[str, str], ...] = (
			("first\nlast\r", "last\r"),
			("first\nlast", "last"),
			("first\nlast\n\r", "\r"),
			("\r", "\r"),
		)
		for text, expected in testCases:
			with self.subTest(text=text):
				obj: Mock = Mock()
				# Ctrl+End constructs POSITION_LAST, collapsed at DocumentRange's end.
				obj.UIATextPattern.documentRange = _LineRange(text, 0, len(text))
				info: WordDocumentTextInfo = WordDocumentTextInfo(obj, textInfos.POSITION_LAST)
				self.assertEqual(len(text), info._rangeObj.start)
				info.expand(textInfos.UNIT_LINE)
				self.assertEqual(expected, info.text)
				self.assertEqual(len(text), info._rangeObj.end)

	def test_ctrlEndSpeaksLastLineWithoutMovingSelectionToFirstLine(self) -> None:
		"""Keep the Ctrl+End caret at document end while speaking the final line."""
		text: str = "first\nlast\r"
		obj: Mock = Mock()
		obj.UIATextPattern.documentRange = _LineRange(text, 0, len(text))
		manager: Mock = Mock(isTextSelectionAnchoredAtStart=True)
		manager.makeTextInfo.side_effect = lambda position: WordDocumentTextInfo(obj, position)
		with (
			patch.object(cursorManager, "isScriptWaiting", return_value=False),
			patch.object(cursorManager, "willSayAllResume", return_value=False),
			patch.object(cursorManager.speech, "speakTextInfo") as speak,
		):
			cursorManager.CursorManager._caretMovementScriptHelper(
				manager,
				None,
				textInfos.UNIT_LINE,
				posConstant=textInfos.POSITION_LAST,
			)
		self.assertEqual("last\r", speak.call_args.args[0].text)
		self.assertTrue(manager.selection.isCollapsed)
		self.assertEqual(len(text), manager.selection._rangeObj.start)

	def test_lineMovementAndBoundaries(self) -> None:
		"""Stop at document boundaries and preserve line movement across blank lines and row markers."""
		testCases: tuple[tuple[str, int, int, int, int, int, str], ...] = (
			("first\nlast\r", 6, 6, 1, 0, 6, "last\r"),
			("first\nlast\r", 8, 8, 1, 0, 8, "last\r"),
			("first\nlast\r", 0, 0, -1, 0, 0, "first\n"),
			("first\nlast\r", 0, 0, 1, 1, 6, "last\r"),
			("first\nlast\r", 6, 6, -1, -1, 0, "first\n"),
			("first\nlast\r", 0, 0, 3, 1, 6, "last\r"),
			("first\nlast\n\r", 6, 6, 1, 1, 11, "\r"),
			("first\nlast\n\r", 11, 11, 1, 0, 11, "\r"),
			("\r", 0, 0, 1, 0, 0, "\r"),
			("first\nlast\r", 6, 11, 1, 0, 6, "last\r"),
			("first\n\x07\nlast\r", 0, 0, 1, 1, 8, "last\r"),
			("first\n\x07\nlast\r", 8, 8, -1, -1, 0, "first\n"),
		)
		for text, start, end, count, moved, expectedOffset, expectedText in testCases:
			with self.subTest(text=text, start=start, end=end, count=count):
				obj: Mock = Mock()
				info: WordDocumentTextInfo = WordDocumentTextInfo(
					obj,
					None,
					_rangeObj=_LineRange(text, start, end),
				)
				self.assertEqual(moved, info.move(textInfos.UNIT_LINE, count))
				self.assertEqual(expectedOffset, info._rangeObj.start)
				self.assertEqual(start == end, info.isCollapsed)
				info.expand(textInfos.UNIT_LINE)
				self.assertEqual(expectedText, info.text)
