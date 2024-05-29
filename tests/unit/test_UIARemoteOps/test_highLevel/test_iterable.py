# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for writing iterable functions that can yield values.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_iterable(TestCase):

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
		"""
		Tests that a long operation is automatically re-executed multiple times
		until it is successfully run without exceeding the instruction limit.
		Using a static variable which is not reset between executions,
		and then incremented once each execution,
		we can track how many times the operation was executed.
		The operation itself involves incrementing a counter variable 'i'
		within a while loop until it reaches 5000,
		yielding i and the execution count on every loop.
		This is expected to take 5 executions to fully complete.
		"""
		op = operation.Operation(localMode=True)

		@op.buildIterableFunction
		def code(ra: remoteAPI.RemoteAPI):
			executionCount = ra.newInt(0, static=True)
			executionCount += 1
			i = ra.newInt(0, static=True)
			with ra.whileBlock(lambda: i < 5000):
				i += 1
				ra.Yield(i, executionCount)

		results = []
		for i, executionCount in op.iterExecute(maxTries=20):
			results.append((i, executionCount))
		self.assertEqual(len(results), 5000)
		last_i, last_executionCount = results[-1]
		self.assertEqual(last_i, 5000)
		self.assertEqual(last_executionCount, 5)

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
		"""
		Tests that a long operation is automatically re-executed multiple times
		until it is successfully run without exceeding the instruction limit.
		Using a static variable which is not reset between executions,
		and then incremented once each execution,
		we can track how many times the operation was executed.
		"""
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
