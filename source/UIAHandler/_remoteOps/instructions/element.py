# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This module contains the instructions that operate on UI Automation elements.
Including to check if an object is an element,
get a property value of an element,
and navigate the UI Automation tree.
"""


from __future__ import annotations
from typing import cast
from dataclasses import dataclass
from ctypes import POINTER
import UIAHandler
from UIAHandler import UIA
from .. import lowLevel
from .. import builder
from ._base import _TypedInstruction


@dataclass
class IsElement(_TypedInstruction):
	opCode = lowLevel.InstructionType.IsElement
	result: builder.Operand
	target: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		registers[self.result.operandId] = isinstance(
			registers[self.target.operandId], POINTER(UIA.IUIAutomationElement)
		)


@dataclass
class ElementGetPropertyValue(_TypedInstruction):
	opCode = lowLevel.InstructionType.GetPropertyValue
	result: builder.Operand
	target: builder.Operand
	propertyId: builder.Operand
	ignoreDefault: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		element = cast(UIA.IUIAutomationElement, registers[self.target.operandId])
		propertyId = cast(int, registers[self.propertyId.operandId])
		ignoreDefault = cast(bool, registers[self.ignoreDefault.operandId])
		value = element.GetCurrentPropertyValueEx(propertyId, ignoreDefault)
		registers[self.result.operandId] = value


@dataclass
class ElementNavigate(_TypedInstruction):
	opCode = lowLevel.InstructionType.Navigate
	result: builder.Operand
	target: builder.Operand
	direction: builder.Operand

	def localExecute(self, registers: dict[lowLevel.OperandId, object]):
		element = cast(UIA.IUIAutomationElement, registers[self.target.operandId])
		if not UIAHandler.handler:
			raise RuntimeError("UIAHandler not initialized")
		client = cast(UIA.IUIAutomation, UIAHandler.handler.clientObject)
		treeWalker = client.RawViewWalker
		direction = cast(lowLevel.NavigationDirection, registers[self.direction.operandId])
		match direction:
			case lowLevel.NavigationDirection.Parent:
				registers[self.result.operandId] = treeWalker.GetParentElement(element)
			case lowLevel.NavigationDirection.FirstChild:
				registers[self.result.operandId] = treeWalker.GetFirstChildElement(element)
			case lowLevel.NavigationDirection.LastChild:
				registers[self.result.operandId] = treeWalker.GetLastChildElement(element)
			case lowLevel.NavigationDirection.NextSibling:
				registers[self.result.operandId] = treeWalker.GetNextSiblingElement(element)
			case lowLevel.NavigationDirection.PreviousSibling:
				registers[self.result.operandId] = treeWalker.GetPreviousSiblingElement(element)
			case _:
				raise ValueError(f"Unknown navigation direction {direction}")
