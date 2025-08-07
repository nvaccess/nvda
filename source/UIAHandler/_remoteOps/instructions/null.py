# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on null values.
Including to create new null values, and check if an object is null.
"""

from __future__ import annotations
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
		registers[self.result.operandId] = registers[self.target.operandId] is None
