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
from . import compatValues
import addonAPIVersion

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
	_persistence = None
	_addonVersionState = None

	@classmethod
	def initialise(
			cls,
			statePersistence=AddonCompatibilityStateSaver(),
			forceReInit=False
	):
		# don't auto re-init
		if cls._addonVersionState is not None and not forceReInit:
			return
		cls._persistence = statePersistence
		state = cls._persistence.loadState()
		cls._addonVersionState = state  # type: dict[tuple, CompatValues]

	@classmethod
	def setAddonCompatibility(
			cls,
			addon,
			NVDAVersion=CURRENT_NVDA_VERSION,
			compatibilityStateValue=compatValues.UNKNOWN
	):
		# type: (addonHandler.AddonBase, tuple, CompatValues) -> None
		"""Sets the compatibility for an addon. Does not save the value to file.
		@param NVDAVersion:
		@param addon: The addon to set compatibility for
		@param compatibilityStateValue: UNKNOWN allows falling back to auto deduced value. Must be either UNKNOWN,
		MANUALLY_SET_COMPATIBLE, or MANUALLY_SET_INCOMPATIBLE
		"""
		cls.initialise()
		acceptedUserSetCompatVals = [
			compatValues.UNKNOWN,
			compatValues.MANUALLY_SET_COMPATIBLE,
			compatValues.MANUALLY_SET_INCOMPATIBLE,
		]
		assert compatibilityStateValue in acceptedUserSetCompatVals

		autoDeduced = cls._getAutoDeduducedAddonCompat(addon, NVDAVersion)

		# we only use the provided value if the compatibility can not be automatically deduced.
		if autoDeduced is not compatValues.UNKNOWN:
			cls._setAddonCompat(addon, NVDAVersion, autoDeduced)
		else:
			cls._setAddonCompat(addon, NVDAVersion, compatibilityStateValue)
		cls._persistence.saveState(cls._addonVersionState)

	@classmethod
	def _setAddonCompat(cls, addon, NVDAVersionTuple, compat):
		addonKey = createVersionStateKey(
			addonName=addon.name,
			addonVersion=addon.version,
			NVDAVersionTuple=NVDAVersionTuple
		)
		cls._addonVersionState[addonKey] = compat

	@classmethod
	def _getAutoDeduducedAddonCompat(cls, addon, NVDAVersionTuple):
		if not hasAddonGotRequiredSupport(addon, version=NVDAVersionTuple):
			return compatValues.AUTO_DEDUCED_INCOMPATIBLE
		elif isAddonTested(addon, version=NVDAVersionTuple):
			return compatValues.AUTO_DEDUCED_COMPATIBLE
		else:
			return compatValues.UNKNOWN

	@classmethod
	def getAddonCompatibility(cls, addon, NVDAVersionTuple=CURRENT_NVDA_VERSION):
		"""
		Get the addon compatibility for a given version of NVDA
		@param addon: The addon to check for compatibility
		@param NVDAVersionTuple: The NVDA version tuple eg (2018.1.1)
		@return: CompatValues
		"""
		cls.initialise()
		autoCompat = cls._getAutoDeduducedAddonCompat(addon, NVDAVersionTuple)
		if autoCompat is not compatValues.UNKNOWN:
			return autoCompat

		addonKey = createVersionStateKey(
			addonName=addon.name,
			addonVersion=addon.version,
			NVDAVersionTuple=NVDAVersionTuple
		)
		try:
			return cls._addonVersionState[addonKey]
		except KeyError:
			return autoCompat

def hasAddonGotRequiredSupport(addon, version=CURRENT_NVDA_VERSION):
	"""True if this add-on is supported by the given version of NVDA.
	This method returns True if the supported state is unsure, e.g. because the minimumNVDAVersion manifest key is
	missing. A missing manifest key likely means that the add-on has not been updated since the introduction of
	the add-on version check feature in 2018.4. We assume support is present in this case to minimise the impact
	of this feature to users. This behaviour may change in the future.
	By default, the current version of NVDA is evaluated.
	"""
	# If minimumNVDAVersion is None, it will always be less than the current NVDA version.
	minVersion = addon.minimumNVDAVersion
	return minVersion <= version


def isAddonTested(addon, version=CURRENT_NVDA_VERSION):
	"""True if this add-on is tested for the given version of NVDA.
	By default, the current version of NVDA is evaluated.
	"""
	# Hard code minor to zero, so minor updates are not considered new versions.
	# Minor updates are very unlikely to cause incompatibility.
	version = (version[0], version[1], 0)  # Year, major, minor
	# if lastTestedNVDAVersion is None it will be less than version.
	return hasAddonGotRequiredSupport(addon, version) and addon.lastTestedNVDAVersion >= version

def isAddonConsideredIncompatible(addon, version=CURRENT_NVDA_VERSION):
	return not isAddonConsideredCompatible(addon, version)

def isAddonConsideredCompatible(addon, version=CURRENT_NVDA_VERSION):
	compat = AddonCompatibilityState.getAddonCompatibility(addon, version)
	return bool(compat & compatValues.COMPATIBLE_BIT)

def isCompatSetManually(addon, version=CURRENT_NVDA_VERSION):
	compat = AddonCompatibilityState.getAddonCompatibility(addon, version)
	return bool(compat & compatValues.MANUALLY_SET_BIT)

def isAddonCompatibilityKnown(addon, version=CURRENT_NVDA_VERSION):
	compat = AddonCompatibilityState.getAddonCompatibility(addon, version)
	return bool(compat & compatValues.KNOWN_MASK)
