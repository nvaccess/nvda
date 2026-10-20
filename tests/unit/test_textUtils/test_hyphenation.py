# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for textUtils.hyphenation."""

import unittest

from textUtils import hyphenation


class TestGetHyphenPositions(unittest.TestCase):
	def test_knownLanguage(self):
		"""Known language returns a non-empty tuple of ints within range(len(text))."""
		text = "hyphenation"
		positions = hyphenation.getHyphenPositions(text, "en_US")
		self.assertIsInstance(positions, tuple)
		self.assertGreater(len(positions), 0)
		for pos in positions:
			self.assertIsInstance(pos, int)
			self.assertGreaterEqual(pos, 0)
			self.assertLess(pos, len(text))

	def test_unknownLanguage_returnsEmptyTuple(self):
		"""Unknown language returns an empty tuple and does not raise."""
		positions = hyphenation.getHyphenPositions("anything", "zz_ZZ")
		self.assertEqual(positions, ())
		# Calling again should still return () and not raise.
		positions = hyphenation.getHyphenPositions("anything", "zz_ZZ")
		self.assertEqual(positions, ())
