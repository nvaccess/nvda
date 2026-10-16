# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for formatting and link lookups in PowerPoint text frames."""

import unittest
from types import SimpleNamespace
from typing import Any

from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


class TestTextFrameTextInfo(unittest.TestCase):
	def setUp(self) -> None:
		self.text = "Hello world"
		self.run = SimpleNamespace(
			start=1,
			length=len(self.text),
			font=SimpleNamespace(),
			paragraphFormat=SimpleNamespace(bullet=SimpleNamespace(type=0)),
		)
		self.textRange = SimpleNamespace(
			length=len(self.text),
			runs=lambda: [self.run],
			characters=lambda start, length: SimpleNamespace(
				text=self.text[start - 1 : start - 1 + length],
				font=self.run.font,
				paragraphFormat=self.run.paragraphFormat,
			),
		)
		frame = _object(powerpnt.TextFrame, ppObject=SimpleNamespace(textRange=self.textRange))
		self.info = _object(powerpnt.TextFrameTextInfo, obj=frame, _startOffset=0, _endOffset=len(self.text))
		self.formatConfig = dict.fromkeys(
			[
				"reportFontName",
				"reportFontSize",
				"fontAttributeReporting",
				"reportSuperscriptsAndSubscripts",
				"reportColor",
				"reportLinks",
			],
			False,
		)

	def test_formattingRunIsFoundFromTheCharacterOffset(self) -> None:
		_field, bounds = self.info._getFormatFieldAndOffsets(4, self.formatConfig)
		self.assertEqual(bounds, (0, len(self.text)))

	def test_formattingWithoutRunsUsesASingleCharacter(self) -> None:
		_field, bounds = self.info._getFormatFieldAndOffsets(4, self.formatConfig, calculateOffsets=False)
		self.assertEqual(bounds, (4, len(self.text)))

	def test_startAfterEndRaisesValueError(self) -> None:
		with self.assertRaises(ValueError):
			self.info._getPptTextRange(5, 2)

	def test_linkAtCaretWithoutAFormattingRunReturnsNone(self) -> None:
		self.info.obj.documentWindow = SimpleNamespace(
			ppSelection=SimpleNamespace(textRange=SimpleNamespace(start=len(self.text) + 1)),
		)
		self.assertIsNone(self.info._getLinkDataAtCaretPosition())

	def test_linkAtCaretReturnsTheSharedLinkType(self) -> None:
		self.info.obj.documentWindow = SimpleNamespace(
			ppSelection=SimpleNamespace(textRange=SimpleNamespace(start=1)),
		)
		self.run.actionSettings = lambda activation: SimpleNamespace(
			action=powerpnt.ppActionHyperlink,
			Hyperlink=SimpleNamespace(TextToDisplay="NV Access", Address="https://www.nvaccess.org"),
		)
		link = self.info._getLinkDataAtCaretPosition()
		self.assertEqual(link.displayText, "NV Access")
		self.assertEqual(link.destination, "https://www.nvaccess.org")
