# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from documentNavigation import paragraphHelper
import textInfos
from .textProvider import BasicTextProvider


class Test_moveTextInfoToSingleLineBreakParagraph(unittest.TestCase):
	def test_singleLineBreakParagraph_forward(self):
		text = """Paragraph 1.
Paragraph 2.
Paragraph 3."""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToSingleLineBreakParagraph(True, ti)  # move to second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 2.\n")
		moved = paragraphHelper._moveTextInfoToSingleLineBreakParagraph(True, ti)  # move to third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.")
		moved = paragraphHelper._moveTextInfoToSingleLineBreakParagraph(True, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_singleLineBreakParagraph_backward(self):
		text = """Paragraph 1.
Paragraph 2.
Paragraph 3.
		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToSingleLineBreakParagraph(False, ti)  # move to third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.\n")
		paragraphHelper._moveTextInfoToSingleLineBreakParagraph(False, ti)
		moved = paragraphHelper._moveTextInfoToSingleLineBreakParagraph(False, ti)  # move to first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToSingleLineBreakParagraph(False, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_doubleLineBreakParagraph_forward(self):
		text = """Paragraph 1.

Paragraph 2.

Paragraph 3.
		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 2.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_doubleLineBreakParagraph_backward(self):
		text = """Paragraph 1.

Paragraph 2.

Paragraph 3.
		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 2.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_multiLineBreakParagraph_forward(self):
		# Along with double line break paragraphs (block style),
		# the algorithm supports any number of blank lines between block paragraphs.
		# It also supports white space in either the blank lines, or preceeding the block paragraph itself.
		text = """


Paragraph 1.


\tParagraph 2.



  \t\t\t


     Paragraph 3.



		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "\tParagraph 2.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "     Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_multiLineBreakParagraph_backward(self):
		# Test moving back when paragraphs are separated by multiple blank lines / whitespace
		text = """


Paragraph 1.


\tParagraph 2.



  \t\t\t


     Paragraph 3.



		"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # third paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "     Paragraph 3.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # second paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "\tParagraph 2.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # first paragraph
		self.assertTrue(moved)
		ti.expand(textInfos.UNIT_LINE)
		self.assertEqual(ti.text, "Paragraph 1.\n")
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)  # no more paragraphs
		self.assertFalse(moved)

	def test_multiLineBreakWithSingleLineBreakContent(self):
		# Algorithm should ignore single line breaks when moving to content with two or more line breaks.
		text = """Paragraph 1.
Paragraph 2.
Paragraph 3."""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(True, ti)
		self.assertFalse(moved)
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		moved = paragraphHelper._moveTextInfoToMultiLineBreakParagraph(False, ti)
		self.assertFalse(moved)

	def test_SingleLineBreakWithMultiLineBreakContent(self):
		# Moving to next single line break paragraph really moves to the next line.
		# Prove that each line is presented when moving by single line break paragraphs
		# through content which is multi-line break
		text = """Paragraph 1.

Paragraph 2.

Paragraph 3.
"""
		obj = BasicTextProvider(text=text)
		ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
		lines = text.split("\n")
		for x in range(len(lines) - 1):  # skip last line
			line = lines[x] + "\n"
			ti.expand(textInfos.UNIT_LINE)
			self.assertEqual(line, ti.text)
			paragraphHelper._moveTextInfoToSingleLineBreakParagraph(True, ti)
		# work backward
		ti = obj.makeTextInfo(textInfos.POSITION_LAST)
		# Normally, one should have to move back by one single line break paragraph
		# to position the TextInfo at the beginning of the last paragraph.
		# I can only assume that BasicTextProvider behaves differently than other TextInfos,
		# as it starts at the beginning of the last paragraph, "Paragraph 3."
		# You can see the difference by pasting the above paragraph in Notepad,
		# and walking backwards through it in the NVDA Console.
		# paragraphHelper._moveTextInfoToSingleLineBreakParagraph(False, ti)
		for x in range(len(lines) - 2, -1, -1):
			line = lines[x] + "\n"
			ti.expand(textInfos.UNIT_LINE)
			self.assertEqual(line, ti.text)
			paragraphHelper._moveTextInfoToSingleLineBreakParagraph(False, ti)


class Test_chunkSplitter(unittest.TestCase):
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
