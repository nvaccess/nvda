# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier
import touchHandler
from unittest.mock import MagicMock, patch


class TestMagnifierTouchscreen(_TestMagnifier):
	"""Tests for touchscreen blocking/warning behaviour when the magnifier starts and stops."""

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
