# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

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


class Test_isNull(TestCase):
	def test_isNull_trueForNullElement(self):
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement()
			ra.Return(element.isNull())

		self.assertTrue(op.execute())

	def test_isNull_falseForImportedElement(self):
		uiaElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement(uiaElement)
			ra.Return(element.isNull())

		self.assertFalse(op.execute())
