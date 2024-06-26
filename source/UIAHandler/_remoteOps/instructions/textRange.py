# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on UI Automation text ranges.
"""


from __future__ import annotations
from typing import cast
from dataclasses import dataclass
from UIAHandler import UIA
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


@dataclass
class TextRangeGetText(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeGetText
	result: builder.Operand
	target: builder.Operand
	maxLength: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		maxLength = cast(int, registers[self.maxLength.operandId])
		registers[self.result.operandId] = textRange.GetText(maxLength)


@dataclass
class TextRangeMove(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeMove
	result: builder.Operand
	target: builder.Operand
	unit: builder.Operand
	count: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		unit = cast(int, registers[self.unit.operandId])
		count = cast(int, registers[self.count.operandId])
		registers[self.result.operandId] = textRange.Move(unit, count)


@dataclass
class TextRangeMoveEndpointByUnit(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeMoveEndpointByUnit
	result: builder.Operand
	target: builder.Operand
	endpoint: builder.Operand
	unit: builder.Operand
	count: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		endPoint = cast(int, registers[self.endpoint.operandId])
		unit = cast(int, registers[self.unit.operandId])
		count = cast(int, registers[self.count.operandId])
		registers[self.result.operandId] = textRange.MoveEndpointByUnit(endPoint, unit, count)


@dataclass
class TextRangeCompare(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeCompare
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		left = cast(UIA.IUIAutomationTextRange, registers[self.left.operandId])
		right = cast(UIA.IUIAutomationTextRange, registers[self.right.operandId])
		registers[self.result.operandId] = left.Compare(right)


@dataclass
class TextRangeClone(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeClone
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		registers[self.result.operandId] = textRange.Clone()


@dataclass
class TextRangeFindAttribute(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeFindAttribute
	result: builder.Operand
	target: builder.Operand
	attributeId: builder.Operand
	value: builder.Operand
	reverse: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		attributeId = cast(int, registers[self.attributeId.operandId])
		value = cast(object, registers[self.value.operandId])
		reverse = cast(bool, registers[self.reverse.operandId])
		registers[self.result.operandId] = textRange.FindAttribute(attributeId, value, reverse)


@dataclass
class TextRangeFindText(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeFindText
	result: builder.Operand
	target: builder.Operand
	value: builder.Operand
	reverse: builder.Operand
	ignoreCase: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		value = cast(str, registers[self.value.operandId])
		reverse = cast(bool, registers[self.reverse.operandId])
		ignoreCase = cast(bool, registers[self.ignoreCase.operandId])
		registers[self.result.operandId] = textRange.FindText(value, reverse, ignoreCase)


@dataclass
class TextRangeGetAttributeValue(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeGetAttributeValue
	result: builder.Operand
	target: builder.Operand
	attributeId: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		attributeId = cast(int, registers[self.attributeId.operandId])
		registers[self.result.operandId] = textRange.GetAttributeValue(attributeId)


@dataclass
class TextRangeGetBoundingRectangles(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeGetBoundingRectangles
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		registers[self.result.operandId] = textRange.GetBoundingRectangles()


@dataclass
class TextRangeGetEnclosingElement(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeGetEnclosingElement
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		registers[self.result.operandId] = textRange.GetEnclosingElement()


@dataclass
class TextRangeExpandToEnclosingUnit(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeExpandToEnclosingUnit
	target: builder.Operand
	unit: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		unit = cast(int, registers[self.unit.operandId])
		textRange.ExpandToEnclosingUnit(unit)


@dataclass
class TextRangeMoveEndpointByRange(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeMoveEndpointByRange
	target: builder.Operand
	srcEndpoint: builder.Operand
	otherRange: builder.Operand
	otherEndpoint: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		srcEndpoint = cast(int, registers[self.srcEndpoint.operandId])
		otherRange = cast(UIA.IUIAutomationTextRange, registers[self.otherRange.operandId])
		otherEndpoint = cast(int, registers[self.otherEndpoint.operandId])
		textRange.MoveEndpointByRange(srcEndpoint, otherRange, otherEndpoint)


@dataclass
class TextRangeCompareEndpoints(_TypedInstruction):
	opCode = lowLevel.InstructionType.TextRangeCompareEndpoints
	result: builder.Operand
	target: builder.Operand
	thisEndpoint: builder.Operand
	otherRange: builder.Operand
	otherEndpoint: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		textRange = cast(UIA.IUIAutomationTextRange, registers[self.target.operandId])
		thisEndpoint = cast(int, registers[self.thisEndpoint.operandId])
		otherRange = cast(UIA.IUIAutomationTextRange, registers[self.otherRange.operandId])
		otherEndpoint = cast(int, registers[self.otherEndpoint.operandId])
		registers[self.result.operandId] = textRange.CompareEndpoints(thisEndpoint, otherRange, otherEndpoint)
