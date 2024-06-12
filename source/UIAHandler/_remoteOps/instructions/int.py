# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on integers.
Including to create new integers, and check if an object is an integer.
Both signed and unsigned integers are supported.
"""


from __future__ import annotations
from dataclasses import dataclass
import ctypes
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
