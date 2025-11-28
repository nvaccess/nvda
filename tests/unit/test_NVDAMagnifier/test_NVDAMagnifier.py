import NVDAMagnifier
import unittest
from unittest.mock import MagicMock, Mock, patch, PropertyMock
import wx
import ctypes
from NVDAMagnifier import ColorFilter


class TestNVDAMagnifier(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""
		self.zoom = 2.0
		self.couleur = ColorFilter.NORMAL
		self.magnifier = NVDAMagnifier.NVDAMagnifier(self.zoom, self.couleur)
		self.screenWidth = ctypes.windll.user32.GetSystemMetrics(0)
		self.screenHeight = ctypes.windll.user32.GetSystemMetrics(1)

	def tearDown(self):
		"""Cleanup after each test."""
		if hasattr(self.magnifier, "timer") and self.magnifier.timer:
			self.magnifier.timer.Stop()
			self.magnifier.timer = None

		if hasattr(self.magnifier, "isActive") and self.magnifier.isActive:
			self.magnifier.isActive = False

	def testMagnifierCreation(self):
		"""Test : Can we create a magnifier with valid parameters or invalid ones?"""
		self.assertEqual(self.magnifier.zoomLevel, 2.0)
		self.assertEqual(self.magnifier.colorFilter, ColorFilter.NORMAL)

	def testStartMagnifier(self):
		"""Test : Activating and deactivating the magnifier."""
		self.magnifier._getFocusCoordinates = MagicMock(return_value=(100, 200))
		self.magnifier._startMagnifier()
		self.assertTrue(self.magnifier.isActive)

	def testUpdateMagnifier(self):
		"""Test : Updating the magnifier's properties."""
		self.magnifier._getFocusCoordinates = MagicMock(return_value=(100, 200))
		self.magnifier._doUpdate = MagicMock()
		self.magnifier._startTimer = MagicMock()

		# Call the update function without activation
		self.magnifier._updateMagnifier()
		self.magnifier._getFocusCoordinates.assert_not_called()
		self.magnifier._doUpdate.assert_not_called()
		self.magnifier._startTimer.assert_not_called()

		# Call the update function with activation
		self.magnifier.isActive = True
		self.magnifier._updateMagnifier()
		self.magnifier._getFocusCoordinates.assert_called_once()
		self.magnifier._doUpdate.assert_called_once()
		self.magnifier._startTimer.assert_called_once()

	def testDoUpdate(self):
		"""Test : DoUpdate function is called when Magnifier is active."""
		with self.assertRaises(NotImplementedError):
			self.magnifier._doUpdate()

	def testStopMagnifier(self):
		"""Test : Stopping the magnifier."""
		self.magnifier._stopTimer = MagicMock()

		# Call the stop function without activation
		self.magnifier._stopMagnifier()
		self.magnifier._stopTimer.assert_not_called()

		# Call the stop function with activation
		self.magnifier.isActive = True
		self.magnifier._stopMagnifier()
		self.magnifier._stopTimer.assert_called_once()
		self.assertFalse(self.magnifier.isActive, "Magnifier should be inactive after stopping")

	@patch("NVDAMagnifier.ui.message")
	def testZoom(self, mockUiMessage):
		"""Test : zoom in and out with valid values and check boundaries."""
		self.magnifier._zoom(True)
		mockUiMessage.assert_called_once()
		self.assertEqual(self.magnifier.zoomLevel, 2.5)

		self.magnifier.zoomLevel = 10.0
		mockUiMessage.reset_mock()

		self.magnifier._zoom(False)
		mockUiMessage.assert_called_once()
		self.assertEqual(self.magnifier.zoomLevel, 9.5)

		self.magnifier.zoomLevel = 10.0
		mockUiMessage.reset_mock()

		self.magnifier._zoom(True)
		mockUiMessage.assert_called_once()
		self.assertEqual(self.magnifier.zoomLevel, 10.0)

		self.magnifier.zoomLevel = 1.0
		mockUiMessage.reset_mock()

		self.magnifier._zoom(False)
		mockUiMessage.assert_called_once()
		self.assertEqual(self.magnifier.zoomLevel, 1.0)

	def testStartTimer(self):
		"""Test : Starting the timer."""
		self.magnifier._stopTimer = MagicMock()

		self.magnifier._startTimer()
		self.magnifier._stopTimer.assert_called_once
		self.assertIsInstance(self.magnifier.timer, wx.Timer, "timer should be an instance of wx.Timer")
		self.assertTrue(self.magnifier.timer.IsRunning(), "timer should be running after starting")

	def testStopTimer(self):
		"""Test : Stopping the timer."""
		self.magnifier._startTimer()
		self.magnifier._stopTimer()
		self.assertIsNone(self.magnifier.timer)

	def testMagnifierPosition(self):
		"""Test : Computing magnifier position and size."""
		x, y = int(self.screenWidth / 2), int(self.screenHeight / 2)
		left, top, width, height = self.magnifier._getMagnifierPosition(x, y)

		expected_width = self.screenWidth / self.magnifier.zoomLevel
		expected_height = self.screenHeight / self.magnifier.zoomLevel
		expected_left = int(x - (expected_width / 2))
		expected_top = int(y - (expected_height / 2))

		self.assertEqual(left, expected_left)
		self.assertEqual(top, expected_top)
		self.assertEqual(width, expected_width)
		self.assertEqual(height, expected_height)

		# Test 2 : Left clamping
		left, top, width, height = self.magnifier._getMagnifierPosition(100, 540)
		self.assertGreaterEqual(left, 0)

		# Test 3 : Right clamping
		left, top, width, height = self.magnifier._getMagnifierPosition(1800, 540)
		self.assertLessEqual(left + width, self.screenWidth)

		# Test 4 : Different zoom
		self.magnifier.zoomLevel = 4.0
		left, top, width, height = self.magnifier._getMagnifierPosition(960, 540)
		expected_width = int(self.screenWidth / self.magnifier.zoomLevel)
		expected_height = int(self.screenHeight / self.magnifier.zoomLevel)
		self.assertEqual(width, expected_width)
		self.assertEqual(height, expected_height)

	def testGetNvdaPosition(self):
		"""Test : Getting NVDA position with different API responses."""
		# Case 1: Review position successful
		with patch("api.getReviewPosition") as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point

			x, y = self.magnifier._getNvdaPosition()
			self.assertEqual((x, y), (300, 400))

		# Case 2: Review position fails, navigator works
		with patch("api.getReviewPosition", return_value=None):
			with patch("api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = (100, 150, 200, 300)

				x, y = self.magnifier._getNvdaPosition()
				# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
				self.assertEqual((x, y), (200, 300))

		# Case 3: Everything fails
		with patch("api.getReviewPosition", return_value=None):
			with patch("api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = Mock(side_effect=Exception())

				x, y = self.magnifier._getNvdaPosition()
				self.assertEqual((x, y), (0, 0))

	def testGetFocusCoordinates(self):
		"""Test : All priority scenarios for focus coordinates."""

		def testValues(
			getNvda: tuple[int, int],
			mousePos: tuple[int, int],
			leftPressed: bool,
			expected_coords: tuple[int, int],
			expected_focused: str,
		):
			self.magnifier._getNvdaPosition = MagicMock(return_value=getNvda)
			self.magnifier.lastNVDAPosition = (0, 0)
			self.magnifier.lastMousePosition = (0, 0)
			self.magnifier._mouseHandler.isLeftClickPressed = MagicMock(return_value=leftPressed)

			type(self.magnifier._mouseHandler).mousePosition = PropertyMock(return_value=mousePos)

			focusCoordinates = self.magnifier._getFocusCoordinates()

			self.assertEqual(focusCoordinates, expected_coords)
			self.assertEqual(self.magnifier.lastFocusedObject, expected_focused)

		# Case 1: Left click is pressed should return mouse position
		testValues((0, 0), (0, 0), True, (0, 0), "mouse")

		# Case 2: Not left click mouse moving
		testValues((0, 0), (10, 10), False, (10, 10), "mouse")

		# Case 3: Last move is NVDA mouse not changed
		testValues((10, 10), (0, 0), False, (10, 10), "nvda")

		# Case 4: Nothing changed last move Mouse
		self.magnifier.lastFocusedObject = "mouse"
		testValues((0, 0), (0, 0), False, (0, 0), "mouse")

		# Case 5: Nothing changed last move NVDA
		self.magnifier.lastFocusedObject = "nvda"
		testValues((0, 0), (0, 0), False, (0, 0), "nvda")

		# Case 6: Both have moved and no Left click
		testValues((10, 10), (20, 20), False, (20, 20), "mouse")

		# Case 7: Both have moved and Left click
		testValues((10, 10), (20, 20), True, (20, 20), "mouse")

		# Case 8: Only nvda moved but left pressed (very unlikely)
		testValues((10, 10), (0, 0), True, (0, 0), "mouse")
