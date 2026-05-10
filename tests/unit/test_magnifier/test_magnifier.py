# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from _magnifier.magnifier import Magnifier
from _magnifier.utils.types import Filter, Direction, Coordinates, MagnifierAction
from comtypes import COMError
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
		self.mag_patcher = patch("winBindings.magnification")
		self.mock_mag = self.mag_patcher.start()
		self.mag_fs_patcher = patch("_magnifier.fullscreenMagnifier.magnification")
		self.mock_mag_fs = self.mag_fs_patcher.start()
		for mock in (self.mock_mag, self.mock_mag_fs):
			mock.MagInitialize.return_value = True
			mock.MagUninitialize.return_value = True
			mock.MagSetFullscreenTransform.return_value = True
			mock.MagSetFullscreenColorEffect.return_value = True

	def tearDown(self):
		"""Cleanup after each test."""
		self.mag_fs_patcher.stop()
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
		self.assertFalse(self.magnifier._isActive)
		self.assertIsNotNone(self.magnifier._focusManager)
		self.assertEqual(self.magnifier._consecutiveErrors, 0)

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
		# Use center coordinates which will always be within bounds
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
		)

		# Test starting from inactive state
		self.assertFalse(self.magnifier._isActive)
		self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)
		self.assertEqual(self.magnifier.currentCoordinates, focusCoords)
		self.magnifier._focusManager.getCurrentFocusCoordinates.assert_called_once()

		# Test starting when already active (should not call getCurrentFocusCoordinates again)
		self.magnifier._focusManager.getCurrentFocusCoordinates.reset_mock()
		self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)
		self.magnifier._focusManager.getCurrentFocusCoordinates.assert_not_called()

	def testUpdateMagnifier(self):
		"""Updating the magnifier's properties."""
		# Use center coordinates which will always be within bounds
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
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

		# getCurrentFocusCoordinates is called twice: once in _managePanning and once to update currentCoordinates
		self.assertEqual(
			self.magnifier._focusManager.getCurrentFocusCoordinates.call_count,
			2,
		)
		self.magnifier._doUpdate.assert_called_once()
		self.magnifier._startTimer.assert_called_once_with(
			self.magnifier._updateMagnifier,
		)
		self.assertEqual(self.magnifier.currentCoordinates, focusCoords)
		# Successful update should reset error counter
		self.assertEqual(self.magnifier._consecutiveErrors, 0)

	def testUpdateMagnifierResumesAfterSingleError(self):
		"""Timer must always be rescheduled even when _doUpdate raises an exception."""
		self.magnifier._isActive = True
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
		)
		self.magnifier._doUpdate = MagicMock(side_effect=OSError("COM failure"))
		self.magnifier._startTimer = MagicMock()

		self.magnifier._updateMagnifier()

		# Timer must still be rescheduled despite the error
		self.magnifier._startTimer.assert_called_once_with(
			self.magnifier._updateMagnifier,
		)
		self.assertEqual(self.magnifier._consecutiveErrors, 1)

	def testUpdateMagnifierTriggersRecoveryAfterMaxErrors(self):
		"""After _MAX_CONSECUTIVE_ERRORS failures, _attemptRecovery is called instead of restarting timer."""
		self.magnifier._isActive = True
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
		)
		self.magnifier._doUpdate = MagicMock(side_effect=OSError("COM failure"))
		self.magnifier._startTimer = MagicMock()
		self.magnifier._attemptRecovery = MagicMock()

		# Simulate reaching max errors
		self.magnifier._consecutiveErrors = Magnifier._MAX_CONSECUTIVE_ERRORS - 1
		self.magnifier._updateMagnifier()

		# Recovery should be called, timer should NOT be rescheduled directly
		self.magnifier._attemptRecovery.assert_called_once()
		self.magnifier._startTimer.assert_not_called()

	def testUpdateMagnifierCatchesCOMError(self):
		"""COMError from UIA must be caught and the timer rescheduled."""
		self.magnifier._isActive = True
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
		)
		self.magnifier._doUpdate = MagicMock(side_effect=COMError(-2147417848, "RPC_E_DISCONNECTED", None))
		self.magnifier._startTimer = MagicMock()

		self.magnifier._updateMagnifier()

		self.magnifier._startTimer.assert_called_once_with(self.magnifier._updateMagnifier)
		self.assertEqual(self.magnifier._consecutiveErrors, 1)

	def testUpdateMagnifierRecoveryFailureSafelyRestartsTimer(self):
		"""If _attemptRecovery itself raises, the timer must still be restarted to prevent a freeze."""
		self.magnifier._isActive = True
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
		)
		self.magnifier._doUpdate = MagicMock(side_effect=OSError("API failure"))
		self.magnifier._startTimer = MagicMock()
		self.magnifier._attemptRecovery = MagicMock(side_effect=RuntimeError("recovery crashed"))

		self.magnifier._consecutiveErrors = Magnifier._MAX_CONSECUTIVE_ERRORS - 1
		self.magnifier._updateMagnifier()

		# Timer must be restarted by the safety net even though recovery failed
		self.magnifier._startTimer.assert_called_once_with(self.magnifier._updateMagnifier)
		self.assertEqual(self.magnifier._consecutiveErrors, 0)

	def testUpdateMagnifierResetsErrorCountOnSuccess(self):
		"""A successful update after errors resets the consecutive error counter."""
		self.magnifier._isActive = True
		self.magnifier._consecutiveErrors = 2
		focusCoords = Coordinates(self.screenWidth // 2, self.screenHeight // 2)
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=focusCoords,
		)
		self.magnifier._doUpdate = MagicMock()  # Success
		self.magnifier._startTimer = MagicMock()

		self.magnifier._updateMagnifier()

		self.assertEqual(self.magnifier._consecutiveErrors, 0)
		self.magnifier._startTimer.assert_called_once()

	def testAttemptRecoveryBase(self):
		"""Base _attemptRecovery resets errors and restarts timer."""
		self.magnifier._consecutiveErrors = 3
		self.magnifier._startTimer = MagicMock()

		self.magnifier._attemptRecovery()

		self.assertEqual(self.magnifier._consecutiveErrors, 0)
		self.magnifier._startTimer.assert_called_once_with(
			self.magnifier._updateMagnifier,
		)

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

	def _setupPanTest(self):
		"""Common setup for pan tests."""
		self.magnifier._doUpdate = MagicMock()
		self.magnifier._isActive = True
		self.magnifier._panStep = 10  # 10% of screen width
		centerX = self.screenWidth // 2
		centerY = self.screenHeight // 2
		self.magnifier.currentCoordinates = Coordinates(centerX, centerY)
		expectedPanPixels = int(
			(self.screenWidth / self.magnifier.zoomLevel) * 10 / 100,
		)
		return centerX, centerY, expectedPanPixels

	def _testSimplePan(
		self,
		action: MagnifierAction,
		axis: str,
		direction: int,
		edgeAttr: str,
	):
		"""
		Test simple pan action (LEFT, RIGHT, UP, DOWN).

		:param action: The pan action to test
		:param axis: 'x' or 'y'
		:param direction: -1 for left/up, +1 for right/down
		:param edgeAttr: The screen limit attribute name ('left', 'right', 'top', 'bottom')
		"""
		centerX, centerY, expectedPanPixels = self._setupPanTest()
		minX, minY, maxX, maxY = self.magnifier._getScreenLimits()
		edgeMap = {"left": minX, "right": maxX, "top": minY, "bottom": maxY}
		edgeValue = edgeMap[edgeAttr]
		centerValue = centerX if axis == "x" else centerY

		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			# Test normal pan - movement succeeds (position changes)
			hasMoved = self.magnifier._pan(action)
			self.assertTrue(hasMoved)
			currentValue = getattr(self.magnifier.currentCoordinates, axis)
			self.assertEqual(currentValue, centerValue + direction * expectedPanPixels)

			# Test reaching edge - movement succeeds on first contact (position changes to edge)
			if axis == "x":
				self.magnifier.currentCoordinates = Coordinates(
					edgeValue - direction * expectedPanPixels,
					centerY,
				)
			else:
				self.magnifier.currentCoordinates = Coordinates(
					centerX,
					edgeValue - direction * expectedPanPixels,
				)

			hasMoved = self.magnifier._pan(action)
			self.assertTrue(hasMoved)
			currentValue = getattr(self.magnifier.currentCoordinates, axis)
			self.assertEqual(currentValue, edgeValue)

			# Test trying to pan beyond edge - movement fails (already at edge, no movement)
			hasMoved = self.magnifier._pan(action)
			self.assertFalse(hasMoved)
			currentValue = getattr(self.magnifier.currentCoordinates, axis)
			self.assertEqual(currentValue, edgeValue)

	def _testPanToEdge(self, action: MagnifierAction, axis: str, edgeAttr: str):
		"""
		Test pan to edge action (PAN_X_EDGE).

		:param action: The pan to edge action to test
		:param axis: 'x' or 'y'
		:param edgeAttr: The screen limit attribute name ('left', 'right', 'top', 'bottom')
		"""
		_ = self._setupPanTest()
		minX, minY, maxX, maxY = self.magnifier._getScreenLimits()
		edgeMap = {"left": minX, "right": maxX, "top": minY, "bottom": maxY}
		edgeValue = edgeMap[edgeAttr]

		with patch("_magnifier.magnifier.winUser.setCursorPos"):
			# Test jump to edge - movement succeeds (moves to edge)
			hasMoved = self.magnifier._pan(action)
			self.assertTrue(hasMoved)
			currentValue = getattr(self.magnifier.currentCoordinates, axis)
			self.assertEqual(currentValue, edgeValue)

			# Test trying to pan to edge again - movement fails (already at edge, no movement)
			hasMoved = self.magnifier._pan(action)
			self.assertFalse(hasMoved)
			currentValue = getattr(self.magnifier.currentCoordinates, axis)
			self.assertEqual(currentValue, edgeValue)

	def testPanLeft(self):
		"""Pan left and detect edge limit."""
		self._testSimplePan(
			MagnifierAction.PAN_LEFT,
			axis="x",
			direction=-1,
			edgeAttr="left",
		)

	def testPanRight(self):
		"""Pan right and detect edge limit."""
		self._testSimplePan(
			MagnifierAction.PAN_RIGHT,
			axis="x",
			direction=1,
			edgeAttr="right",
		)

	def testPanUp(self):
		"""Pan up and detect edge limit."""
		self._testSimplePan(
			MagnifierAction.PAN_UP,
			axis="y",
			direction=-1,
			edgeAttr="top",
		)

	def testPanDown(self):
		"""Pan down and detect edge limit."""
		self._testSimplePan(
			MagnifierAction.PAN_DOWN,
			axis="y",
			direction=1,
			edgeAttr="bottom",
		)

	def testPanToLeftEdge(self):
		"""Pan directly to left edge."""
		self._testPanToEdge(
			MagnifierAction.PAN_LEFT_EDGE,
			axis="x",
			edgeAttr="left",
		)

	def testPanToRightEdge(self):
		"""Pan directly to right edge."""
		self._testPanToEdge(
			MagnifierAction.PAN_RIGHT_EDGE,
			axis="x",
			edgeAttr="right",
		)

	def testPanToTopEdge(self):
		"""Pan directly to top edge."""
		self._testPanToEdge(
			MagnifierAction.PAN_TOP_EDGE,
			axis="y",
			edgeAttr="top",
		)

	def testPanToBottomEdge(self):
		"""Pan directly to bottom edge."""
		self._testPanToEdge(
			MagnifierAction.PAN_BOTTOM_EDGE,
			axis="y",
			edgeAttr="bottom",
		)

	def testManagePanning(self):
		"""Manual panning ends when focus coordinates change, and _lastFocusCoordinates is always kept up to date."""
		focusA = Coordinates(100, 200)
		focusB = Coordinates(300, 400)

		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(return_value=focusA)

		# When not panning, _lastFocusCoordinates is updated every cycle
		self.magnifier._isManualPanning = False
		self.magnifier._managePanning()
		self.assertFalse(self.magnifier._isManualPanning)
		self.assertEqual(self.magnifier._lastFocusCoordinates, focusA)

		# When panning starts and focus hasn't changed, panning continues
		self.magnifier._isManualPanning = True
		self.magnifier._managePanning()
		self.assertTrue(self.magnifier._isManualPanning)
		self.assertEqual(self.magnifier._lastFocusCoordinates, focusA)

		# When focus changes while panning, manual panning ends
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(return_value=focusB)
		self.magnifier._managePanning()
		self.assertFalse(self.magnifier._isManualPanning)
		self.assertEqual(self.magnifier._lastFocusCoordinates, focusB)

	def testKeepMouseCentered(self):
		"""Base _keepMouseCentered moves cursor to currentCoordinates."""
		self.magnifier.currentCoordinates = Coordinates(640, 360)
		with patch("_magnifier.magnifier.winUser.setCursorPos") as mockSetCursor:
			self.magnifier._keepMouseCentered()
			mockSetCursor.assert_called_once_with(640, 360)

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

	def testClampCoordinates(self):
		"""Test all boundary clamps (left, right, top, bottom) for both modes."""
		for isTrueCentered in (False, True):
			self.magnifier.zoomLevel = 2.0
			with patch("_magnifier.magnifier.isTrueCentered", return_value=isTrueCentered):
				minX, minY, maxX, maxY = self.magnifier._getScreenLimits()

				# Test left boundary (far below minimum)
				self.magnifier.currentCoordinates = Coordinates(-1000, 100)
				self.assertGreaterEqual(self.magnifier.currentCoordinates.x, minX)
				self.assertLessEqual(self.magnifier.currentCoordinates.x, maxX)

				# Test right boundary (far above maximum)
				self.magnifier.currentCoordinates = Coordinates(100000, 100)
				self.assertGreaterEqual(self.magnifier.currentCoordinates.x, minX)
				self.assertLessEqual(self.magnifier.currentCoordinates.x, maxX)

				# Test top boundary (far above minimum)
				self.magnifier.currentCoordinates = Coordinates(100, -1000)
				self.assertGreaterEqual(self.magnifier.currentCoordinates.y, minY)
				self.assertLessEqual(self.magnifier.currentCoordinates.y, maxY)

				# Test bottom boundary (far above maximum)
				self.magnifier.currentCoordinates = Coordinates(100, 100000)
				self.assertGreaterEqual(self.magnifier.currentCoordinates.y, minY)
				self.assertLessEqual(self.magnifier.currentCoordinates.y, maxY)

	def testClampCoordinatesWithinBounds(self):
		"""Coordinates within bounds are not modified."""
		self.magnifier.zoomLevel = 2.0
		with patch("_magnifier.magnifier.isTrueCentered", return_value=False):
			minX, minY, maxX, maxY = self.magnifier._getScreenLimits()
			centerX = (minX + maxX) // 2
			centerY = (minY + maxY) // 2

			validCoords = Coordinates(centerX, centerY)
			self.magnifier.currentCoordinates = validCoords
			self.assertEqual(self.magnifier.currentCoordinates, validCoords)
