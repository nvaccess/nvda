# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

import enum
import functools
from numbers import Number
from typing import Optional, Self, Union
import contextlib
import _ctypes
import ctypes
from ctypes import (
	_SimpleCData,
	c_long,
	c_ulong,
	c_ushort,
	c_byte,
	c_char,
	c_wchar,
)
from comtypes import GUID
from dataclasses import dataclass
import inspect
import os
import struct
import itertools
from UIAHandler import UIA
from . import lowLevel
from logHandler import log


def _getLocationString(frame: inspect.FrameInfo) -> str:
	"""
	Returns a string describing the location of the given frame.
	It includes all ancestor frames with the same file path,
	plus one more frame with a different file path,
	so you can see what called into the file.
	"""
	locations = []
	oldPath = None
	while frame:
		path = os.path.relpath(inspect.getfile(frame))
		locations.append(
			f"File \"{path}\", line {frame.f_lineno}, in {frame.f_code.co_name}"
		)
		if oldPath and path != oldPath:
			break
		oldPath = path
		frame = frame.f_back
	locationString = "\n".join(reversed(locations))
	return locationString


@dataclass
class _InstructionRecord:
	instructionType: lowLevel.InstructionType
	params: list[bytes]
	locationString: str

	def __repr__(self):
		return f"{self.instructionType.name}({', '.join(map(repr, self.params))})\n{self.locationString}"


class _RemoteBaseObject:
	""" A base class for all remote objects. """

	_isTypeInstruction: lowLevel.InstructionType

	@classmethod
	def _new(cls, rob: "RemoteOperationBuilder", initialValue: object=None) -> "_RemoteBaseObject":
		operandId = rob._getNewOperandId()
		cls._initOperand(rob, operandId, initialValue)
		return cls(rob, operandId)

	@classmethod
	def _initOperand(cls, operandId: int, initialValue: object):
		raise NotImplementedError()

	def __init__(self, rob: "RemoteOperationBuilder", operandId: int):
		self._rob = rob
		self._operandId = operandId

	def stringify(self) -> "RemoteString":
		resultOperandId = self._rob._getNewOperandId() 
		result = RemoteString(self._rob, resultOperandId)
		self._rob._addInstruction(
			lowLevel.InstructionType.Stringify,
			c_long(resultOperandId),
			c_long(self._operandId)
		)
		return result


class _RemoteIntegral(_RemoteBaseObject):
	_newInstruction: lowLevel.InstructionType
	_initialValueType = _SimpleCData

	@classmethod
	def _initOperand(cls, rob: "RemoteOperationBuilder", operandId: int, initialValue: object):
		rob._addInstruction(
			cls._newInstruction,
			c_long(operandId),
			cls._initialValueType(initialValue)
		)


class _RemoteNumber(_RemoteIntegral):

	def _doBinaryOp(self, instructionType: lowLevel.InstructionType, other: Self | Number) -> Self:
		if not isinstance(other, type(self)):
			other = self._new(self._rob, other)
		resultOperandId = self._rob._getNewOperandId()
		result = type(self)(self._rob, resultOperandId)
		self._rob._addInstruction(
			instructionType,
			c_long(result._operandId),
			c_long(self._operandId),
			c_long(other._operandId)
		)
		return result

	def _doInplaceOp(self, instructionType: lowLevel.InstructionType, other: Self | Number) -> Self:
		if not isinstance(other, type(self)):
			other = self._new(self._rob, other)
		self._rob._addInstruction(
			instructionType,
			c_long(self._operandId),
			c_long(other._operandId)
		)
		return self

	def __add__(self, other: Self | Number) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.AddBinary, other)

	def __iadd__(self, other: Self | Number) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.AddInplace, other)

	def __sub__(self, other: Self | Number) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.SubtractBinary, other)

	def __isub__(self, other: Self | Number) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.SubtractInplace, other)

	def __mul__(self, other: Self | Number) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.MultiplyBinary, other)

	def __imul__(self, other: Self | Number) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.MultiplyInplace, other)

	def __truediv__(self, other: Self | Number) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.DivideBinary, other)

	def __itruediv__(self, other: Self | Number) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.DivideInplace, other)


class RemoteInt(_RemoteNumber):
	_isTypeInstruction = lowLevel.InstructionType.IsInt
	_newInstruction = lowLevel.InstructionType.NewInt
	_initialValueType = c_long


class RemoteBool(_RemoteIntegral):
	_isTypeInstruction = lowLevel.InstructionType.IsBool
	_newInstruction = lowLevel.InstructionType.NewBool
	_initialValueType = c_byte


class RemoteString(_RemoteBaseObject):
	_isTypeInstruction = lowLevel.InstructionType.IsString

	@classmethod
	def _initOperand(cls, rob: "RemoteOperationBuilder", operandId: int, initialValue: str):
		rob._addInstruction(
			lowLevel.InstructionType.NewString,
			c_long(operandId),
			ctypes.create_unicode_buffer(initialValue)
		)

	def _concat(self, other, toResult) -> None:
		if not isinstance(toResult, RemoteString):
			raise TypeError("toResult must be a RemoteString")
		if not isinstance(other, RemoteString):
			if isinstance(other, str):
				other = RemoteString._new(self._rob, other)
			elif isinstance(other, _RemoteBaseObject):
				other = other.stringify()
			else:
				raise TypeError("other must be a RemoteString, a str, or a _RemoteBaseObject")
		self._rob._addInstruction(
			lowLevel.InstructionType.RemoteStringConcat ,
			c_long(toResult._operandId),
			c_long(self._operandId),
			c_long(other._operandId)
		)

	def __add__(self, other: Self | _RemoteBaseObject | str) -> Self:
		resultOperandId = self._rob._getNewOperandId()
		result = RemoteString(self._rob, resultOperandId)
		self._concat(other, result)
		return result

	def __iadd__(self, other: Self | _RemoteBaseObject | str) -> Self:
		self._concat(other, self)
		return self


class _RemoteNullable(_RemoteBaseObject):

	@classmethod
	def _initOperand(cls, rob: "RemoteOperationBuilder", operandId: int, initialValue: None=None):
		rob._addInstruction(
			lowLevel.InstructionType.NewNull,
			c_long(operandId),
		)

	def isNull(self) -> bool:
		result = RemoteBool._new(self._rob, False)
		self._rob._addInstruction(
			lowLevel.InstructionType.IsNull,
			c_long(result._operandId),
			c_long(self._operandId)
		)
		return result


class RemoteVariant(_RemoteNullable):

	def isType(self, remoteClass: type[_RemoteBaseObject]) -> bool:
		if not issubclass(remoteClass, _RemoteBaseObject):
			raise TypeError("remoteClass must be a subclass of _RemoteBaseObject")
		result = self._rob.newBool()
		self._rob._addInstruction(
			lowLevel.InstructionType.IsType,
			c_long(result._operandId),
			c_long(self._operandId)
		)
		return result

	def asType(self, remoteClass: type[_RemoteBaseObject]) -> _RemoteBaseObject:
		return remoteClass(self._rob, self._operandId)


class RemoteExtensionTarget(_RemoteNullable):

	def isExtensionSupported(self, extensionGuid: GUID) -> bool:
		if not isinstance(extensionGuid, RemoteGuid):
			extensionGuid = self._rob.newGuid(extensionGuid)
		resultOperandId = self._rob._getNewOperandId()
		result = RemoteBool(self._rob, resultOperandId)
		self._rob._addInstruction(
			lowLevel.InstructionType.IsExtensionSupported,
			c_long(result._operandId),
			c_long(self._operandId),
			c_ulong(extensionGuid._operandId)
		)
		return result

	def callExtension(self, extensionGuid: GUID, *params: _RemoteBaseObject) -> None:
		if not isinstance(extensionGuid, RemoteGuid):
			extensionGuid = self._rob.newGuid(extensionGuid)
		self._rob._addInstruction(
			lowLevel.InstructionType.CallExtension,
			c_long(self._operandId),
			c_ulong(extensionGuid._operandId),
			c_long(len(params)),
			*(c_long(p._operandId) for p in params)
		)


class RemoteElement(RemoteExtensionTarget):
	_isTypeInstruction = lowLevel.InstructionType.IsElement

	def getPropertyValue(self, propertyId: int, ignoreDefault: bool=False) -> object:
		if not isinstance(propertyId, RemoteInt):
			propertyId = RemoteInt._new(self._rob, propertyId)
		if not isinstance(ignoreDefault, RemoteBool):
			ignoreDefault = RemoteBool._new(self._rob, ignoreDefault)
		resultOperandId = self._rob._getNewOperandId()
		result = RemoteVariant(self._rob, resultOperandId)
		self._rob._addInstruction(
			lowLevel.InstructionType.GetPropertyValue,
			c_long(result._operandId),
			c_long(self._operandId),
			c_long(propertyId._operandId),
			c_long(ignoreDefault._operandId)
		)
		return result


class RemoteTextRange(RemoteExtensionTarget):
	pass


class RemoteGuid(_RemoteBaseObject):
	_isTypeInstruction = lowLevel.InstructionType.IsGuid

	@classmethod
	def _initOperand(cls, rob: "RemoteOperationBuilder", operandId: int, initialValue: Union[GUID, str]):
		if isinstance(initialValue, str):
			initialValue = GUID(initialValue)
		rob._addInstruction(
			lowLevel.InstructionType.NewGuid,
			c_long(operandId),
			c_ulong(initialValue.Data1),
			c_ushort(initialValue.Data2),
			c_ushort(initialValue.Data3),
			*(c_byte(b) for b in initialValue.Data4)
		)


class MalformedBytecodeException(RuntimeError):
	pass


class InstructionLimitExceededException(RuntimeError):
	pass


class RemoteException(RuntimeError):
	pass


class ExecutionFailureException(RuntimeError):
	pass


class RemoteOperationBuilder:

	_versionBytes = struct.pack('l', 0) 

	_pyClassToRemoteClass = {
		int: RemoteInt,
		bool: RemoteBool,
		str: RemoteString,
		GUID: RemoteGuid,
		UIA.IUIAutomationElement: RemoteElement,
		UIA.IUIAutomationTextRange: RemoteTextRange,
	}

	def __init__(self, enableLogging: bool=False):
		self._instructions: list[_InstructionRecord] = []
		self._lastIfConditionInstructionPendingElse: _InstructionRecord | None = None
		self._operandIdGen = itertools.count(start=1)
		self._ro = lowLevel.RemoteOperation()
		self._scopeStack: list["_RemoteScopeContext"] = []
		self._results = None
		self._loggingEnablede = enableLogging
		if enableLogging:
			self._log: RemoteString = self.newString()
			self.addToResults(self._log)

	def _getNewOperandId(self) -> int:
		return next(self._operandIdGen)

	def _addInstruction(self, instruction: lowLevel.InstructionType, *params: _SimpleCData):
		""" Adds an instruction to the instruction list and returns the index of the instruction. """
		""" Adds an instruction to the instruction list and returns the index of the instruction. """
		self._lastIfConditionInstructionPendingElse = None
		frame = inspect.currentframe().f_back
		locationString = _getLocationString(frame)
		self._instructions.append(
			_InstructionRecord(instruction, params, locationString)
		)
		return len(self._instructions) - 1

	def _generateByteCode(self) -> bytes:
		byteCode = b''
		for instruction in self._instructions:
			byteCode += struct.pack('l', instruction.instructionType)
			for param in instruction.params:
				paramBytes = (c_char*ctypes.sizeof(param)).from_address(ctypes.addressof(param)).raw
				if isinstance(param, _ctypes.Array) and param._type_ == c_wchar:
					paramBytes = paramBytes[:-2]
					byteCode += struct.pack('l', len(param) - 1)
				byteCode += paramBytes
		return byteCode

	def importElement(self, element: UIA.IUIAutomationElement) -> RemoteElement:
		operandId = self._getNewOperandId()
		self._ro.importElement(operandId, element)
		return RemoteElement(self, operandId)

	def importTextRange(self, textRange: UIA.IUIAutomationTextRange):
		operandId = self._getNewOperandId()
		self._ro.importTextRange(operandId, textRange)
		return RemoteTextRange(self, operandId)

	@property
	def _lastInstructionIndex(self):
		return len(self._instructions) - 1

	def _getInstructionRecord(self, instructionIndex: int) -> _InstructionRecord:
		return self._instructions[instructionIndex]

	@property
	def _currentScope(self) -> Optional["_RemoteScopeContext"]:
		return self._scopeStack[-1] if self._scopeStack else None

	def newInt(self, initialValue: int=0) -> RemoteInt:
		return RemoteInt._new(self, initialValue)

	def newBool(self, initialValue: bool=False) -> RemoteBool:
		return RemoteBool._new(self, initialValue)

	def newString(self, initialValue: str="") -> RemoteString:
		return RemoteString._new(self, initialValue)

	def newVariant(self) -> RemoteVariant:
		return RemoteVariant._new(self)

	def newNULLExtensionTarget(self) -> RemoteExtensionTarget:
		return RemoteExtensionTarget._new(self)

	def newNULLElement(self) -> RemoteElement:
		return RemoteElement._new(self)

	def newNULLTextRange(self) -> RemoteTextRange:
		return RemoteTextRange._new(self)

	def newGuid(self, initialValue: GUID) -> RemoteGuid:
		return RemoteGuid._new(self, initialValue)

	def ifBlock(self, condition: RemoteBool):
		return _RemoteIfBlockBuilder(self, condition)

	def elseBlock(self):
		return _RemoteElseBlockBuilder(self)

	def halt(self):
		self._addInstruction(lowLevel.InstructionType.Halt)

	def logMessage(self,*strings): 
		if not self._loggingEnablede:
			return
		for string in strings:
			self._log += string
		self._log += "\n"

	def addToResults(self, remoteObj: _RemoteBaseObject):
		self._ro.addToResults(remoteObj._operandId)

	def importObjects(self, *imports: object) -> list[_RemoteBaseObject]:
		remoteObjects = []
		for importObj in imports:
			if isinstance(importObj, enum.Enum):
				importObj = importObj.value
			if isinstance(importObj, UIA.IUIAutomationElement):
				remoteObj = self.importElement(importObj)
			elif isinstance(importObj, UIA.IUIAutomationTextRange):
				remoteObj = self.importTextRange(importObj)
			else:
				remoteClass = self._pyClassToRemoteClass.get(type(importObj))
				if remoteClass:
					remoteObj = remoteClass._new(self, importObj)
				else:
					raise TypeError(f"{type(importObj)} is not a supported type")
			remoteObjects.append(remoteObj)
		return remoteObjects

	def execute(self):
		self.halt()
		byteCode = self._generateByteCode()
		self._results = self._ro.execute(self._versionBytes + byteCode)
		status = self._results.status
		if status == lowLevel.RemoteOperationStatus.MalformedBytecode:
			raise MalformedBytecodeException()
		elif status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
			raise InstructionLimitExceededException()
		elif status == lowLevel.RemoteOperationStatus.UnhandledException:
			instructionRecord = self._getInstructionRecord(self._results.errorLocation)
			message = f"\nError at instruction {self._results.errorLocation}: {instructionRecord}\nExtended error: {self._results.extendedError}"
			if self._loggingEnablede:
				try:
					logText = self.dumpLog()
					message += f"\n{logText}"
				except Exception as e:
					message += f"\nFailed to dump log: {e}\n"
			message += self._dumpInstructions()
			raise RemoteException(message)
		elif status == lowLevel.RemoteOperationStatus.ExecutionFailure:
			raise ExecutionFailureException()

	def getResult(self, remoteObj: _RemoteBaseObject) -> object:
		if not self._results:
			raise RuntimeError("Not executed")
		operandId = remoteObj._operandId
		if not self._results.hasOperand(operandId):
			raise LookupError("No such operand")
		return self._results.getOperand(operandId).value

	def dumpLog(self):
		if not self._loggingEnablede:
			raise RuntimeError("Logging not enabled")
		if self._log is None:
			return "Empty remote log"
		output = "--- remote log start ---\n"
		output += self.getResult(self._log)
		output += "--- remote log end ---"
		return output

	def _dumpInstructions(self) -> str:
		output = "--- Instructions start ---\n"
		for index, instruction in enumerate(self._instructions):
			output += f"{index}: {instruction.instructionType.name} {instruction.params}\n"
		output += "--- Instructions end ---"
		return output


class _RemoteScopeContext:

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder):
		self._rob = remoteOpBuilder

	def __enter__(self):
		self._rob._scopeStack.append(self)

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._rob._scopeStack.pop()


class _RemoteIfBlockBuilder(_RemoteScopeContext):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, condition: RemoteBool):
		super().__init__(remoteOpBuilder)
		self._condition = condition

	def __enter__(self):
		self._conditionInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.ForkIfFalse ,
			c_long(self._condition._operandId),
			c_long(1), # offset updated in Else method 
		)
		super().__enter__()

	def __exit__(self, exc_type, exc_val, exc_tb):
		super().__exit__(exc_type, exc_val, exc_tb)
		nextInstructionIndex = self._rob._lastInstructionIndex + 1
		relativeJumpOffset = nextInstructionIndex - self._conditionInstructionIndex
		conditionInstruction = self._rob._getInstructionRecord(self._conditionInstructionIndex)
		conditionInstruction.params[1].value = relativeJumpOffset
		self._rob._lastIfConditionInstructionPendingElse = conditionInstruction


class _RemoteElseBlockBuilder(_RemoteScopeContext):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder):
		super().__init__(remoteOpBuilder)

	def __enter__(self):
		if not self._rob._lastIfConditionInstructionPendingElse:
			raise RuntimeError("Else block not directly preceded by If block") 
		conditionInstruction = self._rob._lastIfConditionInstructionPendingElse
		self._rob._lastIfConditionInstructionPendingElse = None
		# add a final jump instruction to the previous if block to skip over the else block.
		self._jumpInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.Fork ,
			c_long(1), # offset updated in __exit__ method 
		)
		# increment the false offset of the previous if block to take the new jump instruction into account. 
		conditionInstruction.params[1].value += 1
		super().__enter__()

	def __exit__(self, exc_type, exc_val, exc_tb):
		super().__exit__(exc_type, exc_val, exc_tb)
		# update the jump instruction to jump to the real end of the else block. 
		nextInstructionIndex = self._rob._lastInstructionIndex + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self._rob._getInstructionRecord(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset


class RemoteFuncAPI:

	def __init__(self, rob: "RemoteOperationBuilder"):
		self._rob = rob

	def newInt(self, initialValue: int=0) -> RemoteInt:
		return self._rob.newInt(initialValue)

	def newBool(self, initialValue: bool=False) -> RemoteBool:
		return self._rob.newBool(initialValue)

	def newString(self, initialValue: str="") -> RemoteString:
		return self._rob.newString(initialValue)

	def newVariant(self) -> RemoteVariant:
		return self._rob.newVariant()

	def newNULLExtensionTarget(self) -> RemoteExtensionTarget:
		return self._rob.newNULLExtensionTarget()

	def newNULLElement(self) -> RemoteElement:
		return self._rob.newNULLElement()

	def newNULLTextRange(self) -> RemoteTextRange:
		return self._rob.newNULLTextRange()

	def newGuid(self, initialValue: GUID) -> RemoteGuid:
		return self._rob.newGuid(initialValue)

	def ifBlock(self, condition: RemoteBool):
		return self._rob.ifBlock(condition)

	def elseBlock(self):
		return self._rob.elseBlock()

	def halt(self):
		self._rob.halt()

	def logMessage(self,*strings): 
		self._rob.logMessage(*strings)


def execute(remoteFunc: callable, *imports: object, enableLogging=False) -> object: 
	rob = RemoteOperationBuilder(enableLogging=enableLogging)
	remoteObjects = rob.importObjects(*imports)
	ba = RemoteFuncAPI(rob)
	remoteResults = remoteFunc(ba, *remoteObjects)
	if isinstance(remoteResults, _RemoteBaseObject):
		remoteResults = [remoteResults]
	for remoteResult in remoteResults:
		rob.addToResults(remoteResult)
	rob.execute()
	if enableLogging:
		log.debug(rob.dumpLog())
	if len(remoteResults) == 1:
		return rob.getResult(remoteResults[0])
	return tuple(rob.getResult(remoteResult) for remoteResult in remoteResults)
