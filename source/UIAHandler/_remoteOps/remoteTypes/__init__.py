# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	Any,
	Self,
	ParamSpec,
	Iterable,
	Generic,
	TypeVar,
	cast,
)
from types import NoneType
import ctypes
from ctypes import (
	_SimpleCData,
	c_long,
	c_ulong,
	c_bool,
)
from comtypes import (
	GUID,
	IUnknown,
	COMError,
)
import enum
from UIAHandler import UIA
from .. import lowLevel
from .. import instructions
from .. import builder
from ..remoteFuncWrapper import (
	remoteMethod,
	remoteMethod_mutable,
)
from .. import operation


_remoteFunc_self = TypeVar("_remoteFunc_self", bound=builder._RemoteBase)
_remoteFunc_paramSpec = ParamSpec("_remoteFunc_paramSpec")
_remoteFunc_return = TypeVar("_remoteFunc_return")


LocalTypeVar = TypeVar("LocalTypeVar")


class RemoteBaseObject(builder.Operand, Generic[LocalTypeVar]):
	_IsTypeInstruction: Type[builder.InstructionBase]
	LocalType: Type[LocalTypeVar] | None = None
	_initialValue: LocalTypeVar | None = None
	_executionResult: operation.ExecutionResult | None = None

	def _setExecutionResult(self, executionResult: operation.ExecutionResult):
		self._executionResult = executionResult

	def __bool__(self) -> bool:
		raise TypeError(f"Cannot convert {self.__class__.__name__} to bool")

	def _generateDefaultInitialValue(self) -> LocalTypeVar:
		if self.LocalType is None:
			raise TypeError("LocalType not set")
		return self.LocalType()

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		raise NotImplementedError()

	def _initOperand(self, initialValue: LocalTypeVar | None = None, const: bool = False):
		if initialValue is not None:
			if self.LocalType is None:
				raise TypeError(f"{type(self).__name__} does not support an initial value")
			if not isinstance(initialValue, self.LocalType):
				raise TypeError(
					f"initialValue must be of type {self.LocalType.__name__} "
					f"not {type(initialValue).__name__}",
				)
		self._initialValue = initialValue
		self._mutable = not const
		instructionList = self.rob.getDefaultInstructionList()
		for instruction in self._generateInitInstructions():
			instructionList.addInstruction(instruction)

	@classmethod
	def createNew(
		cls,
		rob: builder.RemoteOperationBuilder,
		initialValue: LocalTypeVar | None = None,
		operandId: lowLevel.OperandId | None = None,
		const: bool = False,
	) -> Self:
		if operandId is None:
			operandId = rob.requestNewOperandId()
		obj = cls(rob, operandId)
		obj._initOperand(initialValue=initialValue, const=const)
		return obj

	@classmethod
	def ensureRemote(cls, rob: builder.RemoteOperationBuilder, obj: Self | LocalTypeVar) -> Self:
		if isinstance(obj, cls):
			if obj.rob is not rob:
				raise RuntimeError(f"Object {obj} is not bound to the given RemoteOperationBuilder")
			return obj
		if cls.LocalType is not None:
			if not isinstance(obj, cls.LocalType):
				raise TypeError(f"obj must be of type {cls.LocalType.__name__} not {type(obj).__name__}")
			RemoteType = cls
		else:
			RemoteType = getRemoteTypeForLocalType(type(obj))
			if not issubclass(RemoteType, cls):
				raise TypeError(
					f"The RemoteType of {type(obj).__name__} is {RemoteType.__name__} "
					f"which is not a subclass of {cls.__name__}",
				)
		cacheKey = (RemoteType, obj)
		cachedRemoteObj = rob._remotedArgCache.get(cacheKey)
		if cachedRemoteObj is not None:
			if not isinstance(cachedRemoteObj, RemoteType):
				raise RuntimeError(f"Cache entry for {cacheKey} is not of type {RemoteType.__name__}")
			rob.getDefaultInstructionList().addComment(
				f"Using cached {cachedRemoteObj} for constant value {repr(obj)}",
			)
			return cast(RemoteType, cachedRemoteObj)
		with rob.overrideDefaultSection("const"):
			remoteObj = RemoteType.createNew(rob, obj, const=True)
		rob.getDefaultInstructionList().addComment(
			f"Using cached {remoteObj} for constant value {repr(obj)}",
		)
		rob._remotedArgCache[cacheKey] = remoteObj
		return remoteObj

	@property
	def initialValue(self) -> LocalTypeVar:
		if self._initialValue is not None:
			return self._initialValue
		return self._generateDefaultInitialValue()

	@property
	def isLocalValueAvailable(self) -> bool:
		return self._executionResult is not None and self._executionResult.hasOperand(self.operandId)

	@property
	def localValue(self) -> LocalTypeVar:
		if self._executionResult is None:
			raise RuntimeError("Operation not executed")
		value = self._executionResult.getOperand(self.operandId)
		return cast(LocalTypeVar, value)

	@remoteMethod_mutable
	def set(self, other: Self | LocalTypeVar):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.Set(
				target=self,
				value=type(self).ensureRemote(self.rob, other),
			),
		)

	@remoteMethod
	def copy(self) -> Self:
		copy = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.Set(
				target=copy,
				value=self,
			),
		)
		return copy

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self | LocalTypeVar) -> RemoteBool:
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.Compare(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
				comparisonType=comparisonType,
			),
		)
		return result

	@remoteMethod
	def __eq__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.Equal, other)

	@remoteMethod
	def __ne__(self, other: Self | LocalTypeVar) -> RemoteBool:
		return self._doCompare(lowLevel.ComparisonType.NotEqual, other)

	@remoteMethod
	def stringify(self) -> RemoteString:
		result = RemoteString(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.Stringify(
				result=result,
				target=self,
			),
		)
		return result


class RemoteVariant(RemoteBaseObject):
	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewNull(
			result=self,
		)

	def _isType(self, RemoteClass: Type[RemoteBaseObject]) -> RemoteBool:
		if not issubclass(RemoteClass, RemoteBaseObject):
			raise TypeError("remoteClass must be a subclass of RemoteBaseObject")
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			RemoteClass._IsTypeInstruction(
				result=result,
				target=self,
			),
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

	_TV_asType = TypeVar("_TV_asType", bound=RemoteBaseObject)

	def asType(self, remoteClass: Type[_TV_asType]) -> _TV_asType:
		return remoteClass(self.rob, self.operandId)


class RemoteNull(RemoteBaseObject):
	_IsTypeInstruction = instructions.IsNull

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewNull(
			result=self,
		)


class RemoteIntegral(RemoteBaseObject[LocalTypeVar], Generic[LocalTypeVar]):
	_NewInstruction: Type[builder.InstructionBase]
	_ctype: Type[_SimpleCData]

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield self._NewInstruction(
			result=self,
			value=self._ctype(self.initialValue),
		)


class RemoteBool(RemoteIntegral[bool]):
	_IsTypeInstruction = instructions.IsBool
	_NewInstruction = instructions.NewBool
	_ctype = c_bool
	LocalType = bool
	_defaultInitialValue = False

	@remoteMethod
	def inverse(self) -> RemoteBool:
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolNot(
				result=result,
				target=self,
			),
		)
		return result

	@remoteMethod
	def __and__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolAnd(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __rand__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolAnd(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __or__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolOr(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __ror__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolOr(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other),
			),
		)
		return result


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

	@remoteMethod
	def __add__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryAdd(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __sub__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinarySubtract(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __mul__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryMultiply(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __truediv__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryDivide(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __mod__(self, other: Self | LocalTypeVar) -> Self:
		return self - (self / other) * other

	@remoteMethod
	def __radd__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryAdd(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __rsub__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinarySubtract(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __rmul__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryMultiply(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __rtruediv__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryDivide(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __rmod__(self, other: Self | LocalTypeVar) -> Self:
		return other - (other / self) * self

	@remoteMethod_mutable
	def __iadd__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceAdd(
				target=self,
				value=type(self).ensureRemote(self.rob, other),
			),
		)
		return self

	@remoteMethod_mutable
	def __isub__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceSubtract(
				target=self,
				value=type(self).ensureRemote(self.rob, other),
			),
		)
		return self

	@remoteMethod_mutable
	def __imul__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceMultiply(
				target=self,
				value=type(self).ensureRemote(self.rob, other),
			),
		)
		return self

	@remoteMethod_mutable
	def __itruediv__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceDivide(
				target=self,
				value=type(self).ensureRemote(self.rob, other),
			),
		)
		return self

	@remoteMethod_mutable
	def __imod__(self, other: Self | LocalTypeVar) -> Self:
		self -= (self / other) * other
		return self


class RemoteIntBase(RemoteNumber[int]):
	__floordiv__ = RemoteNumber.__truediv__
	__rfloordiv__ = RemoteNumber.__rtruediv__
	__ifloordiv__ = RemoteNumber.__itruediv__


class RemoteUint(RemoteIntBase):
	_IsTypeInstruction = instructions.IsUint
	_NewInstruction = instructions.NewUint
	_ctype = c_ulong
	LocalType = int
	_defaultInitialValue = 0


class RemoteInt(RemoteIntBase):
	_IsTypeInstruction = instructions.IsInt
	_NewInstruction = instructions.NewInt
	_ctype = c_long
	LocalType = int
	_defaultInitialValue = 0


class RemoteFloat(RemoteNumber[float]):
	_IsTypeInstruction = instructions.IsFloat
	_NewInstruction = instructions.NewFloat
	_ctype = ctypes.c_double
	LocalType = float
	_defaultInitialValue = 0.0


class RemoteString(RemoteBaseObject[str]):
	_IsTypeInstruction = instructions.IsString
	LocalType = str
	_defaultInitialValue = ""

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		initialValue = self.initialValue
		stringLen = len(initialValue) + 1
		stringVal = ctypes.create_unicode_buffer(initialValue)
		yield instructions.NewString(
			result=self,
			length=c_ulong(stringLen),
			value=stringVal,
		)

	def _concat(self, other: Self | str) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.StringConcat(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return result

	@remoteMethod
	def __add__(self, other: Self | str) -> RemoteString:
		return self._concat(other)

	@remoteMethod
	def __radd__(self, other: Self | str) -> RemoteString:
		return self._concat(other)

	@remoteMethod_mutable
	def __iadd__(self, other: Self | str) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.StringConcat(
				result=self,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
			),
		)
		return self

	@remoteMethod_mutable
	def set(self, other: Self | str):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.NewString(
				result=self,
				length=c_ulong(1),
				value=ctypes.create_unicode_buffer(""),
			),
		)
		self += other

	@remoteMethod
	def copy(self) -> Self:
		copy = type(self)(self.rob, self.rob.requestNewOperandId())
		copy += self
		return copy


class RemoteArray(RemoteBaseObject):
	_LOCAL_COM_INTERFACES = [
		UIA.IUIAutomationElement,
		UIA.IUIAutomationTextRange,
	]

	def _correctCOMPointers(self, *items: object) -> list:
		correctedItems = []
		for i, item in enumerate(items):
			if isinstance(item, IUnknown):
				for interface in self._LOCAL_COM_INTERFACES:
					try:
						item = item.QueryInterface(interface)
						break
					except COMError:
						pass
			elif isinstance(item, tuple):
				item = self._correctCOMPointers(*item)
			correctedItems.append(item)
		return correctedItems

	@property
	def localValue(self) -> list:
		items = super().localValue
		return self._correctCOMPointers(*items)

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewArray(
			result=self,
		)

	@remoteMethod
	def __getitem__(self, index: RemoteIntBase | int) -> RemoteVariant:
		result = RemoteVariant(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArrayGetAt(
				result=result,
				target=self,
				index=RemoteIntBase.ensureRemote(self.rob, index),
			),
		)
		return result

	@remoteMethod
	def size(self) -> RemoteUint:
		result = RemoteUint(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArraySize(
				result=result,
				target=self,
			),
		)
		return result

	@remoteMethod_mutable
	def append(self, value: RemoteBaseObject | int | float | str) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArrayAppend(
				target=self,
				value=RemoteBaseObject.ensureRemote(self.rob, value),
			),
		)

	@remoteMethod_mutable
	def __setitem__(
		self,
		index: RemoteIntBase | int,
		value: RemoteBaseObject | int | float | str,
	) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArraySetAt(
				target=self,
				index=RemoteIntBase.ensureRemote(self.rob, index),
				value=RemoteBaseObject.ensureRemote(self.rob, value),
			),
		)

	@remoteMethod_mutable
	def remove(self, index: RemoteIntBase | int) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArrayRemoveAt(
				target=self,
				index=RemoteIntBase.ensureRemote(self.rob, index),
			),
		)


class RemoteGuid(RemoteBaseObject[GUID]):
	_IsTypeInstruction = instructions.IsGuid
	LocalType = GUID

	@property
	def _defaultInitialValue(self) -> GUID:
		return GUID()

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewGuid(
			result=self,
			value=self.initialValue,
		)


def getRemoteTypeForLocalType(LocalType: Type[object]) -> Type[RemoteBaseObject]:
	if issubclass(LocalType, enum.IntEnum):
		return RemoteIntEnum
	elif issubclass(LocalType, NoneType):
		return RemoteNull
	elif issubclass(LocalType, bool):
		return RemoteBool
	elif issubclass(LocalType, int):
		return RemoteInt
	elif issubclass(LocalType, float):
		return RemoteFloat
	elif issubclass(LocalType, str):
		return RemoteString
	elif issubclass(LocalType, GUID):
		return RemoteGuid
	else:
		raise TypeError(f"No mapping for type {LocalType.__name__}")


# Import some more complex types after defining the base classes to avoid circular imports
# flake8: noqa: F401
# flake8: noqa: E402
from .intEnum import RemoteIntEnum
from .extensionTarget import RemoteExtensionTarget
from .element import RemoteElement
from .textRange import RemoteTextRange
