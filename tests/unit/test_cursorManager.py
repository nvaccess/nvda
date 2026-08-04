# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the cursorManager module."""

import unittest
from unittest.mock import Mock, patch

import wx

import config
import cursorManager
from config.featureFlag import FeatureFlag
from config.featureFlagEnums import BoolFlag
from cursorManager import _MAX_SEARCH_HISTORY_ENTRIES, FindDialog
from .textProvider import CursorManager


class TestMove(unittest.TestCase):
	def setUp(self):
		import speechDictHandler

		speechDictHandler.initialize()  # setting the synth depends on dictionary["voice"]
		import synthDriverHandler

		# Some speech functions (speakTextInfo due to calling getSpellingSpeech) rely on getting config for a
		# synth, they first get the synth, then synth.name.
		# Previously this wasn't necessary since speech.speak and speech.speakSpelling are a no-op
		# (see tests/unit/__init__.py), however, since logic from these methods has moved to get*Speech methods
		# the logic is now executed, and the following dependencies need to be met.
		assert synthDriverHandler.setSynth("silence")
		assert synthDriverHandler.getSynth()
		# Ensure the state management for speech is set up
		from speech import speechInitialize

		speechInitialize()

	def test_nextChar(self):
		cm = CursorManager(text="abc")  # Caret at "a"
		cm.script_moveByCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (1, 1))  # Caret at "b"

	def test_prevChar(self):
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_moveByCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 0))  # Caret at "a"

	def test_endOfLine(self):
		"""End of line in a CursorManager moves to the last character; there is no "insertion point"."""
		cm = CursorManager(text="ab")  # Caret at "a"
		cm.script_endOfLine(None)
		self.assertEqual(cm.selectionOffsets, (1, 1))  # Caret at "b"


class TestSelection(unittest.TestCase):
	def test_selForward(self):
		cm = CursorManager(text="abc")  # Caret at "a"
		cm.script_selectCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (0, 1))  # "a" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selBackward(self):
		"""Same as test_selForward, but with reversed direction."""
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 1))  # "a" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, False)  # the start moved

	def test_selForwardThenUnsel(self):
		"""Depends on behavior tested by test_selForward."""
		cm = CursorManager(text="abc")  # Caret at "a"
		cm.script_selectCharacter_forward(None)  # "a" selected
		cm.script_selectCharacter_back(None)  # "a" unselected
		self.assertEqual(cm.selectionOffsets, (0, 0))  # Caret at "a", no selection

	def test_selBackwardThenUnsel(self):
		"""Depends on behavior tested by test_selBackward.
		Same as test_selForwardThenUnsel, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectCharacter_back(None)  # "a" selected
		cm.script_selectCharacter_forward(None)  # "a" unselected
		self.assertEqual(cm.selectionOffsets, (1, 1))  # Caret at "b", no selection

	def test_selForwardTwice(self):
		"""Depends on behavior tested in test_selForward."""
		cm = CursorManager(text="abc")  # Caret at "a"
		cm.script_selectCharacter_forward(None)  # "a" selected
		cm.script_selectCharacter_forward(None)  # "b" selected
		self.assertEqual(cm.selectionOffsets, (0, 2))  # "ab" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selBackwardTwice(self):
		"""Depends on behavior tested in test_selBackward.
		Same as test_selForwardTwice, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(2, 2))  # Caret at "c"
		cm.script_selectCharacter_back(None)  # "b" selected
		cm.script_selectCharacter_back(None)  # "a" selected
		self.assertEqual(cm.selectionOffsets, (0, 2))  # "ab" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, False)  # the start moved

	def test_selForwardThenUnselThenSelBackward(self):
		"""Test selecting forward, then unselecting and selecting backward.
		Depends on behavior tested by test_selForwardThenUnsel.
		"""
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectCharacter_forward(None)  # "b" selected
		cm.script_selectCharacter_back(None)  # "b" unselected, caret at "b"
		cm.script_selectCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 1))  # "a" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, False)  # the start moved

	def test_selBackwardThenUnselThenSelForward(self):
		"""Test selecting backward, then unselecting and selecting forward.
		Depends on behavior tested by test_selBackwardThenUnsel.
		Same as test_selForwardThenUnselThenSelBackward, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectCharacter_back(None)  # "a" selected
		cm.script_selectCharacter_forward(None)  # "a" unselected, caret at "b"
		cm.script_selectCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (1, 2))  # "b" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selForwardThenSelBackward(self):
		"""Test selecting forward, then selecting backward without unselecting.
		Depends on behavior tested by test_selForward.
		"""
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectCharacter_forward(None)  # "b" selected
		cm.script_selectWord_back(None)  # "b" unselected, "a" selected
		self.assertEqual(cm.selectionOffsets, (0, 1))  # "a" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, False)  # the start moved

	def test_selBackwardThenSelForward(self):
		"""Test selecting backward, then selecting forward without unselecting.
		Same as test_selForwardThenSelBackward, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(2, 2))  # Caret at "c"
		cm.script_selectCharacter_back(None)  # "b" selected
		cm.script_selectWord_forward(None)  # "b" unselected, "c" selected
		self.assertEqual(cm.selectionOffsets, (2, 3))  # "c" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selForwardThenSelBackwardThenUnsel(self):
		"""Test selecting forward, then selecting backward without unselecting, then unselecting forward.
		Depends on behavior tested by test_selForwardThenSelBackward.
		"""
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectCharacter_forward(None)  # "b" selected
		cm.script_selectWord_back(None)  # "b" unselected, "a" selected
		cm.script_selectCharacter_forward(None)  # "a" unselected
		self.assertEqual(cm.selectionOffsets, (1, 1))  # Caret at "b", no selection

	def test_selBackwardThenSelForwardThenUnsel(self):
		"""Test selecting backward, then selecting forward without unselecting, then unselecting backward.
		Same as test_selForwardThenSelBackwardThenUnsel, but with reversed directions.
		Depends on behavior tested by test_selBackwardThenSelForward.
		"""
		cm = CursorManager(text="abc", selection=(2, 2))  # Caret at "c"
		cm.script_selectCharacter_back(None)  # "b" selected
		cm.script_selectWord_forward(None)  # "b" unselected, "c" selected
		cm.script_selectCharacter_back(None)  # "c" unselected
		self.assertEqual(cm.selectionOffsets, (2, 2))  # Caret at "c", no selection

	def test_selToBottom(self):
		cm = CursorManager(text="abc", selection=(1, 1))  # Caret at "b"
		cm.script_selectToBottomOfDocument(None)
		self.assertEqual(cm.selectionOffsets, (1, 3))  # "bc" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selToTop(self):
		cm = CursorManager(text="abc", selection=(2, 2))  # Caret at "c"
		cm.script_selectToTopOfDocument(None)
		self.assertEqual(cm.selectionOffsets, (0, 2))  # "ab" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, False)  # the start moved

	def test_selToEndOfLine(self):
		cm = CursorManager(text="ab\ncd", selection=(1, 1))  # Caret at "b"
		cm.script_selectToEndOfLine(None)
		self.assertEqual(cm.selectionOffsets, (1, 3))  # "b\n" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selToBeginningOfLine(self):
		cm = CursorManager(text="ab\ncd", selection=(4, 4))  # Caret at "d"
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (3, 4))  # "c" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, False)  # the start moved

	def test_selToEndOfLineAtEnd(self):
		"""Test selecting to the end of the line after moving to the end of the line (#7157).
		End of line in a CursorManager moves to the last character; there is no "insertion point".
		So, doing this must select the last character.
		"""
		cm = CursorManager(text="ab", selection=(1, 1))  # Caret at "b"
		cm.script_selectToEndOfLine(None)
		self.assertEqual(cm.selectionOffsets, (1, 2))  # "b" selected
		self.assertEqual(cm.isTextSelectionAnchoredAtStart, True)  # the end moved

	def test_selToBeginningOfLineAtBeginning(self):
		"""Test selecting to the beginning of the line when the caret is already at the beginning of the line.
		In this case, nothing should happen.
		"""
		cm = CursorManager(text="ab\ncd", selection=(3, 3))  # Caret at "c"
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (3, 3))  # No selection

	def test_selForwardThenSelToBeginningOfLine(self):
		"""Depends on behavior tested by test_selForward."""
		cm = CursorManager(text="ab\ncd", selection=(3, 3))  # Caret at "c"
		cm.script_selectCharacter_forward(None)  # "c" selected
		cm.script_selectToBeginningOfLine(None)  # "c" unselected
		self.assertEqual(cm.selectionOffsets, (3, 3))  # Caret at "c", no selection

	def test_selToEndThenBeginningOfLine(self):
		"""Test for #5746.
		Depends on behavior tested in test_selToEndOfLine and test_selToBeginningOfLine.
		"""
		cm = CursorManager(text="ab")  # Caret at "a"
		cm.script_selectToEndOfLine(None)
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (0, 0))  # Caret at "a", no selection


class TestSelectAll(unittest.TestCase):
	"""Tests the select all command starting from different caret positions."""

	def _selectAllTest(self, caret):
		"""Tests select all with the caret at the given offset."""
		cm = CursorManager(text="abc", selection=(caret, caret))
		cm.script_selectAll(None)
		self.assertEqual(cm.selectionOffsets, (0, 3))  # "abc" selected

	def test_selectAllFromStart(self):
		self._selectAllTest(0)  # Caret at "a"

	def test_selectAllFromMiddle(self):
		self._selectAllTest(1)  # Caret at "b"

	def test_selectAllFromEnd(self):
		self._selectAllTest(2)  # Caret at "c"


class TestSearchHistory(unittest.TestCase):
	"""Tests the pure list logic of CursorManager._updateSearchHistory (#8482).
	This is class-level shared state, so it is reset before and after each test.
	"""

	def setUp(self):
		# Clear in place, as assigning would shadow the list shared with the base class.
		CursorManager._searchEntries.clear()

	def tearDown(self):
		CursorManager._searchEntries.clear()

	def test_appendingTermPutsItAtFront(self):
		CursorManager._updateSearchHistory("foo")
		self.assertEqual(CursorManager._searchEntries, ["foo"])

	def test_emptyStringIsIgnored(self):
		CursorManager._updateSearchHistory("foo")
		CursorManager._updateSearchHistory("")
		self.assertEqual(CursorManager._searchEntries, ["foo"])

	def test_retypingExistingTermPromotesItToFrontWithoutDuplicate(self):
		CursorManager._updateSearchHistory("foo")
		CursorManager._updateSearchHistory("bar")
		CursorManager._updateSearchHistory("foo")
		self.assertEqual(CursorManager._searchEntries, ["foo", "bar"])

	def test_caseOnlyVariantDedupsKeepingNewestCasing(self):
		CursorManager._updateSearchHistory("Car")
		CursorManager._updateSearchHistory("car")
		self.assertEqual(CursorManager._searchEntries, ["car"])

	def test_exceedingMaxEntriesTruncatesOldest(self):
		for index in range(_MAX_SEARCH_HISTORY_ENTRIES + 1):
			CursorManager._updateSearchHistory(f"term{index}")
		self.assertEqual(len(CursorManager._searchEntries), _MAX_SEARCH_HISTORY_ENTRIES)
		self.assertEqual(CursorManager._searchEntries[0], f"term{_MAX_SEARCH_HISTORY_ENTRIES}")
		self.assertNotIn("term0", CursorManager._searchEntries)


class TestFindDialogSingleInstance(unittest.TestCase):
	"""Tests that only one find dialog exists at a time (#20484)."""

	def setUp(self):
		self.app = wx.App()
		self._dialogs: list[FindDialog] = []
		config.conf["virtualBuffers"]["findHistory"] = FeatureFlag(BoolFlag.ENABLED, BoolFlag.ENABLED)

	def tearDown(self):
		for dialog in self._dialogs:
			# A dialog whose underlying window has already been destroyed is falsy.
			if dialog:
				dialog.Destroy()
		FindDialog._instance = None
		config.conf["virtualBuffers"]["findHistory"] = FeatureFlag(BoolFlag.DEFAULT, BoolFlag.ENABLED)

	def _createDialog(
		self,
		cursorManager: Mock | None = None,
		text: str = "",
		caseSensitivity: bool = False,
		reverse: bool = False,
		searchEntries: list[str] | None = None,
	) -> FindDialog:
		dialog = FindDialog(
			None,
			cursorManager or Mock(),
			text,
			caseSensitivity,
			reverse,
			searchEntries,
		)
		if not any(known is dialog for known in self._dialogs):
			self._dialogs.append(dialog)
		return dialog

	def test_creatingDialogWhileOneIsOpenReusesIt(self):
		first = self._createDialog(text="foo", searchEntries=["foo"])
		second = self._createDialog(text="bar", searchEntries=["bar", "foo"])
		self.assertIs(second, first)

	def test_reusedDialogIsRetargeted(self):
		self._createDialog(text="foo", searchEntries=["foo"])
		cursorManager = Mock()
		dialog = self._createDialog(
			cursorManager,
			"bar",
			caseSensitivity=True,
			reverse=True,
			searchEntries=["bar", "foo"],
		)
		self.assertIs(dialog.activeCursorManager, cursorManager)
		self.assertTrue(dialog.reverse)
		self.assertTrue(dialog.caseSensitiveCheckBox.GetValue())
		self.assertEqual(dialog.findTextField.GetValue(), "bar")
		self.assertEqual(dialog.findTextField.GetStrings(), ["bar", "foo"])

	def test_destroyedDialogIsNotReused(self):
		first = self._createDialog(text="foo")
		first.Destroy()
		# Destruction of a top level window is deferred until pending events are processed.
		wx.Yield()
		second = self._createDialog(text="bar")
		self.assertIsNot(second, first)
		self.assertEqual(second.findTextField.GetValue(), "bar")

	def test_findFieldIsPlainEditWhenHistoryIsDisabled(self):
		config.conf["virtualBuffers"]["findHistory"] = FeatureFlag(BoolFlag.DISABLED, BoolFlag.ENABLED)
		dialog = self._createDialog(text="foo", searchEntries=["foo"])
		self.assertNotIsInstance(dialog.findTextField, wx.ComboBox)
		self._createDialog(text="bar", searchEntries=["bar", "foo"])
		self.assertEqual(dialog.findTextField.GetValue(), "bar")


class TestFindDialogPopupPairing(unittest.TestCase):
	"""Tests that script_find pairs every prePopup call with a postPopup call (#20484)."""

	def setUp(self):
		self.app = wx.App()
		# A real window is needed as the dialog parent, but the popup bookkeeping is mocked.
		self.mainFrame = wx.Frame(None)
		self.mainFrame.prePopup = Mock()
		self.mainFrame.postPopup = Mock()
		self._patches = [
			patch.object(cursorManager.gui, "mainFrame", self.mainFrame),
			# script_find defers its work to wx.CallAfter, run it inline instead.
			patch.object(cursorManager.wx, "CallAfter", lambda func, *args, **kwargs: func(*args, **kwargs)),
			# ShowModal would block until the dialog is dismissed.
			patch.object(FindDialog, "ShowModal", Mock(return_value=wx.ID_CANCEL)),
		]
		for p in self._patches:
			p.start()
		config.conf["virtualBuffers"]["findHistory"] = FeatureFlag(BoolFlag.ENABLED, BoolFlag.ENABLED)

	def tearDown(self):
		for p in reversed(self._patches):
			p.stop()
		dialog = FindDialog._instance() if FindDialog._instance else None
		if dialog:
			dialog.Destroy()
		FindDialog._instance = None
		self.mainFrame.Destroy()
		config.conf["virtualBuffers"]["findHistory"] = FeatureFlag(BoolFlag.DEFAULT, BoolFlag.ENABLED)

	def test_openingDialogPairsPrePopupWithPostPopup(self):
		CursorManager(text="abc", selection=(0, 0)).script_find(None)
		self.assertEqual(self.mainFrame.prePopup.call_count, 1)
		self.assertEqual(self.mainFrame.postPopup.call_count, 1)

	def test_reusingDialogDoesNotCallPrePopupAgain(self):
		# The dialog created here is still open, as ShowModal is mocked out.
		CursorManager(text="abc", selection=(0, 0)).script_find(None)
		self.mainFrame.prePopup.reset_mock()
		self.mainFrame.postPopup.reset_mock()
		CursorManager(text="def", selection=(0, 0)).script_find(None)
		self.mainFrame.prePopup.assert_not_called()
		self.mainFrame.postPopup.assert_not_called()
