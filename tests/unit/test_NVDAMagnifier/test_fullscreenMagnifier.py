import unittest
from unittest.mock import MagicMock, Mock, patch
import wx
import ctypes

from NVDAMagnifier import ColorFilter, ColorFilterMatrix, MagnifierType, FullScreenMagnifier, FullScreenMode


class TestFullScreenMagnifier(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup that runs once at the beginning."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup avant chaque test."""
		self.patcherStart = patch.object(FullScreenMagnifier, "_startMagnifier")
		self.patcherApplyColorFilter = patch.object(FullScreenMagnifier, "_applyColorFilter")

		self.magnifier = FullScreenMagnifier()

		self.magnifier._SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
		self.magnifier._SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
		self.magnifier._MARGIN_BORDER = 50
		self.centerX = self.magnifier._SCREEN_WIDTH // 2
		self.centerY = self.magnifier._SCREEN_HEIGHT // 2

		self.magnifier.zoomLevel = 2.0

	def tearDown(self):
		"""Cleanup après chaque test."""
		self.patcherStart.stop()
		self.patcherApplyColorFilter.stop()

		if hasattr(self.magnifier, "timer") and self.magnifier.timer:
			self.magnifier.timer.Stop()

	def _createMagnifier(self, **kwargs):
		"""Helper pour créer un magnifier avec patches."""
		return FullScreenMagnifier(**kwargs)

	def testFullScreenMagnifierCreation(self):
		"""Test : Creating the fullscreen magnifier."""
		zoomDefault = 2.0
		colorDefault = ColorFilter.NORMAL
		fullscreenModeDefault = FullScreenMode.CENTER

		def testValues(
			magnifier,
			zoomPassed=zoomDefault,
			colorFilterPassed=colorDefault,
			fullscreenModePassed=fullscreenModeDefault,
		):
			self.assertEqual(magnifier.zoomLevel, zoomPassed, "Zoom level mismatch")
			self.assertEqual(magnifier.colorFilter, colorFilterPassed, "Color filter mismatch")
			self.assertEqual(magnifier.fullscreenMode, fullscreenModePassed, "Fullscreen mode mismatch")
			self.assertIsInstance(magnifier, FullScreenMagnifier, "Expected instance of FullScreenMagnifier")
			self.assertEqual(magnifier.magnifierType, MagnifierType.FULLSCREEN, "Magnifier type mismatch")

		# Case 1: No parameters
		testValues(self.magnifier)

		# Case 2: Only zoom
		magnifier2 = self._createMagnifier(zoomLevel=4.0)
		testValues(magnifier2, zoomPassed=4.0)

		# Case 3: Only color filter
		magnifier3 = self._createMagnifier(colorFilter=ColorFilter.INVERTED)
		testValues(magnifier3, colorFilterPassed=ColorFilter.INVERTED)

		# Case 4: All parameters
		magnifier4 = self._createMagnifier(
			zoomLevel=4.0, colorFilter=ColorFilter.GREYSCALE, fullscreenMode=FullScreenMode.BORDER
		)
		testValues(
			magnifier4,
			zoomPassed=4.0,
			colorFilterPassed=ColorFilter.GREYSCALE,
			fullscreenModePassed=FullScreenMode.BORDER,
		)

	def testStartFullScreenMagnifier(self):
		"""Test : Activating and deactivating the fullscreen magnifier."""
		self.magnifier._loadMagnifierApi = MagicMock()
		self.magnifier._startTimer = MagicMock()

		# Need to stop the patch for _startMagnifier
		self.patcherStart.stop()
		try:
			self.magnifier._startMagnifier()
			self.magnifier._loadMagnifierApi.assert_called_once()
			self.magnifier._startTimer.assert_called_once()
			self.assertTrue(self.magnifier.isActive, "Magnifier should be active")
		finally:
			self.patcherStart.start()

	def testFullScreenDoUpdate(self):
		"""Test : Updating the magnifier."""

		def initValues(currentCoordinates, mode, lastFocusedObject):
			self.magnifier.currentCoordinates = currentCoordinates
			self.magnifier.lastScreenPosition = (0, 0)
			self.magnifier.fullscreenMode = mode
			self.magnifier.lastFocusedObject = lastFocusedObject
			self.magnifier._borderPos = MagicMock(return_value=(20, 20))
			self.magnifier._relativePos = MagicMock(return_value=(30, 30))
			self.magnifier._fullscreenMagnifier = MagicMock()

		def testValues(x, y):
			self.magnifier._doUpdate()
			if (
				self.magnifier.fullscreenMode.value == "border"
				and self.magnifier.lastFocusedObject == "mouse"
			):
				self.magnifier._borderPos.assert_called_once()
			elif self.magnifier.fullscreenMode.value == "relative":
				self.magnifier._relativePos.assert_called_once()
			self.assertEqual(self.magnifier.currentCoordinates, (x, y), "Current coordinates mismatch")
			self.assertEqual(self.magnifier.lastScreenPosition, (x, y), "Last screen position mismatch")
			self.magnifier._fullscreenMagnifier.assert_called_once()

		# Test cases
		test_cases = [
			((10, 10), FullScreenMode.CENTER, "mouse", 10, 10),
			((10, 10), FullScreenMode.CENTER, "nvda", 10, 10),
			((20, 20), FullScreenMode.BORDER, "mouse", 20, 20),
			((20, 20), FullScreenMode.BORDER, "nvda", 20, 20),
			((30, 30), FullScreenMode.RELATIVE, "mouse", 30, 30),
			((30, 30), FullScreenMode.RELATIVE, "nvda", 30, 30),
		]

		for coords, mode, focus_obj, expected_x, expected_y in test_cases:
			with self.subTest(mode=mode.value, focus=focus_obj):
				initValues(coords, mode, focus_obj)
				testValues(expected_x, expected_y)

	def testStopMagnifier(self):
		"""Test : Stopping the magnifier."""
		ctypes.windll.magnification.MagSetFullscreenColorEffect = MagicMock()
		self.magnifier._getMagnificationApi = MagicMock()
		self.magnifier._stopMagnifierApi = MagicMock()

		self.magnifier._stopMagnifier()

		ctypes.windll.magnification.MagSetFullscreenColorEffect.assert_called_once()
		self.magnifier._getMagnificationApi.assert_called_once()
		self.magnifier._stopMagnifierApi.assert_called_once()

	def testApplyColorFilter(self):
		"""Test : Color filter application."""
		test_cases = [
			(ColorFilter.NORMAL, ColorFilterMatrix.NORMAL),
			(ColorFilter.GREYSCALE, ColorFilterMatrix.GREYSCALE),
			(ColorFilter.INVERTED, ColorFilterMatrix.INVERTED),
		]

		for color_filter, matrix in test_cases:
			with self.subTest(filter=color_filter):
				self.magnifier.colorFilter = color_filter
				ctypes.windll.magnification.MagSetFullscreenColorEffect = MagicMock()

				# Stop patch for _applyColorFilter
				self.patcherApplyColorFilter.stop()
				try:
					self.magnifier._applyColorFilter()
					ctypes.windll.magnification.MagSetFullscreenColorEffect.assert_called_once_with(
						matrix.value
					)
				finally:
					self.patcherApplyColorFilter.start()

	def testFullscreenMagnifierTryExcept(self):
		"""Test : Specific try/except behavior in _fullscreenMagnifier."""
		self.magnifier.lastScreenPosition = (self.centerX, self.centerY)

		visibleWidth = int(self.magnifier._SCREEN_WIDTH / self.magnifier.zoomLevel)
		visibleHeight = int(self.magnifier._SCREEN_HEIGHT / self.magnifier.zoomLevel)
		left = self.centerX - visibleWidth // 2
		top = self.centerY - visibleHeight // 2

		with patch.object(
			self.magnifier, "_getMagnifierPosition", return_value=(left, top, visibleWidth, visibleHeight)
		):
			with patch.object(self.magnifier, "_getMagnificationApi") as mockGetApi:
				mockApiFunction = Mock(return_value=True)
				mockGetApi.return_value = mockApiFunction

				self.magnifier._fullscreenMagnifier(self.centerX, self.centerY)

				self.magnifier._getMagnifierPosition.assert_called_once_with(self.centerX, self.centerY)
				mockGetApi.assert_called_once()
				mockApiFunction.assert_called_once()

				call_args = mockApiFunction.call_args[0]
				self.assertEqual(call_args[0].value, self.magnifier.zoomLevel, "Zoom level mismatch")
				self.assertEqual(call_args[1].value, left, "Left position mismatch")
				self.assertEqual(call_args[2].value, top, "Top position mismatch")

	def testBorderPosReal(self):
		"""Test : Border position with realistic screen values."""
		self.magnifier.lastScreenPosition = (self.centerX, self.centerY)

		visibleWidth = int(self.magnifier._SCREEN_WIDTH / self.magnifier.zoomLevel)
		visibleHeight = int(self.magnifier._SCREEN_HEIGHT / self.magnifier.zoomLevel)
		left = self.centerX - visibleWidth // 2
		top = self.centerY - visibleHeight // 2

		with patch.object(
			self.magnifier, "_getMagnifierPosition", return_value=(left, top, visibleWidth, visibleHeight)
		):
			test_cases = [
				(self.centerX, self.centerY, "center"),
				(100, self.centerY, "left_edge"),
				(self.magnifier._SCREEN_WIDTH - 100, self.centerY, "right_edge"),
			]

			for x, y, case_name in test_cases:
				with self.subTest(case=case_name):
					result = self.magnifier._borderPos(x, y)
					self.assertIsInstance(result, tuple, "Expected tuple for border position")
					self.assertEqual(len(result), 2, "Expected tuple of length 2 for border position")
					self.assertGreaterEqual(result[0], 0, "Left border position should be >= 0")
					self.assertLessEqual(
						result[0],
						self.magnifier._SCREEN_WIDTH,
						"Left border position should be <= screen width",
					)
					self.assertGreaterEqual(result[1], 0, "Top border position should be >= 0")
					self.assertLessEqual(
						result[1],
						self.magnifier._SCREEN_HEIGHT,
						"Top border position should be <= screen height",
					)

	def testRelativePos(self):
		"""Test : Relative position calculation."""

		# Test cases
		test_cases = [
			(self.centerX, self.centerY, "center"),
			(50, 50, "near_origin"),
			(self.magnifier._SCREEN_WIDTH - 50, self.magnifier._SCREEN_HEIGHT - 50, "near_end"),
		]

		for x, y, case_name in test_cases:
			with self.subTest(case=case_name):
				result = self.magnifier._relativePos(x, y)
				self.assertIsInstance(result, tuple, "Expected tuple for relative position")
				self.assertEqual(len(result), 2, "Expected tuple of length 2 for relative position")
