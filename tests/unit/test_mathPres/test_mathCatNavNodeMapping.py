# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for MathCAT NavNode mapping helpers."""

import unittest
import xml.etree.ElementTree as ElementTree

from mathPres.MathCAT import _navNodeMapping as navNodeMapping


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
