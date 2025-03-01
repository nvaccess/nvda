from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

import addonAPIVersion

if TYPE_CHECKING:
	from addonStore.models.addon import AddonManifestModel, InstalledAddonStoreModel
from addonStore.models.status import SupportsAddonState
from addonStore.models.version import SupportsVersionCheck

from .AddonManifest import AddonManifest


class AddonBase(SupportsAddonState, SupportsVersionCheck, ABC):
	"""The base class for functionality that is available both for add-on bundles and add-ons on the file system.
	Subclasses should at least implement L{manifest}.
	"""

	@property
	def name(self) -> str:
		"""A unique name, the id of the add-on."""
		return self.manifest["name"]

	@property
	def version(self) -> str:
		"""A display version. Not necessarily semantic"""
		return self.manifest["version"]

	@property
	def minimumNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		return self.manifest.get("minimumNVDAVersion")

	@property
	def lastTestedNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		return self.manifest.get("lastTestedNVDAVersion")

	@property
	@abstractmethod
	def manifest(self) -> "AddonManifest": ...

	@property
	def _addonStoreData(self) -> Optional["InstalledAddonStoreModel"]:
		from addonStore.dataManager import addonDataManager

		assert addonDataManager
		return addonDataManager._getCachedInstalledAddonData(self.name)

	@property
	def _addonGuiModel(self) -> "AddonManifestModel":
		from addonStore.models.addon import _createGUIModelFromManifest

		return _createGUIModelFromManifest(self)


class AddonError(Exception):
	"""Represents an exception coming from the addon subsystem."""
