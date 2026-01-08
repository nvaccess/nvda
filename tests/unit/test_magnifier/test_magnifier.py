# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from _magnifier.magnifier import Magnifier, MagnifierType
from _magnifier.utils.types import Coordinates, Filter, FocusType, Direction
import unittest
from winAPI._displayTracking import getPrimaryDisplayOrientation
from unittest.mock import MagicMock, Mock, patch
import wx
import mouseHandler
import winUser


class TestMagnifier(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""

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

	def testMagnifierCreation(self):
		"""Can we create a magnifier with valid parameters?"""
		self.assertEqual(self.magnifier.zoomLevel, 2.0)
		self.assertEqual(self.magnifier._filterType, Filter.NORMAL)
		self.assertEqual(self.magnifier._magnifierType, MagnifierType.FULLSCREEN)
		self.assertFalse(self.magnifier._isActive)
		self.assertIsNone(self.magnifier._lastFocusedObject)
		self.assertEqual(self.magnifier._lastNVDAPosition, (0, 0))
		self.assertEqual(self.magnifier._lastMousePosition, (0, 0))

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
		self.magnifier._getFocusCoordinates = MagicMock(return_value=(100, 200))

		# Test starting from inactive state
		self.assertFalse(self.magnifier._isActive)
		self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)
		self.assertEqual(self.magnifier._currentCoordinates, (100, 200))
		self.magnifier._getFocusCoordinates.assert_called_once()

		# Test starting when already active (should not call _getFocusCoordinates again)
		self.magnifier._getFocusCoordinates.reset_mock()
		self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)
		self.magnifier._getFocusCoordinates.assert_not_called()

	def testUpdateMagnifier(self):
		"""Updating the magnifier's properties."""
		self.magnifier._getFocusCoordinates = MagicMock(return_value=(100, 200))
		self.magnifier._doUpdate = MagicMock()
		self.magnifier._startTimer = MagicMock()

		# Call the update function without activation
		self.magnifier._updateMagnifier()
		self.magnifier._getFocusCoordinates.assert_not_called()
		self.magnifier._doUpdate.assert_not_called()
		self.magnifier._startTimer.assert_not_called()

		# Call the update function with activation
		self.magnifier._isActive = True
		self.magnifier._updateMagnifier()

		self.magnifier._getFocusCoordinates.assert_called_once()
		self.magnifier._doUpdate.assert_called_once()
		self.magnifier._startTimer.assert_called_once_with(
			self.magnifier._updateMagnifier,
		)
		self.assertEqual(self.magnifier._currentCoordinates, (100, 200))

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

	def testGetNvdaPosition(self):
		"""Getting NVDA position with different API responses."""
		# Case 1: Review position successful
		with patch("_magnifier.magnifier.api.getReviewPosition") as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point

			x, y = self.magnifier._getCursorPosition()
			self.assertEqual((x, y), (300, 400))

		# Case 2: Review position fails, navigator works
		with patch("_magnifier.magnifier.api.getReviewPosition", return_value=None):
			with patch("_magnifier.magnifier.api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = (100, 150, 200, 300)

				x, y = self.magnifier._getCursorPosition()
				# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
				self.assertEqual((x, y), (200, 300))

		# Case 3: Everything fails
		with patch("_magnifier.magnifier.api.getReviewPosition", return_value=None):
			with patch("_magnifier.magnifier.api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = Mock(side_effect=Exception())

				x, y = self.magnifier._getCursorPosition()
				self.assertEqual((x, y), (0, 0))

	def testGetFocusCoordinates(self):
		"""All priority scenarios for focus coordinates."""

		def testValues(
			getNvda: Coordinates,
			mousePos: Coordinates,
			leftPressed: bool,
			expected_coords: Coordinates,
			expected_focused: FocusType,
		):
			self.magnifier._getCursorPosition = MagicMock(return_value=getNvda)
			self.magnifier._lastNVDAPosition = (0, 0)
			self.magnifier._lastMousePosition = (0, 0)
			mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=leftPressed)
			winUser.getCursorPos = MagicMock(return_value=mousePos)

			focusCoordinates = self.magnifier._getFocusCoordinates()

			self.assertEqual(focusCoordinates, expected_coords)
			self.assertEqual(self.magnifier._lastFocusedObject, expected_focused)

		# Case 1: Left click is pressed should return mouse position
		testValues((0, 0), (0, 0), True, (0, 0), FocusType.MOUSE)

		# Case 2: Not left click mouse moving
		testValues((0, 0), (10, 10), False, (10, 10), FocusType.MOUSE)

		# Case 3: Last move is NVDA mouse not changed
		testValues((10, 10), (0, 0), False, (10, 10), FocusType.NVDA)

		# Case 4: Nothing changed last move Mouse
		self.magnifier._lastFocusedObject = FocusType.MOUSE
		testValues((0, 0), (0, 0), False, (0, 0), FocusType.MOUSE)

		# Case 5: Nothing changed last move NVDA
		self.magnifier._lastFocusedObject = FocusType.NVDA
		testValues((0, 0), (0, 0), False, (0, 0), FocusType.NVDA)

		# Case 6: Both have moved and no Left click
		testValues((10, 10), (20, 20), False, (20, 20), FocusType.MOUSE)

		# Case 7: Both have moved and Left click
		testValues((10, 10), (20, 20), True, (20, 20), FocusType.MOUSE)

		# Case 8: Only nvda moved but left pressed (very unlikely)
		testValues((10, 10), (0, 0), True, (0, 0), FocusType.MOUSE)
