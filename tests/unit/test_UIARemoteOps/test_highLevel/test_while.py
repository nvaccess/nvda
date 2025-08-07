# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for while loops, including break and continue.
"""

from unittest import TestCase
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI


class Test_while(TestCase):
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
