# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for the text of PowerPoint shapes, including bullets and numbers."""

import unittest
from types import SimpleNamespace
from typing import Any

from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


def _paragraph(text: str, bulletType: int = 0, number: int = 0, character: int = 0x2022) -> SimpleNamespace:
	bullet = SimpleNamespace(type=bulletType, number=number, character=character)
	return SimpleNamespace(text=text, paragraphFormat=SimpleNamespace(bullet=bullet))


def _textShape(*paragraphs: SimpleNamespace) -> SimpleNamespace:
	return SimpleNamespace(
		hasTextFrame=True,
		textFrame=SimpleNamespace(textRange=SimpleNamespace(paragraphs=lambda: list(paragraphs))),
	)


class TestShapeText(unittest.TestCase):
	def test_valueIncludesTheBulletOfEveryParagraph(self) -> None:
		ppShape = _textShape(_paragraph("First\r", bulletType=1), _paragraph("Second", bulletType=1))
		shape = _object(powerpnt.Shape, ppObject=ppShape)
		self.assertEqual(shape.value, "• First\n• Second")

	def test_valueIncludesTheNumberOfEveryParagraph(self) -> None:
		ppShape = _textShape(
			_paragraph("First\r", powerpnt.ppBulletNumbered, 1),
			_paragraph("Second", powerpnt.ppBulletNumbered, 2),
		)
		shape = _object(powerpnt.Shape, ppObject=ppShape)
		self.assertEqual(shape.value, "1. First\n2. Second")

	def test_valueWithoutBulletsIsPlainText(self) -> None:
		shape = _object(powerpnt.Shape, ppObject=_textShape(_paragraph("Plain text")))
		self.assertEqual(shape.value, "Plain text")

	def test_valueSkipsBlankParagraphsAndNormalizesLineBreaks(self) -> None:
		ppShape = _textShape(_paragraph("One\x0bTwo\r"), _paragraph("  \r"), _paragraph("Three"))
		shape = _object(powerpnt.Shape, ppObject=ppShape)
		self.assertEqual(shape.value, "One\nTwo\nThree")

	def test_shapeWithoutTextHasNoValue(self) -> None:
		shape = _object(powerpnt.Shape, ppObject=SimpleNamespace(hasTextFrame=False))
		self.assertIsNone(shape.value)

	def test_slideShowTextUsesTheSameParagraphText(self) -> None:
		ppShape = _textShape(_paragraph("First\r", bulletType=1), _paragraph("Second", bulletType=1))
		window = _object(powerpnt.SlideShowWindow)
		self.assertEqual(list(window._getShapeText(ppShape)), ["• First", "• Second"])
