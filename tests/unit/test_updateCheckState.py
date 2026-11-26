# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for persisting the update check state as JSON (#19560)."""

import json
import os
import tempfile
import unittest
from unittest import mock

import buildVersion
import globalVars
from NVDAState import WritePaths

# updateCheck refuses to import when the build has no update version type, as is the case when running from source.
with mock.patch.object(buildVersion, "updateVersionType", "snapshot:alpha"):
	import updateCheck


_VALID_STATE = {
	"lastCheck": 1767225600.5,
	"dontRemindVersion": "2027.1",
	"id": "0123456789abcdef0123456789abcdef",
	"pendingUpdateFile": "C:\\Users\\test\\AppData\\Roaming\\nvda\\updates\\nvda_2027.2.exe",
	"pendingUpdateVersion": "2027.2",
	"pendingUpdateAPIVersion": (2027, 2, 0),
	"pendingUpdateBackCompatToAPIVersion": (2027, 1, 0),
}


class _StateFileTestCase(unittest.TestCase):
	def setUp(self) -> None:
		tempDir = tempfile.TemporaryDirectory()
		self.addCleanup(tempDir.cleanup)
		self.configDir = tempDir.name
		configPathPatcher = mock.patch.object(globalVars.appArgs, "configPath", self.configDir)
		configPathPatcher.start()
		self.addCleanup(configPathPatcher.stop)

	def writeStateFile(self, content: str) -> None:
		with open(WritePaths.updateCheckStateFile, "wt", encoding="utf-8") as stateFile:
			stateFile.write(content)

	def assertStateIsDefault(self, state: dict) -> None:
		self.assertEqual(0, state["lastCheck"])
		self.assertIsNone(state["dontRemindVersion"])
		self.assertRegex(state["id"], r"^[0-9a-f]{32}$")
		self.assertIsNone(state["pendingUpdateFile"])
		self.assertIsNone(state["pendingUpdateVersion"])
		self.assertEqual((0, 0, 0), state["pendingUpdateAPIVersion"])
		self.assertEqual((0, 0, 0), state["pendingUpdateBackCompatToAPIVersion"])


class TestStatePaths(_StateFileTestCase):
	def test_stateFileIsJson(self):
		self.assertEqual(
			os.path.join(self.configDir, "updateCheckState.json"),
			WritePaths.updateCheckStateFile,
		)

	def test_oldStateFileIsPickle(self):
		self.assertEqual(
			os.path.join(self.configDir, "updateCheckState.pickle"),
			WritePaths._oldUpdateCheckStateFile,
		)


class TestSaveAndLoad(_StateFileTestCase):
	def test_roundTripPreservesStateAndRestoresTuples(self):
		with mock.patch.object(updateCheck, "state", dict(_VALID_STATE), create=True):
			updateCheck.saveState()

		with open(WritePaths.updateCheckStateFile, "rt", encoding="utf-8") as stateFile:
			# The file must be plain JSON.
			self.assertEqual("2027.2", json.load(stateFile)["pendingUpdateVersion"])
		loadedState = updateCheck._loadState(WritePaths.updateCheckStateFile)

		self.assertEqual(_VALID_STATE, loadedState)
		# Other code compares API versions with tuples, so they must not be loaded as lists.
		self.assertIsInstance(loadedState["pendingUpdateAPIVersion"], tuple)
		self.assertIsInstance(loadedState["pendingUpdateBackCompatToAPIVersion"], tuple)

	def test_defaultStateRoundTrips(self):
		defaultState = updateCheck._getDefaultState()
		with mock.patch.object(updateCheck, "state", defaultState, create=True):
			updateCheck.saveState()

		self.assertEqual(defaultState, updateCheck._loadState(WritePaths.updateCheckStateFile))

	def test_missingFileGivesDefaultState(self):
		self.assertStateIsDefault(updateCheck._loadState(WritePaths.updateCheckStateFile))

	def test_invalidJsonGivesDefaultState(self):
		self.writeStateFile("{not json")
		self.assertStateIsDefault(updateCheck._loadState(WritePaths.updateCheckStateFile))

	def test_invalidUtf8GivesDefaultState(self):
		with open(WritePaths.updateCheckStateFile, "wb") as stateFile:
			stateFile.write(b'{"dontRemindVersion": "\xff"}')
		self.assertStateIsDefault(updateCheck._loadState(WritePaths.updateCheckStateFile))

	def test_deeplyNestedJsonGivesDefaultState(self):
		self.writeStateFile("[" * 30_000 + "]" * 30_000)
		self.assertStateIsDefault(updateCheck._loadState(WritePaths.updateCheckStateFile))

	def test_nonMappingGivesDefaultState(self):
		self.writeStateFile(json.dumps(["lastCheck", 5]))
		self.assertStateIsDefault(updateCheck._loadState(WritePaths.updateCheckStateFile))

	def test_oversizedFileIsNotLoaded(self):
		oversizedState = dict(_VALID_STATE, padding="x" * updateCheck._MAX_STATE_FILESIZE_BYTES)
		self.writeStateFile(json.dumps(oversizedState))
		self.assertStateIsDefault(updateCheck._loadState(WritePaths.updateCheckStateFile))


class TestStateValidation(unittest.TestCase):
	def test_validStateIsKept(self):
		self.assertEqual(_VALID_STATE, updateCheck._stateFromDict(_VALID_STATE))

	def test_emptyDictGivesDefaultState(self):
		state = updateCheck._stateFromDict({})
		self.assertEqual(0, state["lastCheck"])
		self.assertRegex(state["id"], r"^[0-9a-f]{32}$")
		self.assertIsNone(state["pendingUpdateFile"])

	def test_unknownKeysAreDropped(self):
		state = updateCheck._stateFromDict(dict(_VALID_STATE, unexpected="value"))
		self.assertNotIn("unexpected", state)

	def test_invalidLastCheckIsReset(self):
		for lastCheck in (-1, float("inf"), float("nan"), 1e300, True, "0", None):
			with self.subTest(lastCheck=lastCheck):
				state = updateCheck._stateFromDict(dict(_VALID_STATE, lastCheck=lastCheck))
				self.assertEqual(0, state["lastCheck"])
				self.assertEqual("2027.1", state["dontRemindVersion"])

	def test_invalidDontRemindVersionIsReset(self):
		for dontRemindVersion in (1, ["2027.1"], {"version": "2027.1"}):
			with self.subTest(dontRemindVersion=dontRemindVersion):
				state = updateCheck._stateFromDict(dict(_VALID_STATE, dontRemindVersion=dontRemindVersion))
				self.assertIsNone(state["dontRemindVersion"])

	def test_invalidIdIsRegenerated(self):
		for userId in (None, 1, "", "not a hex id", "0123456789ABCDEF0123456789ABCDEF", "a" * 33):
			with self.subTest(userId=userId):
				state = updateCheck._stateFromDict(dict(_VALID_STATE, id=userId))
				self.assertRegex(state["id"], r"^[0-9a-f]{32}$")
				self.assertNotEqual(userId, state["id"])

	def test_apiVersionsAcceptListsFromJson(self):
		state = updateCheck._stateFromDict(
			dict(
				_VALID_STATE,
				pendingUpdateAPIVersion=[2027, 2, 0],
				pendingUpdateBackCompatToAPIVersion=[2027, 1, 0],
			),
		)
		self.assertEqual((2027, 2, 0), state["pendingUpdateAPIVersion"])
		self.assertEqual((2027, 1, 0), state["pendingUpdateBackCompatToAPIVersion"])

	def test_invalidPendingUpdateDetailsAreDiscardedTogether(self):
		invalidValues = {
			"pendingUpdateFile": 5,
			"pendingUpdateVersion": ["2027.2"],
			"pendingUpdateAPIVersion": [2027, 2],
			"pendingUpdateBackCompatToAPIVersion": [2027, 1, "0"],
		}
		for key, value in invalidValues.items():
			with self.subTest(key=key):
				state = updateCheck._stateFromDict(dict(_VALID_STATE, **{key: value}))
				self.assertIsNone(state["pendingUpdateFile"])
				self.assertIsNone(state["pendingUpdateVersion"])
				self.assertEqual((0, 0, 0), state["pendingUpdateAPIVersion"])
				self.assertEqual((0, 0, 0), state["pendingUpdateBackCompatToAPIVersion"])
				# Unrelated values are kept.
				self.assertEqual(_VALID_STATE["id"], state["id"])

	def test_apiVersionRejectsBoolsAndNegatives(self):
		for apiVersion in ([True, False, True], [2027, -1, 0], (2027.0, 1, 0), None):
			with self.subTest(apiVersion=apiVersion):
				self.assertIsNone(updateCheck._apiVersionFromJson(apiVersion))


class TestOldStateFileRemoval(_StateFileTestCase):
	def setUp(self) -> None:
		super().setUp()
		with open(WritePaths._oldUpdateCheckStateFile, "wb") as oldStateFile:
			oldStateFile.write(b"not a real pickle")

	def test_oldStateFileIsRemovedWithoutBeingLoaded(self):
		with (
			mock.patch("NVDAState.shouldWriteToDisk", return_value=True),
			mock.patch("pickle.load", side_effect=AssertionError("pickle must not be loaded")),
			mock.patch("pickle.loads", side_effect=AssertionError("pickle must not be loaded")),
		):
			updateCheck._removeOldStateFile()

		self.assertFalse(os.path.exists(WritePaths._oldUpdateCheckStateFile))

	def test_oldStateFileIsKeptWhenNotWritingToDisk(self):
		with mock.patch("NVDAState.shouldWriteToDisk", return_value=False):
			updateCheck._removeOldStateFile()

		self.assertTrue(os.path.exists(WritePaths._oldUpdateCheckStateFile))

	def test_missingOldStateFileIsIgnored(self):
		os.remove(WritePaths._oldUpdateCheckStateFile)
		with mock.patch("NVDAState.shouldWriteToDisk", return_value=True):
			updateCheck._removeOldStateFile()
