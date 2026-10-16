# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for finding the speaker notes of a PowerPoint slide."""

import unittest
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import comtypes
from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


def _textShape(text: str, placeholderType: int | None) -> SimpleNamespace:
	shape = SimpleNamespace(
		type=powerpnt.msoTextBox,
		hasTextFrame=True,
		textFrame=SimpleNamespace(
			textRange=SimpleNamespace(
				text=text,
				paragraphs=lambda: [
					SimpleNamespace(
						text=text, paragraphFormat=SimpleNamespace(bullet=SimpleNamespace(type=0))
					),
				],
			),
		),
	)
	if placeholderType is not None:
		shape.placeholderFormat = SimpleNamespace(type=placeholderType)
	return shape


def _slide(*notesShapes: SimpleNamespace) -> SimpleNamespace:
	return SimpleNamespace(shapes=[], notesPage=SimpleNamespace(shapes=list(notesShapes)))


class TestNotesBodyShape(unittest.TestCase):
	def test_bodyIsFoundByPlaceholderTypeWhateverItsPosition(self) -> None:
		footer = _textShape("Footer", powerpnt.ppPlaceholderFooter)
		number = _textShape("3", powerpnt.ppPlaceholderSlideNumber)
		body = _textShape("Notes", powerpnt.ppPlaceholderBody)
		self.assertIs(powerpnt.getNotesBodyShape(_slide(footer, number, body)), body)

	def test_shapesWithoutAPlaceholderAreSkipped(self) -> None:
		picture = SimpleNamespace(hasTextFrame=False)
		body = _textShape("Notes", powerpnt.ppPlaceholderBody)
		self.assertIs(powerpnt.getNotesBodyShape(_slide(picture, body)), body)

	def test_unreadablePlaceholderIsSkipped(self) -> None:
		class Unreadable:
			@property
			def placeholderFormat(self) -> None:
				raise comtypes.COMError(-1, "No placeholder", None)

		body = _textShape("Notes", powerpnt.ppPlaceholderBody)
		self.assertIs(powerpnt.getNotesBodyShape(_slide(Unreadable(), body)), body)

	def test_noBodyReturnsNone(self) -> None:
		footer = _textShape("Footer", powerpnt.ppPlaceholderFooter)
		self.assertIsNone(powerpnt.getNotesBodyShape(_slide(footer)))


class TestNotesEditing(unittest.TestCase):
	def _document(self, slide: SimpleNamespace) -> powerpnt.DocumentWindow:
		class NoParent:
			@property
			def parent(self) -> None:
				raise comtypes.COMError(-1, "No parent", None)

		class NoShapes:
			def __getitem__(self, index: int) -> None:
				raise comtypes.COMError(-1, "No shape is selected", None)

		return _object(
			powerpnt.DocumentWindow,
			windowHandle=1,
			ppActivePaneViewType=powerpnt.ppViewNotesPage,
			ppDocumentViewType=powerpnt.ppViewNormal,
			ppVersionMajor=16,
			ppSelection=SimpleNamespace(
				type=powerpnt.ppSelectionText,
				textRange=NoParent(),
				shapeRange=NoShapes(),
				slideRange={1: slide},
			),
		)

	def test_selectionIsTheNotesBodyEvenWhenItIsNotTheSecondShape(self) -> None:
		body = _textShape("Notes", powerpnt.ppPlaceholderBody)
		slide = _slide(_textShape("", None), _textShape("", None), body)
		document = self._document(slide)
		with patch.object(powerpnt, "NotesTextFrame") as notesTextFrame:
			self.assertIs(document.selection, notesTextFrame.return_value)
		notesTextFrame.assert_called_once_with(
			windowHandle=1,
			documentWindow=document,
			ppObject=body.textFrame,
		)


class TestSlideShowNotes(unittest.TestCase):
	def _window(self, slide: SimpleNamespace) -> powerpnt.SlideShowWindow:
		currentSlide = SimpleNamespace(ppObject=slide)
		return _object(
			powerpnt.SlideShowWindow,
			windowHandle=1,
			currentSlide=currentSlide,
			notesMode=True,
		)

	def test_onlyTheNotesBodyIsRead(self) -> None:
		slide = _slide(
			_textShape("Header", powerpnt.ppPlaceholderHeader),
			_textShape("Actual notes", powerpnt.ppPlaceholderBody),
			_textShape("Footer", powerpnt.ppPlaceholderFooter),
		)
		self.assertEqual(self._window(slide).basicText, "Actual notes")

	def test_slideWithoutNotesBodyHasNoNotes(self) -> None:
		slide = _slide(_textShape("Footer", powerpnt.ppPlaceholderFooter))
		self.assertEqual(self._window(slide).basicText, "No notes")
