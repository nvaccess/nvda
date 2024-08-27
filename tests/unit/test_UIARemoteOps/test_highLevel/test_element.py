# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""
High-level UIA remote ops Unit tests for UIA element methods.
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


class Test_element(TestCase):
	def test_getName(self):
		uiaElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement(uiaElement)
			name = element.getPropertyValue(PropertyId.Name)
			ra.Return(name)

		uiaElement.GetCurrentPropertyValueEx.return_value = "foo"
		name = op.execute()
		uiaElement.GetCurrentPropertyValueEx.assert_called_once_with(PropertyId.Name, False)
		self.assertEqual(name, "foo")
