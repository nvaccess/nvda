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
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_OK), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_OK])

	def test_addCancelButton(self):
		"""Test adding a Cancel button to the dialog."""
		self.dialog.addCancelButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CANCEL), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_CANCEL])

	def test_addYesButton(self):
		"""Test adding a Yes button to the dialog."""
		self.dialog.addYesButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_YES), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_YES])

	def test_addNoButton(self):
		"""Test adding a No button to the dialog."""
		self.dialog.addNoButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_NO), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_NO])

	def test_addSaveButton(self):
		"""Test adding a Save button to the dialog."""
		self.dialog.addSaveButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_SAVE), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_SAVE])

	def test_addApplyButton(self):
		"""Test adding an Apply button to the dialog."""
		self.dialog.addApplyButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_APPLY), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_APPLY])

	def test_addCloseButton(self):
		"""Test adding a Close button to the dialog."""
		self.dialog.addCloseButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_CLOSE), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_CLOSE])

	def test_addHelpButton(self):
		"""Test adding a Help button to the dialog."""
		self.dialog.addHelpButton()
		self.assertIsInstance(self.dialog.FindWindowById(wx.ID_HELP), wx.Button)
		self.assertEqual(self.dialog.GetMainButtonIds(), [wx.ID_HELP])
