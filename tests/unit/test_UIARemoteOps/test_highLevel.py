# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited

"""
Unit tests for the high-level UI Automation Remote Operations API.
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


class TestHighLevel(TestCase):

	def test_bool_false(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			b = ra.newBool(False)
			ra.Return(b)

		b = op.execute()
		self.assertFalse(b)

	def test_bool_setTrue(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			b = ra.newBool(False)
			b.set(True)
			ra.Return(b)

		b = op.execute()
		self.assertTrue(b)

	def test_bool_inverse(self):
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

	def test_bool_and(self):
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

	def test_bool_or(self):
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

	def test_multiple_returns_first(self):
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

	def test_multiple_returns_second(self):
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

	def test_no_return(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			condition = ra.newBool(False)
			with ra.ifBlock(condition):
				ra.Return(1)

		with self.assertRaises(operation.NoReturnException):
			op.execute()

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
			ra.Return(was_in_catch)

		was_in_catch = op.execute()
		self.assertTrue(was_in_catch)

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

	def test_while(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			counter = ra.newInt(0)
			with ra.whileBlock(lambda: counter < 7):
				counter += 2
			ra.Return(counter)

		counter = op.execute()
		self.assertEqual(counter, 8)

	def test_breakLoop(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			counter = ra.newInt(0)
			with ra.whileBlock(lambda: counter < 7):
				counter += 2
				with ra.ifBlock(counter == 4):
					ra.breakLoop()
			ra.Return(counter)

		counter = op.execute()
		self.assertEqual(counter, 4)

	def test_continueLoop(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(0)
			j = ra.newInt(0)
			with ra.whileBlock(lambda: i < 7):
				i += 1
				with ra.ifBlock(i == 4):
					ra.continueLoop()
				j += 1
			ra.Return(i, j)

		i, j = op.execute()
		self.assertEqual(i, 7)
		self.assertEqual(j, 6)

	def test_string_concat(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			s = ra.newString("hello")
			t = ra.newString(" world")
			u = (s + t)
			ra.Return(u)

		u = op.execute()
		self.assertEqual(u, "hello world")

	def test_element_getName(self):
		uiaElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement(uiaElement)
			name = element.getPropertyValue(PropertyId.Name)
			ra.Return(name)

		uiaElement.GetCurrentPropertyValueEx.return_value = "foo"
		name = op.execute()
		uiaElement.GetCurrentPropertyValueEx.assert_called_once_with(PropertyId.Name, False)
		self.assertEqual(name, "foo")

	def test_instructionLimitExceeded(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(0)
			with ra.whileBlock(lambda: i < 20000):
				i += 1
			ra.Return(i)

		with self.assertRaises(operation.InstructionLimitExceededException):
			op.execute()

	def test_instructionLimitExceeded_with_static(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			executionCount = ra.newInt(0, static=True)
			executionCount += 1
			i = ra.newInt(0, static=True)
			with ra.whileBlock(lambda: i < 20000):
				i += 1
			ra.Return(executionCount, i)

		executionCount, i = op.execute(maxTries=20)
		self.assertEqual(i, 20000)
		self.assertEqual(executionCount, 9)

	def test_iterableFunction(self):
		op = operation.Operation(localMode=True)

		@op.buildIterableFunction
		def code(ra: remoteAPI.RemoteAPI):
			i = ra.newInt(0)
			with ra.whileBlock(lambda: i < 4):
				ra.Yield(i)
				i += 1

		results = []
		for i in op.iterExecute():
			results.append(i)
		self.assertEqual(results, [0, 1, 2, 3])

	def test_long_iterableFunction(self):
		op = operation.Operation(localMode=True)

		@op.buildIterableFunction
		def code(ra: remoteAPI.RemoteAPI):
			executionCount = ra.newInt(0, static=True)
			executionCount += 1
			i = ra.newInt(0, static=True)
			j = ra.newInt(0, static=True)
			with ra.whileBlock(lambda: i < 5000):
				with ra.ifBlock(j == 1000):
					ra.Yield(i)
					j.set(0)
				i += 1
				j += 1
			ra.Yield(executionCount)

		results = []
		for i in op.iterExecute(maxTries=20):
			results.append(i)
		self.assertEqual(results[:-1], list(range(1000, 5000, 1000)))
		self.assertEqual(results[-1], 4)

	def test_forEachNumInRange(self):
		op = operation.Operation(localMode=True)

		@op.buildIterableFunction
		def code(ra: remoteAPI.RemoteAPI):
			with ra.forEachNumInRange(10, 15) as i:
				ra.Yield(i)

		results = []
		for i in op.iterExecute():
			results.append(i)
		self.assertEqual(results, [10, 11, 12, 13, 14])

	def test_forEachItemInArray(self):
		op = operation.Operation(localMode=True)

		@op.buildIterableFunction
		def code(ra: remoteAPI.RemoteAPI):
			array = ra.newArray()
			with ra.forEachNumInRange(0, 10, 2) as i:
				array.append(i)
			with ra.forEachItemInArray(array) as item:
				ra.Yield(item)

		results = []
		for i in op.iterExecute():
			results.append(i)
		self.assertEqual(results, [0, 2, 4, 6, 8])
