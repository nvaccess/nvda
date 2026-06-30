# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from unittest.mock import MagicMock, patch
from _magnifier.config import ZoomLevel
from _magnifier.magnifier import Magnifier
from _magnifier.utils.types import Filter, FullScreenMode, MagnifiedView, Direction, Coordinates
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

		self.mock_mag_fs.reset_mock()
		magnifier._attemptRecovery()

		# MagUninitialize: once best-effort uninit + once in _clearStaleApiState
		self.assertEqual(self.mock_mag_fs.MagUninitialize.call_count, 2)
		# MagInitialize: once in _clearStaleApiState + once for the real init
		self.assertEqual(self.mock_mag_fs.MagInitialize.call_count, 2)
		self.mock_mag_fs.MagSetFullscreenTransform.assert_called_once_with(magnifier.zoomLevel / 100.0, 0, 0)
		# MagSetFullscreenColorEffect: once in _clearStaleApiState + once in _attemptRecovery
		self.assertEqual(self.mock_mag_fs.MagSetFullscreenColorEffect.call_count, 2)
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


class TestFullScreenMagnifierApi(_TestMagnifier):
	"""Tests for FullScreenMagnifier interactions with the Windows Magnification API."""

	def testCannotStartWhenWindowsMagnifierRunning(self):
		"""MagSetFullscreenTransform fails because Windows Magnifier is running: magnifier must not start."""
		self.mock_mag_fs.MagSetFullscreenTransform.side_effect = OSError("API in use by another magnifier")

		with patch("_magnifier.fullscreenMagnifier.ui.message") as mock_message:
			magnifier = FullScreenMagnifier()
			magnifier._startMagnifier()

		self.assertFalse(magnifier._isActive)
		mock_message.assert_called_once()
		self.assertIsNone(magnifier._timer)

	def testCannotStartWhenMagInitializeFails(self):
		"""MagInitialize fails: magnifier must not start and the user must be notified."""
		self.mock_mag_fs.MagInitialize.side_effect = OSError("Cannot initialize magnification API")

		with patch("_magnifier.fullscreenMagnifier.ui.message") as mock_message:
			magnifier = FullScreenMagnifier()
			magnifier._startMagnifier()

		self.assertFalse(magnifier._isActive)
		mock_message.assert_called_once()
		self.assertIsNone(magnifier._timer)

	def testRecoveryCapStopsMagnifier(self):
		"""After _MAX_RECOVERY_ATTEMPTS failed attempts, the magnifier stops and the user is notified."""
		magnifier = FullScreenMagnifier()
		magnifier._recoveryAttempts = FullScreenMagnifier._MAX_RECOVERY_ATTEMPTS

		with patch("_magnifier.fullscreenMagnifier.ui.message") as mock_message:
			magnifier._attemptRecovery()

		self.assertFalse(magnifier._isActive)
		mock_message.assert_called_once()

	def testRecoveryFailsWhenTransformStillUnavailable(self):
		"""Recovery declares failure if MagSetFullscreenTransform still raises after reinit."""
		magnifier = FullScreenMagnifier()
		magnifier._startTimer = MagicMock()

		with patch("_magnifier.fullscreenMagnifier.magnification") as mock_mag:
			mock_mag.MagSetFullscreenTransform.side_effect = OSError("Still in use")
			with patch("_magnifier.fullscreenMagnifier.ui.message"):
				magnifier._attemptRecovery()

		self.assertFalse(magnifier._isActive)
		magnifier._startTimer.assert_not_called()


class TestFullScreenMagnifierMoveMouseToViewCenter(_TestMagnifier):
	"""Tests for moveMouseToViewCenter in FullScreenMagnifier."""

	def setUp(self):
		super().setUp()
		self.magnifier = FullScreenMagnifier()
		self.magnifier._startMagnifier()
		self.screen = getPrimaryDisplayOrientation()

	def tearDown(self):
		self.magnifier._stopMagnifier()
		super().tearDown()

	def _expectedCenter(self, rawCoords: Coordinates) -> tuple[int, int]:
		"""Compute the expected cursor position using the same pipeline as _computeMagnifiedViewCenter."""
		coords = self.magnifier._getCoordinatesForMode(rawCoords)
		params = self.magnifier._getMagnifierParameters(coords)
		return (
			params.coordinates.x + params.magnifierSize.width // 2,
			params.coordinates.y + params.magnifierSize.height // 2,
		)

	def testMoveMouseToViewCenterPlacesCursorAtCenter(self):
		"""moveMouseToViewCenter places cursor at the computed view center."""
		self.magnifier._fullscreenMode = FullScreenMode.CENTER
		raw = Coordinates(self.screen.width // 2, self.screen.height // 2)
		self.magnifier._currentCoordinates = raw
		expectedX, expectedY = self._expectedCenter(raw)
		with patch("_magnifier.magnifier.winUser.setCursorPos") as mockSet:
			self.magnifier.moveMouseToViewCenter()
			mockSet.assert_called_once_with(expectedX, expectedY)
