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
from parameterized import parameterized
from typing import Iterable, NamedTuple


NO_CALLBACK = (EscapeCode.NONE, None)


def dummyCallback1(*a):
	pass


def dummyCallback2(*a):
	pass


class AddDefaultButtonHelpersArgList(NamedTuple):
	func: str
	expectedButtons: Iterable[int]
	expectedHasFallback: bool = False
	expectedFallbackId: int = wx.ID_NONE


class MDTestBase(unittest.TestCase):
	"""Base class for test cases testing MessageDialog. Handles wx initialisation."""

	def setUp(self) -> None:
		self.app = wx.App()
		self.dialog = MessageDialog(None, "Test dialog", buttons=None)


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
	@parameterized.expand(
		[
			AddDefaultButtonHelpersArgList(
				func="addOkButton",
				expectedButtons=(wx.ID_OK,),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_OK,
			),
			AddDefaultButtonHelpersArgList(
				func="addCancelButton",
				expectedButtons=(wx.ID_CANCEL,),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
			AddDefaultButtonHelpersArgList(func="addYesButton", expectedButtons=(wx.ID_YES,)),
			AddDefaultButtonHelpersArgList(func="addNoButton", expectedButtons=(wx.ID_NO,)),
			AddDefaultButtonHelpersArgList(func="addSaveButton", expectedButtons=(wx.ID_SAVE,)),
			AddDefaultButtonHelpersArgList(func="addApplyButton", expectedButtons=(wx.ID_APPLY,)),
			AddDefaultButtonHelpersArgList(func="addCloseButton", expectedButtons=(wx.ID_CLOSE,)),
			AddDefaultButtonHelpersArgList(func="addHelpButton", expectedButtons=(wx.ID_HELP,)),
			AddDefaultButtonHelpersArgList(
				func="addOkCancelButtons",
				expectedButtons=(wx.ID_OK, wx.ID_CANCEL),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
			AddDefaultButtonHelpersArgList(func="addYesNoButtons", expectedButtons=(wx.ID_YES, wx.ID_NO)),
			AddDefaultButtonHelpersArgList(
				func="addYesNoCancelButtons",
				expectedButtons=(wx.ID_YES, wx.ID_NO, wx.ID_CANCEL),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
			AddDefaultButtonHelpersArgList(
				func="addSaveNoCancelButtons",
				expectedButtons=(wx.ID_SAVE, wx.ID_NO, wx.ID_CANCEL),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
		],
	)
	def test_addDefaultButtonHelpers(
		self,
		func: str,
		expectedButtons: Iterable[int],
		expectedHasFallback: bool,
		expectedFallbackId: int,
	):
		"""Test the various /add*buttons?/ functions."""
		getattr(self.dialog, func)()
		with self.subTest("Test all expected buttons are in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), expectedButtons)
		for id in expectedButtons:
			with self.subTest("Check that all buttons have the expected type", id=id):
				self.assertIsInstance(self.dialog.FindWindowById(id), wx.Button)
		with self.subTest("Test whether the fallback status is as expected."):
			self.assertEqual(self.dialog.hasDefaultAction, expectedHasFallback)
		with self.subTest("Test whether getting the fallback action returns the expected id and action type"):
			actualFallbackId, actualFallbackAction = self.dialog._getFallbackAction()
			self.assertEqual(actualFallbackId, expectedFallbackId)
			if expectedHasFallback:
				self.assertIsNotNone(actualFallbackAction)
			else:
				self.assertIsNone(actualFallbackAction)

	def test_addButton_with_defaultFocus(self):
		"""Test adding a button with default focus."""
		self.dialog.addButton(
			Button(label="Custom", id=ReturnCode.CUSTOM_1, defaultFocus=True),
		)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CUSTOM_1)

	def test_addButton_with_fallbackAction(self):
		"""Test adding a button with fallback action."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				fallbackAction=True,
				closesDialog=True,
			),
		)
		id, command = self.dialog._getFallbackAction()
		self.assertEqual(id, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closesDialog)

	def test_addButton_with_non_closing_fallbackAction(self):
		"""Test adding a button with fallback action that does not close the dialog."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				fallbackAction=True,
				closesDialog=False,
			),
		)
		id, command = self.dialog._getFallbackAction()
		self.assertEqual(id, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closesDialog)


class Test_MessageDialog_DefaultAction(MDTestBase):
	def test_defaultAction_defaultEscape_OkCancel(self):
		"""Test that when adding OK and Cancel buttons with default escape code, that the fallback action is cancel."""
		self.dialog.addOkButton(callback=dummyCallback1).addCancelButton(callback=dummyCallback2)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_defaultAction_defaultEscape_CancelOk(self):
		"""Test that when adding cancel and ok buttons with default escape code, that the fallback action is cancel."""
		self.dialog.addCancelButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_defaultAction_defaultEscape_OkClose(self):
		"""Test that when adding OK and Close buttons with default escape code, that the fallback action is OK."""
		self.dialog.addOkButton(callback=dummyCallback1).addCloseButton(callback=dummyCallback2)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_defaultAction_defaultEscape_CloseOk(self):
		"""Test that when adding Close and OK buttons with default escape code, that the fallback action is OK."""
		self.dialog.addCloseButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_setDefaultAction_existant_action(self):
		"""Test that setting the fallback action results in the correct action being returned from both getFallbackAction and getFallbackActionOrFallback."""
		self.dialog.addYesNoButtons()
		self.dialog.setDefaultAction(ReturnCode.YES)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.YES)
			self.assertIsNone(command.callback)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_setDefaultAction_nonexistant_action(self):
		"""Test that setting the fallback action to an action that has not been set up results in KeyError, and that a fallback action is returned from getFallbackActionOrFallback."""
		self.dialog.addYesNoButtons()
		with self.subTest("Test getting the fallback action."):
			with self.assertRaises(KeyError):
				self.dialog.setDefaultAction(ReturnCode.APPLY)
		with self.subTest("Test getting the fallback fallback action."):
			self.assertEqual(self.dialog._getFallbackAction(), NO_CALLBACK)

	def test_setDefaultAction_nonclosing_action(self):
		"""Check that setting the fallback action to an action that does not close the dialog fails with a ValueError."""
		self.dialog.addOkButton().addApplyButton(closesDialog=False)
		with self.subTest("Test getting the fallback action."):
			with self.assertRaises(ValueError):
				self.dialog.setDefaultAction(ReturnCode.APPLY)

	def test_getFallbackActionOrFallback_no_controls(self):
		"""Test that getFallbackActionOrFallback returns wx.ID_NONE and a close command with no callback when the dialog has no buttons."""
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, EscapeCode.NONE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_no_defaultFocus_closing_button(self):
		"""Test that getFallbackActionOrFallback returns the first button when no fallback action or default focus is specified."""
		self.dialog.addApplyButton(closesDialog=False).addCloseButton()
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_no_defaultFocus_no_closing_button(self):
		"""Test that getFallbackActionOrFallback returns the first button when no fallback action or default focus is specified."""
		self.dialog.addApplyButton(closesDialog=False).addCloseButton(closesDialog=False)
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.APPLY)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_no_defaultAction(self):
		"""Test that getFallbackActionOrFallback returns the default focus if one is specified but there is no fallback action."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultFocus(ReturnCode.CLOSE)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CLOSE)
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_custom_defaultAction(self):
		"""Test that getFallbackActionOrFallback returns the custom defaultAction if set."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultAction(ReturnCode.CLOSE)
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)


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
