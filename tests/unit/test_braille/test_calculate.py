# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2025 NV Access Limited, Noelia Ruiz Martínez

"""Unit tests for the _calculate function in the braille module."""

import unittest
import braille


class TestCalculate(unittest.TestCase):

	def setUp(self):
		self.handler = braille.handler

	def test_noCells(self):
		self.handler.buffer.brailleCells = []
		self.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 0)]
		self.assertEqual(self.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_firstPositionNotZero(self):
		self.handler.buffer.brailleCells = [1] * self.handler.displaySize
		self.handler.buffer._calculateWindowRowBufferOffsets(1)
		expectedOffsets = [(1, 40)]
		self.assertEqual(self.handler.buffer._windowRowBufferOffsets, expectedOffsets)
