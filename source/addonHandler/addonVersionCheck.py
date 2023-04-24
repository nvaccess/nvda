# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Optional
from typing_extensions import Protocol  # Python 3.8 adds native support
import addonAPIVersion


def getAddonCompatibilityMessage() -> str:
	return pgettext(
		"addonStore",
		# Translators: A message indicating that some add-ons will be disabled
		# unless reviewed before installation.
		"Your NVDA configuration contains add-ons that are incompatible with this version of NVDA. "
		"These add-ons will be disabled after installation. "
		"After installation, you will be able to manually re-enable these add-ons at your own risk. "
		"If you rely on these add-ons, please review the list to decide whether to continue with the installation. "
	)


def getAddonCompatibilityConfirmationMessage() -> str:
	return pgettext(
		"addonStore",
		# Translators: A message to confirm that the user understands that incompatible add-ons
		# will be disabled after installation, and can be manually re-enabled.
		"I understand that incompatible add-ons will be disabled "
		"and can be manually re-enabled at my own risk after installation."
	)


class SupportsVersionCheck(Protocol):
	""" Examples implementing this protocol include:
	- addonHandler.Addon
	- addonHandler.AddonBundle
	- addonStore.models.AddonDetailsModel
	- addonStore.models.AddonStoreModel
	"""
	minimumNVDAVersion: addonAPIVersion.AddonApiVersionT
	lastTestedNVDAVersion: addonAPIVersion.AddonApiVersionT
	name: str

	@property
	def overrideIncompatibility(self) -> bool:
		from addonHandler import AddonStateCategory, state
		return (
			self.name in state[AddonStateCategory.OVERRIDE_COMPATIBILITY]
			and self.canOverrideCompatibility
		)

	def enableCompatibilityOverride(self):
		"""
		Should be reset when changing to a new breaking release,
		and when this add-on is updated, disabled or removed.
		"""
		from addonHandler import AddonStateCategory, state
		overiddenAddons = state[AddonStateCategory.OVERRIDE_COMPATIBILITY]
		assert self.name not in overiddenAddons and self.canOverrideCompatibility
		overiddenAddons.add(self.name)
		state[AddonStateCategory.BLOCKED].discard(self.name)
		state[AddonStateCategory.DISABLED].discard(self.name)

	@property
	def canOverrideCompatibility(self) -> bool:
		return hasAddonGotRequiredSupport(self) and not isAddonTested(self)

	def getIncompatibleReason(
			self,
			backwardsCompatToVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.BACK_COMPAT_TO,
			currentAPIVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.CURRENT,
	) -> Optional[str]:
		if not hasAddonGotRequiredSupport(self, currentAPIVersion):
			return pgettext(
				"addonStore",
				# Translators: The reason an add-on is not compatible.
				# A more recent version of NVDA is required for the add-on to work.
				# The placeholder will be replaced with Year.Major.Minor (e.g. 2019.1).
				"An updated version of NVDA is required. "
				"NVDA version {nvdaVersion} or later."
				).format(
			nvdaVersion=addonAPIVersion.formatForGUI(self.minimumNVDAVersion)
			)
		elif not isAddonTested(self, backwardsCompatToVersion):
			# Translators: The reason an add-on is not compatible. The addon relies on older, removed features of NVDA,
			# an updated add-on is required. The placeholder will be replaced with Year.Major.Minor (EG 2019.1).
			return pgettext(
				"addonStore",
				"An updated version of this add-on is required. "
				"The minimum supported API version is now {nvdaVersion}. "
				"This add-on was last tested with {lastTestedNVDAVersion}. "
				"You can enable this add-on at your own risk. "
				).format(
			nvdaVersion=addonAPIVersion.formatForGUI(backwardsCompatToVersion),
			lastTestedNVDAVersion=addonAPIVersion.formatForGUI(self.lastTestedNVDAVersion),
			)
		else:
			return None


def hasAddonGotRequiredSupport(
		addon: SupportsVersionCheck,
		currentAPIVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.CURRENT
) -> bool:
	"""True if NVDA provides the add-on with an API version high enough to meet the add-on's minimum requirements
	"""
	minVersion = addon.minimumNVDAVersion
	return minVersion <= currentAPIVersion


def isAddonTested(
		addon: SupportsVersionCheck,
		backwardsCompatToVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.BACK_COMPAT_TO
) -> bool:
	"""True if this add-on is tested for the given API version.
	By default, the current version of NVDA is evaluated.
	"""
	return addon.lastTestedNVDAVersion >= backwardsCompatToVersion


def isAddonCompatible(
		addon: SupportsVersionCheck,
		currentAPIVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.CURRENT,
		backwardsCompatToVersion: addonAPIVersion.AddonApiVersionT = addonAPIVersion.BACK_COMPAT_TO
) -> bool:
	"""Tests if the addon is compatible.
	The compatibility is defined by having the required features in NVDA, and by having been tested / built against
	an API version that is still supported by this version of NVDA.
	"""
	return hasAddonGotRequiredSupport(addon, currentAPIVersion) and isAddonTested(addon, backwardsCompatToVersion)
