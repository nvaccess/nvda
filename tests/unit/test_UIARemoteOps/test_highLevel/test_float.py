# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for floating point arithmetic.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_float(TestCase):

	def test_inplace_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(5.4)
			j = ra.newFloat(3.4)
			i += j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 8.8)

	def test_binary_add(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(3.3)
			j = ra.newFloat(4.4)
			k = i + j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7.7)

	def test_inplace_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(5.7)
			j = ra.newFloat(3.5)
			i -= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 2.2)

	def test_binary_subtract(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(7.3)
			j = ra.newFloat(3.2)
			k = i - j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 4.1)

	def test_inplace_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(5.0)
			j = ra.newFloat(3.0)
			i *= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 15.0)

	def test_binary_multiply(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(3.2)
			j = ra.newFloat(4.5)
			k = i * j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 14.4)

	def test_inplace_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(20.0)
			j = ra.newFloat(2.5)
			i /= j
			ra.Return(i)

		i = op.execute()
		self.assertEqual(i, 8.0)

	def test_binary_divide(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newFloat(21.0)
			j = ra.newFloat(3.0)
			k = i / j
			ra.Return(k)

		k = op.execute()
		self.assertEqual(k, 7.0)
