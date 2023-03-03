# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Optional,
)
from typing_extensions import Protocol  # Python 3.8 adds native support

import addonAPIVersion
from addonStore.models import Channel
from buildVersion import isPreReleaseVersion


class SupportsVersionCheck(Protocol):
	""" Examples implementing this protocol include:
	- addonHandler.AddonBundle
	- addonStore.models.AddonDetailsModel
	"""
	minimumNVDAVersion: addonAPIVersion.AddonApiVersionT
	lastTestedNVDAVersion: addonAPIVersion.AddonApiVersionT
	channel: Optional[Channel]


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
	Dev add-ons are made available to any pre-release version of NVDA.
	"""
	if addon.channel == Channel.DEV:
		# Allow dev add-ons for pre-release versions
		return isPreReleaseVersion
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
