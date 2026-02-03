# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from _magnifier.magnifier import Magnifier, MagnifierType
from _magnifier.utils.types import Filter, Direction, Coordinates
import unittest
from winAPI._displayTracking import getPrimaryDisplayOrientation
from unittest.mock import MagicMock, patch
import wx


class _TestMagnifier(unittest.TestCase):
	"""Base class for magnifier tests with common setup and teardown."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test - mock magnification API to prevent actual screen magnification."""
		# Mock the Windows Magnification API to prevent affecting the user's screen
		self.mag_patcher = patch("winBindings.magnification")
		self.mock_mag = self.mag_patcher.start()

		# Configure mocked API methods to return success
		self.mock_mag.MagInitialize.return_value = True
		self.mock_mag.MagUninitialize.return_value = True
		self.mock_mag.MagSetFullscreenTransform.return_value = True
		self.mock_mag.MagSetFullscreenColorEffect.return_value = True

	def tearDown(self):
		"""Cleanup after each test."""
		self.mag_patcher.stop()


class TestMagnifier(_TestMagnifier):
	"""Tests for the Magnifier class."""

	def setUp(self):
		"""Setup before each test."""
		super().setUp()

		self.magnifier = Magnifier()
		self.screenWidth = getPrimaryDisplayOrientation().width
		self.screenHeight = getPrimaryDisplayOrientation().height

	def tearDown(self):
		"""Cleanup after each test."""
		if hasattr(self.magnifier, "_timer") and self.magnifier._timer:
			self.magnifier._timer.Stop()
			self.magnifier._timer = None

		if hasattr(self.magnifier, "_isActive") and self.magnifier._isActive:
			self.magnifier._isActive = False

		super().tearDown()

	def testMagnifierCreation(self):
		"""Can we create a magnifier with valid parameters?"""
		self.assertEqual(self.magnifier.zoomLevel, 2.0)
		self.assertEqual(self.magnifier._filterType, Filter.NORMAL)
		self.assertEqual(self.magnifier._magnifierType, MagnifierType.FULLSCREEN)
		self.assertFalse(self.magnifier._isActive)
		self.assertIsNotNone(self.magnifier._focusManager)

	def testZoomLevelProperty(self):
		"""ZoomLevel property."""
		# Test valid directions
		self.magnifier.zoomLevel = 5.0
		self.assertEqual(self.magnifier.zoomLevel, 5.0)

		self.magnifier.zoomLevel = 1.0
		self.magnifier._zoom(Direction.IN)
		self.assertEqual(self.magnifier.zoomLevel, 1.5)

		self.magnifier.zoomLevel = 10.0
		self.magnifier._zoom(Direction.OUT)
		self.assertEqual(self.magnifier.zoomLevel, 9.5)

		# Test limits
		self.magnifier.zoomLevel = 1.0
		self.magnifier._zoom(Direction.OUT)  # Should stay at min
		self.assertEqual(self.magnifier.zoomLevel, 1.0)

		self.magnifier.zoomLevel = 10.0
		self.magnifier._zoom(Direction.IN)  # Should stay at max
		self.assertEqual(self.magnifier.zoomLevel, 10.0)

	def testStartMagnifier(self):
		"""Activating the magnifier."""
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=Coordinates(100, 200),
		)

		# Test starting from inactive state
		self.assertFalse(self.magnifier._isActive)
		self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)
		self.assertEqual(self.magnifier._currentCoordinates, Coordinates(100, 200))
		self.magnifier._focusManager.getCurrentFocusCoordinates.assert_called_once()

		# Test starting when already active (should not call getCurrentFocusCoordinates again)
		self.magnifier._focusManager.getCurrentFocusCoordinates.reset_mock()
		self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)
		self.magnifier._focusManager.getCurrentFocusCoordinates.assert_not_called()

	def testUpdateMagnifier(self):
		"""Updating the magnifier's properties."""
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=Coordinates(100, 200),
		)
		self.magnifier._doUpdate = MagicMock()
		self.magnifier._startTimer = MagicMock()

		# Call the update function without activation
		self.magnifier._updateMagnifier()
		self.magnifier._focusManager.getCurrentFocusCoordinates.assert_not_called()
		self.magnifier._doUpdate.assert_not_called()
		self.magnifier._startTimer.assert_not_called()

		# Call the update function with activation
		self.magnifier._isActive = True
		self.magnifier._updateMagnifier()

		self.magnifier._focusManager.getCurrentFocusCoordinates.assert_called_once()
		self.magnifier._doUpdate.assert_called_once()
		self.magnifier._startTimer.assert_called_once_with(
			self.magnifier._updateMagnifier,
		)
		self.assertEqual(self.magnifier._currentCoordinates, Coordinates(100, 200))

	def testDoUpdate(self):
		"""DoUpdate function raises NotImplementedError."""
		with self.assertRaises(NotImplementedError):
			self.magnifier._doUpdate()

	def testStopMagnifier(self):
		"""Stopping the magnifier."""
		self.magnifier._stopTimer = MagicMock()

		# Call the stop function without activation
		self.magnifier._stopMagnifier()
		self.magnifier._stopTimer.assert_not_called()

		# Call the stop function with activation
		self.magnifier._isActive = True
		self.magnifier._stopMagnifier()

		self.magnifier._stopTimer.assert_called_once()
		self.assertFalse(self.magnifier._isActive)

	def testZoom(self):
		"""zoom in and out with valid values and check boundaries."""
		# Set initial zoom to 1.0 for predictable testing
		self.magnifier.zoomLevel = 1.0

		# Test zoom in
		self.magnifier._zoom(Direction.IN)
		self.assertEqual(self.magnifier.zoomLevel, 1.5)

		# Test zoom out
		self.magnifier._zoom(Direction.OUT)
		self.assertEqual(self.magnifier.zoomLevel, 1.0)

		# Test zoom in at maximum boundary
		self.magnifier.zoomLevel = 10.0
		self.magnifier._zoom(Direction.IN)
		self.assertEqual(self.magnifier.zoomLevel, 10.0)  # Should remain at max

		# Test zoom out at minimum boundary
		self.magnifier.zoomLevel = 1.0
		self.magnifier._zoom(Direction.OUT)
		self.assertEqual(self.magnifier.zoomLevel, 1.0)  # Should remain at min

	def testPanLeft(self):
		"""Pan left and detect edge limit."""
		from _magnifier.utils.types import MagnifierAction

		# Mock dependencies
		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			# Setup initial position at center
			self.magnifier._isActive = True
			self.magnifier._panStep = 10  # 10% of screen width
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Calculate expected pan pixels: (screenWidth / zoomLevel) * panStep / 100
			expectedPanPixels = int(
				(self.screenWidth / self.magnifier.zoomLevel) * 10 / 100,
			)

			# Test normal pan
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_LEFT)
			self.assertFalse(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.x,
				centerX - expectedPanPixels,
			)

			# Test reaching left edge
			self.magnifier._currentCoordinates = Coordinates(
				self.magnifier._panMargin.left,
				centerY,
			)
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_LEFT)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.x,
				self.magnifier._panMargin.left,
			)

	def testPanRight(self):
		"""Pan right and detect edge limit."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier._panStep = 10  # 10% of screen width
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Calculate expected pan pixels
			expectedPanPixels = int(
				(self.screenWidth / self.magnifier.zoomLevel) * 10 / 100,
			)

			# Test normal pan
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_RIGHT)
			self.assertFalse(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.x,
				centerX + expectedPanPixels,
			)

			# Test reaching right edge
			self.magnifier._currentCoordinates = Coordinates(
				self.magnifier._panMargin.right,
				centerY,
			)
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_RIGHT)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.x,
				self.magnifier._panMargin.right,
			)

	def testPanUp(self):
		"""Pan up and detect edge limit."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier._panStep = 10  # 10% of screen width
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Calculate expected pan pixels (based on width for consistency)
			expectedPanPixels = int(
				(self.screenWidth / self.magnifier.zoomLevel) * 10 / 100,
			)

			# Test normal pan
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_UP)
			self.assertFalse(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.y,
				centerY - expectedPanPixels,
			)

			# Test reaching top edge
			self.magnifier._currentCoordinates = Coordinates(
				centerX,
				self.magnifier._panMargin.top,
			)
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_UP)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.y,
				self.magnifier._panMargin.top,
			)

	def testPanDown(self):
		"""Pan down and detect edge limit."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier._panStep = 10  # 10% of screen width
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Calculate expected pan pixels (based on width for consistency)
			expectedPanPixels = int(
				(self.screenWidth / self.magnifier.zoomLevel) * 10 / 100,
			)

			# Test normal pan
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_DOWN)
			self.assertFalse(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.y,
				centerY + expectedPanPixels,
			)

			# Test reaching bottom edge
			self.magnifier._currentCoordinates = Coordinates(
				centerX,
				self.magnifier._panMargin.bottom,
			)
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_DOWN)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.y,
				self.magnifier._panMargin.bottom,
			)

	def testPanToLeftEdge(self):
		"""Pan directly to left edge."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Test jump to left edge
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_LEFT_EDGE)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.x,
				self.magnifier._panMargin.left,
			)

	def testPanToRightEdge(self):
		"""Pan directly to right edge."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Test jump to right edge
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_RIGHT_EDGE)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.x,
				self.magnifier._panMargin.right,
			)

	def testPanToTopEdge(self):
		"""Pan directly to top edge."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Test jump to top edge
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_TOP_EDGE)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.y,
				self.magnifier._panMargin.top,
			)

	def testPanToBottomEdge(self):
		"""Pan directly to bottom edge."""
		from _magnifier.utils.types import MagnifierAction

		self.magnifier._doUpdate = MagicMock()
		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			self.magnifier._isActive = True
			self.magnifier.setPanMarginBorder()
			centerX = self.screenWidth // 2
			centerY = self.screenHeight // 2
			self.magnifier._currentCoordinates = Coordinates(centerX, centerY)

			# Test jump to bottom edge
			reachedEdge = self.magnifier._pan(MagnifierAction.PAN_BOTTOM_EDGE)
			self.assertTrue(reachedEdge)
			self.assertEqual(
				self.magnifier._currentCoordinates.y,
				self.magnifier._panMargin.bottom,
			)

	def testStartTimer(self):
		"""Starting the timer."""
		self.magnifier._stopTimer = MagicMock()
		callback = MagicMock()

		self.magnifier._startTimer(callback)

		self.magnifier._stopTimer.assert_called_once()
		self.assertIsInstance(self.magnifier._timer, wx.Timer)
		self.assertTrue(self.magnifier._timer.IsRunning())

		# Clean up the timer
		self.magnifier._timer.Stop()
		self.magnifier._timer = None

	def testStopTimer(self):
		"""Stopping the timer."""
		# Test stopping when timer exists
		self.magnifier._startTimer(lambda: None)
		self.assertIsNotNone(self.magnifier._timer)

		self.magnifier._stopTimer()
		self.assertIsNone(self.magnifier._timer)

		# Test stopping when no timer exists (should not raise error)
		self.magnifier._stopTimer()
		self.assertIsNone(self.magnifier._timer)

	def testMagnifierPosition(self):
		"""Computing magnifier position and size."""
		x, y = int(self.screenWidth / 2), int(self.screenHeight / 2)
		left, top, width, height = self.magnifier._getMagnifierPosition((x, y))

		expected_width = int(self.screenWidth / self.magnifier.zoomLevel)
		expected_height = int(self.screenHeight / self.magnifier.zoomLevel)
		expected_left = int(x - (expected_width / 2))
		expected_top = int(y - (expected_height / 2))

		self.assertEqual(left, expected_left)
		self.assertEqual(top, expected_top)
		self.assertEqual(width, expected_width)
		self.assertEqual(height, expected_height)

		# Test left clamping
		left, top, width, height = self.magnifier._getMagnifierPosition((100, 540))
		self.assertGreaterEqual(left, 0)

		# Test right clamping
		left, top, width, height = self.magnifier._getMagnifierPosition((1800, 540))
		self.assertLessEqual(left + width, self.screenWidth)

		# Test different zoom level
		self.magnifier.zoomLevel = 4.0
		left, top, width, height = self.magnifier._getMagnifierPosition((960, 540))
		expected_width = int(self.screenWidth / self.magnifier.zoomLevel)
		expected_height = int(self.screenHeight / self.magnifier.zoomLevel)
		self.assertEqual(width, expected_width)
		self.assertEqual(height, expected_height)
