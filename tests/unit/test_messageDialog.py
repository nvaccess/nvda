# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the message dialog API."""

import unittest
from unittest.mock import MagicMock, patch

import wx
from gui.messageDialog import MessageDialog, MessageDialogType


@patch.object(wx.ArtProvider, "GetIconBundle")
class Test_MessageDialog_Icons(unittest.TestCase):
	"""Tests for the message dialog API."""

	def setUp(self) -> None:
		self.app = wx.App()
		self.dialog = MessageDialog(None, "Test dialog")

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
class Test_MessageDialog_Sounds(unittest.TestCase):
	def setUp(self):
		self.app = wx.App()
		self.dialog = MessageDialog(None, "Test dialog")

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
