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
	NamedTuple,
	Optional,
)

import addonAPIVersion


class Channel(str, Enum):
	STABLE = "stable"
	BETA = "beta"
	DEV = "dev"
	ALL = "all"


class MajorMinorPatch(NamedTuple):
	major: int
	minor: int
	patch: int = 0

	def __str__(self) -> str:
		return f"{self.major}.{self.minor}.{self.patch}"


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
	addonVersionNumber: MajorMinorPatch
	minNVDAVersion: MajorMinorPatch
	lastTestedVersion: MajorMinorPatch

	@property
	def minimumNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		"""In order to support addonHandler.addonVersionCheck.SupportsVersionCheck"""
		return self.minNVDAVersion

	@property
	def lastTestedNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		"""In order to support addonHandler.addonVersionCheck.SupportsVersionCheck"""
		return self.lastTestedVersion

	def asdict(self) -> Dict[str, Any]:
		jsonData = dataclasses.asdict(self)
		for field in jsonData:
			# dataclasses.asdict parses NamedTuples to JSON arrays,
			# rather than JSON object dictionaries,
			# which is expected by add-on infrastructure.
			fieldValue = getattr(self, field)
			if isinstance(fieldValue, MajorMinorPatch):
				jsonData[field] = fieldValue._asdict()
		return jsonData


def _createAddonModelFromData(addon: Dict[str, Any]) -> AddonDetailsModel:
	return AddonDetailsModel(
		addonId=addon["addonId"],
		displayName=addon["displayName"],
		description=addon["description"],
		publisher=addon["publisher"],
		channel=Channel(addon["channel"]),
		addonVersionName=addon["addonVersionName"],
		addonVersionNumber=MajorMinorPatch(**addon["addonVersionNumber"]),
		homepage=addon.get("homepage"),
		license=addon["license"],
		licenseURL=addon.get("licenseURL"),
		sourceURL=addon["sourceURL"],
		URL=addon["URL"],
		sha256=addon["sha256"],
		minNVDAVersion=MajorMinorPatch(**addon["minNVDAVersion"]),
		lastTestedVersion=MajorMinorPatch(**addon["lastTestedVersion"]),
	)


def _createModelFromData(jsonData: str) -> List[AddonDetailsModel]:
	"""Use json string to construct a listing of available addons.
	See https://github.com/nvaccess/addon-datastore#api-data-generation-details
	for details of the data.
	"""
	data: List[Dict[str, Any]] = json.loads(jsonData)
	return [_createAddonModelFromData(addon) for addon in data]
