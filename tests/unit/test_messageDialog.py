# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the message dialog API."""

import unittest
from unittest.mock import MagicMock, patch

import wx
from gui.messageDialog import (
	MessageDialog,
	MessageDialogEscapeCode,
	MessageDialogReturnCode,
	MessageDialogType,
)


NO_CALLBACK = (MessageDialogEscapeCode.NONE, None)


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
		mocked_GetIconBundle.return_value = wx.IconBundle()
		type = MessageDialogType.ERROR
		self.dialog._MessageDialog__setIcon(type)
		mocked_GetIconBundle.assert_called_once()

	def test_setIcon_with_type_without_icon(self, mocked_GetIconBundle: MagicMock):
		type = MessageDialogType.STANDARD
		self.dialog._MessageDialog__setIcon(type)
		mocked_GetIconBundle.assert_not_called()


@patch("winsound.MessageBeep")
class Test_MessageDialog_Sounds(MDTestBase):
	"""Test that message dialog sounds are set and played correctly."""

	def test_playSound_with_type_with_Sound(self, mocked_MessageBeep: MagicMock):
		type = MessageDialogType.ERROR
		self.dialog._MessageDialog__setSound(type)
		self.dialog._MessageDialog__playSound()
		mocked_MessageBeep.assert_called_once()

	def test_playSound_with_type_without_Sound(self, mocked_MessageBeep: MagicMock):
		type = MessageDialogType.STANDARD
		self.dialog._MessageDialog__setSound(type)
		self.dialog._MessageDialog__playSound()
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
			self.assertEqual(id, MessageDialogReturnCode.OK)
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
			self.assertEqual(id, MessageDialogReturnCode.CANCEL)
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


class Test_MessageDialog_DefaultAction(MDTestBase):
	def test_defaultAction_defaultEscape_OkCancel(self):
		"""Test that when adding OK and Cancel buttons with default escape code, that the default action is cancel."""
		self.dialog.addOkButton(callback=dummyCallback1).addCancelButton(callback=dummyCallback2)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, MessageDialogReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_defaultAction_defaultEscape_CancelOk(self):
		"""Test that when adding cancel and ok buttons with default escape code, that the default action is cancel."""
		self.dialog.addCancelButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, MessageDialogReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_defaultAction_defaultEscape_OkClose(self):
		"""Test that when adding OK and Close buttons with default escape code, that the default action is OK."""
		self.dialog.addOkButton(callback=dummyCallback1).addCloseButton(callback=dummyCallback2)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, MessageDialogReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_defaultAction_defaultEscape_CloseOk(self):
		"""Test that when adding Close and OK buttons with default escape code, that the default action is OK."""
		self.dialog.addCloseButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, MessageDialogReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_setDefaultAction_existant_action(self):
		self.dialog.addYesNoButtons()
		self.dialog.setDefaultAction(MessageDialogReturnCode.YES)
		id, command = self.dialog._getDefaultAction()
		with self.subTest("Test getting the default action."):
			self.assertEqual(id, MessageDialogReturnCode.YES)
			self.assertIsNone(command.callback)
		with self.subTest(
			"Test getting the default action or fallback returns the same as getting the default action.",
		):
			self.assertEqual((id, command), self.dialog._getDefaultActionOrFallback())

	def test_setDefaultAction_nonexistant_action(self):
		self.dialog.addYesNoButtons()
		with self.assertRaises(KeyError):
			self.dialog.setDefaultAction(MessageDialogReturnCode.APPLY)
		self.assertEqual(self.dialog._getDefaultAction(), NO_CALLBACK)

	def test_setDefaultAction_nonclosing_action(self):
		self.dialog.addOkButton().addApplyButton(closes_dialog=False)
		with self.assertRaises(ValueError):
			self.dialog.setDefaultAction(MessageDialogReturnCode.APPLY)

	def test_getDefaultActionOrFallback_no_controls(self):
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, MessageDialogEscapeCode.NONE)
		self.assertIsNotNone(command)
		self.assertEqual(command.closes_dialog, True)

	def test_getDefaultActionOrFallback_no_defaultFocus(self):
		self.dialog.addApplyButton().addCloseButton()
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, MessageDialogReturnCode.APPLY)
		self.assertIsNotNone(command)
		self.assertEqual(command.closes_dialog, True)

	def test_getDefaultActionOrFallback_no_defaultAction(self):
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultFocus(MessageDialogReturnCode.CLOSE)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), MessageDialogReturnCode.CLOSE)
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, MessageDialogReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertEqual(command.closes_dialog, True)

	def test_getDefaultActionOrFallback_custom_defaultAction(self):
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultAction(MessageDialogReturnCode.CLOSE)
		id, command = self.dialog._getDefaultActionOrFallback()
		self.assertEqual(id, MessageDialogReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertEqual(command.closes_dialog, True)
