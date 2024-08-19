# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for resizing a cell array before displaying on device. """

import braille
import unittest


class Test_normalizeCellArraySize(unittest.TestCase):
	"""
	Tests for BrailleHandler._normalizeCellArraySize.
	"""


	def test_shrinkSingleLine(self):
		oldCells = [1, 2, 3, 4, 5, 6, 7, 8]
		expectedNewCells = [1, 2, 3, 4]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 8, 1, 4, 1)
		self.assertEqual(newcells, expectedNewCells)

	def test_growSingleLine(self):
		oldCells = [1, 2, 3, 4]
		expectedNewCells = [1, 2, 3, 4, 0, 0, 0, 0]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 4, 1, 8, 1)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumRows(self):
		oldCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
			21, 22, 23, 24, 25,
		]
		expectedNewCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 15, 3, 10, 2)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumRows(self):
		oldCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
		]
		expectedNewCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
			0, 0, 0, 0, 0,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 10, 2, 15, 3)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumColumns(self):
		oldCells = [
			1, 2, 3, 4,
			11, 12, 13, 14,
			21, 22, 23, 24,
		]
		expectedNewCells = [
			1, 2,
			11, 12,
			21, 22,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 12, 3, 6, 3)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumColumns(self):
		oldCells = [
			1, 2,
			11, 12,
			21, 22,
		]
		expectedNewCells = [
			1, 2, 0, 0,
			11, 12, 0, 0,
			21, 22, 0, 0,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 6, 3, 12, 3)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumRowsAndColumns(self):
		oldCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
			21, 22, 23, 24, 25,
		]
		expectedNewCells = [
			1, 2,
			11, 12,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 15, 3, 4, 2)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumRowsAndColumns(self):
		oldCells = [
			1, 2,
			11, 12,
		]
		expectedNewCells = [
			1, 2, 0, 0,
			11, 12, 0, 0,
			0, 0, 0, 0,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 4, 2, 12, 3)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumRowsAndIncreaseNumColumns(self):
		oldCells = [
			1, 2,
			11, 12,
			21, 22,
		]
		expectedNewCells = [
			1, 2, 0, 0,
			11, 12, 0, 0,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 6, 3, 8, 2)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumRowsAndDecreaseNumColumns(self):
		oldCells = [
			1, 2, 3, 4,
			11, 12, 13, 14,
		]
		expectedNewCells = [
			1, 2,
			11, 12,
			0, 0,
		]
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(oldCells, 8, 2, 6, 3)
		self.assertEqual(newcells, expectedNewCells)
