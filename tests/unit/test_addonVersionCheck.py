#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited

"""Unit tests for the addonVersionCheck module."""

import unittest

import addonAPIVersion
from addonHandler import AddonBase
from addonHandler import addonVersionCheck

latestVersionTuple = (2018, 2, 0)
nextVersionTuple = (2018, 3, 0)
previousVersionTuple = (2018, 1, 0)
oldVersionTuple = (2017, 1, 0)

class mockAddon(AddonBase):
	def __init__(
			self,
			minAPIVersion,
			lastTestedAPIVersion,
			name="mockAddon",
			version="1.0"
	):
		super(mockAddon, self).__init__()
		self._name = name
		self._version = version
		self._minAPIVersion = minAPIVersion
		self._lastTestedAPIVersion = lastTestedAPIVersion

	@AddonBase.name.getter
	def name(self):
		return self._name

	@AddonBase.version.getter
	def version(self):
		return self._version

	@AddonBase.minimumNVDAVersion.getter
	def minimumNVDAVersion(self):
		return self._minAPIVersion

	@AddonBase.lastTestedNVDAVersion.getter
	def lastTestedNVDAVersion(self):
		return self._lastTestedAPIVersion

class TestAddonVersionCheck(unittest.TestCase):
	"""Tests that the addon version check works as expected."""

	def test_addonCompat_addonRequiresNewFeature(self):
		"""Test an addon that has just been developed, requiring an API feature introduced in the current release."""
		addon = mockAddon(minAPIVersion=latestVersionTuple, lastTestedAPIVersion=latestVersionTuple)
		nvda_current, nvda_backwardsCompatTo = latestVersionTuple, previousVersionTuple
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(addon, nvda_current))
		self.assertTrue(addonVersionCheck.isAddonTested(addon, nvda_backwardsCompatTo))
		self.assertTrue(addonVersionCheck.isAddonCompatible(addon, nvda_current, nvda_backwardsCompatTo))

	def test_addonCompat_testedAgainstLastBackwardsCompatVersion(self):
		"""Test an addon has been maintained and tested against the backwardsCompatTo version."""
		addon = mockAddon(minAPIVersion=oldVersionTuple, lastTestedAPIVersion=previousVersionTuple)
		nvda_current, nvda_backwardsCompatTo = latestVersionTuple, previousVersionTuple
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(addon, nvda_current))
		self.assertTrue(addonVersionCheck.isAddonTested(addon, nvda_backwardsCompatTo))
		self.assertTrue(addonVersionCheck.isAddonCompatible(addon, nvda_current, nvda_backwardsCompatTo))

	def test_addonCompat_lastTestedAgainstNowNoLongerSupportedAPIVersion(self):
		"""Test an addon is considered incompatible if the backwards compatible to version is moved forward for an addon
		that has not been updated."""
		addon = mockAddon(minAPIVersion=oldVersionTuple, lastTestedAPIVersion=previousVersionTuple)
		# NVDA backwards compatible to has been moved forward one version:
		nvda_current, nvda_backwardsCompatTo = latestVersionTuple, latestVersionTuple
		self.assertTrue(addonVersionCheck.hasAddonGotRequiredSupport(addon, nvda_current))
		self.assertFalse(addonVersionCheck.isAddonTested(addon, nvda_backwardsCompatTo))
		self.assertFalse(addonVersionCheck.isAddonCompatible(addon, nvda_current, nvda_backwardsCompatTo))

	def test_addonCompat_attemptingToUseAddonRequiringNewAPIFeaturesWithOldNVDA(self):
		"""Test that is considered incompatible if a user tries to install a new addon with an old version of NVDA"""
		# addon requires API features in the future release
		addon = mockAddon(minAPIVersion=nextVersionTuple, lastTestedAPIVersion=nextVersionTuple)
		nvda_current, nvda_backwardsCompatTo = latestVersionTuple, previousVersionTuple
		self.assertFalse(addonVersionCheck.hasAddonGotRequiredSupport(addon, latestVersionTuple))
		self.assertTrue(addonVersionCheck.isAddonTested(addon, latestVersionTuple))
		self.assertFalse(addonVersionCheck.isAddonCompatible(addon, nvda_current, nvda_backwardsCompatTo))



class TestGetAPIVersionTupleFromString(unittest.TestCase):

	def test_getAPIVersionTupleFromString_3_succeeds(self):
		"""Tests trying to get the API version tuple from an API version string with a standard version
		layout will succeed.
		"""
		self.assertEqual((2019, 1, 0), addonAPIVersion.getAPIVersionTupleFromString("2019.1.0"))

	def test_getAPIVersionTupleFromString_2_succeeds(self):
		"""Tests trying to get the API version tuple from an API version where the Minor part is omitted and therefore defaults to 0.
		This will succeed.
		"""
		self.assertEqual((2019, 1, 0), addonAPIVersion.getAPIVersionTupleFromString("2019.1"))

	def test_getAPIVersionTupleFromString_allZeros_succeeds(self):
		"""Tests trying to get the API version tuple from an API version string that is all zeros.
		This is used as the FIRST api version.
		"""
		self.assertEqual((0, 0, 0), addonAPIVersion.getAPIVersionTupleFromString("0.0.0"))

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


class TestFormatAsString(unittest.TestCase):

	def test_formatAsString_full(self):
		res = addonAPIVersion.formatForGUI((2019, 1, 1))
		self.assertEqual("2019.1.1", res)

	def test_formatAsString_missingMinor(self):
		res = addonAPIVersion.formatForGUI((2019, 1, 0))
		self.assertEqual("2019.1", res)

	def test_formatAsString_zeros(self):
		res = addonAPIVersion.formatForGUI((0, 0, 0))
		self.assertEqual("0.0", res)

	def test_formatAsString_none(self):
		res = addonAPIVersion.formatForGUI(None)
		self.assertEqual("unknown", res)

	def test_formatAsString_tupleTooSmall(self):
		res = addonAPIVersion.formatForGUI((2019, 1))
		self.assertEqual("unknown", res)

	def test_formatAsString_tupleTooLong(self):
		res = addonAPIVersion.formatForGUI((2019, 1, 1, 1))
		self.assertEqual("unknown", res)
