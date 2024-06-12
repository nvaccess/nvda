# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on the status of operations.
"""


from __future__ import annotations
from dataclasses import dataclass
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


@dataclass
class SetOperationStatus(_TypedInstruction):
	opCode = lowLevel.InstructionType.SetOperationStatus
	status: builder.Operand


@dataclass
class GetOperationStatus(_TypedInstruction):
	opCode = lowLevel.InstructionType.GetOperationStatus
	result: builder.Operand
