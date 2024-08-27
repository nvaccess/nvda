# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that perform arithmetic operations,
such as addition, subtraction, multiplication, and division.
Both binary and in-place operations are supported.
"""

from __future__ import annotations
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
