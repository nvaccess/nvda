# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Feature flag value enumerations.
Some feature flags require feature specific options, this file defines those options.
All feature flags enums should
- inherit from DisplayStringEnum and implement _displayStringLabels (for the 'displayString' property)
- have a 'DEFAULT' member.
"""
import enum
import typing

from utils.displayString import (
	DisplayStringEnum
)

from typing_extensions import Protocol  # Python 3.8 adds native support

_displayString = typing.TypeVar("_displayString", bound=DisplayStringEnum)


class FeatureFlagEnumProtocol(Protocol):
	""" All feature flags are expected to have a "DEFAULT" value.
	"""
	DEFAULT: enum.Enum  # Required enum member


FlagValueEnum = typing.Union[FeatureFlagEnumProtocol, _displayString]


class BoolFlag(DisplayStringEnum):
	"""Generic logically bool feature flag.
	The explicit DEFAULT option allows developers to differentiate between a value set that happens to be
	the current default, and a value that has been returned to the "default" explicitly.
	"""

	@property
	def _displayStringLabels(self):
		# To prevent duplication, self.DEFAULT is not included here.
		return {
			# Translators: Label for an option in NVDA settings.
			self.DISABLED: _("Disabled"),
			# Translators: Label for an option in NVDA settings.
			self.ENABLED: _("Enabled"),
		}

	DEFAULT = enum.auto()
	DISABLED = enum.auto()
	ENABLED = enum.auto()

	def __bool__(self):
		if self == BoolFlag.DEFAULT:
			raise ValueError(
				"Only ENABLED or DISABLED are valid bool values"
				", DEFAULT must be combined with a 'behavior for default' to be Truthy or Falsy"
			)
		return self == BoolFlag.ENABLED


def getAvailableEnums() -> typing.Generator[typing.Tuple[str, DisplayStringEnum], None, None]:
	for name, value in globals().items():
		if (
			isinstance(value, type)  # is a class
			and issubclass(value, DisplayStringEnum)  # inherits from DisplayStringEnum
			and value != DisplayStringEnum  # but isn't DisplayStringEnum
		):
			yield name, value
