# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Helper functions to test extension points."""

from extensionPoints import (
	Action,
	Chain,
	ChainValueTypeT,
	Decider,
	Filter,
	FilterValueT,
)
import unittest
from contextlib import contextmanager
from typing import Iterable


@contextmanager
def actionTester(
	testCase: unittest.TestCase,
	action: Action,
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
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
	expectedKwargs["_called"] = True
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True

	action.register(handler)
	try:
		yield
	finally:
		action.unregister(handler)
		testFunc = (
			testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		)
		testFunc(expectedKwargs, actualKwargs)


@contextmanager
def deciderTester(
	testCase: unittest.TestCase,
	decider: Decider,
	expectedDecision: bool,
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
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
	expectedKwargs["_called"] = True
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True
		return expectedDecision

	decider.register(handler)
	try:
		yield expectedDecision
	finally:
		decider.unregister(handler)
		testFunc = (
			testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		)
		testFunc(expectedKwargs, actualKwargs)


@contextmanager
def filterTester(
	testCase: unittest.TestCase,
	filter: Filter,
	expectedInput: FilterValueT,
	expectedOutput: FilterValueT,
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
):
	"""A context manager that allows testing a Filter.
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
	expectedKwargs["_called"] = True
	expectedKwargs["_value"] = expectedInput
	actualKwargs = {}

	def handler(value: FilterValueT, **kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True
		actualKwargs["_value"] = value
		return expectedOutput

	filter.register(handler)
	try:
		yield expectedOutput
	finally:
		filter.unregister(handler)
		testFunc = (
			testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		)
		testFunc(expectedKwargs, actualKwargs)


@contextmanager
def chainTester(
	testCase: unittest.TestCase,
	chain: Chain,
	expectedOutput: Iterable[ChainValueTypeT],
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
):
	"""A context manager that allows testing a Filter.
	@param testCase: The test case to apply the assertion on.
	@param chain: The Chain that will be iterated by the test case.
	@param expectedOutput: The expected output as returned by L{Chain.iter}
		it will also be yielded by the context manager
	@param useAssertDictContainsSubset: Whether to use L{unittest.TestCase.assertDictContainsSubset} instead of
		L{unittest.TestCase.assertDictEqual}
		This can be used if a Chain is iterated with dictionary values that can't be predicted at test time,
		such as a driver instance.
	@param expectedKwargs: The kwargs that are expected to be passed to the Chain handler.
	"""
	expectedKwargs["_called"] = True
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True
		return expectedOutput

	chain.register(handler)
	try:
		yield expectedOutput
	finally:
		chain.unregister(handler)
		testFunc = (
			testCase.assertDictContainsSubset if useAssertDictContainsSubset else testCase.assertDictEqual
		)
		testFunc(expectedKwargs, actualKwargs)
