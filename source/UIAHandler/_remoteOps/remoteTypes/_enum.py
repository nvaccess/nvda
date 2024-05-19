# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	cast
)
from ctypes import (
	_SimpleCData,
	c_long
)
import enum


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
