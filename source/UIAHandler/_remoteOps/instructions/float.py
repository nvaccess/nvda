# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on floating point numbers.
Including to create new floating point numbers, and check if an object is a floating point number.
"""


from __future__ import annotations
from dataclasses import dataclass
import ctypes
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
