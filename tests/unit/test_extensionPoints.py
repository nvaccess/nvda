#tests/unit/test_extensionPoints.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the extensionPoints module.
"""

import unittest
import extensionPoints

class ExampleClass(object):
	def method(self):
		return 42

def exampleFunc():
	return 3.14

class TestBoundMethodWeakref(unittest.TestCase):

	def onDelete(self, weak):
		self.deleted = weak

	def setUp(self):
		self.deleted = None
		self.instance = ExampleClass()
		self.weak = extensionPoints.BoundMethodWeakref(self.instance.method, self.onDelete)

	def test_get(self):
		"""Test that we get the right strong reference from the weak reference.
		"""
		method = self.weak()
		self.assertEqual(method, self.instance.method)

	def test_onDelete(self):
		"""Test that the deletion callback gets called.
		"""
		del self.instance
		self.assertEqual(self.deleted, self.weak)

	def test_isWeak(self):
		"""Test that this is actually a weak reference;
		i.e. that it dies when the instance dies.
		"""
		del self.instance
		method = self.weak()
		self.assertIsNone(method)

class TestCallWithSupportedKwargs(unittest.TestCase):

	def test_supportsNoKwargs(self):
		called = []
		def handler():
			called.append(True)
		extensionPoints.callWithSupportedKwargs(handler, a=1)
		self.assertEqual(called, [True])

	def test_supportsLessKwargs(self):
		gotKwargs = {}
		def handler(a=None):
			gotKwargs["a"] = a
		extensionPoints.callWithSupportedKwargs(handler, a=1, b=2)
		self.assertEqual(gotKwargs, {"a": 1})

	def test_supportsExtraKwargs(self):
		gotKwargs = {}
		def handler(a=None, b=2):
			gotKwargs["a"] = a
			gotKwargs["b"] = b
		extensionPoints.callWithSupportedKwargs(handler, a=1)
		self.assertEqual(gotKwargs, {"a": 1, "b": 2})

	def test_supportsAllKwargs(self):
		gotKwargs = {}
		def handler(**kwargs):
			gotKwargs.update(kwargs)
		extensionPoints.callWithSupportedKwargs(handler, a=1)
		self.assertEqual(gotKwargs, {"a": 1})

	def test_positionalsPassedWhenSupportsNoKwargs(self):
		"""Test that positional arguments are passed untouched.
		"""
		gotArgs = []
		def handler(a, b):
			gotArgs.append(a)
			gotArgs.append(b)
		extensionPoints.callWithSupportedKwargs(handler, 1, 2)
		self.assertEqual(gotArgs, [1, 2])

	def test_positionalsPassedWhenSupportsAllKwargs(self):
		"""Test that positional arguments are passed untouched when the function has **kwargs,
		since **kwargs is a special case early return in the code.
		"""
		gotArgs = []
		def handler(a, b, **kwargs):
			gotArgs.append(a)
			gotArgs.append(b)
		extensionPoints.callWithSupportedKwargs(handler, 1, 2, c=3)
		self.assertEqual(gotArgs, [1, 2])

class TestHandlerRegistrar(unittest.TestCase):

	def setUp(self):
		self.reg = extensionPoints.HandlerRegistrar()

	def test_noHandlers(self):
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [])

	def test_registerFunc(self):
		self.reg.register(exampleFunc)
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [exampleFunc])

	def test_registerInstanceMethod(self):
		inst = ExampleClass()
		self.reg.register(inst.method)
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [inst.method])

	def test_unregisterFunc(self):
		self.reg.register(exampleFunc)
		self.reg.unregister(exampleFunc)
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [])

	def test_unregisterInstanceMethod(self):
		inst = ExampleClass()
		self.reg.register(inst.method)
		self.reg.unregister(inst.method)
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [])

	def test_autoUnregisterFunc(self):
		"""Test that a function gets automatically unregistered when the function dies.
		"""
		def tempFunc():
			return 42
		self.reg.register(tempFunc)
		del tempFunc
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [])

	def test_autoUnregisterInstanceMethod(self):
		"""Test that a method gets automatically unregistered when the instance dies.
		"""
		inst = ExampleClass()
		self.reg.register(inst.method)
		del inst
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [])

	def test_registerMultiple(self):
		"""Test that registration of multiple handlers is ordered.
		"""
		inst3 = ExampleClass()
		inst2 = ExampleClass()
		inst1 = ExampleClass()
		self.reg.register(inst1.method)
		self.reg.register(inst2.method)
		self.reg.register(inst3.method)
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [inst1.method, inst2.method, inst3.method])

	def test_unregisterMiddle(self):
		"""Test behaviour when unregistering a handler registered between of other handlers.
		"""
		inst3 = ExampleClass()
		inst2 = ExampleClass()
		inst1 = ExampleClass()
		self.reg.register(inst1.method)
		self.reg.register(inst2.method)
		self.reg.register(inst3.method)
		self.reg.unregister(inst2.method)
		actual = list(self.reg.handlers)
		self.assertEqual(actual, [inst1.method, inst3.method])

class TestAction(unittest.TestCase):

	def setUp(self):
		self.action = extensionPoints.Action()

	def test_noHandlers(self):
		# We can only test that this doesn't fail.
		self.action.notify(a=1)

	def test_oneHandler(self):
		called = []
		def handler():
			called.append(handler)
		self.action.register(handler)
		self.action.notify()
		self.assertEqual(called, [handler])

	def test_twoHandlers(self):
		called = []
		def handler1():
			called.append(handler1)
		def handler2():
			called.append(handler2)
		self.action.register(handler1)
		self.action.register(handler2)
		self.action.notify()
		self.assertEqual(called, [handler1, handler2])

	def test_kwargs(self):
		"""Test that keyword arguments get passed to handlers.
		"""
		calledKwargs = {}
		def handler(**kwargs):
			calledKwargs.update(kwargs)
		self.action.register(handler)
		self.action.notify(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerException(self):
		"""Test that a handler which raises an exception doesn't affect later handlers.
		"""
		called = []
		def handler1():
			raise Exception("barf")
		def handler2():
			called.append(handler2)
		self.action.register(handler1)
		self.action.register(handler2)
		self.action.notify()
		self.assertEqual(called, [handler2])

class TestFilter(unittest.TestCase):

	def setUp(self):
		self.filter = extensionPoints.Filter()

	def test_noHandlers(self):
		# We can only test that this doesn't fail.
		self.filter.apply("value", a=1)

	def test_oneHandler(self):
		def handler(value):
			return 1
		self.filter.register(handler)
		filtered = self.filter.apply(0)
		self.assertEqual(filtered, 1)

	def test_twoHandlers(self):
		def handler1(value):
			return 1
		def handler2(value):
			return 2
		self.filter.register(handler1)
		self.filter.register(handler2)
		filtered = self.filter.apply(0)
		self.assertEqual(filtered, 2)

	def test_kwargs(self):
		"""Test that keyword arguments get passed to handlers.
		"""
		calledKwargs = {}
		def handler(value, **kwargs):
			calledKwargs.update(kwargs)
		self.filter.register(handler)
		self.filter.apply(0, a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerException(self):
		"""Test that a handler which raises an exception doesn't affect later handlers.
		"""
		def handler1(value):
			raise Exception("barf")
		def handler2(value):
			return 2
		self.filter.register(handler1)
		self.filter.register(handler2)
		filtered = self.filter.apply(0)
		self.assertEqual(filtered, 2)

class TestDecider(unittest.TestCase):

	def setUp(self):
		self.decider = extensionPoints.Decider()

	def test_noHandlers(self):
		decision = self.decider.decide(a=1)
		self.assertEqual(decision, True)

	def test_oneHandlerFalse(self):
		def handler():
			return False
		self.decider.register(handler)
		decision = self.decider.decide()
		self.assertEqual(decision, False)

	def test_oneHandlerTrue(self):
		def handler():
			return True
		self.decider.register(handler)
		decision = self.decider.decide()
		self.assertEqual(decision, True)

	def test_twoHandlersFalseTrue(self):
		def handler1():
			return False
		def handler2():
			return True
		self.decider.register(handler1)
		self.decider.register(handler2)
		decision = self.decider.decide()
		self.assertEqual(decision, False)

	def test_twoHandlersTrueFalse(self):
		def handler1():
			return True
		def handler2():
			return False
		self.decider.register(handler1)
		self.decider.register(handler2)
		decision = self.decider.decide()
		self.assertEqual(decision, False)

	def test_kwargs(self):
		"""Test that keyword arguments get passed to handlers.
		"""
		calledKwargs = {}
		def handler(**kwargs):
			calledKwargs.update(kwargs)
			return False
		self.decider.register(handler)
		self.decider.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerException(self):
		"""Test that a handler which raises an exception doesn't affect later handlers.
		"""
		def handler1():
			raise Exception("barf")
		def handler2():
			return False
		self.decider.register(handler1)
		self.decider.register(handler2)
		decision = self.decider.decide()
		self.assertEqual(decision, False)
