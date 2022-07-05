# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Feature flag value enumerations.
Some feature flags require feature specific options, this file defines those options.
All feature flags enums must have a 'DEFAULT'
"""
import enum
import logging
import sys
import typing

from typing_extensions import Protocol  # Python 3.8 adds native support


class FeatureFlagEnumProtocol(Protocol):
	""" All feature flags are expected to have a "DEFAULT" value.
	"""
	DEFAULT: enum.Enum
	name: str
	value: typing.Type


class BoolFlag(enum.Enum):
	"""Generic logically bool feature flag.
	The explicit DEFAULT option allows developers to differentiate between a value set that happens to be
	the current default, and a value that has been returned to the "default" explicitly.
	"""
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


def getAvailableEnums() -> typing.Generator[typing.Tuple[str, enum.EnumMeta], None, None]:
	for name, value in globals().items():
		logging.debug(f"Found Enum class: {name}:{value}")
		if isinstance(value, enum.EnumMeta) and hasattr(value, "DEFAULT"):
			yield name, value
