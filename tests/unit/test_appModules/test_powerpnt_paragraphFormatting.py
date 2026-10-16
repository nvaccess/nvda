# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for paragraph level formatting (bullets, numbering and alignment) in PowerPoint text frames."""

import unittest
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock

from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


class TestParagraphFormatting(unittest.TestCase):
	def setUp(self) -> None:
		self.text = "First\rSecond\x0bline\rThird"
		# One font run covers three paragraphs, each with its own number and alignment.
		self.paragraphs = [
			SimpleNamespace(
				start=start,
				length=len(text),
				paragraphFormat=SimpleNamespace(
					alignment=alignment,
					bullet=SimpleNamespace(type=powerpnt.ppBulletNumbered, number=number),
				),
			)
			for start, text, alignment, number in [
				(1, "First\r", 1, 1),
				(7, "Second\x0bline\r", 2, 2),
				(19, "Third", 3, 3),
			]
		]
		self.run = SimpleNamespace(start=1, length=len(self.text), font=SimpleNamespace())
		self.textRange = Mock(length=len(self.text))
		self.textRange.runs.return_value = [self.run]
		self.textRange.paragraphs.side_effect = lambda *args: (
			self.paragraphs[args[0] - 1] if args else self.paragraphs
		)
		self.textRange.characters.side_effect = lambda start, length: SimpleNamespace(font=self.run.font)
		frame = _object(powerpnt.TextFrame, ppObject=SimpleNamespace(textRange=self.textRange))
		self.info = _object(
			powerpnt.TextFrameTextInfo,
			obj=frame,
			_startOffset=0,
			_endOffset=len(self.text),
		)
		self.formatConfig = dict.fromkeys(
			[
				"reportFontName",
				"reportFontSize",
				"fontAttributeReporting",
				"reportSuperscriptsAndSubscripts",
				"reportColor",
				"reportLinks",
				"reportAlignment",
			],
			False,
		)

	def test_runStopsAtTheParagraphBoundary(self) -> None:
		field, bounds = self.info._getFormatFieldAndOffsets(6, self.formatConfig)
		self.assertEqual(bounds, (6, 18))
		self.assertEqual(field["line-prefix"], "2.")
		self.assertTrue(field["line-prefix_speakAlways"])

	def test_everyParagraphOfOneRunReportsItsOwnNumber(self) -> None:
		for offset, number in [(0, 1), (6, 2), (18, 3)]:
			with self.subTest(offset=offset):
				field, _bounds = self.info._getFormatFieldAndOffsets(offset, self.formatConfig)
				self.assertEqual(field["line-prefix"], f"{number}.")

	def test_bulletIsNotRepeatedInTheMiddleOfAParagraphOrAfterASoftLineBreak(self) -> None:
		for offset in (2, 13):
			with self.subTest(offset=offset):
				field, _bounds = self.info._getFormatFieldAndOffsets(offset, self.formatConfig)
				self.assertNotIn("line-prefix", field)

	def test_unnumberedParagraphHasNoPrefix(self) -> None:
		self.paragraphs[0].paragraphFormat.bullet = SimpleNamespace(type=0)
		field, _bounds = self.info._getFormatFieldAndOffsets(0, self.formatConfig)
		self.assertNotIn("line-prefix", field)

	def test_paragraphIsUsedWhenRunBoundsAreNotCalculated(self) -> None:
		field, _bounds = self.info._getFormatFieldAndOffsets(18, self.formatConfig, calculateOffsets=False)
		self.assertEqual(field["line-prefix"], "3.")
		self.textRange.runs.assert_not_called()

	def test_alignmentIsReadFromTheCurrentParagraph(self) -> None:
		self.formatConfig["reportAlignment"] = True
		for offset, alignment in [(0, "left"), (6, "center"), (18, "right")]:
			with self.subTest(offset=offset):
				field, _bounds = self.info._getFormatFieldAndOffsets(offset, self.formatConfig)
				self.assertEqual(field["text-align"], alignment)

	def test_everyKnownAlignmentIsMapped(self) -> None:
		self.formatConfig["reportAlignment"] = True
		for value, alignment in [(4, "justify"), (5, "distribute"), (6, "distribute"), (7, "justify")]:
			with self.subTest(value=value):
				self.paragraphs[0].paragraphFormat.alignment = value
				field, _bounds = self.info._getFormatFieldAndOffsets(0, self.formatConfig)
				self.assertEqual(field["text-align"], alignment)

	def test_unknownAlignmentIsNotReported(self) -> None:
		self.formatConfig["reportAlignment"] = True
		for value in (-2, 0, 99):
			with self.subTest(value=value):
				self.paragraphs[0].paragraphFormat.alignment = value
				field, _bounds = self.info._getFormatFieldAndOffsets(0, self.formatConfig)
				self.assertNotIn("text-align", field)

	def test_alignmentIsNotReportedWhenDisabled(self) -> None:
		field, _bounds = self.info._getFormatFieldAndOffsets(6, self.formatConfig)
		self.assertNotIn("text-align", field)
