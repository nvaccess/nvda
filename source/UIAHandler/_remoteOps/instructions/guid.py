# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on GUID values.
Including to create new GUID values, and check if an object is a GUID.
"""

from __future__ import annotations
from dataclasses import dataclass
from comtypes import GUID
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


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
