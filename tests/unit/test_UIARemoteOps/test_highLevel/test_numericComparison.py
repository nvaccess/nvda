# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for numeric comparisons.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_numericComparison(TestCase):

	def test_compare_lowToHigh(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = ra.newInt(4)
			lt = i < j
			le = i <= j
			eq = i == j
			ne = i != j
			ge = i >= j
			gt = i > j
			ra.Return(lt, le, eq, ne, ge, gt)

		lt, le, eq, ne, ge, gt = op.execute()
		self.assertTrue(lt)
		self.assertTrue(le)
		self.assertFalse(eq)
		self.assertTrue(ne)
		self.assertFalse(ge)
		self.assertFalse(gt)

	def test_compare_highToLow(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(4)
			j = ra.newInt(3)
			lt = i < j
			le = i <= j
			eq = i == j
			ne = i != j
			ge = i >= j
			gt = i > j
			ra.Return(lt, le, eq, ne, ge, gt)

		lt, le, eq, ne, ge, gt = op.execute()
		self.assertFalse(lt)
		self.assertFalse(le)
		self.assertFalse(eq)
		self.assertTrue(ne)
		self.assertTrue(ge)
		self.assertTrue(gt)

	def test_compare_same(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = ra.newInt(3)
			lt = i < j
			le = i <= j
			eq = i == j
			ne = i != j
			ge = i >= j
			gt = i > j
			ra.Return(lt, le, eq, ne, ge, gt)

		lt, le, eq, ne, ge, gt = op.execute()
		self.assertFalse(lt)
		self.assertTrue(le)
		self.assertTrue(eq)
		self.assertFalse(ne)
		self.assertTrue(ge)
		self.assertFalse(gt)
