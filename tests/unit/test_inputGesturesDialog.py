# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Justin Coffin
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for removing all gestures from a category in the Input Gestures dialog."""

import unittest
from unittest.mock import MagicMock, patch

import inputCore
from gui.inputGestures import (
	_CategoryVM,
	_EmuCategoryVM,
	_InputGesturesViewModel,
	_PendingGesture,
)


class _FakeScriptOwner:
	"""Stands in for the class that defines the scripts."""


def _makeScriptInfo(
	scriptName: str,
	gestures: list[str],
	infoClass: type[inputCore.AllGesturesScriptInfo] = inputCore.AllGesturesScriptInfo,
) -> inputCore.AllGesturesScriptInfo:
	scriptInfo = infoClass(_FakeScriptOwner, scriptName)
	scriptInfo.displayName = scriptName
	scriptInfo.gestures = gestures
	return scriptInfo


def _makeCategory() -> _CategoryVM:
	return _CategoryVM(
		"Magnifier",
		{
			"Zoom in": _makeScriptInfo("zoomIn", ["kb:nvda+shift+=", "kb:nvda+numpadplus"]),
			"Zoom out": _makeScriptInfo("zoomOut", ["kb:nvda+shift+-"]),
			"Toggle magnifier": _makeScriptInfo("toggleMagnifier", []),
		},
	)


class Test_CategoryGestureRemoval(unittest.TestCase):
	def test_countsAllGesturesInCategory(self):
		catVM = _makeCategory()
		self.assertEqual(catVM.getRemovableGestureCount(), 3)
		self.assertTrue(catVM.canRemove)

	def test_removeAllGestures_keepsCategoryAndScripts(self):
		catVM = _makeCategory()
		removedCount = catVM.removeAllGestures()
		self.assertEqual(removedCount, 3)
		self.assertEqual(len(catVM.scripts), 3)
		for scriptVM in catVM.scripts:
			self.assertEqual(scriptVM.gestures, [])
		self.assertFalse(catVM.canRemove)
		self.assertEqual(catVM.getRemovableGestureCount(), 0)

	def test_removeAllGestures_marksExistingGesturesAsRemoved(self):
		catVM = _makeCategory()
		catVM.removeAllGestures()
		removedIdentifiers = sorted(
			identifier for scriptVM in catVM.scripts for identifier in scriptVM.removedGestures
		)
		self.assertEqual(
			removedIdentifiers,
			["kb:nvda+numpadplus", "kb:nvda+shift+-", "kb:nvda+shift+="],
		)

	def test_removeAllGestures_discardsGesturesAddedInSession(self):
		catVM = _makeCategory()
		toggleScript = next(s for s in catVM.scripts if s.displayName == "Toggle magnifier")
		toggleScript._addGesture("kb:nvda+shift+w")
		catVM.removeAllGestures()
		self.assertEqual(toggleScript.addedGestures, [])
		# A gesture that was only added in this session was never saved, so it must not be unbound.
		self.assertEqual(toggleScript.removedGestures, {})

	def test_pendingGestureIsNotRemoved(self):
		catVM = _makeCategory()
		toggleScript = next(s for s in catVM.scripts if s.displayName == "Toggle magnifier")
		toggleScript.createPendingGesture()
		self.assertEqual(catVM.getRemovableGestureCount(), 3)
		catVM.removeAllGestures()
		self.assertEqual(len(toggleScript.gestures), 1)
		self.assertIsInstance(toggleScript.gestures[0], _PendingGesture)

	def test_categoryWithoutGesturesCanNotBeRemovedFrom(self):
		catVM = _CategoryVM("Unused", {"Do nothing": _makeScriptInfo("doNothing", [])})
		self.assertFalse(catVM.canRemove)
		self.assertEqual(catVM.removeAllGestures(), 0)

	def test_emulatedKeysCategory_keepsEmulationsAndPendingEntry(self):
		catVM = _EmuCategoryVM(
			inputCore.SCRCAT_KBEMU,
			{
				"escape": _makeScriptInfo(
					"kb:escape",
					["br(freedomScientific):dot1+dot5"],
					infoClass=inputCore.KbEmuScriptInfo,
				),
			},
		)
		catVM.createPendingEmuGesture()
		self.assertEqual(catVM.getRemovableGestureCount(), 1)
		self.assertEqual(catVM.removeAllGestures(), 1)
		self.assertEqual(len(catVM.scripts), 2)
		self.assertEqual(catVM.removedKbEmulation, {})

	def test_filteredCategoryOnlyRemovesMatchingScripts(self):
		viewModel = _InputGesturesViewModel.__new__(_InputGesturesViewModel)
		viewModel.allGestures = [_makeCategory()]
		viewModel.filter("zoom in")
		(filteredCategory,) = viewModel.filteredGestures
		self.assertEqual(filteredCategory.removeAllGestures(), 2)
		zoomOutScript = next(s for s in viewModel.allGestures[0].scripts if s.displayName == "Zoom out")
		self.assertEqual(len(zoomOutScript.gestures), 1)


class Test_commitCategoryGestureRemoval(unittest.TestCase):
	def test_removedDefaultGesturesAreUnbound(self):
		viewModel = _InputGesturesViewModel.__new__(_InputGesturesViewModel)
		viewModel.allGestures = [_makeCategory()]
		viewModel.allGestures[0].removeAllGestures()
		userGestureMap = MagicMock()
		# Default gestures are not in the user gesture map, so they are unbound with a None script instead.
		userGestureMap.remove.side_effect = ValueError
		with patch.object(inputCore, "manager", MagicMock(userGestureMap=userGestureMap)):
			self.assertTrue(viewModel.commitChanges())
		unboundIdentifiers = sorted(call.args[0] for call in userGestureMap.add.call_args_list)
		self.assertEqual(
			unboundIdentifiers,
			["kb:nvda+numpadplus", "kb:nvda+shift+-", "kb:nvda+shift+="],
		)
		for call in userGestureMap.add.call_args_list:
			self.assertIsNone(call.args[3])
		userGestureMap.save.assert_called_once()
