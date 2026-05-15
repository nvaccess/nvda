# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the _get_windowBrailleCells property in the braille module."""

import unittest

import braille


def _getDisplayDimensions(dimensions: braille.DisplayDimensions) -> braille.DisplayDimensions:
	"""Used to build a braille handler with particular dimensions."""
	return braille.DisplayDimensions(
		numRows=2,
		numCols=20,
	)


class TestWindowBrailleCells(unittest.TestCase):
	def setUp(self):
		braille.filter_displayDimensions.register(_getDisplayDimensions)

	def tearDown(self):
		braille.filter_displayDimensions.unregister(_getDisplayDimensions)

	def test_continuationRow_hasContinuationShape(self):
		"""A row present in _continuationRows gets CONTINUATION_SHAPE as its last cell."""
		buffer = braille.handler.buffer
		# 15 real cells in row 0, remainder will be padded; row index 0 is marked.
		buffer.brailleCells = [1] * 15 + [1] * 5
		buffer._windowRowBufferOffsets = [(0, 15), (15, 20)]
		buffer._continuationRows = [0]
		cells = buffer.windowBrailleCells
		# First row: 15 real cells, then CONTINUATION_SHAPE, then 4 padding zeroes.
		self.assertEqual(len(cells), 40)
		self.assertEqual(cells[15], braille.CONTINUATION_SHAPE)
		self.assertEqual(cells[16:20], [0, 0, 0, 0])

	def test_nonContinuationRow_lastCellIsZero(self):
		"""A row absent from _continuationRows has padding zero, not CONTINUATION_SHAPE."""
		buffer = braille.handler.buffer
		buffer.brailleCells = [1] * 15 + [1] * 5
		buffer._windowRowBufferOffsets = [(0, 15), (15, 20)]
		buffer._continuationRows = []
		cells = buffer.windowBrailleCells
		# No continuation marker anywhere; positions 15..19 of row 0 should all be 0.
		self.assertEqual(cells[15:20], [0, 0, 0, 0, 0])
		self.assertNotIn(braille.CONTINUATION_SHAPE, cells)
