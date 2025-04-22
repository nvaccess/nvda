# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for arrays.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_array(TestCase):

	def test_newArray(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			array = ra.newArray()
			ra.Return(array)

		array = op.execute()
		self.assertEqual(array, [])

	def test_append(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			array = ra.newArray()
			array.append("hello")
			array.append("goodbye")
			ra.Return(array)

		array = op.execute()
		self.assertEqual(array, ["hello", "goodbye"])

	def test_index(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			array = ra.newArray()
			array.append("hello")
			array.append("goodbye")
			a = array[0]
			b = array[1]
			ra.Return(a, b)

		a, b = op.execute()
		self.assertEqual(a, "hello")
		self.assertEqual(b, "goodbye")

	def test_remove(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			array = ra.newArray()
			array.append("hello")
			array.append("goodbye")
			array.remove(0)
			ra.Return(array)

		array = op.execute()
		self.assertEqual(array, ["goodbye"])

	def test_size(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			array = ra.newArray()
			initialSize = array.size()
			array.append("hello")
			array.append("goodbye")
			finalSize = array.size()
			ra.Return(initialSize, finalSize)

		initialSize, finalSize = op.execute()
		self.assertEqual(initialSize, 0)
		self.assertEqual(finalSize, 2)
