# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Bill Dengler, Rob Meredith
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
from typing import Protocol

from utils.displayString import (
	DisplayStringEnum,
	_DisplayStringEnumMixin,
)


class FeatureFlagEnumProtocol(Protocol):
	""" All feature flags are expected to have a "DEFAULT" value.
	This definition is provided only for type annotations
	"""
	DEFAULT: enum.Enum  # Required enum member
	name: str  # comes from enum.Enum
	value: str  # comes from enum.Enum


class FlagValueEnum(enum.EnumMeta, _DisplayStringEnumMixin, FeatureFlagEnumProtocol):
	"""Provided only for type annotations.
	"""
	pass


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


class ParagraphNavigationFlag(DisplayStringEnum):
	@property
	def _displayStringLabels(self):
		return {
			# Translators: Label for a paragraph style in NVDA settings.
			self.APPLICATION: _("Handled by application"),
			# Translators: Label for a paragraph style in NVDA settings.
			self.SINGLE_LINE_BREAK: _("Single line break"),
			# Translators: Label for a paragraph style in NVDA settings.
			self.MULTI_LINE_BREAK: _("Multi line break")
		}

	DEFAULT = enum.auto()
	APPLICATION = enum.auto()
	SINGLE_LINE_BREAK = enum.auto()
	MULTI_LINE_BREAK = enum.auto()


class ReviewRoutingMovesSystemCaretFlag(DisplayStringEnum):
	@property
	def _displayStringLabels(self):
		return {
			# Translators: Label for setting to move the system caret when routing review cursor with braille.
			self.NEVER: _("Never"),
			# Translators: Label for setting to move the system caret when routing review cursor with braille.
			self.ONLY_WHEN_AUTO_TETHERED: _("Only when tethered automatically"),
			# Translators: Label for setting to move the system caret when routing review cursor with braille.
			self.ALWAYS: _("Always")
		}

	DEFAULT = enum.auto()
	NEVER = enum.auto()
	ONLY_WHEN_AUTO_TETHERED = enum.auto()
	ALWAYS = enum.auto()


class WindowsTerminalStrategyFlag(DisplayStringEnum):
	"""
	A feature flag for defining how new text is calculated in Windows Terminal
	(wt.exe).
	"""

	@property
	def _displayStringLabels(self):
		return {
			# Translators: Label for an option in NVDA settings.
			self.DIFFING: _("Diffing"),
			# Translators: Label for an option in NVDA settings.
			self.NOTIFICATIONS: _("UIA notifications"),
		}

	DEFAULT = enum.auto()
	DIFFING = enum.auto()
	NOTIFICATIONS = enum.auto()


def getAvailableEnums() -> typing.Generator[typing.Tuple[str, FlagValueEnum], None, None]:
	for name, value in globals().items():
		if (
			isinstance(value, type)  # is a class
			and issubclass(value, DisplayStringEnum)  # inherits from DisplayStringEnum
			and value != DisplayStringEnum  # but isn't DisplayStringEnum
		):
			yield name, value
