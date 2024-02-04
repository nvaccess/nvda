# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


from __future__ import annotations
from dataclasses import dataclass
from . import lowLevel
from .builder import (
	InstructionBase,
)
from . import remoteAPI


class _TypedInstruction(InstructionBase):

	@property
	def params(self):
		return vars(self)


@dataclass
class Instruction_Fork(_TypedInstruction):
	opCode = lowLevel.InstructionType.Fork
	jumpTo: lowLevel.RelativeOffset


@dataclass
class Instruction_ForkIfFalse(_TypedInstruction):
	opCode = lowLevel.InstructionType.ForkIfFalse
	condition: remoteAPI.RemoteBool
	branch: lowLevel.RelativeOffset


@dataclass
class Instruction_NewLoopBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewLoopBlock
	breakBranch: lowLevel.RelativeOffset
	continueBranch: lowLevel.RelativeOffset


@dataclass
class Instruction_NewTryBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewTryBlock
	catchBranch: lowLevel.RelativeOffset
