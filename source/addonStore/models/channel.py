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
	ALL = "all"
	STABLE = "stable"
	BETA = "beta"
	DEV = "dev"
	EXTERNAL = "external"  # for add-ons installed externally

	@property
	def _displayStringLabels(self) -> Dict["Channel", str]:
		return {
			# Translators: Label for add-on channel in the add-on sotre
			self.ALL: pgettext("addonStore", "All"),
			# Translators: Label for add-on channel in the add-on sotre
			self.STABLE: pgettext("addonStore", "Stable"),
			# Translators: Label for add-on channel in the add-on sotre
			self.BETA: pgettext("addonStore", "Beta"),
			# Translators: Label for add-on channel in the add-on sotre
			self.DEV: pgettext("addonStore", "Dev"),
			# Translators: Label for add-on channel in the add-on sotre
			self.EXTERNAL: pgettext("addonStore", "External"),
		}


_channelFilters: OrderedDict[Channel, Set[Channel]] = OrderedDict({
	Channel.ALL: {
		Channel.STABLE,
		Channel.BETA,
		Channel.DEV,
		Channel.EXTERNAL,
	},
	Channel.STABLE: {Channel.STABLE},
	Channel.BETA: {Channel.BETA},
	Channel.DEV: {Channel.DEV},
	Channel.EXTERNAL: {Channel.EXTERNAL},
})
"""A dictionary where the keys are channel groups to filter by,
and the values are which channels should be shown for a given filter.
"""
