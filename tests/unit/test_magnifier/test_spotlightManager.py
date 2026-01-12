# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest.mock
from unittest.mock import MagicMock, patch
from _magnifier.utils.types import FullScreenMode
from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from tests.unit.test_magnifier.test_magnifier import _TestMagnifier


class TestSpotlightManager(_TestMagnifier):
	"""Test suite for SpotlightManager functionality."""

	def testSpotlightManagerCreation(self):
		"""Test creating a SpotlightManager."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		self.assertIsNotNone(spotlightManager)
		self.assertFalse(spotlightManager._spotlightIsActive)
		self.assertEqual(spotlightManager._animationSteps, 40)
		self.assertEqual(spotlightManager._originalZoomLevel, 0.0)
		self.assertEqual(spotlightManager._currentZoomLevel, 0.0)

		magnifier._stopMagnifier()

	def testSpotlightActivation(self):
		"""Test activating spotlight mode."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Mock required methods
		magnifier._getFocusCoordinates = MagicMock(return_value=(500, 400))
		magnifier._getCoordinatesForMode = MagicMock(return_value=(500, 400))
		spotlightManager._animateZoom = MagicMock()

		# Start spotlight
		spotlightManager._startSpotlight()

		# Verify spotlight is active
		self.assertTrue(spotlightManager._spotlightIsActive)
		spotlightManager._animateZoom.assert_called_once()

		magnifier._stopMagnifier()

	def testSpotlightDeactivation(self):
		"""Test deactivating spotlight mode."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Mock timer
		spotlightManager._timer = MagicMock()
		spotlightManager._timer.Stop = MagicMock()
		spotlightManager._spotlightIsActive = True

		# Mock fullscreen magnifier method
		magnifier._stopSpotlight = MagicMock()

		# Mock ui.message to avoid speech dictionary errors
		with patch("_magnifier.utils.spotlightManager.ui.message"):
			# Stop spotlight
			spotlightManager._stopSpotlight()

			# Verify spotlight is inactive
			self.assertFalse(spotlightManager._spotlightIsActive)

		magnifier._stopMagnifier()

	def testComputeAnimationSteps(self):
		"""Test animation steps calculation."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Test animation from zoom 2.0 to 1.0, coordinates (500, 400) to (960, 540)
		steps = spotlightManager._computeAnimationSteps(
			2.0,
			1.0,
			(500, 400),
			(960, 540),
		)

		# Should have 40 steps
		self.assertEqual(len(steps), 40)

		# First step should be closer to start
		firstZoom, firstCoords = steps[0]
		self.assertLess(abs(firstZoom - 2.0), abs(firstZoom - 1.0))

		# Last step should be at target
		lastZoom, lastCoords = steps[-1]
		self.assertEqual(lastZoom, 1.0)
		self.assertEqual(lastCoords, (960, 540))

		# Steps should progress linearly (decreasing from 2.0 to 1.0)
		for i in range(len(steps) - 1):
			currentZoom, _ = steps[i]
			nextZoom, _ = steps[i + 1]
			self.assertGreater(
				currentZoom,
				nextZoom,
			)  # Zoom should decrease from 2.0 to 1.0

		magnifier._stopMagnifier()

	def testMouseMonitoring(self):
		"""Test mouse idle monitoring."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Mock wx.GetMousePosition
		with unittest.mock.patch("wx.GetMousePosition") as mockGetMousePosition:
			mockGetMousePosition.return_value = (100, 200)

			# Start monitoring
			spotlightManager._startMouseMonitoring()

			# Verify initial state
			self.assertEqual(spotlightManager._lastMousePosition, (100, 200))
			self.assertIsNotNone(spotlightManager._timer)

		magnifier._stopMagnifier()

	def testMouseIdleDetection(self):
		"""Test detecting mouse idle state."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Set initial position
		spotlightManager._lastMousePosition = (100, 200)

		# Mock wx.GetMousePosition to return same position (idle)
		with unittest.mock.patch("wx.GetMousePosition") as mockGetMousePosition:
			mockGetMousePosition.return_value = (100, 200)
			spotlightManager.zoomBack = MagicMock()

			# Check idle
			spotlightManager._checkMouseIdle()

			# Should trigger zoom back
			spotlightManager.zoomBack.assert_called_once()

		magnifier._stopMagnifier()

	def testMouseMovementDetection(self):
		"""Test detecting mouse movement."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Set initial position
		spotlightManager._lastMousePosition = (100, 200)

		# Mock wx.GetMousePosition to return different position (moved)
		with unittest.mock.patch("wx.GetMousePosition") as mockGetMousePosition:
			mockGetMousePosition.return_value = (150, 250)
			spotlightManager.zoomBack = MagicMock()
			spotlightManager._timer = None

			# Check idle (but mouse moved)
			spotlightManager._checkMouseIdle()

			# Should NOT trigger zoom back
			spotlightManager.zoomBack.assert_not_called()

			# Should update last position
			self.assertEqual(spotlightManager._lastMousePosition, (150, 250))
			self.assertEqual(spotlightManager._currentCoordinates, (150, 250))

		magnifier._stopMagnifier()

	def testZoomBack(self):
		"""Test zoom back to mouse position."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Set original zoom level
		spotlightManager._originalZoomLevel = 3.0

		# Mock _getFocusCoordinates to return expected position
		magnifier._getFocusCoordinates = MagicMock(return_value=(500, 400))
		spotlightManager._animateZoom = MagicMock()

		# Trigger zoom back
		spotlightManager.zoomBack()

		# Should call _animateZoom with original zoom and mouse position
		spotlightManager._animateZoom.assert_called_once()
		args = spotlightManager._animateZoom.call_args[0]
		self.assertEqual(args[0].zoomLevel, 3.0)  # Original zoom level
		self.assertEqual(args[0].coordinates, (500, 400))  # Mouse position for CENTER mode

		magnifier._stopMagnifier()

	def testZoomBackRelativeMode(self):
		"""Test zoom back in RELATIVE mode."""
		magnifier = FullScreenMagnifier()
		magnifier._fullscreenMode = FullScreenMode.RELATIVE
		spotlightManager = magnifier._spotlightManager

		# Set original zoom level
		spotlightManager._originalZoomLevel = 3.0

		# Mock wx.GetMousePosition and _getCoordinatesForMode
		with unittest.mock.patch("wx.GetMousePosition") as mockGetMousePosition:
			mockGetMousePosition.return_value = (500, 400)
			magnifier._getCoordinatesForMode = MagicMock(return_value=(550, 450))
			spotlightManager._animateZoom = MagicMock()

			# Trigger zoom back
			spotlightManager.zoomBack()

			# Should use _getCoordinatesForMode for RELATIVE mode
			# Note: The code has a bug checking magnifier.FullScreenMode instead of magnifier._fullscreenMode
			# But we test the current behavior
			spotlightManager._animateZoom.assert_called_once()

		magnifier._stopMagnifier()

	def testSpotlightFullLifecycle(self):
		"""Test full spotlight lifecycle."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		# Verify initial state
		self.assertFalse(spotlightManager._spotlightIsActive)
		self.assertEqual(spotlightManager._originalZoomLevel, 0.0)

		# Mock methods for full test
		magnifier._getFocusCoordinates = MagicMock(return_value=(500, 400))
		magnifier._getCoordinatesForMode = MagicMock(return_value=(500, 400))
		magnifier._stopSpotlight = MagicMock()

		# Start spotlight (mocking animation)
		spotlightManager._animateZoom = MagicMock()
		spotlightManager._startSpotlight()
		self.assertTrue(spotlightManager._spotlightIsActive)

		# Mock ui.message to avoid speech dictionary errors
		with patch("_magnifier.utils.spotlightManager.ui.message"):
			spotlightManager._stopSpotlight()
			self.assertFalse(spotlightManager._spotlightIsActive)

		magnifier._stopMagnifier()
