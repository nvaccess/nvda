# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Dict,
	OrderedDict,
	Set,
)

from utils.displayString import DisplayStringStrEnum


class Channel(DisplayStringStrEnum):
	STABLE = "stable"
	BETA = "beta"
	DEV = "dev"
	ALL = "all"

	@property
	def _displayStringLabels(self) -> Dict["Channel", str]:
		return {
			# Translators: Label for add-on channel in the add-on sotre
			self.STABLE: pgettext("addonStore", "Stable"),
			# Translators: Label for add-on channel in the add-on sotre
			self.BETA: pgettext("addonStore", "Beta"),
			# Translators: Label for add-on channel in the add-on sotre
			self.DEV: pgettext("addonStore", "Dev"),
			# Translators: Label for add-on channel in the add-on sotre
			self.ALL: pgettext("addonStore", "All"),
		}


_channelFilters: OrderedDict[str, Set[Channel]] = OrderedDict({
	Channel.ALL.displayString: {
		Channel.STABLE,
		Channel.BETA,
		Channel.DEV,
	},
	Channel.STABLE.displayString: {Channel.STABLE},
	Channel.BETA.displayString: {Channel.BETA},
	Channel.DEV.displayString: {Channel.DEV},
})
"""A dictionary where the keys are channel groups to filter by,
and the values are which channels should be shown for a given filter.
"""
