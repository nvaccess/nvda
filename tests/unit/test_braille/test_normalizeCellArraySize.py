# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for resizing a cell array before displaying on device."""

import braille
import unittest


class Test_normalizeCellArraySize(unittest.TestCase):
	"""
	Tests for BrailleHandler._normalizeCellArraySize.
	"""

	def test_shrinkSingleLine(self):
		oldCells = [1, 2, 3, 4, 5, 6, 7, 8]  # fmt: skip
		expectedNewCells = [1, 2, 3, 4]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=8,
			oldNumRows=1,
			newCellCount=4,
			newNumRows=1,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_growSingleLine(self):
		oldCells = [1, 2, 3, 4]  # fmt: skip
		expectedNewCells = [1, 2, 3, 4, 0, 0, 0, 0]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=4,
			oldNumRows=1,
			newCellCount=8,
			newNumRows=1,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumRows(self):
		oldCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
			21, 22, 23, 24, 25,
		]  # fmt: skip
		expectedNewCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=15,
			oldNumRows=3,
			newCellCount=10,
			newNumRows=2,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumRows(self):
		oldCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
		]  # fmt: skip
		expectedNewCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
			0, 0, 0, 0, 0,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=10,
			oldNumRows=2,
			newCellCount=15,
			newNumRows=3,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumColumns(self):
		oldCells = [
			1, 2, 3, 4,
			11, 12, 13, 14,
			21, 22, 23, 24,
		]  # fmt: skip
		expectedNewCells = [
			1, 2,
			11, 12,
			21, 22,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=12,
			oldNumRows=3,
			newCellCount=6,
			newNumRows=3,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumColumns(self):
		oldCells = [
			1, 2,
			11, 12,
			21, 22,
		]  # fmt: skip
		expectedNewCells = [
			1, 2, 0, 0,
			11, 12, 0, 0,
			21, 22, 0, 0,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=6,
			oldNumRows=3,
			newCellCount=12,
			newNumRows=3,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumRowsAndColumns(self):
		oldCells = [
			1, 2, 3, 4, 5,
			11, 12, 13, 14, 15,
			21, 22, 23, 24, 25,
		]  # fmt: skip
		expectedNewCells = [
			1, 2,
			11, 12,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=15,
			oldNumRows=3,
			newCellCount=4,
			newNumRows=2,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumRowsAndColumns(self):
		oldCells = [
			1, 2,
			11, 12,
		]  # fmt: skip
		expectedNewCells = [
			1, 2, 0, 0,
			11, 12, 0, 0,
			0, 0, 0, 0,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=4,
			oldNumRows=2,
			newCellCount=12,
			newNumRows=3,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_decreaseNumRowsAndIncreaseNumColumns(self):
		oldCells = [
			1, 2,
			11, 12,
			21, 22,
		]  # fmt: skip
		expectedNewCells = [
			1, 2, 0, 0,
			11, 12, 0, 0,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=6,
			oldNumRows=3,
			newCellCount=8,
			newNumRows=2,
		)
		self.assertEqual(newcells, expectedNewCells)

	def test_increaseNumRowsAndDecreaseNumColumns(self):
		oldCells = [
			1, 2, 3, 4,
			11, 12, 13, 14,
		]  # fmt: skip
		expectedNewCells = [
			1, 2,
			11, 12,
			0, 0,
		]  # fmt: skip
		assert braille.handler is not None
		newcells = braille.handler._normalizeCellArraySize(
			oldCells,
			oldCellCount=8,
			oldNumRows=2,
			newCellCount=6,
			newNumRows=3,
		)
		self.assertEqual(newcells, expectedNewCells)
