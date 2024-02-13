# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited 

"""
Unit tests for the high-level UI Automation Remote Operations API. 
"""

import unittest

from UIAHandler._remoteOps import operation


class TestHighLevel(unittest.TestCase):

	def test_bool_false(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			b = ra.newBool(False)
			op.addToResults(b)

		op.execute()
		self.assertFalse(b.localValue)

	def test_bool_setTrue(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			b = ra.newBool(False)
			op.addToResults(b)
			b.set(True)

		op.execute()
		self.assertTrue(b.localValue)

	def test_bool_inverse(self):
		op = operation.LocalOperation()

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
		op = operation.LocalOperation()

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
		op = operation.LocalOperation()

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
		op = operation.LocalOperation()
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
		op = operation.LocalOperation()
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

	def test_else_no_if(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			with self.assertRaises(RuntimeError):
				with ra.elseBlock():
					pass

	def test_error(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(3)
			j = i / 0
			op.addToResults(j)

		with self.assertRaises(operation.UnhandledException):
			op.execute()

	def test_try_with_no_error(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(3)
			was_in_catch = ra.newBool(False)
			with ra.tryBlock():
				j = i + 1
			with ra.catchBlock():
				was_in_catch.set(True)
		op.addToResults(j, was_in_catch)

		op.execute()
		self.assertEqual(j.localValue, 4)
		self.assertFalse(was_in_catch.localValue)

	def test_try_with_error(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(3)
			was_in_catch = ra.newBool(False)
			with ra.tryBlock():
				j = i / 0
			with ra.catchBlock() as e:
				was_in_catch.set(True)
		op.addToResults(was_in_catch)

		op.execute()
		self.assertTrue(was_in_catch.localValue)


	def test_int_inplace_add(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(5)
			j = ra.newInt(3)
			i += j
			op.addToResults(i)

		op.execute()
		self.assertEqual(i.localValue, 8)

	def test_int_binary_add(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(3)
			j = ra.newInt(4)
			k = i + j
			op.addToResults(k)

		op.execute()
		self.assertEqual(k.localValue, 7)

	def test_compare_lowToHigh(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(3)
			j = ra.newInt(4)
			lt = i < j
			le = i <= j
			eq = i == j
			ne = i != j
			ge = i >= j
			gt = i > j
			op.addToResults(lt, le, eq, ne, ge, gt)

		op.execute()
		self.assertTrue(lt.localValue)
		self.assertTrue(le.localValue)
		self.assertFalse(eq.localValue)
		self.assertTrue(ne.localValue)
		self.assertFalse(ge.localValue)
		self.assertFalse(gt.localValue)

	def test_compare_highToLow(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(4)
			j = ra.newInt(3)
			lt = i < j
			le = i <= j
			eq = i == j
			ne = i != j
			ge = i >= j
			gt = i > j
			op.addToResults(lt, le, eq, ne, ge, gt)

		op.execute()
		self.assertFalse(lt.localValue)
		self.assertFalse(le.localValue)
		self.assertFalse(eq.localValue)
		self.assertTrue(ne.localValue)
		self.assertTrue(ge.localValue)
		self.assertTrue(gt.localValue)

	def test_compare_same(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(3)
			j = ra.newInt(3)
			lt = i < j
			le = i <= j
			eq = i == j
			ne = i != j
			ge = i >= j
			gt = i > j
			op.addToResults(lt, le, eq, ne, ge, gt)

		op.execute()
		self.assertFalse(lt.localValue)
		self.assertTrue(le.localValue)
		self.assertTrue(eq.localValue)
		self.assertFalse(ne.localValue)
		self.assertTrue(ge.localValue)
		self.assertFalse(gt.localValue)

	def test_while(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			counter = ra.newInt(0)
			with ra.whileBlock(lambda: counter < 7):
				counter += 2
			op.addToResults(counter)

		op.execute()
		self.assertEqual(counter.localValue, 8)

	def test_breakLoop(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			counter = ra.newInt(0)
			with ra.whileBlock(lambda: counter < 7):
				counter += 2
				with ra.ifBlock(counter == 4):
					ra.breakLoop()
			op.addToResults(counter)

		op.execute()
		self.assertEqual(counter.localValue, 4)

	def test_continueLoop(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			i = ra.newInt(0)
			j = ra.newInt(0)
			with ra.whileBlock(lambda: i < 7):
				i += 1
				with ra.ifBlock(i == 4):
					ra.continueLoop()
				j += 1
			op.addToResults(i, j)

		op.execute()
		self.assertEqual(i.localValue, 7)
		self.assertEqual(j.localValue, 6)

	def test_string_concat(self):
		op = operation.LocalOperation()

		with op.buildContext() as ra:
			s = ra.newString("hello")
			t = ra.newString(" world")
			u = (s + t)
			op.addToResults(u)

		op.execute()
		self.assertEqual(u.localValue, "hello world")
