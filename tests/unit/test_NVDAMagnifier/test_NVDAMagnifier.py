import NVDAMagnifier
import unittest
from unittest.mock import MagicMock, Mock, patch
import wx
import ctypes

from NVDAMagnifier import ColorFilter, NVDAMagnifier


class TestNVDAMagnifier(unittest.TestCase):



	@classmethod
	def setUpClass(cls):
		"""Setup qui s'exécute une fois au début."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def testMagnifierCreation(self):
		"""Test : Can we create a magnifier with valid parameters or invalid ones?"""
		zoom = 2.0
		couleur = ColorFilter.NORMAL

		magnifier = NVDAMagnifier(zoom, couleur)

		self.assertEqual(magnifier.zoomLevel, 2.0)
		self.assertEqual(magnifier.colorFilter, ColorFilter.NORMAL)

	def testStartMagnifier(self):
		"""Test : Activating and deactivating the magnifier."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)
		magnifier._getFocusCoordinates = MagicMock(return_value=(100, 200))
		magnifier._startMagnifier()
		self.assertTrue(magnifier.isActive)

	def testUpdateMagnifier(self):
		"""Test : Updating the magnifier's properties."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)
		magnifier._getFocusCoordinates = MagicMock(return_value=(100, 200))
		magnifier._doUpdate = MagicMock()
		magnifier._startTimer = MagicMock()

		# Call the update function without activation

		magnifier._updateMagnifier()
		magnifier._getFocusCoordinates.assert_not_called()
		magnifier._doUpdate.assert_not_called()
		magnifier._startTimer.assert_not_called()

		# Call the update function with activation

		magnifier.isActive = True
		magnifier._updateMagnifier()
		magnifier._getFocusCoordinates.assert_called_once()
		magnifier._doUpdate.assert_called_once()
		magnifier._startTimer.assert_called_once()


	def testDoUpdate(self):
		"""Test : DoUpdate function is called when Magnifier is active."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)

		with self.assertRaises(NotImplementedError):
			magnifier._doUpdate()

	def testStopMagnifier(self):
		"""Test : Stopping the magnifier."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)
		magnifier._stopTimer = MagicMock()

		# Call the stop function without activation

		magnifier._stopMagnifier()
		magnifier._stopTimer.assert_not_called()

		# Call the stop function with activation
		
		magnifier.isActive = True
		magnifier._stopMagnifier()
		magnifier._stopTimer.assert_called_once()
		self.assertFalse(magnifier.isActive, "Magnifier should be inactive after stopping")

	def testZoom(self):
		"""Test : zoom in and out with valid values and check boundaries."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)

		magnifier._zoom(True)
		self.assertEqual(magnifier.zoomLevel, 2.5)

		magnifier.zoomLevel = 10.0
		magnifier._zoom(False)
		self.assertEqual(magnifier.zoomLevel, 9.5)

		magnifier.zoomLevel = 10.0
		magnifier._zoom(True)
		self.assertEqual(magnifier.zoomLevel, 10.0)

		magnifier.zoomLevel = 1.0
		magnifier._zoom(False)
		self.assertEqual(magnifier.zoomLevel, 1.0)

	def testStartTimer(self):
		"""Test : Starting the timer."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)
		magnifier._stopTimer = MagicMock()

		magnifier._startTimer()
		magnifier._stopTimer.assert_called_once
		self.assertIsInstance(magnifier.timer, wx.Timer, "timer should be an instance of wx.Timer")
		self.assertTrue(magnifier.timer.IsRunning(), "timer should be running after starting")

	def testStopTimer(self):
		"""Test : Stopping the timer (version corrigée)."""
		
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)

		magnifier._startTimer()
		magnifier._stopTimer()
		self.assertIsNone(magnifier.timer)

	def testMagnifierPosition(self):
		"""Test : Computing magnifier position and size."""
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)

		screenWidth = ctypes.windll.user32.GetSystemMetrics(0)
		screenHeight = ctypes.windll.user32.GetSystemMetrics(1)

		x, y = int(screenWidth / 2), int(screenHeight / 2)  
		left, top, width, height = magnifier._getMagnifierPosition(x, y)

		expected_width = screenWidth / magnifier.zoomLevel
		expected_height = screenHeight / magnifier.zoomLevel 
		expected_left = int(x - (expected_width / 2)) 
		expected_top = int(y - (expected_height / 2)) 
		
		self.assertEqual(left, expected_left)
		self.assertEqual(top, expected_top)
		self.assertEqual(width, expected_width)
		self.assertEqual(height, expected_height)

		# Test 2 : Left clamping
		left, top, width, height = magnifier._getMagnifierPosition(100, 540)
		self.assertGreaterEqual(left, 0)

		# Test 3 : Right clamping
		left, top, width, height = magnifier._getMagnifierPosition(1800, 540)
		self.assertLessEqual(left + width, screenWidth)

		# Test 4 : Different zoom
		magnifier.zoomLevel = 4.0
		left, top, width, height = magnifier._getMagnifierPosition(960, 540)
		expected_width = int(screenWidth / magnifier.zoomLevel)
		expected_height = int(screenHeight / magnifier.zoomLevel)
		self.assertEqual(width, expected_width)
		self.assertEqual(height, expected_height)

	def testGetNvdaPosition(self):
		"""Test : Getting NVDA position with different API responses."""
		
		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)
		
		# Scenario 1: Review position successful
		with patch('api.getReviewPosition') as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point
			
			x, y = magnifier._getNvdaPosition()
			self.assertEqual((x, y), (300, 400))
		
		# Scenario 2: Review position fails, navigator works
		with patch('api.getReviewPosition', return_value=None):
			with patch('api.getNavigatorObject') as mock_navigator:
				mock_navigator.return_value.location = (100, 150, 200, 300)
				
				x, y = magnifier._getNvdaPosition()
				# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
				self.assertEqual((x, y), (200, 300))
		
		# Scenario 3: Everything fails
		with patch('api.getReviewPosition', return_value=None):
			with patch('api.getNavigatorObject') as mock_navigator:
				mock_navigator.return_value.location = Mock(side_effect=Exception())
				
				x, y = magnifier._getNvdaPosition()
				self.assertEqual((x, y), (0, 0))

	def testGetFocusCoordinatesScenarios(self):
		"""Test : All priority scenarios for focus coordinates."""

		magnifier = NVDAMagnifier(2.0, ColorFilter.NORMAL)
		
		def initValues(getNvda: tuple[int, int], mousePos: tuple[int, int], leftPressed: bool):
			magnifier._getNvdaPosition = MagicMock(return_value=getNvda)
			magnifier.lastNVDAPosition = (0,0)

			magnifier._mouseHandler.mousePosition = mousePos
			magnifier.lastMousePosition = (0,0)
			magnifier._mouseHandler.isLeftClickPressed = MagicMock(return_value=leftPressed)


		def testValues(returned: tuple[int, int], lastFocusedObject: str):
			focusCoordinates = magnifier._getFocusCoordinates()
			self.assertEqual(focusCoordinates, returned, f"Focus coordinates should return {returned} and not {focusCoordinates}")
			self.assertEqual(magnifier.lastFocusedObject, lastFocusedObject, f"Last focused object should return {lastFocusedObject} and not {magnifier.lastFocusedObject}")


		# Case 1 Left click is pressed should return mouse position
		initValues((0, 0), (0, 0), True)
		testValues((0, 0), "mouse")

		# case 2 Not left click mouse moving

		initValues((0, 0), (10, 10), False)
		testValues((10, 10), "mouse")

		# Case 3 Last move is NVDA mouse not changed

		initValues((10, 10), (0, 0), False)
		testValues((10,10), "nvda")

		# Case 4 noting changed last move Mouse

		initValues((0, 0), (0, 0), False)
		magnifier.lastFocusedObject = "mouse"
		testValues((0, 0), "mouse")

		# Case 5 noting changed last move NVDA

		initValues((0, 0), (0, 0), False)
		magnifier.lastFocusedObject = "nvda"
		testValues((0, 0), "nvda")

		# Case 6 both haved moved and no Left click

		initValues((10, 10), (20, 20), False)
		testValues((20, 20), "mouse")

		# Case 7 Both haved moved and Left click

		initValues((10, 10), (20, 20), True)
		testValues((20, 20), "mouse")

		# Case 8 only nvda moved but left pressed (very unlikely)

		initValues((10, 10), (0, 0), True)
		testValues((0, 0), "mouse")
