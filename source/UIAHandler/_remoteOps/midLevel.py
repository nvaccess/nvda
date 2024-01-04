# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


from itertools import chain
from abc import ABCMeta, abstractmethod
from typing import (
	Self,
	Callable,
	Iterable,
	Generic,
	TypeVar,
	cast,
)
import types
import _ctypes
import ctypes
from ctypes import (
	_SimpleCData,
	c_long,
	c_char,
	c_wchar,
	c_bool
)
from comtypes import GUID
from dataclasses import dataclass
import inspect
import os
import struct
import itertools
from UIAHandler import UIA
from . import lowLevel
from .lowLevel import OperandId


def ensureString(val: str | None) -> str:
	if isinstance(val, str):
		return val
	elif val is None:
		return ""
	raise TypeError("val must be a str or None")


def ensureGuid(val: GUID | str | None) -> GUID:
	if isinstance(val, GUID):
		return val
	elif isinstance(val, str):
		return GUID(val)
	elif val is None:
		return GUID()
	raise TypeError("val must be a GUID, a str, or None")


class RelativeOffset(c_long):
	def __repr__(self) -> str:
		return f"RelativeOffset {self.value}"


def _getLocationString(frame: types.FrameType) -> str:
	"""
	Returns a string describing the location of the given frame.
	It includes all ancestor frames with the same file path,
	plus one more frame with a different file path,
	so you can see what called into the file.
	"""
	locations = []
	oldPath: str | None = None
	curFrame: types.FrameType | None = frame
	while curFrame:
		path = os.path.relpath(inspect.getfile(curFrame))
		locations.append(
			f"File \"{path}\", line {curFrame.f_lineno}, in {curFrame.f_code.co_name}"
		)
		if oldPath and path != oldPath:
			break
		oldPath = path
		curFrame = curFrame.f_back
	locationString = "\n".join(reversed(locations))
	return locationString


@dataclass
class _InstructionRecord:
	instructionType: lowLevel.InstructionType
	params: tuple[_SimpleCData | ctypes.Array | ctypes.Structure, ...]
	locationString: str | None

	def __init__(
		self, instructionType: lowLevel.InstructionType,
		*params: _SimpleCData | ctypes.Array | ctypes.Structure,
		locationString: str | None = None
	):
		self.instructionType = instructionType
		self.params = params
		self.locationString = locationString

	def __repr__(self):
		return f"{self.instructionType.name}({', '.join(map(repr, self.params))})\n{self.locationString}"


LocalTypeVar = TypeVar('LocalTypeVar')


class _RemoteBaseObject(Generic[LocalTypeVar], metaclass=ABCMeta):
	""" A base class for all remote objects. """

	_isTypeInstruction: lowLevel.InstructionType

	@classmethod
	def _new(cls, rob: "RemoteOperationBuilder", initialValue: LocalTypeVar | None = None) -> Self:
		obj = cls(rob)
		for instruction in obj._generateInitInstructions(initialValue):
			rob._addInstruction(instruction.instructionType, *instruction.params)
		return obj

	@abstractmethod
	def _generateInitInstructions(
		self, initialValue: LocalTypeVar | None = None
	) -> Iterable[_InstructionRecord]:
		raise NotImplementedError()

	@classmethod
	def ensureArgumentIsRemote(
		cls, rob: "RemoteOperationBuilder",
		obj: Self | LocalTypeVar,
		useCache: bool = False
	) -> Self:
		if isinstance(obj, cls):
			remoteObj = cast(Self, obj)
			if remoteObj._rob is not rob:
				raise RuntimeError("Object belongs to a different RemoteOperationBuilder")
			return remoteObj
		if useCache:
			cacheKey = (cls, obj)
			cachedRemoteObj = rob._remotedArgCache.get(cacheKey)
			if cachedRemoteObj is not None:
				assert isinstance(cachedRemoteObj, cls)
				return cast(Self, cachedRemoteObj)
		remoteObj = cls(rob)
		for instruction in remoteObj._generateInitInstructions(cast(LocalTypeVar, obj)):
			rob._addInstruction(instruction.instructionType, *instruction.params, globalSection=useCache)
		if useCache:
			rob._remotedArgCache[cacheKey] = remoteObj
		return remoteObj

	def __init__(self, rob: "RemoteOperationBuilder", operandId: OperandId | None = None):
		self._rob = rob
		self._operandId = operandId if operandId is not None else rob._getNewOperandId()

	def __repr__(self) -> str:
		return f"{self.__class__.__name__} at {self.operandId}"

	@property
	def operandId(self) -> OperandId:
		return self._operandId

	def set(self, value: Self | LocalTypeVar) -> None:
		remoteValue = type(self).ensureArgumentIsRemote(self._rob, value, useCache=True)
		self._rob._addInstruction(
			lowLevel.InstructionType.Set,
			self.operandId,
			remoteValue.operandId
		)

	def stringify(self) -> "RemoteString":
		remoteResult = RemoteString(self._rob)
		self._rob._addInstruction(
			lowLevel.InstructionType.Stringify,
			remoteResult.operandId,
			self.operandId
		)
		return remoteResult

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self | LocalTypeVar) -> "RemoteBool":
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, useCache=True)
		remoteResult = RemoteBool(self._rob)
		self._rob._addInstruction(
			lowLevel.InstructionType.Compare,
			remoteResult.operandId,
			self.operandId,
			remoteOther.operandId,
			c_long(comparisonType)
		)
		return remoteResult

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, type(self)):
			return False
		return self.operandId == other.operandId


class _RemoteEqualityComparible(_RemoteBaseObject[LocalTypeVar], Generic[LocalTypeVar]):

	def isEqual(self, other: Self | LocalTypeVar) -> "RemoteBool":
		return self._doCompare(lowLevel.ComparisonType.Equal, other)


class _RemoteIntegral(_RemoteEqualityComparible[LocalTypeVar], Generic[LocalTypeVar]):
	_newInstruction: lowLevel.InstructionType
	_initialValueType: type[_SimpleCData]

	def _generateInitInstructions(
		self, initialValue: LocalTypeVar | None = None
	) -> Iterable[_InstructionRecord]:
		yield _InstructionRecord(
			self._newInstruction,
			self.operandId,
			self._initialValueType(initialValue)
		)


class RemoteBool(_RemoteIntegral[bool]):
	_isTypeInstruction = lowLevel.InstructionType.IsBool
	_newInstruction = lowLevel.InstructionType.NewBool
	_initialValueType = c_bool


class _RemoteNumber(_RemoteIntegral[LocalTypeVar], Generic[LocalTypeVar]):

	def __gt__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.GreaterThan, other)

	def __lt__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.LessThan, other)

	def __ge__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.GreaterThanOrEqual, other)

	def __le__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.LessThanOrEqual, other)

	def _doBinaryOp(self, instructionType: lowLevel.InstructionType, other: Self | LocalTypeVar) -> Self:
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, useCache=True)
		remoteResult = type(self)(self._rob)
		self._rob._addInstruction(
			instructionType,
			remoteResult.operandId,
			self.operandId,
			remoteOther.operandId
		)
		return remoteResult

	def _doInplaceOp(self, instructionType: lowLevel.InstructionType, other: Self | LocalTypeVar) -> Self:
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, useCache=True)
		self._rob._addInstruction(
			instructionType,
			self.operandId,
			remoteOther.operandId
		)
		return self

	def __add__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryAdd, other)

	def __iadd__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Add, other)

	def __sub__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinarySubtract, other)

	def __isub__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Subtract, other)

	def __mul__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryMultiply, other)

	def __imul__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Multiply, other)

	def __truediv__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryDivide, other)

	def __itruediv__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Divide, other)


class RemoteInt(_RemoteNumber[int]):
	_isTypeInstruction = lowLevel.InstructionType.IsInt
	_newInstruction = lowLevel.InstructionType.NewInt
	_initialValueType = c_long


class RemoteString(_RemoteEqualityComparible[str]):
	_isTypeInstruction = lowLevel.InstructionType.IsString

	def _generateInitInstructions(
		self, initialValue: str | None = ""
	) -> Iterable[_InstructionRecord]:
		initialStringValue = ensureString(initialValue)
		yield _InstructionRecord(
			lowLevel.InstructionType.NewString,
			self.operandId,
			ctypes.create_unicode_buffer(initialStringValue)
		)

	@classmethod
	def ensureArgumentIsRemote(
		cls, rob: "RemoteOperationBuilder",
		obj: Self | str | _RemoteBaseObject,
		useCache: bool = False,
	) -> "RemoteString":
		if not isinstance(obj, cls) and isinstance(obj, _RemoteBaseObject):
			return cast(_RemoteBaseObject, obj).stringify()
		return super().ensureArgumentIsRemote(rob, obj, useCache)

	def _concat(self, other: Self | str | _RemoteBaseObject, toResult: Self) -> None:
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, useCache=True)
		self._rob._addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			toResult.operandId,
			self.operandId,
			remoteOther.operandId
		)

	def __add__(self, other: Self | str | _RemoteBaseObject) -> Self:
		remoteResult = type(self)(self._rob)
		self._concat(other, remoteResult)
		return remoteResult

	def __iadd__(self, other: Self | _RemoteBaseObject | str) -> Self:
		self._concat(other, self)
		return self


class _RemoteNullable(_RemoteBaseObject[LocalTypeVar], Generic[LocalTypeVar]):

	def _generateInitInstructions(
		self, initialValue: object = None
	) -> Iterable[_InstructionRecord]:
		yield _InstructionRecord(
			lowLevel.InstructionType.NewNull,
			self.operandId,
		)

	def isNull(self) -> RemoteBool:
		remoteResult = RemoteBool(self._rob)
		self._rob._addInstruction(
			lowLevel.InstructionType.IsNull,
			remoteResult.operandId,
			self.operandId
		)
		return remoteResult


class RemoteVariant(_RemoteNullable):

	def isType(self, remoteClass: type[_RemoteBaseObject]) -> RemoteBool:
		if not issubclass(remoteClass, _RemoteBaseObject):
			raise TypeError("remoteClass must be a subclass of _RemoteBaseObject")
		result = self._rob.newBool()
		self._rob._addInstruction(
			remoteClass._isTypeInstruction,
			result.operandId,
			self.operandId
		)
		return result

	def asType(self, remoteClass: type[_RemoteBaseObject]) -> _RemoteBaseObject:
		return remoteClass(self._rob, self.operandId)


class RemoteExtensionTarget(_RemoteNullable[LocalTypeVar], Generic[LocalTypeVar]):

	def isExtensionSupported(self, extensionGuid: GUID) -> RemoteBool:
		extensionGuid = RemoteGuid.ensureArgumentIsRemote(self._rob, extensionGuid, useCache=True)
		remoteResult = RemoteBool(self._rob)
		self._rob._addInstruction(
			lowLevel.InstructionType.IsExtensionSupported,
			remoteResult.operandId,
			self.operandId,
			extensionGuid.operandId
		)
		return remoteResult

	def callExtension(self, extensionGuid: GUID, *params: _RemoteBaseObject) -> None:
		extensionGuid = RemoteGuid.ensureArgumentIsRemote(self._rob, extensionGuid, useCache=True)
		self._rob._addInstruction(
			lowLevel.InstructionType.CallExtension,
			self.operandId,
			extensionGuid.operandId,
			c_long(len(params)),
			*(p.operandId for p in params)
		)


class RemoteElement(RemoteExtensionTarget[UIA.IUIAutomationElement]):
	_isTypeInstruction = lowLevel.InstructionType.IsElement

	def getPropertyValue(
		self,
		propertyId: int | RemoteInt,
		ignoreDefault: bool | RemoteBool = False
	) -> RemoteVariant:
		remotePropertyId = RemoteInt.ensureArgumentIsRemote(self._rob, propertyId, useCache=True)
		remoteIgnoreDefault = RemoteBool.ensureArgumentIsRemote(self._rob, ignoreDefault, useCache=True)
		remoteResult = self._rob.newVariant()
		self._rob._addInstruction(
			lowLevel.InstructionType.GetPropertyValue,
			remoteResult.operandId,
			self.operandId,
			remotePropertyId.operandId,
			remoteIgnoreDefault.operandId
		)
		return remoteResult


class RemoteTextRange(RemoteExtensionTarget[UIA.IUIAutomationTextRange]):
	pass


class RemoteGuid(_RemoteEqualityComparible[GUID]):
	_isTypeInstruction = lowLevel.InstructionType.IsGuid

	def _generateInitInstructions(
		self, initialValue: GUID | str | None = None
	) -> Iterable[_InstructionRecord]:
		guid = ensureGuid(initialValue)
		yield _InstructionRecord(
			lowLevel.InstructionType.NewGuid,
			self.operandId,
			guid
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

	def __init__(self, enableLogging: bool = False):
		self._scopeJustExited: _RemoteScope | None = None
		self._globalInstructions: list[_InstructionRecord] = []
		self._mainInstructions: list[_InstructionRecord] = []
		self._remotedArgCache: dict[object, _RemoteBaseObject] = {}
		self.operandIdGen = itertools.count(start=1)
		self._ro = lowLevel.RemoteOperation()
		self._results = None
		self._loggingEnablede = enableLogging
		if enableLogging:
			self._log: RemoteString = self.newString()
			self.addToResults(self._log)

	def _getNewOperandId(self) -> OperandId:
		return OperandId(next(self.operandIdGen))

	def _addInstruction(
		self,
		instruction: lowLevel.InstructionType,
		*params: _SimpleCData | ctypes.Array | ctypes.Structure,
		globalSection: bool = False
	):
		""" Adds an instruction to the instruction list and returns the index of the instruction. """
		self._scopeJustExited = None
		locationString: str | None = None
		frame = inspect.currentframe()
		if frame:
			frame = frame.f_back
			if frame:
				locationString = _getLocationString(frame)
		record = _InstructionRecord(instruction, *params, locationString=locationString)
		if globalSection:
			self._globalInstructions.append(record)
			return len(self._globalInstructions) - 1
		else:
			self._mainInstructions.append(record)
			return len(self._mainInstructions) - 1

	def _generateByteCode(self) -> bytes:
		byteCode = b''
		for instruction in chain(self._globalInstructions, self._mainInstructions):
			byteCode += struct.pack('l', instruction.instructionType)
			for param in instruction.params:
				paramBytes = (c_char * ctypes.sizeof(param)).from_address(ctypes.addressof(param)).raw
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

	def _getLastInstructionIndex(self, globalSection: bool = False):
		if globalSection:
			return len(self._globalInstructions) - 1
		else:
			return len(self._mainInstructions) - 1

	def _getInstruction(self, instructionIndex: int, globalSection: bool = False) -> _InstructionRecord:
		if globalSection:
			return self._globalInstructions[instructionIndex]
		else:
			return self._mainInstructions[instructionIndex]

	def newInt(self, initialValue: int = 0) -> RemoteInt:
		return RemoteInt._new(self, initialValue)

	def newBool(self, initialValue: bool = False) -> RemoteBool:
		return RemoteBool._new(self, initialValue)

	def newString(self, initialValue: str = "") -> RemoteString:
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

	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool]):
		return _RemoteWhileBlockBuilder(self, conditionBuilderFunc)

	def breakLoop(self):
		self._addInstruction(lowLevel.InstructionType.BreakLoop)

	def continueLoop(self):
		self._addInstruction(lowLevel.InstructionType.ContinueLoop)

	def tryBlock(self):
		return _RemoteTryBlockBuilder(self)

	def catchBlock(self):
		return _RemoteCatchBlockBuilder(self)

	def setOperationStatus(self, status: int | RemoteInt):
		remoteStatus = RemoteInt.ensureArgumentIsRemote(self, status, useCache=True)
		self._addInstruction(
			lowLevel.InstructionType.SetOperationStatus,
			remoteStatus.operandId
		)

	def getOperationStatus(self) -> RemoteInt:
		remoteResult = RemoteInt(self)
		self._addInstruction(
			lowLevel.InstructionType.GetOperationStatus,
			remoteResult.operandId
		)
		return remoteResult

	def halt(self):
		self._addInstruction(lowLevel.InstructionType.Halt)

	def logMessage(self, *strings):
		if not self._loggingEnablede:
			return
		for string in strings:
			self._log += string
		self._log += "\n"

	def addToResults(self, remoteObj: _RemoteBaseObject):
		self._ro.addToResults(remoteObj.operandId)

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
			instructionRecord = self._getInstruction(self._results.errorLocation)
			message = (
				f"\nError at instruction {self._results.errorLocation}: "
				f"{instructionRecord}\n"
				f"Extended error: {self._results.extendedError}\n"
			)
			if self._loggingEnablede:
				try:
					logText = self.dumpLog()
					message += f"\n{logText}"
				except Exception as e:
					message += f"\nFailed to dump log: {e}\n"
			message += self.dumpInstructions()
			raise RemoteException(message)
		elif status == lowLevel.RemoteOperationStatus.ExecutionFailure:
			raise ExecutionFailureException()

	def getResult(self, remoteObj: _RemoteBaseObject) -> object:
		if not self._results:
			raise RuntimeError("Not executed")
		operandId = remoteObj.operandId
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

	def dumpInstructions(self) -> str:
		output = "--- Instructions start ---\n"
		for index, instruction in enumerate(chain(self._globalInstructions, self._mainInstructions)):
			output += f"{index}: {instruction.instructionType.name} {instruction.params}\n"
		output += "--- Instructions end ---"
		return output


class _RemoteScope:

	def __init__(self, rob: RemoteOperationBuilder):
		self._rob = rob

	def __enter__(self):
		self._rob._scopeJustExited = None

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._rob._scopeJustExited = self


class _RemoteIfBlockBuilder(_RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, condition: RemoteBool):
		super().__init__(remoteOpBuilder)
		self._condition = condition

	def __enter__(self):
		super().__enter__()
		self._conditionInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.ForkIfFalse,
			self._condition.operandId,
			RelativeOffset(1),  # offset updated in Else method
		)

	def __exit__(self, exc_type, exc_val, exc_tb):
		nextInstructionIndex = self._rob._getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._conditionInstructionIndex
		conditionInstruction = self._rob._getInstruction(self._conditionInstructionIndex)
		conditionInstruction.params[1].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class _RemoteElseBlockBuilder(_RemoteScope):

	def __enter__(self):
		if not isinstance(self._rob._scopeJustExited, _RemoteIfBlockBuilder):
			raise RuntimeError("Else block not directly preceded by If block")
		ifScope = self._rob._scopeJustExited
		super().__enter__()
		conditionInstruction = self._rob._getInstruction(ifScope._conditionInstructionIndex)
		# add a final jump instruction to the previous if block to skip over the else block.
		self._jumpInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		# increment the false offset of the previous if block to take the new jump instruction into account.
		conditionInstruction.params[1].value += 1

	def __exit__(self, exc_type, exc_val, exc_tb):
		# update the jump instruction to jump to the real end of the else block.
		nextInstructionIndex = self._rob._getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self._rob._getInstruction(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class _RemoteWhileBlockBuilder(_RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, conditionBuilderFunc: Callable[[], RemoteBool]):
		super().__init__(remoteOpBuilder)
		self._conditionBuilderFunc = conditionBuilderFunc

	def __enter__(self):
		super().__enter__()
		# Add a new loop block instruction to start the while loop
		self._newLoopBlockInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.NewLoopBlock,
			RelativeOffset(1),  # offset updated in __exit__ method
			RelativeOffset(1)
		)
		# Generate the loop condition instructions and enter the if block.
		condition = self._conditionBuilderFunc()
		self._ifBlock = self._rob.ifBlock(condition)
		self._ifBlock.__enter__()

	def __exit__(self, exc_type, exc_val, exc_tb):
		# Add a jump instruction to the end of the body to jump back to the start of the loop block.
		relativeContinueOffset = self._newLoopBlockInstructionIndex - self._rob._getLastInstructionIndex()
		self._rob._addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(relativeContinueOffset)
		)
		# Complete the if block.
		self._ifBlock.__exit__(exc_type, exc_val, exc_tb)
		# Add an end loop block instruction after the if block.
		self._rob._addInstruction(
			lowLevel.InstructionType.EndLoopBlock,
		)
		# Update the break offset of the new loop block instruction to jump to after the end loop block instruction.
		nextInstructionIndex = self._rob._getLastInstructionIndex() + 1
		relativeBreakOffset = nextInstructionIndex - self._newLoopBlockInstructionIndex
		newLoopBlockInstruction = self._rob._getInstruction(self._newLoopBlockInstructionIndex)
		newLoopBlockInstruction.params[0].value = relativeBreakOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class _RemoteTryBlockBuilder(_RemoteScope):

	def __enter__(self):
		super().__enter__()
		self._newTryBlockInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.NewTryBlock,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		super().__enter__()

	def __exit__(self, exc_type, exc_val, exc_tb):
		# Add an end try block instruction after the try block.
		self._rob._addInstruction(
			lowLevel.InstructionType.EndTryBlock,
		)
		# Update the catchoffset of the new try block instruction to jump to after the end try block instruction.
		nextInstructionIndex = self._rob._getLastInstructionIndex() + 1
		relativeCatchOffset = nextInstructionIndex - self._newTryBlockInstructionIndex
		newTryBlockInstruction = self._rob._getInstruction(self._newTryBlockInstructionIndex)
		newTryBlockInstruction.params[0].value = relativeCatchOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class _RemoteCatchBlockBuilder(_RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder):
		super().__init__(remoteOpBuilder)

	def __enter__(self):
		if not isinstance(self._rob._scopeJustExited, _RemoteTryBlockBuilder):
			raise RuntimeError("Catch block not directly preceded by Try block")
		tryScope = self._rob._scopeJustExited
		super().__enter__()
		# Add a jump instruction directly after the try block to skip over the catch block.
		self._jumpInstructionIndex = self._rob._addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		# Increment the catch offset of the try block to take the new jump instruction into account.
		newTryBlockInstruction = self._rob._getInstruction(tryScope._newTryBlockInstructionIndex)
		newTryBlockInstruction.params[0].value += 1

	def __exit__(self, exc_type, exc_val, exc_tb):
		# Update the jump instruction to jump to the real end of the catch block.
		nextInstructionIndex = self._rob._getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self._rob._getInstruction(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)
