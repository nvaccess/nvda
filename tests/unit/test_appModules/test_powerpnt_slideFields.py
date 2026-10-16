# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for the text and fields of a PowerPoint slide show."""

import unittest
from types import SimpleNamespace
from typing import Any

import textInfos
from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


def _textShape(text: str) -> SimpleNamespace:
	paragraph = SimpleNamespace(text=text, paragraphFormat=SimpleNamespace(bullet=SimpleNamespace(type=0)))
	return SimpleNamespace(
		type=powerpnt.msoTextBox,
		hasTextFrame=True,
		textFrame=SimpleNamespace(textRange=SimpleNamespace(text=text, paragraphs=lambda: [paragraph])),
	)


class TestSlideShowFields(unittest.TestCase):
	def setUp(self) -> None:
		slide = SimpleNamespace(ppObject=SimpleNamespace(shapes=[_textShape("Body text")]))
		self.window = _object(powerpnt.SlideShowWindow, windowHandle=1, currentSlide=slide, notesMode=False)

	def test_textWithFieldsDoesNotNeedThePreviouslyBuiltText(self) -> None:
		# The fields do not exist until the text has been built, which is the case for a new slide.
		info = _object(
			powerpnt.SlideShowTreeInterceptorTextInfo,
			obj=SimpleNamespace(rootNVDAObject=self.window),
			_startOffset=0,
			_endOffset=100,
		)
		self.assertEqual(info.getTextWithFields(), ["Body text"])

	def test_fieldsOfTheCompletedShowAreCleared(self) -> None:
		self.window.currentSlide = None
		self.window.basicTextFields = [(5, textInfos.ControlField(role="math"))]
		_ = self.window.basicText
		self.assertEqual(self.window.basicTextFields, [])
