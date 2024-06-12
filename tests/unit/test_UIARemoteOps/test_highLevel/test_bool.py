# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops unit tests for setting and comparing booleans.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_bool(TestCase):

	def test_false(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			b = ra.newBool(False)
			ra.Return(b)

		b = op.execute()
		self.assertFalse(b)

	def test_setTrue(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			b = ra.newBool(False)
			b.set(True)
			ra.Return(b)

		b = op.execute()
		self.assertTrue(b)

	def test_inverse(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			t = ra.newBool(True)
			f = ra.newBool(False)
			t_inverse = t.inverse()
			f_inverse = f.inverse()
			ra.Return(t_inverse, f_inverse)

		t_inverse, f_inverse = op.execute()
		self.assertFalse(t_inverse)
		self.assertTrue(f_inverse)

	def test_and(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			t = ra.newBool(True)
			f = ra.newBool(False)
			t_and_t = t & t
			t_and_f = t & f
			f_and_t = f & t
			f_and_f = f & f
			ra.Return(t_and_t, t_and_f, f_and_t, f_and_f)

		t_and_t, t_and_f, f_and_t, f_and_f = op.execute()
		self.assertTrue(t_and_t)
		self.assertFalse(t_and_f)
		self.assertFalse(f_and_t)
		self.assertFalse(f_and_f)

	def test_or(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			t = ra.newBool(True)
			f = ra.newBool(False)
			t_or_t = t | t
			t_or_f = t | f
			f_or_t = f | t
			f_or_f = f | f
			ra.Return(t_or_t, t_or_f, f_or_t, f_or_f)

		t_or_t, t_or_f, f_or_t, f_or_f = op.execute()
		self.assertTrue(t_or_t)
		self.assertTrue(t_or_f)
		self.assertTrue(f_or_t)
		self.assertFalse(f_or_f)
