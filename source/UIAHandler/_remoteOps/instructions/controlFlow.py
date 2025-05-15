# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that control the flow of execution.
Including to halt execution, fork execution, and manage loops and try blocks.
"""

from __future__ import annotations
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


@dataclass
class Halt(_TypedInstruction):
	opCode = lowLevel.InstructionType.Halt


@dataclass
class Fork(_TypedInstruction):
	opCode = lowLevel.InstructionType.Fork
	jumpTo: lowLevel.RelativeOffset


@dataclass
class ForkIfFalse(_TypedInstruction):
	opCode = lowLevel.InstructionType.ForkIfFalse
	condition: builder.Operand
	branch: lowLevel.RelativeOffset


@dataclass
class NewLoopBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewLoopBlock
	breakBranch: lowLevel.RelativeOffset
	continueBranch: lowLevel.RelativeOffset


@dataclass
class EndLoopBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.EndLoopBlock


@dataclass
class NewTryBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewTryBlock
	catchBranch: lowLevel.RelativeOffset


@dataclass
class EndTryBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.EndTryBlock


@dataclass
class BreakLoop(_TypedInstruction):
	opCode = lowLevel.InstructionType.BreakLoop


@dataclass
class ContinueLoop(_TypedInstruction):
	opCode = lowLevel.InstructionType.ContinueLoop


class JumpElse(Fork):
	"""
	A specialized Fork instruction used specifically to jump over the else branch of an if statement.
	The bytecode for this instruction is the same as Fork, but it is used to indicate that an else branch can be inserted here.
	It also tracks the previous JumpElse instruction, so that they can all be incremented together, in the case of an if elif elif else chain.
	"""
	_prevJumpElse: Fork | None = None


class JumpCatch(Fork):
	"""
	A specialized Fork instruction used specifically to jump over the catch branch of a try statement.
	The bytecode for this instruction is the same as Fork, but it is used to indicate that a catch branch can be inserted here.
	"""
