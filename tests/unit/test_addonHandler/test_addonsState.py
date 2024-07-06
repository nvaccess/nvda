# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Unit tests veryfying loading and saving of addon state."""

import unittest

import addonStore.models.status
from addonStore.models.version import MajorMinorPatch
import addonHandler
import utils.caseInsensitiveCollections


class TestDefaultStateContent(unittest.TestCase):
	def test_expectedDefaultValsInState(self):
		state = addonHandler.AddonsState()
		state.setDefaultStateValues()
		self.assertEqual(state.manualOverridesAPIVersion.major, 2023)
		self.assertEqual(state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(state.manualOverridesAPIVersion.patch, 0)
		for stateKey in addonStore.models.status.AddonStateCategory:
			stateVals = state.pop(stateKey)
			self.assertEqual(stateVals, utils.caseInsensitiveCollections.CaseInsensitiveSet())
		# Verify that only known categories are in the state.
		# Since each known key was removed from the state above, we expect it to be empty at this point.
		self.assertEqual(state, {})


class TestStatePopulationFromPickledData(unittest.TestCase):
	def setUp(self) -> None:
		self.state = addonHandler.AddonsState()
		self.state.setDefaultStateValues()

	def test_addonNamesCaseInsensitive(self):
		self.state.fromPickledDict({"pendingRemovesSet": set(("foo", "FOO"))})
		self.assertEqual(self.state[addonStore.models.status.AddonStateCategory.PENDING_REMOVE], {"foo"})

	def test_noBackCompatInStateBackCompatSetToDefault(self):
		self.state.fromPickledDict({"pendingRemovesSet": set(("foo", "FOO"))})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2023)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 0)

	def test_backCompatToProvidedAsATuple(self):
		self.state.fromPickledDict({"backCompatToAPIVersion": (2024, 1, 1)})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2024)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 1)

	def test_backCompatToProvidedAsAMajorMinorPatch(self):
		# While addons state should be pickled using builtin data types only for backward compatibility,
		# In PR #15439 `backCompatToVersion` was mistakenly pickled as a custom named tuple `MajorMinorPatch`.
		# This tests verifies that data in this format can be loaded by versions of NVDA where `MajorMinorPatch`
		# is defined.
		self.state.fromPickledDict({"backCompatToAPIVersion": MajorMinorPatch(major=2024, minor=1, patch=1)})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2024)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 1)


class TestStateConversionForPickling(unittest.TestCase):
	def test_stateConvertedToBuiltInTypes(self):
		state = addonHandler.AddonsState()
		state.setDefaultStateValues()
		state.fromPickledDict({"backCompatToAPIVersion": (2024, 1, 1), "pendingRemovesSet": set(("foo",))})
		dataForPickling = state.toDict()
		backCompatInfo = dataForPickling.pop("backCompatToAPIVersion")
		with self.assertRaises(AttributeError):
			# Ensure this is serialized as a standard tuple, and not as `MajorMinorPatch`
			# by checking that values of a tuple cannot be accessed as attributes.
			# Note that we cannot check for types using `isinstance`, since named tuples are tuple subclasses,
			# yet when trying to unpickle them in versions of NVDA where `MajorMinorPatch` is not defined,
			#  they are not converted to a plain tuple automatically.
			backCompatInfo.major, backCompatInfo.minor, backCompatInfo.patch
		self.assertEqual(backCompatInfo[0], 2024)
		self.assertEqual(backCompatInfo[1], 1)
		self.assertEqual(backCompatInfo[2], 1)
		# All keys in the state should be strings, all values should be plain sets.
		for key in dataForPickling.keys():
			# Compare by identity, to make sure keys are not enum members.
			self.assertIs(key, addonStore.models.status.AddonStateCategory(key).value)

		for knownStateKey in addonStore.models.status.AddonStateCategory:
			value = dataForPickling.pop(knownStateKey.value)
			# Verify the values are converted to standard sets, by adding two strings which differ in case.
			# Normal sets should preserve them both.
			value.update({"bar", "BAR"})
			self.assertTrue({"bar", "BAR"}.issubset(value))
		# Finally make sure that we handled all keys in the dictionary.
		self.assertEqual(dataForPickling, {})
