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
		def h():
			called.append(True)
		extensionPoints.callWithSupportedKwargs(h, a=1)
		self.assertEqual(called, [True])

	def test_supportsLessKwargs(self):
		gotKwargs = {}
		def h(a=None):
			gotKwargs["a"] = a
		extensionPoints.callWithSupportedKwargs(h, a=1, b=2)
		self.assertEqual(gotKwargs, {"a": 1})

	def test_supportsExtraKwargs(self):
		gotKwargs = {}
		def h(a=None, b=2):
			gotKwargs["a"] = a
			gotKwargs["b"] = b
		extensionPoints.callWithSupportedKwargs(h, a=1)
		self.assertEqual(gotKwargs, {"a": 1, "b": 2})

	def test_supportsAllKwargs(self):
		gotKwargs = {}
		def h(**kwargs):
			gotKwargs.update(kwargs)
		extensionPoints.callWithSupportedKwargs(h, a=1)
		self.assertEqual(gotKwargs, {"a": 1})

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
		def h():
			called.append(h)
		self.action.register(h)
		self.action.notify()
		self.assertEqual(called, [h])

	def test_twoHandlers(self):
		called = []
		def h1():
			called.append(h1)
		def h2():
			called.append(h2)
		self.action.register(h1)
		self.action.register(h2)
		self.action.notify()
		self.assertEqual(called, [h1, h2])

	def test_kwargs(self):
		"""Test that keyword arguments get passed to handlers.
		"""
		calledKwargs = {}
		def h(**kwargs):
			calledKwargs.update(kwargs)
		self.action.register(h)
		self.action.notify(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerException(self):
		"""Test that a handler which raises an exception doesn't affect later handlers.
		"""
		called = []
		def h1():
			raise Exception("barf")
		def h2():
			called.append(h2)
		self.action.register(h1)
		self.action.register(h2)
		self.action.notify()
		self.assertEqual(called, [h2])

class TestFilter(unittest.TestCase):

	def setUp(self):
		self.filter = extensionPoints.Filter()

	def test_noHandlers(self):
		# We can only test that this doesn't fail.
		self.filter.apply("value", a=1)

	def test_oneHandler(self):
		def h(value):
			return 1
		self.filter.register(h)
		filtered = self.filter.apply(0)
		self.assertEqual(filtered, 1)

	def test_twoHandlers(self):
		def h1(value):
			return 1
		def h2(value):
			return 2
		self.filter.register(h1)
		self.filter.register(h2)
		filtered = self.filter.apply(0)
		self.assertEqual(filtered, 2)

	def test_kwargs(self):
		"""Test that keyword arguments get passed to handlers.
		"""
		calledKwargs = {}
		def h(value, **kwargs):
			calledKwargs.update(kwargs)
		self.filter.register(h)
		self.filter.apply(0, a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerException(self):
		"""Test that a handler which raises an exception doesn't affect later handlers.
		"""
		def h1(value):
			raise Exception("barf")
		def h2(value):
			return 2
		self.filter.register(h1)
		self.filter.register(h2)
		filtered = self.filter.apply(0)
		self.assertEqual(filtered, 2)
