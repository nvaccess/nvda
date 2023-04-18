# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Needed for type hinting CaseInsensitiveDict
# Can be removed in a future version of python (3.8+)
from __future__ import annotations

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
from typing_extensions import (
	Protocol,
)

from requests.structures import CaseInsensitiveDict

import addonAPIVersion
from addonHandler import (
	Addon as AddonHandlerModel,
	state as addonHandlerState,
)
from addonHandler.addonVersionCheck import SupportsVersionCheck


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

	@classmethod
	def _parseVersionFromVersionStr(cls, version: str) -> "MajorMinorPatch":
		versionParts = version.split(".")
		versionLen = len(versionParts)
		if versionLen < 2 or versionLen > 3:
			raise ValueError(f"Version string not valid: {version}")
		return cls(
			int(versionParts[0]),
			int(versionParts[1]),
			0 if len(versionParts) == 2 else int(versionParts[2])
		)


class _AddonDetailsModel(SupportsVersionCheck, Protocol):
	"""Needed to display information in add-on store.
	May come from manifest or add-on store data.
	"""
	addonId: str
	displayName: str
	description: str
	publisher: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
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

	@property
	def _addonHandlerModel(self) -> Optional[AddonHandlerModel]:
		"""Returns the Addon model tracked in addonHandler, if it exists."""
		return addonHandlerState._addonHandlerCache.availableAddons.get(self.addonId)

	@property
	def name(self) -> str:
		"""In order to support addonHandler.addonVersionCheck.SupportsVersionCheck"""
		return self.addonId

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


@dataclasses.dataclass(frozen=True)
class AddonDetailsModel(_AddonDetailsModel):
	"""Needed to display information in add-on store GUI.
	May come from manifest or add-on store data.
	"""
	addonId: str
	displayName: str
	description: str
	publisher: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
	minNVDAVersion: MajorMinorPatch
	lastTestedVersion: MajorMinorPatch


@dataclasses.dataclass(frozen=True)  # once created, it should not be modified.
class AddonStoreModel(_AddonDetailsModel):
	"""
	Data from an add-on from the add-on store.
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


def _createStoreModelFromData(addon: Dict[str, Any]) -> AddonStoreModel:
	return AddonStoreModel(
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


def _createDetailsFromManifest(addon: AddonHandlerModel) -> AddonDetailsModel:
	return AddonDetailsModel(
		addonId=addon.name,
		displayName=addon.manifest["summary"],
		description=addon.manifest["description"],
		publisher=addon.manifest["author"],
		channel=Channel.STABLE,
		addonVersionName=addon.version,
		homepage=addon.manifest.get("url"),
		minNVDAVersion=MajorMinorPatch(*addon.minimumNVDAVersion),
		lastTestedVersion=MajorMinorPatch(*addon.lastTestedNVDAVersion),
	)


def _createStoreCollectionFromJson(jsonData: str) -> CaseInsensitiveDict["AddonStoreModel"]:
	"""Use json string to construct a listing of available addons.
	See https://github.com/nvaccess/addon-datastore#api-data-generation-details
	for details of the data.
	"""
	data: List[Dict[str, Any]] = json.loads(jsonData)
	return CaseInsensitiveDict({addon["addonId"]: _createStoreModelFromData(addon) for addon in data})
