import collections
import os
import pickle
from typing import Dict, Set, Union

import NVDAState
import addonAPIVersion
from addonStore.models.status import AddonStateCategory, WritePaths
from addonStore.models.version import MajorMinorPatch
from logHandler import log
from utils.caseInsensitiveCollections import CaseInsensitiveSet


AddonStateDictT = Dict[AddonStateCategory, CaseInsensitiveSet[str]]


class AddonsState(collections.UserDict[AddonStateCategory, CaseInsensitiveSet[str]]):
	"""
	Subclasses `collections.UserDict` to preserve backwards compatibility.
	AddonStateCategory string enums mapped to a set of the add-on "name/id" currently in that state.
	Add-ons that have the same ID except differ in casing cause a path collision,
	as add-on IDs are installed to a case insensitive path.
	Therefore add-on IDs should be treated as case insensitive.
	"""

	@staticmethod
	def _generateDefaultStateContent() -> AddonStateDictT:
		return {category: CaseInsensitiveSet() for category in AddonStateCategory}

	data: AddonStateDictT
	manualOverridesAPIVersion: MajorMinorPatch

	@property
	def statePath(self) -> os.PathLike:
		"""Returns path to the state file."""
		return WritePaths.addonStateFile

	def setDefaultStateValues(self) -> None:
		self.update(self._generateDefaultStateContent())

		# Set default value for manualOverridesAPIVersion.
		# The ability to override add-ons only appeared in 2023.2,
		# where the BACK_COMPAT_TO API version was 2023.1.0.
		self.manualOverridesAPIVersion = MajorMinorPatch(2023, 1, 0)

	def fromPickledDict(
		self,
		pickledState: Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT, MajorMinorPatch]],
	) -> None:
		# Load from pickledState
		if "backCompatToAPIVersion" in pickledState:
			self.manualOverridesAPIVersion = MajorMinorPatch(*pickledState["backCompatToAPIVersion"])
		for category in AddonStateCategory:
			# Make pickles case insensitive
			self[AddonStateCategory(category)] = CaseInsensitiveSet(pickledState.get(category, set()))

	def toDict(self) -> Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT]]:
		# We cannot pickle instance of `AddonsState` directly
		# since older versions of NVDA aren't aware about this class and they're expecting
		# the state to be using inbuilt data types only.
		picklableState: Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT]] = dict()
		for category in self.data:
			picklableState[category.value] = set(self.data[category])
		picklableState["backCompatToAPIVersion"] = tuple(self.manualOverridesAPIVersion)
		return picklableState

	def load(self) -> None:
		"""Populates state with the default content and then loads values from the config."""
		self.setDefaultStateValues()
		try:
			# #9038: Python 3 requires binary format when working with pickles.
			with open(self.statePath, "rb") as f:
				pickledState: Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT]] = pickle.load(f)
		except FileNotFoundError:
			pass  # Clean config - no point logging in this case
		except IOError:
			log.debug("Error when reading state file", exc_info=True)
		except pickle.UnpicklingError:
			log.debugWarning("Failed to unpickle state", exc_info=True)
		except Exception:
			log.exception()
		else:
			self.fromPickledDict(pickledState)
		if self.manualOverridesAPIVersion != addonAPIVersion.BACK_COMPAT_TO:
			log.debug(
				"BACK_COMPAT_TO API version for manual compatibility overrides has changed. "
				f"NVDA API has been upgraded: from {self.manualOverridesAPIVersion} to {addonAPIVersion.BACK_COMPAT_TO}",
			)
		if self.manualOverridesAPIVersion < addonAPIVersion.BACK_COMPAT_TO:
			# Reset compatibility overrides as the API version has upgraded.
			# For the installer, this is not written to disk.
			# Portable/temporary copies will write this on the first run.
			# Mark overridden compatible add-ons as blocked.
			self[AddonStateCategory.BLOCKED].update(self[AddonStateCategory.OVERRIDE_COMPATIBILITY])
			# Reset overridden compatibility for add-ons that were overridden by older versions of NVDA.
			self[AddonStateCategory.OVERRIDE_COMPATIBILITY].clear()
			self[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].clear()
		self.manualOverridesAPIVersion = MajorMinorPatch(*addonAPIVersion.BACK_COMPAT_TO)

	def removeStateFile(self) -> None:
		if not NVDAState.shouldWriteToDisk():
			log.debugWarning("NVDA should not write to disk from secure mode or launcher", stack_info=True)
			return
		try:
			os.remove(self.statePath)
		except FileNotFoundError:
			pass  # Probably clean config - no point in logging in this case.
		except OSError:
			log.error(f"Failed to remove state file {self.statePath}", exc_info=True)

	def save(self) -> None:
		"""Saves content of the state to a file unless state is empty in which case this would be pointless."""
		if not NVDAState.shouldWriteToDisk():
			log.error("NVDA should not write to disk from secure mode or launcher", stack_info=True)
			return

		if any(self.values()):
			try:
				# #9038: Python 3 requires binary format when working with pickles.
				with open(self.statePath, "wb") as f:
					pickle.dump(self.toDict(), f, protocol=0)
			except (IOError, pickle.PicklingError):
				log.debugWarning("Error saving state", exc_info=True)
		else:
			# Empty state - just delete state file and don't save anything.
			self.removeStateFile()

	def cleanupRemovedDisabledAddons(self) -> None:
		"""Versions of NVDA before #12792 failed to remove add-on from list of disabled add-ons
		during uninstallation. As a result after reinstalling add-on with the same name it was disabled
		by default confusing users. Fix this by removing all add-ons no longer present in the config
		from the list of disabled add-ons in the state."""
		from . import getAvailableAddons

		installedAddonNames = CaseInsensitiveSet(a.name for a in getAvailableAddons())
		for disabledAddonName in CaseInsensitiveSet(self[AddonStateCategory.DISABLED]):
			# Iterate over copy of set to prevent updating the set while iterating over it.
			if disabledAddonName not in installedAddonNames:
				log.debug(f"Discarding {disabledAddonName} from disabled add-ons as it has been uninstalled.")
				self[AddonStateCategory.DISABLED].discard(disabledAddonName)

	def _cleanupCompatibleAddonsFromDowngrade(self) -> None:
		from addonStore.dataManager import addonDataManager

		installedAddons = addonDataManager._installedAddonsCache.installedAddons
		for blockedAddon in CaseInsensitiveSet(
			self[AddonStateCategory.BLOCKED].union(
				self[AddonStateCategory.OVERRIDE_COMPATIBILITY],
			),
		):
			# Iterate over copy of set to prevent updating the set while iterating over it.
			if (
				blockedAddon not in installedAddons
				and blockedAddon not in self[AddonStateCategory.PENDING_INSTALL]
			):
				log.debug(f"Discarding {blockedAddon} from blocked add-ons as it has been uninstalled.")
				self[AddonStateCategory.BLOCKED].discard(blockedAddon)
				self[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(blockedAddon)
			elif installedAddons[blockedAddon].isCompatible:
				log.debug(f"Discarding {blockedAddon} from blocked add-ons as it has become compatible.")
				self[AddonStateCategory.BLOCKED].discard(blockedAddon)
				self[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(blockedAddon)
