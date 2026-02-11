# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Unit tests verifying loading and saving of addon state."""

import unittest

import addonStore.models.status
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


class TestStatePopulationFromJsonData(unittest.TestCase):
	def setUp(self) -> None:
		self.state = addonHandler.AddonsState()
		self.state.setDefaultStateValues()

	def test_addonNamesCaseInsensitive(self):
		self.state.fromJsonDict({"pendingRemovesSet": ["foo", "FOO"]})
		self.assertEqual(self.state[addonStore.models.status.AddonStateCategory.PENDING_REMOVE], {"foo"})

	def test_noBackCompatInStateBackCompatSetToDefault(self):
		self.state.fromJsonDict({"pendingRemovesSet": ["foo", "FOO"]})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2023)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 0)

	def test_backCompatToProvidedAsATuple(self):
		self.state.fromJsonDict({"backCompatToAPIVersion": (2024, 1, 1)})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2024)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 1)

	# def test_backCompatToProvidedAsAMajorMinorPatch(self):
	# While addons state should be pickled using builtin data types only for backward compatibility,
	# In PR #15439 `backCompatToVersion` was mistakenly pickled as a custom named tuple `MajorMinorPatch`.
	# This tests verifies that data in this format can be loaded by versions of NVDA where `MajorMinorPatch`
	# is defined.
	# self.state.fromPickledDict({"backCompatToAPIVersion": MajorMinorPatch(major=2024, minor=1, patch=1)})
	# self.assertEqual(self.state.manualOverridesAPIVersion.major, 2024)
	# self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
	# self.assertEqual(self.state.manualOverridesAPIVersion.patch, 1)


class TestStateConversionForJsonifying(unittest.TestCase):
	def test_stateConvertedToBuiltInTypes(self):
		state = addonHandler.AddonsState()
		state.setDefaultStateValues()
		state.fromJsonDict({"backCompatToAPIVersion": [2024, 1, 1], "pendingRemovesSet": ["foo"]})
		dataForJsonifying = state.toDict()
		backCompatInfo = dataForJsonifying.pop("backCompatToAPIVersion")
		with self.assertRaises(AttributeError):
			# Ensure this is serialized as a standard tuple, and not as `MajorMinorPatch`
			# by checking that values of a tuple cannot be accessed as attributes.
			# Note that we cannot check for types using `isinstance`, since named tuples are tuple subclasses,
			# yet when trying to unpickle them in versions of NVDA where `MajorMinorPatch` is not defined,
			#  they are not converted to a plain tuple automatically.
			backCompatInfo.major, backCompatInfo.minor, backCompatInfo.patch  # type: ignore[reportUnusedExpression]
		self.assertEqual(backCompatInfo[0], 2024)
		self.assertEqual(backCompatInfo[1], 1)
		self.assertEqual(backCompatInfo[2], 1)
		# All keys in the state should be strings, all values should be plain sets.
		for key in dataForJsonifying.keys():
			# Compare by identity, to make sure keys are not enum members.
			self.assertIs(key, addonStore.models.status.AddonStateCategory(key).value)

		for knownStateKey in addonStore.models.status.AddonStateCategory:
			value = dataForJsonifying.pop(knownStateKey.value)
			# Verify the values are converted to lists.
			self.assertIsInstance(value, list)
		# Finally make sure that we handled all keys in the dictionary.
		self.assertEqual(dataForJsonifying, {})


class TestPickleToJsonConversion(unittest.TestCase):
	def test_fullyPopulatedState(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{
					"PENDING_OVERRIDE_COMPATIBILITY": {"addonPendingOverrideCompatibility"},
					"backCompatToAPIVersion": (2025, 1, 0),
					"blocked": {"blockedAddon"},
					"disabledAddons": {"disabledAddon"},
					"overrideCompatibility": {"addonWithOverriddenCompatibility"},
					"pendingDisableSet": {"addonPendingDisable"},
					"pendingEnableSet": {"addonPendingEnable"},
					"pendingInstallsSet": {"addonPendingInstall"},
					"pendingRemovesSet": {"addonPendingRemoval"},
				},
			),
			{
				"PENDING_OVERRIDE_COMPATIBILITY": ["addonPendingOverrideCompatibility"],
				"backCompatToAPIVersion": (2025, 1, 0),
				"blocked": ["blockedAddon"],
				"disabledAddons": ["disabledAddon"],
				"overrideCompatibility": ["addonWithOverriddenCompatibility"],
				"pendingDisableSet": ["addonPendingDisable"],
				"pendingEnableSet": ["addonPendingEnable"],
				"pendingInstallsSet": ["addonPendingInstall"],
				"pendingRemovesSet": ["addonPendingRemoval"],
			},
		)

	def test_categoryWithMultipleIds(self):
		converted = addonHandler._pickledStateDictToJsonStateDict(
			{"disabledAddons": {"firstDisabledAddon", "2ndDisabledAddon", "disabledAddonIII"}},
		)
		addons = converted.pop("disabledAddons")
		self.assertCountEqual(addons, ("firstDisabledAddon", "2ndDisabledAddon", "disabledAddonIII"))
		self.assertEqual(len(converted), 0)

	def test_invalidAddonIds(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict({"blocked": {"disabledAddon1", True, None, 42}}),
			{"blocked": ["disabledAddon1"]},
		)

	def test_invalidCategoryValue(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{"overrideCompatibility": 42, "PENDING_OVERRIDE_COMPATIBILITY": {"addon"}},
			),
			{"PENDING_OVERRIDE_COMPATIBILITY": ["addon"]},
		)

	def test_invalidCategoryKey(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{"pendingEnableSet": {"addonPendingEnable"}, "notAKey": ("shouldn't", "be", "here")},
			),
			{"pendingEnableSet": ["addonPendingEnable"]},
		)

	def test_insufficientVersionParts(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{"backCompatToAPIVersion": (1,), "pendingDisableSet": {"addonPendingDisable"}},
			),
			{"pendingDisableSet": ["addonPendingDisable"]},
		)

	def test_surplusVersionParts(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{"backCompatToAPIVersion": (1, 2, 3, 4), "pendingEnableSet": {"addonPendingEnable"}},
			),
			{"pendingEnableSet": ["addonPendingEnable"]},
		)

	def test_invalidVersionParts(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{
					"backCompatToAPIVersion": ("not", "a", "version"),
					"pendingInstallsSet": {"addonPendingInstall"},
				},
			),
			{"pendingInstallsSet": ["addonPendingInstall"]},
		)

	def test_invalidVersionType(self):
		self.assertDictEqual(
			addonHandler._pickledStateDictToJsonStateDict(
				{"backCompatToAPIVersion": 42, "pendingRemovesSet": {"addonPendingRemoval"}},
			),
			{"pendingRemovesSet": ["addonPendingRemoval"]},
		)
