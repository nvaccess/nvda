# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
This module contains the instructions that operate on UIA cache requests.
Including to create a cache request, add properties and patterns to it,
and populate the cache of a UI Automation element from it.
"""

from __future__ import annotations
from typing import cast
from dataclasses import dataclass
from ctypes import POINTER
import UIAHandler
from UIAHandler import UIA
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


@dataclass
class NewCacheRequest(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewCacheRequest
	result: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		if not UIAHandler.handler:
			raise RuntimeError("UIAHandler not initialized")
		client = cast(UIA.IUIAutomation, UIAHandler.handler.clientObject)
		registers[self.result.operandId] = client.CreateCacheRequest()


@dataclass
class IsCacheRequest(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsCacheRequest
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(
			registers[self.target.operandId],
			POINTER(UIA.IUIAutomationCacheRequest),
		)


@dataclass
class CacheRequestAddProperty(_TypedInstruction):
	opCode = lowLevel.InstructionType.CacheRequestAddProperty
	target: builder.Operand
	propertyId: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		cacheRequest = cast(UIA.IUIAutomationCacheRequest, registers[self.target.operandId])
		propertyId = cast(int, registers[self.propertyId.operandId])
		cacheRequest.AddProperty(propertyId)


@dataclass
class CacheRequestAddPattern(_TypedInstruction):
	opCode = lowLevel.InstructionType.CacheRequestAddPattern
	target: builder.Operand
	patternId: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		cacheRequest = cast(UIA.IUIAutomationCacheRequest, registers[self.target.operandId])
		patternId = cast(int, registers[self.patternId.operandId])
		cacheRequest.AddPattern(patternId)


@dataclass
class PopulateCache(_TypedInstruction):
	opCode = lowLevel.InstructionType.PopulateCache
	target: builder.Operand
	cacheRequest: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		element = cast(UIA.IUIAutomationElement, registers[self.target.operandId])
		cacheRequest = cast(UIA.IUIAutomationCacheRequest, registers[self.cacheRequest.operandId])
		registers[self.target.operandId] = element.BuildUpdatedCache(cacheRequest)
