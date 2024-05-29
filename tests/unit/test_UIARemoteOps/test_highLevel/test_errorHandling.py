# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for error handling including try, except, and uncaught errors.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_errorHandling(TestCase):

	def test_error(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			j = i / 0
			ra.Return(j)

		with self.assertRaises(operation.UnhandledException):
			op.execute()

	def test_try_with_no_error(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			was_in_catch = ra.newBool(False)
			with ra.tryBlock():
				j = i + 1
			with ra.catchBlock():
				was_in_catch.set(True)
			ra.Return(j, was_in_catch)

		j, was_in_catch = op.execute()
		self.assertEqual(j, 4)
		self.assertFalse(was_in_catch)

	def test_try_with_error(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(3)
			was_in_catch = ra.newBool(False)
			with ra.tryBlock():
				i / 0
			with ra.catchBlock():
				was_in_catch.set(True)
			ra.Return(i, was_in_catch)

		i, was_in_catch = op.execute()
		self.assertEqual(i, 3)
		self.assertTrue(was_in_catch)
