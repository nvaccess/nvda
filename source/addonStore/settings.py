# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from dataclasses import dataclass, replace
import json
import os
from typing import Any

from logHandler import log
import NVDAState

from .models.channel import UpdateChannel

__all__ = ["_AddonStoreSettings"]


@dataclass
class _AddonSettings:
	"""Settings for the Add-on Store management of an add-on.

	All options must have a default value.
	"""

	updateChannel: UpdateChannel = UpdateChannel.DEFAULT
	"""Preferred update channels for the add-on."""

	# TODO: migrate enabled/disabled/blocked state tracking
	# from addonHandler.AddonState/AddonStateCategory to here.
	# The set based state tracking could be replaced by maintaining state data on each add-on.
	#
	# blocked: bool = False
	# """Whether the add-on is blocked from being running due to incompatibility."""
	#
	# disabled: bool = False
	# """Whether the add-on is disabled."""


class _AddonStoreSettings:
	"""Settings for the Add-on Store."""

	_CACHE_FILENAME: str = "_cachedSettings.json"

	_showWarning: bool
	"""Show warning when opening Add-on Store."""

	_addonSettings: dict[str, _AddonSettings]
	"""Settings related to the management of add-ons"""

	def __init__(self):
		self._storeSettingsFile = os.path.join(
			NVDAState.WritePaths.addonStoreDir,
			self._CACHE_FILENAME,
		)
		self._showWarning = True
		self._addonSettings = {}
		self.load()

	def load(self):
		try:
			with open(self._storeSettingsFile, "r", encoding="utf-8") as storeSettingsFile:
				settingsDict: dict[str, Any] = json.load(storeSettingsFile)
		except FileNotFoundError:
			return
		except (json.JSONDecodeError, UnicodeDecodeError):
			log.exception("Invalid add-on store settings")
			if NVDAState.shouldWriteToDisk():
				os.remove(self._storeSettingsFile)
			return
		else:
			self._loadFromSettingsDict(settingsDict)

	def _loadFromSettingsDict(self, settingsDict: dict[str, Any]):
		try:
			if not isinstance(settingsDict["addonSettings"], dict):
				raise ValueError("addonSettings must be a dict")

			if not isinstance(settingsDict["showWarning"], bool):
				raise ValueError("showWarning must be a bool")

		except (KeyError, ValueError):
			log.exception(f"Invalid add-on store cache:\n{settingsDict}")
			if NVDAState.shouldWriteToDisk():
				os.remove(self._storeSettingsFile)
			return

		self._showWarning = settingsDict["showWarning"]
		for addonId, settings in settingsDict["addonSettings"].items():
			try:
				updateChannel = UpdateChannel(settings["updateChannel"])
			except ValueError:
				log.exception(f"Invalid add-on settings for {addonId}:\n{settings}. Ignoring settings")
				continue
			else:
				self._addonSettings[addonId] = _AddonSettings(
					updateChannel=updateChannel,
				)

	def save(self):
		if not NVDAState.shouldWriteToDisk():
			log.error("Shouldn't write to disk, not saving add-on store settings")
			return
		settingsDict = {
			"showWarning": self._showWarning,
			"addonSettings": {
				addonId: {
					"updateChannel": addonSettings.updateChannel.value,
				}
				for addonId, addonSettings in self._addonSettings.items()
			},
		}
		with open(self._storeSettingsFile, "w", encoding="utf-8") as storeSettingsFile:
			json.dump(settingsDict, storeSettingsFile, ensure_ascii=False)

	def setAddonSettings(self, addonId: str, **kwargs):
		"""Set settings for an add-on.

		Keyword arguments the same as _AddonSettings:
			- updateChannel: Update channel for the add-on.
		"""
		if addonId not in self._addonSettings:
			self._addonSettings[addonId] = _AddonSettings(**kwargs)
		else:
			self._addonSettings[addonId] = replace(self._addonSettings[addonId], **kwargs)
		self.save()

	def getAddonSettings(self, addonId: str) -> _AddonSettings:
		"""Get settings for an add-on.

		Returns default settings if the add-on has no stored settings.
		"""
		return self._addonSettings.get(addonId, _AddonSettings())

	@property
	def showWarning(self) -> bool:
		return self._showWarning

	@showWarning.setter
	def showWarning(self, showWarning: bool):
		self._showWarning = showWarning
		self.save()
