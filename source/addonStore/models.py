# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import dataclasses
from enum import Enum
import json
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Tuple,
)

import addonAPIVersion

AddonVersionT = Tuple[int, int, int]


class Channel(str, Enum):
	STABLE = "stable"
	BETA = "beta"
	DEV = "dev"
	ALL = "all"


@dataclasses.dataclass(frozen=True)  # once created, it should not be modified.
class AddonDetailsModel:
	"""Typing for information from API
	"""
	addonId: str
	displayName: str
	description: str
	publisher: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
	license: str
	licenseURL: Optional[str]
	sourceURL: str
	URL: str
	sha256: str
	addonVersionNumber: AddonVersionT
	minimumNVDAVersion: addonAPIVersion.AddonApiVersionT
	"""Deviates from name in JSON, in order to match name required for addonAPIVersion"""
	lastTestedNVDAVersion: addonAPIVersion.AddonApiVersionT
	"""Deviates from name in JSON, in order to match name required for addonAPIVersion"""


def _createAddonApiVersion(versionDict: Dict[str, int]) -> addonAPIVersion.AddonApiVersionT:
	"""
	@param versionDict: expected to contain a Dict like: {"major": 2019, "minor": 3, "patch": 0}
	"""
	return versionDict["major"], versionDict["minor"], versionDict["patch"]


def _createAddonModelFromData(addon: Dict[str, Any]) -> AddonDetailsModel:
	return AddonDetailsModel(
		addonId=addon["addonId"],
		displayName=addon["displayName"],
		description=addon["description"],
		publisher=addon["publisher"],
		channel=Channel(addon["channel"]),
		addonVersionName=addon["addonVersionName"],
		addonVersionNumber=_createAddonApiVersion(addon["addonVersionNumber"]),
		homepage=addon.get("homepage"),
		license=addon["license"],
		licenseURL=addon.get("licenseURL"),
		sourceURL=addon["sourceURL"],
		URL=addon["URL"],
		sha256=addon["sha256"],
		minimumNVDAVersion=_createAddonApiVersion(addon["minNVDAVersion"]),
		lastTestedNVDAVersion=_createAddonApiVersion(addon["lastTestedVersion"]),
	)


def _createModelFromData(jsonData: str) -> List[AddonDetailsModel]:
	"""Use json string to construct a listing of available addons.
	See https://github.com/nvaccess/addon-datastore#api-data-generation-details
	for details of the data.
	"""
	data: List[Dict[str, Any]] = json.loads(jsonData)
	return [_createAddonModelFromData(addon) for addon in data]
