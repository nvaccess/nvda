# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import unittest
from tactile import TactileGraphicsBuffer
from tactile.drawing import drawLine, drawRectangle


class MockTactileBuffer(TactileGraphicsBuffer):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.dots = set()

	def setDot(self, x: int, y: int):
		self.dots.add((x, y))


class TestTactileDrawing(unittest.TestCase):
	def setUp(self):
		self.buffer = MockTactileBuffer(20, 15)

	def test_drawLine_horizontal(self):
		drawLine(self.buffer, 1, 1, 5, 1)
		expected_dots = {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)}
		self.assertEqual(self.buffer.dots, expected_dots)

	def test_drawLine_vertical(self):
		drawLine(self.buffer, 1, 1, 1, 5)
		expected_dots = {(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)}
		self.assertEqual(self.buffer.dots, expected_dots)

	def test_drawLine_diagonal(self):
		drawLine(self.buffer, 0, 0, 2, 2)
		expected_dots = {(0, 0), (1, 1), (2, 2)}
		self.assertEqual(self.buffer.dots, expected_dots)

	def test_drawLine_outOfBounds(self):
		# Line partially out of bounds
		drawLine(self.buffer, -1, -1, 2, 2)
		expected_dots = {(0, 0), (1, 1), (2, 2)}
		self.assertEqual(self.buffer.dots, expected_dots)

	def test_drawRectangle_outline(self):
		drawRectangle(self.buffer, 1, 1, 3, 3, fill=False)
		expected_dots = {
			(1, 1), (2, 1), (3, 1),  # Top edge
			(1, 2), (3, 2),          # Middle edges
			(1, 3), (2, 3), (3, 3)   # Bottom edge
		}
		self.assertEqual(self.buffer.dots, expected_dots)

	def test_drawRectangle_filled(self):
		drawRectangle(self.buffer, 1, 1, 2, 2, fill=True)
		expected_dots = {
			(1, 1), (2, 1),  # Top row
			(1, 2), (2, 2)   # Bottom row
		}
		self.assertEqual(self.buffer.dots, expected_dots)

	def test_drawRectangle_outOfBounds(self):
		# Rectangle partially out of bounds
		drawRectangle(self.buffer, -1, -1, 3, 3, fill=True)
		expected_dots = {
			(0, 0), (1, 0),
			(0, 1), (1, 1)
		}
		self.assertEqual(self.buffer.dots, expected_dots)
