# A part of NonVisual Desktop Access (NVDA)
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for MathCAT NavNode mapping helpers."""

import unittest
import xml.etree.ElementTree as ElementTree

from mathPres.MathCAT import navNodeMapping


class TestMathCatNavNodeMapping(unittest.TestCase):
	def test_stripMathMlNamespace(self):
		self.assertEqual(
			navNodeMapping._stripMathMlNamespace("{http://www.w3.org/1998/Math/MathML}mi"),
			"mi",
		)
		self.assertEqual(navNodeMapping._stripMathMlNamespace("mi"), "mi")

	def test_prepareMathMlForNavigation_withoutSourceObj_returnsOriginalMathMl(self):
		mathml = "<math><mi>x</mi></math>"
		self.assertEqual(navNodeMapping.prepareMathMlForNavigation(mathml, sourceObj=None), (mathml, {}))

	def test_removeSyntheticIdsFromMathMl_removesGeneratedId(self):
		mathml = (
			'<math><mi id="nvda-math-node-0" data-nvda-math-id-added="true">x</mi></math>'
		)
		result = navNodeMapping.removeSyntheticIdsFromMathMl(mathml)
		mi = ElementTree.fromstring(result).find("mi")
		assert mi is not None
		self.assertNotIn("id", mi.attrib)
		self.assertNotIn("data-nvda-math-id-added", mi.attrib)

	def test_removeSyntheticIdsFromMathMl_restoresOriginalId(self):
		mathml = (
			'<math><mi id="nvda-math-node-0" '
			'data-nvda-math-id-added="true" '
			'data-nvda-math-original-id="author-id">x</mi></math>'
		)
		result = navNodeMapping.removeSyntheticIdsFromMathMl(mathml)
		mi = ElementTree.fromstring(result).find("mi")
		assert mi is not None
		self.assertEqual(mi.get("id"), "author-id")
		self.assertNotIn("data-nvda-math-id-added", mi.attrib)
		self.assertNotIn("data-nvda-math-original-id", mi.attrib)
