# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited

"""
High-level UIA remote ops Unit tests for ints and floats including arithmetic and comparisons. 
"""

from unittest import TestCase
from unittest.mock import Mock
from ctypes import POINTER
from UIAHandler import UIA
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI
from UIAHandler._remoteOps.lowLevel import (
	PropertyId,
)


class Test_numeric(TestCase):

	def test_int_inplace_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(5)
			j = ra.newInt(3)
			i += j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 8)

	def test_int_binary_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = ra.newInt(4)
			k = i + j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7)

	def test_int_inplace_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(5)
			j = ra.newInt(3)
			i -= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 2)

	def test_int_binary_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(7)
			j = ra.newInt(3)
			k = i - j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 4)

	def test_int_inplace_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(5)
			j = ra.newInt(3)
			i *= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 15)

	def test_int_binary_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = ra.newInt(4)
			k = i * j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 12)

	def test_int_inplace_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(18)
			j = ra.newInt(3)
			i /= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 6)

	def test_int_binary_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(21)
			j = ra.newInt(3)
			k = i / j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7)

	def test_int_inplace_mod(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(9)
			j = ra.newInt(2)
			i %= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 1)

	def test_int_binary_mod(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(10)
			j = ra.newInt(5)
			k = i % j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 0)

	def test_float_inplace_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(5.4)
			j = ra.newFloat(3.4)
			i += j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 8.8)

	def test_float_binary_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(3.3)
			j = ra.newFloat(4.4)
			k = i + j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7.7)

	def test_float_inplace_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(5.7)
			j = ra.newFloat(3.5)
			i -= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 2.2)

	def test_float_binary_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(7.3)
			j = ra.newFloat(3.2)
			k = i - j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 4.1)

	def test_float_inplace_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(5.0)
			j = ra.newFloat(3.0)
			i *= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 15.0)

	def test_float_binary_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(3.2)
			j = ra.newFloat(4.5)
			k = i * j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 14.4)

	def test_float_inplace_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(20.0)
			j = ra.newFloat(2.5)
			i /= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 8.0)

	def test_float_binary_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(21.0)
			j = ra.newFloat(3.0)
			k = i / j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7.0)

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
