# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import IntEnum, unique

from utils.displayString import DisplayStringIntEnum

VolumeTupleT = tuple[float, float]


@unique
class SoundSplitState(DisplayStringIntEnum):
	OFF = 0
	NVDA_BOTH_APPS_BOTH = 1
	NVDA_LEFT_APPS_RIGHT = 2
	NVDA_LEFT_APPS_BOTH = 3
	NVDA_RIGHT_APPS_LEFT = 4
	NVDA_RIGHT_APPS_BOTH = 5
	NVDA_BOTH_APPS_LEFT = 6
	NVDA_BOTH_APPS_RIGHT = 7

	@property
	def _displayStringLabels(self) -> dict[IntEnum, str]:
		return {
			# Translators: Sound split state
			SoundSplitState.OFF: pgettext("SoundSplit", "Sound split disabled"),
			SoundSplitState.NVDA_BOTH_APPS_BOTH: pgettext(
				"SoundSplit",
				# Translators: Sound split state
				"NVDA in both channels and applications in both channels",
			),
			# Translators: Sound split state
			SoundSplitState.NVDA_LEFT_APPS_RIGHT: _("NVDA on the left and applications on the right"),
			# Translators: Sound split state
			SoundSplitState.NVDA_LEFT_APPS_BOTH: _("NVDA on the left and applications in both channels"),
			# Translators: Sound split state
			SoundSplitState.NVDA_RIGHT_APPS_LEFT: _("NVDA on the right and applications on the left"),
			# Translators: Sound split state
			SoundSplitState.NVDA_RIGHT_APPS_BOTH: _("NVDA on the right and applications in both channels"),
			# Translators: Sound split state
			SoundSplitState.NVDA_BOTH_APPS_LEFT: _("NVDA in both channels and applications on the left"),
			# Translators: Sound split state
			SoundSplitState.NVDA_BOTH_APPS_RIGHT: _("NVDA in both channels and applications on the right"),
		}

	def getAppVolume(self) -> VolumeTupleT:
		match self:
			case (
				SoundSplitState.NVDA_BOTH_APPS_BOTH
				| SoundSplitState.NVDA_LEFT_APPS_BOTH
				| SoundSplitState.NVDA_RIGHT_APPS_BOTH
			):
				return (1.0, 1.0)
			case SoundSplitState.NVDA_RIGHT_APPS_LEFT | SoundSplitState.NVDA_BOTH_APPS_LEFT:
				return (1.0, 0.0)
			case SoundSplitState.NVDA_LEFT_APPS_RIGHT | SoundSplitState.NVDA_BOTH_APPS_RIGHT:
				return (0.0, 1.0)
			case _:
				raise RuntimeError(f"Unexpected or unknown state {self=}")

	def getNVDAVolume(self) -> VolumeTupleT:
		match self:
			case (
				SoundSplitState.NVDA_BOTH_APPS_BOTH
				| SoundSplitState.NVDA_BOTH_APPS_LEFT
				| SoundSplitState.NVDA_BOTH_APPS_RIGHT
			):
				return (1.0, 1.0)
			case SoundSplitState.NVDA_LEFT_APPS_RIGHT | SoundSplitState.NVDA_LEFT_APPS_BOTH:
				return (1.0, 0.0)
			case SoundSplitState.NVDA_RIGHT_APPS_LEFT | SoundSplitState.NVDA_RIGHT_APPS_BOTH:
				return (0.0, 1.0)
			case _:
				raise RuntimeError(f"Unexpected or unknown state {self=}")
