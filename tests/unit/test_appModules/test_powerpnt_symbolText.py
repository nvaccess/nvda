# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for reading text boxes holding symbols in a PowerPoint slide show."""

import unittest
from types import SimpleNamespace
from typing import Any

from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


def _textBox(text: str, fontName: str, alternativeText: str = "") -> SimpleNamespace:
	paragraph = SimpleNamespace(text=text, paragraphFormat=SimpleNamespace(bullet=SimpleNamespace(type=0)))
	return SimpleNamespace(
		type=powerpnt.msoTextBox,
		hasTextFrame=True,
		alternativeText=alternativeText,
		textFrame=SimpleNamespace(
			textRange=SimpleNamespace(
				text=text,
				font=SimpleNamespace(name=fontName),
				paragraphs=lambda: [paragraph],
			),
		),
	)


class TestSymbolText(unittest.TestCase):
	def setUp(self) -> None:
		self.window = _object(powerpnt.SlideShowWindow)

	def test_symbolFontTextIsReplacedByItsAlternativeText(self) -> None:
		for fontName in ("Symbol", "Webdings", "Wingdings", "Wingdings 2", "Wingdings 3"):
			with self.subTest(fontName=fontName):
				shape = _textBox("q", fontName, "cycle symbol")
				self.assertEqual(list(self.window._getShapeText(shape)), ["cycle symbol"])

	def test_symbolFontTextWithoutAlternativeTextIsStillRead(self) -> None:
		shape = _textBox("q", "Webdings")
		self.assertEqual(list(self.window._getShapeText(shape)), ["q"])

	def test_ordinaryTextIsNotReplacedByItsAlternativeText(self) -> None:
		shape = _textBox("Quarterly results", "Calibri", "A text box about results")
		self.assertEqual(list(self.window._getShapeText(shape)), ["Quarterly results"])
