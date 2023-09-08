# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import TYPE_CHECKING

import addonAPIVersion
from buildVersion import version_year

if TYPE_CHECKING:
	from _addonStore.models.version import SupportsVersionCheck  # noqa: F401


if version_year < 2024:
	def _isAddonForceDisabled(addon: "SupportsVersionCheck") -> bool:
		from addonHandler import AddonBase as AddonHandlerModel
		from _addonStore.models.addon import _AddonManifestModel, _AddonStoreModel
		from _addonStore.models.version import MajorMinorPatch
		forceDisabledAddons = {
			"tonysEnhancements": MajorMinorPatch(1, 15),
		}
		if isinstance(addon, _AddonStoreModel):
			addonVersion = addon.addonVersionNumber
		elif isinstance(addon, AddonHandlerModel):
			addonVersion = MajorMinorPatch._parseVersionFromVersionStr(addon.version)
		elif isinstance(addon, _AddonManifestModel):
			addonVersion = MajorMinorPatch._parseVersionFromVersionStr(addon.addonVersionName)
		else:
			raise NotImplementedError(f"Unexpected type for addon: {addon.name}, type: {type(addon)}")
		return (
			addon.name in forceDisabledAddons
			and addonVersion <= forceDisabledAddons[addon.name]
		)


def hasAddonGotRequiredSupport(
		addon: "SupportsVersionCheck",
		currentAPIVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.CURRENT
) -> bool:
	"""True if NVDA provides the add-on with an API version high enough to meet the add-on's minimum requirements
	"""
	minVersion = addon.minimumNVDAVersion
	return minVersion <= currentAPIVersion


def isAddonTested(
		addon: "SupportsVersionCheck",
		backwardsCompatToVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.BACK_COMPAT_TO
) -> bool:
	"""True if this add-on is tested for the given API version.
	By default, the current version of NVDA is evaluated.
	"""
	if version_year < 2024:
		if _isAddonForceDisabled(addon):
			return False
	return addon.lastTestedNVDAVersion >= backwardsCompatToVersion


def isAddonCompatible(
		addon: "SupportsVersionCheck",
		currentAPIVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.CURRENT,
		backwardsCompatToVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.BACK_COMPAT_TO
) -> bool:
	"""Tests if the addon is compatible.
	The compatibility is defined by having the required features in NVDA, and by having been tested / built against
	an API version that is still supported by this version of NVDA.
	"""
	return hasAddonGotRequiredSupport(addon, currentAPIVersion) and isAddonTested(addon, backwardsCompatToVersion)
