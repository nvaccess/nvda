# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import dataclasses
import json
import os
from typing import (
	TYPE_CHECKING,
	Any,
	Dict,
	Generator,
	List,
	Optional,
	Protocol,
	Union,
)

from requests.structures import CaseInsensitiveDict

import addonAPIVersion
from NVDAState import WritePaths

from .channel import Channel
from .status import SupportsAddonState
from .version import (
	MajorMinorPatch,
	SupportsVersionCheck,
)

if TYPE_CHECKING:
	from addonHandler import (  # noqa: F401
		Addon as AddonHandlerModel,
		AddonBase as AddonHandlerBaseModel,
		AddonManifest,
	)
	AddonGUICollectionT = Dict[Channel, CaseInsensitiveDict["_AddonGUIModel"]]
	"""
	Add-ons that have the same ID except differ in casing cause a path collision,
	as add-on IDs are installed to a case insensitive path.
	Therefore addon IDs should be treated as case insensitive.
	"""


AddonHandlerModelGeneratorT = Generator["AddonHandlerModel", None, None]


class _AddonGUIModel(SupportsAddonState, SupportsVersionCheck, Protocol):
	"""Needed to display information in add-on store.
	May come from manifest or add-on store data.
	"""
	addonId: str
	displayName: str
	description: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
	minNVDAVersion: MajorMinorPatch
	lastTestedVersion: MajorMinorPatch
	legacy: bool
	"""
	Legacy add-ons contain invalid metadata
	and should not be accessible through the add-on store.
	"""

	@property
	def minimumNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		"""In order to support SupportsVersionCheck"""
		return self.minNVDAVersion

	@property
	def lastTestedNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		"""In order to support SupportsVersionCheck"""
		return self.lastTestedVersion

	@property
	def _addonHandlerModel(self) -> Optional["AddonHandlerModel"]:
		"""Returns the Addon model tracked in addonHandler, if it exists."""
		from ..dataManager import addonDataManager
		if addonDataManager is None:
			return None
		return addonDataManager._installedAddonsCache.installedAddons.get(self.addonId)

	@property
	def name(self) -> str:
		"""In order to support SupportsVersionCheck"""
		return self.addonId

	@property
	def listItemVMId(self) -> str:
		return f"{self.addonId}-{self.channel}"

	def asdict(self) -> Dict[str, Any]:
		assert dataclasses.is_dataclass(self)
		jsonData = dataclasses.asdict(self)
		for field in jsonData:
			# dataclasses.asdict parses NamedTuples to JSON arrays,
			# rather than JSON object dictionaries,
			# which is expected by add-on infrastructure.
			fieldValue = getattr(self, field)
			if isinstance(fieldValue, MajorMinorPatch):
				jsonData[field] = fieldValue._asdict()
		return jsonData


class _AddonStoreModel(_AddonGUIModel):
	addonId: str
	displayName: str
	description: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
	minNVDAVersion: MajorMinorPatch
	lastTestedVersion: MajorMinorPatch
	legacy: bool
	publisher: str
	license: str
	licenseURL: Optional[str]
	sourceURL: str
	URL: str
	sha256: str
	addonVersionNumber: MajorMinorPatch
	reviewURL: Optional[str]

	@property
	def tempDownloadPath(self) -> str:
		"""
		Path where this add-on should be downloaded to.
		After download completion, the add-on is moved to cachedDownloadPath.
		"""
		return os.path.join(
			WritePaths.addonStoreDownloadDir,
			f"{self.name}.download"
		)

	@property
	def cachedDownloadPath(self) -> str:
		"""
		Path where this add-on file should be cached,
		after a successful download.
		A file at this path may or may not be currently installed to the NVDA system.
		"""
		return os.path.join(
			WritePaths.addonStoreDownloadDir,
			f"{self.name}-{self.addonVersionName}.nvda-addon"
		)

	@property
	def isPendingInstall(self) -> bool:
		"""True if this addon has not yet been fully installed."""
		from ..dataManager import addonDataManager
		assert addonDataManager
		nameInDownloadsPendingInstall = filter(
			lambda m: m[0].model.name == self.name,
			# add-ons which have been downloaded but
			# have not been installed yet
			addonDataManager._downloadsPendingInstall
		)
		return (
			super().isPendingInstall
			# True if this add-on has been downloaded but
			# has not been installed yet
			or bool(next(nameInDownloadsPendingInstall, False))
			# True if this add-on is currently being downloaded
			or os.path.exists(self.tempDownloadPath)
		)


class _AddonManifestModel(_AddonGUIModel):
	"""Get data from an add-on's manifest.
	Can be from an add-on bundle or installed add-on.
	"""
	addonId: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
	minNVDAVersion: MajorMinorPatch
	lastTestedVersion: MajorMinorPatch
	manifest: "AddonManifest"
	legacy: bool = False
	"""
	Legacy add-ons contain invalid metadata
	and should not be accessible through the add-on store.
	"""

	@property
	def displayName(self) -> str:
		return self.manifest["summary"]

	@property
	def description(self) -> str:
		description: Optional[str] = self.manifest.get("description")
		if description is None:
			return ""
		return description

	@property
	def author(self) -> str:
		return self.manifest["author"]


@dataclasses.dataclass(frozen=True)  # once created, it should not be modified.
class AddonManifestModel(_AddonManifestModel):
	"""Get data from an add-on's manifest.
	Can be from an add-on bundle or installed add-on.
	"""
	addonId: str
	addonVersionName: str
	channel: Channel
	homepage: Optional[str]
	minNVDAVersion: MajorMinorPatch
	lastTestedVersion: MajorMinorPatch
	manifest: "AddonManifest"
	legacy: bool = False
	"""
	Legacy add-ons contain invalid metadata
	and should not be accessible through the add-on store.
	"""


@dataclasses.dataclass(frozen=True)  # once created, it should not be modified.
class InstalledAddonStoreModel(_AddonManifestModel, _AddonStoreModel):
	"""
	Data from an add-on installed from the add-on store.
	"""
	addonId: str
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
	reviewURL: Optional[str]
	legacy: bool = False
	"""
	Legacy add-ons contain invalid metadata
	and should not be accessible through the add-on store.
	"""

	@property
	def manifest(self) -> "AddonManifest":
		from ..dataManager import addonDataManager
		assert addonDataManager
		return addonDataManager._installedAddonsCache.installedAddons[self.name].manifest


@dataclasses.dataclass(frozen=True)  # once created, it should not be modified.
class AddonStoreModel(_AddonStoreModel):
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
	reviewURL: Optional[str]
	legacy: bool = False
	"""
	Legacy add-ons contain invalid metadata
	and should not be accessible through the add-on store.
	"""


@dataclasses.dataclass
class CachedAddonsModel:
	cachedAddonData: "AddonGUICollectionT"
	cacheHash: Optional[str]
	cachedLanguage: str
	# AddonApiVersionT or the string .network._LATEST_API_VER
	nvdaAPIVersion: Union[addonAPIVersion.AddonApiVersionT, str]


def _createInstalledStoreModelFromData(addon: Dict[str, Any]) -> InstalledAddonStoreModel:
	return InstalledAddonStoreModel(
		addonId=addon["addonId"],
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
		reviewURL=addon.get("reviewURL"),
		legacy=addon.get("legacy", False),
	)


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
		reviewURL=addon.get("reviewUrl"),
		legacy=addon.get("legacy", False),
	)


def _createGUIModelFromManifest(addon: "AddonHandlerBaseModel") -> AddonManifestModel:
	homepage: Optional[str] = addon.manifest.get("url")
	if homepage == "None":
		# Manifest strings can be set to "None"
		homepage = None
	return AddonManifestModel(
		addonId=addon.name,
		channel=Channel.EXTERNAL,
		addonVersionName=addon.version,
		homepage=homepage,
		minNVDAVersion=MajorMinorPatch(*addon.minimumNVDAVersion),
		lastTestedVersion=MajorMinorPatch(*addon.lastTestedNVDAVersion),
		manifest=addon.manifest,
	)


def _createAddonGUICollection() -> "AddonGUICollectionT":
	"""
	Add-ons that have the same ID except differ in casing cause a path collision,
	as add-on IDs are installed to a case insensitive path.
	Therefore addon IDs should be treated as case insensitive.
	"""
	return {
		channel: CaseInsensitiveDict()
		for channel in Channel
		if channel != Channel.ALL
	}


def _createStoreCollectionFromJson(jsonData: str) -> "AddonGUICollectionT":
	"""Use json string to construct a listing of available addons.
	See https://github.com/nvaccess/addon-datastore#api-data-generation-details
	for details of the data.
	"""
	data: List[Dict[str, Any]] = json.loads(jsonData)
	addonCollection = _createAddonGUICollection()

	for addon in data:
		addonCollection[addon["channel"]][addon["addonId"]] = _createStoreModelFromData(addon)
	return addonCollection
