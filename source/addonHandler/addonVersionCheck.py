# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import addonAPIVersion

def hasAddonGotRequiredSupport(addon, currentAPIVersion=addonAPIVersion.CURRENT):
	"""True if NVDA provides the add-on with an API version high enough to meet the add-on's minimum requirements
	"""
	minVersion = addon.minimumNVDAVersion
	return minVersion <= currentAPIVersion


def isAddonTested(addon, backwardsCompatToVersion=addonAPIVersion.BACK_COMPAT_TO):
	"""True if this add-on is tested for the given API version.
	By default, the current version of NVDA is evaluated.
	"""
	return addon.lastTestedNVDAVersion >= backwardsCompatToVersion


def isAddonCompatible(
		addon,
		currentAPIVersion=addonAPIVersion.CURRENT,
		backwardsCompatToVersion=addonAPIVersion.BACK_COMPAT_TO
):
	"""Tests if the addon is compatible.
	The compatibility is defined by having the required features in NVDA, and by having been tested / built against
	an API version that is still supported by this version of NVDA.
	"""
	return hasAddonGotRequiredSupport(addon, currentAPIVersion) and isAddonTested(addon, backwardsCompatToVersion)
