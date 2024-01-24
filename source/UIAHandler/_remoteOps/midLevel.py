# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	Any,
	Generator,
	ContextManager,
	Self,
	Callable,
	Concatenate,
	Iterable,
	Generic,
	TypeVar,
	cast
)
import types
import inspect
import functools
import contextlib
import weakref
import ctypes
from ctypes import (
	_SimpleCData,
	c_long,
	c_ulong,
	c_char,
	c_wchar,
	c_bool,
	POINTER
)
from comtypes import GUID
from dataclasses import dataclass
import os
import struct
import itertools
import enum
from UIAHandler import UIA
from . import lowLevel
from .lowLevel import OperandId, RelativeOffset


class c_long_enum(c_long):
	_enumType: Type[enum.IntEnum]

	def __repr__(self):
		return f"{c_long.__name__} enum {repr(self._enumType(self.value))}"


_ctypeIntEnumCache: dict[Type[enum.IntEnum], Type[_SimpleCData]] = {}


def _makeCtypeIntEnum(enumType: Type[enum.IntEnum]) -> Type[_SimpleCData]:
	cachedCls = _ctypeIntEnumCache.get(enumType)
	if cachedCls is not None:
		return cachedCls

	class cls(c_long_enum):
		_enumType = enumType

	cls.__name__ = f"{cls.__name__}_{enumType.__name__}"
	cast(Type[_SimpleCData], cls)
	_ctypeIntEnumCache[enumType] = cls
	return cls


_RemoteEnumCache: dict[Type[enum.IntEnum], Type[RemoteInt]] = {}


def _makeRemoteEnum(enumType: Type[enum.IntEnum]) -> Type[RemoteInt]:
	cachedCls = _RemoteEnumCache.get(enumType)
	if cachedCls is not None:
		return cachedCls

	class cls(RemoteInt):
		LocalType = enumType
		_ctype = _makeCtypeIntEnum(enumType)

	cls.__name__ = f"RemoteEnum_{enumType.__name__}"
	cast(Type[RemoteInt], cls)
	_RemoteEnumCache[enumType] = cls
	return cls


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


class Record:

	def dumpRecord(self) -> str:
		raise NotImplementedError()


@dataclass
class MetaStringRecord(Record):
	metaString: str

	def dumpRecord(self) -> str:
		return self.metaString


@dataclass
class InstructionRecord(Record):
	instructionType: lowLevel.InstructionType
	params: list[RemoteBaseObject | _SimpleCData | ctypes.Array | ctypes.Structure]
	paramNames: list[str]
	locationString: str | None = None

	def __init__(
		self, instructionType: lowLevel.InstructionType,
		**kwargs: RemoteBaseObject | _SimpleCData | ctypes.Array | ctypes.Structure
	):
		self.instructionType = instructionType
		self.params = list(kwargs.values())
		self.paramNames = list(kwargs.keys())

	def getByteCode(self) -> bytes:
		byteCode = struct.pack('l', self.instructionType)
		for param in self.params:
			if isinstance(param, RemoteBaseObject):
				param = param.operandId
			paramBytes = (c_char * ctypes.sizeof(param)).from_address(ctypes.addressof(param)).raw
			byteCode += paramBytes
		return byteCode

	def dumpRecord(self) -> str:
		output = f"{self.instructionType.name}"
		for index, param in enumerate(self.params):
			paramName = self.paramNames[index]
			paramOutput = f"{paramName}="
			if isinstance(param, ctypes.Array) and param._type_ == c_wchar:
				paramOutput += f"c_wchar_array({repr(param.value)})"
			else:
				paramOutput += f"{param}"
			output += f"\n\t{paramOutput}"
		return output


class _RemoteBase:

	_builderRef: weakref.ReferenceType[RemoteOperationBuilder] | None = None
	_mutable: bool = True

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


def processArg(func: Callable, arg: object, paramInfo: inspect.Parameter) -> object:
	if paramInfo.default is not inspect.Parameter.empty:
		return arg
	if isinstance(arg, _RemoteBase):
		return arg
	if isinstance(arg, enum.IntEnum):
		return RemoteIntEnum(arg, const=True)
	RemoteType = _LocalTypeToRemoteType.get(type(arg))
	if RemoteType is None:
		raise TypeError(f"Argument {repr(arg)} of function {func.__qualname__} has no Remote equivalent")
	if issubclass(RemoteType, CacheableRemoteValue):
		return RemoteType(arg, const=True)
	else:
		return RemoteType(arg)
	raise TypeError(f"Argument {repr(arg)} must be or convertable to a Remote type")


def processArgs(func: Callable, funcSelf, *args, **kwargs):
	funcSig = inspect.signature(func, eval_str=True)
	boundFuncSig = funcSig.bind(funcSelf, *args, **kwargs)
	processedArgs = []
	processedKwargs = {}
	for index, (name, val) in enumerate(boundFuncSig.arguments.items()):
		if index == 0:
			continue
		paramInfo = funcSig.parameters[name]
		if paramInfo.kind == paramInfo.VAR_POSITIONAL:
			for subVal in val:
				processedArg = processArg(func, subVal, paramInfo)
				processedArgs.append(processedArg)
		elif paramInfo.kind == paramInfo.VAR_KEYWORD:
			for subName, subVal in val.items():
				processedArg = processArg(func, subVal, paramInfo)
				processedKwargs[subName] = processedArg
		else:
			processedArg = processArg(func, val, paramInfo)
			processedArgs.append(processedArg)
	return processedArgs, processedKwargs


_remoteFunc_self = TypeVar('_remoteFunc_self', bound=_RemoteBase)
_remoteFunc_return = TypeVar('_remoteFunc_return')


class RemoteFuncWrapper:

	_mutable: bool

	def __init__(self, mutable: bool = False):
		self._mutable = mutable

	def generateArgsKwargsString(self, *args, **kwargs):
		argsString = ", ".join(map(repr, args))
		kwargsString = ", ".join(f"{key}={repr(val)}" for key, val in kwargs.items())
		return f"({', '.join([argsString, kwargsString])})"

	def _execRawFunc(self, func, funcSelf, *args, **kwargs):
		funcSelf.builder.addComment(
			f"Entering function {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}"
		)
		res = func(funcSelf, *args, **kwargs)
		funcSelf.builder.addComment(f"Exiting function {func.__qualname__}")
		return res

	def __call__(
		self,
		func: Callable[Concatenate[_remoteFunc_self, ...], _remoteFunc_return],
	) -> Callable[Concatenate[_remoteFunc_self, ...], _remoteFunc_return]:
		@functools.wraps(func)
		def wrapper(funcSelf: _remoteFunc_self, *args, **kwargs):
			if self._mutable and not funcSelf._mutable:
				raise RuntimeError(f"{funcSelf.__class__.__name__} is not mutable")
			processedArgs, processedKwargs = processArgs(func, funcSelf, *args, **kwargs)
			for processedArg in processedArgs:
				if isinstance(processedArg, _RemoteBase):
					processedArg.bind(funcSelf.builder)
			for processedArg in processedKwargs.values():
				if isinstance(processedArg, _RemoteBase):
					processedArg.bind(funcSelf.builder)
			return self._execRawFunc(func, funcSelf, *processedArgs, **processedKwargs)
		return wrapper


remoteFunc = RemoteFuncWrapper()
remoteFunc_mutable = RemoteFuncWrapper(mutable=True)


class RemoteContextManager(RemoteFuncWrapper):

	def __call__(
		self,
		func: Callable[Concatenate[_remoteFunc_self, ...], Generator[_remoteFunc_return, None, None]]
	) -> Callable[Concatenate[_remoteFunc_self, ...], ContextManager[_remoteFunc_return]]:
		contextFunc = contextlib.contextmanager(func)
		return super().__call__(contextFunc)

	@contextlib.contextmanager
	def _execRawFunc(self, func, funcSelf, *args, **kwargs) -> Generator[Any, None, None]:
		funcSelf.builder.addComment(
			f"Entering context manager {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}"
		)
		with func(funcSelf, *args, **kwargs) as val:
			funcSelf.builder.addComment("Yielding back to caller")
			yield val
			funcSelf.builder.addComment(f"Reentering context manager {func.__qualname__}")
		funcSelf.builder.addComment(f"Exiting context manager {func.__qualname__}")


remoteContextManager = RemoteContextManager()


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

	def __bool__(self) -> bool:
		raise TypeError(f"Cannot convert {self.__class__.__name__} to bool")

	def __repr__(self) -> str:
		builder = self._builderRef() if self._builderRef is not None else None
		if builder is None:
			return f"unbound {self.__class__.__name__}"
		output = ""
		if self._section == "imports":
			output += "imported "
		if not self._mutable:
			output += "const "
		output += f"{self.__class__.__name__} at {self.operandId}"
		return output

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

	def _generateInitInstructions(self, operandId: OperandId) -> Iterable[InstructionRecord]:
		raise NotImplementedError()

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		operandId = builder._getNewOperandId()
		for record in self._generateInitInstructions(operandId):
			builder.addInstructionRecord(record, section=section)
		return operandId

	_section: str | None = None
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
		if section is None:
			section = self._defaultSectionForInitInstructions
		operandId = self._initOperand(builder, section)
		super().bind(builder)
		self._operandId = operandId
		self._section = section

	@remoteFunc
	def stringify(self) -> RemoteString:
		result = RemoteString.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.Stringify,
			result=result,
			target=self
		)
		return result


class RemoteVariantSupportedType(RemoteBaseObject):

	_isTypeInstruction: lowLevel.InstructionType


class RemoteNull(RemoteVariantSupportedType):
	_isTypeInstruction = lowLevel.InstructionType.IsNull

	def _generateInitInstructions(self, operandId: OperandId) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewNull,
			result=operandId
		)


class RemoteSetable(RemoteVariantSupportedType):

	@remoteFunc_mutable
	def set(self, other: Self):
		self.builder.addInstruction(
			lowLevel.InstructionType.Set,
			target=self,
			value=other
		)

	@remoteFunc
	def copy(self) -> Self:
		copy = type(self)()
		copy.bind(self.builder)
		self.builder.addInstruction(
			lowLevel.InstructionType.Set,
			result=copy,
			target=self
		)
		return copy


class RemoteVariant(RemoteBaseObject):

	def _generateInitInstructions(self, operandId: OperandId) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewNull,
			result=operandId
		)

	def _isType(self, RemoteClass: Type[RemoteVariantSupportedType]) -> RemoteBool:
		if not issubclass(RemoteClass, RemoteVariantSupportedType):
			raise TypeError("remoteClass must be a subclass of RemoteBaseObject")
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			RemoteClass._isTypeInstruction,
			result=result,
			target=self
		)
		return result

	@remoteFunc
	def isNull(self) -> RemoteBool:
		return self._isType(RemoteNull)

	@remoteFunc
	def isBool(self) -> RemoteBool:
		return self._isType(RemoteBool)

	@remoteFunc
	def isInt(self) -> RemoteBool:
		return self._isType(RemoteInt)

	@remoteFunc
	def isUint(self) -> RemoteBool:
		return self._isType(RemoteUint)

	@remoteFunc
	def isFloat(self) -> RemoteBool:
		return self._isType(RemoteFloat)

	@remoteFunc
	def isString(self) -> RemoteBool:
		return self._isType(RemoteString)

	@remoteFunc
	def isGuid(self) -> RemoteBool:
		return self._isType(RemoteGuid)

	@remoteFunc
	def isArray(self) -> RemoteBool:
		return self._isType(RemoteArray)

	@remoteFunc
	def isElement(self) -> RemoteBool:
		return self._isType(RemoteElement)

	_TV_asType = TypeVar('_TV_asType', bound=RemoteVariantSupportedType)

	def asType(self, remoteClass: Type[_TV_asType]) -> _TV_asType:
		return remoteClass.fromOperandId(self.builder, self.operandId)


LocalTypeVar = TypeVar('LocalTypeVar')


class RemoteValue(RemoteSetable, RemoteVariantSupportedType, Generic[LocalTypeVar]):

	LocalType: Type[LocalTypeVar]
	_initialValue: LocalTypeVar | None = None

	def _generateDefaultInitialValue(self) -> LocalTypeVar:
		return self.LocalType()

	def __init__(self, initialValue: LocalTypeVar | None = None, const=False):
		if initialValue is not None and not isinstance(initialValue, self.LocalType):
			raise TypeError(
				f"initialValue must be of type {self.LocalType.__name__} not {type(initialValue).__name__}"
			)
		super().__init__()
		self._mutable = not const
		if const:
			self._defaultSectionForInitInstructions = "globals"
		self._initialValue = initialValue

	def _generateInitInstructions(
		self,
		operandId: OperandId,
		initialValue: LocalTypeVar
	) -> Iterable[InstructionRecord]:
		raise NotImplementedError()

	@property
	def initialValue(self) -> LocalTypeVar:
		if self._initialValue is not None:
			return self._initialValue
		return self._generateDefaultInitialValue()

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		operandId = builder._getNewOperandId()
		for record in self._generateInitInstructions(operandId, self.initialValue):
			builder.addInstructionRecord(record, section=section)
		return operandId

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.Compare,
			result=result,
			target=self,
			other=other,
			comparison=_makeCtypeIntEnum(lowLevel.ComparisonType)(comparisonType)
		)
		return result

	@remoteFunc
	def __eq__(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.Equal, other)

	@remoteFunc
	def __ne__(self, other: Self) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.NotEqual, other)


class CacheableRemoteValue(RemoteValue[LocalTypeVar], Generic[LocalTypeVar]):

	def __init__(self, initialValue: LocalTypeVar | None = None, const=False):
		super().__init__(initialValue)
		self._mutable = not const
		if const:
			self._defaultSectionForInitInstructions = "globals"

	def _generateCacheKey(self):
		return (type(self), self.initialValue)

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		if self._mutable:
			return super()._initOperand(builder, section)
		cacheKey = self._generateCacheKey()
		cachedOperandId = builder._remotedArgCache.get(cacheKey)
		if cachedOperandId is not None:
			return cachedOperandId
		operandId = super()._initOperand(builder, section)
		if not self._mutable:
			builder._remotedArgCache[cacheKey] = operandId
		return operandId

	def __repr__(self) -> str:
		output = super().__repr__()
		if not self._mutable:
			output += f" with cached value {repr(self.initialValue)}"
		return output


class RemoteIntegral(CacheableRemoteValue[LocalTypeVar], Generic[LocalTypeVar]):

	_newInstruction: lowLevel.InstructionType
	_ctype: Type[_SimpleCData]

	def _generateInitInstructions(
		self,
		operandId: OperandId,
		initialValue: LocalTypeVar
	) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			self._newInstruction,
			result=operandId,
			value=self._ctype(initialValue)
		)


class RemoteBool(RemoteIntegral[bool]):
	_isTypeInstruction = lowLevel.InstructionType.IsBool
	_newInstruction = lowLevel.InstructionType.NewBool
	_ctype = c_bool
	LocalType = bool
	_defaultInitialValue = False

	@remoteFunc
	def inverse(self) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.BoolNot,
			result=result,
			target=self
		)
		return result

	@remoteFunc
	def __and__(self, other: Self) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.BoolAnd,
			result=result,
			left=self,
			right=other
		)
		return result

	@remoteFunc
	def __or__(self, other: Self) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.BoolOr,
			result=result,
			left=self,
			right=other
		)
		return result


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
		result = type(self).fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			instructionType,
			result=result,
			left=self,
			right=other
		)
		return result

	@remoteFunc
	def __add__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryAdd, other)

	@remoteFunc
	def __sub__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinarySubtract, other)

	@remoteFunc
	def __mul__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryMultiply, other)

	@remoteFunc
	def __truediv__(self, other: Self) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryDivide, other)

	def _doInplaceOp(self, instructionType: lowLevel.InstructionType, other: Self) -> Self:
		self.builder.addInstruction(
			instructionType,
			target=self,
			other=other
		)
		return self

	@remoteFunc_mutable
	def __iadd__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Add, other)

	@remoteFunc_mutable
	def __isub__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Subtract, other)

	@remoteFunc_mutable
	def __imul__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Multiply, other)

	@remoteFunc_mutable
	def __itruediv__(self, other: Self) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Divide, other)


class RemoteUint(RemoteNumber[int]):
	_isTypeInstruction = lowLevel.InstructionType.IsUint
	_newInstruction = lowLevel.InstructionType.NewUint
	_ctype = c_ulong
	LocalType = int
	_defaultInitialValue = 0


class RemoteInt(RemoteNumber[int]):
	_isTypeInstruction = lowLevel.InstructionType.IsInt
	_newInstruction = lowLevel.InstructionType.NewInt
	_ctype = c_long
	LocalType = int
	_defaultInitialValue = 0


_RemoteIntEnum_LocalTypeVar = TypeVar('_RemoteIntEnum_LocalTypeVar', bound=enum.IntEnum)


class RemoteIntEnum(RemoteInt, Generic[_RemoteIntEnum_LocalTypeVar]):
	localType = enum.IntEnum
	_enumType: _RemoteIntEnum_LocalTypeVar

	def __init__(self, initialValue: _RemoteIntEnum_LocalTypeVar | None = None, const=False):
		if initialValue is not None:
			self._enumType = cast(_RemoteIntEnum_LocalTypeVar, type(initialValue))
			self._ctype = _makeCtypeIntEnum(type(initialValue))
		elif initialValue is None:
			raise TypeError("initialValue must be given")
		else:
			raise TypeError(f"initialValue must be of type {enum.IntEnum.__name__} not {type(initialValue).__name__}")
		super().__init__(initialValue, const=const)

	def _generateCacheKey(self):
		return (
			type(self),
			self.initialValue.value if isinstance(self.initialValue, enum.IntEnum) else self.initialValue
		)

	@remoteFunc
	def set(self, other: Self):
		if other._enumType is not self._enumType:
			raise TypeError(f"other must be of type {self._enumType.__name__} not {other._enumType.__name__}")
			other = other.value
		super().set(other)


class RemoteFloat(RemoteNumber[float]):
	_isTypeInstruction = lowLevel.InstructionType.IsDouble
	_newInstruction = lowLevel.InstructionType.NewDouble
	_ctype = ctypes.c_double
	LocalType = float
	_defaultInitialValue = 0.0


class RemoteString(CacheableRemoteValue[str]):
	_isTypeInstruction = lowLevel.InstructionType.IsString
	LocalType = str
	_defaultInitialValue = ""

	def _generateInitInstructions(self, operandId: OperandId, initialValue: str) -> Iterable[InstructionRecord]:
		stringLen = (len(initialValue) + 1)
		stringVal = ctypes.create_unicode_buffer(initialValue)
		yield InstructionRecord(
			lowLevel.InstructionType.NewString,
			result=operandId,
			length=c_ulong(stringLen),
			value=stringVal
		)

	def __init__(self, initialValue: str | None = None, const=False):
		if initialValue is None:
			initialValue = ""
		super().__init__(initialValue, const=const)

	@remoteFunc
	def __add__(self, other: Self) -> RemoteString:
		result = RemoteString.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			result=result,
			left=self,
			right=other
		)
		return result

	@remoteFunc_mutable
	def __iadd__(self, other: RemoteString) -> Self:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			result=self,
			left=self,
			right=other
		)
		return self

	@remoteFunc_mutable
	def set(self, other: Self):
		self.builder.addInstruction(
			lowLevel.InstructionType.NewString,
			result=self,
			length=c_ulong(0)
		)
		self += other

	@remoteFunc
	def copy(self) -> Self:
		copy = type(self)()
		copy.bind(self.builder)
		copy += self
		return copy


class RemoteArray(RemoteVariantSupportedType):

	def _generateInitInstructions(self, operandId: OperandId) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewArray,
			result=operandId
		)

	@remoteFunc
	def __getitem__(self, index: RemoteUint | RemoteInt) -> RemoteVariant:
		result = RemoteVariant.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArrayGetAt,
			result=result,
			target=self,
			index=index
		)
		return result

	@remoteFunc
	def size(self) -> RemoteUint:
		result = RemoteUint.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArraySize,
			result=result,
			target=self
		)
		return result

	@remoteFunc_mutable
	def append(self, remoteValue: RemoteBaseObject) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArrayAppend,
			target=self,
			value=remoteValue
		)

	@remoteFunc_mutable
	def __setitem__(self, index: RemoteUint | RemoteInt, remoteValue: RemoteBaseObject) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArraySetAt,
			target=self,
			index=index,
			value=remoteValue
		)

	@remoteFunc_mutable
	def remove(self, index: RemoteUint | RemoteInt) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.RemoteArrayRemoveAt,
			target=self,
			index=index
		)


class RemoteGuid(CacheableRemoteValue[GUID]):
	_isTypeInstruction = lowLevel.InstructionType.IsGuid
	LocalType = GUID

	@property
	def _defaultInitialValue(self) -> GUID:
		return GUID()

	def _generateInitInstructions(self, operandId: OperandId, initialValue: GUID) -> Iterable[InstructionRecord]:
		yield InstructionRecord(
			lowLevel.InstructionType.NewGuid,
			result=operandId,
			value=initialValue
		)

	def __init__(self, initialValue: GUID | str, const=False):
		if isinstance(initialValue, str):
			initialValue = GUID(initialValue)
		super().__init__(initialValue, const=const)


class RemoteExtensionTarget(RemoteVariantSupportedType):

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		operandId = builder._getNewOperandId()
		builder.addInstruction(
			lowLevel.InstructionType.NewNull,
			result=operandId
		)
		return operandId

	@remoteFunc
	def isNull(self):
		return RemoteVariant.fromOperandId(self.builder, self.operandId)._isType(RemoteNull)

	@remoteFunc
	def isExtensionSupported(self, extensionGuid: RemoteGuid) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.IsExtensionSupported,
			result=result,
			target=self,
			extensionId=extensionGuid
		)
		return result

	@remoteFunc_mutable
	def callExtension(self, extensionGuid: RemoteGuid, *params: RemoteBaseObject) -> None:
		self.builder.addInstruction(
			lowLevel.InstructionType.CallExtension,
			target=self,
			extensionId=extensionGuid,
			paramCount=c_ulong(len(params)),
			**{f"param{index}": param for index, param in enumerate(params, start=1)}
		)


class RemoteElement(RemoteExtensionTarget, RemoteValue[POINTER(UIA.IUIAutomationElement)]):
	_isTypeInstruction = lowLevel.InstructionType.IsElement
	LocalType = POINTER(UIA.IUIAutomationElement)

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		if self.initialValue:
			if section != "imports":
				raise RuntimeError("RemoteElement can only be initialized in the imports section")
			return builder.importElement(self.initialValue)
		return super()._initOperand(builder, section)

	@remoteFunc
	def getPropertyValue(
		self,
		propertyId: RemoteInt,
		ignoreDefault: RemoteBool
	) -> RemoteVariant:
		result = RemoteVariant. fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.GetPropertyValue,
			result=result,
			target=self,
			propertyId=propertyId,
			ignoreDefault=ignoreDefault
		)
		return result

	@remoteFunc
	def _navigate(self, navigationDirection: RemoteInt) -> RemoteElement:
		result = RemoteElement.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.Navigate,
			result=result,
			target=self,
			direction=navigationDirection
		)
		return result

	@remoteFunc
	def getParentElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.Parent)

	@remoteFunc
	def getFirstChildElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.FirstChild)

	@remoteFunc
	def getLastChildElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.LastChild)

	@remoteFunc
	def getNextSiblingElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.NextSibling)

	@remoteFunc
	def getPreviousSiblingElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.PreviousSibling)


class RemoteTextRange(RemoteExtensionTarget, RemoteValue[POINTER(UIA.IUIAutomationTextRange)]):
	LocalType = POINTER(UIA.IUIAutomationTextRange)

	def _initOperand(self, builder: RemoteOperationBuilder, section: str) -> OperandId:
		if self.initialValue:
			if section != "imports":
				raise RuntimeError("RemoteTextRange can only be initialized in the imports section")
			return builder.importTextRange(self.initialValue)
		return super()._initOperand(builder, section)

	@remoteFunc
	def clone(self):
		result = RemoteTextRange.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeClone,
			result=result,
			target=self
		)
		return result

	@remoteFunc
	def getEnclosingElement(self) -> RemoteElement:
		result = RemoteElement.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeGetEnclosingElement,
			result=result,
			target=self
		)
		return result

	@remoteFunc
	def getText(self, maxLength: RemoteInt) -> RemoteString:
		result = RemoteString.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeGetText,
			result=result,
			target=self,
			maxLength=maxLength
		)
		return result

	@remoteFunc_mutable
	def expandToEnclosingUnit(self, unit: RemoteInt):
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeExpandToEnclosingUnit,
			target=self,
			unit=unit
		)

	@remoteFunc_mutable
	def moveEndpointByUnit(self, endpoint: RemoteInt, unit: RemoteInt, count: RemoteInt):
		result = RemoteInt.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeMoveEndpointByUnit,
			result=result,
			target=self,
			endpoint=endpoint,
			unit=unit,
			count=count
		)
		return result

	@remoteFunc_mutable
	def moveEndpointByRange(self, srcEndpoint: RemoteInt, otherRange: RemoteTextRange, otherEndpoint: RemoteInt):
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeMoveEndpointByRange,
			target=self,
			srcEndpoint=srcEndpoint,
			otherRange=otherRange,
			otherEndpoint=otherEndpoint
		)

	@remoteFunc
	def getAttributeValue(self, attributeId: RemoteInt) -> RemoteVariant:
		result = RemoteVariant.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeGetAttributeValue,
			result=result,
			target=self,
			attributeId=attributeId
		)
		return result

	@remoteFunc
	def compareEndpoints(
		self, thisEndpoint: RemoteInt, otherRange: RemoteTextRange, otherEndpoint: RemoteInt
	) -> RemoteInt:
		result = RemoteInt.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.addInstruction(
			lowLevel.InstructionType.TextRangeCompareEndpoints,
			result=result,
			target=self,
			thisEndpoint=thisEndpoint,
			otherRange=otherRange,
			otherEndpoint=otherEndpoint
		)
		return result

	def getLogicalAdapter(self, reverse=False) -> RemoteTextRangeLogicalAdapter:
		obj = RemoteTextRangeLogicalAdapter(self, reverse=reverse)
		return obj


class _RemoteTextRangeEndpoint(_RemoteBase):

	def __init__(self, textRangeLA: RemoteTextRangeLogicalAdapter, isStart: bool):
		self._la = textRangeLA
		self.bind(textRangeLA.builder)
		self._endpoint = (
			lowLevel.TextPatternRangeEndpoint.Start
			if isStart ^ self.isReversed
			else lowLevel.TextPatternRangeEndpoint.End
		)

	@property
	def textRange(self: _RemoteTextRangeEndpoint) -> RemoteTextRange:
		return self._la.textRange

	@property
	def isReversed(self: _RemoteTextRangeEndpoint) -> bool:
		return self._la.isReversed

	@property
	def endpoint(self: _RemoteTextRangeEndpoint) -> lowLevel.TextPatternRangeEndpoint:
		return self._endpoint

	def compareWith(self, other: _RemoteTextRangeEndpoint) -> RemoteInt:
		res = self.textRange.compareEndpoints(self.endpoint, other.textRange, other.endpoint)
		if self.isReversed:
			res *= -1
		return res

	def moveTo(self, other: _RemoteTextRangeEndpoint):
		self.textRange.moveEndpointByRange(self.endpoint, other.textRange, other.endpoint)

	def moveByUnit(
		self,
		unit: lowLevel.TextUnit | RemoteIntEnum[lowLevel.TextUnit],
		count: int | RemoteInt
	) -> RemoteInt:
		realCount = (count * -1) if self.isReversed else count
		res = self.textRange.moveEndpointByUnit(self.endpoint, unit, realCount)
		return res

	def __lt__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__lt__(0)

	def __le__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__le__(0)

	def __gt__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__gt__(0)

	def __ge__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__ge__(0)

	def __eq__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other) == 0

	def __ne__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return (self == other).inverse()


class RemoteTextRangeLogicalAdapter(_RemoteBase):

	def __init__(self, textRange: RemoteTextRange, reverse=False):
		self.bind(textRange.builder)
		self._textRange = textRange
		self._isReversed = reverse

	@property
	def textRange(self) -> RemoteTextRange:
		return self._textRange

	@property
	def isReversed(self) -> bool:
		return self._isReversed

	@property
	def start(self) -> _RemoteTextRangeEndpoint:
		obj = _RemoteTextRangeEndpoint(self, isStart=True)
		obj.bind(self.builder)
		return obj

	@start.setter
	def start(self, value: _RemoteTextRangeEndpoint):
		self.start.moveTo(value)

	@property
	def end(self) -> _RemoteTextRangeEndpoint:
		obj = _RemoteTextRangeEndpoint(self, isStart=False)
		obj.bind(self.builder)
		return obj

	@end.setter
	def end(self, value: _RemoteTextRangeEndpoint):
		self.end.moveTo(value)

	def clone(self):
		return self.textRange.clone().getLogicalAdapter(self.isReversed)


class RecordList:

	_allRecords: list[Record]
	_instructionRecords: list[InstructionRecord]

	def __init__(self):
		super().__init__()
		self._allRecords = []
		self._instructionRecords = []

	def addMetaStringRecord(self, record: MetaStringRecord):
		self._allRecords.append(record)

	def addInstructionRecord(self, record: InstructionRecord) -> int:
		self._allRecords.append(record)
		if isinstance(record, InstructionRecord):
			self._instructionRecords.append(record)
		return len(self._instructionRecords) - 1

	def getByteCode(self):
		byteCode = b''
		for instruction in self._instructionRecords:
			byteCode += instruction.getByteCode()
		return byteCode

	def getInstructionRecord(self, index) -> InstructionRecord:
		return self._instructionRecords[index]

	def getInstructionCount(self) -> int:
		return len(self._instructionRecords)

	def iterRecords(self) -> Iterable[Record]:
		return iter(self._allRecords)


class RemoteOperationBuilder:

	_versionBytes: bytes = struct.pack('l', 0)

	def __init__(self, ro: lowLevel.RemoteOperation, remoteLogging: bool = False):
		self._ro = ro
		self._scopeJustExited: RemoteScope | None = None
		sectionNames = ["imports", "globals", "main"]
		self._recordListBySection: dict[str, RecordList] = {
			sectionName: RecordList() for sectionName in sectionNames
		}
		self._remotedArgCache: dict[object, OperandId] = {}
		self.operandIdGen = itertools.count(start=1)
		self._results = None
		self._loggingEnablede = remoteLogging
		if remoteLogging:
			self.addComment("Logger object", section="globals")
			self._log: RemoteString = RemoteString("")
			self._log.bind(self, section="globals")

	def _getNewOperandId(self) -> OperandId:
		operandId = OperandId(next(self.operandIdGen))
		return operandId

	def getRecordList(self, section: str) -> RecordList:
		return self._recordListBySection[section]

	def addInstruction(
		self,
		instruction: lowLevel.InstructionType,
		**params: RemoteBaseObject | _SimpleCData | ctypes.Array | ctypes.Structure,
	):
		record = InstructionRecord(instruction, **params)
		return self.addInstructionRecord(record)

	def addInstructionRecord(self, record: InstructionRecord, section: str = "main") -> int:
		recordList = self.getRecordList(section)
		index = recordList.addInstructionRecord(record)
		self._scopeJustExited = None
		return index

	def _addMetaString(self, metaString: str, section: str):
		record = MetaStringRecord(metaString)
		recordList = self.getRecordList(section)
		recordList.addMetaStringRecord(record)

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
		records = self.getRecordList(section)
		return records.getInstructionCount() - 1

	def getNextInstructionIndex(self, section: str = "main") -> int:
		records = self.getRecordList(section)
		return records.getInstructionCount()

	def getInstruction(self, index: int, section: str = "main") -> InstructionRecord:
		records = self.getRecordList(section)
		return records.getInstructionRecord(index)

	def lookupInstructionByGlobalIndex(self, index: int) -> InstructionRecord:
		baseIndex = 0
		for records in self._recordListBySection.values():
			instructionCount = records.getInstructionCount()
			if baseIndex + instructionCount > index:
				return records.getInstructionRecord(index - baseIndex)
			baseIndex += instructionCount
		raise IndexError(f"Instruction index {index} out of range")

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
			value=status
		)

	def getOperationStatus(self) -> RemoteInt:
		result = RemoteInt.fromOperandId(self, self._getNewOperandId())
		self.addInstruction(
			lowLevel.InstructionType.GetOperationStatus,
			result=result
		)
		return result

	def halt(self):
		self.addInstruction(lowLevel.InstructionType.Halt)

	def getLogOperandId(self) -> OperandId | None:
		if self._loggingEnablede:
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
				string = RemoteString(string)
			self._log += cast(RemoteString, string)
		if requiresNewLine:
			self._log += RemoteString("\n", const=True)
		self.addComment("End logMessage code")

	def dumpInstructions(self) -> str:
		output = "--- Instructions start ---\n"
		globalInstructionIndex = 0
		for sectionName, records in self._recordListBySection.items():
			output += f"{sectionName}:\n"
			for record in records.iterRecords():
				if isinstance(record, InstructionRecord):
					output += f"{globalInstructionIndex}: "
					globalInstructionIndex += 1
				output += record.dumpRecord()
				output += "\n"
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

	def __init__(self, remoteOpBuilder: RemoteOperationBuilder, condition: RemoteBool, silent=False):
		self._silent = silent
		super().__init__(remoteOpBuilder)
		self._condition = condition

	def __enter__(self):
		super().__enter__()
		self._conditionInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.ForkIfFalse,
			condition=self._condition,
			branch=RelativeOffset(1),  # offset updated in Else method
		)
		if not self._silent:
			self.builder.addComment("If block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._conditionInstructionIndex
		conditionInstruction = self.builder.getInstruction(self._conditionInstructionIndex)
		cast(RelativeOffset, conditionInstruction.params[1]).value = relativeJumpOffset
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
			jumpTo=RelativeOffset(1),  # offset updated in __exit__ method
		)
		# increment the false offset of the previous if block to take the new jump instruction into account.
		cast(RelativeOffset, conditionInstruction.params[1]).value += 1
		self.builder.addComment("Else block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of else block body")
		# update the jump instruction to jump to the real end of the else block.
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self.builder.getInstruction(self._jumpInstructionIndex)
		cast(RelativeOffset, jumpInstruction.params[0]).value = relativeJumpOffset
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
			breakOffset=RelativeOffset(1),  # offset updated in __exit__ method
			continueOffset=RelativeOffset(1)
		)
		# Generate the loop condition instructions and enter the if block.
		self.builder.addComment("Loop condition")
		condition = self._conditionBuilderFunc()
		self._ifBlock = RemoteIfBlockBuilder(self.builder, condition, silent=True)
		self._ifBlock.__enter__()
		self.builder.addComment("Loop block body")

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of loop block body")
		# Add a jump instruction to the end of the body to jump back to the start of the loop block.
		self.builder.addComment("Jump back to loop condition")
		relativeContinueOffset = self._newLoopBlockInstructionIndex - self.builder.getLastInstructionIndex()
		self.builder.addInstruction(
			lowLevel.InstructionType.Fork,
			jumpTo=RelativeOffset(relativeContinueOffset)
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
		cast(RelativeOffset, newLoopBlockInstruction.params[0]).value = relativeBreakOffset
		super().__exit__(exc_type, exc_val, exc_tb)


class RemoteTryBlockBuilder(RemoteScope):

	def __enter__(self):
		super().__enter__()
		self._newTryBlockInstructionIndex = self.builder.addInstruction(
			lowLevel.InstructionType.NewTryBlock,
			catch=RelativeOffset(1),  # offset updated in __exit__ method
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
		cast(RelativeOffset, newTryBlockInstruction.params[0]).value = relativeCatchOffset
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
			jumpTo=RelativeOffset(1),  # offset updated in __exit__ method
		)
		# Increment the catch offset of the try block to take the new jump instruction into account.
		newTryBlockInstruction = self.builder.getInstruction(tryScope._newTryBlockInstructionIndex)
		cast(RelativeOffset, newTryBlockInstruction.params[0]).value += 1
		e = self.builder.getOperationStatus()
		self.builder.setOperationStatus(RemoteInt(0, const=True))
		self.builder.addComment("Catch block body")
		return e

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.builder.addComment("End of catch block body")
		# Update the jump instruction to jump to the real end of the catch block.
		nextInstructionIndex = self.builder.getLastInstructionIndex() + 1
		relativeJumpOffset = nextInstructionIndex - self._jumpInstructionIndex
		jumpInstruction = self.builder.getInstruction(self._jumpInstructionIndex)
		cast(RelativeOffset, jumpInstruction.params[0]).value = relativeJumpOffset
		super().__exit__(exc_type, exc_val, exc_tb)


_LocalTypeToRemoteType: dict[Type[object], Type[RemoteValue]] = {
	bool: RemoteBool,
	int: RemoteInt,
	float: RemoteFloat,
	str: RemoteString,
	GUID: RemoteGuid,
	POINTER(UIA.IUIAutomationElement): RemoteElement,
	POINTER(UIA.IUIAutomationTextRange): RemoteTextRange,
}
