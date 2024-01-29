# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	Any,
	ClassVar,
	Generator,
	ContextManager,
	Self,
	Callable,
	Concatenate,
	ParamSpec,
	Iterable,
	Generic,
	TypeVar,
	cast
)
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


class _InstructionBase:
	opCode: ClassVar[lowLevel.InstructionType]

	@property
	def params(self) -> dict[str, Any]:
		raise NotImplementedError()

	def getByteCode(self) -> bytes:
		byteCode = struct.pack('l', self.opCode.value)
		for param in self.params.values():
			if isinstance(param, RemoteBaseObject):
				param = param.operandId
			paramBytes = (c_char * ctypes.sizeof(param)).from_address(ctypes.addressof(param)).raw
			byteCode += paramBytes
		return byteCode

	def dumpInstruction(self) -> str:
		output = f"{self.opCode.name}"
		for paramName, param in self.params.items():
			paramOutput = f"{paramName}="
			if isinstance(param, ctypes.Array) and param._type_ == c_wchar:
				paramOutput += f"c_wchar_array({repr(param.value)})"
			else:
				paramOutput += f"{param}"
			output += f"\n\t{paramOutput}"
		return output


@dataclass
class Instruction(_InstructionBase):
	opCode: lowLevel.InstructionType
	_params: dict[str, RemoteBaseObject | _SimpleCData | ctypes.Array | ctypes.Structure]

	def __init__(
		self,
		opCode: lowLevel.InstructionType,
		**kwargs: RemoteBaseObject | _SimpleCData | ctypes.Array | ctypes.Structure
	):
		self.opCode = opCode
		self._params = kwargs

	@property
	def params(self):
		return self._params


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

	def __init__(self, builder: RemoteOperationBuilder):
		self._builderRef = weakref.ref(builder)


_remoteFunc_self = TypeVar('_remoteFunc_self', bound=_RemoteBase)
_remoteFunc_paramSpec = ParamSpec('_remoteFunc_paramSpec')
_remoteFunc_return = TypeVar('_remoteFunc_return')


class _BaseRemoteFuncWrapper:

	def generateArgsKwargsString(self, *args, **kwargs):
		argsString = ", ".join(map(repr, args))
		kwargsString = ", ".join(f"{key}={repr(val)}" for key, val in kwargs.items())
		return f"({', '.join([argsString, kwargsString])})"

	def _execRawFunc(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
		funcSelf: _remoteFunc_self,
		*args: _remoteFunc_paramSpec.args,
		**kwargs: _remoteFunc_paramSpec.kwargs
	) -> _remoteFunc_return:
		main = funcSelf.builder.getInstructionList('main')
		main.addComment(
			f"Entering {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}"
		)
		res = func(funcSelf, *args, **kwargs)
		main.addComment(f"Exiting {func.__qualname__}")
		return res

	def __call__(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return]:
		@functools.wraps(func)
		def wrapper(
			funcSelf: _remoteFunc_self,
			*args: _remoteFunc_paramSpec.args,
			**kwargs: _remoteFunc_paramSpec.kwargs
		) -> _remoteFunc_return:
			return self._execRawFunc(func, funcSelf, *args, **kwargs)
		return wrapper


class RemoteMethodWrapper(_BaseRemoteFuncWrapper):

	_mutable: bool

	def __init__(self, mutable: bool = False):
		self._mutable = mutable

	def _execRawFunc(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
		funcSelf: _remoteFunc_self,
		*args: _remoteFunc_paramSpec.args,
		**kwargs: _remoteFunc_paramSpec.kwargs
	) -> _remoteFunc_return:
		if self._mutable and not funcSelf._mutable:
			raise RuntimeError(f"{funcSelf.__class__.__name__} is not mutable")
		return super()._execRawFunc(func, funcSelf, *args, **kwargs)


remoteMethod = RemoteMethodWrapper()
remoteMethod_mutable = RemoteMethodWrapper(mutable=True)


class RemoteContextManager(_BaseRemoteFuncWrapper):

	def __call__(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], Generator[_remoteFunc_return, None, None]]
	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], ContextManager[_remoteFunc_return]]:
		contextFunc = contextlib.contextmanager(func)
		return super().__call__(contextFunc)

	@contextlib.contextmanager
	def _execRawFunc(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], ContextManager[_remoteFunc_return]],
		funcSelf: _remoteFunc_self,
		*args: _remoteFunc_paramSpec.args,
		**kwargs: _remoteFunc_paramSpec.kwargs
	) -> Generator[_remoteFunc_return, None, None]:
		main = funcSelf.builder.getInstructionList('main')
		main.addComment(
			f"Entering context manager {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}"
		)
		with func(funcSelf, *args, **kwargs) as val:
			main.addComment("Yielding to outer scope") 
			yield val
			main.addComment(f"Reentering context manager {func.__qualname__}")
		funcSelf.builder.getInstructionList().addComment(f"Exiting context manager {func.__qualname__}")


remoteContextManager = RemoteContextManager()


class RemoteBaseObject(_RemoteBase):

	_operandId: OperandId | None = None
	_sectionForInitInstructions: str | None = None
	_defaultSectionForInitInstructions: str = "main"

	def __init__(self):
		pass

	def bind(self, builder: RemoteOperationBuilder, operandId: OperandId):
		super().__init__(builder)
		self._operandId = operandId

	@classmethod
	def fromOperandId(cls, builder: RemoteOperationBuilder, operandId: OperandId) -> Self:
		obj = cls()
		obj.bind(builder, operandId)
		return obj

	@classmethod
	def createNew(cls, builder: RemoteOperationBuilder, section: str | None = None) -> Self:
		obj = cls()
		obj.bind(builder, builder._getNewOperandId())
		obj._initOperand(section)
		return obj

	def isBound(self, toBuilder: RemoteOperationBuilder) -> bool:
		if self._builderRef is None:
			return False
		builder = self._builderRef()
		if builder is None:
			raise RuntimeError("Builder has died")
		if builder is not toBuilder:
			raise RuntimeError("Builder mismatch")
		return True

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
		output = ""
		if self._sectionForInitInstructions == "imports":
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

	@property
	def sectionForInitInstructions(self) -> str:
		return self._sectionForInitInstructions or self._defaultSectionForInitInstructions

	def _generateInitInstructions(self) -> Iterable[Instruction]:
		raise NotImplementedError()

	def _initOperand(self, section: str | None = None):
		if section is None:
			section = self._defaultSectionForInitInstructions
		instructionList = self.builder.getInstructionList(section)
		for instruction in self._generateInitInstructions():
			instructionList.addInstructionObject(instruction)

	@remoteMethod
	def stringify(self) -> RemoteString:
		result = RemoteString.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.Stringify,
			result=result,
			target=self
		)
		return result


LocalTypeVar = TypeVar('LocalTypeVar')


class RemoteVariantSupportedType(RemoteBaseObject, Generic[LocalTypeVar]):

	_isTypeInstruction: lowLevel.InstructionType
	LocalType: Type[LocalTypeVar] | None = None
	_initialValue: LocalTypeVar | None = None

	def _generateDefaultInitialValue(self) -> LocalTypeVar:
		if self.LocalType is None:
			raise TypeError("LocalType not set")
		return self.LocalType()

	def __init__(self, initialValue: LocalTypeVar | None = None, const=False):
		if initialValue is not None:
			if self.LocalType is None:
				raise TypeError(f"{type(self).__name__} does not support an initial value")
			if not isinstance(initialValue, self.LocalType):
				raise TypeError(f"initialValue must be of type {self.LocalType.__name__} not {type(initialValue).__name__}")
		self._initialValue = initialValue
		self._mutable = not const

	@classmethod
	def createNew(cls, builder: RemoteOperationBuilder, initialValue: LocalTypeVar | None = None, section: str | None = None, const: bool = False) -> Self:
		obj = cls(initialValue, const=const)
		obj.bind(builder, builder._getNewOperandId())
		obj._initOperand(section)
		return obj

	@classmethod
	def ensureRemote(cls, builder: RemoteOperationBuilder, obj: Self | LocalTypeVar) -> Self:
		if isinstance(obj, cls):
			if not obj.isBound(builder):
				obj.bind(builder, builder._getNewOperandId())
				obj._initOperand()
			return obj
		if cls.LocalType is not None:
			if not isinstance(obj, cls.LocalType):
				raise TypeError(f"obj must be of type {cls.LocalType.__name__} not {type(obj).__name__}")
			RemoteType = cls
		else:
			RemoteType = _LocalTypeToRemoteType[type(obj)]
			if not issubclass(RemoteType, cls):
				raise TypeError(f"The RemoteType of {type(obj).__name__} is {RemoteType.__name__} which is not a subclass of {cls.__name__}")
		cacheKey = (RemoteType, obj)
		cachedRemoteObj = builder._remotedArgCache.get(cacheKey)
		if cachedRemoteObj is not None:
			if not isinstance(cachedRemoteObj, RemoteType):
				raise RuntimeError(f"Cache entry for {cacheKey} is not of type {RemoteType.__name__}")
			return cast(RemoteType, cachedRemoteObj)
		remoteObj = RemoteType.createNew(builder, obj, section="globals", const=True)
		builder._remotedArgCache[cacheKey] = remoteObj
		return remoteObj

	@property
	def initialValue(self) -> LocalTypeVar:
		if self._initialValue is not None:
			return self._initialValue
		return self._generateDefaultInitialValue()

	@remoteMethod_mutable
	def set(self, other: Self | LocalTypeVar):
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.Set,
			target=self,
			value=type(self).ensureRemote(self.builder, other)
		)

	@remoteMethod
	def copy(self) -> Self:
		copy = type(self).fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.Set,
			result=copy,
			target=self
		)
		return copy

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self | LocalTypeVar) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.Compare,
			result=result,
			target=self,
			other=type(self).ensureRemote(self.builder, other),
			comparison=_makeCtypeIntEnum(lowLevel.ComparisonType)(comparisonType)
		)
		return result

	@remoteMethod
	def __eq__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.Equal, other)

	@remoteMethod
	def __ne__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.NotEqual, other)

	def __repr__(self) -> str:
		output = super().__repr__()
		if not self._mutable:
			output += f" with cached value {repr(self.initialValue)}"
		return output


class RemoteVariant(RemoteVariantSupportedType):

	def _generateInitInstructions(self) -> Iterable[Instruction]:
		yield Instruction(
			lowLevel.InstructionType.NewNull,
			result=self.operandId
		)

	def _isType(self, RemoteClass: Type[RemoteVariantSupportedType]) -> RemoteBool:
		if not issubclass(RemoteClass, RemoteVariantSupportedType):
			raise TypeError("remoteClass must be a subclass of RemoteBaseObject")
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			RemoteClass._isTypeInstruction,
			result=result,
			target=self
		)
		return result

	@remoteMethod
	def isNull(self) -> RemoteBool:
		return self._isType(RemoteNull)

	@remoteMethod
	def isBool(self) -> RemoteBool:
		return self._isType(RemoteBool)

	@remoteMethod
	def isInt(self) -> RemoteBool:
		return self._isType(RemoteInt)

	@remoteMethod
	def isUint(self) -> RemoteBool:
		return self._isType(RemoteUint)

	@remoteMethod
	def isFloat(self) -> RemoteBool:
		return self._isType(RemoteFloat)

	@remoteMethod
	def isString(self) -> RemoteBool:
		return self._isType(RemoteString)

	@remoteMethod
	def isGuid(self) -> RemoteBool:
		return self._isType(RemoteGuid)

	@remoteMethod
	def isArray(self) -> RemoteBool:
		return self._isType(RemoteArray)

	@remoteMethod
	def isElement(self) -> RemoteBool:
		return self._isType(RemoteElement)

	_TV_asType = TypeVar('_TV_asType', bound=RemoteVariantSupportedType)

	def asType(self, remoteClass: Type[_TV_asType]) -> _TV_asType:
		return remoteClass.fromOperandId(self.builder, self.operandId)


class RemoteNull(RemoteVariantSupportedType):
	_isTypeInstruction = lowLevel.InstructionType.IsNull

	def _generateInitInstructions(self,) -> Iterable[Instruction]:
		yield Instruction(
			lowLevel.InstructionType.NewNull,
			result=self.operandId
		)


class RemoteIntegral(RemoteVariantSupportedType[LocalTypeVar], Generic[LocalTypeVar]):

	_newInstruction: lowLevel.InstructionType
	_ctype: Type[_SimpleCData]

	def _generateInitInstructions(
		self) -> Iterable[Instruction]:
		yield Instruction(
			self._newInstruction,
			result=self.operandId,
			value=self._ctype(self.initialValue)
		)


class RemoteBool(RemoteIntegral[bool]):
	_isTypeInstruction = lowLevel.InstructionType.IsBool
	_newInstruction = lowLevel.InstructionType.NewBool
	_ctype = c_bool
	LocalType = bool
	_defaultInitialValue = False

	@remoteMethod
	def inverse(self) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.BoolNot,
			result=result,
			target=self
		)
		return result

	def _doBinaryBoolOp(self, instructionType: lowLevel.InstructionType, other: Self | bool) -> Self:
		result = type(self).fromOperandId(self.builder, self.builder._getNewOperandId())
		main = self.builder.getInstructionList()
		main.addInstruction(
			instructionType,
			result=result,
			left=self,
			right=RemoteBool.ensureRemote(self.builder, other)
		)
		return result

	@remoteMethod
	def __and__(self, other: Self | bool) -> RemoteBool:
		return self._doBinaryBoolOp(lowLevel.InstructionType.BoolAnd, other)

	@remoteMethod
	def __rand__(self, other: Self | bool) -> RemoteBool:
		return self._doBinaryBoolOp(lowLevel.InstructionType.BoolAnd, other)

	@remoteMethod
	def __or__(self, other: Self | bool) -> RemoteBool:
		return self._doBinaryBoolOp(lowLevel.InstructionType.BoolOr, other)

	@remoteMethod
	def __ror__(self, other: Self | bool) -> RemoteBool:
		return self._doBinaryBoolOp(lowLevel.InstructionType.BoolOr, other)


class RemoteNumber(RemoteIntegral[LocalTypeVar], Generic[LocalTypeVar]):

	@remoteMethod
	def __gt__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.GreaterThan, other)

	@remoteMethod
	def __lt__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.LessThan, other)

	@remoteMethod
	def __ge__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.GreaterThanOrEqual, other)

	@remoteMethod
	def __le__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.LessThanOrEqual, other)

	def _doBinaryOp(self, instructionType: lowLevel.InstructionType, other: Self | LocalTypeVar) -> Self:
		result = type(self).fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			instructionType,
			result=result,
			left=self,
			right=type(self).ensureRemote(self.builder, other)
		)
		return result

	@remoteMethod
	def __add__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryAdd, other)

	@remoteMethod
	def __sub__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinarySubtract, other)

	@remoteMethod
	def __mul__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryMultiply, other)

	@remoteMethod
	def __truediv__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryDivide, other)

	@remoteMethod
	def __radd__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryAdd, other)

	@remoteMethod
	def __rsub__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinarySubtract, other)

	@remoteMethod
	def __rmul__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryMultiply, other)

	@remoteMethod
	def __rtruediv__(self, other: Self | LocalTypeVar) -> Self:
		return self._doBinaryOp(lowLevel.InstructionType.BinaryDivide, other)

	def _doInplaceOp(self, instructionType: lowLevel.InstructionType, other: Self | LocalTypeVar) -> Self:
		self.builder.getInstructionList().addInstruction(
			instructionType,
			target=self,
			other=type(self).ensureRemote(self.builder, other)
		)
		return self

	@remoteMethod_mutable
	def __iadd__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Add, other)

	@remoteMethod_mutable
	def __isub__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Subtract, other)

	@remoteMethod_mutable
	def __imul__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Multiply, other)

	@remoteMethod_mutable
	def __itruediv__(self, other: Self | LocalTypeVar) -> Self:
		return self._doInplaceOp(lowLevel.InstructionType.Divide, other)


class RemoteIntBase(RemoteNumber[int]):
		pass


class RemoteUint(RemoteIntBase):
	_isTypeInstruction = lowLevel.InstructionType.IsUint
	_newInstruction = lowLevel.InstructionType.NewUint
	_ctype = c_ulong
	LocalType = int
	_defaultInitialValue = 0


class RemoteInt(RemoteIntBase):
	_isTypeInstruction = lowLevel.InstructionType.IsInt
	_newInstruction = lowLevel.InstructionType.NewInt
	_ctype = c_long
	LocalType = int
	_defaultInitialValue = 0


_RemoteIntEnum_LocalTypeVar = TypeVar('_RemoteIntEnum_LocalTypeVar', bound=enum.IntEnum)


class RemoteIntEnum(RemoteInt, Generic[_RemoteIntEnum_LocalTypeVar]):
	localType = enum.IntEnum
	_enumType: _RemoteIntEnum_LocalTypeVar

	def __init__(self, initialValue: _RemoteIntEnum_LocalTypeVar, const=False):
		if not isinstance(initialValue, enum.IntEnum):
			raise TypeError(f"initialValue must be of type {enum.IntEnum.__name__} not {type(initialValue).__name__}")
		self.LocalType = type(initialValue)
		self._ctype = _makeCtypeIntEnum(type(initialValue))
		super().__init__(initialValue, const=const)

	@classmethod
	def ensureRemote(cls, builder: RemoteOperationBuilder, obj: RemoteIntEnum[_RemoteIntEnum_LocalTypeVar] | _RemoteIntEnum_LocalTypeVar) -> RemoteIntEnum[_RemoteIntEnum_LocalTypeVar]:
		remoteObj = super().ensureRemote(builder, cast(Any, obj))
		return cast(RemoteIntEnum[_RemoteIntEnum_LocalTypeVar], remoteObj)

	@remoteMethod
	def set(self, other: Self | _RemoteIntEnum_LocalTypeVar):
		super().set(other)


class RemoteFloat(RemoteNumber[float]):
	_isTypeInstruction = lowLevel.InstructionType.IsDouble
	_newInstruction = lowLevel.InstructionType.NewDouble
	_ctype = ctypes.c_double
	LocalType = float
	_defaultInitialValue = 0.0


class RemoteString(RemoteVariantSupportedType[str]):
	_isTypeInstruction = lowLevel.InstructionType.IsString
	LocalType = str
	_defaultInitialValue = ""

	def _generateInitInstructions(self) -> Iterable[Instruction]:
		initialValue = self.initialValue
		stringLen = (len(initialValue) + 1)
		stringVal = ctypes.create_unicode_buffer(initialValue)
		yield Instruction(
			lowLevel.InstructionType.NewString,
			result=self.operandId,
			length=c_ulong(stringLen),
			value=stringVal
		)

	def _concat(self, other: Self | str) -> Self:
		result = type(self).fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			result=result,
			left=self,
			right=type(self).ensureRemote(self.builder, other)
		)
		return result

	@remoteMethod
	def __add__(self, other: Self | str) -> RemoteString:
		return self._concat(other)

	@remoteMethod
	def __radd__(self, other: Self | str) -> RemoteString:
		return self._concat(other)

	@remoteMethod_mutable
	def __iadd__(self, other: RemoteString) -> Self:
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteStringConcat,
			result=self,
			left=self,
			right=other
		)
		return self

	@remoteMethod_mutable
	def set(self, other: Self | str):
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.NewString,
			result=self,
			length=c_ulong(0)
		)
		self += other

	@remoteMethod
	def copy(self) -> Self:
		copy = type(self).fromOperandId(self.builder, self.builder._getNewOperandId())
		copy += self
		return copy


class RemoteArray(RemoteVariantSupportedType):

	def _generateInitInstructions(self) -> Iterable[Instruction]:
		yield Instruction(
			lowLevel.InstructionType.NewArray,
			result=self.operandId
		)

	@remoteMethod
	def __getitem__(self, index: RemoteUint | RemoteInt | int) -> RemoteVariant:
		result = RemoteVariant.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteArrayGetAt,
			result=result,
			target=self,
			index=RemoteIntBase.ensureRemote(self.builder, index)
		)
		return result

	@remoteMethod
	def size(self) -> RemoteUint:
		result = RemoteUint.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteArraySize,
			result=result,
			target=self
		)
		return result

	@remoteMethod_mutable
	def append(self, value: RemoteBaseObject| int | float | str) -> None:
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteArrayAppend,
			target=self,
			value=RemoteVariantSupportedType.ensureRemote(self.builder, value)
		)

	@remoteMethod_mutable
	def __setitem__(self, index: RemoteUint | RemoteInt | int, value: RemoteBaseObject | int | float | str) -> None:
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteArraySetAt,
			target=self,
			index=RemoteIntBase.ensureRemote(self.builder, index),
			value=RemoteVariantSupportedType.ensureRemote(self.builder, value)
		)

	@remoteMethod_mutable
	def remove(self, index: RemoteUint | RemoteInt | int) -> None:
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.RemoteArrayRemoveAt,
			target=self,
			index=RemoteIntBase.ensureRemote(self.builder, index)
		)


class RemoteGuid(RemoteVariantSupportedType[GUID]):
	_isTypeInstruction = lowLevel.InstructionType.IsGuid
	LocalType = GUID

	@property
	def _defaultInitialValue(self) -> GUID:
		return GUID()

	def __init__(self, initialValue: GUID | str | None = None, const=False):
		if isinstance(initialValue, str):
			initialValue = GUID(initialValue)
		super().__init__(initialValue, const=const)

	def _generateInitInstructions(self) -> Iterable[Instruction]:
		yield Instruction(
			lowLevel.InstructionType.NewGuid,
			result=self.operandId,
			value=self.initialValue
		)


class RemoteExtensionTarget(RemoteVariantSupportedType[LocalTypeVar], Generic[LocalTypeVar]):

	def _generateInitInstructions(self) -> Iterable[Instruction]:
		yield Instruction(
			lowLevel.InstructionType.NewNull,
			result=self.operandId
		)

	@remoteMethod
	def isNull(self):
		variant = RemoteVariant.fromOperandId(self.builder, self.operandId)
		return variant.isNull()

	@remoteMethod
	def isExtensionSupported(self, extensionGuid: RemoteGuid | GUID) -> RemoteBool:
		result = RemoteBool.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.IsExtensionSupported,
			result=result,
			target=self,
			extensionId=RemoteGuid.ensureRemote(self.builder, extensionGuid)
		)
		return result

	@remoteMethod_mutable
	def callExtension(self, extensionGuid: RemoteGuid | GUID, *params: RemoteBaseObject | int | float |str) -> None:
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.CallExtension,
			target=self,
			extensionId=RemoteGuid.ensureRemote(self.builder, extensionGuid),
			paramCount=c_ulong(len(params)),
			**{
				f"param{index}": RemoteVariantSupportedType.ensureRemote(self.builder, param)
				for index, param in enumerate(params, start=1)
			}
		)


class RemoteElement(RemoteExtensionTarget[POINTER(UIA.IUIAutomationElement)]):
	_isTypeInstruction = lowLevel.InstructionType.IsElement
	LocalType = POINTER(UIA.IUIAutomationElement)

	def _initOperand(self, section: str | None = None):
		if self._initialValue is None:
			return super()._initOperand(section)
		if section != "imports":
			raise RuntimeError("Can only initialize element operand in the imports section")
		self.builder.importElement(self.operandId, self.initialValue)

	def getPropertyValue(
		self,
		propertyId: RemoteIntEnum[lowLevel.PropertyId] | lowLevel.PropertyId,
		ignoreDefault: RemoteBool | bool = False
	) -> RemoteVariant:
		result = RemoteVariant.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.GetPropertyValue,
			result=result,
			target=self,
			propertyId=RemoteIntEnum.ensureRemote(self.builder, propertyId),
			ignoreDefault=RemoteBool.ensureRemote(self.builder, ignoreDefault)
		)
		return result

	def _navigate(self, navigationDirection: lowLevel.NavigationDirection) -> RemoteElement:
		result = RemoteElement.fromOperandId(self.builder, self.builder._getNewOperandId())
		main = self.builder.getInstructionList()
		main.addInstruction(
			lowLevel.InstructionType.Navigate,
			result=result,
			target=self,
			direction=RemoteIntEnum.ensureRemote(self.builder, navigationDirection)
		)
		return result

	@remoteMethod
	def getParentElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.Parent)

	@remoteMethod
	def getFirstChildElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.FirstChild)

	@remoteMethod
	def getLastChildElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.LastChild)

	@remoteMethod
	def getNextSiblingElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.NextSibling)

	@remoteMethod
	def getPreviousSiblingElement(self) -> RemoteElement:
		return self._navigate(lowLevel.NavigationDirection.PreviousSibling)


class RemoteTextRange(RemoteExtensionTarget[POINTER(UIA.IUIAutomationTextRange)]):
	LocalType = POINTER(UIA.IUIAutomationTextRange)

	def _initOperand(self, section: str | None = None):
		if self._initialValue is None:
			return super()._initOperand(section)
		if section != "imports":
			raise RuntimeError("Can only initialize textRange  operand in the imports section")
		self.builder.importTextRange(self.operandId, self.initialValue)

	@remoteMethod
	def clone(self):
		result = RemoteTextRange.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeClone,
			result=result,
			target=self
		)
		return result

	@remoteMethod
	def getEnclosingElement(self) -> RemoteElement:
		result = RemoteElement.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeGetEnclosingElement,
			result=result,
			target=self
		)
		return result

	@remoteMethod
	def getText(self, maxLength: RemoteInt | int) -> RemoteString:
		result = RemoteString.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeGetText,
			result=result,
			target=self,
			maxLength=RemoteInt.ensureRemote(self.builder, maxLength)
		)
		return result

	@remoteMethod_mutable
	def expandToEnclosingUnit(self, unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit):
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeExpandToEnclosingUnit,
			target=self,
			unit=RemoteIntEnum.ensureRemote(self.builder, unit)
		)

	@remoteMethod_mutable
	def moveEndpointByUnit(self, endpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint, unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit, count: RemoteInt | int):
		result = RemoteInt.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeMoveEndpointByUnit,
			result=result,
			target=self,
			endpoint=RemoteIntEnum.ensureRemote(self.builder, endpoint),
			unit=RemoteIntEnum.ensureRemote(self.builder, unit),
			count=RemoteInt.ensureRemote(self.builder, count)
		)
		return result

	@remoteMethod_mutable
	def moveEndpointByRange(self, srcEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint, otherRange: RemoteTextRange, otherEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint):
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeMoveEndpointByRange,
			target=self,
			srcEndpoint=RemoteIntEnum.ensureRemote(self.builder, srcEndpoint),
			otherRange=otherRange,
			otherEndpoint=RemoteIntEnum.ensureRemote(self.builder, otherEndpoint)
		)

	@remoteMethod
	def getAttributeValue(self, attributeId: RemoteIntEnum[lowLevel.AttributeId] | lowLevel.AttributeId) -> RemoteVariant:
		result = RemoteVariant.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeGetAttributeValue,
			result=result,
			target=self,
			attributeId=RemoteIntEnum.ensureRemote(self.builder, attributeId)
		)
		return result

	@remoteMethod
	def compareEndpoints(
		self,
		thisEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
		otherRange: RemoteTextRange,
		otherEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint
	) -> RemoteInt:
		result = RemoteInt.fromOperandId(self.builder, self.builder._getNewOperandId())
		self.builder.getInstructionList().addInstruction(
			lowLevel.InstructionType.TextRangeCompareEndpoints,
			result=result,
			target=self,
			thisEndpoint=RemoteIntEnum.ensureRemote(self.builder, thisEndpoint),
			otherRange=otherRange,
			otherEndpoint=RemoteIntEnum.ensureRemote(self.builder, otherEndpoint)
		)
		return result

	def getLogicalAdapter(self, reverse=False) -> RemoteTextRangeLogicalAdapter:
		obj = RemoteTextRangeLogicalAdapter(self.builder, self, reverse=reverse)
		return obj


class _RemoteTextRangeEndpoint(_RemoteBase):

	def __init__(
		self,
		  builder: RemoteOperationBuilder,
		  textRangeLA: RemoteTextRangeLogicalAdapter, isStart: bool
	  ):
		super().__init__(builder)
		self._la = textRangeLA
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
		unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit ,
		count: RemoteInt | int
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

	def __init__(
		self,
		builder: RemoteOperationBuilder,
		textRange: RemoteTextRange, reverse=False
	):
		super().__init__(builder)
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
		obj = _RemoteTextRangeEndpoint(self.builder, self, isStart=True)
		return obj

	@start.setter
	def start(self, value: _RemoteTextRangeEndpoint):
		self.start.moveTo(value)

	@property
	def end(self) -> _RemoteTextRangeEndpoint:
		obj = _RemoteTextRangeEndpoint(self.builder, self, isStart=False)
		return obj

	@end.setter
	def end(self, value: _RemoteTextRangeEndpoint):
		self.end.moveTo(value)

	def clone(self):
		return self.textRange.clone().getLogicalAdapter(self.isReversed)


class InstructionList:

	_all: list[_InstructionBase | str]
	_instructions: list[_InstructionBase]

	def __init__(self):
		super().__init__()
		self._all = []
		self._instructions = []

	def _addMetaString(self, metaString: str):
		self._all.append(metaString)

	def addComment(self, comment: str):
		self._addMetaString(f"# {comment}")

	def addInstructionObject(self, instruction: _InstructionBase) -> int:
		self._all.append(instruction)
		self._instructions.append(instruction)
		return len(self._instructions) - 1

	def addInstruction(
		self,
		instruction: lowLevel.InstructionType,
		**params: RemoteBaseObject | _SimpleCData | ctypes.Array | ctypes.Structure,
	) -> int:
		return self.addInstructionObject(Instruction(instruction, **params))

	def addMetaCommand(self, command: str):
		self._addMetaString(f"[{command}]")

	def getByteCode(self):
		byteCode = b''
		for instruction in self._instructions:
			byteCode += instruction.getByteCode()
		return byteCode

	def getInstruction(self, index) -> Instruction:
		return self._instructions[index]

	def getInstructionCount(self) -> int:
		return len(self._instructions)

	def iterItems(self) -> Iterable[_InstructionBase | str]:
		return iter(self._all)

	def dumpInstructions(self) -> str:
		output = ""
		for item in self.iterItems():
			if isinstance(item, _InstructionBase):
				output += item.dumpInstruction()
			elif isinstance(item, str):
				output += item
			output += "\n"
		return output


class RemoteOperationBuilder:

	_versionBytes: bytes = struct.pack('l', 0)
	_sectionNames = ["imports", "globals", "main"]

	def __init__(self, ro: lowLevel.RemoteOperation, remoteLogging: bool = False):
		self._ro = ro
		self._instructionListBySection: dict[str, InstructionList] = {
			sectionName: InstructionList() for sectionName in self._sectionNames
		}
		self._remotedArgCache: dict[object, RemoteBaseObject] = {}
		self.operandIdGen = itertools.count(start=1)
		self._results = None
		self._loggingEnablede = remoteLogging
		if remoteLogging:
			self.getInstructionList('globals').addComment("Logger object")
			self._log: RemoteString = RemoteString()
			self._log.bind(self, self._getNewOperandId())
			self._log._initOperand()

	def _getNewOperandId(self) -> OperandId:
		operandId = OperandId(next(self.operandIdGen))
		return operandId

	def getInstructionList(self, section: str = "main") -> InstructionList:
		return self._instructionListBySection[section]

	def importElement(self, operandId: OperandId, element: UIA.IUIAutomationElement):
		self.getInstructionList('imports').addMetaCommand(f"ImportElement into {operandId}, value {element}")
		self._ro.importElement(operandId, element)

	def importTextRange(self, operandId: OperandId, textRange: UIA.IUIAutomationTextRange):
		self.getInstructionList('imports').addMetaCommand(f"ImportTextRange into {operandId}, value {textRange}")
		self._ro.importTextRange(operandId, textRange)

	def lookupInstructionByGlobalIndex(self, index: int) -> Instruction:
		baseIndex = 0
		for instructionList in self._instructionListBySection.values():
			instructionCount = instructionList.getInstructionCount()
			if baseIndex + instructionCount > index:
				return instructionList.getInstruction(index - baseIndex)
			baseIndex += instructionCount
		raise IndexError(f"Instruction index {index} out of range")

	def getLogOperandId(self) -> OperandId | None:
		if self._loggingEnablede:
			return self._log.operandId

	def dumpInstructions(self) -> str:
		output = ""
		globalInstructionIndex = 0
		for sectionName, instructionList in self._instructionListBySection.items():
			output += f"{sectionName}:\n"
			for item in instructionList.iterItems():
				if isinstance(item, _InstructionBase):
					output += f"{globalInstructionIndex}: "
					globalInstructionIndex += 1
					output += item.dumpInstruction()
				elif isinstance(item, str):
					output += item
				output += "\n"
		return output


class _TypedInstruction(_InstructionBase):

	@property
	def params(self):
		return vars(self)


@dataclass
class Instruction_Fork(_TypedInstruction):
	opCode = lowLevel.InstructionType.Fork
	jumpTo: RelativeOffset


@dataclass
class Instruction_IfFalse(_TypedInstruction):
	opCode = lowLevel.InstructionType.ForkIfFalse
	condition: RemoteBool
	branch: RelativeOffset


@dataclass
class Instruction_NewLoopBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewLoopBlock
	breakBranch: RelativeOffset
	continueBranch: RelativeOffset


@dataclass
class Instruction_NewTryBlock(_TypedInstruction):
	opCode = lowLevel.InstructionType.NewTryBlock
	catchBranch: RelativeOffset


class RemoteAPI(_RemoteBase):

	_newObject_RemoteType = TypeVar('_newObject_RemoteType', bound=RemoteVariantSupportedType)
	def _newObject(self, RemoteType: Type[_newObject_RemoteType], value: Any) -> _newObject_RemoteType :
		if isinstance(value, RemoteType):
			return value.copy()
		return RemoteType.createNew(self.builder, value)

	def newUint(self, value: RemoteUint | int = 0) -> RemoteUint:
		if isinstance(value, RemoteUint):
			return value.copy()
		return RemoteUint.createNew(self.builder, value)

	def newInt(self, value: RemoteInt | int = 0) -> RemoteInt:
		if isinstance(value, RemoteInt):
			return value.copy()
		return RemoteInt.createNew(self.builder, value)

	def newFloat(self, value: RemoteFloat | float = 0.0) -> RemoteFloat:
		if isinstance(value, RemoteFloat):
			return value.copy()
		return RemoteFloat.createNew(self.builder, value)

	def newString(self, value: RemoteString | str = "") -> RemoteString:
		if isinstance(value, RemoteString):
			return value.copy()
		return RemoteString.createNew(self.builder, value)

	def newBool(self, value: RemoteBool | bool = False) -> RemoteBool:
		if isinstance(value, RemoteBool):
			return value.copy()
		return RemoteBool.createNew(self.builder, value)

	def newGuid(self, value: RemoteGuid | GUID | str | None = None) -> RemoteGuid:
		if isinstance(value, RemoteGuid):
			return value.copy()
		elif value is None:
			realValue = GUID()
		elif isinstance(value, str):
			realValue = GUID(value)
		else:
			realValue = value
		return RemoteGuid.createNew(self.builder, realValue)

	def newVariant(self) -> RemoteVariant:
		return RemoteVariant.createNew(self.builder)

	def newArray(self) -> RemoteArray:
		return RemoteArray.createNew(self.builder)

	def newNullElement(self) -> RemoteElement:
		return RemoteElement.createNew(self.builder)

	def newNullTextRange(self) -> RemoteTextRange:
		return RemoteTextRange.createNew(self.builder)

	def getOperationStatus(self) -> RemoteInt:
		main = self.builder.getInstructionList('main')
		result = RemoteInt.fromOperandId(self.builder, self.builder._getNewOperandId())
		main.addInstruction(
			lowLevel.InstructionType.GetOperationStatus,
			result=result
		)
		return result

	def setOperationStatus(self, status: RemoteInt | int):
		main = self.builder.getInstructionList('main')
		main.addInstruction(
			lowLevel.InstructionType.SetOperationStatus,
			status=RemoteInt.ensureRemote(self.builder, status)
		)

	_scopeInstructionJustExited: _InstructionBase | None = None

	@contextlib.contextmanager
	def ifBlock(self, condition: RemoteBool, silent=False):
		main = self.builder.getInstructionList('main')
		conditionInstruction = Instruction_IfFalse(
			condition=condition,
			branch=RelativeOffset(1),  # offset updated after yield 
		)
		conditionInstructionIndex = main.addInstructionObject(conditionInstruction)
		if not silent:
			main.addComment("If block body")
		yield
		if not silent:
			main.addComment("End of if block body")
		nextInstructionIndex = main.getInstructionCount()
		conditionInstruction.branch = RelativeOffset(nextInstructionIndex - conditionInstructionIndex)
		self._scopeInstructionJustExited = conditionInstruction

	@contextlib.contextmanager
	def elseBlock(self, silent=False):
		scopeInstructionJustExited = self._scopeInstructionJustExited
		if not isinstance(scopeInstructionJustExited, Instruction_IfFalse):
			raise RuntimeError("Else block not directly preceded by If block")
		main = self.builder.getInstructionList('main')
		ifConditionInstruction = cast(Instruction_IfFalse, scopeInstructionJustExited)
		# add a final jump instruction to the previous if block to skip over the else block.
		if not silent:
			main.addComment("Jump over else block")
		jumpElseInstruction = Instruction_Fork(RelativeOffset(1))  # offset updated after yield
		jumpElseInstructionIndex = main.addInstructionObject(jumpElseInstruction)
		# increment the false offset of the previous if block to take the new jump instruction into account.
		ifConditionInstruction.branch.value += 1
		if not silent:
			main.addComment("Else block body")
		yield
		if not silent:
			main.addComment("End of else block body")
		# update the jump instruction to jump to the real end of the else block.
		nextInstructionIndex = main.getInstructionCount()
		jumpElseInstruction.jumpTo = RelativeOffset(nextInstructionIndex - jumpElseInstructionIndex)
		self._scopeInstructionJustExited = None

	def continueLoop(self):
		main = self.builder.getInstructionList('main')
		main.addInstruction(lowLevel.InstructionType.ContinueLoop)

	def breakLoop(self):
		main = self.builder.getInstructionList('main')
		main.addInstruction(lowLevel.InstructionType.BreakLoop)

	@contextlib.contextmanager
	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool], silent=False):
		main = self.builder.getInstructionList('main')
		# Add a new loop block instruction to start the while loop
		loopBlockInstruction = Instruction_NewLoopBlock(
			breakBranch=RelativeOffset(1),  # offset updated after yield
			continueBranch=RelativeOffset(1)
		)
		loopBlockInstructionIndex = main.addInstructionObject(loopBlockInstruction)
		# generate the loop condition.
		# This must be evaluated lazily via a callable
		# because any instructions that produce the condition bool
		# must be added inside the loop body.
		condition = conditionBuilderFunc()
		with self.ifBlock(condition, silent=True):
			# Add the loop body
			if not silent:
				main.addComment("While block body")
			yield
			if not silent:
				main.addComment("End of while block body")
			self.continueLoop()
		main.addInstruction(lowLevel.InstructionType.EndLoopBlock)
		# update the loop break offset to jump to the end of the loop body
		nextInstructionIndex = main.getInstructionCount()
		loopBlockInstruction.breakBranch = RelativeOffset(nextInstructionIndex - loopBlockInstructionIndex)
		self._scopeInstructionJustExited = loopBlockInstruction

	@contextlib.contextmanager
	def tryBlock(self, silent=False):
		main = self.builder.getInstructionList('main')
		# Add a new try block instruction to start the try block
		tryBlockInstruction = Instruction_NewTryBlock(
			catchBranch=RelativeOffset(1),  # offset updated after yield
		)
		tryBlockInstructionIndex = main.addInstructionObject(tryBlockInstruction)
		# Add the try block body
		if not silent:
			main.addComment("Try block body")
		yield
		if not silent:
			main.addComment("End of try block body")
		main.addInstruction(lowLevel.InstructionType.EndTryBlock)
		# update the try block catch offset to jump to the end of the try block body
		nextInstructionIndex = main.getInstructionCount()
		tryBlockInstruction.catchBranch = RelativeOffset(nextInstructionIndex - tryBlockInstructionIndex)
		self._scopeInstructionJustExited = tryBlockInstruction

	@contextlib.contextmanager
	def catchBlock(self, silent=False):
		scopeInstructionJustExited = self._scopeInstructionJustExited
		if not isinstance(scopeInstructionJustExited, Instruction_NewTryBlock):
			raise RuntimeError("Catch block not directly preceded by Try block")
		main = self.builder.getInstructionList('main')
		tryBlockInstruction = cast(Instruction_NewTryBlock, scopeInstructionJustExited)
		# add a final jump instruction to the previous try block to skip over the catch block.
		if not silent:
			main.addComment("Jump over catch block")
		jumpCatchInstruction = Instruction_Fork(
			jumpTo=RelativeOffset(1)  # offset updated after yield
		)
		jumpCatchInstructionIndex = main.addInstructionObject(jumpCatchInstruction)
		# increment the catch offset of the previous try block to take the new jump instruction into account.
		tryBlockInstruction.catchBranch.value += 1
		# fetch the error status that caused the catch
		status = self.getOperationStatus()
		# reset the error status to 0
		self.setOperationStatus(0)
		# Add the catch block body
		if not silent:
			main.addComment("Catch block body")
		yield status
		if not silent:
			main.addComment("End of catch block body")
		# update the jump instruction to jump to the real end of the catch block.
		nextInstructionIndex = main.getInstructionCount()
		jumpCatchInstruction.jumpTo = RelativeOffset(nextInstructionIndex - jumpCatchInstructionIndex)
		self._scopeInstructionJustExited = None

	def halt(self):
		main = self.builder.getInstructionList('main')
		main.addInstruction(lowLevel.InstructionType.Halt)

	def logRuntimeMessage(self, *args: str | RemoteBaseObject) -> None:
		if not self.builder._loggingEnablede:
			return
		main = self.builder.getInstructionList('main')
		logObj = self.builder._log
		main.addComment("Begin logMessage code")
		lastIndex = len(args) - 1
		requiresNewLine = True
		for index, arg in enumerate(args):
			if index == lastIndex and isinstance(arg, str):
				arg += "\n"
				requiresNewLine = False
			if isinstance(arg, RemoteString):
				string = arg
			elif isinstance(arg, RemoteBaseObject):
				string = arg.stringify()
			else: # arg is str
				string = self.newString(arg)
			logObj += string
		if requiresNewLine:
			logObj += "\n"
		main.addComment("End logMessage code")

	def addCompiletimeComment(self, comment: str):
		main = self.builder.getInstructionList('main')
		main.addComment(comment)


_LocalTypeToRemoteType: dict[Type[object], Type[RemoteVariantSupportedType]] = {
	bool: RemoteBool,
	int: RemoteInt,
	float: RemoteFloat,
	str: RemoteString,
	GUID: RemoteGuid,
	POINTER(UIA.IUIAutomationElement): RemoteElement,
	POINTER(UIA.IUIAutomationTextRange): RemoteTextRange,
}
