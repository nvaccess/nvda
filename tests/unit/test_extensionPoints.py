# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2021 NV Access Limited, Joseph lee, Leonard de Ruijter, Łukasz Golonka

"""Unit tests for the extensionPoints module.
"""

import unittest
import extensionPoints
from functools import partial

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
	"""
	Tests to ensure that the correct parameters/**kwargs are passed through to the handler method.
	There are a few combinations of what the handler takes:
	- self for instance method handlers
	- no params
	- params with default values
	- params without default values
	- **kwargs only
	- params with default values and **kwargs
	- params without default values and **kwargs
	What is given to `callWithSupportedKwargs`:
	- keyword args that match the handler params
	- positional args that match the handler params
	- extra keyword args that the handler DOES NOT expect
	- missing args that the handler DOES expect
	"""

	def test_unboundInstanceMethodHandler_exceptionRaised(self):
		"""Test to ensure that unhandled callable types (unbound instance methods) are caught and an exception is raised.
		"""
		class handlerClass():
			def handlerMethod(self):
				pass

		unboundInstanceMethod = handlerClass.handlerMethod
		with self.assertRaises(TypeError):
			extensionPoints.callWithSupportedKwargs(unboundInstanceMethod)

	def test_instanceMethodHandlerTakesKwargs_givenKwargs(self):
		"""Test to ensure that a instance method handler gets the correct arguments, including implicit "self"
		Handler takes **kwargs.
		callWithSupportedKwargs given key word arguments.
		Handler should get all values.
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, **kwargs):
				calledKwargs.update(kwargs)

		h = handlerClass()
		extensionPoints.callWithSupportedKwargs(h.handlerMethod, a='a value', b='b value')
		self.assertEqual(calledKwargs, {'a': 'a value', 'b': 'b value'})

	def test_instanceMethodHandlerTakesParamsAndKwargs_givenKwargs(self):
		"""Test to ensure that a instance method handler gets the correct arguments, including implicit "self"
		Handler takes a parameter and **kwargs.
		callWithSupportedKwargs given key word arguments.
		Handler should get all values.
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, a, **kwargs):
				calledKwargs['a'] = a
				calledKwargs.update(kwargs)

		h = handlerClass()
		extensionPoints.callWithSupportedKwargs(h.handlerMethod, a='a value', b='b value')
		self.assertEqual(calledKwargs, {'a': 'a value', 'b': 'b value'})

	def test_instanceMethodHandlerTakesParamsAndKwargs_givenPositional(self):
		"""Test to ensure that a instanceMethod handler gets the correct arguments, including implicit "self"
		Handler takes parameter and key word arguments.
		callWithSupportedKwargs given a positional.
		Handler should get positional.
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, a, **kwargs):
				calledKwargs['a'] = a
				calledKwargs.update(kwargs)

		h = handlerClass()
		extensionPoints.callWithSupportedKwargs(h.handlerMethod, 'a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

	def test_instanceMethodHandlerTakesParams_givenPositional(self):
		"""Test to ensure that a instance method handler gets the correct arguments, including implicit "self"
		Handler takes a parameter.
		callWithSupportedKwargs given a positional.
		Handler should get positional.
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, a):
				calledKwargs['a'] = a

		h = handlerClass()
		extensionPoints.callWithSupportedKwargs(h.handlerMethod, 'a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

	def test_instanceMethodHandlerTakesParams_givenRequiredKwarg(self):
		"""Test to ensure that a instance method handler gets the correct arguments, including implicit "self"
		Handler takes a required keyword argument.
		callWithSupportedKwargs given a keyword arg with a matching name.
		Handler should get required kwarg.
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, *, a):
				calledKwargs['a'] = a

		h = handlerClass()
		extensionPoints.callWithSupportedKwargs(h.handlerMethod, a='a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

	def test_instanceMethodHandlerTakesParams_givenMatchingNameKwarg(self):
		"""Test to ensure that a instance method handler gets the correct arguments, including implicit "self"
		Handler takes a parameter.
		callWithSupportedKwargs given a keyword arg with a matching name.
		Handler should get kwarg.
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, a):
				calledKwargs['a'] = a

		h = handlerClass()
		extensionPoints.callWithSupportedKwargs(h.handlerMethod, a='a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

	def test_handlerTakesNoParams_noArgsGiven_handlerIsCalled(self):
		"""Essentially another variation of `test_handlerParamsMatchKwargsGiven_valuePassedIn` test
		The handler function expects no params.
		callWithSupportedKwargs is given no arguments.
		Expectation: handler is still called.
		"""
		called = []
		def handler():
			called.append(True)
		extensionPoints.callWithSupportedKwargs(handler)
		self.assertEqual(called, [True])

	def test_handlerTakesNoParams_kwargsGiven_handlerIsCalled(self):
		""" Tests that if the kwargs given are surplus to requirements the handler is still called. This test ensures
		that the functionality to be able to extend extension points exists. New arguments can be added without breaking
		backwards compatibility.
		The handler function expects no params.
		callWithSupportedKwargs is given some keyword args.
		Expectation: The handler is expected to be called, no args given.
		"""
		called = []
		def handler():
			called.append(True)
		extensionPoints.callWithSupportedKwargs(handler, a='a value')
		self.assertEqual(called, [True])

	def test_handlerTakesParamWithDefault_kwargsGivenMatch_valuePassedIn(self):
		""" Basic test for callWithSupportedKwargs function.
		Handler expects a single parameter, with a default provided.
		callWithSupportedKwargs is called with a single keyword argument that matches the name of the handler param.
		Expectation: handler called with parameter value equal to the keyword args given to callWithSupportedKwargs.
		"""
		gotParams = {}
		def handler(a=None):
			gotParams['a'] = a
		extensionPoints.callWithSupportedKwargs(handler, a='a value')
		self.assertEqual(gotParams, {"a": 'a value'})

	def test_handlerTakesParamWithDefault_noKwargsGiven_handlerIsCalled(self):
		""" Tests that when there are default values for the handler param, then it is truly optional.
		The handler function takes a param with a default value set.
		callWithSupportedKwargs is not given any arguments
		Expectation: the handler is expected to be called.
		"""
		gotParams = {}
		def handler(a='default a value'):
			gotParams['a'] = a
		extensionPoints.callWithSupportedKwargs(handler)
		self.assertEqual(gotParams, {'a': 'default a value'})

	def test_handlerTakesParamWithoutDefault_kwargsMatch_handlerIsCalled(self):
		""" Tests that when there are not default values for the handler param, then matching keyword arguments are given.
		The handler function takes a param with no default value set.
		callWithSupportedKwargs is given a keyword arg that match the expected param name.
		Expectation: the handler is expected to be called with the keyword argument value.
		"""
		gotParams = {}
		def handler(a):
			gotParams['a'] = a
		extensionPoints.callWithSupportedKwargs(handler, a='a value')
		self.assertEqual(gotParams, {'a': 'a value'})

	def test_handlerTakesParamsWithoutDefaults_positionalArgsGiven_handlerReceivesArgs(self):
		"""Test that positional arguments are passed untouched.
		"""
		gotParams = {}
		def handler(a, b):
			gotParams['a'] = a
			gotParams['b'] = b
		extensionPoints.callWithSupportedKwargs(handler, 'a value', 'b value')
		self.assertEqual(gotParams, {'a': 'a value', 'b': 'b value'})

	def test_handlerTakesParamWithoutDefault_kwargsDoNotMatch_exceptionRaised(self):
		""" Tests that handlers that when a handler expects params which are not provided, then the function is not called.
		The handler function takes a param with no default value set.
		callWithSupportedKwargs is given keyword arguments that don't match the expected param names.
		Expectation: an exception is raised.
		"""
		gotParams = {}
		def handler(a):
			gotParams['a'] = a
		with self.assertRaises(TypeError):
			extensionPoints.callWithSupportedKwargs(handler, b='b value')

	def test_handlerTakesTwoParamsWithoutDefaults_NotEnoughPositionalsGiven_exceptionRaised(self):
		""" Tests that handlers that when a handler expects params which are not provided, then the function is not called.
		The handler function takes a param with no default value set.
		callWithSupportedKwargs is given keyword arguments that don't match the expected param names.
		Expectation: an exception is raised.
		"""
		gotParams = {}
		def handler(a, b):
			gotParams['a'] = a
			gotParams['b'] = b
		with self.assertRaises(TypeError):
			extensionPoints.callWithSupportedKwargs(handler, "a value") # "b value" not provided

	def test_handlerTakesOnlyKwargs_kwargsGiven_handlerReceivesKwargs(self):
		gotParams = {}
		def handler(**kwargs):
			gotParams.update(kwargs)
		extensionPoints.callWithSupportedKwargs(handler, a='a value')
		self.assertEqual(gotParams, {'a': 'a value'})

	def test_handlerTakesParamsWithoutDefaultsAndKwargs_positionalArgsAndKwargsGiven_handlerReceivesArgsAndKwargs(self):
		"""Test that positional arguments are passed untouched when the function has **kwargs,
		since **kwargs is a special case early return in the code.
		"""
		gotParams = {}
		gotKwargs = {}
		def handler(a, b, **kwargs):
			gotParams['a'] = a
			gotParams['b'] = b
			gotKwargs.update(kwargs)
		extensionPoints.callWithSupportedKwargs(handler, 'a value', b='b value', c='c value')
		self.assertEqual(gotParams, {'a': 'a value', 'b': 'b value'})
		self.assertEqual(gotKwargs, {'c': 'c value'})

	def test_handlerTakesParamsWithDefaultAndKwargs_otherKwargsGiven_handlerGetsOtherKwargsAndDefaultValues(self):
		"""Test that extra keyword args is still passed in when params aren't provided.
		Handler has default values for params, and takes **kwargs.
		callWithSupportedKwargs is called only with non-matching keyword arguments.
		Expected: handler is called, non-matching keyword arguments are passed to handler
		"""
		gotParams = {}
		gotKwargs = {}

		def handler(a='a default', **kwargs):
			gotParams['a'] = a
			gotKwargs.update(kwargs)
		extensionPoints.callWithSupportedKwargs(handler, c='c value')
		self.assertEqual(gotParams, {'a': 'a default'})
		self.assertEqual(gotKwargs, {'c': 'c value'})

	def test_handlerParamsChangeOrder_KwargsGiven_correctArgValuesReceived(self):
		""" Test that the order of params for handlers does not matter if keyword arguments are used with
		`callWithSupportedKwargs`
		Note: Positionals passed to `callWithSupportedKwargs` will be position dependent, thus handlers with differing order
		may be called with incorrect argument order, it is recommended to use keyword arguments when calling
		`callWithSupportedKwargs`
		"""
		calledKwargsAB = {}
		def handlerAB(a, b):
			calledKwargsAB.update({'a': a, 'b': b})

		calledKwargsBA = {}
		def handlerBA(b, a):
			calledKwargsBA.update({'a': a, 'b': b})

		extensionPoints.callWithSupportedKwargs(handlerAB, a='a-value', b='b-value')
		extensionPoints.callWithSupportedKwargs(handlerBA, a='a-value', b='b-value')

		expected = {'a': 'a-value', 'b': 'b-value'}
		self.assertEqual(calledKwargsAB, expected)
		self.assertEqual(calledKwargsBA, expected)

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

	def test_registerUnboundInstanceMethod_raisesException(self):
		unboundInstMethod = ExampleClass.method
		with self.assertRaises(TypeError):
			self.reg.register(unboundInstMethod)

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
		self.action.notify(a='a value')

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

	def test_instanceMethodHandler(self):
		""" Test that a instance method function is called as expected
		"""
		calledKwargs = {}
		class handlerClass():
			def handlerMethod(self, **kwargs):
				calledKwargs.update(kwargs)

		h = handlerClass()
		self.action.register(h.handlerMethod)
		self.action.notify(a='a value', b='b value')
		self.assertEqual(calledKwargs, {'a': 'a value', 'b': 'b value'})

	def test_lambdaHandler(self):
		""" Test that a lambda can be used as a handler.
		Note: the lambda must be kept alive, since register uses a weak reference to it.
		"""
		calledKwargs = {}
		l = lambda a: calledKwargs.update({'a': a})
		self.action.register(l)
		self.action.notify(a='a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

	def test_partialHandler(self):
		""" Test that a L{functools.partial} can be used as a handler.
		Note: the partial must be kept alive, since register uses a weak reference to it.
		"""

		calledKwargs = {}

		def handler(a, b):
			calledKwargs['a'] = a
			calledKwargs['b'] = b

		p = partial(handler, a=1)
		self.action.register(p)
		self.action.notify(b='a value')
		self.assertEqual(calledKwargs, {'a': 1, 'b': 'a value'})

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

	def test_handlerAcceptsKwargs(self):
		""" Test that a handler that accepts **kwargs receives all arguments
		"""
		calledKwargs = {}
		def handler(**kwargs):
			calledKwargs.update(kwargs)

		self.action.register(handler)
		self.action.notify(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithoutDefault(self):
		""" Test that a handler that accepts params without a default receives arguments
		"""
		calledKwargs = {}
		def handler(a):
			calledKwargs["a"] = a

		self.action.register(handler)
		self.action.notify(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithDefault(self):
		""" Test that a handler that accepts params with a default receives arguments
		"""
		calledKwargs = {}
		def handler(a=0):
			calledKwargs["a"] = a

		self.action.register(handler)
		self.action.notify(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithRequiredKwarg(self):
		""" Test that a handler that accepts required keyword arguments receives arguments
		"""
		calledKwargs = {}
		def handler(*, a):
			calledKwargs["a"] = a

		self.action.register(handler)
		self.action.notify(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

class TestFilter(unittest.TestCase):

	def setUp(self):
		self.filter = extensionPoints.Filter()

	def test_noHandlers(self):
		# We can only test that this doesn't fail.
		self.filter.apply('value', a='a value')

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

	def test_instanceMethodHandler(self):
		""" Test that a instance method function is called as expected
		"""
		calledKwargs = {}
		class handlerClass():
			def handlerMethod(self, a):
				calledKwargs['a'] = a
				return 'instance method value'

		h = handlerClass()
		self.filter.register(h.handlerMethod)
		self.filter.apply('a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

	def test_lambdaHandler(self):
		""" Test that a lambda can be used as a handler.
		Note: the lambda must be kept alive, since register uses a weak reference to it.
		"""
		calledKwargs = {}

		def recordKwarg(a):
			calledKwargs.update({'a': a})
			return 'lambda value'

		l = lambda a: recordKwarg(a)
		self.filter.register(l)
		self.filter.apply('a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

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

	def test_handlerAcceptsKwargs(self):
		""" Test that a handler that accepts **kwargs receives all arguments
		"""
		calledKwargs = {}

		def handler(value, **kwargs):
			calledKwargs['value'] = value
			calledKwargs.update(kwargs)

		self.filter.register(handler)
		self.filter.apply("some value", a=1)
		self.assertEqual(calledKwargs, {"value": "some value", "a": 1})

	def test_handlerParamsWithoutDefault(self):
		""" Test that a handler that accepts params without a default receives arguments
		"""
		calledKwargs = {}

		def handler(value, a):
			calledKwargs['value'] = value
			calledKwargs["a"] = a

		self.filter.register(handler)
		self.filter.apply("some value", a=1)
		self.assertEqual(calledKwargs, {"value": "some value", "a": 1})

	def test_handlerParamsWithDefault(self):
		""" Test that a handler that accepts params with a default receives arguments
		"""
		calledKwargs = {}

		def handler(value, a=0):
			calledKwargs['value'] = value
			calledKwargs["a"] = a

		self.filter.register(handler)
		self.filter.apply("some value", a=1)
		self.assertEqual(calledKwargs, {"value": "some value", "a": 1})

	def test_handlerParamsWithRequiredKwarg(self):
		""" Test that a handler that accepts required keyword arguments receives arguments
		"""
		calledKwargs = {}

		def handler(value, *, a):
			calledKwargs['value'] = value
			calledKwargs["a"] = a

		self.filter.register(handler)
		self.filter.apply("some value", a=1)
		self.assertEqual(calledKwargs, {"value": "some value", "a": 1})

class TestDecider(unittest.TestCase):

	def setUp(self):
		self.decider = extensionPoints.Decider()

	def test_noHandlers(self):
		decision = self.decider.decide(a='a value')
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

	def test_instanceMethodHandler(self):
		""" Test that a instance method function is called as expected
		"""
		calledKwargs = {}
		class handlerClass():
			def handlerMethod(self, **kwargs):
				calledKwargs.update(kwargs)

		h = handlerClass()
		self.decider.register(h.handlerMethod)
		self.decider.decide(a='a value', b='b value')
		self.assertEqual(calledKwargs, {'a': 'a value', 'b': 'b value'})

	def test_lambdaHandler(self):
		""" Test that a lambda can be used as a handler.
		Note: the lambda must be kept alive, since register uses a weak reference to it.
		"""
		calledKwargs = {}
		l = lambda a: calledKwargs.update({'a': a})
		self.decider.register(l)
		self.decider.decide(a='a value')
		self.assertEqual(calledKwargs, {'a': 'a value'})

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

	def test_handlerAcceptsKwargs(self):
		""" Test that a handler that accepts **kwargs receives all arguments
		"""
		calledKwargs = {}

		def handler(**kwargs):
			calledKwargs.update(kwargs)

		self.decider.register(handler)
		self.decider.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithoutDefault(self):
		""" Test that a handler that accepts params without a default receives arguments
		"""
		calledKwargs = {}

		def handler(a):
			calledKwargs["a"] = a

		self.decider.register(handler)
		self.decider.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithDefault(self):
		""" Test that a handler that accepts params with a default receives arguments
		"""
		calledKwargs = {}

		def handler(a=0):
			calledKwargs["a"] = a

		self.decider.register(handler)
		self.decider.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithRequiredKwarg(self):
		""" Test that a handler that accepts required keyword arguments receives arguments
		"""
		calledKwargs = {}

		def handler(*, a):
			calledKwargs["a"] = a

		self.decider.register(handler)
		self.decider.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})


class TestAccumulatingDecider(unittest.TestCase):

	def test_noHandlers(self):
		positiveDecision = extensionPoints.AccumulatingDecider(defaultDecision=True).decide(a='a value')
		self.assertEqual(positiveDecision, True)
		negativeDecision = extensionPoints.AccumulatingDecider(defaultDecision=False).decide(a='a value')
		self.assertEqual(negativeDecision, False)

	def test_oneHandlerFalse(self):
		def handler():
			return False
		decider = extensionPoints.AccumulatingDecider(defaultDecision=True)
		decider.register(handler)
		decision = decider.decide()
		self.assertEqual(decision, False)

	def test_oneHandlerTrue(self):
		def handler():
			return True
		decider = extensionPoints.AccumulatingDecider(defaultDecision=False)
		decider.register(handler)
		decision = decider.decide()
		self.assertEqual(decision, True)

	def test_instanceMethodHandler(self):
		""" Test that a instance method function is called as expected
		"""
		calledKwargs = {}

		class handlerClass():
			def handlerMethod(self, **kwargs):
				calledKwargs.update(kwargs)

		h = handlerClass()
		deciderDefaultDecisionTrue = extensionPoints.AccumulatingDecider(defaultDecision=True)
		deciderDefaultDecisionTrue.register(h.handlerMethod)
		deciderDefaultDecisionTrue.decide(a='a value', b='b value')
		self.assertEqual(calledKwargs, {'a': 'a value', 'b': 'b value'})
		calledKwargs.clear()
		deciderDefaultDecisionFalse = extensionPoints.AccumulatingDecider(defaultDecision=False)
		deciderDefaultDecisionFalse.register(h.handlerMethod)
		deciderDefaultDecisionFalse.decide(a='a value', b='b value')
		self.assertEqual(calledKwargs, {'a': 'a value', 'b': 'b value'})

	def test_twoHandlersNonDefaultDefault(self):
		def handler1():
			return False

		def handler2():
			return True
		decider = extensionPoints.AccumulatingDecider(defaultDecision=True)
		decider.register(handler1)
		decider.register(handler2)
		decision = decider.decide()
		self.assertEqual(decision, False)

	def test_twoHandlersDefaultNonDefault(self):
		def handler1():
			return True

		def handler2():
			return False
		decider = extensionPoints.AccumulatingDecider(defaultDecision=True)
		decider.register(handler1)
		decider.register(handler2)
		decision = decider.decide()
		self.assertEqual(decision, False)

	def test_handlerException(self):
		"""Test that a handler which raises an exception doesn't affect later handlers.
		"""
		def handler1():
			raise Exception("barf")

		def handler2():
			return False
		decider = extensionPoints.AccumulatingDecider(defaultDecision=True)
		decider.register(handler1)
		decider.register(handler2)
		decision = decider.decide()
		self.assertEqual(decision, False)

	def test_handlerAcceptsKwargs(self):
		""" Test that a handler that accepts **kwargs receives all arguments
		"""
		calledKwargs = {}

		def handler(**kwargs):
			calledKwargs.update(kwargs)

		deciderDefaultDecisionTrue = extensionPoints.AccumulatingDecider(defaultDecision=True)
		deciderDefaultDecisionTrue.register(handler)
		deciderDefaultDecisionTrue.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})
		calledKwargs.clear()
		deciderDefaultDecisionFalse = extensionPoints.AccumulatingDecider(defaultDecision=False)
		deciderDefaultDecisionFalse.register(handler)
		deciderDefaultDecisionFalse.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithoutDefault(self):
		""" Test that a handler that accepts params without a default receives arguments
		"""
		calledKwargs = {}

		def handler(a):
			calledKwargs["a"] = a

		deciderDefaultDecisionFalse = extensionPoints.AccumulatingDecider(defaultDecision=False)
		deciderDefaultDecisionFalse.register(handler)
		deciderDefaultDecisionFalse.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})
		calledKwargs.clear()

		deciderDefaultDecisionTrue = extensionPoints.AccumulatingDecider(defaultDecision=True)
		deciderDefaultDecisionTrue.register(handler)
		deciderDefaultDecisionTrue.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithDefault(self):
		""" Test that a handler that accepts params with a default receives arguments
		"""
		calledKwargs = {}

		def handler(a=0):
			calledKwargs["a"] = a

		deciderDefaultDecisionFalse = extensionPoints.AccumulatingDecider(defaultDecision=False)
		deciderDefaultDecisionFalse.register(handler)
		deciderDefaultDecisionFalse.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

		calledKwargs.clear()
		deciderDefaultDecisionTrue = extensionPoints.AccumulatingDecider(defaultDecision=True)
		deciderDefaultDecisionTrue.register(handler)
		deciderDefaultDecisionTrue.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_handlerParamsWithRequiredKwarg(self):
		""" Test that a handler that accepts required keyword arguments receives arguments
		"""
		calledKwargs = {}

		def handler(*, a):
			calledKwargs["a"] = a

		deciderDefaultDecisionTrue = extensionPoints.AccumulatingDecider(defaultDecision=True)
		deciderDefaultDecisionTrue.register(handler)
		deciderDefaultDecisionTrue.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

		calledKwargs.clear()
		deciderDefaultDecisionFalse = extensionPoints.AccumulatingDecider(defaultDecision=False)
		deciderDefaultDecisionFalse.register(handler)
		deciderDefaultDecisionFalse.decide(a=1)
		self.assertEqual(calledKwargs, {"a": 1})

	def test_allHandlersCalledAllDecisionsDefault(self):
		"""Ensure that all handlers are called when each one returns the default decision.
		"""
		value = 0

		def h1():
			nonlocal value
			value += 3
			return False

		def h2():
			nonlocal value
			value += 11
			return False

		def h3():
			nonlocal value
			value += 22
			return False

		decider = extensionPoints.AccumulatingDecider(defaultDecision=False)
		decider.register(h1)
		decider.register(h2)
		decider.register(h3)
		decision = decider.decide()
		self.assertEqual(value, 36)
		self.assertEqual(decision, False)

	def test_allHandlersCalledAllDecisionsNonDefault(self):
		"""Ensure that all handlers are called when each one returns the non default decision.
		"""
		value = 0

		def h1():
			nonlocal value
			value += 3
			return False

		def h2():
			nonlocal value
			value += 11
			return False

		def h3():
			nonlocal value
			value += 22
			return False

		decider = extensionPoints.AccumulatingDecider(defaultDecision=True)
		decider.register(h1)
		decider.register(h2)
		decider.register(h3)
		decision = decider.decide()
		self.assertEqual(value, 36)
		self.assertEqual(decision, False)

	def test_allHandlersCalledLastDecisionNonDefault(self):
		"""Ensure that all handlers are called when all but last one returns the default decision.
		"""
		value = 0

		def h1():
			nonlocal value
			value += 3
			return False

		def h2():
			nonlocal value
			value += 11
			return False

		def h3():
			nonlocal value
			value += 22
			return True

		decider = extensionPoints.AccumulatingDecider(defaultDecision=False)
		decider.register(h1)
		decider.register(h2)
		decider.register(h3)
		decision = decider.decide()
		self.assertEqual(value, 36)
		self.assertEqual(decision, True)
