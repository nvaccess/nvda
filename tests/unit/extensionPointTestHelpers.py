# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Helper functions to test extension points."""

from collections.abc import Callable, Generator, Iterable
from typing import Any, TypeVar
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

ExpectedOutputT = TypeVar("ExpectedOutputT", bound=Any)


def _extensionPointTester(
	testCase: unittest.TestCase,
	extensionPoint: Action | Chain | Decider | Filter,
	expectedOutput: ExpectedOutputT,
	handler: Callable[..., None],
	useAssertDictContainsSubset: bool,
	expectedKwargs: dict,
	actualKwargs: dict,
) -> Generator[ExpectedOutputT, None, None]:
	"""A helper function to test extension points.
	:param testCase: The test case to apply assertions on.
	:param extensionPoint: The extensionPoint that will be triggered by the test case.
	:param expectedOutput: The expected output as returned by the extension point handler.
	:param handler: The handler that will be registered to the extension point.
	:param useAssertDictContainsSubset: Whether to check if the actual dictionary contains all expected key-value pairs
		instead of checking for equality.
		This can be used if an extension point is notified with dictionary values that can't be predicted at test time,
		such as a driver instance.
	:param expectedKwargs: The kwargs that are expected to be passed to the extension point handler
	:param actualKwargs: The actual kwargs that were passed to the extension point handler
	"""
	extensionPoint.register(handler)
	try:
		yield expectedOutput
	finally:
		unregistered = extensionPoint.unregister(handler)
		testCase.assertTrue(unregistered)
		if useAssertDictContainsSubset:
			testCase.assertDictEqual(
				actualKwargs,
				actualKwargs | expectedKwargs,
				f"Actual dictionary {actualKwargs} does not contain all expected key-value pairs {expectedKwargs}.",
			)
		else:
			testCase.assertDictEqual(
				actualKwargs,
				expectedKwargs,
				f"Actual dictionary {actualKwargs} does not match expected dictionary {expectedKwargs}.",
			)


@contextmanager
def actionTester(
	testCase: unittest.TestCase,
	action: Action,
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
):
	"""A context manager that allows testing an Action.
	:param testCase: The test case to apply assertions on.
	:param action: The action that will be triggered by the test case.
	:param useAssertDictContainsSubset: Whether to check if the actual dictionary contains all expected key-value pairs
		instead of checking for equality.
		This can be used if an action is notified with dictionary values that can't be predicted at test time,
		such as a driver instance.
	:param expectedKwargs: The kwargs that are expected to be passed to the action
	"""
	expectedKwargs["_called"] = True
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True

	action.register(handler)
	yield from _extensionPointTester(
		testCase,
		action,
		None,  # No expected output for action
		handler,
		useAssertDictContainsSubset,
		expectedKwargs,
		actualKwargs,
	)


@contextmanager
def deciderTester(
	testCase: unittest.TestCase,
	decider: Decider,
	expectedDecision: bool,
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
):
	"""A context manager that allows testing a Decider.
	:param testCase: The test case to apply the assertion on.
	:param decider: The Decider that will be consulted by the test case.
	:param expectedDecision: The expected decision as returned by L{Decider.decide}
		it will also be yielded by the context manager.
	:param useAssertDictContainsSubset: Whether to check if the actual dictionary contains all expected key-value pairs
		instead of checking for equality.
		This can be used if a decider is consulted with dictionary values that can't be predicted at test time,
		such as a driver instance.
	:param expectedKwargs: The kwargs that are expected to be passed to the decider handler
	"""
	expectedKwargs["_called"] = True
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True
		return expectedDecision

	yield from _extensionPointTester(
		testCase,
		decider,
		expectedDecision,
		handler,
		useAssertDictContainsSubset,
		expectedKwargs,
		actualKwargs,
	)


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
	:param testCase: The test case to apply the assertion on.
	:param filter: The filter that will be applied by the test case.
	:param expectedInput: The expected input as entering the filter handler.
	:param expectedOutput: The expected output as returned by L{Filter.apply}
		it will also be yielded by the context manager
	:param useAssertDictContainsSubset: Whether to check if the actual dictionary contains all expected key-value pairs
		instead of checking for equality.
		This can be used if a filter is applied with dictionary values that can't be predicted at test time,
		such as a driver instance.
	:param expectedKwargs: The kwargs that are expected to be passed to the filter handler.
	"""
	expectedKwargs["_called"] = True
	expectedKwargs["_value"] = expectedInput
	actualKwargs = {}

	def handler(value: FilterValueT, **kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True
		actualKwargs["_value"] = value
		return expectedOutput

	yield from _extensionPointTester(
		testCase,
		filter,
		expectedOutput,
		handler,
		useAssertDictContainsSubset,
		expectedKwargs,
		actualKwargs,
	)


@contextmanager
def chainTester(
	testCase: unittest.TestCase,
	chain: Chain,
	expectedOutput: Iterable[ChainValueTypeT],
	useAssertDictContainsSubset: bool = False,
	**expectedKwargs,
):
	"""A context manager that allows testing a Filter.
	:param testCase: The test case to apply the assertion on.
	:param chain: The Chain that will be iterated by the test case.
	:param expectedOutput: The expected output as returned by L{Chain.iter}
		it will also be yielded by the context manager
	:param useAssertDictContainsSubset: Whether to check if the actual dictionary contains all expected key-value pairs
		instead of checking for equality.
		This can be used if a Chain is iterated with dictionary values that can't be predicted at test time,
		such as a driver instance.
	:param expectedKwargs: The kwargs that are expected to be passed to the Chain handler.
	"""
	expectedKwargs["_called"] = True
	actualKwargs = {}

	def handler(**kwargs):
		actualKwargs.update(kwargs)
		actualKwargs["_called"] = True
		return expectedOutput

	yield from _extensionPointTester(
		testCase,
		chain,
		expectedOutput,
		handler,
		useAssertDictContainsSubset,
		expectedKwargs,
		actualKwargs,
	)
