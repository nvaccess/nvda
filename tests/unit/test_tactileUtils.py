# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import unittest
from tactile import TactileGraphicsBuffer
from tactile.utils import isPointInBounds, setDotIfInBounds, getLineDirections


class MockTactileBuffer(TactileGraphicsBuffer):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.dots = set()

	def setDot(self, x: int, y: int):
		self.dots.add((x, y))


class TestTactileUtils(unittest.TestCase):
	def setUp(self):
		self.buffer = MockTactileBuffer(10, 8)

	def test_isPointInBounds(self):
		# Test points inside bounds
		self.assertTrue(isPointInBounds(self.buffer, 0, 0))  # Origin
		self.assertTrue(isPointInBounds(self.buffer, 9, 7))  # Far corner
		self.assertTrue(isPointInBounds(self.buffer, 5, 4))  # Middle

		# Test points outside bounds
		self.assertFalse(isPointInBounds(self.buffer, -1, 0))  # Left edge
		self.assertFalse(isPointInBounds(self.buffer, 0, -1))  # Top edge
		self.assertFalse(isPointInBounds(self.buffer, 10, 5))  # Right edge
		self.assertFalse(isPointInBounds(self.buffer, 5, 8))  # Bottom edge
		self.assertFalse(isPointInBounds(self.buffer, -1, -1))  # Outside corner

	def test_setDotIfInBounds(self):
		# Test setting dots inside bounds
		setDotIfInBounds(self.buffer, 1, 1)
		self.assertIn((1, 1), self.buffer.dots)

		setDotIfInBounds(self.buffer, 8, 6)
		self.assertIn((8, 6), self.buffer.dots)

		# Test setting dots outside bounds
		setDotIfInBounds(self.buffer, -1, 5)
		self.assertNotIn((-1, 5), self.buffer.dots)

		setDotIfInBounds(self.buffer, 15, 15)
		self.assertNotIn((15, 15), self.buffer.dots)

	def test_getLineDirections(self):
		# Test horizontal line right
		dx, dy, xDir, yDir = getLineDirections(0, 0, 5, 0)
		self.assertEqual((dx, dy, xDir, yDir), (5, 0, 1, 1))

		# Test horizontal line left
		dx, dy, xDir, yDir = getLineDirections(5, 0, 0, 0)
		self.assertEqual((dx, dy, xDir, yDir), (5, 0, -1, 1))

		# Test vertical line down
		dx, dy, xDir, yDir = getLineDirections(0, 0, 0, 5)
		self.assertEqual((dx, dy, xDir, yDir), (0, 5, 1, 1))

		# Test vertical line up
		dx, dy, xDir, yDir = getLineDirections(0, 5, 0, 0)
		self.assertEqual((dx, dy, xDir, yDir), (0, 5, 1, -1))

		# Test diagonal line
		dx, dy, xDir, yDir = getLineDirections(0, 0, 3, 3)
		self.assertEqual((dx, dy, xDir, yDir), (3, 3, 1, 1))

		# Test diagonal line reverse
		dx, dy, xDir, yDir = getLineDirections(3, 3, 0, 0)
		self.assertEqual((dx, dy, xDir, yDir), (3, 3, -1, -1))
