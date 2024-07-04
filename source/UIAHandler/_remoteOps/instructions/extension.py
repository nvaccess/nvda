# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that check for and call UI Automation custom extensions.
"""

from __future__ import annotations
from dataclasses import dataclass
import ctypes
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


@dataclass
class IsExtensionSupported(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsExtensionSupported
	result: builder.Operand
	target: builder.Operand
	extensionId: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		raise NotImplementedError("Extension support is not implemented")


@dataclass
class CallExtension(_TypedInstruction):
	opCode = lowLevel.InstructionType.CallExtension
	target: builder.Operand
	extensionId: builder.Operand
	argCount: ctypes.c_ulong
	arguments: list[builder.Operand]

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		raise NotImplementedError("Extension support is not implemented")
