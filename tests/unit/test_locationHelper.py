#tests/unit/test_locationHelper.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Unit tests for the locationHelper module.
"""

import unittest
from locationHelper import *

class TestRectOperators(unittest.TestCase):

	def test_and(self):
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4) & RectLTRB(left=3,top=3,right=5,bottom=5),RectLTRB(left=3,top=3,right=4,bottom=4))
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4) & RectLTRB(left=5,top=5,right=7,bottom=7),RectLTRB(left=0,top=0,right=0,bottom=0))

	def test_gt(self):
		self.assertGreater(RectLTRB(left=2,top=2,right=6,bottom=6),RectLTRB(left=2,top=2,right=4,bottom=4))
		self.assertGreaterEqual(RectLTRB(left=2,top=2,right=6,bottom=6),RectLTRB(left=2,top=2,right=4,bottom=4))

	def test_lt(self):
		self.assertLess(RectLTRB(left=2,top=2,right=4,bottom=4),RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertLessEqual(RectLTRB(left=2,top=2,right=4,bottom=4),RectLTRB(left=2,top=2,right=6,bottom=6))

	def test_in(self):
		self.assertIn(RectLTRB(left=2,top=2,right=4,bottom=4),RectLTRB(left=2,top=2,right=6,bottom=6))
		self.assertIn(Point(x=2,y=6),RectLTRB(left=2,top=2,right=6,bottom=6))

	def test_sub(self):
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4) - RectLTRB(left=3,top=3,right=5,bottom=5),RectLTRB(left=-1,top=-1,right=-1,bottom=-1))
		self.assertEqual(RectLTRB(left=2,top=2,right=4,bottom=4) - RectLTRB(left=5,top=5,right=8,bottom=8),RectLTRB(left=-3,top=-3,right=-4,bottom=0-4))

class TestRectUtilities(unittest.TestCase):

	def test_center(self):
		self.assertEqual(RectLTRB(left=-5,top=-5,right=5,bottom=5).center, Point(x=0,y=0))

class TestToRectLTRB(unittest.TestCase):

	def test_collection(self):
		rect=RectLTRB(left=10,top=15,right=500,bottom=1000)
		self.assertEqual(toRectLTRB(
			rect.topLeft, 
			rect.bottomRight, 
			rect.center, 
			Point(15,15),
			Point(20,20),
			Point(50,50),
			Point(400,400),
			RectLTRB(left=450,top=450,right=490,bottom=990)
		), rect)

	def test_integers(self):
		self.assertEqual(RectLTRB(left=10,top=10,right=20,bottom=20),toRectLTRB(10,10,20,20))

class TestToRectLTWH(unittest.TestCase):

	def test_collection(self):
		location=RectLTWH(left=10,top=15,width=500,height=1000)
		self.assertEqual(toRectLTWH(
			location.topLeft, 
			location.bottomRight, 
			location.center, 
			Point(15,15),
			Point(20,20),
			Point(50,50),
			Point(400,400),
			RectLTRB(left=450,top=450,right=505,bottom=1010)
		), location)

	def test_integers(self):
		self.assertEqual(RectLTWH(left=10,top=10,width=20,height=20),toRectLTWH(10,10,20,20))

class TestPointOperators(unittest.TestCase):

	def test_add(self):
		self.assertEqual(Point(x=2,y=4)+Point(x=2,y=4),Point(x=4,y=8))

	def test_sum(self):
		point=Point(x=2,y=4)
		self.assertEqual(sum((point, point, point)), Point(x=6,y=12))

	def test_sub(self):
		self.assertEqual(Point(x=2,y=4)-Point(x=4,y=8),Point(x=-2,y=-4))

	def test_gt(self):
		self.assertGreater(Point(x=3,y=4), Point(x=4,y=3))

	def test_lt(self):
		self.assertLess(Point(x=4,y=3), Point(x=3,y=4))


