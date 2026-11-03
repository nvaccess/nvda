# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the maximum number of characters on one line in browse mode."""

import unittest

import config
import wx
from gui.settingsDialogs import BrowseModePanel


class Test_BrowseModePanel_maxLineLength(unittest.TestCase):
	def setUp(self):
		self.app = wx.App()
		self.frame = wx.Frame(None)
		origMaxLineLength = config.conf["virtualBuffers"]["maxLineLength"]
		self.addCleanup(config.conf["virtualBuffers"].__setitem__, "maxLineLength", origMaxLineLength)
		self.panel = BrowseModePanel(self.frame)

	def tearDown(self):
		self.frame.Destroy()
		self.app.Destroy()

	def _saveMaxLineLength(self, value: int) -> int:
		self.panel.maxLengthEdit.SetValue(value)
		self.panel.onSave()
		return config.conf["virtualBuffers"]["maxLineLength"]

	def test_range(self):
		self.assertEqual(self.panel.maxLengthEdit.GetMin(), 0)
		self.assertEqual(self.panel.maxLengthEdit.GetMax(), 1000)

	def test_saveUpperLimit(self):
		"""Values above the previous upper limit of 250 are saved, up to 1000."""
		self.assertEqual(self._saveMaxLineLength(1000), 1000)

	def test_valueAboveUpperLimitIsClamped(self):
		self.assertEqual(self._saveMaxLineLength(1001), 1000)

	def test_saveZero(self):
		"""0 is saved, which disables splitting lines by length."""
		self.assertEqual(self._saveMaxLineLength(0), 0)
