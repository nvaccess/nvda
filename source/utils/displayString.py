# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited.

from abc import ABC, ABCMeta, abstractproperty
from enum import Enum, EnumMeta
from typing import Dict

from logHandler import log


class DisplayStringEnumMixinMeta(ABCMeta, EnumMeta):
	"""
	This helps correct the Method Resolution Order (MRO) when using the `DisplayStringEnumMixin`.
	When creating an Enum with a Mixin, Python suggest an ordering of
	`class EnumWithMixin(Mixin, type, EnumClass):`.
	This creates a metaclass conflict as both DisplayStringEnumMixin and Enum both have metaclasses,
	ABCMeta and EnumMeta. This requires a new MetaClass which subclasses both of these. This follows the
	same ordering of the EnumWithMixin usage.
	See `DisplayStringEnumMixin`.
	"""
	pass


class DisplayStringEnumMixin(ABC):
	"""
	This mixin can be used with a class which subclasses Enum to provided translated display strings for
	members of the enum. The abstract properties must be overridden.
	To be used with `DisplayStringEnumMixinMeta`.
	Usage for python 3.7 is as follows:
	```
	class ExampleEnum(DisplayStringEnumMixin, str, Enum, metaclass=DisplayStringEnumMixinMeta):
		pass

	class ExampleIntEnum(DisplayStringEnumMixin, IntEnum, metaclass=DisplayStringEnumMixinMeta):
		pass
	```
	"""
	@abstractproperty
	def _displayStringLabels(self) -> Dict[Enum, str]:
		"""
		Specify a dictionary which takes members of the Enum and returns the translated display string.
		"""
		pass

	@abstractproperty
	def defaultValue(self) -> Enum:
		"""
		Specify an Enum member with a known translated display string to use as a default if there is no known
		display string for a given member in _displayStringLabels.
		"""
		pass

	@property
	def displayString(self) -> str:
		"""
		@return: The translated UI display string that should be used for this value of the enum.
		"""
		try:
			return self._displayStringLabels[self]
		except KeyError:
			log.error(f"No translation mapping for: {self}")
			return self._displayStringLabels[self.defaultValue]
