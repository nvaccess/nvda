# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Helper functions to test extension points."""

from extensionPoints import Action, Decider, Filter, FilterValueTypeT
import unittest
from contextlib import contextmanager
from typing import Callable, Optional


@contextmanager
def actionTester(
	testCase: unittest.TestCase,
	action: Action,
	**expectedKwargs
):
	"""A context manager that allows testing an Action.
	@param testCase: The test case to apply assertions on.
	@param action: The action that will be triggered by the test case.
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
		testCase.assertDictEqual(expectedKwargs, actualKwargs)


def deciderTester(
	testCase: unittest.TestCase,
	decider: Decider,
	expectedDecision: bool,
	actualDecisionGetter: Callable[[], bool],
):
	"""A function that allows testing a Decider.
	@param testCase: The test case to apply the assertion on.
	@param decider: The Decider that will be consulted by the test case.
	@param expectedDecision: The expected decision as returned by L{Decider.decide}
	@param actualDecisionGetter: A callable that returns the actual decision
	"""
	def handler(**kwargs):
		return expectedDecision

	decider.register(handler)
	try:
		testCase.assertEqual(expectedDecision, actualDecisionGetter())
	finally:
		decider.unregister(handler)


def filterTester(
	testCase: unittest.TestCase,
	filter: Filter,
	expectedInput: FilterValueTypeT,
	expectedOutput: FilterValueTypeT,
	actualOutputGetter: Callable[[], FilterValueTypeT],
):
	"""A function that allows testing a Filter.
	@param testCase: The test case to apply the assertion on.
	@param filter: The filter that will be applied by the test case.
	@param expectedInput: The expected input as entering the filter handler.
	@param expectedOutput: The expected output as returned by L{Filter.apply}
	@param actualOutputGetter: A callable that returns the actual output
	"""

	class InputValueContainer:
		"""A class to propagate the input value entering the handler to the filterTester"""
		value: Optional[FilterValueTypeT] = None

	container = InputValueContainer()

	def handler(inputVal: FilterValueTypeT):
		container.value = inputVal
		return expectedOutput

	filter.register(handler)
	testCase.assertEqual(expectedOutput, actualOutputGetter())
	testCase.assertEqual(expectedInput, container.value)
	filter.unregister(handler)
