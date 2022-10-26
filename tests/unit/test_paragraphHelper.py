# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
import documentNavigation.paragraphHelper as paragraphHelper
import textInfos
from .textProvider import BasicTextProvider


class TestParagraphHelper(unittest.TestCase):
	def test_singleLineBreakParagraphForward(self):
		text = """Paragraph 1.
Paragraph 2.
Paragraph 3."""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToParagraph(True, ti)  # move to second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 2.\n")
		moved = paragraphHelper._moveTextInfoToParagraph(True, ti)  # move to third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.")
		moved = paragraphHelper._moveTextInfoToParagraph(True, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_singleLineBreakParagraphBack(self):
		text = """Paragraph 1.
Paragraph 2.
Paragraph 3.
		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToParagraph(False, ti)  # move to third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.\n")
		paragraphHelper._moveTextInfoToParagraph(False, ti)
		moved = paragraphHelper._moveTextInfoToParagraph(False, ti)  # move to first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToParagraph(False, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_DoubleLineBreakParagraphForward(self):
		text = """Paragraph 1.

Paragraph 2.

Paragraph 3.
		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 2.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_DoubleLineBreakParagraphBack(self):
		text = """Paragraph 1.

Paragraph 2.

Paragraph 3.
		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 2.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_multiLineBreakParagraphForward(self):
		"""
			Along with double line break paragraphs (block style),
			the algorithm supports any number of blank lines between block paragraphs.
			It also supports white space in either the blank lines,
			or preceeding the block paragraph itself.
		"""
		text = """


Paragraph 1.


\tParagraph 2.



  \t\t\t


     Paragraph 3.



		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "\tParagraph 2.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "     Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_multiLineBreakParagraphBack(self):
		"""
			Test moving back when paragraphs are separated by multiple blank lines / whitespace
		"""
		text = """


Paragraph 1.


\tParagraph 2.



  \t\t\t


     Paragraph 3.



		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "     Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "\tParagraph 2.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_DoubleLineBreakWithSingleLineBreakContent(self):
		"""
			Algorithm should ignore single line breaks when moving to content with two ore more line breaks.
		"""
		text = """Paragraph 1.
Paragraph 2.
Paragraph 3."""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToBlockParagraph(True, ti)
		self.assertFalse(moved)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToBlockParagraph(False, ti)
		self.assertFalse(moved)

	def test_paragraphChunkerWithChunkableContent(self):
		paragraph = "Multiple sentences for testing. " * 1000 + "\n"
		gen = paragraphHelper._splitParagraphIntoChunks(paragraph)
		accumulatedLength = 0
		for chunk in gen:
			self.assertTrue(len(chunk) <= paragraphHelper.PREFERRED_CHUNK_SIZE)
			accumulatedLength += len(chunk)
		self.assertEqual(accumulatedLength, len(paragraph))

	def test_paragraphChunkerWithNonchunkableContent(self):
		paragraph = "Content for testing " * 1000 + "\n"  # not sentences -- not chunkable
		gen = paragraphHelper._splitParagraphIntoChunks(paragraph)
		chunkCount = 0
		for chunk in gen:
			chunkCount += 1
		self.assertEqual(chunkCount, 1)
		self.assertEqual(chunk, paragraph)
