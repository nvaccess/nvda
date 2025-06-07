# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2025 NV Access Limited, Noelia Ruiz Martínez

"""Unit tests for the _calculate function in the braille module."""

import unittest

import braille
from braille import DisplayDimensions


def _getDisplayDimensions(dimensions: "DisplayDimensions") -> "DisplayDimensions":
	"""Called by the :attr:`braille.filter_displayDimensions` extension point to get the display dimensions."""
	return DisplayDimensions(
		numRows=2,
		numCols=20,
	)


class TestCalculate(unittest.TestCase):
	def setUp(self):
		braille.filter_displayDimensions.register(_getDisplayDimensions)

	def tearDown(self):
		braille.filter_displayDimensions.unregister(_getDisplayDimensions)

	def test_noCells(self):
		braille.handler.buffer.brailleCells = []
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 0)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_firstPosition(self):
		"""Checks that first offset is equal to start pos parameter."""
		braille.handler.buffer.brailleCells = [1] * braille.handler.displaySize
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		braille.handler.buffer._calculateWindowRowBufferOffsets(1)
		expectedOffsets = [(1, 21), (21, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
