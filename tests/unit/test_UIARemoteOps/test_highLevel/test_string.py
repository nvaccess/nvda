# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited

"""
High-level UIA remote ops Unit tests for strings.
"""

from unittest import TestCase
from unittest.mock import Mock
from ctypes import POINTER
from UIAHandler import UIA
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI
from UIAHandler._remoteOps.lowLevel import (
	PropertyId,
)


class Test_string(TestCase):

	def test_string_concat(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			s = ra.newString("hello")
			t = ra.newString(" world")
			u = (s + t)
			ra.Return(u)

		u = op.execute()
		self.assertEqual(u, "hello world")
