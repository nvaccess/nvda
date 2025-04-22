# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on string maps (dictionaries).
Including to create new string mapss, inserting elements, looking up elements, checking for a key, and querying the size of the map.
"""

from __future__ import annotations
from typing import cast, Any
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction

@dataclass
class NewStringMap(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewStringMap
	result: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = {}


@dataclass
class IsStringmap(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsStringMap
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(registers[self.target.operandId], str)


@dataclass
class StringMapInsert(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteStringMapInsert
	target: builder.Operand
	key: builder.Operand
	value: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		stringMap = cast(dict[str,Any], registers[self.target.operandId])
		key = cast(str, registers[self.key.operandId])
		value = registers[self.value.operandId]
		stringMap[key] = value


@dataclass
class StringMapLookup(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteStringMapLookup
	result: builder.Operand
	target: builder.Operand
	key: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		stringMap = cast(dict[str,Any], registers[self.target.operandId])
		key = cast(str, registers[self.key.operandId])
		registers[self.result.operandId] = stringMap[key]


@dataclass
class StringMapHasKey(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteStringMapHasKey
	result: builder.Operand
	target: builder.Operand
	key: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		stringMap = cast(dict[str,Any], registers[self.target.operandId])
		key = cast(str, registers[self.key.operandId])
		registers[self.result.operandId] = key in stringMap

@dataclass
class StringMapRemove(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteStringMapRemove
	target: builder.Operand
	key: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		StringMap = cast(dict[str,Any], registers[self.target.operandId])
		key = cast(str, registers[self.key.operandId])
		del StringMap[key]


@dataclass
class StringMapSize(_TypedInstruction):
	opCode = lowLevel.InstructionType.RemoteStringMapSize
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		StringMap = cast(dict[str,Any], registers[self.target.operandId])
		registers[self.result.operandId] = len(StringMap)
