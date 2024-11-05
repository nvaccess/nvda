# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the message dialog API."""

import unittest
from unittest.mock import MagicMock, patch

import wx
from gui.messageDialog import (
	DefaultButton,
	DefaultButtonSet,
	MessageDialog,
	Button,
	EscapeCode,
	ReturnCode,
	DialogType,
	_flattenButtons,
)


NO_CALLBACK = (EscapeCode.NONE, None)


def dummyCallback1(*a):
	pass


def dummyCallback2(*a):
	pass


class MDTestBase(unittest.TestCase):
	"""Base class for test cases testing MessageDialog. Handles wx initialisation."""

	def setUp(self) -> None:
		self.app = wx.App()
		self.dialog = MessageDialog(None, "Test dialog")


@patch.object(wx.ArtProvider, "GetIconBundle")
class Test_MessageDialog_Icons(MDTestBase):
	"""Test that message dialog icons are set correctly."""

	def test_setIcon_with_type_with_icon(self, mocked_GetIconBundle: MagicMock):
		"""Test that setting the dialog's icons has an effect when the dialog's type has icons."""
		mocked_GetIconBundle.return_value = wx.IconBundle()
		type = DialogType.ERROR
		self.dialog._setIcon(type)
		mocked_GetIconBundle.assert_called_once()

	def test_setIcon_with_type_without_icon(self, mocked_GetIconBundle: MagicMock):
		"""Test that setting the dialog's icons doesn't have an effect when the dialog's type doesn't have icons."""
		type = DialogType.STANDARD
		self.dialog._setIcon(type)
		mocked_GetIconBundle.assert_not_called()


@patch("winsound.MessageBeep")
class Test_MessageDialog_Sounds(MDTestBase):
	"""Test that message dialog sounds are set and played correctly."""

	def test_playSound_with_type_with_Sound(self, mocked_MessageBeep: MagicMock):
		"""Test that sounds are played for message dialogs whose type has an associated sound."""
		type = DialogType.ERROR
		self.dialog._setSound(type)
		self.dialog._playSound()
		mocked_MessageBeep.assert_called_once()

	def test_playSound_with_type_without_Sound(self, mocked_MessageBeep: MagicMock):
		"""Test that no sounds are played for message dialogs whose type has an associated sound."""
		type = DialogType.STANDARD
		self.dialog._setSound(type)
		self.dialog._playSound()
		mocked_MessageBeep.assert_not_called()


class Test_MessageDialog_Buttons(MDTestBase):
	def test_addOkButton(self):
		"""Test adding an OK button to the dialog."""
		self.dialog.addOkButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_OK), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_OK])
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			id, callback = self.dialog._getDefaultAction()
			self.assertEqual(id, ReturnCode.OK)
			self.assertIsNotNone(callback)

	def test_addCancelButton(self):
		"""Test adding a Cancel button to the dialog."""
		self.dialog.addCancelButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_CANCEL])
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			id, callback = self.dialog._getDefaultAction()
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertIsNotNone(callback)

	def test_addYesButton(self):
		"""Test adding a Yes button to the dialog."""
		self.dialog.addYesButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_YES])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addNoButton(self):
		"""Test adding a No button to the dialog."""
		self.dialog.addNoButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_NO])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addSaveButton(self):
		"""Test adding a Save button to the dialog."""
		self.dialog.addSaveButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_SAVE), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_SAVE])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addApplyButton(self):
		"""Test adding an Apply button to the dialog."""
		self.dialog.addApplyButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_APPLY), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_APPLY])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addCloseButton(self):
		"""Test adding a Close button to the dialog."""
		self.dialog.addCloseButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CLOSE), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_CLOSE])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addHelpButton(self):
		"""Test adding a Help button to the dialog."""
		self.dialog.addHelpButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_HELP), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_HELP])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addOkCancelButtons(self):
		"""Test adding OK and Cancel buttons to the dialog."""
		self.dialog.addOkCancelButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_OK), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_OK, wx.ID_CANCEL))
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertIsNotNone(self.dialog._getDefaultAction())

	def test_addYesNoButtons(self):
		"""Test adding Yes and No buttons to the dialog."""
		self.dialog.addYesNoButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_YES, wx.ID_NO))
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_addYesNoCancelButtons(self):
		"""Test adding Yes, No and Cancel buttons to the dialog."""
		self.dialog.addYesNoCancelButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_YES, wx.ID_NO, wx.ID_CANCEL))
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertIsNotNone(self.dialog._getDefaultAction())

	def test_addSaveNoCancelButtons(self):
		"""Test adding Save, Don't save and Cancel buttons to the dialog."""
		self.dialog.addSaveNoCancelButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_SAVE), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_SAVE, wx.ID_NO, wx.ID_CANCEL))
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)
		with self.subTest("Test default action assignment."):
			self.assertIsNotNone(self.dialog._getDefaultAction())

	def test_addButton_with_default_focus(self):
		"""Test adding a button with default focus."""
		self.dialog.addButton(
			Button(label="Custom", id=ReturnCode.CUSTOM_1, default_focus=True),
		)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CUSTOM_1)

	def test_addButton_with_default_action(self):
		"""Test adding a button with default action."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				default_action=True,
				closes_dialog=True,
			),
		)
		id, command = self.dialog._getDefaultAction()
		self.assertEqual(id, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closes_dialog)

	def test_addButton_with_non_closing_default_action(self):
		"""Test adding a button with default action that does not close the dialog."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				default_action=True,
				closes_dialog=False,
			),
		)
		id, command = self.dialog._getDefaultAction()
		self.assertEqual(id, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closes_dialog)


class Test_MessageDialog_DefaultAction(MDTestBase):
	def test_defaultAction_defaultEscape_OkCancel(self):
		"""Test that when adding OK and Cancel buttons with default escape code, that the default action is cancel."""
		self.dialog.addOkButton(callback=dummyCallback1).addCancelButton(callback=dummyCallback2)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closes_dialog)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_defaultAction_defaultEscape_CancelOk(self):
		"""Test that when adding cancel and ok buttons with default escape code, that the default action is cancel."""
		self.dialog.addCancelButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closes_dialog)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_defaultAction_defaultEscape_OkClose(self):
		"""Test that when adding OK and Close buttons with default escape code, that the default action is OK."""
		self.dialog.addOkButton(callback=dummyCallback1).addCloseButton(callback=dummyCallback2)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closes_dialog)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_defaultAction_defaultEscape_CloseOk(self):
		"""Test that when adding Close and OK buttons with default escape code, that the default action is OK."""
		self.dialog.addCloseButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closes_dialog)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_setDefaultAction_existant_action(self):
		"""Test that setting the default action results in the correct action being returned from both getDefaultAction and getDefaultActionOrFallback."""
		self.dialog.addYesNoButtons()
		self.dialog.setDefaultAction(ReturnCode.YES)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, ReturnCode.YES)
			self.assertIsNone(command.callback)
			self.assertTrue(command.closes_dialog)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_setDefaultAction_nonexistant_action(self):
		"""Test that setting the default action to an action that has not been set up results in KeyError, and that a fallback action is returned from getDefaultActionOrFallback."""
		self.dialog.addYesNoButtons()
		with self.subTest("Test getting the default action."):
			with self.assertRaises(KeyError):
				self.dialog.setDefaultAction(ReturnCode.APPLY)
		with self.subTest("Test getting the fallback default action."):
			self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_setDefaultAction_nonclosing_action(self):
		"""Check that setting the default action to an action that does not close the dialog fails with a ValueError."""
		self.dialog.addOkButton().addApplyButton(closes_dialog=False)
		with self.subTest("Test getting the default action."):
			with self.assertRaises(ValueError):
				self.dialog.setDefaultAction(ReturnCode.APPLY)

	def test_getDefaultActionOrFallback_no_controls(self):
		"""Test that getDefaultActionOrFallback returns wx.ID_NONE and a close command with no callback when the dialog has no buttons."""
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, EscapeCode.NONE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closes_dialog)

	def test_getDefaultActionOrFallback_no_defaultFocus_closing_button(self):
		"""Test that getDefaultActionOrFallback returns the first button when no default action or default focus is specified."""
		self.dialog.addApplyButton(closes_dialog=False).addCloseButton()
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closes_dialog)

	def test_getDefaultActionOrFallback_no_defaultFocus_no_closing_button(self):
		"""Test that getDefaultActionOrFallback returns the first button when no default action or default focus is specified."""
		self.dialog.addApplyButton(closes_dialog=False).addCloseButton(closes_dialog=False)
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, ReturnCode.APPLY)
		self.assertIsNotNone(command)
		self.assertTrue(command.closes_dialog)

	def test_getDefaultActionOrFallback_no_defaultAction(self):
		"""Test that getDefaultActionOrFallback returns the default focus if one is specified but there is no default action."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultFocus(ReturnCode.CLOSE)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CLOSE)
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closes_dialog)

	def test_getDefaultActionOrFallback_custom_defaultAction(self):
		"""Test that getDefaultActionOrFallback returns the custom defaultAction if set."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultAction(ReturnCode.CLOSE)
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closes_dialog)


class Test_FlattenButtons(unittest.TestCase):
	"""Tests for the _flattenButtons function."""

	def test_flatten_single_button(self):
		"""Test flattening a single button."""
		button = Button(id=ReturnCode.OK, label="OK")
		result = list(_flattenButtons([button]))
		self.assertEqual(result, [button])

	def test_flatten_multiple_buttons(self):
		"""Test flattening multiple buttons."""
		button1 = Button(id=ReturnCode.OK, label="OK")
		button2 = Button(id=ReturnCode.CANCEL, label="Cancel")
		result = list(_flattenButtons([button1, button2]))
		self.assertEqual(result, [button1, button2])

	def test_flatten_default_button_set(self):
		"""Test flattening a default button set."""
		result = list(_flattenButtons([DefaultButtonSet.OK_CANCEL]))
		expected = [DefaultButton.OK.value, DefaultButton.CANCEL.value]
		self.assertEqual(result, expected)

	def test_flatten_mixed_buttons_and_sets(self):
		"""Test flattening a mix of buttons and default button sets."""
		button = Button(id=ReturnCode.YES, label="Yes")
		result = list(_flattenButtons([button, DefaultButtonSet.OK_CANCEL]))
		expected = [button, DefaultButton.OK.value, DefaultButton.CANCEL.value]
		self.assertEqual(result, expected)

	def test_flatten_empty(self):
		"""Test flattening an empty iterable."""
		result = list(_flattenButtons([]))
		self.assertEqual(result, [])
