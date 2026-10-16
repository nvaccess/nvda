# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for reading the text of PowerPoint SmartArt graphics."""

import unittest
from types import SimpleNamespace
from typing import Any

from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


def _smartArt(*nodeTexts: str) -> SimpleNamespace:
	return SimpleNamespace(
		type=powerpnt.msoSmartArt,
		hasTextFrame=False,
		smartArt=SimpleNamespace(
			allNodes=[
				SimpleNamespace(textFrame2=SimpleNamespace(textRange=SimpleNamespace(text=text)))
				for text in nodeTexts
			],
		),
	)


class TestSmartArtText(unittest.TestCase):
	def test_nodesAreYieldedInModelOrderWithoutEmptyNodes(self) -> None:
		shape = _smartArt("Start", "", "  ", "Finish")
		self.assertEqual(list(powerpnt.iterSmartArtNodeTexts(shape)), ["Start", "Finish"])

	def test_lineBreaksInANodeAreNormalized(self) -> None:
		shape = _smartArt("Review\rApprove\x0bPublish\r")
		self.assertEqual(list(powerpnt.iterSmartArtNodeTexts(shape)), ["Review\nApprove\nPublish"])

	def test_slideShowReadsEveryNode(self) -> None:
		window = _object(powerpnt.SlideShowWindow)
		self.assertEqual(list(window._getShapeText(_smartArt("Start", "Finish"))), ["Start", "Finish"])

	def test_editorValueContainsEveryNode(self) -> None:
		shape = _object(powerpnt.Shape, ppObject=_smartArt("Start", "Finish"))
		self.assertEqual(shape.value, "Start\nFinish")

	def test_graphicWithoutNodesHasAnEmptyValue(self) -> None:
		shape = _object(powerpnt.Shape, ppObject=_smartArt())
		self.assertEqual(shape.value, "")
