# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for MathCAT NavNode mapping helpers."""

import sys
import unittest
import xml.etree.ElementTree as ElementTree
from types import ModuleType
from typing import TYPE_CHECKING, cast
from unittest.mock import patch

from locationHelper import RectLTRB
from mathPres._mathMlNode import MathMlNodeInfo, MathMlNodeRectInfo
from mathPres.MathCAT import _navNodeMapping as navNodeMapping

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject


class TestMathCatNavNodeMapping(unittest.TestCase):
	def test_stripMathMlNamespace(self):
		testCases = [
			("{http://www.w3.org/1998/Math/MathML}mi", "mi"),
			("{http://www.w3.org/1998/Math/MathML}math", "math"),
			("mi", "mi"),
		]
		for tag, expectedTag in testCases:
			with self.subTest(tag=tag):
				self.assertEqual(navNodeMapping._stripMathMlNamespace(tag), expectedTag)

	def test_prepareMathMlForNavigation_withoutSourceObj_returnsOriginalMathMl(self):
		testCases = [
			"<math><mi>x</mi></math>",
			"<math xmlns='http://www.w3.org/1998/Math/MathML'><mn>1</mn></math>",
		]
		for mathml in testCases:
			with self.subTest(mathml=mathml):
				self.assertEqual(
					navNodeMapping.prepareMathMlForNavigation(mathml, sourceObj=None),
					(mathml, {}),
				)

	def test_addNavigationIdsToMathMl_preservesAuthorIdsAndAvoidsPrefixCollisions(self) -> None:
		mathml = (
			'<math id="author-root">'
			'<mrow id="nvda-math-node-author">'
			'<mi href="#author-root">x</mi>'
			"</mrow>"
			"</math>"
		)

		result, nodeInfoById = navNodeMapping._addNavigationIdsToMathMl(mathml)

		root = ElementTree.fromstring(result)
		mrow = root.find("mrow")
		assert mrow is not None
		mi = mrow.find("mi")
		assert mi is not None
		self.assertEqual(root.attrib, {"id": "author-root"})
		self.assertEqual(mrow.attrib, {"id": "nvda-math-node-author"})
		self.assertEqual(
			mi.attrib,
			{
				"href": "#author-root",
				"id": "nvda-math-node-1-0-0",
				"data-nvda-math-id-added": "true",
			},
		)
		self.assertEqual(
			nodeInfoById,
			{
				"author-root": MathMlNodeInfo(path=(), tag="math"),
				"nvda-math-node-author": MathMlNodeInfo(path=(0,), tag="mrow"),
				"nvda-math-node-1-0-0": MathMlNodeInfo(path=(0, 0), tag="mi"),
			},
		)

	def test_prepareMathMlForNavigation_mapsMatchingIa2Nodes(self) -> None:
		rootRect = RectLTRB(left=0, top=0, right=100, bottom=50)
		mismatchedRect = RectLTRB(left=10, top=10, right=20, bottom=20)

		class FakeIa2WebMath:
			def _getMathNodeInfoByPath(self) -> dict[tuple[int, ...], MathMlNodeRectInfo]:
				return {
					(): MathMlNodeRectInfo(path=(), tag="math", rect=rootRect),
					(0,): MathMlNodeRectInfo(path=(0,), tag="mstyle", rect=mismatchedRect),
				}

		sourceObj = cast("NVDAObject", FakeIa2WebMath())
		fakeIa2WebModule = ModuleType("NVDAObjects.IAccessible.ia2Web")
		setattr(fakeIa2WebModule, "Math", FakeIa2WebMath)
		with patch.dict(sys.modules, {"NVDAObjects.IAccessible.ia2Web": fakeIa2WebModule}):
			result, rectsById = navNodeMapping.prepareMathMlForNavigation(
				"<math><mrow><mi>x</mi></mrow></math>",
				sourceObj,
			)

		root = ElementTree.fromstring(result)
		self.assertEqual(root.get("id"), "nvda-math-node-root")
		self.assertEqual(rectsById, {"nvda-math-node-root": rootRect})

	def test_removeSyntheticIdsFromMathMl(self):
		testCases = [
			(
				'<math><mi id="nvda-math-node-0" data-nvda-math-id-added="true">x</mi></math>',
				{},
			),
			(
				'<math><mi id="author-id" href="#author-id">x</mi></math>',
				{"id": "author-id", "href": "#author-id"},
			),
			(
				'<math><mi id="author-id">x</mi></math>',
				{"id": "author-id"},
			),
		]
		for mathml, expectedAttrs in testCases:
			with self.subTest(mathml=mathml):
				result = navNodeMapping.removeSyntheticIdsFromMathMl(mathml)
				mi = ElementTree.fromstring(result).find("mi")
				assert mi is not None
				self.assertEqual(mi.attrib, expectedAttrs)

	def test_removeSyntheticIdsFromMathMl_parseError_returnsOriginalMathMl(self):
		mathml = "<math><mi>x</math>"
		self.assertEqual(navNodeMapping.removeSyntheticIdsFromMathMl(mathml), mathml)

	def test_removeSyntheticIdsFromMathMl_removesMathCatIdAndPreservesNamespace(self) -> None:
		mathml = (
			'<?xml version="1.0"?>\n'
			'<math xmlns="http://www.w3.org/1998/Math/MathML">'
			'<mi id="MathCAT-generated" data-id-added="true">x</mi>'
			"</math>"
		)

		result = navNodeMapping.removeSyntheticIdsFromMathMl(mathml)

		self.assertEqual(
			result,
			'<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>x</mi></math>',
		)
