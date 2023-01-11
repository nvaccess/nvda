# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Helper functions to test extension points."""

from extensionPoints import Action, Decider, Filter, FilterValueTypeT
import unittest
from contextlib import contextmanager
from typing import Optional


@contextmanager
def actionTester(
		testCase: unittest.TestCase,
		action: Action,
		useAssertDictContainsSubset: bool = False,
		**expectedKwargs
):
	"""A context manager that allows testing an Action.
	@param testCase: The test case to apply assertions on.
	@param action: The action that will be triggered by the test case.
	@param useAssertDictContainsSubset: Whether to use L{unittest.TestCase.assertDictContainsSubset} instead of
		L{unittest.TestCase.assertDictEqual}
		This can be used if an action is notified with dictionary values that can't be predicted at test time,
		such as a driver instance.
	@param expectedKwargs: The kwargs that are expected to be passed to the action
	"""
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)

	action.register(handler)
	try:
		yield
	finally:
		action.unregister(handler)
		testFunc = testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		testFunc(expectedKwargs, actualKwargs)


@contextmanager
def deciderTester(
		testCase: unittest.TestCase,
		decider: Decider,
		expectedDecision: bool,
		useAssertDictContainsSubset: bool = False,
		**expectedKwargs
):
	"""A context manager that allows testing a Decider.
	@param testCase: The test case to apply the assertion on.
	@param decider: The Decider that will be consulted by the test case.
	@param expectedDecision: The expected decision as returned by L{Decider.decide}
		it will also be yielded by the context manager.
	@param useAssertDictContainsSubset: Whether to use L{unittest.TestCase.assertDictContainsSubset} instead of
		L{unittest.TestCase.assertDictEqual}
		This can be used if a decider is consulted with dictionary values that can't be predicted at test time,
		such as a driver instance.
	@param expectedKwargs: The kwargs that are expected to be passed to the decider handler
	"""
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		return expectedDecision

	decider.register(handler)
	try:
		yield expectedDecision
	finally:
		decider.unregister(handler)
		testFunc = testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		testFunc(expectedKwargs, actualKwargs)


@contextmanager
def filterTester(
		testCase: unittest.TestCase,
		filter: Filter,
		expectedInput: FilterValueTypeT,
		expectedOutput: FilterValueTypeT,
		useAssertDictContainsSubset: bool = False,
		**expectedKwargs
):
	"""A function that allows testing a Filter.
	@param testCase: The test case to apply the assertion on.
	@param filter: The filter that will be applied by the test case.
	@param expectedInput: The expected input as entering the filter handler.
	@param expectedOutput: The expected output as returned by L{Filter.apply}
		it will also be yielded by the context manager
	@param useAssertDictContainsSubset: Whether to use L{unittest.TestCase.assertDictContainsSubset} instead of
		L{unittest.TestCase.assertDictEqual}
		This can be used if a filter is applied with dictionary values that can't be predicted at test time,
		such as a driver instance.
	@param expectedKwargs: The kwargs that are expected to be passed to the filter handler.
	"""
	actualKwargs = {}

	class InputValueContainer:
		"""A class to propagate the input value entering the handler to the filterTester"""
		value: Optional[FilterValueTypeT] = None

	container = InputValueContainer()

	def handler(inputVal: FilterValueTypeT, **kwargs):
		container.value = inputVal
		actualKwargs.update(kwargs)
		return expectedOutput

	filter.register(handler)
	try:
		yield expectedOutput
	finally:
		filter.unregister(handler)
		testCase.assertEqual(expectedInput, container.value)
		testFunc = testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		testFunc(expectedKwargs, actualKwargs)
