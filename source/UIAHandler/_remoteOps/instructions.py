# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import cast
from dataclasses import dataclass
import ctypes
from ctypes import POINTER
from comtypes import GUID
import UIAHandler
from UIAHandler import UIA
from . import lowLevel
from . import builder
from .builder import (
	InstructionBase,
)


class _TypedInstruction(InstructionBase):

	@property
	def params(self):
		return vars(self)


@dataclass
class Halt(_TypedInstruction):
	opCode = lowLevel.InstructionType.Halt


@dataclass
class Fork(_TypedInstruction):
	opCode = lowLevel.InstructionType.Fork
	jumpTo: lowLevel.RelativeOffset


@dataclass
class ForkIfFalse(_TypedInstruction):
	opCode = lowLevel.InstructionType.ForkIfFalse
	condition: builder.Operand
	branch: lowLevel.RelativeOffset


@dataclass
class NewLoopBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewLoopBlock
	breakBranch: lowLevel.RelativeOffset
	continueBranch: lowLevel.RelativeOffset


@dataclass
class EndLoopBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.EndLoopBlock


@dataclass
class NewTryBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewTryBlock
	catchBranch: lowLevel.RelativeOffset


@dataclass
class EndTryBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.EndTryBlock


@dataclass
class BreakLoop(_TypedInstruction):
	opCode = lowLevel.InstructionType.BreakLoop


@dataclass
class ContinueLoop(_TypedInstruction):
	opCode = lowLevel.InstructionType.ContinueLoop


@dataclass
class SetOperationStatus(_TypedInstruction):
	opCode = lowLevel.InstructionType.SetOperationStatus
	status: builder.Operand


@dataclass
class GetOperationStatus(_TypedInstruction):
	opCode = lowLevel.InstructionType.GetOperationStatus
	result: builder.Operand


@dataclass
class Set(_TypedInstruction):
	opCode = lowLevel.InstructionType.Set
	target: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		value = registers[self.value.operandId]
		registers[self.target.operandId] = value


@dataclass
class Compare(_TypedInstruction):
	opCode = lowLevel.InstructionType.Compare
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand
	comparisonType: lowLevel.ComparisonType

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		localLeft = registers[self.left.operandId]
		localRight = registers[self.right.operandId]
		if self.comparisonType == lowLevel.ComparisonType.Equal:
			localResult = (localLeft == localRight)
		elif self.comparisonType == lowLevel.ComparisonType.NotEqual:
			localResult = (localLeft != localRight)
		elif self.comparisonType == lowLevel.ComparisonType.LessThan:
			localResult = (localLeft < localRight)
		elif self.comparisonType == lowLevel.ComparisonType.LessThanOrEqual:
			localResult = (localLeft <= localRight)
		elif self.comparisonType == lowLevel.ComparisonType.GreaterThan:
			localResult = (localLeft > localRight)
		elif self.comparisonType == lowLevel.ComparisonType.GreaterThanOrEqual:
			localResult = (localLeft >= localRight)
		else:
			raise NotImplementedError(f"Unknown comparison type {self.comparisonType}")
		registers[self.result.operandId] = localResult


@dataclass
class Stringify(_TypedInstruction):
	opCode = lowLevel.InstructionType.Stringify
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = str(registers[self.target.operandId])


@dataclass
class NewNull(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewNull
	result: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = None


@dataclass
class IsNull(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsNull
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = (registers[self.target.operandId] is None)


@dataclass
class NewBool(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewBool
	result: builder.Operand
	value: ctypes.c_bool

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = self.value.value


@dataclass
class IsBool(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsBool
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], bool)


@dataclass
class BoolNot(_TypedInstruction):
	opCode = lowLevel.InstructionType.BoolNot
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = not registers[self.target.operandId]


@dataclass
class BoolAnd(_TypedInstruction):
	opCode = lowLevel.InstructionType.BoolAnd
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = registers[self.left.operandId] and registers[self.right.operandId]


@dataclass
class BoolOr(_TypedInstruction):
	opCode = lowLevel.InstructionType.BoolOr
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = registers[self.left.operandId] or registers[self.right.operandId]


@dataclass
class BinaryAdd(_TypedInstruction):
	opCode = lowLevel.InstructionType.BinaryAdd
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = registers[self.left.operandId] + registers[self.right.operandId]


@dataclass
class BinarySubtract(_TypedInstruction):
	opCode = lowLevel.InstructionType.BinarySubtract
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = registers[self.left.operandId] - registers[self.right.operandId]


@dataclass
class BinaryMultiply(_TypedInstruction):
	opCode = lowLevel.InstructionType.BinaryMultiply
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = registers[self.left.operandId] * registers[self.right.operandId]


@dataclass
class BinaryDivide(_TypedInstruction):
	opCode = lowLevel.InstructionType.BinaryDivide
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		left = registers[self.left.operandId]
		right = registers[self.right.operandId]
		if isinstance(left, int) and isinstance(right, int):
			result = left // right
		else:
			result = left / right
		registers[self.result.operandId] = result


@dataclass
class InplaceAdd(_TypedInstruction):
	opCode = lowLevel.InstructionType.Add
	target: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.target.operandId] += registers[self.value.operandId]


@dataclass
class InplaceSubtract(_TypedInstruction):
	opCode = lowLevel.InstructionType.Subtract
	target: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.target.operandId] -= registers[self.value.operandId]


@dataclass
class InplaceMultiply(_TypedInstruction):
	opCode = lowLevel.InstructionType.Multiply
	target: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.target.operandId] *= registers[self.value.operandId]


@dataclass
class InplaceDivide(_TypedInstruction):
	opCode = lowLevel.InstructionType.Divide
	target: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		target = registers[self.target.operandId]
		value = registers[self.value.operandId]
		if isinstance(target, int) and isinstance(value, int):
			registers[self.target.operandId] //= value
		else:
			registers[self.target.operandId] /= value


@dataclass
class NewInt(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewInt
	result: builder.Operand
	value: ctypes.c_long

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = self.value.value


@dataclass
class IsInt(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsInt
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], int)


@dataclass
class NewUint(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewUint
	result: builder.Operand
	value: ctypes.c_ulong

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = self.value.value


@dataclass
class IsUint(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsUint
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		val = registers[self.target.operandId]
		registers[self.result.operandId] = isinstance(val, int) and val >= 0


@dataclass
class NewFloat(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewDouble
	result: builder.Operand
	value: ctypes.c_double

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = self.value.value


@dataclass
class IsFloat(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsDouble
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], float)


@dataclass
class NewString(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewString
	result: builder.Operand
	length: ctypes.c_ulong
	value: ctypes.Array[ctypes.c_wchar]

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = self.value.value


@dataclass
class IsString(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsString
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], str)


@dataclass
class StringConcat(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteStringConcat
	result: builder.Operand
	left: builder.Operand
	right: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		localLeft = cast(str, registers[self.left.operandId])
		localRight = cast(str, registers[self.right.operandId])
		localResult = localLeft + localRight
		registers[self.result.operandId] = localResult


@dataclass
class NewArray(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewArray
	result: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = []


@dataclass
class IsArray(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsArray
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], list)


@dataclass
class ArrayAppend(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteArrayAppend
	target: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		array = cast(list, registers[self.target.operandId])
		array.append(registers[self.value.operandId])


@dataclass
class ArrayGetAt(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteArrayGetAt
	result: builder.Operand
	target: builder.Operand
	index: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		array = cast(list, registers[self.target.operandId])
		registers[self.result.operandId] = array[cast(int, registers[self.index.operandId])]


@dataclass
class ArrayRemoveAt(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteArrayRemoveAt
	target: builder.Operand
	index: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		array = cast(list, registers[self.target.operandId])
		del array[cast(int, registers[self.index.operandId])]


@dataclass
class ArraySetAt(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteArraySetAt
	target: builder.Operand
	index: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		array = cast(list, registers[self.target.operandId])
		array[cast(int, registers[self.index.operandId])] = registers[self.value.operandId]


@dataclass
class ArraySize(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteArraySize
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		array = cast(list, registers[self.target.operandId])
		registers[self.result.operandId] = len(array)


@dataclass
class NewGuid(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewGuid
	result: builder.Operand
	value: GUID

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = self.value


@dataclass
class IsGuid(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsGuid
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], GUID)


@dataclass
class IsExtensionSupported(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsExtensionSupported
	result: builder.Operand
	target: builder.Operand
	extensionId: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		raise NotImplementedError("Extension support is not implemented")


@dataclass
class CallExtension(_TypedInstruction):
	opCode = lowLevel.InstructionType.CallExtension
	target: builder.Operand
	extensionId: builder.Operand
	argCount: ctypes.c_ulong
	arguments: list[builder.Operand]

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		raise NotImplementedError("Extension support is not implemented")


@dataclass
class IsElement(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsElement
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(
			registers[self.target.operandId], POINTER(UIA.IUIAutomationElement)
		)


@dataclass
class ElementGetPropertyValue(_TypedInstruction):
	opCode = lowLevel.InstructionType.GetPropertyValue
	result: builder.Operand
	target: builder.Operand
	propertyId: builder.Operand
	ignoreDefault: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		element = cast(UIA.IUIAutomationElement, registers[self.target.operandId])
		propertyId = cast(int, registers[self.propertyId.operandId])
		ignoreDefault = cast(bool, registers[self.ignoreDefault.operandId])
		value = element.GetCurrentPropertyValueEx(propertyId, ignoreDefault)
		registers[self.result.operandId] = value


@dataclass
class ElementNavigate(_TypedInstruction):
	opCode = lowLevel.InstructionType.Navigate
	result: builder.Operand
	target: builder.Operand
	direction: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		element = cast(UIA.IUIAutomationElement, registers[self.target.operandId])
		if not UIAHandler.handler:
			raise RuntimeError("UIAHandler not initialized")
		client = cast(UIA.IUIAutomation, UIAHandler.handler.clientObject)
		treeWalker = client.RawViewWalker
		direction = cast(lowLevel.NavigationDirection, registers[self.direction.operandId])
		if direction == lowLevel.NavigationDirection.Parent:
			registers[self.result.operandId] = treeWalker.GetParentElement(element)
		elif direction == lowLevel.NavigationDirection.FirstChild:
			registers[self.result.operandId] = treeWalker.GetFirstChildElement(element)
		elif direction == lowLevel.NavigationDirection.LastChild:
			registers[self.result.operandId] = treeWalker.GetLastChildElement(element)
		elif direction == lowLevel.NavigationDirection.NextSibling:
			registers[self.result.operandId] = treeWalker.GetNextSiblingElement(element)
		elif direction == lowLevel.NavigationDirection.PreviousSibling:
			registers[self.result.operandId] = treeWalker.GetPreviousSiblingElement(element)
		else:
			raise ValueError(f"Unknown navigation direction {direction}")


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
