# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from six.moves import cPickle
import os

import buildVersion
import globalVars
from logHandler import log
from typing import Dict
from . import compatValues


addonCompatState = None  # type: AddonCompatibilityState

def initAddonCompatibilityState():
	global addonCompatState
	addonCompatState = AddonCompatibilityState()

# A named tuple was being used for the version state key, however pickle is unable to save a named tuple.
# https://stackoverflow.com/questions/4677012/python-cant-pickle-type-x-attribute-lookup-failed
def createVersionStateKey(addonName, addonVersion, NVDAVersionTuple):
	# type: (basestring, basestring, tuple) -> dict
	return (addonName, addonVersion, NVDAVersionTuple)

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


CURRENT_NVDA_VERSION = buildVersion.getCurrentVersionTuple()


class AddonCompatibilityState(object):
	"""This class keeps track of the compatibility state for addons.
	State is loaded and saved (using Pickle).
	- Addons that do not have the required support in NVDA are considered incompatible
	- Addons that have been tested against this version of NVDA are considered compatible
	- Addons that have not been tested, are considered to have unknown compatibility."""

	def __init__(
			self,
			statePersistence=AddonCompatibilityStateSaver()
	):
		self._persistence = statePersistence
		state=self._persistence.loadState() # Reef Note: this is a potential source of bugs, if there are several
		# instances of this class state will not be in sync.
		self.addonVersionState = state  # type: Dict[tuple, CompatValues]

	def setAddonCompatibility(
			self,
			addon,
			NVDAVersion=CURRENT_NVDA_VERSION,
			compatibilityStateValue=compatValues.UNKNOWN
	):
		# type: (addonHandler.AddonBase, tuple, CompatValues) -> None
		"""Sets the compatibility for an addon. Does not save the value to file.
		@param NVDAVersion:
		@param addon: The addon to set compatibility for
		@param compatibilityStateValue: Unknown allows falling back to auto deduced value
		@return:
		"""
		acceptedUserSetCompatVals = [
			compatValues.UNKNOWN,
			compatValues.MANUALLY_SET_COMPATIBLE,
			compatValues.MANUALLY_SET_INCOMPATIBLE,
		]
		assert compatibilityStateValue in acceptedUserSetCompatVals

		autoDeduced = self._getAutoDeduducedAddonCompat(addon, NVDAVersion)

		# we only use the provided value if the compatibility can not be automatically deduced.
		if autoDeduced is not compatValues.UNKNOWN:
			self._setAddonCompat(addon, NVDAVersion, autoDeduced)
		else:
			self._setAddonCompat(addon, NVDAVersion, compatibilityStateValue)
		self._persistence.saveState(self.addonVersionState)

	def _setAddonCompat(self, addon, NVDAVersionTuple, compat):
		addonKey = createVersionStateKey(
			addonName=addon.name,
			addonVersion=addon.version,
			NVDAVersionTuple=NVDAVersionTuple
		)
		self.addonVersionState[addonKey] = compat

	def _getAutoDeduducedAddonCompat(self, addon, NVDAVersionTuple):
		if not hasAddonGotRequiredSupport(addon, version=NVDAVersionTuple):
			return compatValues.AUTO_DEDUCED_INCOMPATIBLE
		elif isAddonTested(addon, version=NVDAVersionTuple):
			return compatValues.AUTO_DEDUCED_COMPATIBLE
		else:
			return compatValues.UNKNOWN

	def getAddonCompatibility(self, addon, NVDAVersionTuple=CURRENT_NVDA_VERSION):
		"""
		Get the addon compatibility for a given version of NVDA
		@param addon: The addon to check for compatibility
		@param NVDAVersionTuple: The NVDA version tuple eg (2018.1.1)
		@return: CompatValues
		"""
		autoCompat = self._getAutoDeduducedAddonCompat(addon, NVDAVersionTuple)
		if autoCompat is not compatValues.UNKNOWN:
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

def hasAddonGotRequiredSupport(addon, version=CURRENT_NVDA_VERSION):
	"""True if this add-on is supported by the given version of NVDA.
	This method returns False if the supported state is unsure, e.g. because the minimumNVDAVersion manifest key is missing.
	By default, the current version of NVDA is evaluated.
	"""
	# If minimumNVDAVersion is None, it will always be less than the current NVDA version.
	# Therefore, we should account for this.
	minVersion = addon.minimumNVDAVersion
	return bool(minVersion) and minVersion <= version


def isAddonTested(addon, version=CURRENT_NVDA_VERSION):
	"""True if this add-on is tested for the given version of NVDA.
	By default, the current version of NVDA is evaluated.
	"""
	return hasAddonGotRequiredSupport(addon, version) and addon.lastTestedNVDAVersion >= version

def isAddonConsideredIncompatible(addon, version=CURRENT_NVDA_VERSION):
	return not isAddonConsideredIncompatible(addon, version)

def isAddonConsideredCompatible(addon, version=CURRENT_NVDA_VERSION):
	compat = addonCompatState.getAddonCompatibility(addon, version)
	return bool(compat & compatValues.COMPATIBLE_BIT)

def isAddonCompatibilityKnown(addon, version=CURRENT_NVDA_VERSION):
	compat = addonCompatState.getAddonCompatibility(addon, version)
	return bool(compat & compatValues.KNOWN_MASK)
