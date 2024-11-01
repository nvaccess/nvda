# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the message dialog API."""

import unittest
from unittest.mock import MagicMock, patch

import wx
from gui.messageDialog import MessageDialog, MessageDialogType


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

	def test_addCancelButton(self):
		"""Test adding a Cancel button to the dialog."""
		self.dialog.addCancelButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_CANCEL])
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)

	def test_addYesButton(self):
		"""Test adding a Yes button to the dialog."""
		self.dialog.addYesButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_YES])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addNoButton(self):
		"""Test adding a No button to the dialog."""
		self.dialog.addNoButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_NO])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addSaveButton(self):
		"""Test adding a Save button to the dialog."""
		self.dialog.addSaveButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_SAVE), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_SAVE])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addApplyButton(self):
		"""Test adding an Apply button to the dialog."""
		self.dialog.addApplyButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_APPLY), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_APPLY])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addCloseButton(self):
		"""Test adding a Close button to the dialog."""
		self.dialog.addCloseButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CLOSE), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_CLOSE])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addHelpButton(self):
		"""Test adding a Help button to the dialog."""
		self.dialog.addHelpButton()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_HELP), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_HELP])
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addOkCancelButtons(self):
		self.dialog.addOkCancelButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_OK), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_OK, wx.ID_CANCEL))
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)

	def test_addYesNoButtons(self):
		self.dialog.addYesNoButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_YES, wx.ID_NO))
		with self.subTest("Test has default action."):
			self.assertFalse(self.dialog.hasDefaultAction)

	def test_addYesNoCancelButtons(self):
		self.dialog.addYesNoCancelButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_YES, wx.ID_NO, wx.ID_CANCEL))
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)

	def test_addSaveNoCancelButtons(self):
		self.dialog.addSaveNoCancelButtons()
		with self.subTest("Check button types"):
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_SAVE), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
			self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		with self.subTest("Test in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), (wx.ID_SAVE, wx.ID_NO, wx.ID_CANCEL))
		with self.subTest("Test has default action."):
			self.assertTrue(self.dialog.hasDefaultAction)
