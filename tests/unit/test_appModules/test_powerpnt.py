# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for PowerPoint slide title and content reporting."""

import unittest
from collections.abc import Iterable
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, PropertyMock, patch

import comtypes
import textInfos
from appModules import powerpnt


class _Shapes(list[SimpleNamespace]):
	def __init__(self, shapes: Iterable[SimpleNamespace] = (), title: SimpleNamespace | None = None) -> None:
		super().__init__(shapes)
		self._title = title

	@property
	def title(self) -> SimpleNamespace:
		if self._title is None:
			raise comtypes.COMError(-1, "No title", None)
		return self._title


def _textShape(shapeID: int, text: str) -> SimpleNamespace:
	paragraphs = [
		SimpleNamespace(text=paragraph, paragraphFormat=SimpleNamespace(bullet=SimpleNamespace(type=0)))
		for paragraph in text.split("\r")
	]
	return SimpleNamespace(
		ID=shapeID,
		hasTextFrame=True,
		title="",
		textFrame=SimpleNamespace(textRange=SimpleNamespace(text=text, paragraphs=lambda: paragraphs)),
	)


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


class TestSlideTitles(unittest.TestCase):
	def setUp(self) -> None:
		self.titleShape = _textShape(1, "Παράδειγμα")
		self.bodyShape = _textShape(2, "Body text")
		self.ppSlide = SimpleNamespace(
			slideNumber=1,
			slideID=101,
			shapes=_Shapes([self.titleShape, self.bodyShape], title=self.titleShape),
		)
		self.document = _object(
			powerpnt.DocumentWindow,
			ppActivePaneViewType=powerpnt.ppViewSlide,
		)
		self.slide = _object(powerpnt.Slide, ppObject=self.ppSlide, documentWindow=self.document)
		self.document.currentSlide = self.slide
		self.window = _object(powerpnt.SlideShowWindow, currentSlide=self.slide, notesMode=False)

	def test_slideNameLabelsTitleWithoutParentheses(self) -> None:
		self.assertEqual(self.slide.name, "Slide 1 - Slide title: Παράδειγμα")

	def test_documentContextDoesNotRepeatTitle(self) -> None:
		self.assertNotIn("Παράδειγμα", self.document.name)
		self.assertIn("Slide 1", self.document.name)

	def test_slideShowTitleOccursOnceAndStaysReviewable(self) -> None:
		self.assertNotIn("Παράδειγμα", self.window.name)
		self.assertEqual(
			self.window.basicText,
			"Slide title: Παράδειγμα\nSlide contents\nBody text",
		)

	def test_titleIsReportedFirstEvenWhenNotFirstShape(self) -> None:
		self.ppSlide.shapes.reverse()
		self.assertTrue(self.window.basicText.startswith("Slide title: Παράδειγμα\n"))

	def test_sameTextInAnotherShapeIsNotRemoved(self) -> None:
		self.bodyShape.textFrame.textRange.paragraphs = self.titleShape.textFrame.textRange.paragraphs
		self.assertEqual(self.window.basicText.count("Παράδειγμα"), 2)

	def test_titleOnlySlideDoesNotAnnounceEmptyContents(self) -> None:
		self.ppSlide.shapes = _Shapes([self.titleShape], title=self.titleShape)
		self.assertEqual(self.window.basicText, "Slide title: Παράδειγμα")

	def test_untitledSlideStillReportsContents(self) -> None:
		self.ppSlide.shapes = _Shapes([self.bodyShape])
		self.assertEqual(self.window.basicText, "Slide contents\nBody text")
		self.assertEqual(self.slide.name, "Slide 1")

	def test_emptySlideKeepsEmptySlideMessage(self) -> None:
		self.ppSlide.shapes = _Shapes()
		self.assertEqual(self.window.basicText, "Empty slide")

	def test_blankTitleDoesNotHideContent(self) -> None:
		self.titleShape.textFrame.textRange.text = "\r "
		self.titleShape.textFrame.textRange.paragraphs = list
		self.assertEqual(self.window.basicText, "Slide contents\nBody text")

	def test_notesKeepSlideTitleAndDoNotAddContentLabels(self) -> None:
		self.window.notesMode = True
		self.ppSlide.notesPage = SimpleNamespace(shapes=_Shapes([_textShape(3, "Speaker notes")]))
		self.assertIn("Slide title: Παράδειγμα", self.window.name)
		self.assertEqual(self.window.basicText, "Speaker notes")

	def test_mathFieldOffsetsIncludeSectionLabels(self) -> None:
		field = textInfos.ControlField(role="math")
		with patch.object(powerpnt.SlideShowWindow, "_getShapeText", return_value=iter([field])):
			self.assertEqual(self.window.basicText, "Slide title: Παράδειγμα\nSlide contents\n ")
		self.assertEqual(
			self.window.basicTextFields,
			[(len("Slide title: Παράδειγμα\nSlide contents\n"), field)],
		)

	def test_greekSectionLabels(self) -> None:
		translations = {
			"Slide title: {title}": "Τίτλος διαφάνειας: {title}",
			"Slide contents": "Περιεχόμενα διαφάνειας",
		}
		with patch.object(powerpnt, "_", side_effect=lambda text: translations.get(text, text), create=True):
			self.assertEqual(
				self.window.basicText,
				"Τίτλος διαφάνειας: Παράδειγμα\nΠεριεχόμενα διαφάνειας\nBody text",
			)

	def test_editingTitleShapeUsesSlideTitleLabel(self) -> None:
		shape = _object(powerpnt.Shape, ppObject=self.titleShape, documentWindow=self.document)
		self.assertEqual(shape.name, "Slide title")
		self.assertEqual(shape.value, "Παράδειγμα")

	def test_editingAnnouncesContentsOnSectionTransition(self) -> None:
		title = _object(powerpnt.Shape, ppObject=self.titleShape, documentWindow=self.document)
		body = _object(powerpnt.Shape, ppObject=self.bodyShape, documentWindow=self.document)
		with (
			patch.object(powerpnt.Window, "reportFocus"),
			patch.object(powerpnt.speech, "speakMessage") as speakMessage,
		):
			self.slide.reportFocus()
			title.reportFocus()
			speakMessage.assert_not_called()
			body.reportFocus()
			body.reportFocus()
			speakMessage.assert_called_once_with("Slide contents")
			title.reportFocus()
			body.reportFocus()
			self.assertEqual(speakMessage.call_count, 2)

	def test_editingDirectTextFrameEntryReportsContents(self) -> None:
		parent = _object(powerpnt.Shape, ppObject=self.bodyShape, documentWindow=self.document)
		frame = _object(powerpnt.TextFrame, documentWindow=self.document, parent=parent)
		with (
			patch.object(powerpnt.Window, "reportFocus"),
			patch.object(powerpnt.speech, "speakMessage") as speakMessage,
		):
			frame.reportFocus()
			speakMessage.assert_called_once_with("Slide contents")

	def test_editingTableCellEntryReportsContents(self) -> None:
		table = _object(powerpnt.Table, ppObject=_textShape(3, ""), documentWindow=self.document)
		cell = _object(powerpnt.TableCell, parent=table, table=table, documentWindow=self.document)
		frame = _object(powerpnt.TableCellTextFrame, documentWindow=self.document, parent=cell)
		with (
			patch.object(powerpnt.Window, "reportFocus"),
			patch.object(powerpnt.speech, "speakMessage") as speakMessage,
		):
			frame.reportFocus()
			speakMessage.assert_called_once_with("Slide contents")

	def test_editingNewSlideReportsContentsAgain(self) -> None:
		body = _object(powerpnt.Shape, ppObject=self.bodyShape, documentWindow=self.document)
		with (
			patch.object(powerpnt.Window, "reportFocus"),
			patch.object(powerpnt.speech, "speakMessage") as speakMessage,
		):
			body.reportFocus()
			self.ppSlide.slideID += 1
			body.reportFocus()
			self.assertEqual(speakMessage.call_count, 2)

	def test_notesEditingDoesNotAnnounceSlideContents(self) -> None:
		self.document.ppActivePaneViewType = powerpnt.ppViewNotesPage
		body = _object(powerpnt.Shape, ppObject=self.bodyShape, documentWindow=self.document)
		with (
			patch.object(powerpnt.Window, "reportFocus"),
			patch.object(powerpnt.speech, "speakMessage") as speakMessage,
		):
			body.reportFocus()
			speakMessage.assert_not_called()

	def test_slideChangeStillDetectsTitleEdits(self) -> None:
		self.window._lastSlideChangeID = None
		with (
			patch.object(
				powerpnt.SlideShowWindow,
				"treeInterceptor",
				new_callable=PropertyMock,
			) as treeInterceptor,
			patch.object(powerpnt.SlideShowWindow, "currentSlide", new_callable=PropertyMock) as currentSlide,
			patch.object(powerpnt.SlideShowWindow, "reportFocus") as reportFocus,
		):
			treeInterceptor.return_value = Mock()
			currentSlide.return_value = self.slide
			self.window.handleSlideChange()
			self.window.handleSlideChange()
			reportFocus.assert_called_once()
			self.titleShape.textFrame.textRange.text = "Changed title"
			self.slide.invalidateCache()
			self.window.invalidateCache()
			self.window.handleSlideChange()
			self.assertEqual(reportFocus.call_count, 2)
			self.assertEqual(treeInterceptor.return_value.reportNewSlide.call_count, 2)

	def test_bulletAndParagraphContentIsPreserved(self) -> None:
		paragraph = SimpleNamespace(
			text="First\x0bSecond\r",
			paragraphFormat=SimpleNamespace(bullet=SimpleNamespace(type=powerpnt.ppBulletNumbered, number=2)),
		)
		self.bodyShape.textFrame.textRange.paragraphs = Mock(return_value=[paragraph])
		self.assertTrue(self.window.basicText.endswith("2. First\nSecond"))
