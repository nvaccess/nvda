# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from datetime import timedelta
from enum import (
	auto,
	unique,
)
from typing import (
	Dict,
)

from utils.displayString import DisplayStringEnum


@unique
class TimeOutputFormat(DisplayStringEnum):
	SECONDS = auto()
	MINUTES = auto()
	HOURS = auto()
	DAY = auto()
	DAYS = auto()

	@property
	def _displayStringLabels(self) -> Dict["TimeOutputFormat", str]:
		return {
			# Translators: used to format time locally.
			# substitution rules: {S} seconds
			self.SECONDS: pgettext("time format", "{S}"),
			# Translators: used to format time locally.
			# substitution rules: {S} seconds, {M} minutes
			self.MINUTES: pgettext("time format", "{M}:{S}"),
			# Translators: used to format time locally.
			# substitution rules: {S} seconds, {M} minutes, {H} hours
			self.HOURS: pgettext("time format", "{H}:{M}:{S}"),
			# Translators: used to format time locally.
			# substitution rules: {S} seconds, {M} minutes, {H} hours, {D} day
			self.DAY: pgettext("time format", "{D} day {H}:{M}:{S}"),
			# Translators: used to format time locally.
			# substitution rules: {S} seconds, {M} minutes, {H} hours, {D} days
			self.DAYS: pgettext("time format", "{D} days {H}:{M}:{S}"),
		}

	@staticmethod
	def convertTimeDeltaToTimeOutputFormat(td: timedelta) -> "TimeOutputFormat":
		"""Returns a TimeOutputFormat with the least leading zeros."""
		seconds = td.total_seconds()
		if seconds < 60:
			return TimeOutputFormat.SECONDS
		elif seconds < 60 * 60:
			return TimeOutputFormat.MINUTES
		elif seconds < 60 * 60 * 24:
			return TimeOutputFormat.HOURS
		elif seconds < 60 * 60 * 24 * 2:
			return TimeOutputFormat.DAY
		else:
			return TimeOutputFormat.DAYS

	@staticmethod
	def parseTimeDeltaToFormatted(td: timedelta) -> str:
		outputFormat = TimeOutputFormat.convertTimeDeltaToTimeOutputFormat(td)
		return outputFormat.displayString.format(
			D=td.days,
			H=td.seconds // 3600,
			M=(td.seconds // 60) % 60,
			S=td.seconds % 60,
		)
