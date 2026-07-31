# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier
import touchHandler
from unittest.mock import MagicMock, patch


class TestMagnifierTouchscreen(_TestMagnifier):
	"""Tests for touchscreen behaviour when the magnifier starts and stops."""

	def testStartMagnifierDoesNotBlockTouchWhenHandlerActive(self):
		"""blockTouchInput remains False when the magnifier starts with touch handler running."""
		with (
			patch("touchHandler.handler", new=MagicMock()),
			patch("touchHandler.blockTouchInput", False),
		):
			self.magnifier._startMagnifier()
			self.assertFalse(touchHandler.blockTouchInput)

	def testStartMagnifierDoesNotShowTouchWarning(self):
		"""No warning dialog is shown when starting magnifier on touch-capable devices."""
		with (
			patch("touchHandler.handler", new=None),
			patch("winBindings.user32.GetSystemMetrics", return_value=5),
			patch("touchHandler.touchSupported", return_value=True),
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
