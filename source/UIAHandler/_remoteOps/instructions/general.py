# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on all object types.
Including to set a value, or compare two values.
"""


from __future__ import annotations
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
		match self.comparisonType:
			case lowLevel.ComparisonType.Equal:
				localResult = (localLeft == localRight)
			case lowLevel.ComparisonType.NotEqual:
				localResult = (localLeft != localRight)
			case lowLevel.ComparisonType.LessThan:
				localResult = (localLeft < localRight)
			case lowLevel.ComparisonType.LessThanOrEqual:
				localResult = (localLeft <= localRight)
			case lowLevel.ComparisonType.GreaterThan:
				localResult = (localLeft > localRight)
			case lowLevel.ComparisonType.GreaterThanOrEqual:
				localResult = (localLeft >= localRight)
			case _:
				raise NotImplementedError(f"Unknown comparison type {self.comparisonType}")
		registers[self.result.operandId] = localResult
