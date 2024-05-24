# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for integer arithmetic.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_int(TestCase):

	def test_inplace_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(5)
			j = ra.newInt(3)
			i += j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 8)

	def test_binary_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = ra.newInt(4)
			k = i + j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7)

	def test_inplace_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(5)
			j = ra.newInt(3)
			i -= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 2)

	def test_binary_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(7)
			j = ra.newInt(3)
			k = i - j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 4)

	def test_inplace_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(5)
			j = ra.newInt(3)
			i *= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 15)

	def test_binary_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = ra.newInt(4)
			k = i * j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 12)

	def test_inplace_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(18)
			j = ra.newInt(3)
			i /= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 6)

	def test_binary_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(21)
			j = ra.newInt(3)
			k = i / j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7)

	def test_inplace_mod(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(9)
			j = ra.newInt(2)
			i %= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 1)

	def test_binary_mod(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(10)
			j = ra.newInt(5)
			k = i % j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 0)
