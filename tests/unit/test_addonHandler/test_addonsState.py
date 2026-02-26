# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2026 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Unit tests verifying loading and saving of addon state."""

import json
import os
import tempfile
from typing import Any
import unittest
from unittest.mock import patch

import addonStore.models.status
import addonHandler
from addonStore.models.version import MajorMinorPatch
import utils.caseInsensitiveCollections

DEFAULT_BACKCOMPAT_VERSION = MajorMinorPatch(2023, 1, 0)


class AddonsStateTestCase(unittest.TestCase):
	def assertStateIsDefault(self, state: addonHandler.AddonsState) -> None:
		self.assertMMPEqual(state.manualOverridesAPIVersion, DEFAULT_BACKCOMPAT_VERSION)
		for category in addonStore.models.status.AddonStateCategory:
			self.assertIn(category, state)
			self.assertIsInstance(state[category], utils.caseInsensitiveCollections.CaseInsensitiveSet)
			self.assertEqual(len(state[category]), 0)
		self.assertEqual(len(state), len(addonStore.models.status.AddonStateCategory))

	def assertMMPEqual(self, obj: Any, mmp: tuple[int, int, int]) -> None:
		self.assertIsInstance(obj, MajorMinorPatch)
		self.assertEqual(obj, mmp)


class TestDefaultStateContent(AddonsStateTestCase):
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

	def test_constructorSetsDefaults(self):
		state = addonHandler.AddonsState()
		self.assertStateIsDefault(state)


class TestDeserialization(AddonsStateTestCase):
	def setUp(self) -> None:
		self.state = addonHandler.AddonsState()
		self.tempDir = tempfile.TemporaryDirectory()
		self.statePath = os.path.join(self.tempDir.name, "addonsState.json")

	def tearDown(self) -> None:
		self.tempDir.cleanup()

	def test_addonNamesCaseInsensitive(self):
		self.state.fromDict({"pendingRemovesSet": ["foo", "FOO"]})
		self.assertEqual(self.state[addonStore.models.status.AddonStateCategory.PENDING_REMOVE], {"foo"})

	def test_noBackCompatInStateBackCompatSetToDefault(self):
		self.state.fromDict({"pendingRemovesSet": ["foo", "FOO"]})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2023)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 0)

	def test_backCompatToProvidedAsATuple(self):
		self.state.fromDict({"backCompatToAPIVersion": (2024, 1, 1)})
		self.assertEqual(self.state.manualOverridesAPIVersion.major, 2024)
		self.assertEqual(self.state.manualOverridesAPIVersion.minor, 1)
		self.assertEqual(self.state.manualOverridesAPIVersion.patch, 1)

	def test_invalidBackCompatToVersionKeepsDefault(self):
		self.state.fromDict({"backCompatToAPIVersion": "not_iterable"})
		self.assertMMPEqual(self.state.manualOverridesAPIVersion, DEFAULT_BACKCOMPAT_VERSION)

	def test_backCompatToProvidedAsAList(self):
		self.state.fromDict({"backCompatToAPIVersion": [2025, 1, 0]})
		self.assertMMPEqual(self.state.manualOverridesAPIVersion, (2025, 1, 0))

	def test_loadFileNotFoundNoError(self):
		nonexistentPath = os.path.join(self.tempDir.name, "does_not_exist.json")
		state = addonHandler.AddonsState()
		state._load(nonexistentPath)
		# State should remain at defaults.
		self.assertStateIsDefault(state)

	def test_loadInvalidJson(self):
		with open(self.statePath, "wt", encoding="utf-8") as f:
			f.write("{invalid json content!!!")
		state = addonHandler.AddonsState()
		state._load(self.statePath)
		# State should remain at defaults.
		self.assertStateIsDefault(state)

	def test_loadFileTooLarge(self):
		# Write a file exceeding _MAX_STATE_FILESIZE_BYTES (1 MiB).
		with open(self.statePath, "wt", encoding="utf-8") as f:
			f.write(" " * (addonHandler._MAX_STATE_FILESIZE_BYTES + 1))
		state = addonHandler.AddonsState()
		state._load(self.statePath)
		# State should remain at defaults.
		self.assertStateIsDefault(state)

	def test_loadNonMappingJson(self):
		with open(self.statePath, "wt", encoding="utf-8") as f:
			json.dump([1, 2, 3], f)
		state = addonHandler.AddonsState()
		state._load(self.statePath)
		# State should remain at defaults.
		self.assertStateIsDefault(state)


class TestSerialization(unittest.TestCase):
	def setUp(self) -> None:
		self.tempDir = tempfile.TemporaryDirectory()
		self.statePath = os.path.join(self.tempDir.name, "addonsState.json")

	def tearDown(self) -> None:
		self.tempDir.cleanup()

	def test_stateConvertedToBuiltInTypes(self):
		state = addonHandler.AddonsState()
		state.setDefaultStateValues()
		state.fromDict({"backCompatToAPIVersion": [2024, 1, 1], "pendingRemovesSet": ["foo"]})
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

	def test_saveProducesValidJson(self):
		state = addonHandler.AddonsState()
		state.fromDict({"pendingRemovesSet": ["testAddon"]})
		self.assertTrue(state._save(self.statePath))
		with open(self.statePath, "rt", encoding="utf-8") as f:
			loaded = json.load(f)
		self.assertIsInstance(loaded, dict)
		self.assertIn("pendingRemovesSet", loaded)
		# CaseInsensitiveSet casefolds its members
		self.assertIn("testaddon", loaded["pendingRemovesSet"])

	def test_saveEmptyStateReturnsFalse(self):
		state = addonHandler.AddonsState()
		self.assertFalse(state._save(self.statePath))
		self.assertFalse(os.path.exists(self.statePath))

	def test_saveRaisesWhenShouldNotWriteToDisk(self):
		state = addonHandler.AddonsState()
		state.fromDict({"disabledAddons": ["someAddon"]})
		with patch("NVDAState.shouldWriteToDisk", return_value=False):
			with self.assertRaises(RuntimeError):
				state._save(self.statePath)


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

	def test_nonDictInputReturnsEmptyDict(self):
		for invalidInput in (["a", "list"], "a string", None, 42):
			with self.subTest(invalidInput=invalidInput):
				self.assertDictEqual(
					addonHandler._pickledStateDictToJsonStateDict(invalidInput),
					{},
				)


class TestSaveLoadRoundTrip(AddonsStateTestCase):
	def setUp(self) -> None:
		self.tempDir = tempfile.TemporaryDirectory()
		self.statePath = os.path.join(self.tempDir.name, "addonsState.json")

	def tearDown(self) -> None:
		self.tempDir.cleanup()

	def test_roundTripPreservesState(self):
		state = addonHandler.AddonsState()
		state.fromDict(
			{
				"backCompatToAPIVersion": [2025, 1, 0],
				"pendingRemovesSet": ["addonToRemove"],
				"disabledAddons": ["disabledAddon1", "disabledAddon2"],
				"blocked": ["blockedAddon"],
				"pendingInstallsSet": ["newAddon"],
			},
		)
		state._save(self.statePath)

		loadedState = addonHandler.AddonsState()
		loadedState._load(self.statePath)

		self.assertMMPEqual(loadedState.manualOverridesAPIVersion, (2025, 1, 0))
		for category in addonStore.models.status.AddonStateCategory:
			self.assertEqual(state[category], loadedState[category])
