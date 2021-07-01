# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited.

from abc import ABC, ABCMeta, abstractproperty
from enum import Enum, EnumMeta, IntEnum
from typing import Dict

from logHandler import log


class _DisplayStringEnumMixinMeta(ABCMeta, EnumMeta):
	"""
	This helps correct the Method Resolution Order (MRO) when using the `_DisplayStringEnumMixin`.
	When creating an Enum with a Mixin, Python suggest an ordering of
	`class EnumWithMixin(Mixin, type, EnumClass):`.
	This creates a metaclass conflict as both _DisplayStringEnumMixin and Enum both have metaclasses,
	ABCMeta and EnumMeta. This requires a new MetaClass which subclasses both of these. This follows the
	same ordering of the EnumWithMixin usage.
	See `_DisplayStringEnumMixin`.
	"""
	pass


class _DisplayStringEnumMixin(ABC):
	"""
	This mixin can be used with a class which subclasses Enum to provided translated display strings for
	members of the enum. The abstract properties must be overridden.
	To be used with `_DisplayStringEnumMixinMeta`.
	Usage for python 3.7 is as follows:
	```
	class ExampleEnum(_DisplayStringEnumMixin, str, Enum, metaclass=_DisplayStringEnumMixinMeta):
		pass

	class ExampleIntEnum(_DisplayStringEnumMixin, IntEnum, metaclass=_DisplayStringEnumMixinMeta):
		pass
	```
	"""
	@abstractproperty
	def _displayStringLabels(self) -> Dict[Enum, str]:
		"""
		Specify a dictionary which takes members of the Enum and returns the translated display string.
		"""
		pass

	@property
	def displayString(self) -> str:
		"""
		@return: The translated UI display string that should be used for this value of the enum.
		"""
		try:
			return self._displayStringLabels[self]
		except KeyError as e:
			log.error(f"No translation mapping for: {self}")
			raise e


class DisplayStringEnum(_DisplayStringEnumMixin, Enum, metaclass=_DisplayStringEnumMixinMeta):
	"""An Enum class that adds a displayString property defined by _displayStringLabels"""
	pass


class DisplayStringStrEnum(_DisplayStringEnumMixin, str, Enum, metaclass=_DisplayStringEnumMixinMeta):
	"""A str Enum class that adds a displayString property defined by _displayStringLabels"""
	pass


class DisplayStringIntEnum(_DisplayStringEnumMixin, IntEnum, metaclass=_DisplayStringEnumMixinMeta):
	"""An IntEnum class that adds a displayString property defined by _displayStringLabels"""
	pass
