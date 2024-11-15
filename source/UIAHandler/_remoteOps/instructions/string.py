# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on strings.
Including to create new strings, check if an object is a string, and concatenate strings.
"""

from __future__ import annotations
from typing import cast
from dataclasses import dataclass
import ctypes
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
class Stringify(_TypedInstruction):
	opCode = lowLevel.InstructionType.Stringify
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = str(registers[self.target.operandId])
