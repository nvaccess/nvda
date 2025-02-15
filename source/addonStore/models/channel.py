# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Dict,
	OrderedDict,
	Set,
)

import config
from utils.displayString import DisplayStringIntEnum, DisplayStringStrEnum


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


_channelFilters: OrderedDict[Channel, Set[Channel]] = OrderedDict(
	{
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
	},
)
"""A dictionary where the keys are channel groups to filter by,
and the values are which channels should be shown for a given filter.
"""


class UpdateChannel(DisplayStringIntEnum):
	"""Update channel for an addon used for automatic updates."""

	DEFAULT = -1
	"""Default channel.
	Specified in [addonStore][defaultUpdateChannel] section of config.
	"""

	SAME = 0
	"""Keep the same channel as the current version"""

	ANY = 1
	"""Use any channel, keep to the latest version"""

	NO_UPDATE = 2
	"""Do not update the addon"""

	STABLE = 3
	"""Use the stable channel"""

	BETA_DEV = 4
	"""Use the beta or development channel, keep to the latest version"""

	BETA = 5
	"""Use the beta channel"""

	DEV = 6
	"""Use the development channel"""

	@property
	def displayString(self) -> str:
		# Handle the default channel separately to avoid recursive dependency
		# on _displayStringLabels.
		if self is UpdateChannel.DEFAULT:
			channel = UpdateChannel(config.conf["addonStore"]["defaultUpdateChannel"])
			assert channel is not UpdateChannel.DEFAULT
			# Translators: Update channel for an addon.
			# {defaultChannel} will be replaced with the name of the channel the user has selected as default
			return _("Default ({defaultChannel})").format(
				defaultChannel=self._displayStringLabels[channel],
			)
		return super().displayString

	@property
	def _displayStringLabels(self) -> dict["UpdateChannel", str]:
		return {
			# Translators: Update channel for an addon.
			# Same means an add-on only updates to a newer version in the same channel.
			# e.g. an installed beta version only updates to beta versions.
			UpdateChannel.SAME: _("Same"),
			# Translators: Update channel for an addon.
			# Any means an add-on updates to the latest version regardless of the channel.
			UpdateChannel.ANY: _("Any"),
			# Translators: Update channel for an addon
			UpdateChannel.NO_UPDATE: _("Do not update"),
			# Translators: Update channel for an addon
			UpdateChannel.STABLE: _("Stable"),
			# Translators: Update channel for an addon
			UpdateChannel.BETA_DEV: _("Beta or dev"),
			# Translators: Update channel for an addon
			UpdateChannel.BETA: _("Beta"),
			# Translators: Update channel for an addon
			UpdateChannel.DEV: _("Dev"),
		}

	def _availableChannelsForAddonWithChannel(self, addonChannel: Channel) -> set[Channel]:
		"""Return the available update channels for an addon with the given channel and the update channel set."""
		if self == UpdateChannel.DEFAULT:
			channel = UpdateChannel(config.conf["addonStore"]["defaultUpdateChannel"])
			assert channel is not UpdateChannel.DEFAULT
		else:
			channel = self
		match channel:
			case UpdateChannel.SAME:
				return {addonChannel}
			case UpdateChannel.ANY:
				return _channelFilters[Channel.ALL]
			case UpdateChannel.NO_UPDATE:
				return {}
			case UpdateChannel.STABLE:
				return {Channel.STABLE}
			case UpdateChannel.BETA_DEV:
				return {Channel.BETA, Channel.DEV}
			case UpdateChannel.BETA:
				return {Channel.BETA}
			case UpdateChannel.DEV:
				return {Channel.DEV}
			case _:
				raise ValueError(f"Invalid update channel: {self}")
