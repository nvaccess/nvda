# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import cPickle
import os
from collections import namedtuple

import buildVersion
import globalVars
from logHandler import log
from typing import Dict


addonCompatState = None  # type: AddonCompatibilityState

def initAddonCompatibilityState():
	global addonCompatState
	addonCompatState = AddonCompatibilityState()

# A named tuple was being used for the version state key, however pickle is unable to save a named tuple.
# https://stackoverflow.com/questions/4677012/python-cant-pickle-type-x-attribute-lookup-failed
def createVersionStateKey(addonName, addonVersion, NVDAVersionTuple):
	# type: (basestring, basestring, tuple) -> dict
	return (addonName, addonVersion, NVDAVersionTuple)

class CompatValues(object):
	(
		Unknown,
		Compatible,
		Incompatible,
		ManuallySetCompatible,
		ManuallySetIncompatible
	) = range(5)

	IncompatibleValuesSet = [Unknown, Incompatible, ManuallySetIncompatible]
	CompatibleValuesSet = [Compatible, ManuallySetCompatible]
	AutoDeducedValuesSet = [Unknown, Compatible, Incompatible]
	ManualValuesSet = [ManuallySetCompatible, ManuallySetIncompatible]
	UserInterventionSet = [Unknown, ManuallySetIncompatible, ManuallySetCompatible]

class AddonCompatibilityStateSaver(object):

	STATE_FILENAME = "addonVersionCheckState.pickle"
	PICKLED_STATE_NAME = "versionCompatibilityState"

	def loadState(self):
		statePath = os.path.join(globalVars.appArgs.configPath, self.STATE_FILENAME)
		try:
			with open(statePath, "r") as f:
				state = cPickle.load(f)
				return state.get(self.PICKLED_STATE_NAME, {})
		except IOError:
			log.debug("Can't open addonVersion pickle", exc_info=True)
		except cPickle.PickleError:
			log.debugWarning("Error loading version check state", exc_info=True)
		return {}

	def saveState(self, addonVersionState):
		# We put the addonVersionState into a dictionary entry as a simple heuristic that the file contains the data we
		# expect.
		state = {self.PICKLED_STATE_NAME: addonVersionState}
		statePath = os.path.join(globalVars.appArgs.configPath, self.STATE_FILENAME)
		try:
			with open(statePath, "wb") as f:
				cPickle.dump(state, f)
		except IOError:
			pass
		except cPickle.PickleError:
			log.debugWarning("Error saving version check state", exc_info=True)


class AddonCompatibilityState(object):
	"""This class keeps track of the compatibility state for addons.
	State is loaded and saved (using Pickle).
	- Addons that do not have the required support in NVDA are considered incompatible
	- Addons that have been tested against this version of NVDA are considered compatible
	- Addons that have not been tested, are considered to have unknown compatibility."""

	def __init__(
			self,
			NVDAVersionTuple=buildVersion.getNextReleaseVersionTuple(),
			statePersistance = AddonCompatibilityStateSaver()
	):
		self.NVDAVersionTuple = NVDAVersionTuple
		self._persistence = statePersistance
		state = self._persistence.loadState() # Reef Note: this is a potential source of bugs, if there are several
		# instances of this class state will not be in sync.
		self.addonVersionState = state  # type: Dict[tuple, CompatValues]

	def setAddonCompatibility(self, addon, compatibilityStateValue=CompatValues.Unknown):
		# type: (addonHandler.AddonBase, CompatValues) -> None
		"""

		:param addon:
		:param compatibilityStateValue: unknown allows falling back to auto deduced value
		:return:
		"""
		acceptedUserSetCompatVals = [
			CompatValues.Unknown,
			CompatValues.ManuallySetCompatible,
			CompatValues.ManuallySetIncompatible,
		]
		assert compatibilityStateValue in acceptedUserSetCompatVals

		addonCompat = self._getAutoDeduducedAddonCompat(addon)

		# we only use the provided value if the compatibility can not be automatically deduced.
		if addonCompat is not CompatValues.Unknown:
			self._setAddonCompat(addon, addonCompat)
		else:
			self._setAddonCompat(addon, compatibilityStateValue)

	def _setAddonCompat(self, addon, compat):
		addonKey = createVersionStateKey(
			addonName=addon.name,
			addonVersion=addon.version,
			NVDAVersionTuple=self.NVDAVersionTuple
		)
		self.addonVersionState[addonKey] = compat
		self._persistence.saveState(self.addonVersionState)

	def _getAutoDeduducedAddonCompat(self, addon):
		if not hasAddonGotRequiredSupport(addon, version=self.NVDAVersionTuple):
			return CompatValues.Incompatible
		elif isAddonTested(addon, version=self.NVDAVersionTuple):
			return CompatValues.Compatible
		else:
			return CompatValues.Unknown

	def getAddonCompatibilityForNVDAVersion(self, addon, NVDAVersionTuple):
		"""
		:type addon: addonHandler.Addon
		"""
		autoCompat = self._getAutoDeduducedAddonCompat(addon)
		if autoCompat is not CompatValues.Unknown:
			return autoCompat

		addonKey = createVersionStateKey(
			addonName=addon.name,
			addonVersion=addon.version,
			NVDAVersionTuple=NVDAVersionTuple
		)
		try:
			return self.addonVersionState[addonKey]
		except KeyError:
			return autoCompat

	def getAddonCompatibility(self, addon):
		return self.getAddonCompatibilityForNVDAVersion(addon, self.NVDAVersionTuple)

DEFAULT_NVDA_VERSION = buildVersion.getNextReleaseVersionTuple()

def hasAddonGotRequiredSupport(addon, version=DEFAULT_NVDA_VERSION):
	"""True if this add-on is supported by the given version of NVDA.
	This method returns False if the supported state is unsure, e.g. because the minimumNVDAVersion manifest key is missing.
	By default, the current version of NVDA is evaluated.
	"""
	# If minimumNVDAVersion is None, it will always be less than the current NVDA version.
	# Therefore, we should account for this.
	minVersion = addon.minimumNVDAVersion
	return bool(minVersion) and minVersion <= version


def isAddonTested(addon, version=DEFAULT_NVDA_VERSION):
	"""True if this add-on is tested for the given version of NVDA.
	By default, the current version of NVDA is evaluated.
	"""
	return hasAddonGotRequiredSupport(addon, version) and addon.lastTestedNVDAVersion >= version

def isAddonConsideredIncompatible(addon, version=buildVersion.getNextReleaseVersionTuple()):
	return addonCompatState.getAddonCompatibilityForNVDAVersion(addon, version) in CompatValues.IncompatibleValuesSet

def isAddonConsideredCompatible(addon, version=buildVersion.getNextReleaseVersionTuple()):
	return addonCompatState.getAddonCompatibilityForNVDAVersion(addon, version) in CompatValues.CompatibleValuesSet

def isAddonCompatibilityKnown(addon, version=buildVersion.getNextReleaseVersionTuple()):
	return CompatValues.Unknown != addonCompatState.getAddonCompatibilityForNVDAVersion(addon, version)