# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	Any,
	Self,
	Generic,
	TypeVar,
	cast,
)
from ctypes import (
	_SimpleCData,
	c_long
)
import enum
from .. import builder
from . import (
	RemoteInt,
	remoteMethod
)


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


_RemoteIntEnum_LocalTypeVar = TypeVar('_RemoteIntEnum_LocalTypeVar', bound=enum.IntEnum)


class RemoteIntEnum(RemoteInt, Generic[_RemoteIntEnum_LocalTypeVar]):
	localType = enum.IntEnum
	_enumType: _RemoteIntEnum_LocalTypeVar

	def _initOperand(self, initialValue: _RemoteIntEnum_LocalTypeVar, const: bool = False):
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
