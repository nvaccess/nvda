#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited

"""Unit tests for the baseObject module, its classes and their derivatives."""

import unittest

import versionInfo
from addonHandler import AddonBase
from addonHandler import addonVersionCheck
from addonHandler.addonVersionCheck import CompatValues

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
		self.assertFalse(addonVersionCheck.hasAddonGotRequiredSupport(addonNoMinNVDAVer, CurrentNVDAVersionTuple))
		self.assertFalse(addonVersionCheck.isAddonTested(addonNoMinNVDAVer, CurrentNVDAVersionTuple))

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

	_compatValStrings = [
		"Unknown",
		"Compatible",
		"Incompatible",
		"ManuallySetCompatible",
		"ManuallySetIncompatible"
	]

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
		self.compatState = addonVersionCheck.AddonCompatibilityState(
			statePersistence=self.mockStateSaver
		)

	def setUp(self):
		self.resetMockStateSaver()

	def test_getAddonCompatibility_noState_testedAndSupported_compatible(self):
		compatibleAddon = mockAddon()
		compat = self.compatState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)

	def test_getAddonCompatibility_noState_testedNotSupported_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		compat = self.compatState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_getAddonCompatibility_noState_notTestedNotSupported_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		compat = self.compatState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_getAddonCompatibility_noState_notTestedWithSupport_unknown(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		compat = self.compatState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Unknown)

	def test_getAddonCompatibility_stateUnknown_testedAndSupported_compatible(self):
		compatibleAddon = mockAddon()
		self.resetMockStateSaver(compatibleAddon, CompatValues.Unknown)
		compat = self.compatState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)

	def test_getAddonCompatibility_stateUnknown_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.resetMockStateSaver(addonNotSupported, CompatValues.Unknown)
		compat = self.compatState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_getAddonCompatibility_stateUnknown_unknown(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.resetMockStateSaver(notTestedAddon, CompatValues.Unknown)
		compat = self.compatState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Unknown)

	def test_getAddonCompatibility_whiteListed_compatible(self):
		compatibleAddon = mockAddon()
		self.resetMockStateSaver(compatibleAddon, CompatValues.ManuallySetCompatible)
		compat = self.compatState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)  # auto deduced compat trumps manual set compat

	def test_getAddonCompatibility_whiteListed_untestedWithSupport_manuallySetCompatible(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.resetMockStateSaver(notTestedAddon, CompatValues.ManuallySetCompatible)
		compat = self.compatState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.ManuallySetCompatible)

	def test_getAddonCompatibility_whiteListed_testedWithoutSupport_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.resetMockStateSaver(addonNotSupported, CompatValues.ManuallySetCompatible)
		compat = self.compatState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)  # auto deduced incompat trumps manual set compat

	def test_getAddonCompatibility_blackListed_testedWithSupport_compatible(self):
		compatibleAddon = mockAddon()
		self.resetMockStateSaver(compatibleAddon, CompatValues.ManuallySetIncompatible)
		compat = self.compatState.getAddonCompatibility(compatibleAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)  # auto deduced compat trumps manual set incompat

	def test_getAddonCompatibility_blackListed_untestedWithSupport_manuallySetIncompatible(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.resetMockStateSaver(notTestedAddon, CompatValues.ManuallySetIncompatible)
		compat = self.compatState.getAddonCompatibility(notTestedAddon, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.ManuallySetIncompatible)

	def test_getAddonCompatibility_blackListed_testedWithoutSupport_incompatible(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.resetMockStateSaver(addonNotSupported, CompatValues.ManuallySetIncompatible)
		compat = self.compatState.getAddonCompatibility(addonNotSupported, CurrentNVDAVersionTuple)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)  # auto deduced incompt trumps manual set incompat

	def test_setAddonCompatibility_testedWithSupportToUnknown_compatibleStored(self):
		compatibleAddon = mockAddon()
		self.compatState.setAddonCompatibility(
			compatibleAddon,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(compatibleAddon)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)

	def test_setAddonCompatibility_testedWithoutSupportToUnknown_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.compatState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_setAddonCompatibility_untestedWithoutSupportToUnknown_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		self.compatState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_setAddonCompatibility_untestedWithSupportToUnknown_unknownStored(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.compatState.setAddonCompatibility(
			notTestedAddon,
			NVDAVersion=CurrentNVDAVersionTuple
		)
		compat = self.mockStateSaver.getSavedState(notTestedAddon)
		self.assertCompatValuesMatch(compat, CompatValues.Unknown)

	def test_setAddonCompatibility_testedWithSupportToCompatible_compatibleStored(self):
		compatibleAddon = mockAddon()
		self.compatState.setAddonCompatibility(
			compatibleAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetCompatible
		)
		compat = self.mockStateSaver.getSavedState(compatibleAddon)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)

	def test_setAddonCompatibility_testedWithoutSupportToCompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.compatState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetCompatible
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_setAddonCompatibility_untestedWithoutSupportToCompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		self.compatState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetCompatible
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_setAddonCompatibility_untestedWithSupportToCompatible_manuallySetCompatibleStored(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.compatState.setAddonCompatibility(
			notTestedAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetCompatible
		)
		compat = self.mockStateSaver.getSavedState(notTestedAddon)
		self.assertCompatValuesMatch(compat, CompatValues.ManuallySetCompatible)

	def test_setAddonCompatibility_testedWithSupportToIncompatible_compatibleStored(self):
		compatibleAddon = mockAddon()
		self.compatState.setAddonCompatibility(
			compatibleAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetIncompatible
		)
		compat = self.mockStateSaver.getSavedState(compatibleAddon)
		self.assertCompatValuesMatch(compat, CompatValues.Compatible)

	def test_setAddonCompatibility_testedWithoutSupportToIncompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString)
		self.compatState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetIncompatible
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_setAddonCompatibility_untestedWithoutSupportToIncompatible_incompatibleStored(self):
		addonNotSupported = mockAddon(minNVDAVersion=NextNVDAVersionString, lastTestedNVDAVersion=LastNVDAVersionString)
		self.compatState.setAddonCompatibility(
			addonNotSupported,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetIncompatible
		)
		compat = self.mockStateSaver.getSavedState(addonNotSupported)
		self.assertCompatValuesMatch(compat, CompatValues.Incompatible)

	def test_setAddonCompatibility_untestedWithSupportToIncompatible_manuallySetIncompatibleStored(self):
		notTestedAddon = mockAddon(lastTestedNVDAVersion=LastNVDAVersionString)
		self.compatState.setAddonCompatibility(
			notTestedAddon,
			NVDAVersion=CurrentNVDAVersionTuple,
			compatibilityStateValue=CompatValues.ManuallySetIncompatible
		)
		compat = self.mockStateSaver.getSavedState(notTestedAddon)
		self.assertCompatValuesMatch(compat, CompatValues.ManuallySetIncompatible)
