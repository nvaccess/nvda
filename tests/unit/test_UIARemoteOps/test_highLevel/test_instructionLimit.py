# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for reaching and handling the remote ops instruction limit.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_instructionLimit(TestCase):

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
