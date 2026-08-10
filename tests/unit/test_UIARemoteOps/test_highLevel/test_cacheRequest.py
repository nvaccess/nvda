# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
High-level UIA remote ops unit tests for cache request support.
"""

import struct
from unittest import TestCase
from unittest.mock import Mock, patch
from ctypes import POINTER
import UIAHandler
from UIAHandler import UIA
from UIAHandler._remoteOps import builder
from UIAHandler._remoteOps import instructions
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps import remoteAPI
from UIAHandler._remoteOps.lowLevel import (
	PatternId,
	PropertyId,
)


class Test_cacheRequest(TestCase):
	def test_populateCache_buildsAndAppliesClientCacheRequest(self):
		uiaElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		cachedElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		clientCacheRequest = Mock(spec=POINTER(UIA.IUIAutomationCacheRequest))
		handlerMock = Mock()
		handlerMock.clientObject.CreateCacheRequest.return_value = clientCacheRequest
		uiaElement.BuildUpdatedCache.return_value = cachedElement
		cachedElement.GetCurrentPropertyValueEx.return_value = "cached name"
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement(uiaElement)
			cacheRequest = ra.newCacheRequest()
			cacheRequest.addProperty(PropertyId.Name)
			cacheRequest.addPattern(PatternId.Text)
			element.populateCache(cacheRequest)
			ra.Return(element.getPropertyValue(PropertyId.Name))

		with patch.object(UIAHandler, "handler", handlerMock):
			name = op.execute()

		handlerMock.clientObject.CreateCacheRequest.assert_called_once_with()
		clientCacheRequest.AddProperty.assert_called_once_with(PropertyId.Name)
		clientCacheRequest.AddPattern.assert_called_once_with(PatternId.Text)
		uiaElement.BuildUpdatedCache.assert_called_once_with(clientCacheRequest)
		cachedElement.GetCurrentPropertyValueEx.assert_called_once_with(PropertyId.Name, False)
		uiaElement.GetCurrentPropertyValueEx.assert_not_called()
		self.assertEqual(name, "cached name")


class Test_isNotSupported(TestCase):
	def test_trueForReservedValue(self):
		uiaElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		reservedValue = object()
		handlerMock = Mock()
		handlerMock.reservedNotSupportedValue = reservedValue
		uiaElement.GetCurrentPropertyValueEx.return_value = reservedValue
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement(uiaElement)
			value = element.getPropertyValue(PropertyId.RangeValueValue, True)
			ra.Return(value.isNotSupported())

		with patch.object(UIAHandler, "handler", handlerMock):
			self.assertTrue(op.execute())

	def test_falseForSupportedValue(self):
		uiaElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		handlerMock = Mock()
		handlerMock.reservedNotSupportedValue = object()
		uiaElement.GetCurrentPropertyValueEx.return_value = 42.0
		op = operation.Operation(localMode=True)

		@op.buildFunction
		def code(ra: remoteAPI.RemoteAPI):
			element = ra.newElement(uiaElement)
			value = element.getPropertyValue(PropertyId.RangeValueValue, True)
			ra.Return(value.isNotSupported())

		with patch.object(UIAHandler, "handler", handlerMock):
			self.assertFalse(op.execute())


class Test_instructionByteCode(TestCase):
	def test_byteCode_layout(self):
		"""The wire encoding of the cache request instructions:
		a 32 bit little endian opcode followed by 32 bit little endian operand IDs,
		in the operand order of the Microsoft remote operations instruction set.
		"""
		cases = (
			(instructions.NewCacheRequest, 0x4C, 1),
			(instructions.IsCacheRequest, 0x4D, 2),
			(instructions.CacheRequestAddProperty, 0x4E, 2),
			(instructions.CacheRequestAddPattern, 0x4F, 2),
			(instructions.PopulateCache, 0x50, 2),
			(instructions.IsNotSupported, 0x3B, 2),
		)
		rob = builder.RemoteOperationBuilder()
		for instructionClass, opCode, operandCount in cases:
			with self.subTest(instruction=instructionClass.__name__):
				operands = [builder.Operand(rob, rob.requestNewOperandId()) for _ in range(operandCount)]
				instruction = instructionClass(*operands)
				expected = struct.pack("<l", opCode)
				for operand in operands:
					expected += struct.pack("<L", operand.operandId.value)
				self.assertEqual(instruction.getByteCode(), expected)
