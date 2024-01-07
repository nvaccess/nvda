# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


import contextlib
from abc import ABCMeta, abstractmethod
import typing
from typing import (
	Self,
	Callable,
	Iterable,
	Generic,
	TypeVar,
	cast,
)
import types
import ctypes
from ctypes import (
	_SimpleCData,
	c_long,
	c_ulong,
	c_char,
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
from .lowLevel import OperandId, RelativeOffset


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


def _validateInstructionParams(
	instructionType: lowLevel.InstructionType,
	*params: ctypes._SimpleCData | ctypes.Array | ctypes.Structure
):
	try:
		instructionSpec = lowLevel.InstructionSpecs[instructionType]
	except KeyError:
		raise ValueError(f"Unknown instruction type {instructionType.name}")
	paramNames: list[str] = []
	for index, param in enumerate(params):
		if index >= len(instructionSpec.paramSpecs):
			if instructionSpec.finalParamRepeat:
				finalParamIndex = len(instructionSpec.paramSpecs) - 1
				finalParamCount = cast(ctypes._SimpleCData, params[finalParamIndex - 1]).value
				if (index - finalParamIndex) <= finalParamCount:
					index = finalParamIndex
				else:
					raise ValueError(
						f"Final parameter of instruction {instructionType.name} "
						f"must be given {finalParamCount} times, "
						"but more were given"
					)
			else:
				raise ValueError(f"Too many parameters for instruction {instructionType.name}")
		paramSpec = instructionSpec.paramSpecs[index]
		validParam = False
		if type(param) is paramSpec.ctype:
			validParam = True
		elif index > 0 and isinstance(param, ctypes.Array) and typing.get_origin(paramSpec.ctype) is ctypes.Array:
			if typing.get_args(paramSpec.ctype)[0] is param._type_:
				arrayLength = cast(c_ulong, params[index - 1]).value
				if len(param) != arrayLength:
					raise ValueError(
						f"param {index} ({paramSpec.name}) "
						f" of instruction {instructionType.name} "
						f"must have length {arrayLength}, not {len(param)}"
					)
				validParam = True
		if not validParam:
			raise TypeError(
				f"param {index} ({paramSpec.name}) "
				f"of instruction {instructionType.name} "
				f"must be of type {paramSpec.ctype.__name__}, "
				f"not {type(param).__name__}"
			)
		paramNames.append(paramSpec.name)
	return paramNames


@dataclass
class _InstructionRecord:
	instructionType: lowLevel.InstructionType
	params: tuple[_SimpleCData | ctypes.Array | ctypes.Structure, ...]
	validatedParamNames: list[str] | None = None
	locationString: str | None = None

	def __init__(
		self, instructionType: lowLevel.InstructionType,
		*params: _SimpleCData | ctypes.Array | ctypes.Structure,
		locationString: str | None = None
	):
		self.instructionType = instructionType
		self.params = params
		self.locationString = locationString
		self.validatedParamNames = _validateInstructionParams(instructionType, *params)

	def __repr__(self):
		return f"{self.instructionType.name}({', '.join(map(repr, self.params))})"


LocalTypeVar = TypeVar('LocalTypeVar')


class _RemoteBaseObject(Generic[LocalTypeVar], metaclass=ABCMeta):
	""" A base class for all remote objects. """

	_isTypeInstruction: lowLevel.InstructionType

	@classmethod
	def _new(cls, rob: "RemoteOperationBuilder", initialValue: LocalTypeVar | None = None) -> Self:
		obj = cls(rob)
		for record in obj._generateInitInstructions(initialValue):
			rob.addInstructionRecord(record)
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
		readOnly: bool = False
	) -> Self:
		if isinstance(obj, cls):
			remoteObj = cast(Self, obj)
			if remoteObj._rob is not rob:
				raise RuntimeError("Object belongs to a different RemoteOperationBuilder")
			return remoteObj
		if readOnly:
			cacheKey = (cls, obj)
			cachedRemoteObj = rob._remotedArgCache.get(cacheKey)
			if cachedRemoteObj is not None:
				assert isinstance(cachedRemoteObj, cls)
				return cast(Self, cachedRemoteObj)
		remoteObj = cls(rob)
		for record in remoteObj._generateInitInstructions(cast(LocalTypeVar, obj)):
			section = "constants" if readOnly else "main"
			rob.addInstructionRecord(record, section)
		if readOnly:
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
		remoteValue = type(self).ensureArgumentIsRemote(self._rob, value, readOnly=True)
		self._rob.addInstruction(
			lowLevel.InstructionType.Set,
			self.operandId,
			remoteValue.operandId
		)

	def stringify(self) -> "RemoteString":
		remoteResult = RemoteString(self._rob)
		self._rob.addInstruction(
			lowLevel.InstructionType.Stringify,
			remoteResult.operandId,
			self.operandId
		)
		return remoteResult

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self | LocalTypeVar) -> "RemoteBool":
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, readOnly=True)
		remoteResult = RemoteBool(self._rob)
		self._rob.addInstruction(
			lowLevel.InstructionType.Compare,
			remoteResult.operandId,
			self.operandId,
			remoteOther.operandId,
			c_ulong(comparisonType)
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
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, readOnly=True)
		remoteResult = type(self)(self._rob)
		self._rob.addInstruction(
			instructionType,
			remoteResult.operandId,
			self.operandId,
			remoteOther.operandId
		)
		return remoteResult

	def _doInplaceOp(self, instructionType: lowLevel.InstructionType, other: Self | LocalTypeVar) -> Self:
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, readOnly=True)
		self._rob.addInstruction(
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
			c_ulong(len(initialStringValue) + 1),
			ctypes.create_unicode_buffer(initialStringValue)
		)

	@classmethod
	def ensureArgumentIsRemote(
		cls, rob: "RemoteOperationBuilder",
		obj: Self | str | _RemoteBaseObject,
		readOnly: bool = False,
	) -> "RemoteString":
		if not isinstance(obj, cls) and isinstance(obj, _RemoteBaseObject):
			return cast(_RemoteBaseObject, obj).stringify()
		return super().ensureArgumentIsRemote(rob, obj, readOnly)

	def _concat(self, other: Self | str | _RemoteBaseObject, toResult: Self) -> None:
		remoteOther = type(self).ensureArgumentIsRemote(self._rob, other, readOnly=True)
		self._rob.addInstruction(
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
		self._rob.addInstruction(
			lowLevel.InstructionType.IsNull,
			remoteResult.operandId,
			self.operandId
		)
		return remoteResult


class RemoteVariant(_RemoteNullable):

	def isType(self, remoteClass: type[_RemoteBaseObject]) -> RemoteBool:
		if not issubclass(remoteClass, _RemoteBaseObject):
			raise TypeError("remoteClass must be a subclass of _RemoteBaseObject")
		remoteResult = RemoteBool(self._rob)
		self._rob.addInstruction(
			remoteClass._isTypeInstruction,
			remoteResult.operandId,
			self.operandId
		)
		return remoteResult

	def asType(self, remoteClass: type[_RemoteBaseObject]) -> _RemoteBaseObject:
		return remoteClass(self._rob, self.operandId)


class RemoteExtensionTarget(_RemoteNullable[LocalTypeVar], Generic[LocalTypeVar]):

	def isExtensionSupported(self, extensionGuid: GUID) -> RemoteBool:
		extensionGuid = RemoteGuid.ensureArgumentIsRemote(self._rob, extensionGuid, readOnly=True)
		remoteResult = RemoteBool(self._rob)
		self._rob.addInstruction(
			lowLevel.InstructionType.IsExtensionSupported,
			remoteResult.operandId,
			self.operandId,
			extensionGuid.operandId
		)
		return remoteResult

	def callExtension(self, extensionGuid: GUID, *params: _RemoteBaseObject) -> None:
		extensionGuid = RemoteGuid.ensureArgumentIsRemote(self._rob, extensionGuid, readOnly=True)
		self._rob.addInstruction(
			lowLevel.InstructionType.CallExtension,
			self.operandId,
			extensionGuid.operandId,
			c_ulong(len(params)),
			*(p.operandId for p in params)
		)


class RemoteElement(RemoteExtensionTarget[UIA.IUIAutomationElement]):
	_isTypeInstruction = lowLevel.InstructionType.IsElement

	def getPropertyValue(
		self,
		propertyId: int | RemoteInt,
		ignoreDefault: bool | RemoteBool = False
	) -> RemoteVariant:
		remotePropertyId = RemoteInt.ensureArgumentIsRemote(self._rob, propertyId, readOnly=True)
		remoteIgnoreDefault = RemoteBool.ensureArgumentIsRemote(self._rob, ignoreDefault, readOnly=True)
		remoteResult = RemoteVariant(self._rob)
		self._rob.addInstruction(
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
	errorLocation: int
	extendedError: int

	def __init__(self, errorLocation: int, extendedError: int):
		super().__init__(f"Remote exception at instruction {errorLocation}")
		self.errorLocation = errorLocation
		self.extendedError = extendedError


class ExecutionFailureException(RuntimeError):
	pass


class _InstructionList(list[_InstructionRecord]):

	_byteCodeCache: bytes | None = None
	_isModified: bool = False
	_commentsByInstructionIndex: dict[int, list[str]]

	def __init__(self):
		super().__init__()
		self._commentsByInstructionIndex = {}

	def prependComment(self, instructionIndex: int, comment: str):
		if instructionIndex not in self._commentsByInstructionIndex:
			self._commentsByInstructionIndex[instructionIndex] = []
		self._commentsByInstructionIndex[instructionIndex].append(comment)

	def getPrependedComments(self, instructionIndex: int) -> list[str]:
		return self._commentsByInstructionIndex.get(instructionIndex, [])

	def addInstructionRecord(self, record: _InstructionRecord, section: str = "main") -> int:
		if record.locationString is None:
			frame = inspect.currentframe()
			if frame:
				frame = frame.f_back
				if frame:
					record.locationString = _getLocationString(frame)
		self.append(record)
		self._isModified = True
		return len(self) - 1

	def getByteCode(self):
		if not self._isModified and self._byteCodeCache is not None:
			return self._byteCodeCache
		byteCode = b''
		for instruction in self:
			byteCode += struct.pack('l', instruction.instructionType)
			for param in instruction.params:
				paramBytes = (c_char * ctypes.sizeof(param)).from_address(ctypes.addressof(param)).raw
				byteCode += paramBytes
		self._byteCodeCache = byteCode
		return byteCode


class RemoteOperationBuilder:

	def __init__(self, ro: lowLevel.RemoteOperation, remoteLogging: bool = False):
		self._ro = ro
		self._scopeJustExited: _RemoteScope | None = None
		sectionNames = ["imports", "constants", "main"]
		self._instructionListBySection: dict[str, _InstructionList] = {
			sectionName: _InstructionList() for sectionName in sectionNames
		}
		self._remotedArgCache: dict[object, _RemoteBaseObject] = {}
		self.operandIdGen = itertools.count(start=1)
		self._results = None
		self._loggingEnablede = remoteLogging
		if remoteLogging:
			self._log: RemoteString = RemoteString._new(self)

	def _getNewOperandId(self) -> OperandId:
		return OperandId(next(self.operandIdGen))

	def getInstructionList(self, section: str) -> _InstructionList:
		return self._instructionListBySection[section]

	def addInstruction(
		self,
		instruction: lowLevel.InstructionType,
		*params: _SimpleCData | ctypes.Array | ctypes.Structure,
		section: str = "main"
	):
		record = _InstructionRecord(instruction, *params)
		return self.addInstructionRecord(record, section)

	def addInstructionRecord(self, record: _InstructionRecord, section: str = "main") -> int:
		instructionsList = self.getInstructionList(section)
		index = instructionsList.addInstructionRecord(record, section)
		self._scopeJustExited = None
		return index

	def addComment(self, comment: str, section: str = "main"):
		instructions = self.getInstructionList(section)
		instructionIndex = len(instructions)
		instructions.prependComment(instructionIndex, comment)

	def importElement(self, element: UIA.IUIAutomationElement) -> RemoteElement:
		operandId = self._getNewOperandId()
		self._ro.importElement(operandId, element)
		return RemoteElement(self, operandId)

	def importTextRange(self, textRange: UIA.IUIAutomationTextRange):
		operandId = self._getNewOperandId()
		self._ro.importTextRange(operandId, textRange)
		return RemoteTextRange(self, operandId)

	def getLastInstructionIndex(self, section: str = "main") -> int:
		instructions = self.getInstructionList(section)
		return len(instructions) - 1

	def getNextInstructionIndex(self, section: str = "main") -> int:
		instructions = self.getInstructionList(section)
		return len(instructions)

	def getInstruction(self, instructionIndex: int, section: str = "main") -> _InstructionRecord:
		instructions = self.getInstructionList(section)
		return instructions[instructionIndex]

	def lookupInstructionByGlobalIndex(self, instructionIndex: int) -> _InstructionRecord:
		instructions = [instruction for instructionList in self._instructionListBySection.values() for instruction in instructionList]
		return instructions[instructionIndex]

	def ifBlock(self, condition: RemoteBool):
		return _RemoteIfBlockBuilder(self, condition)

	def elseBlock(self):
		return _RemoteElseBlockBuilder(self)

	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool]):
		return _RemoteWhileBlockBuilder(self, conditionBuilderFunc)

	def breakLoop(self):
		self.addInstruction(lowLevel.InstructionType.BreakLoop)

	def continueLoop(self):
		self.addInstruction(lowLevel.InstructionType.ContinueLoop)

	def tryBlock(self):
		return _RemoteTryBlockBuilder(self)

	def catchBlock(self):
		return _RemoteCatchBlockBuilder(self)

	def setOperationStatus(self, status: int | RemoteInt):
		remoteStatus = RemoteInt.ensureArgumentIsRemote(self, status, readOnly=True)
		self.addInstruction(
			lowLevel.InstructionType.SetOperationStatus,
			remoteStatus.operandId
		)

	def getOperationStatus(self) -> RemoteInt:
		remoteResult = RemoteInt(self)
		self.addInstruction(
			lowLevel.InstructionType.GetOperationStatus,
			remoteResult.operandId
		)
		return remoteResult

	def halt(self):
		self.addInstruction(lowLevel.InstructionType.Halt)

	def _getLogOperandId(self) -> OperandId:
		return self._log.operandId

	def logMessage(self, *strings):
		if not self._loggingEnablede:
			return
		self.addComment("Begin logMessage code")
		for string in strings:
			self._log += string
		self._log += "\n"
		self.addComment("End logMessage code")

	def dumpInstructions(self) -> str:
		output = "--- Instructions start ---\n"
		globalInstructionIndex = 0
		for sectionName, instructions in self._instructionListBySection.items():
			output += f"{sectionName}:\n"
			for localInstructionIndex, instruction in enumerate(instructions):
				comments = instructions.getPrependedComments(localInstructionIndex)
				for comment in comments:
					output += f"#{comment}\n"
				output += f"{globalInstructionIndex}: {instruction.instructionType.name} ("
				paramOutputs = []
				for paramIndex, param in enumerate(instruction.params):
					if instruction.validatedParamNames is not None:
						paramName = instruction.validatedParamNames[paramIndex]
					else:
						paramName = "param"
					paramOutput = f"{paramName} {param}"
					paramOutputs.append(paramOutput)
				paramsOutput = ", ".join(paramOutputs)
				output += f"{paramsOutput})\n"
				globalInstructionIndex += 1
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

	def __enter__(self, silent: bool = False):
		self._silent = silent
		super().__enter__()
		self._conditionInstructionIndex = self._rob.addInstruction(
			lowLevel.InstructionType.ForkIfFalse,
			self._condition.operandId,
			RelativeOffset(1),  # offset updated in Else method
		)
		if not silent:
			self._rob.addComment("If block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		nextInstructionIndex = self._rob.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._conditionInstructionIndex
		conditionInstruction = self._rob.getInstruction(self._conditionInstructionIndex)
		conditionInstruction.params[1].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)
		if not self._silent:
			self._rob.addComment("End of if block body")


class _RemoteElseBlockBuilder(_RemoteScope):

	def __enter__(self):
		if not isinstance(self._rob._scopeJustExited, _RemoteIfBlockBuilder):
			raise RuntimeError("Else block not directly preceded by If block")
		ifScope = self._rob._scopeJustExited
		super().__enter__()
		conditionInstruction = self._rob.getInstruction(ifScope._conditionInstructionIndex)
		# add a final jump instruction to the previous if block to skip over the else block.
		self._rob.addComment("Jump over else block")
		self._jumpInstructionIndex = self._rob.addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		# increment the false offset of the previous if block to take the new jump instruction into account.
		conditionInstruction.params[1].value += 1
		self._rob.addComment("Else block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._rob.addComment("End of else block body")
		# update the jump instruction to jump to the real end of the else block.
		nextInstructionIndex = self._rob.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self._rob.getInstruction(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class _RemoteWhileBlockBuilder(_RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, conditionBuilderFunc: Callable[[], RemoteBool]):
		super().__init__(remoteOpBuilder)
		self._conditionBuilderFunc = conditionBuilderFunc

	def __enter__(self):
		super().__enter__()
		# Add a new loop block instruction to start the while loop
		self._newLoopBlockInstructionIndex = self._rob.addInstruction(
			lowLevel.InstructionType.NewLoopBlock,
			RelativeOffset(1),  # offset updated in __exit__ method
			RelativeOffset(1)
		)
		# Generate the loop condition instructions and enter the if block.
		self._rob.addComment("Loop condition")
		condition = self._conditionBuilderFunc()
		self._ifBlock = self._rob.ifBlock(condition)
		self._ifBlock.__enter__(silent=True)
		self._rob.addComment("Loop block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._rob.addComment("End of loop block body")
		# Add a jump instruction to the end of the body to jump back to the start of the loop block.
		self._rob.addComment("Jump back to loop condition")
		relativeContinueOffset = self._newLoopBlockInstructionIndex - self._rob.getLastInstructionIndex()
		self._rob.addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(relativeContinueOffset)
		)
		# Complete the if block.
		self._ifBlock.__exit__(exc_type, exc_val, exc_tb)
		# Add an end loop block instruction after the if block.
		self._rob.addInstruction(
			lowLevel.InstructionType.EndLoopBlock,
		)
		# Update the break offset of the new loop block instruction to jump to after the end loop block instruction.
		nextInstructionIndex = self._rob.getLastInstructionIndex() + 1
		relativeBreakOffset = nextInstructionIndex - self._newLoopBlockInstructionIndex
		newLoopBlockInstruction = self._rob.getInstruction(self._newLoopBlockInstructionIndex)
		newLoopBlockInstruction.params[0].value = relativeBreakOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class _RemoteTryBlockBuilder(_RemoteScope):

	def __enter__(self):
		super().__enter__()
		self._newTryBlockInstructionIndex = self._rob.addInstruction(
			lowLevel.InstructionType.NewTryBlock,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		super().__enter__()
		self._rob.addComment("Try block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._rob.addComment("End of try block body")
		# Add an end try block instruction after the try block.
		self._rob.addInstruction(
			lowLevel.InstructionType.EndTryBlock,
		)
		# Update the catchoffset of the new try block instruction to jump to after the end try block instruction.
		nextInstructionIndex = self._rob.getLastInstructionIndex() + 1
		relativeCatchOffset = nextInstructionIndex - self._newTryBlockInstructionIndex
		newTryBlockInstruction = self._rob.getInstruction(self._newTryBlockInstructionIndex)
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
		self._rob.addComment("Jump over catch block")
		self._jumpInstructionIndex = self._rob.addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		# Increment the catch offset of the try block to take the new jump instruction into account.
		newTryBlockInstruction = self._rob.getInstruction(tryScope._newTryBlockInstructionIndex)
		newTryBlockInstruction.params[0].value += 1
		self._rob.addComment("Catch block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._rob.addComment("End of catch block body")
		# Update the jump instruction to jump to the real end of the catch block.
		nextInstructionIndex = self._rob.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self._rob.getInstruction(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class RemoteOperationExecutor:

	_versionBytes = struct.pack('l', 0)

	def __init__(self, ro: lowLevel.RemoteOperation):
		self._ro = ro
		self._logOperandId: OperandId | None = None

	def addToResults(self, operandId: OperandId):
		self._ro.addToResults(operandId)

	def setLogOperandId(self, operandId: OperandId):
		self.addToResults(operandId)
		self._logOperandId = operandId

	def execute(self, byteCode: bytes):
		self._results = self._ro.execute(self._versionBytes + byteCode)
		status = self._results.status
		if status == lowLevel.RemoteOperationStatus.MalformedBytecode:
			raise MalformedBytecodeException()
		elif status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
			raise InstructionLimitExceededException()
		elif status == lowLevel.RemoteOperationStatus.UnhandledException:
			raise RemoteException(self._results.errorLocation, self._results.extendedError)
		elif status == lowLevel.RemoteOperationStatus.ExecutionFailure:
			raise ExecutionFailureException()

	def getResult(self, operandId: OperandId) -> object:
		if not self._results:
			raise RuntimeError("Not executed")
		if not self._results.hasOperand(operandId):
			raise LookupError("No such operand")
		return self._results.getOperand(operandId).value

	def getLogOutput(self):
		if not self._results:
			raise RuntimeError("Not executed")
		if self._logOperandId is None:
			return "Empty remote log"
		return self.getResult(self._logOperandId)
