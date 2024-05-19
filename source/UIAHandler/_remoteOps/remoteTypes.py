# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	Any,
	Self,
	Callable,
	ParamSpec,
	Iterable,
	Generator,
	Generic,
	TypeVar,
	cast
)
import contextlib
import ctypes
from ctypes import (
	_SimpleCData,
	c_long,
	c_ulong,
	c_bool,
	POINTER
)
from comtypes import (
	GUID,
	IUnknown,
	COMError
)
import enum
from UIAHandler import UIA
from . import lowLevel
from .lowLevel import RelativeOffset
from . import instructions
from . import builder
from .remoteFuncWrapper import (
	remoteMethod,
	remoteMethod_mutable,
	remoteContextManager
)
from . import operation


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


_remoteFunc_self = TypeVar('_remoteFunc_self', bound=builder._RemoteBase)
_remoteFunc_paramSpec = ParamSpec('_remoteFunc_paramSpec')
_remoteFunc_return = TypeVar('_remoteFunc_return')


LocalTypeVar = TypeVar('LocalTypeVar')


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

	def _initOperand(self, initialValue: LocalTypeVar | None = None, const=False):
		if initialValue is not None:
			if self.LocalType is None:
				raise TypeError(f"{type(self).__name__} does not support an initial value")
			if not isinstance(initialValue, self.LocalType):
				raise TypeError(
					f"initialValue must be of type {self.LocalType.__name__} "
					f"not {type(initialValue).__name__}"
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
			const: bool = False
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
					f"which is not a subclass of {cls.__name__}"
				)
		cacheKey = (RemoteType, obj)
		cachedRemoteObj = rob._remotedArgCache.get(cacheKey)
		if cachedRemoteObj is not None:
			if not isinstance(cachedRemoteObj, RemoteType):
				raise RuntimeError(f"Cache entry for {cacheKey} is not of type {RemoteType.__name__}")
			rob.getDefaultInstructionList().addComment(
				f"Using cached {cachedRemoteObj} for constant value {repr(obj)}"
			)
			return cast(RemoteType, cachedRemoteObj)
		with rob.overrideDefaultSection('const'):
			remoteObj = RemoteType.createNew(rob, obj, const=True)
		rob.getDefaultInstructionList().addComment(
			f"Using cached {remoteObj} for constant value {repr(obj)}"
		)
		rob._remotedArgCache[cacheKey] = remoteObj
		return remoteObj

	@property
	def initialValue(self) -> LocalTypeVar:
		if self._initialValue is not None:
			return self._initialValue
		return self._generateDefaultInitialValue()

	@property
	def isLocalValueAvailable(self):
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
				value=type(self).ensureRemote(self.rob, other)
			)
		)

	@remoteMethod
	def copy(self) -> Self:
		copy = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.Set(
				target=copy,
				value=self
			)
		)
		return copy

	def _doCompare(self, comparisonType: lowLevel.ComparisonType, other: Self | LocalTypeVar) -> RemoteBool:
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.Compare(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other),
				comparisonType=comparisonType
			)
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
				target=self
			)
		)
		return result


class RemoteVariant(RemoteBaseObject):

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewNull(
			result=self
		)

	def _isType(self, RemoteClass: Type[RemoteBaseObject]) -> RemoteBool:
		if not issubclass(RemoteClass, RemoteBaseObject):
			raise TypeError("remoteClass must be a subclass of RemoteBaseObject")
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			RemoteClass._IsTypeInstruction(
				result=result,
				target=self
			)
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

	_TV_asType = TypeVar('_TV_asType', bound=RemoteBaseObject)

	def asType(self, remoteClass: Type[_TV_asType]) -> _TV_asType:
		return remoteClass(self.rob, self.operandId)


class RemoteNull(RemoteBaseObject):
	_IsTypeInstruction = instructions.IsNull

	def _generateInitInstructions(self,) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewNull(
			result=self
		)


class RemoteIntegral(RemoteBaseObject[LocalTypeVar], Generic[LocalTypeVar]):

	_NewInstruction: Type[builder.InstructionBase]
	_ctype: Type[_SimpleCData]

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield self._NewInstruction(
			result=self,
			value=self._ctype(self.initialValue)
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
				target=self
			)
		)
		return result

	@remoteMethod
	def __and__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolAnd(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __rand__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolAnd(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __or__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolOr(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __ror__(self, other: Self | bool) -> RemoteBool:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BoolOr(
				result=result,
				left=self,
				right=RemoteBool.ensureRemote(self.rob, other)
			)
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
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __sub__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinarySubtract(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __mul__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryMultiply(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __truediv__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryDivide(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __mod__(self, other: Self | LocalTypeVar) -> Self:
		return (self - (self / other) * other)

	@remoteMethod
	def __radd__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryAdd(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __rsub__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinarySubtract(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __rmul__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryMultiply(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __rtruediv__(self, other: Self | LocalTypeVar) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.BinaryDivide(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return result

	@remoteMethod
	def __rmod__(self, other: Self | LocalTypeVar) -> Self:
		return (other - (other / self) * self)

	@remoteMethod_mutable
	def __iadd__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceAdd(
				target=self,
				value=type(self).ensureRemote(self.rob, other)
			)
		)
		return self

	@remoteMethod_mutable
	def __isub__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceSubtract(
				target=self,
				value=type(self).ensureRemote(self.rob, other)
			)
		)
		return self

	@remoteMethod_mutable
	def __imul__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceMultiply(
				target=self,
				value=type(self).ensureRemote(self.rob, other)
			)
		)
		return self

	@remoteMethod_mutable
	def __itruediv__(self, other: Self | LocalTypeVar) -> Self:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.InplaceDivide(
				target=self,
				value=type(self).ensureRemote(self.rob, other)
			)
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


_RemoteIntEnum_LocalTypeVar = TypeVar('_RemoteIntEnum_LocalTypeVar', bound=enum.IntEnum)


class RemoteIntEnum(RemoteInt, Generic[_RemoteIntEnum_LocalTypeVar]):
	localType = enum.IntEnum
	_enumType: _RemoteIntEnum_LocalTypeVar

	def _initOperand(self, initialValue: _RemoteIntEnum_LocalTypeVar, const=False):
		if not isinstance(initialValue, enum.IntEnum):
			raise TypeError(f"initialValue must be of type {enum.IntEnum.__name__} not {type(initialValue).__name__}")
		self.LocalType = type(initialValue)
		self._ctype = _makeCtypeIntEnum(type(initialValue))
		super()._initOperand(initialValue=initialValue, const=const)

	@classmethod
	def ensureRemote(
			cls,
			rob: builder.RemoteOperationBuilder,
			obj: RemoteIntEnum[_RemoteIntEnum_LocalTypeVar] | _RemoteIntEnum_LocalTypeVar
	) -> RemoteIntEnum[_RemoteIntEnum_LocalTypeVar]:
		remoteObj = super().ensureRemote(rob, cast(Any, obj))
		return cast(RemoteIntEnum[_RemoteIntEnum_LocalTypeVar], remoteObj)

	@remoteMethod
	def set(self, other: Self | _RemoteIntEnum_LocalTypeVar):
		super().set(other)


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
		stringLen = (len(initialValue) + 1)
		stringVal = ctypes.create_unicode_buffer(initialValue)
		yield instructions.NewString(
			result=self,
			length=c_ulong(stringLen),
			value=stringVal
		)

	def _concat(self, other: Self | str) -> Self:
		result = type(self)(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.StringConcat(
				result=result,
				left=self,
				right=type(self).ensureRemote(self.rob, other)
			)
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
				right=type(self).ensureRemote(self.rob, other)
			)
		)
		return self

	@remoteMethod_mutable
	def set(self, other: Self | str):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.NewString(
				result=self,
				length=c_ulong(1),
				value=ctypes.create_unicode_buffer("")
			)
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
		UIA.IUIAutomationTextRange
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
			result=self
		)

	@remoteMethod
	def __getitem__(self, index: RemoteIntBase | int) -> RemoteVariant:
		result = RemoteVariant(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArrayGetAt(
				result=result,
				target=self,
				index=RemoteIntBase.ensureRemote(self.rob, index)
			)
		)
		return result

	@remoteMethod
	def size(self) -> RemoteUint:
		result = RemoteUint(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArraySize(
				result=result,
				target=self
			)
		)
		return result

	@remoteMethod_mutable
	def append(self, value: RemoteBaseObject | int | float | str) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArrayAppend(
				target=self,
				value=RemoteBaseObject.ensureRemote(self.rob, value)
			)
		)

	@remoteMethod_mutable
	def __setitem__(
			self,
			index: RemoteIntBase | int,
			value: RemoteBaseObject | int | float | str
	) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArraySetAt(
				target=self,
				index=RemoteIntBase.ensureRemote(self.rob, index),
				value=RemoteBaseObject.ensureRemote(self.rob, value)
			)
		)

	@remoteMethod_mutable
	def remove(self, index: RemoteIntBase | int) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ArrayRemoveAt(
				target=self,
				index=RemoteIntBase.ensureRemote(self.rob, index)
			)
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
			value=self.initialValue
		)


class RemoteExtensionTarget(RemoteBaseObject[LocalTypeVar], Generic[LocalTypeVar]):

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewNull(
			result=self
		)

	@remoteMethod
	def isNull(self):
		variant = RemoteVariant(self.rob, self.operandId)
		return variant.isNull()

	@remoteMethod
	def isExtensionSupported(self, extensionId: RemoteGuid | GUID) -> RemoteBool:
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.IsExtensionSupported(
				result=result,
				target=self,
				extensionId=RemoteGuid.ensureRemote(self.rob, extensionId)
			)
		)
		return result

	@remoteMethod_mutable
	def callExtension(
			self,
			extensionId: RemoteGuid | GUID,
			*params: RemoteBaseObject | int | float | str
	) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.CallExtension(
				target=self,
				extensionId=RemoteGuid.ensureRemote(self.rob, extensionId),
				argCount=c_ulong(len(params)),
				arguments=[RemoteBaseObject.ensureRemote(self.rob, param) for param in params]
			)
		)


class RemoteElement(RemoteExtensionTarget[POINTER(UIA.IUIAutomationElement)]):
	_IsTypeInstruction = instructions.IsElement
	LocalType = POINTER(UIA.IUIAutomationElement)

	def _initOperand(self, initialValue: None = None, const=False):
		if initialValue is not None:
			raise TypeError("Cannot initialize RemoteElement with an initial value.")
		return super()._initOperand()

	@property
	def localValue(self) -> UIA.IUIAutomationElement:
		value = super().localValue
		if value is None:
			return POINTER(UIA.IUIAutomationElement)()
		return cast(UIA.IUIAutomationElement, value.QueryInterface(UIA.IUIAutomationElement))

	@remoteMethod
	def getPropertyValue(
			self,
			propertyId: RemoteIntEnum[lowLevel.PropertyId] | lowLevel.PropertyId,
			ignoreDefault: RemoteBool | bool = False
	) -> RemoteVariant:
		result = RemoteVariant(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ElementGetPropertyValue(
				result=result,
				target=self,
				propertyId=RemoteIntEnum.ensureRemote(self.rob, propertyId),
				ignoreDefault=RemoteBool.ensureRemote(self.rob, ignoreDefault)
			)
		)
		return result

	def _navigate(self, navigationDirection: lowLevel.NavigationDirection) -> RemoteElement:
		result = RemoteElement(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.ElementNavigate(
				result=result,
				target=self,
				direction=RemoteIntEnum.ensureRemote(self.rob, navigationDirection)
			)
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

	def _initOperand(self, initialValue: None = None, const=False):
		if initialValue is not None:
			raise TypeError("Cannot initialize RemoteTextRange with an initial value.")
		return super()._initOperand()

	@property
	def localValue(self) -> UIA.IUIAutomationTextRange:
		value = super().localValue
		if value is None:
			return POINTER(UIA.IUIAutomationTextRange)()
		return cast(UIA.IUIAutomationTextRange, value.QueryInterface(UIA.IUIAutomationTextRange))

	@remoteMethod
	def clone(self):
		result = RemoteTextRange(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeClone(
				result=result,
				target=self
			)
		)
		return result

	@remoteMethod
	def getEnclosingElement(self) -> RemoteElement:
		result = RemoteElement(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeGetEnclosingElement(
				result=result,
				target=self
			)
		)
		return result

	@remoteMethod
	def getText(self, maxLength: RemoteInt | int) -> RemoteString:
		result = RemoteString(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeGetText(
				result=result,
				target=self,
				maxLength=RemoteInt.ensureRemote(self.rob, maxLength)
			)
		)
		return result

	@remoteMethod_mutable
	def expandToEnclosingUnit(self, unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeExpandToEnclosingUnit(
				target=self,
				unit=RemoteIntEnum.ensureRemote(self.rob, unit)
			)
		)

	@remoteMethod_mutable
	def moveEndpointByUnit(
			self,
			endpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
			unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit,
			count: RemoteInt | int
	):
		result = RemoteInt(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeMoveEndpointByUnit(
				result=result,
				target=self,
				endpoint=RemoteIntEnum.ensureRemote(self.rob, endpoint),
				unit=RemoteIntEnum.ensureRemote(self.rob, unit),
				count=RemoteInt.ensureRemote(self.rob, count)
			)
		)
		return result

	@remoteMethod_mutable
	def moveEndpointByRange(
			self,
			srcEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
			otherRange: RemoteTextRange,
			otherEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint
	):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeMoveEndpointByRange(
				target=self,
				srcEndpoint=RemoteIntEnum.ensureRemote(self.rob, srcEndpoint),
				otherRange=otherRange,
				otherEndpoint=RemoteIntEnum.ensureRemote(self.rob, otherEndpoint)
			)
		)

	@remoteMethod
	def getAttributeValue(
			self,
			attributeId: RemoteIntEnum[lowLevel.AttributeId] | lowLevel.AttributeId
	) -> RemoteVariant:
		result = RemoteVariant(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeGetAttributeValue(
				result=result,
				target=self,
				attributeId=RemoteIntEnum.ensureRemote(self.rob, attributeId)
			)
		)
		return result

	@remoteMethod
	def compareEndpoints(
			self,
			thisEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
			otherRange: RemoteTextRange,
			otherEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint
	) -> RemoteInt:
		result = RemoteInt(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeCompareEndpoints(
				result=result,
				target=self,
				thisEndpoint=RemoteIntEnum.ensureRemote(self.rob, thisEndpoint),
				otherRange=otherRange,
				otherEndpoint=RemoteIntEnum.ensureRemote(self.rob, otherEndpoint)
			)
		)
		return result

	def getLogicalAdapter(self, reverse=False) -> RemoteTextRangeLogicalAdapter:
		obj = RemoteTextRangeLogicalAdapter(self.rob, self, reverse=reverse)
		return obj


class _RemoteTextRangeEndpoint(builder._RemoteBase):

	def __init__(
			self,
			rob: builder.RemoteOperationBuilder,
			textRangeLA: RemoteTextRangeLogicalAdapter, isStart: bool
	):
		super().__init__(rob)
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
			unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit,
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


class RemoteTextRangeLogicalAdapter(builder._RemoteBase):

	def __init__(
			self,
			rob: builder.RemoteOperationBuilder,
			textRange: RemoteTextRange, reverse=False
	):
		super().__init__(rob)
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
		obj = _RemoteTextRangeEndpoint(self.rob, self, isStart=True)
		return obj

	@start.setter
	def start(self, value: _RemoteTextRangeEndpoint):
		self.start.moveTo(value)

	@property
	def end(self) -> _RemoteTextRangeEndpoint:
		obj = _RemoteTextRangeEndpoint(self.rob, self, isStart=False)
		return obj

	@end.setter
	def end(self, value: _RemoteTextRangeEndpoint):
		self.end.moveTo(value)

	def clone(self):
		return self.textRange.clone().getLogicalAdapter(self.isReversed)


def getRemoteTypeForLocalType(LocalType: Type[object]) -> Type[RemoteBaseObject]:
	if issubclass(LocalType, enum.IntEnum):
		return RemoteIntEnum
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
