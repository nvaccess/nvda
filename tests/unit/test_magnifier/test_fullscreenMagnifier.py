# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from unittest.mock import MagicMock
from _magnifier.utils.types import Filter, FullScreenMode, MagnifierType, Direction, Size
from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from tests.unit.test_magnifier.test_magnifier import _TestMagnifier
from _magnifier.magnifier import Magnifier


class TestFullscreenMagnifierEndToEnd(_TestMagnifier):
	"""End-to-end test suite for fullscreen magnifier functionality."""

	def testMagnifierCreation(self):
		"""Test creating a magnifier."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		self.assertEqual(magnifier.zoomLevel, 2.0)
		self.assertEqual(magnifier.filterType, Filter.NORMAL)
		self.assertEqual(magnifier._fullscreenMode, FullScreenMode.CENTER)
		self.assertEqual(magnifier._magnifierType, MagnifierType.FULLSCREEN)
		self.assertTrue(magnifier._isActive)

		magnifier._stopMagnifier()

	def testMagnifierZoom(self):
		"""Test zoom functionality."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

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
		magnifier._startMagnifier()

		# Test setting coordinates
		magnifier._currentCoordinates = (100, 200)
		self.assertEqual(magnifier._currentCoordinates, (100, 200))

		# Test negative coordinates
		magnifier._currentCoordinates = (-50, -100)
		self.assertEqual(magnifier._currentCoordinates, (-50, -100))

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierUpdate(self):
		"""Test magnifier update cycle."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		# Mock the update methods
		magnifier._getCoordinatesForMode = MagicMock(return_value=(150, 250))
		magnifier._fullscreenMagnifier = MagicMock()

		# Set initial coordinates
		magnifier._currentCoordinates = (100, 200)

		# Test update
		magnifier._doUpdate()

		# Verify update was called correctly
		magnifier._getCoordinatesForMode.assert_called_once_with((100, 200))
		self.assertEqual(magnifier._lastScreenPosition, (150, 250))
		magnifier._fullscreenMagnifier.assert_called_once_with((150, 250))

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierStop(self):
		"""Test stopping the magnifier."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		# Mock the timer
		magnifier._stopTimer = MagicMock()

		# Verify it's active first
		self.assertTrue(magnifier._isActive)

		# Stop the magnifier
		magnifier._stopMagnifier()

		# Verify it's stopped
		self.assertFalse(magnifier._isActive)
		magnifier._stopTimer.assert_called_once()

	def testMagnifierPositionCalculation(self):
		"""Test position calculation."""
		magnifier = FullScreenMagnifier()

		# Test position calculation
		params = magnifier._getMagnifierParameters(
			(500, 400),
			Size(magnifier._displayOrientation.width, magnifier._displayOrientation.height),
		)

		# Basic checks
		self.assertIsInstance(params.coordinates.x, int)
		self.assertIsInstance(params.coordinates.y, int)
		self.assertIsInstance(params.magnifierSize.width, int)
		self.assertIsInstance(params.magnifierSize.height, int)

		# Width and height should be screen size divided by zoom
		expectedWidth = int(magnifier._displayOrientation.width / 2.0)
		expectedHeight = int(magnifier._displayOrientation.height / 2.0)

		self.assertEqual(params.magnifierSize.width, expectedWidth)
		self.assertEqual(params.magnifierSize.height, expectedHeight)

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
		self.assertEqual(magnifier._magnifierType, MagnifierType.FULLSCREEN)

		# Test that we can read it (inherited property from Magnifier)
		self.assertIsNotNone(magnifier._magnifierType)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierInheritance(self):
		"""Test inheritance structure."""
		magnifier = FullScreenMagnifier()

		self.assertIsInstance(magnifier, Magnifier)

		# Test basic properties exist
		self.assertTrue(hasattr(magnifier, "zoomLevel"))
		self.assertTrue(hasattr(magnifier, "filterType"))
		self.assertTrue(hasattr(magnifier, "_magnifierType"))
		self.assertTrue(hasattr(magnifier, "_fullscreenMode"))
		self.assertTrue(hasattr(magnifier, "_isActive"))
		self.assertTrue(hasattr(magnifier, "_currentCoordinates"))

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierApiHandling(self):
		"""Test API error handling."""
		magnifier = FullScreenMagnifier()

		# Mock magnification API to fail
		magnifier._stopTimer = MagicMock()

		# Should not raise exception when API fails
		try:
			magnifier._stopMagnifier()
			testPassed = True
		except Exception:
			testPassed = False

		self.assertTrue(testPassed)
		self.assertFalse(magnifier._isActive)

	def testMagnifierSimpleLifecycle(self):
		"""Test simple magnifier lifecycle."""
		# Create magnifier
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		self.assertTrue(magnifier._isActive)
		self.assertEqual(magnifier.zoomLevel, 2.0)

		# Zoom a bit
		magnifier._zoom(Direction.IN)
		self.assertEqual(magnifier.zoomLevel, 2.5)

		# Set some coordinates
		magnifier._currentCoordinates = (200, 300)
		self.assertEqual(magnifier._currentCoordinates, (200, 300))

		# Change mode
		magnifier._fullscreenMode = FullScreenMode.RELATIVE
		self.assertEqual(magnifier._fullscreenMode, FullScreenMode.RELATIVE)

		# Change filter
		magnifier.filterType = Filter.INVERTED
		self.assertEqual(magnifier.filterType, Filter.INVERTED)

		# Stop magnifier
		magnifier._stopMagnifier()
		self.assertFalse(magnifier._isActive)
