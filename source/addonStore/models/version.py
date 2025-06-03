# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2024 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	NamedTuple,
	Optional,
	Protocol,
)
import addonAPIVersion


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
			0 if len(versionParts) == 2 else int(versionParts[2]),
		)


class SupportsVersionCheck(Protocol):
	"""Examples implementing this protocol include:
	- addonHandler.Addon
	- addonHandler.AddonBundle
	- addonStore.models._AddonGUIModel
	- addonStore.models._AddonStoreModel
	- addonStore.models.AddonManifestModel
	- addonStore.models.AddonStoreModel
	- addonStore.models.InstalledAddonStoreModel
	"""

	minimumNVDAVersion: addonAPIVersion.AddonApiVersionT
	lastTestedNVDAVersion: addonAPIVersion.AddonApiVersionT
	name: str

	@property
	def _hasOverriddenCompat(self) -> bool:
		"""If True, this add-on has been manually overriden. The affects of override may be pending restart"""
		import addonHandler
		from addonStore.models.status import AddonStateCategory

		return (
			self.name in addonHandler.state[AddonStateCategory.OVERRIDE_COMPATIBILITY]
			or self.name in addonHandler.state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY]
		)

	@property
	def overrideIncompatibility(self) -> bool:
		"""If True, NVDA should enable this add-on where it would normally be blocked due to incompatibility."""
		from addonHandler import AddonStateCategory, state

		return self.name in state[AddonStateCategory.OVERRIDE_COMPATIBILITY] and self.canOverrideCompatibility

	def enableCompatibilityOverride(self):
		"""
		Should be reset when changing to a new breaking release,
		and when this add-on is updated, disabled or removed.
		"""
		from addonHandler import AddonStateCategory, state

		if self.name in state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY]:
			raise RuntimeError(f"{self.name} is already pending override compatibility.")
		assert self.canOverrideCompatibility
		state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].add(self.name)
		state[AddonStateCategory.BLOCKED].discard(self.name)
		state[AddonStateCategory.DISABLED].discard(self.name)

	@property
	def canOverrideCompatibility(self) -> bool:
		from addonHandler.addonVersionCheck import hasAddonGotRequiredSupport, isAddonTested

		return hasAddonGotRequiredSupport(self) and not isAddonTested(self)

	@property
	def _isTested(self) -> bool:
		from addonHandler.addonVersionCheck import isAddonTested

		return isAddonTested(self)

	@property
	def _hasGotRequiredSupport(self) -> bool:
		from addonHandler.addonVersionCheck import hasAddonGotRequiredSupport

		return hasAddonGotRequiredSupport(self)

	@property
	def isCompatible(self) -> bool:
		return self._isTested and self._hasGotRequiredSupport

	def getIncompatibleReason(
		self,
		backwardsCompatToVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.BACK_COMPAT_TO,
		currentAPIVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.CURRENT,
	) -> Optional[str]:
		from addonHandler.addonVersionCheck import hasAddonGotRequiredSupport, isAddonTested

		if not hasAddonGotRequiredSupport(self, currentAPIVersion):
			return pgettext(
				"addonStore",
				# Translators: The reason an add-on is not compatible.
				# A more recent version of NVDA is required for the add-on to work.
				# The placeholder will be replaced with Year.Major.Minor (e.g. 2019.1).
				"An updated version of NVDA is required. NVDA version {nvdaVersion} or later.",
			).format(
				nvdaVersion=addonAPIVersion.formatForGUI(self.minimumNVDAVersion),
			)
		elif not isAddonTested(self, backwardsCompatToVersion):
			return pgettext(
				"addonStore",
				# Translators: The reason an add-on is not compatible.
				# The addon relies on older, removed features of NVDA, an updated add-on is required.
				# The placeholder will be replaced with Year.Major.Minor (e.g. 2019.1).
				"An updated version of this add-on is required. "
				"This add-on was last tested with NVDA {lastTestedNVDAVersion}. "
				"NVDA requires this add-on to be tested with NVDA {nvdaVersion} or higher. "
				"You can enable this add-on at your own risk. ",
			).format(
				nvdaVersion=addonAPIVersion.formatForGUI(backwardsCompatToVersion),
				lastTestedNVDAVersion=addonAPIVersion.formatForGUI(self.lastTestedNVDAVersion),
			)
		else:
			return None


def getAddonCompatibilityMessage() -> str:
	return pgettext(
		"addonStore",
		# Translators: A message indicating that some add-ons will be disabled
		# unless reviewed before installation.
		"Your NVDA configuration contains add-ons that are incompatible with this version of NVDA. "
		"These add-ons will be disabled after installation. "
		"After installation, you will be able to manually re-enable these add-ons at your own risk. "
		"If you rely on these add-ons, please review the list to decide whether to continue with the installation. ",
	)


def getAddonCompatibilityConfirmationMessage() -> str:
	return pgettext(
		"addonStore",
		# Translators: A message to confirm that the user understands that incompatible add-ons
		# will be disabled after installation, and can be manually re-enabled.
		"I understand that incompatible add-ons will be disabled "
		"and can be manually re-enabled at my own risk after installation.",
	)
