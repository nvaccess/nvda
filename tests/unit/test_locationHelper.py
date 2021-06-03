# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2021 NV Access Limited, Babbage B.V., Łukasz Golonka

"""Unit tests for the locationHelper module.
"""

import unittest
from locationHelper import Point, RectLTRB, RectLTWH
from ctypes.wintypes import RECT, POINT

class TestRectOperators(unittest.TestCase):

	def test_intersection(self):
		self.assertEqual(RectLTRB(left=2, top=2, right=4, bottom=4).intersection(RectLTRB(left=3, top=3, right=5, bottom=5)), RectLTRB(left=3, top=3, right=4, bottom=4))
		self.assertEqual(RectLTRB(left=2, top=2, right=4, bottom=4).intersection(RectLTRB(left=5, top=5, right=7, bottom=7)), RectLTRB(left=0, top=0, right=0, bottom=0))

	def test_superset(self):
		self.assertTrue(RectLTRB(left=2, top=2, right=6, bottom=6).isSuperset(RectLTRB(left=2, top=2, right=4, bottom=4)))
		self.assertFalse(RectLTRB(left=2, top=2, right=4, bottom=4).isSuperset(RectLTRB(left=2, top=2, right=6, bottom=6)))
		self.assertTrue(RectLTRB(left=2, top=2, right=6, bottom=6).isSuperset(RectLTRB(left=2, top=2, right=6, bottom=6)))

	def test_subset(self):
		self.assertTrue(RectLTRB(left=2, top=2, right=4, bottom=4).isSubset(RectLTRB(left=2, top=2, right=6, bottom=6)))
		self.assertFalse(RectLTRB(left=2, top=2, right=6, bottom=6).isSubset(RectLTRB(left=2, top=2, right=4, bottom=4)))
		self.assertTrue(RectLTRB(left=2, top=2, right=6, bottom=6).isSubset(RectLTRB(left=2, top=2, right=6, bottom=6)))

	def test_in(self):
		rect = RectLTRB(left=2, top=2, right=6, bottom=6)
		self.assertIn(RectLTRB(left=2, top=2, right=4, bottom=4), rect)
		self.assertNotIn(rect, rect)
		self.assertIn(Point(x=2, y=2), rect)
		self.assertIn(Point(x=4, y=4), rect)
		self.assertNotIn(Point(x=2, y=6), rect)
		self.assertNotIn(Point(x=6, y=2), rect)
		self.assertNotIn(Point(x=6, y=6), rect)

	def test_equal(self):
		self.assertEqual(RectLTRB(left=2, top=2, right=4, bottom=4), RectLTRB(left=2, top=2, right=4, bottom=4))
		self.assertNotEqual(RectLTRB(left=2, top=2, right=4, bottom=4), RectLTRB(left=2, top=2, right=6, bottom=6))
		self.assertEqual(RectLTRB(left=2, top=2, right=4, bottom=4), RectLTWH(left=2, top=2, width=2, height=2))
		self.assertNotEqual(RectLTRB(left=2, top=2, right=4, bottom=4), RectLTWH(left=2, top=2, width=4, height=4))

	def test_ctypesRECT(self):
		# Intersection
		self.assertEqual(RectLTRB(left=2, top=2, right=4, bottom=4).intersection(RECT(left=3, top=3, right=5, bottom=5)), RectLTRB(left=3, top=3, right=4, bottom=4))
		# Superset
		self.assertTrue(RectLTRB(left=2, top=2, right=6, bottom=6).isSuperset(RECT(left=2, top=2, right=4, bottom=4)))
		# Subset
		self.assertTrue(RectLTRB(left=2, top=2, right=4, bottom=4).isSubset(RECT(left=2, top=2, right=6, bottom=6)))
		# in
		self.assertIn(RECT(left=2, top=2, right=4, bottom=4), RectLTRB(left=2, top=2, right=6, bottom=6))
		self.assertNotIn(RECT(left=2, top=2, right=4, bottom=4), RectLTRB(left=2, top=2, right=4, bottom=4))
		# Equality
		self.assertEqual(RECT(left=2, top=2, right=4, bottom=4), RectLTRB(left=2, top=2, right=4, bottom=4))
		self.assertNotEqual(RECT(left=2, top=2, right=4, bottom=4), RectLTRB(left=2, top=2, right=6, bottom=6))

class TestRectUtilities(unittest.TestCase):

	def test_points(self):
		rect = RectLTRB(left=-5, top=-5, right=5, bottom=5)
		self.assertEqual(rect.topLeft, Point(x=-5, y=-5))
		self.assertEqual(rect.topRight, Point(x=5, y=-5))
		self.assertEqual(rect.bottomLeft, Point(x=-5, y=5))
		self.assertEqual(rect.bottomRight, Point(x=5, y=5))
		self.assertEqual(rect.center, Point(x=0, y=0))
		# Specifically test some other edge cases for center
		self.assertEqual(RectLTRB(left=10, top=10, right=20, bottom=20).center, Point(x=15, y=15))
		self.assertEqual(RectLTRB(left=-20, top=-20, right=-10, bottom=-10).center, Point(x=-15, y=-15))
		self.assertEqual(RectLTRB(left=10, top=10, right=21, bottom=21).center, Point(x=16, y=16))
		self.assertEqual(RectLTRB(left=-21, top=-21, right=-10, bottom=-10).center, Point(x=-16, y=-16))

	def test_collection(self):
		"""Tests whether a collection of several rectangle and point types convert to the expected L{RectLTRB}."""
		rect=RectLTRB(left=10, top=15, right=500, bottom=1000)
		self.assertEqual(RectLTRB.fromCollection(
			rect.topLeft,
			rect.bottomRight,
			rect.center,
			Point(15, 15),
			Point(20, 20),
			Point(50, 50),
			Point(400, 400),
			POINT(x=15, y=15),
			POINT(x=20, y=20),
			POINT(x=50, y=50),
			POINT(x=400, y=400),
			RectLTRB(left=450, top=450, right=490, bottom=990),
			RECT(450, 450, 490, 990)
		), rect)

		location=RectLTWH(left=10, top=15, width=500, height=1000)
		self.assertEqual(RectLTWH.fromCollection(
			location.topLeft,
			location.bottomRight,
			location.center,
			Point(15, 15),
			Point(20, 20),
			Point(50, 50),
			Point(400, 400),
			POINT(x=15, y=15),
			POINT(x=20, y=20),
			POINT(x=50, y=50),
			POINT(x=400, y=400),
			RectLTRB(left=450, top=450, right=505, bottom=1010),
			RECT(450, 450, 490, 990)
		), location)

	def test_fromFloatCollection(self):
		self.assertEqual(RectLTRB(left=10, top=10, right=20, bottom=20), RectLTRB.fromFloatCollection(10.0, 10.0, 20.0, 20.0))
		self.assertEqual(RectLTWH(left=10, top=10, width=20, height=20), RectLTWH.fromFloatCollection(10.0, 10.0, 20.0, 20.0))

	def test_valueErrorForUnsuportedInput(self):
		self.assertRaises(ValueError, RectLTRB, left=10, top=10, right=9, bottom=9)

	def test_expandOrShrink(self):
		"""Tests the expand or shrink functionality to resize a rectangle given a specified margin."""
		rect = RectLTRB(left=10, top=10, right=20, bottom=20)
		self.assertEqual(rect.expandOrShrink(10), RectLTRB(left=0, top=0, right=30, bottom=30))
		self.assertEqual(rect.expandOrShrink(-2), RectLTRB(left=12, top=12, right=18, bottom=18))
		self.assertRaises(RuntimeError, rect.expandOrShrink, -10)

		location = RectLTWH(left=10, top=10, width=10, height=10)
		self.assertEqual(location.expandOrShrink(10), RectLTWH(left=0, top=0, width=30, height=30))
		self.assertEqual(location.expandOrShrink(-2), RectLTWH(left=12, top=12, width=6, height=6))
		self.assertRaises(RuntimeError, location.expandOrShrink, -10)

class TestPointOperators(unittest.TestCase):

	def test_add(self):
		self.assertEqual(Point(x=2, y=4)+Point(x=2, y=4),Point(x=4, y=8))

	def test_sum(self):
		point=Point(x=2, y=4)
		self.assertEqual(sum((point, point, point)), Point(x=6, y=12))

	def test_sub(self):
		self.assertEqual(Point(x=2, y=4)-Point(x=4, y=8),Point(x=-2, y=-4))

	def test_greaterThan(self):
		self.assertTrue(Point(x=3, y=4).yWiseGreaterThan(Point(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).xWiseGreaterThan(Point(x=4, y=3)))
		self.assertTrue(Point(x=4, y=3).xWiseGreaterThan(Point(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).yWiseGreaterThan(Point(x=3, y=4)))
		self.assertTrue(Point(x=3, y=4).yWiseGreaterOrEq(Point(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).xWiseGreaterOrEq(Point(x=4, y=3)))
		self.assertTrue(Point(x=4, y=3).xWiseGreaterOrEq(Point(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).yWiseGreaterOrEq(Point(x=3, y=4)))

	def test_lessThan(self):
		self.assertTrue(Point(x=4, y=3).yWiseLessThan(Point(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).xWiseLessThan(Point(x=3, y=4)))
		self.assertTrue(Point(x=3, y=4).xWiseLessThan(Point(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).yWiseLessThan(Point(x=4, y=3)))
		self.assertTrue(Point(x=4, y=3).yWiseLessOrEq(Point(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).xWiseLessOrEq(Point(x=3, y=4)))
		self.assertTrue(Point(x=3, y=4).xWiseLessOrEq(Point(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).yWiseLessOrEq(Point(x=4, y=3)))

	def test_equal(self):
		self.assertEqual(Point(x=4, y=3), Point(x=4, y=3))
		self.assertNotEqual(Point(x=3, y=4), Point(x=4, y=3))

	def test_ctypesPOINT(self):
		# Add
		self.assertEqual(Point(x=2, y=4)+POINT(x=2, y=4),Point(x=4, y=8))
		self.assertEqual(POINT(x=2, y=4)+Point(x=2, y=4),Point(x=4, y=8))
		# Sum
		self.assertEqual(sum((Point(x=2, y=4), POINT(x=2, y=4), Point(x=2, y=4))), Point(x=6, y=12))
		# Subtract
		self.assertEqual(Point(x=2, y=4)-POINT(x=4, y=8),Point(x=-2, y=-4))
		self.assertEqual(POINT(x=2, y=4)-Point(x=4, y=8),Point(x=-2, y=-4))
		# Greater than
		self.assertTrue(Point(x=3, y=4).yWiseGreaterThan(POINT(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).xWiseGreaterThan(POINT(x=4, y=3)))
		self.assertTrue(Point(x=4, y=3).xWiseGreaterThan(POINT(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).yWiseGreaterThan(POINT(x=3, y=4)))
		self.assertTrue(Point(x=3, y=4).yWiseGreaterOrEq(POINT(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).xWiseGreaterOrEq(POINT(x=4, y=3)))
		self.assertTrue(Point(x=4, y=3).xWiseGreaterOrEq(POINT(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).yWiseGreaterOrEq(POINT(x=3, y=4)))
		# Less than
		self.assertTrue(Point(x=4, y=3).yWiseLessThan(POINT(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).xWiseLessThan(POINT(x=3, y=4)))
		self.assertTrue(Point(x=3, y=4).xWiseLessThan(POINT(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).yWiseLessThan(POINT(x=4, y=3)))
		self.assertTrue(Point(x=4, y=3).yWiseLessOrEq(POINT(x=3, y=4)))
		self.assertFalse(Point(x=4, y=3).xWiseLessOrEq(POINT(x=3, y=4)))
		self.assertTrue(Point(x=3, y=4).xWiseLessOrEq(POINT(x=4, y=3)))
		self.assertFalse(Point(x=3, y=4).yWiseLessOrEq(POINT(x=4, y=3)))
		# Equality
		self.assertEqual(POINT(x=4, y=3), Point(x=4, y=3))
		self.assertNotEqual(POINT(x=3, y=4), Point(x=4, y=3))


class TestFailuresFromUnexpectedTypes(unittest.TestCase):

	def test_PointFailures(self):
		self.assertRaises(TypeError, Point.fromFloatCollection, 22.22, 22, 33)
		self.assertRaises(TypeError, Point.fromCompatibleType, 22.22)
		self.assertRaises(TypeError, Point.fromDWORD, 22.22)

	def test_RectLTRBFailures(self):
		self.assertRaises(TypeError, RectLTRB.fromFloatCollection, 22, 33.33, 44.44)
		self.assertRaises(TypeError, RectLTRB.fromCompatibleType, 33.33)
		self.assertRaises(TypeError, RectLTRB.fromPoint, 33.33)
		self.assertRaises(TypeError, RectLTRB.fromCollection)
		self.assertRaises(ValueError, RectLTRB.fromCollection, 22.22)

	def test_RectLTWHFailures(self):
		self.assertRaises(TypeError, RectLTWH.fromFloatCollection, 22, 33.33, 44.44)
		self.assertRaises(TypeError, RectLTWH.fromCompatibleType, 33.33)
		self.assertRaises(TypeError, RectLTWH.fromPoint, 33.33)
		self.assertRaises(TypeError, RectLTWH.fromCollection)
		self.assertRaises(ValueError, RectLTWH.fromCollection, 22.22)
