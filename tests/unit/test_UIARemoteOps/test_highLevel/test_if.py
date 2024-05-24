# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for if conditions.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_if(TestCase):

	def test_if_true(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			true_condition = ra.newBool(True)
			was_in_if = ra.newBool(False)
			was_in_else = ra.newBool(False)
			with ra.ifBlock(true_condition):
				was_in_if.set(True)
			with ra.elseBlock():
				was_in_else.set(True)
			ra.Return(was_in_if, was_in_else)

		was_in_if, was_in_else = op.execute()
		self.assertTrue(was_in_if)
		self.assertFalse(was_in_else)

	def test_if_false(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			false_condition = ra.newBool(False)
			was_in_if = ra.newBool(False)
			was_in_else = ra.newBool(False)
			with ra.ifBlock(false_condition):
				was_in_if.set(True)
			with ra.elseBlock():
				was_in_else.set(True)
			ra.Return(was_in_if, was_in_else)

		was_in_if, was_in_else = op.execute()
		self.assertFalse(was_in_if)
		self.assertTrue(was_in_else)

	def test_else_no_if(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			with self.assertRaises(RuntimeError):
				with ra.elseBlock():
					pass

	def test_if_with_multiple_returns_first(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			condition = ra.newBool(True)
			with ra.ifBlock(condition):
				ra.Return(1)
			with ra.elseBlock():
				ra.Return(2)

		res = op.execute()
		self.assertEqual(res, 1)

	def test_if_with_multiple_returns_second(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			condition = ra.newBool(False)
			with ra.ifBlock(condition):
				ra.Return(1)
			with ra.elseBlock():
				ra.Return(2)

		res = op.execute()
		self.assertEqual(res, 2)

	def test_if_with_no_return(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			condition = ra.newBool(False)
			with ra.ifBlock(condition):
				ra.Return(1)

		with self.assertRaises(operation.NoReturnException):
			op.execute()
