# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the compoundDocuments module."""

import unittest

import compoundDocuments
import controlTypes
import textInfos
from .objectProvider import PlaceholderNVDAObject
from .textProvider import BasicTextInfo, BasicTextProvider


class BasicCompoundTextLeafTextInfo(compoundDocuments.CompoundTextLeafTextInfo, BasicTextInfo): ...


class BasicCompoundTextLeaf(BasicTextProvider):
	TextInfo = BasicCompoundTextLeafTextInfo
	windowHandle = 0
	states = {controlTypes.State.FOCUSABLE}
	flowsFrom = None
	flowsTo = None


class CompoundTreePlaceholderObject(PlaceholderNVDAObject):
	"""A placeholder NVDAObject for testing CompoundTextInfo implementations.
	This class represents a tree structure of text providers.
	Note that it also mutates the text providers to link them in a flow."""

	def __init__(self, objs: list[BasicCompoundTextLeaf], **kwargs):
		super().__init__(**kwargs)
		assert len(objs) > 0, "At least one text provider must be provided"
		self.children = objs
		self.firstChild = objs[0]
		self.lastChild = objs[-1]
		lastProcessedObj = None
		for obj in objs:
			if lastProcessedObj is not None:
				lastProcessedObj.flowsTo = obj
				obj.flowsFrom = lastProcessedObj
			lastProcessedObj = obj


class TestTreeCompoundTextInfo(unittest.TestCase):
	"""Tests for the TreeCompoundTextInfo class."""

	def setUp(self) -> None:
		objs = [
			BasicCompoundTextLeaf(text="one\r\n"),
			BasicCompoundTextLeaf(text="two\r\n"),
			BasicCompoundTextLeaf(text="three"),
		]
		self.objs = objs
		self.rootObj = CompoundTreePlaceholderObject(objs=objs)
		self.document = compoundDocuments.CompoundDocument(self.rootObj)
		self.fullText = "one\r\ntwo\r\nthree"

	def test_innerInfos(self):
		"""Test that the text infos are created correctly."""
		info: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_ALL)
		innerInfos = list(info._getTextInfos())
		self.assertEqual(len(innerInfos), 3)
		for obj, info in zip(self.objs, innerInfos):
			self.assertEqual(obj, info.obj)

	def test_text(self):
		"""Test that the combined text is correct."""
		info: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_ALL)
		self.assertEqual(info.text, self.fullText)

	def test_characterMovement(self):
		"""Test character movement across the compound text info."""
		info: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_FIRST)
		expected = [*"one\r\n", "", *"two\r\n", "", *"three"]
		for i in range(len(expected) + 1):
			c = expected[i] if i < len(expected) else ""
			with self.subTest(i=i, c=c):
				info.collapse()
				movement = min(i, 1)
				self.assertEqual(info.move(textInfos.UNIT_CHARACTER, movement), movement)
				info.expand(textInfos.UNIT_CHARACTER)
				self.assertEqual(info.text, c)
		last: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_LAST)
		# Allow moving past end
		self.assertGreater(info.compareEndPoints(last, "endToEnd"), 0)

	def test_wordMovement(self):
		"""Test word movement across the compound text info."""
		info: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_FIRST)
		expected = ["one\r\n", "", "two\r\n", "", "three"]
		for i in range(len(expected) + 1):
			w = expected[i] if i < len(expected) else ""
			with self.subTest(i=i, w=w):
				info.collapse()
				movement = min(i, 1)
				self.assertEqual(info.move(textInfos.UNIT_WORD, movement), movement)
				info.expand(textInfos.UNIT_WORD)
				self.assertEqual(info.text, w)
		last: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_LAST)
		# Allow moving past end
		self.assertGreater(info.compareEndPoints(last, "endToEnd"), 0)

	def test_lineMovement(self):
		"""Test line movement across the compound text info."""
		info: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_FIRST)
		expected = ["one\r\n", "two\r\n", "three"]
		for i in range(len(expected) + 1):
			if i < len(expected):
				line = expected[i]
			with self.subTest(i=i, line=line):
				info.collapse()
				movement = min(i, 1)
				self.assertEqual(info.move(textInfos.UNIT_LINE, movement), movement)
				info.expand(textInfos.UNIT_LINE)
				self.assertEqual(info.text, line)
		last: compoundDocuments.TreeCompoundTextInfo = self.document.makeTextInfo(textInfos.POSITION_LAST)
		# Allow moving past end
		self.assertGreater(info.compareEndPoints(last, "endToEnd"), 0)
