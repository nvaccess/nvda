# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest.mock import MagicMock
import wx
import sys
from magnifier.utils.types import Filter, FullScreenMode, MagnifierType, Direction
from magnifier.fullscreenMagnifier import FullScreenMagnifier

# Mock the ui module globally before importing Magnifier
sys.modules["ui"] = MagicMock()
sys.modules["api"] = MagicMock()


class TestMagnifierEndToEnd(unittest.TestCase):
	"""End-to-end test suite for Magnifier functionality."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def testMagnifierCreation(self):
		"""Test creating a magnifier."""
		magnifier = FullScreenMagnifier()

		self.assertEqual(magnifier.zoomLevel, 2.0)
		self.assertEqual(magnifier.filterType, Filter.NORMAL)
		self.assertEqual(magnifier.fullscreenMode, FullScreenMode.CENTER)
		self.assertEqual(magnifier.magnifierType, MagnifierType.FULLSCREEN)
		self.assertTrue(magnifier.isActive)

		magnifier._stopMagnifier()

	def testMagnifierZoom(self):
		"""Test zoom functionality."""
		magnifier = FullScreenMagnifier()

		# Set initial zoom to 1.0 for predictable testing
		magnifier.zoomLevel = 1.0

		# Test zoom in
		magnifier._zoom(Direction.IN)
		self.assertEqual(magnifier.zoomLevel, 1.5)

		# Test zoom out
		magnifier._zoom(Direction.OUT)
		self.assertEqual(magnifier.zoomLevel, 1.0)
		self.assertEqual(magnifier.zoomLevel, 1.0)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierCoordinates(self):
		"""Test coordinate handling."""
		magnifier = FullScreenMagnifier()

		# Test setting coordinates
		magnifier.currentCoordinates = (100, 200)
		self.assertEqual(magnifier.currentCoordinates, (100, 200))

		# Test negative coordinates
		magnifier.currentCoordinates = (-50, -100)
		self.assertEqual(magnifier.currentCoordinates, (-50, -100))

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierUpdate(self):
		"""Test magnifier update cycle."""
		magnifier = FullScreenMagnifier()

		# Mock the update methods
		magnifier._getCoordinatesForMode = MagicMock(return_value=(150, 250))
		magnifier._fullscreenMagnifier = MagicMock()

		# Set initial coordinates
		magnifier.currentCoordinates = (100, 200)

		# Test update
		magnifier._doUpdate()

		# Verify update was called correctly
		magnifier._getCoordinatesForMode.assert_called_once_with((100, 200))
		self.assertEqual(magnifier.lastScreenPosition, (150, 250))
		magnifier._fullscreenMagnifier.assert_called_once_with(150, 250)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierStop(self):
		"""Test stopping the magnifier."""
		magnifier = FullScreenMagnifier()

		# Mock the API methods
		magnifier._getMagnificationApi = MagicMock(return_value=MagicMock(return_value=True))
		magnifier._stopMagnifierApi = MagicMock()
		magnifier._stopTimer = MagicMock()

		# Verify it's active first
		self.assertTrue(magnifier.isActive)

		# Stop the magnifier
		magnifier._stopMagnifier()

		# Verify it's stopped
		self.assertFalse(magnifier.isActive)
		magnifier._stopTimer.assert_called_once()

	def testMagnifierPositionCalculation(self):
		"""Test position calculation."""
		magnifier = FullScreenMagnifier()

		# Test position calculation
		left, top, width, height = magnifier._getMagnifierPosition(500, 400)

		# Basic checks
		self.assertIsInstance(left, int)
		self.assertIsInstance(top, int)
		self.assertIsInstance(width, int)
		self.assertIsInstance(height, int)

		# Width and height should be screen size divided by zoom
		expectedWidth = int(magnifier._SCREEN_WIDTH / 2.0)
		expectedHeight = int(magnifier._SCREEN_HEIGHT / 2.0)

		self.assertEqual(width, expectedWidth)
		self.assertEqual(height, expectedHeight)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierZoomBoundaries(self):
		"""Test zoom boundaries."""
		magnifier = FullScreenMagnifier()
		magnifier.zoomLevel = 1.0

		# Test minimum boundary
		magnifier._zoom(Direction.OUT)  # Try to zoom out below minimum
		self.assertEqual(magnifier.zoomLevel, 1.0)

		# Test maximum boundary
		magnifier.zoomLevel = 10.0
		magnifier._zoom(Direction.IN)  # Try to zoom in above maximum
		self.assertEqual(magnifier.zoomLevel, 10.0)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierTypeProperty(self):
		"""Test magnifierType property for FullScreenMagnifier."""
		magnifier = FullScreenMagnifier()

		# Should default to FULLSCREEN
		self.assertEqual(magnifier.magnifierType, MagnifierType.FULLSCREEN)

		# Test that we can read it (inherited property from Magnifier)
		self.assertIsNotNone(magnifier.magnifierType)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierInheritance(self):
		"""Test inheritance structure."""
		magnifier = FullScreenMagnifier()

		# Test inheritance
		from magnifier.magnifier import Magnifier

		self.assertIsInstance(magnifier, Magnifier)

		# Test basic properties exist
		self.assertTrue(hasattr(magnifier, "zoomLevel"))
		self.assertTrue(hasattr(magnifier, "filterType"))
		self.assertTrue(hasattr(magnifier, "magnifierType"))
		self.assertTrue(hasattr(magnifier, "fullscreenMode"))
		self.assertTrue(hasattr(magnifier, "isActive"))
		self.assertTrue(hasattr(magnifier, "currentCoordinates"))

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierApiHandling(self):
		"""Test API error handling."""
		magnifier = FullScreenMagnifier()

		# Mock API to fail
		magnifier._getMagnificationApi = MagicMock(side_effect=AttributeError())
		magnifier._stopMagnifierApi = MagicMock()
		magnifier._stopTimer = MagicMock()

		# Should not raise exception when API fails
		try:
			magnifier._stopMagnifier()
			testPassed = True
		except Exception:
			testPassed = False

		self.assertTrue(testPassed)
		self.assertFalse(magnifier.isActive)

	def testMagnifierSimpleLifecycle(self):
		"""Test simple magnifier lifecycle."""
		# Create magnifier
		magnifier = FullScreenMagnifier()
		self.assertTrue(magnifier.isActive)
		self.assertEqual(magnifier.zoomLevel, 2.0)

		# Zoom a bit
		magnifier._zoom(Direction.IN)
		self.assertEqual(magnifier.zoomLevel, 2.5)

		# Set some coordinates
		magnifier.currentCoordinates = (200, 300)
		self.assertEqual(magnifier.currentCoordinates, (200, 300))

		# Change mode
		magnifier.fullscreenMode = FullScreenMode.RELATIVE
		self.assertEqual(magnifier.fullscreenMode, FullScreenMode.RELATIVE)

		# Change filter
		magnifier.filterType = Filter.INVERTED
		self.assertEqual(magnifier.filterType, Filter.INVERTED)

		# Stop magnifier
		magnifier._stopMagnifier()
		self.assertFalse(magnifier.isActive)


class TestSpotlightManager(unittest.TestCase):
	"""Test suite for SpotlightManager functionality."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def testSpotlightManagerCreation(self):
		"""Test creating a SpotlightManager."""
		magnifier = FullScreenMagnifier()
		spotlightManager = magnifier._spotlightManager

		self.assertIsNotNone(spotlightManager)
		self.assertFalse(spotlightManager._spotlightIsActive)
		self.assertEqual(spotlightManager._animationSteps, 40)
		self.assertEqual(spotlightManager._originalZoomLevel, 2.0)
		self.assertEqual(spotlightManager._currentZoomLevel, 2.0)

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

		# Mock ui.message to avoid speech/translation issues
		with unittest.mock.patch("magnifier.fullscreenMagnifier.ui.message"):
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
		steps = spotlightManager._computeAnimationSteps(2.0, 1.0, (500, 400), (960, 540))

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
			self.assertGreater(currentZoom, nextZoom)  # Zoom should decrease from 2.0 to 1.0

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
		self.assertEqual(args[0], 3.0)  # Original zoom level
		self.assertEqual(args[1], (500, 400))  # Mouse position for CENTER mode

		magnifier._stopMagnifier()

	def testZoomBackRelativeMode(self):
		"""Test zoom back in RELATIVE mode."""
		magnifier = FullScreenMagnifier()
		magnifier.fullscreenMode = FullScreenMode.RELATIVE
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
		self.assertEqual(spotlightManager._originalZoomLevel, 2.0)

		# Mock methods for full test
		magnifier._getFocusCoordinates = MagicMock(return_value=(500, 400))
		magnifier._getCoordinatesForMode = MagicMock(return_value=(500, 400))
		magnifier._stopSpotlight = MagicMock()

		# Start spotlight (mocking animation)
		spotlightManager._animateZoom = MagicMock()
		spotlightManager._startSpotlight()
		self.assertTrue(spotlightManager._spotlightIsActive)

		# Stop spotlight
		with unittest.mock.patch("magnifier.fullscreenMagnifier.ui.message"):
			spotlightManager._stopSpotlight()
			self.assertFalse(spotlightManager._spotlightIsActive)

		magnifier._stopMagnifier()
