# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from _magnifier.magnifier import Magnifier
from _magnifier.utils.types import Coordinates
import touchHandler
import unittest
from winAPI._displayTracking import getPrimaryDisplayOrientation
from unittest.mock import MagicMock, patch
import wx


class TestMagnifierTouchscreen(unittest.TestCase):
	"""Tests for touchscreen blocking/warning behaviour when the magnifier starts and stops."""

	@classmethod
	def setUpClass(cls):
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		self.mag_patcher = patch("winBindings.magnification")
		self.mock_mag = self.mag_patcher.start()
		self.mag_fs_patcher = patch("_magnifier.fullscreenMagnifier.magnification")
		self.mock_mag_fs = self.mag_fs_patcher.start()
		for mock in (self.mock_mag, self.mock_mag_fs):
			mock.MagInitialize.return_value = True
			mock.MagUninitialize.return_value = True
			mock.MagSetFullscreenTransform.return_value = True
			mock.MagSetFullscreenColorEffect.return_value = True

		self.magnifier = Magnifier()
		screenDimensions = getPrimaryDisplayOrientation()
		self.focusCoords = Coordinates(screenDimensions.width // 2, screenDimensions.height // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(return_value=self.focusCoords)

	def tearDown(self):
		if hasattr(self.magnifier, "_timer") and self.magnifier._timer:
			self.magnifier._timer.Stop()
			self.magnifier._timer = None
		if hasattr(self.magnifier, "_isActive") and self.magnifier._isActive:
			self.magnifier._isActive = False
		self.mag_fs_patcher.stop()
		self.mag_patcher.stop()

	def testStartMagnifierBlocksTouchWhenHandlerActive(self):
		"""blockTouchInput is set when the magnifier starts with the touch handler running."""
		with (
			patch("touchHandler.handler", new=MagicMock()),
			patch("touchHandler.blockTouchInput", False),
		):
			self.magnifier._startMagnifier()
			self.assertTrue(touchHandler.blockTouchInput)

	def testStartMagnifierWarnsWhenTouchSupportDisabled(self):
		"""Dialog shown when device has a touchscreen but NVDA touch support is disabled."""
		with (
			patch("touchHandler.handler", new=None),
			patch("winBindings.user32.GetSystemMetrics", return_value=5),
			patch("touchHandler.touchSupported", return_value=True),
			patch("_magnifier.magnifier.wx.CallAfter") as mock_call_after,
		):
			self.magnifier._startMagnifier()

		mock_call_after.assert_called_once()

	def testStartMagnifierWarnsOnPortableOrNoUIAccess(self):
		"""Dialog shown when device has a touchscreen but NVDA cannot intercept (portable/no UI access)."""
		with (
			patch("touchHandler.handler", new=None),
			patch("winBindings.user32.GetSystemMetrics", return_value=5),
			patch("touchHandler.touchSupported", return_value=False),
			patch("_magnifier.magnifier.wx.CallAfter") as mock_call_after,
		):
			self.magnifier._startMagnifier()

		mock_call_after.assert_called_once()

	def testStartMagnifierNoActionWithoutTouchscreen(self):
		"""No dialog and no blocking when the device has no touchscreen."""
		with (
			patch("touchHandler.handler", new=None),
			patch("winBindings.user32.GetSystemMetrics", return_value=0),
			patch("_magnifier.magnifier.wx.CallAfter") as mock_call_after,
		):
			self.magnifier._startMagnifier()

		mock_call_after.assert_not_called()

	def testStopMagnifierUnblocksTouchInput(self):
		"""blockTouchInput is reset to False when the magnifier stops with the touch handler active."""
		self.magnifier._stopTimer = MagicMock()
		self.magnifier._isActive = True
		touchHandler.blockTouchInput = True
		self.addCleanup(setattr, touchHandler, "blockTouchInput", False)

		with patch("touchHandler.handler", new=MagicMock()):
			self.magnifier._stopMagnifier()

		self.assertFalse(touchHandler.blockTouchInput)
