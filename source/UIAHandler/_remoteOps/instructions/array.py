# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on arrays.
Including to create new arrays, append, get, set, and remove elements from arrays,
and check if an object is an array.
"""

from __future__ import annotations
from typing import cast
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
