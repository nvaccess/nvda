#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited

"""Unit tests for the addonVersionCheck module."""

import unittest

import addonAPIVersion
import versionInfo
from addonHandler import AddonBase
from addonHandler import addonVersionCheck
from addonHandler import compatValues
from addonHandler.addonVersionCheck import AddonCompatibilityState

def versionString(version):
	return "{}.{}.{}".format(*version)

CurrentNVDAVersionTuple = (2018, 2, 0)
NextNVDAVersionTuple = (2018, 3, 0)
LastNVDAVersionTuple = (2018, 1, 0)

CurrentNVDAVersionString = versionString(CurrentNVDAVersionTuple)
NextNVDAVersionString = versionString(NextNVDAVersionTuple)
LastNVDAVersionString = versionString(LastNVDAVersionTuple)

class mockAddon(AddonBase):
	def __init__(
			self,
			name="mockAddon",
			version="1.0",
			minNVDAVersion=LastNVDAVersionString,
			lastTestedNVDAVersion=CurrentNVDAVersionString
	):
		super(mockAddon, self).__init__()
		self._name = name
		self._version = version
		self._minNVDAVersion = None
		if minNVDAVersion:
			self._minNVDAVersion = versionInfo.getNVDAVersionTupleFromString(minNVDAVersion)
		self._lastTestedNVDAVersion = None
		if lastTestedNVDAVersion:
			self._lastTestedNVDAVersion = versionInfo.getNVDAVersionTupleFromString(lastTestedNVDAVersion)

	@AddonBase.name.getter
	def name(self):
		return self._name

	@AddonBase.version.getter
	def version(self):
		return self._version

	@AddonBase.minimumNVDAVersion.getter
	def minimumNVDAVersion(self):
		return self._minNVDAVersion

	@AddonBase.lastTestedNVDAVersion.getter
	def lastTestedNVDAVersion(self):
		return self._lastTestedNVDAVersion

class TestAddonVersionCheck(unittest.TestCase):
	"""Tests that the addon version check works as expected."""

	def test_addonWithUpToDateTesting(self):
		uptoDate = mockAddon()
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(uptoDate, CurrentNVDAVersionTuple))
		self.assertTrue(addonVersionCheck.isAddonTested(uptoDate, CurrentNVDAVersionTuple))

	def test_addonUntestedWithSupport(self):
		addonNotTested = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(addonNotTested, CurrentNVDAVersionTuple))
		self.assertFalse(addonVersionCheck.isAddonTested(addonNotTested, CurrentNVDAVersionTuple))

	def test_addonWithoutNVDASupportTested(self):
		addonNvdaDoesntSupport = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.assertFalse(addonVersionCheck.hasAddonGotRequiredSupport(addonNvdaDoesntSupport, CurrentNVDAVersionTuple))
		self.assertFalse(addonVersionCheck.isAddonTested(addonNvdaDoesntSupport, CurrentNVDAVersionTuple))

	def test_addonWithoutNVDASupportUntested(self):
		addonNvdaDoesntSupport = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		self.assertFalse(addonVersionCheck.hasAddonGotRequiredSupport(addonNvdaDoesntSupport, CurrentNVDAVersionTuple))
		self.assertFalse(addonVersionCheck.isAddonTested(addonNvdaDoesntSupport, CurrentNVDAVersionTuple))

	def test_addonMissingNVDASupportField(self):
		addonNoMinNVDAVer = mockAddon(minNVDAVersion=None)
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(addonNoMinNVDAVer, CurrentNVDAVersionTuple))
		self.assertTrue(addonVersionCheck.isAddonTested(addonNoMinNVDAVer, CurrentNVDAVersionTuple))

	def test_addonMissingLastTestedField(self):
		addonNoLastTested = mockAddon(lastTestedNVDAVersion=None)
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(addonNoLastTested, CurrentNVDAVersionTuple))
		self.assertFalse(addonVersionCheck.isAddonTested(addonNoLastTested, CurrentNVDAVersionTuple))

class TestAddonCompatibilityState(unittest.TestCase):

	class MockStateSaver(object):
		def __init__(self, NVDAVersionTuple):
			self.NVDAVersion = NVDAVersionTuple
			self.state = {}

		def setReturnOnLoad(self, addon, compat):
			"""Mock method, used to control the behaviour of the loadState method"""
			addonKey = addonVersionCheck.createVersionStateKey(
					addonName=addon.name,
					addonVersion=addon.version,
					NVDAVersionTuple=self.NVDAVersion
				)
			self.state = {
				addonKey: compat
			}

		def loadState(self):
			return self.state

		def saveState(self, state):
			self.state = state

		def getSavedState(self, addon):
			"""Spy method, to inspect what has been given to the saveState method."""
			addonKey = addonVersionCheck.createVersionStateKey(
				addonName=addon.name,
				addonVersion=addon.version,
				NVDAVersionTuple=self.NVDAVersion
			)
			try:
				return self.state[addonKey]
			except KeyError:
				msg = "Unable to find addon key in state dict. Key: {} Dict contents: {}".format(addonKey, self.state)
				raise AssertionError(msg)

	_compatValStrings = {
		compatValues.UNKNOWN: "UNKNOWN",
		compatValues.AUTO_DEDUCED_COMPATIBLE: "AUTO_DEDUCED_COMPATIBLE",
		compatValues.AUTO_DEDUCED_INCOMPATIBLE: "AUTO_DEDUCED_INCOMPATIBLE",
		compatValues.MANUALLY_SET_COMPATIBLE: "MANUALLY_SET_COMPATIBLE",
		compatValues.MANUALLY_SET_INCOMPATIBLE: "MANUALLY_SET_INCOMPATIBLE"
	}

	def assertCompatValuesMatch(self, actual, expected):
		if actual != expected:
			msg="Actual:{} does not match Expected:{}".format(
				self._compatValStrings[actual],
				self._compatValStrings[expected]
			)
			raise AssertionError(msg)

	def resetMockStateSaver(self, addon=None, compatVal=None):
		self.mockStateSaver = self.MockStateSaver(NVDAVersionTuple=CurrentNVDAVersionTuple)
		if addon is not None and compatVal is not None:
			self.mockStateSaver.setReturnOnLoad(addon, compatVal)
		AddonCompatibilityState.initialise(statePersistence=self.mockStateSaver, forceReInit=True)

	def setUp(self):
		self.resetMockStateSaver()

	def test_getAddonCompatibility_noState_testedAndSupported_compatible(self):
		compatibleAddon = mockAddon()
		compat = AddonCompatibilityState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)

	def test_getAddonCompatibility_noState_testedNotSupported_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		compat = AddonCompatibilityState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_getAddonCompatibility_noState_notTestedNotSupported_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		compat = AddonCompatibilityState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_getAddonCompatibility_noState_notTestedWithSupport_unknown(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		compat = AddonCompatibilityState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.UNKNOWN)

	def test_getAddonCompatibility_stateUnknown_testedAndSupported_compatible(self):
		compatibleAddon = mockAddon()
		self.resetMockStateSaver(compatibleAddon, compatValues.UNKNOWN)
		compat = AddonCompatibilityState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)

	def test_getAddonCompatibility_stateUnknown_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.resetMockStateSaver(addonNotSupported, compatValues.UNKNOWN)
		compat = AddonCompatibilityState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_getAddonCompatibility_stateUnknown_unknown(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.resetMockStateSaver(notTestedAddon, compatValues.UNKNOWN)
		compat = AddonCompatibilityState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.UNKNOWN)

	def test_getAddonCompatibility_whiteListed_compatible(self):
		compatibleAddon = mockAddon()
		self.resetMockStateSaver(compatibleAddon, compatValues.MANUALLY_SET_COMPATIBLE)
		compat = AddonCompatibilityState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)  # auto deduced compat trumps manual set compat

	def test_getAddonCompatibility_whiteListed_untestedWithSupport_manuallySetCompatible(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.resetMockStateSaver(notTestedAddon, compatValues.MANUALLY_SET_COMPATIBLE)
		compat = AddonCompatibilityState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.MANUALLY_SET_COMPATIBLE)

	def test_getAddonCompatibility_whiteListed_testedWithoutSupport_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.resetMockStateSaver(addonNotSupported, compatValues.MANUALLY_SET_COMPATIBLE)
		compat = AddonCompatibilityState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)  # auto deduced incompat trumps manual set compat

	def test_getAddonCompatibility_blackListed_testedWithSupport_compatible(self):
		compatibleAddon = mockAddon()
		self.resetMockStateSaver(compatibleAddon, compatValues.MANUALLY_SET_INCOMPATIBLE)
		compat = AddonCompatibilityState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)  # auto deduced compat trumps manual set incompat

	def test_getAddonCompatibility_blackListed_untestedWithSupport_manuallySetIncompatible(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.resetMockStateSaver(notTestedAddon, compatValues.MANUALLY_SET_INCOMPATIBLE)
		compat = AddonCompatibilityState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.MANUALLY_SET_INCOMPATIBLE)

	def test_getAddonCompatibility_blackListed_testedWithoutSupport_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.resetMockStateSaver(addonNotSupported, compatValues.MANUALLY_SET_INCOMPATIBLE)
		compat = AddonCompatibilityState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)  # auto deduced incompt trumps manual set incompat

	def test_setAddonCompatibility_testedWithSupportToUnknown_compatibleStored(self):
		compatibleAddon = mockAddon()
		AddonCompatibilityState.setAddonCompatibility(
			compatibleAddon,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(compatibleAddon)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)

	def test_setAddonCompatibility_testedWithoutSupportToUnknown_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_setAddonCompatibility_untestedWithoutSupportToUnknown_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_setAddonCompatibility_untestedWithSupportToUnknown_unknownStored(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			notTestedAddon,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(notTestedAddon)
		self.assertCompatValuesMatch(compat, compatValues.UNKNOWN)

	def test_setAddonCompatibility_testedWithSupportToCompatible_compatibleStored(self):
		compatibleAddon = mockAddon()
		AddonCompatibilityState.setAddonCompatibility(
			compatibleAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_COMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(compatibleAddon)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)

	def test_setAddonCompatibility_testedWithoutSupportToCompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_COMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_setAddonCompatibility_untestedWithoutSupportToCompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_COMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_setAddonCompatibility_untestedWithSupportToCompatible_manuallySetCompatibleStored(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			notTestedAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_COMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(notTestedAddon)
		self.assertCompatValuesMatch(compat, compatValues.MANUALLY_SET_COMPATIBLE)

	def test_setAddonCompatibility_testedWithSupportToIncompatible_compatibleStored(self):
		compatibleAddon = mockAddon()
		AddonCompatibilityState.setAddonCompatibility(
			compatibleAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_INCOMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(compatibleAddon)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_COMPATIBLE)

	def test_setAddonCompatibility_testedWithoutSupportToIncompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_INCOMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_setAddonCompatibility_untestedWithoutSupportToIncompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_INCOMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, compatValues.AUTO_DEDUCED_INCOMPATIBLE)

	def test_setAddonCompatibility_untestedWithSupportToIncompatible_manuallySetIncompatibleStored(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		AddonCompatibilityState.setAddonCompatibility(
			notTestedAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=compatValues.MANUALLY_SET_INCOMPATIBLE
		)
		compat = self.mockStateSaver.getSavedState(notTestedAddon)
		self.assertCompatValuesMatch(compat, compatValues.MANUALLY_SET_INCOMPATIBLE)


class TestGetAPIVersionTupleFromString(unittest.TestCase):

	def test_getAPIVersionTupleFromString_succeeds(self):
		"""Tests trying to get the API version tuple from an API version string with one matching group
		results in an error being raised
		"""
		self.assertEqual((2019, 1, 0), addonAPIVersion.getAPIVersionTupleFromString("2019.1.0"))


	def test_getAPIVersionTupleFromString_noGroupsMatch_raises(self):
		"""Tests trying to get the API version tuple from an API version string with no matching groups
		results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "not valid")

	def test_getAPIVersionTupleFromString_twoYearDigits_raises(self):
		"""Tests trying to get the API version tuple from an API version string with not enough (2) digits
		in the year part results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "19.1.0")

	def test_getAPIVersionTupleFromString_threeYearDigits_raises(self):
		"""Tests trying to get the API version tuple from an API version string with not enough (3) digits
		in the year part results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "019.1.0")

	def test_getAPIVersionTupleFromString_oneMatch_raises(self):
		"""Tests trying to get the API version tuple from an API version string with one matching group
		results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "2019.")

	def test_getAPIVersionTupleFromString_twoMatch_raises(self):
		"""Tests trying to get the API version tuple from an API version string with two matching groups
		results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "2019.1")

	def test_getAPIVersionTupleFromString_devAppended_raises(self):
		"""Tests trying to get the API version tuple from an API version string with three matching groups
		and some extra appended results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "2019.1.0dev")

	def test_getAPIVersionTupleFromString_devPrepended_raises(self):
		"""Tests trying to get the API version tuple from an API version string with three matching groups
		and some extra prepended results in an error being raised
		"""
		self.assertRaises(ValueError, addonAPIVersion.getAPIVersionTupleFromString, "dev2019.1.0")
