# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from unittest.mock import MagicMock, patch
from _magnifier.config import ZoomLevel
from _magnifier.magnifier import Magnifier
from _magnifier.utils.types import (
	Filter,
	FullScreenMode,
	MagnifiedView,
	Direction,
	Coordinates,
	MagnifierFollowFocusType,
)
from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from tests.unit.test_magnifier.test_magnifier import _TestMagnifier
from winAPI._displayTracking import getPrimaryDisplayOrientation


class TestFullscreenMagnifierEndToEnd(_TestMagnifier):
	"""End-to-end test suite for fullscreen magnifier functionality."""

	def testMagnifierCreation(self):
		"""Test creating a magnifier."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		self.assertEqual(magnifier.zoomLevel, 200)
		self.assertEqual(magnifier.filterType, Filter.NORMAL)
		self.assertEqual(magnifier._fullscreenMode, FullScreenMode.CENTER)
		self.assertEqual(magnifier._MAGNIFIED_VIEW, MagnifiedView.FULLSCREEN)
		self.assertTrue(magnifier._isActive)

		magnifier._stopMagnifier()

	def testMagnifierZoom(self):
		"""Test zoom functionality."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		# Set initial zoom to 100 for predictable testing
		magnifier.zoomLevel = 100

		# Test zoom in
		magnifier._zoom(Direction.IN)
		self.assertEqual(magnifier.zoomLevel, 150)

		# Test zoom out
		magnifier._zoom(Direction.OUT)
		self.assertEqual(magnifier.zoomLevel, 100)
		self.assertEqual(magnifier.zoomLevel, 100)

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
		# Bypass animation so this test only covers _doUpdate plumbing
		magnifier._advanceAnimation = MagicMock(side_effect=lambda coords, **_: coords)

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
		magnifier._startMagnifier()

		# Test position calculation
		params = magnifier._getMagnifierParameters((500, 400))

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
		magnifier._startMagnifier()
		magnifier.zoomLevel = ZoomLevel.MIN_ZOOM

		# Test minimum boundary
		magnifier._zoom(Direction.OUT)  # Try to zoom out below minimum
		self.assertEqual(magnifier.zoomLevel, ZoomLevel.MIN_ZOOM)

		# Test maximum boundary
		magnifier.zoomLevel = ZoomLevel.MAX_ZOOM
		magnifier._zoom(Direction.IN)  # Try to zoom in above maximum
		self.assertEqual(magnifier.zoomLevel, ZoomLevel.MAX_ZOOM)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifiedViewProperty(self):
		"""Test magnifiedView property for FullScreenMagnifier."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		# Should default to FULLSCREEN
		self.assertEqual(magnifier._MAGNIFIED_VIEW, MagnifiedView.FULLSCREEN)

		# Test that we can read it (inherited property from Magnifier)
		self.assertIsNotNone(magnifier._MAGNIFIED_VIEW)

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierInheritance(self):
		"""Test inheritance structure."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		self.assertIsInstance(magnifier, Magnifier)

		# Test basic properties exist
		self.assertTrue(hasattr(magnifier, "zoomLevel"))
		self.assertTrue(hasattr(magnifier, "filterType"))
		self.assertTrue(hasattr(magnifier, "_MAGNIFIED_VIEW"))
		self.assertTrue(hasattr(magnifier, "_fullscreenMode"))
		self.assertTrue(hasattr(magnifier, "_isActive"))
		self.assertTrue(hasattr(magnifier, "_currentCoordinates"))

		# Cleanup
		magnifier._stopMagnifier()

	def testMagnifierApiHandling(self):
		"""Test API error handling."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

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
		self.assertEqual(magnifier.zoomLevel, 200)

		# Zoom a bit
		magnifier._zoom(Direction.IN)
		self.assertEqual(magnifier.zoomLevel, 250)

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

	def testAttemptRecoverySuccess(self):
		"""FullScreenMagnifier._attemptRecovery reinitialises API and restarts timer on success."""
		with patch(
			"_magnifier.magnifier.FocusManager.getCurrentFocusCoordinates",
			return_value=Coordinates(0, 0),
		):
			magnifier = FullScreenMagnifier()
		magnifier._consecutiveErrors = 3
		magnifier._startTimer = MagicMock()

		with patch("_magnifier.fullscreenMagnifier.magnification") as mock_mag:
			magnifier._attemptRecovery()

			mock_mag.MagUninitialize.assert_called_once()
			mock_mag.MagInitialize.assert_called_once()
			mock_mag.MagSetFullscreenTransform.assert_called_once_with(magnifier.zoomLevel / 100.0, 0, 0)
			mock_mag.MagSetFullscreenColorEffect.assert_called_once()
			self.assertEqual(magnifier._consecutiveErrors, 0)
			magnifier._startTimer.assert_called_once_with(magnifier._updateMagnifier)

		magnifier._stopMagnifier()

	def testAttemptRecoveryFailureStopsMagnifier(self):
		"""When recovery fails, magnifier is stopped and user is notified."""
		magnifier = FullScreenMagnifier()
		magnifier._consecutiveErrors = 3
		magnifier._stopMagnifier = MagicMock()

		with patch("_magnifier.fullscreenMagnifier.magnification") as mock_mag:
			mock_mag.MagInitialize.side_effect = OSError("Init failed")
			with patch("_magnifier.fullscreenMagnifier.ui.message"):
				magnifier._attemptRecovery()

		magnifier._stopMagnifier.assert_called_once()
		self.assertEqual(magnifier._consecutiveErrors, 0)

	def testUpdateLoopSurvivesSingleDoUpdateError(self):
		"""A single _doUpdate error does not kill the update loop."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._startTimer = MagicMock()
		magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			return_value=(100, 200),
		)

		# First call fails, second succeeds
		magnifier._doUpdate = MagicMock(side_effect=[OSError("Transient"), None])

		# First update — error
		magnifier._updateMagnifier()
		self.assertEqual(magnifier._consecutiveErrors, 1)
		magnifier._startTimer.assert_called_with(magnifier._updateMagnifier)

		# Second update — success
		magnifier._startTimer.reset_mock()
		magnifier._updateMagnifier()
		self.assertEqual(magnifier._consecutiveErrors, 0)
		magnifier._startTimer.assert_called_with(magnifier._updateMagnifier)

		magnifier._stopMagnifier()


class TestFullScreenMagnifierPositionAnimation(_TestMagnifier):
	"""Tests for smooth position animation in FullScreenMagnifier._doUpdate."""

	def setUp(self):
		super().setUp()
		self.magnifier = FullScreenMagnifier()
		self.magnifier._startMagnifier()
		self.magnifier._fullscreenMagnifier = MagicMock()
		# Isolate from real system state: real mouse position at setUp time can set
		# _lastFocusedObject = MOUSE, which would force animate=False in all tests.
		self.magnifier._focusManager.getLastFocusType = MagicMock(return_value=None)

	def tearDown(self):
		self.magnifier._stopMagnifier()
		super().tearDown()

	def testAnimatorInitialisedOnStart(self):
		"""Position animator must be ready after _startMagnifier."""
		self.assertIsNotNone(self.magnifier._positionAnimator)

	def testDoUpdateAnimatesPositionOverMultipleSteps(self):
		"""For a distance larger than one speed unit, _doUpdate must interpolate on the first tick."""
		start = Coordinates(0, 0)
		# 10× speed_px_per_tick guarantees > 1 step
		dist = int(Magnifier._ANIMATION_SPEED_PX_PER_TICK * 10)
		target = Coordinates(dist, 0)
		self.magnifier._initPositionAnimator(start)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=target)

		self.magnifier._doUpdate()
		firstPos = self.magnifier._lastScreenPosition

		self.assertGreater(firstPos.x, start.x)
		self.assertLess(firstPos.x, target.x)

	def testDoUpdateReachesTargetWhenComplete(self):
		"""Once the animation completes, _doUpdate must render exactly the target."""
		start = Coordinates(0, 0)
		target = Coordinates(100, 0)
		self.magnifier._initPositionAnimator(start)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=target)

		for _ in range(60):  # generous upper bound
			self.magnifier._doUpdate()
			if self.magnifier._positionAnimator.isComplete:
				break

		self.assertEqual(self.magnifier._lastScreenPosition, target)

	def testDoUpdateSpeedIsConstantOverDistance(self):
		"""The number of animation steps must scale linearly with distance."""
		speed = Magnifier._ANIMATION_SPEED_PX_PER_TICK

		self.magnifier._initPositionAnimator(Coordinates(0, 0))
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=Coordinates(int(speed * 5), 0))
		self.magnifier._doUpdate()
		short_steps = self.magnifier._positionAnimator._totalSteps

		self.magnifier._initPositionAnimator(Coordinates(0, 0))
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=Coordinates(int(speed * 10), 0))
		self.magnifier._doUpdate()
		long_steps = self.magnifier._positionAnimator._totalSteps

		self.assertEqual(long_steps, short_steps * 2)

	def testDoUpdateRedirectsOnNewTarget(self):
		"""A new target mid-animation must redirect smoothly and end at the new target."""
		start = Coordinates(0, 0)
		first_target = Coordinates(int(Magnifier._ANIMATION_SPEED_PX_PER_TICK * 10), 0)
		self.magnifier._initPositionAnimator(start)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=first_target)

		for _ in range(3):
			self.magnifier._doUpdate()
		mid = self.magnifier._lastScreenPosition
		self.assertGreater(mid.x, start.x)

		new_target = Coordinates(0, int(Magnifier._ANIMATION_SPEED_PX_PER_TICK * 10))
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=new_target)

		for _ in range(60):
			self.magnifier._doUpdate()
			if self.magnifier._positionAnimator.isComplete:
				break

		self.assertEqual(self.magnifier._lastScreenPosition, new_target)

	def testDoUpdateNoAnimationBeforeInit(self):
		"""Without a position animator, _doUpdate applies target coordinates immediately."""
		self.magnifier._positionAnimator = None
		target = Coordinates(300, 200)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=target)

		self.magnifier._doUpdate()

		self.assertEqual(self.magnifier._lastScreenPosition, target)

	def testDoUpdateNoAnimationForMouseTracking(self):
		"""When tracking the mouse, _doUpdate must snap to target without interpolation."""
		dist = int(Magnifier._ANIMATION_SPEED_PX_PER_TICK * 10)
		self.magnifier._initPositionAnimator(Coordinates(0, 0))
		self.magnifier._focusManager.getLastFocusType = MagicMock(
			return_value=MagnifierFollowFocusType.MOUSE,
		)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=Coordinates(dist, 0))

		self.magnifier._doUpdate()

		self.assertEqual(self.magnifier._lastScreenPosition, Coordinates(dist, 0))

	def testTransitionFromMouseToKeyboardAnimatesFromMousePosition(self):
		"""After mouse tracking ends, animation must depart from the last mouse position."""
		mousePos = Coordinates(200, 0)
		keyboardPos = Coordinates(0, 0)

		self.magnifier._initPositionAnimator(Coordinates(0, 0))

		# Snap to mouse position
		self.magnifier._focusManager.getLastFocusType = MagicMock(
			return_value=MagnifierFollowFocusType.MOUSE,
		)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=mousePos)
		self.magnifier._doUpdate()
		self.assertEqual(self.magnifier._lastScreenPosition, mousePos)

		# Switch to keyboard focus — first animated step must depart from mousePos
		self.magnifier._focusManager.getLastFocusType = MagicMock(return_value=None)
		self.magnifier._getCoordinatesForMode = MagicMock(return_value=keyboardPos)
		self.magnifier._doUpdate()

		firstPos = self.magnifier._lastScreenPosition
		self.assertGreater(firstPos.x, keyboardPos.x)
		self.assertLess(firstPos.x, mousePos.x)


class TestFullScreenMagnifierApiConflict(_TestMagnifier):
	"""Tests for Windows Magnification API conflict detection at startup and during recovery."""

	def testCannotStartWhenWindowsMagnifierRunning(self):
		"""
		MagInitialize succeeds but MagSetFullscreenTransform fails: Windows Magnifier is running.
		NVDA Magnifier must not start, the user must be notified, and no timer must be started.
		"""
		self.mock_mag_fs.MagSetFullscreenTransform.side_effect = OSError("API in use by another magnifier")

		with patch("_magnifier.fullscreenMagnifier.ui.message") as mock_message:
			magnifier = FullScreenMagnifier()
			magnifier._startMagnifier()

		self.assertFalse(magnifier._isActive)
		mock_message.assert_called_once()
		self.assertIsNone(magnifier._timer)

	def testCannotStartWhenMagInitializeFails(self):
		"""
		MagInitialize itself fails: NVDA Magnifier must not start and the user must be notified.
		"""
		self.mock_mag_fs.MagInitialize.side_effect = OSError("Cannot initialize magnification API")

		with patch("_magnifier.fullscreenMagnifier.ui.message") as mock_message:
			magnifier = FullScreenMagnifier()
			magnifier._startMagnifier()

		self.assertFalse(magnifier._isActive)
		mock_message.assert_called_once()
		self.assertIsNone(magnifier._timer)

	def testRecoveryCapStopsMagnifier(self):
		"""
		After _MAX_RECOVERY_ATTEMPTS failed attempts, the magnifier stops and the user is notified.
		"""
		magnifier = FullScreenMagnifier()
		magnifier._recoveryAttempts = FullScreenMagnifier._MAX_RECOVERY_ATTEMPTS

		with patch("_magnifier.fullscreenMagnifier.ui.message") as mock_message:
			magnifier._attemptRecovery()

		self.assertFalse(magnifier._isActive)
		mock_message.assert_called_once()

	def testRecoveryFailsWhenTransformStillUnavailable(self):
		"""
		Recovery declares failure if MagSetFullscreenTransform still raises after reinit.
		This is the root cause of the Windows Magnifier conflict infinite loop.
		"""
		magnifier = FullScreenMagnifier()
		magnifier._startTimer = MagicMock()

		with patch("_magnifier.fullscreenMagnifier.magnification") as mock_mag:
			mock_mag.MagSetFullscreenTransform.side_effect = OSError("Still in use")
			with patch("_magnifier.fullscreenMagnifier.ui.message"):
				magnifier._attemptRecovery()

		self.assertFalse(magnifier._isActive)
		magnifier._startTimer.assert_not_called()


class TestFullScreenMagnifierKeepMouseCentered(_TestMagnifier):
	"""Tests for _keepMouseCentered in FullScreenMagnifier."""

	def setUp(self):
		super().setUp()
		self.magnifier = FullScreenMagnifier()
		self.magnifier._startMagnifier()
		self.screen = getPrimaryDisplayOrientation()

	def tearDown(self):
		self.magnifier._stopMagnifier()
		super().tearDown()

	def _expectedCenter(self, rawCoords: Coordinates) -> tuple[int, int]:
		"""Compute the expected cursor position using the same pipeline as _keepMouseCentered."""
		coords = self.magnifier._getCoordinatesForMode(rawCoords)
		params = self.magnifier._getMagnifierParameters(coords)
		return (
			params.coordinates.x + params.magnifierSize.width // 2,
			params.coordinates.y + params.magnifierSize.height // 2,
		)

	def testSkipsWhenLeftButtonPressed(self):
		"""Cursor is not moved when the left mouse button is held."""
		self.magnifier._currentCoordinates = Coordinates(500, 400)
		with (
			patch(
				"_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState",
				side_effect=lambda key: -1 if key == 1 else 0,
			),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_not_called()

	def testSkipsWhenRightButtonPressed(self):
		"""Cursor is not moved when the right mouse button is held."""
		self.magnifier._currentCoordinates = Coordinates(500, 400)
		with (
			patch(
				"_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState",
				side_effect=lambda key: -1 if key == 2 else 0,
			),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_not_called()

	def testSkipsWhenMiddleButtonPressed(self):
		"""Cursor is not moved when the middle mouse button is held."""
		self.magnifier._currentCoordinates = Coordinates(500, 400)
		with (
			patch(
				"_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState",
				side_effect=lambda key: -1 if key == 4 else 0,
			),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_not_called()

	def testCenterModeMiddleOfScreen(self):
		"""CENTER mode at screen center: cursor placed at the mode-adjusted, clamped center."""
		self.magnifier._fullscreenMode = FullScreenMode.CENTER
		raw = Coordinates(self.screen.width // 2, self.screen.height // 2)
		self.magnifier._currentCoordinates = raw
		expectedX, expectedY = self._expectedCenter(raw)
		with (
			patch("_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState", return_value=0),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_called_once_with(expectedX, expectedY)

	def testCenterModeAtEdge(self):
		"""CENTER mode near top-left corner: cursor lands at clamped view center, not raw coordinates."""
		self.magnifier._fullscreenMode = FullScreenMode.CENTER
		raw = Coordinates(10, 10)
		self.magnifier._currentCoordinates = raw
		expectedX, expectedY = self._expectedCenter(raw)
		# Clamping should shift the center away from (10, 10)
		self.assertNotEqual((expectedX, expectedY), (raw.x, raw.y))
		with (
			patch("_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState", return_value=0),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_called_once_with(expectedX, expectedY)

	def testRelativeMode(self):
		"""RELATIVE mode: cursor placed at the computed relative center, not raw coordinates."""
		self.magnifier._fullscreenMode = FullScreenMode.RELATIVE
		raw = Coordinates(self.screen.width // 4, self.screen.height // 4)
		self.magnifier._currentCoordinates = raw
		expectedX, expectedY = self._expectedCenter(raw)
		with (
			patch("_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState", return_value=0),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_called_once_with(expectedX, expectedY)

	def testBorderModeNoMovement(self):
		"""BORDER mode with focus inside margins: cursor placed at center of current screen position."""
		self.magnifier._fullscreenMode = FullScreenMode.BORDER
		screenCenter = Coordinates(self.screen.width // 2, self.screen.height // 2)
		self.magnifier._lastScreenPosition = screenCenter
		# Focus is inside the visible area margins — no scroll needed
		self.magnifier._currentCoordinates = screenCenter
		expectedX, expectedY = self._expectedCenter(screenCenter)
		with (
			patch("_magnifier.fullscreenMagnifier.winUser.getAsyncKeyState", return_value=0),
			patch("_magnifier.fullscreenMagnifier.winUser.setCursorPos") as mockSet,
		):
			self.magnifier._keepMouseCentered()
			mockSet.assert_called_once_with(expectedX, expectedY)
