# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on boolean values.
Including to create new boolean values, check if an object is a boolean,
and perform boolean operations such as and, or and not.
"""

from __future__ import annotations
from dataclasses import dataclass
import ctypes
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
