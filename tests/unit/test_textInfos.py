# -*- coding: UTF-8 -*-
#tests/unit/test_textInfos.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the textInfos module, its submodules and classes."""

import unittest
from .textProvider import BasicTextProvider
import textInfos
from textInfos.offsets import Offsets

class TestCharacterOffsets(unittest.TestCase):
	"""
	Tests for textInfos.offsets.OffsetsTextInfo for its ability to deal with
	UTF-16 surrogate characters (i.e. whether a surrogate pair is treated as one character).
	These tests are also implicit tests for the textUtils module,
	as its logic is used for character offset calculation in wide character strings.
	"""

	def test_nonSurrogateForward(self):
		obj = BasicTextProvider(text="abc")
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at b
		self.assertEqual(ti.offsets, (1, 2)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (2, 3)) # One offset

	def test_nonSurrogateBackward(self):
		obj = BasicTextProvider(text="abc")
		ti = obj.makeTextInfo(Offsets(2, 2))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (2, 3)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at b
		self.assertEqual(ti.offsets, (1, 2)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset

	def test_surrogatePairsForward(self):
		obj = BasicTextProvider(text=u"\U0001f926\U0001f60a\U0001f44d") # 🤦😊👍
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (0, 2)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 😊
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 👍
		self.assertEqual(ti.offsets, (4, 6)) # Two offsets

	def test_surrogatePairsBackward(self):
		obj = BasicTextProvider(text=u"\U0001f926\U0001f60a\U0001f44d") # 🤦😊👍
		ti = obj.makeTextInfo(Offsets(5, 5))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 👍
		self.assertEqual(ti.offsets, (4, 6)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 😊
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (0, 2)) # Two offsets

	def test_mixedSurrogatePairsAndNonSurrogatesForward(self):
		obj = BasicTextProvider(text=u"a\U0001f926b") # a🤦b
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (1, 3)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (3, 4)) # One offset

	def test_mixedSurrogatePairsAndNonSurrogatesBackward(self):
		obj = BasicTextProvider(text=u"a\U0001f926b") # a🤦b
		ti = obj.makeTextInfo(Offsets(3, 3))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (3, 4)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (1, 3)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogatesForward(self):
		"""
		Tests surrogate pairs, non surrogates as well as
		single surrogate characters (i.e. incomplete pairs)
		"""
		obj = BasicTextProvider(text=u"a\ud83e\U0001f926\udd26b")
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🠀
		self.assertEqual(ti.offsets, (1, 2)) # Leading surrogate without a trailing surrogate
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 񙠀
		self.assertEqual(ti.offsets, (4, 5)) # Trailing surrogate without a leading surrogate.
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (5, 6)) # One offset

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogatesBackward(self):
		obj = BasicTextProvider(text=u"a\ud83e\U0001f926\udd26b")
		ti = obj.makeTextInfo(Offsets(5, 5))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (5, 6)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 񙠀
		self.assertEqual(ti.offsets, (4, 5)) # Trailing surrogate without a leading surrogate.
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🠀
		self.assertEqual(ti.offsets, (1, 2)) # Leading surrogate without a trailing surrogate
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset


class TestEndpoints(unittest.TestCase):

	def test_TextInfoEndpoint_largerAndSmaller(self):
		obj = BasicTextProvider(text="abcdef")
		ti = obj.makeTextInfo(Offsets(0, 2))
		smaller = ti.start
		larger = ti.end
		self.assertTrue(smaller < larger)
		self.assertFalse(larger < smaller)
		self.assertTrue(smaller <= larger)
		self.assertFalse(larger <= smaller)
		self.assertFalse(smaller >= larger)
		self.assertTrue(larger >= smaller)
		self.assertFalse(smaller > larger)
		self.assertTrue(larger > smaller)
		self.assertTrue(smaller != larger)
		self.assertTrue(larger != smaller)

	def test_TextInfoEndpoint_equal(self):
		obj = BasicTextProvider(text="abcdef")
		ti = obj.makeTextInfo(Offsets(1, 1))
		self.assertTrue(ti.start == ti.end)
		self.assertFalse(ti.start != ti.end)
		self.assertFalse(ti.start < ti.end)
		self.assertTrue(ti.start <= ti.end)
		self.assertTrue(ti.start >= ti.end)
		self.assertFalse(ti.start > ti.end)

	def test_setEndpoint(self):
		obj = BasicTextProvider(text="abcdef")
		ti1 = obj.makeTextInfo(Offsets(0, 2))
		ti2 = obj.makeTextInfo(Offsets(3, 5))
		ti1.end = ti2.end
		self.assertEqual((ti1._startOffset, ti1._endOffset), (0, 5))
		ti1.start = ti2.start
		self.assertEqual((ti1._startOffset, ti1._endOffset), (3, 5))
		ti1.end = ti2.start
		self.assertEqual((ti1._startOffset, ti1._endOffset), (3, 3))
		ti1.start = ti2.end
		self.assertEqual((ti1._startOffset, ti1._endOffset), (5, 5))
