# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited 

"""
Unit tests for the high-level UI Automation Remote Operations API. 
"""

import unittest

from UIAHandler._remoteOps.operation import LocalOperation


class TestHighLevel(unittest.TestCase):

	def test_bool_false(self):
		op = LocalOperation()

		with op.buildContext() as ra:
			b = ra.newBool(False)
			op.addToResults(b)

		op.execute()
		self.assertFalse(b.localValue)

	def test_bool_setTrue(self):
		op = LocalOperation()

		with op.buildContext() as ra:
			b = ra.newBool(False)
			op.addToResults(b)
			b.set(True)

		op.execute()
		self.assertTrue(b.localValue)

	def test_bool_inverse(self):
		op = LocalOperation()

		with op.buildContext() as ra:
			t = ra.newBool(True)
			f = ra.newBool(False)
			t_inverse = t.inverse()
			f_inverse = f.inverse()
			op.addToResults(t_inverse, f_inverse)

		op.execute()
		self.assertFalse(t_inverse.localValue)
		self.assertTrue(f_inverse.localValue)

	def test_bool_and(self):
		op = LocalOperation()

		with op.buildContext() as ra:
			t = ra.newBool(True)
			f = ra.newBool(False)
			t_and_t = t & t
			t_and_f = t & f
			f_and_t = f & t
			f_and_f = f & f
			op.addToResults(t_and_t, t_and_f, f_and_t, f_and_f)

		op.execute()
		self.assertTrue(t_and_t.localValue)
		self.assertFalse(t_and_f.localValue)
		self.assertFalse(f_and_t.localValue)
		self.assertFalse(f_and_f.localValue)

	def test_bool_or(self):
		op = LocalOperation()

		with op.buildContext() as ra:
			t = ra.newBool(True)
			f = ra.newBool(False)
			t_or_t = t | t
			t_or_f = t | f
			f_or_t = f | t
			f_or_f = f | f
			op.addToResults(t_or_t, t_or_f, f_or_t, f_or_f)

		op.execute()
		self.assertTrue(t_or_t.localValue)
		self.assertTrue(t_or_f.localValue)
		self.assertTrue(f_or_t.localValue)
		self.assertFalse(f_or_f.localValue)

	def test_if_true(self):
		op = LocalOperation()
		with op.buildContext() as ra:
			true_condition = ra.newBool(True)
			was_in_if = ra.newBool(False)
			was_in_else = ra.newBool(False)
			with ra.ifBlock(true_condition):
				was_in_if.set(True)
			with ra.elseBlock():
				was_in_else.set(True)
			op.addToResults(was_in_if, was_in_else)

		op.execute()
		self.assertTrue(was_in_if.localValue)
		self.assertFalse(was_in_else.localValue)

	def test_if_false(self):
		op = LocalOperation()
		with op.buildContext() as ra:
			false_condition = ra.newBool(False)
			was_in_if = ra.newBool(False)
			was_in_else = ra.newBool(False)
			with ra.ifBlock(false_condition):
				was_in_if.set(True)
			with ra.elseBlock():
				was_in_else.set(True)
			op.addToResults(was_in_if, was_in_else)

		op.execute()
		self.assertFalse(was_in_if.localValue)
		self.assertTrue(was_in_else.localValue)

	def test_int_inplace_add(self):
		op = LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(5)
			j = ra.newInt(3)
			i += j
			i += 2
			op.addToResults(i)

		op.execute()
		self.assertEqual(i.localValue, 10)
