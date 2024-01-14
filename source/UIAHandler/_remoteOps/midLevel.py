# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


from __future__ import annotations
import typing
from typing import (
	Type,
	Self,
	Callable,
	ParamSpec,
	Concatenate,
	Iterable,
	Generic,
	TypeVar,
	cast
	)
import types
import inspect
import functools
import threading
import weakref
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
import os
import struct
import itertools
from UIAHandler import UIA
from . import lowLevel
from .lowLevel import OperandId, RelativeOffset, InstructionType


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
class InstructionRecord:
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


class _RemoteBase:

	_builderRef: weakref.ReferenceType[RemoteOperationBuilder] | None = None

	@property
	def builder(self) -> RemoteOperationBuilder:
		if self._builderRef is None:
			raise RuntimeError("Object not bound yet")
		builder = self._builderRef()
		if builder is None:
			raise RuntimeError("Builder has died")
		return builder

	def bind(self, builder: RemoteOperationBuilder):
		self._builderRef = weakref.ref(builder)


_remoteFunc_self = TypeVar('_remoteFunc_self', bound=_RemoteBase)
_remoteFunc_paramSpec = ParamSpec('_remoteFunc_paramSpec')
_remoteFunc_return = TypeVar('_remoteFunc_return')
_remoteFunc_localData = threading.local()
_remoteFunc_localData.funcDepth = 0
def remoteFunc(
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return]:
	@functools.wraps(func)
	def wrapper(self: _remoteFunc_self, *args: _remoteFunc_paramSpec.args, **kwargs: _remoteFunc_paramSpec.kwargs) -> _remoteFunc_return:
		topLevel = _remoteFunc_localData.funcDepth == 0
		callArgs = inspect.getcallargs(func, self, *args, **kwargs)
		for index, (name, val) in enumerate(callArgs.items()):
			if index == 0:
				continue
			for subVal in (val if isinstance(val, Iterable) else [val]):
				if not isinstance(subVal, RemoteBaseObject):
					raise TypeError(f"Argument must be a RemoteBaseObject, not {type(subVal).__name__}")
				section = "imports" if topLevel else None
				print(f"binding {subVal} to {self.builder}")
				subVal.bind(self.builder, section=section)
		try:
			_remoteFunc_localData.funcDepth += 1
			return func(self, *args, **kwargs)
		finally:
			_remoteFunc_localData.funcDepth -= 1
		return func(self, *args, **kwargs)
	return wrapper


class RemoteBaseObject(_RemoteBase):

	_operandId: OperandId | None = None

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, type(self)):
			return False
		builder = self._builderRef() if self._builderRef is not None else None
		otherBuilder = other._builderRef() if other._builderRef is not None else None
		if builder != otherBuilder:
			return False
		if self._operandId != other._operandId:
			return False
		return True

	def __repr__(self) -> str:
		builder = self._builderRef() if self._builderRef is not None else None
		if builder is None:
			return f"unbound {self.__class__.__name__}"
		return f"{self.__class__.__name__} at {self.operandId}"

	@property
	def operandId(self) -> OperandId:
		if self._operandId is None:
			raise RuntimeError("Object not bound yet")
		return self._operandId

	@classmethod
	def fromOperandId(cls, builder: RemoteOperationBuilder, operandId: OperandId) -> Self:
		remoteObj = cls()
		remoteObj._builderRef = weakref.ref(builder)
		remoteObj._operandId = operandId
		return remoteObj

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId) -> Iterable[InstructionRecord]:
		raise NotImplementedError()

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		operandId = builder._getNewOperandId()
		for record in self._generateInitInstructions(operandId):
			builder.addInstructionRecord(record, section=section)
		return operandId

	_defaultSectionForInitInstructions: str = "main"

	def bind(self, builder: RemoteOperationBuilder, section: str | None = None):
		oldBuilder = self._builderRef() if self._builderRef is not None else None
		if oldBuilder is not None:
			if builder != oldBuilder:
				import gc
				referrers = gc.get_referrers(oldBuilder)
				raise RuntimeError(f"Object already bound to a different RemoteOperationBuilder.\n{referrers=}")
			else:
				# already bound.
				return
		operandId = self._initOperand(builder, section or self._defaultSectionForInitInstructions)
		super().bind(builder)
		self._operandId = operandId

	@remoteFunc
	def set(self, other: Self):
		self.builder.addInstruction(
			lowLevel.InstructionType.Set,
			self.operandId,
			other.operandId
		)

	@remoteFunc
	def stringify(self) -> RemoteString:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.Stringify,
			resultOperandId,
			self.operandId
		)
		result = RemoteString.fromOperandId(self.builder, resultOperandId)
		return result


class RemoteVariantSupportedType(RemoteBaseObject):

	_isTypeInstruction: lowLevel.InstructionType


class RemoteNull(RemoteVariantSupportedType):
	_isTypeInstruction = lowLevel.InstructionType.IsNull

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewNull,
			operandId
		)


class RemoteVariant(RemoteBaseObject):

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewNull,
			operandId
		)

	def isType(self, remoteClass: Type[RemoteVariantSupportedType]) -> RemoteBool:
		if not issubclass(remoteClass, RemoteVariantSupportedType):
			raise TypeError("remoteClass must be a subclass of _RemoteBaseObject")
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			remoteClass._isTypeInstruction,
			resultOperandId,
			self.operandId
		)
		return RemoteBool.fromOperandId(self.builder, resultOperandId)

	def isNull(self) -> RemoteBool:
		return self.isType(RemoteNull)

	_TV_asType = TypeVar('_TV_asType', bound=RemoteVariantSupportedType)
	def asType(self, remoteClass: Type[_TV_asType]) -> _TV_asType:
		return remoteClass.fromOperandId(self.builder, self.operandId)

LocalTypeVar = TypeVar('LocalTypeVar')
class RemoteValue(RemoteVariantSupportedType, Generic[LocalTypeVar]):

	LocalType: Type[LocalTypeVar]
	_initialValue: LocalTypeVar | None = None
	_defaultInitialValue: LocalTypeVar | None = None

	def __init__(self, initialValue: LocalTypeVar | None = None):
		if initialValue is not None and not isinstance(initialValue, self.LocalType):
			raise TypeError(f"initialValue must be of type {self.LocalType.__name__}")
		super().__init__()
		self._initialValue = initialValue

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId, initialValue: LocalTypeVar) -> Iterable[InstructionRecord]:
		raise NotImplementedError()

	@property
	def initialValue(self) -> LocalTypeVar:
		if self._initialValue is not None:
			return self._initialValue
		defaultInitialValue = self._defaultInitialValue
		if defaultInitialValue is not None:
			return defaultInitialValue
		raise RuntimeError("No initial or default value")

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		operandId = builder._getNewOperandId()
		for record in self._generateInitInstructions(operandId, self.initialValue):
			builder.addInstructionRecord(record, section=section)
		return operandId

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self) -> RemoteBool:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.Compare,
			resultOperandId,
			self.operandId,
			other.operandId,
			c_ulong(comparisonType)
		)
		return RemoteBool.fromOperandId(self.builder, resultOperandId)

	@remoteFunc
	def isEqual(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.Equal, other)


class CachedRemoteValue(RemoteValue[LocalTypeVar], Generic[LocalTypeVar]):

	_defaultSectionForInitInstructions = "constants"

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		cacheKey = (type(self), self.initialValue)
		cachedOperandId = builder._remotedArgCache.get(cacheKey)
		if cachedOperandId is not None:
			return cachedOperandId
		operandId = super()._initOperand(builder, section)
		builder._remotedArgCache[cacheKey] = operandId
		return operandId

	@remoteFunc
	def set(self, other: Self):
		raise RuntimeError("Cannot set a const remote value")


class RemoteIntegral(RemoteValue[LocalTypeVar], Generic[LocalTypeVar]):

	_newInstruction: lowLevel.InstructionType
	_ctype: Type[_SimpleCData]

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId, initialValue: LocalTypeVar) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			cls._newInstruction,
			operandId,
			cls._ctype(initialValue) 
		)

	@remoteFunc
	def copy(self) -> Self:
		copy = type(self)()
		copy.bind(self.builder)
		self.builder.addInstruction(
			lowLevel.InstructionType.Set,
			copy.operandId,
			self.operandId
		)
		return copy


class RemoteBool(RemoteIntegral[bool]):
	_isTypeInstruction = lowLevel.InstructionType.IsBool
	_newInstruction = lowLevel.InstructionType.NewBool
	_ctype = c_bool
	LocalType = bool
	_defaultInitialValue = False


class CachedRemoteBool(CachedRemoteValue[bool], RemoteBool):
	pass


class RemoteNumber(RemoteIntegral[LocalTypeVar], Generic[LocalTypeVar]):

	@remoteFunc
	def __gt__(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.GreaterThan, other)

	@remoteFunc
	def __lt__(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.LessThan, other)

	@remoteFunc
	def __ge__(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.GreaterThanOrEqual, other)

	@remoteFunc
	def __le__(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.LessThanOrEqual, other)

	def _doBinaryOp(self, instructionType: lowLevel.InstructionType, other: Self) -> Self:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			instructionType,
			resultOperandId,
			self.operandId,
			other.operandId
		)
		return type(self).fromOperandId(self.builder, resultOperandId)

	def _doInplaceOp(self, instructionType: lowLevel.InstructionType, other: Self) -> Self:
		self.builder.addInstruction(
			instructionType,
			self.operandId,
			other.operandId
		)
		return self

	@remoteFunc
	def __add__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryAdd, other)

	@remoteFunc
	def __iadd__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Add, other)

	@remoteFunc
	def __sub__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinarySubtract, other)

	@remoteFunc
	def __isub__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Subtract, other)

	@remoteFunc
	def __mul__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryMultiply, other)

	@remoteFunc
	def __imul__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Multiply, other)

	@remoteFunc
	def __truediv__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryDivide, other)

	@remoteFunc
	def __itruediv__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Divide, other)


class CachedRemotenumber(CachedRemoteValue[LocalTypeVar], RemoteNumber[LocalTypeVar], Generic[LocalTypeVar]):

	def _doInplaceOp(self, instructionType: InstructionType, other: Self) -> Self:
		raise RuntimeError("Cannot perform in-place operations on a const remote number")


class RemoteUint(RemoteNumber[int]):
	_isTypeInstruction = lowLevel.InstructionType.IsUint
	_newInstruction = lowLevel.InstructionType.NewUint
	_ctype = c_ulong
	LocalType = int
	_defaultInitialValue = 0


class CachedRemoteUint(CachedRemoteValue[int], RemoteUint):
	pass


class RemoteInt(RemoteNumber[int]):
	_isTypeInstruction = lowLevel.InstructionType.IsInt
	_newInstruction = lowLevel.InstructionType.NewInt
	_ctype = c_long
	LocalType = int
	_defaultInitialValue = 0


class CachedRemoteInt(CachedRemoteValue[int], RemoteInt):
	pass

class RemoteString(RemoteValue[str]):
	_isTypeInstruction = lowLevel.InstructionType.IsString
	LocalType = str
	_defaultInitialValue = ""

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId, initialValue: str) -> Iterable[InstructionRecord]:
		stringLen = (len(initialValue) + 1)
		stringVal = ctypes.create_unicode_buffer(initialValue)
		yield InstructionRecord(
			lowLevel.InstructionType.NewString,
			operandId,
			c_ulong(stringLen),
			stringVal
		)

	def __init__(self, initialValue: str | None = None):
		if initialValue is None:
			initialValue = ""
		super().__init__(initialValue)

	@remoteFunc
	def __add__(self, other: Self) -> Self:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			resultOperandId,
			self.operandId,
			other.operandId
		)
		return type(self).fromOperandId(self.builder, resultOperandId)

	@remoteFunc
	def __iadd__(self, other: RemoteString) -> Self:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			self.operandId,
			self.operandId,
			other.operandId
		)
		return self


class CachedRemoteString(CachedRemoteValue[str], RemoteString):

	@remoteFunc
	def __iadd__(self, other: RemoteString) -> Self:
		raise RuntimeError("Cannot perform in-place operations on a const remote string")


class RemoteArray(RemoteVariant):

	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewArray,
			operandId
		)

	@remoteFunc
	def append(self, remoteValue: RemoteBaseObject) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArrayAppend,
			self.operandId,
			remoteValue.operandId
		)

	@remoteFunc
	def __setitem__(self, index: RemoteUint | RemoteInt, remoteValue: RemoteBaseObject) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArraySetAt,
			self.operandId,
			index.operandId,
			remoteValue.operandId
		)

	@remoteFunc
	def __getitem__(self, index: RemoteUint | RemoteInt) -> RemoteVariant:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArrayGetAt,
			resultOperandId,
			self.operandId,
			index.operandId
		)
		return RemoteVariant.fromOperandId(self.builder, resultOperandId)

	@remoteFunc
	def remove(self, index: RemoteUint | RemoteInt) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArrayRemoveAt,
			self.operandId,
			index.operandId
		)

	@remoteFunc
	def size(self) -> RemoteUint:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArraySize,
			resultOperandId,
			self.operandId
		)
		return RemoteUint.fromOperandId(self.builder, resultOperandId)


class RemoteGuid(RemoteValue[GUID]):
	_isTypeInstruction = lowLevel.InstructionType.IsGuid
	LocalType = GUID

	@property
	def _defaultInitialValue(self) -> GUID:
		return GUID()


	@classmethod
	def _generateInitInstructions(cls, operandId: OperandId, initialValue: GUID) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewGuid,
			operandId,
			initialValue
		)

	def __init__(self, initialValue: GUID | str):
		if isinstance(initialValue, str):
			initialValue = GUID(initialValue)
		super().__init__(initialValue)


class CachedRemoteGuid(CachedRemoteValue[GUID], RemoteGuid):
	pass


class RemoteExtensionTarget(RemoteVariantSupportedType):

	@remoteFunc
	def isExtensionSupported(self, extensionGuid: RemoteGuid) -> RemoteBool:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.IsExtensionSupported,
			resultOperandId,
			self.operandId,
			extensionGuid.operandId
		)
		return RemoteBool.fromOperandId(self.builder, resultOperandId)

	@remoteFunc
	def callExtension(self, extensionGuid: RemoteGuid, *params: RemoteBaseObject) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.CallExtension,
			self.operandId,
			extensionGuid.operandId,
			c_ulong(len(params)),
			*(p.operandId for p in params)
		)


class RemoteElement(RemoteExtensionTarget, CachedRemoteValue[UIA.IUIAutomationElement]):
	_isTypeInstruction = lowLevel.InstructionType.IsElement
	LocalType = UIA.IUIAutomationElement

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		if section != "imports":
			raise RuntimeError("RemoteElement can only be initialized in the imports section")
		return builder.importElement(self.initialValue)

	@remoteFunc
	def getPropertyValue(
		self,
		propertyId: RemoteInt,
		ignoreDefault: RemoteBool = CachedRemoteBool(False)
	) -> RemoteVariant:
		resultOperandId = self.builder._getNewOperandId()
		self.builder.addInstruction(
			lowLevel.InstructionType.GetPropertyValue,
			resultOperandId,
			self.operandId,
			propertyId.operandId,
			ignoreDefault.operandId
		)
		return RemoteVariant.fromOperandId(self.builder, resultOperandId)


class RemoteTextRange(RemoteExtensionTarget, CachedRemoteValue[UIA.IUIAutomationTextRange]):
	LocalType = UIA.IUIAutomationTextRange

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		if section != "imports":
			raise RuntimeError("RemoteTextRange can only be initialized in the imports section")
		return builder.importTextRange(self.initialValue)


class InstructionList(list[InstructionRecord]):

	_byteCodeCache: bytes | None = None
	_isModified: bool = False
	_metaStringsByInstructionIndex: dict[int, list[str]]

	def __init__(self):
		super().__init__()
		self._metaStringsByInstructionIndex = {}

	def prependMetaString(self, instructionIndex: int, comment: str):
		if instructionIndex not in self._metaStringsByInstructionIndex:
			self._metaStringsByInstructionIndex[instructionIndex] = []
		self._metaStringsByInstructionIndex[instructionIndex].append(comment)

	def getPrependedMetaStrings(self, instructionIndex: int) -> list[str]:
		return self._metaStringsByInstructionIndex.get(instructionIndex, [])

	def addInstructionRecord(self, record: InstructionRecord, section: str = "main") -> int:
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

	_versionBytes: bytes = struct.pack('l', 0)

	def __init__(self, ro: lowLevel.RemoteOperation, remoteLogging: bool = False):
		self._ro = ro
		self._scopeJustExited: RemoteScope | None = None
		sectionNames = ["imports", "constants", "main"]
		self._instructionListBySection: dict[str, InstructionList] = {
			sectionName: InstructionList() for sectionName in sectionNames
		}
		self._remotedArgCache: dict[object, OperandId] = {}
		self.operandIdGen = itertools.count(start=1)
		self._results = None
		self._loggingEnablede = remoteLogging
		if remoteLogging:
			self._log: RemoteString = RemoteString("")
			self._log.bind(self)

	def _getNewOperandId(self) -> OperandId:
		operandId = OperandId(next(self.operandIdGen))
		return operandId

	def getInstructionList(self, section: str) -> InstructionList:
		return self._instructionListBySection[section]

	def addInstruction(
		self,
		instruction: lowLevel.InstructionType,
		*params: _SimpleCData | ctypes.Array | ctypes.Structure,
		section: str = "main"
	):
		record = InstructionRecord(instruction, *params)
		return self.addInstructionRecord(record, section)

	def addInstructionRecord(self, record: InstructionRecord, section: str = "main") -> int:
		instructionsList = self.getInstructionList(section)
		index = instructionsList.addInstructionRecord(record, section)
		self._scopeJustExited = None
		return index

	def _addMetaString(self, metaString: str, section: str):
		instructions = self.getInstructionList(section)
		instructionIndex = len(instructions)
		instructions.prependMetaString(instructionIndex, metaString)

	def addComment(self, comment: str, section: str = "main"):
		self._addMetaString(f"# {comment}", section)

	def addMetaCommand(self, command: str, section: str = "main"):
		self._addMetaString(f"[{command}]", section)

	def importElement(self, element: UIA.IUIAutomationElement) -> OperandId:
		operandId = self._getNewOperandId()
		self.addMetaCommand(f"ImportElement into {operandId}, value {element}", section="imports")
		self._ro.importElement(operandId, element)
		return operandId

	def importTextRange(self, textRange: UIA.IUIAutomationTextRange) -> OperandId:
		operandId = self._getNewOperandId()
		self.addMetaCommand(f"ImportTextRange into {operandId}, value {textRange}", section="imports")
		self._ro.importTextRange(operandId, textRange)
		return operandId

	def getLastInstructionIndex(self, section: str = "main") -> int:
		instructions = self.getInstructionList(section)
		return len(instructions) - 1

	def getNextInstructionIndex(self, section: str = "main") -> int:
		instructions = self.getInstructionList(section)
		return len(instructions)

	def getInstruction(self, instructionIndex: int, section: str = "main") -> InstructionRecord:
		instructions = self.getInstructionList(section)
		return instructions[instructionIndex]

	def lookupInstructionByGlobalIndex(self, instructionIndex: int) -> InstructionRecord:
		instructions = [instruction for instructionList in self._instructionListBySection.values() for instruction in instructionList]
		return instructions[instructionIndex]

	def ifBlock(self, condition: RemoteBool):
		return RemoteIfBlockBuilder(self, condition)

	def elseBlock(self):
		return RemoteElseBlockBuilder(self)

	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool]):
		return RemoteWhileBlockBuilder(self, conditionBuilderFunc)

	def breakLoop(self):
		self.addInstruction(lowLevel.InstructionType.BreakLoop)

	def continueLoop(self):
		self.addInstruction(lowLevel.InstructionType.ContinueLoop)

	def tryBlock(self):
		return RemoteTryBlockBuilder(self)

	def catchBlock(self):
		return RemoteCatchBlockBuilder(self)

	def setOperationStatus(self, status: RemoteInt):
		status.bind(self)
		self.addInstruction(
			lowLevel.InstructionType.SetOperationStatus,
			status.operandId
		)

	def getOperationStatus(self) -> RemoteInt:
		resultOperandId = self._getNewOperandId()
		self.addInstruction(
			lowLevel.InstructionType.GetOperationStatus,
			resultOperandId
		)
		return RemoteInt.fromOperandId(self, resultOperandId)

	def halt(self):
		self.addInstruction(lowLevel.InstructionType.Halt)

	def _getLogOperandId(self) -> OperandId:
		return self._log.operandId

	def logMessage(self, *strings: str | RemoteString) -> None:
		if not self._loggingEnablede:
			return
		self.addComment("Begin logMessage code")
		lastIndex = len(strings) - 1
		requiresNewLine = True
		for index, string in enumerate(strings):
			if index == lastIndex and isinstance(string, str):
				string += "\n"
				requiresNewLine = False
			if not isinstance(string, RemoteString):
				string = CachedRemoteString(string)
			self._log += cast(RemoteString, string)
		if requiresNewLine:
			self._log += CachedRemoteString("\n")
		self.addComment("End logMessage code")

	def dumpInstructions(self) -> str:
		output = "--- Instructions start ---\n"
		globalInstructionIndex = 0
		for sectionName, instructions in self._instructionListBySection.items():
			output += f"{sectionName}:\n"
			for localInstructionIndex, instruction in enumerate(instructions):
				comments = instructions.getPrependedMetaStrings(localInstructionIndex)
				for comment in comments:
					output += f"{comment}\n"
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


class RemoteScope(_RemoteBase):

	def __init__(self, builder: RemoteOperationBuilder):
		self.bind(builder)

	def __enter__(self):
		self.builder._scopeJustExited = None

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder._scopeJustExited = self


class RemoteIfBlockBuilder(RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, condition: RemoteBool):
		super().__init__(remoteOpBuilder)
		self._condition = condition

	def __enter__(self, silent: bool = False):
		self._silent = silent
		super().__enter__()
		self._conditionInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.ForkIfFalse,
			self._condition.operandId,
			RelativeOffset(1),  # offset updated in Else method
		)
		if not silent:
			self.builder.addComment("If block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._conditionInstructionIndex
		conditionInstruction = self.builder.getInstruction(self._conditionInstructionIndex)
		conditionInstruction.params[1].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)
		if not self._silent:
			self.builder.addComment("End of if block body")


class RemoteElseBlockBuilder(RemoteScope):

	def __enter__(self):
		if not isinstance(self.builder._scopeJustExited, RemoteIfBlockBuilder):
			raise RuntimeError("Else block not directly preceded by If block")
		ifScope = self.builder._scopeJustExited
		super().__enter__()
		conditionInstruction = self.builder.getInstruction(ifScope._conditionInstructionIndex)
		# add a final jump instruction to the previous if block to skip over the else block.
		self.builder.addComment("Jump over else block")
		self._jumpInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		# increment the false offset of the previous if block to take the new jump instruction into account.
		conditionInstruction.params[1].value += 1
		self.builder.addComment("Else block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of else block body")
		# update the jump instruction to jump to the real end of the else block.
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self.builder.getInstruction(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class RemoteWhileBlockBuilder(RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, conditionBuilderFunc: Callable[[], RemoteBool]):
		super().__init__(remoteOpBuilder)
		self._conditionBuilderFunc = conditionBuilderFunc

	def __enter__(self):
		super().__enter__()
		# Add a new loop block instruction to start the while loop
		self._newLoopBlockInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.NewLoopBlock,
			RelativeOffset(1),  # offset updated in __exit__ method
			RelativeOffset(1)
		)
		# Generate the loop condition instructions and enter the if block.
		self.builder.addComment("Loop condition")
		condition = self._conditionBuilderFunc()
		self._ifBlock = self.builder.ifBlock(condition)
		self._ifBlock.__enter__(silent=True)
		self.builder.addComment("Loop block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of loop block body")
		# Add a jump instruction to the end of the body to jump back to the start of the loop block.
		self.builder.addComment("Jump back to loop condition")
		relativeContinueOffset = self._newLoopBlockInstructionIndex - self.builder.getLastInstructionIndex()
		self.builder.addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(relativeContinueOffset)
		)
		# Complete the if block.
		self._ifBlock.__exit__(exc_type, exc_val, exc_tb)
		# Add an end loop block instruction after the if block.
		self.builder.addInstruction(
			lowLevel.InstructionType.EndLoopBlock,
		)
		# Update the break offset of the new loop block instruction to jump to after the end loop block instruction.
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeBreakOffset = nextInstructionIndex - self._newLoopBlockInstructionIndex
		newLoopBlockInstruction = self.builder.getInstruction(self._newLoopBlockInstructionIndex)
		newLoopBlockInstruction.params[0].value = relativeBreakOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class RemoteTryBlockBuilder(RemoteScope):

	def __enter__(self):
		super().__enter__()
		self._newTryBlockInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.NewTryBlock,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		super().__enter__()
		self.builder.addComment("Try block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of try block body")
		# Add an end try block instruction after the try block.
		self.builder.addInstruction(
			lowLevel.InstructionType.EndTryBlock,
		)
		# Update the catchoffset of the new try block instruction to jump to after the end try block instruction.
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeCatchOffset = nextInstructionIndex - self._newTryBlockInstructionIndex
		newTryBlockInstruction = self.builder.getInstruction(self._newTryBlockInstructionIndex)
		newTryBlockInstruction.params[0].value = relativeCatchOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class RemoteCatchBlockBuilder(RemoteScope):

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder):
		super().__init__(remoteOpBuilder)

	def __enter__(self):
		if not isinstance(self.builder._scopeJustExited, RemoteTryBlockBuilder):
			raise RuntimeError("Catch block not directly preceded by Try block")
		tryScope = self.builder._scopeJustExited
		super().__enter__()
		# Add a jump instruction directly after the try block to skip over the catch block.
		self.builder.addComment("Jump over catch block")
		self._jumpInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.Fork,
			RelativeOffset(1),  # offset updated in __exit__ method
		)
		# Increment the catch offset of the try block to take the new jump instruction into account.
		newTryBlockInstruction = self.builder.getInstruction(tryScope._newTryBlockInstructionIndex)
		newTryBlockInstruction.params[0].value += 1
		e = self.builder.getOperationStatus()
		self.builder.setOperationStatus(CachedRemoteInt(0))
		self.builder.addComment("Catch block body")
		return e

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of catch block body")
		# Update the jump instruction to jump to the real end of the catch block.
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self.builder.getInstruction(self._jumpInstructionIndex)
		jumpInstruction.params[0].value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)
