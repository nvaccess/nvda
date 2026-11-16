# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for leaving the full-screen magnifier's screen overview cleanly."""

from unittest.mock import MagicMock, patch

from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from _magnifier.utils.types import Coordinates

from .test_magnifier import _TestMagnifier


class _TestScreenOverview(_TestMagnifier):
	def setUp(self):
		super().setUp()
		self.callLaterPatcher = patch("_magnifier.utils.spotlightManager.wx.CallLater")
		self.mockCallLater = self.callLaterPatcher.start()
		self.addCleanup(self.callLaterPatcher.stop)
		self.uiMessagePatcher = patch("_magnifier.utils.spotlightManager.ui.message")
		self.mockUiMessage = self.uiMessagePatcher.start()
		self.addCleanup(self.uiMessagePatcher.stop)
		self.fullscreen = FullScreenMagnifier()
		self.fullscreen._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=Coordinates(500, 400),
		)
		self.fullscreen.zoomLevel = 300
		self.fullscreen._startMagnifier()
		self.fullscreen._fullscreenMagnifier = MagicMock()
		self.spotlight = self.fullscreen._spotlightManager

	def tearDown(self):
		if self.fullscreen._timer:
			self.fullscreen._timer.Stop()
			self.fullscreen._timer = None
		self.fullscreen._isActive = False
		super().tearDown()

	def _startDuringAnimation(self) -> MagicMock:
		"""Start the overview and run its first step; return the pending step timer."""
		self.fullscreen._startSpotlight()
		self.assertTrue(self.spotlight._spotlightIsActive)
		return self.mockCallLater.return_value

	def _startDuringHold(self) -> MagicMock:
		"""Put the overview at the end of its zoom-out; return the pending mouse-idle timer."""
		self.spotlight._originalZoomLevel = 300
		self.spotlight._spotlightIsActive = True
		self.fullscreen._setZoomRawValue(100)
		self.spotlight._timer = MagicMock()
		return self.spotlight._timer


class TestStopDuringOverview(_TestScreenOverview):
	def test_stopDuringAnimation_stopsTheSteps(self):
		stepTimer = self._startDuringAnimation()
		self.fullscreen._fullscreenMagnifier.reset_mock()
		self.fullscreen._stopMagnifier()
		stepTimer.Stop.assert_called_once()
		self.assertFalse(self.spotlight._spotlightIsActive)
		self.fullscreen._fullscreenMagnifier.assert_not_called()

	def test_stopDuringHold_isSilentAndDoesNotRestartUpdates(self):
		idleTimer = self._startDuringHold()
		self.fullscreen._stopMagnifier()
		idleTimer.Stop.assert_called_once()
		self.assertFalse(self.spotlight._spotlightIsActive)
		self.mockUiMessage.assert_not_called()
		self.assertIsNone(self.fullscreen._timer)

	def test_stopDuringOverview_restoresTheZoomLevel(self):
		self._startDuringHold()
		self.fullscreen._stopMagnifier()
		self.assertEqual(self.fullscreen.zoomLevel, 300)

	def test_cancel_whenInactive_changesNothing(self):
		self.fullscreen._setZoomRawValue(250)
		self.spotlight.cancel()
		self.assertEqual(self.fullscreen.zoomLevel, 250)
		self.mockUiMessage.assert_not_called()
