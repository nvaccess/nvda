# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from abc import ABCMeta, abstractproperty
from typing import (
	Self,
	ClassVar,
	Any,
	Iterable
)
import ctypes
from ctypes import (
	_SimpleCData,
	c_char,
	c_long,
	c_wchar
)
import enum
from dataclasses import dataclass
import weakref
import struct
import itertools
import contextlib
from . import lowLevel
from .lowLevel import OperandId


class _RemoteBase:

	_robRef: weakref.ReferenceType[RemoteOperationBuilder] | None = None
	_mutable: bool = True

	@property
	def rob(self) -> RemoteOperationBuilder:
		if self._robRef is None:
			raise RuntimeError("Object not bound yet")
		rob = self._robRef()
		if rob is None:
			raise RuntimeError("Builder has died")
		return rob

	def __init__(self, rob: RemoteOperationBuilder):
		self._robRef = weakref.ref(rob)

	def isBound(self, toBuilder: RemoteOperationBuilder) -> bool:
		if self._robRef is None:
			return False
		rob = self._robRef()
		if rob is None:
			raise RuntimeError("Builder has died")
		if rob is not toBuilder:
			raise RuntimeError("Builder mismatch")
		return True

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, type(self)):
			return False
		rob = self._robRef() if self._robRef is not None else None
		otherBuilder = other._robRef() if other._robRef is not None else None
		if rob != otherBuilder:
			return False
		if self._mutable != other._mutable:
			return False
		return True


class Operand(_RemoteBase):

	_operandId: OperandId | None = None
	_sectionForInitInstructions: str | None = None
	_defaultSectionForInitInstructions: str = "main"

	def __init__(self, rob: RemoteOperationBuilder, operandId: OperandId):
		super().__init__(rob)
		self._operandId = operandId

	@property
	def operandId(self) -> OperandId:
		if self._operandId is None:
			raise RuntimeError("Object not bound yet")
		return self._operandId

	@property
	def sectionForInitInstructions(self) -> str:
		return self._sectionForInitInstructions or self._defaultSectionForInitInstructions

	def __eq__(self, other: Self | object) -> bool:
		if super().__eq__(other) is False:
			return False
		if type(other) is not Operand:
			return False
		if self._operandId != other._operandId:
			return False
		return True

	def __repr__(self) -> str:
		output = ""
		if self._sectionForInitInstructions == "static":
			output += "static "
		if not self._mutable:
			output += "const "
		output += f"{self.__class__.__name__} at {self.operandId}"
		return output


class InstructionBase(metaclass=ABCMeta):
	opCode: ClassVar[lowLevel.InstructionType]

	@abstractproperty
	def params(self) -> dict[str, Any]:
		raise NotImplementedError()

	def getByteCode(self) -> bytes:
		byteCode = struct.pack('l', self.opCode.value)
		params = list(self.params.values())
		if len(params) > 0 and isinstance(params[-1], list):
			# If the last parameter is a list, it is a variable length parameter.
			params[-1:] = params[-1]
		for param in params:
			if isinstance(param, enum.IntEnum):
				param = c_long(param.value)
			elif isinstance(param, Operand):
				param = param.operandId
			paramBytes = (c_char * ctypes.sizeof(param)).from_address(ctypes.addressof(param)).raw
			byteCode += paramBytes
		return byteCode

	def dumpInstruction(self) -> str:
		output = f"{self.opCode.name}"
		paramOutputList = []
		for paramName, param in self.params.items():
			paramOutput = f"{paramName}="
			if isinstance(param, ctypes.Array) and param._type_ == c_wchar:
				paramOutput += f"c_wchar_array({repr(param.value)})"
			else:
				paramOutput += f"{repr(param)}"
			paramOutputList.append(paramOutput)
		output += "(" + ", ".join(paramOutputList) + ")"
		return output

	def localExecute(self, registers: dict[OperandId, object]):
		raise NotImplementedError()


@dataclass
class GenericInstruction(InstructionBase):
	opCode: lowLevel.InstructionType
	_params: dict[str, Operand | _SimpleCData | ctypes.Array | ctypes.Structure]

	def __init__(
			self,
			opCode: lowLevel.InstructionType,
			**kwargs: Operand | _SimpleCData | ctypes.Array | ctypes.Structure
	):
		self.opCode = opCode
		self._params = kwargs

	@property
	def params(self) -> dict[str, Operand | _SimpleCData | ctypes.Array | ctypes.Structure]:
		return self._params


class InstructionList:

	_all: list[InstructionBase | str]
	_instructions: list[InstructionBase]
	_modified = False
	_byteCodeCache: bytes | None = None

	def __init__(self):
		super().__init__()
		self._all = []
		self._instructions = []

	def _addItem(self, item: InstructionBase | str):
		self._all.append(item)
		if isinstance(item, InstructionBase):
			self._instructions.append(item)
		self._modified = True

	def addComment(self, comment: str):
		self._addItem(f"# {comment}")

	def addInstruction(self, instruction: InstructionBase) -> int:
		self._addItem(instruction)
		return self.getInstructionCount() - 1

	def addGenericInstruction(
			self,
			opCode: lowLevel.InstructionType,
			**params: Operand | _SimpleCData | ctypes.Array | ctypes.Structure,
	) -> int:
		return self.addInstruction(GenericInstruction(opCode, **params))

	def addMetaCommand(self, command: str):
		self._addItem(f"[{command}]")

	def getByteCode(self) -> bytes:
		if self._byteCodeCache is not None and not self._modified:
			return self._byteCodeCache
		byteCode = b''
		for instruction in self._instructions:
			byteCode += instruction.getByteCode()
		self._byteCodeCache = byteCode
		self._modified = False
		return byteCode

	def getInstruction(self, index) -> InstructionBase:
		return self._instructions[index]

	def getInstructionCount(self) -> int:
		return len(self._instructions)

	def iterItems(self) -> Iterable[InstructionBase | str]:
		return iter(self._all)

	def dumpInstructions(self) -> str:
		output = ""
		for item in self.iterItems():
			if isinstance(item, InstructionBase):
				output += item.dumpInstruction()
			elif isinstance(item, str):
				output += item
			output += "\n"
		return output

	def clear(self):
		self._all.clear()
		self._instructions.clear()
		self._modified = False
		self._byteCodeCache = None


class RemoteOperationBuilder:

	_versionBytes: bytes = struct.pack('l', 0)
	_sectionNames = ["static", "const", "main"]
	_lastOperandIdRequested = OperandId(1)
	_defaultSection: str = "main"

	@property
	def lastOperandIdRequested(self) -> OperandId:
		return self._lastOperandIdRequested

	def __init__(self):
		self._instructionListBySection: dict[str, InstructionList] = {
			sectionName: InstructionList() for sectionName in self._sectionNames
		}
		self._remotedArgCache: dict[object, Operand] = {}
		self.operandIdGen = itertools.count(start=1)
		self._results = None

	def requestNewOperandId(self) -> OperandId:
		operandID = self.lastOperandIdRequested
		self._lastOperandIdRequested = OperandId(operandID.value + 1)
		return operandID

	def getInstructionList(self, section) -> InstructionList:
		return self._instructionListBySection[section]

	def getDefaultInstructionList(self) -> InstructionList:
		return self.getInstructionList(self._defaultSection)

	@contextlib.contextmanager
	def overrideDefaultSection(self, section: str):
		oldDefaultSection = self._defaultSection
		self._defaultSection = section
		yield
		self._defaultSection = oldDefaultSection

	def getAllInstructions(self) -> list[InstructionBase]:
		return list(itertools.chain.from_iterable(
			instructionList._instructions for instructionList in self._instructionListBySection.values()
		))

	def getByteCode(self) -> bytes:
		byteCode = self._versionBytes
		for sectionName in self._sectionNames:
			byteCode += self._instructionListBySection[sectionName].getByteCode()
		return byteCode

	def dumpInstructions(self) -> str:
		output = ""
		globalInstructionIndex = 0
		for sectionName, instructionList in self._instructionListBySection.items():
			output += f"{sectionName}:\n"
			for item in instructionList.iterItems():
				if isinstance(item, InstructionBase):
					output += f"{globalInstructionIndex}: "
					globalInstructionIndex += 1
					output += item.dumpInstruction()
				elif isinstance(item, str):
					output += item
				output += "\n"
		return output
