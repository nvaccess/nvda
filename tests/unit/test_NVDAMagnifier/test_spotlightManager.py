import unittest
from unittest.mock import MagicMock, patch
import wx

from NVDAMagnifier import SpotlightManager, FullScreenMagnifier


class TestSpotlightManager(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup qui s'exécute une fois au début."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""
		self.fullscreenMagnifier = FullScreenMagnifier()
		self.spotlightManager = SpotlightManager(self.fullscreenMagnifier)

	def tearDown(self):
		"""Cleanup after each test."""
		if self.spotlightManager._timer:
			self.spotlightManager._timer.Stop()
			self.spotlightManager._timer = None

	def _createMagnifier(self, **kwargs):
		"""Helper for creating a magnifier with patches."""
		return FullScreenMagnifier(**kwargs)

	def _createSpotlightManager(self):
		"""Helper for creating a spotlight manager with patches."""
		return SpotlightManager(self.fullscreenMagnifier)

	def testInitSpotlight(self):
		"""Test : SpotlightManager initialization."""
		self.assertIsNone(self.spotlightManager._timer)
		self.assertFalse(self.spotlightManager._spotlightIsActive)
		self.assertEqual(self.spotlightManager._animationSteps, 40)
		self.assertIsInstance(self.spotlightManager._fullscreenMagnifier, FullScreenMagnifier)

	@patch("NVDAMagnifier.ui.message")
	def testStartSpotlight(self, mockUiMessage):
		"""Test : SpotlightManager start spotlight."""
		self.spotlightManager._animateZoom = MagicMock()
		self.fullscreenMagnifier._getFocusCoordinates = MagicMock()
		self.fullscreenMagnifier._getCoordinatesForMode = MagicMock()

		self.spotlightManager._startSpotlight()

		mockUiMessage.assert_called_once()
		self.assertTrue(self.spotlightManager._spotlightIsActive)
		self.fullscreenMagnifier._getFocusCoordinates.assert_called_once()
		self.fullscreenMagnifier._getCoordinatesForMode.assert_called_once()
		self.spotlightManager._animateZoom.assert_called_once()

	@patch("NVDAMagnifier.ui.message")
	def testStopSpotlight(self, mockUiMessage):
		"""Test : SpotlightManager stop spotlight."""
		self.fullscreenMagnifier._stopSpotlight = MagicMock()

		self.spotlightManager._stopSpotlight()

		mockUiMessage.assert_called_once()
		self.assertIsNone(self.spotlightManager._timer)
		self.assertFalse(self.spotlightManager._spotlightIsActive)
		self.fullscreenMagnifier._stopSpotlight.assert_called_once()

	def testAnimateZoom(self):
		"""Test : SpotlightManager animate zoom."""
		self.spotlightManager._executeStep = MagicMock()
		self.spotlightManager._computeAnimationSteps = MagicMock()
		targetZoom, targetCoordinates, callback = 2.0, (200, 200), MagicMock()

		self.spotlightManager._animateZoom(targetZoom, targetCoordinates, callback)

		self.spotlightManager._computeAnimationSteps.assert_called_once_with(
			self.spotlightManager._currentZoomLevel,
			targetZoom,
			self.spotlightManager._currentCoordinates,
			targetCoordinates,
		)
		self.spotlightManager._executeStep.assert_called_once_with(0, callback)

	@patch("wx.CallLater")
	def testExecuteStep(self, mockCallLater):
		"""Test : SpotlightManager execute step."""
		self.fullscreenMagnifier._fullscreenMagnifier = MagicMock()
		callback = MagicMock()

		self.spotlightManager._animationStepsList = [(5.0, (300, 300)), (1.0, (100, 100))]

		self.spotlightManager._executeStep(0, callback)

		zoomLevel, (x, y) = self.spotlightManager._animationStepsList[0]
		self.assertEqual(self.fullscreenMagnifier.zoomLevel, zoomLevel)
		self.fullscreenMagnifier._fullscreenMagnifier.assert_called_once_with(x, y)
		self.assertEqual(self.spotlightManager._currentZoomLevel, zoomLevel)
		self.assertEqual(self.spotlightManager._currentCoordinates, (x, y))

		mockCallLater.assert_called_once_with(12, unittest.mock.ANY)
		callback.assert_not_called()

		# Reset mocks
		self.fullscreenMagnifier._fullscreenMagnifier.reset_mock()
		mockCallLater.reset_mock()

		self.spotlightManager._executeStep(2, callback)

		mockCallLater.assert_not_called()
		self.fullscreenMagnifier._fullscreenMagnifier.assert_not_called()
		callback.assert_called_once()

	@patch("wx.CallLater")
	def testStartMouseMonitoring(self, mockCallLater):
		"""Test : SpotlightManager start mouse monitoring."""
		mockTimer = MagicMock()
		mockCallLater.return_value = mockTimer

		self.spotlightManager._startMouseMonitoring()
		self.assertEqual(self.spotlightManager._lastMousePosition, wx.GetMousePosition())
		mockCallLater.assert_called_once_with(2000, self.spotlightManager._checkMouseIdle)
		self.assertEqual(self.spotlightManager._timer, mockTimer)

	@patch("wx.CallLater")
	def testCheckMouseIdle(self, mockCallLater):
		"""Test : SpotlightManager check mouse idle."""
		self.spotlightManager._animateZoom = MagicMock()
		self.fullscreenMagnifier._getCoordinatesForMode = MagicMock()

		# Test case: mouse didn't move
		self.spotlightManager._spotlightIsActive = True
		self.spotlightManager._lastMousePosition = wx.GetMousePosition()

		self.spotlightManager._checkMouseIdle()

		self.fullscreenMagnifier._getCoordinatesForMode.assert_called_once_with(
			self.spotlightManager._lastMousePosition
		)
		self.spotlightManager._animateZoom.assert_called_once()

		# Reset mocks
		self.spotlightManager._animateZoom.reset_mock()
		self.fullscreenMagnifier._getCoordinatesForMode.reset_mock()
		mockCallLater.reset_mock()

		# Test case: mouse moved
		self.spotlightManager._lastMousePosition = wx.GetMousePosition()

		mock_timer = MagicMock()
		mockCallLater.return_value = mock_timer
		newMousePos = (200, 300)
		wx.GetMousePosition = MagicMock(return_value=newMousePos)
		self.spotlightManager._checkMouseIdle()

		self.assertEqual(self.spotlightManager._lastMousePosition, newMousePos)
		mockCallLater.assert_called_once_with(1500, self.spotlightManager._checkMouseIdle)
		self.assertEqual(self.spotlightManager._timer, mock_timer)
		self.spotlightManager._animateZoom.assert_not_called()
		self.fullscreenMagnifier._getCoordinatesForMode.assert_not_called()

	def testComputeAnimationSteps(self):
		"""Test : SpotlightManager compute animation steps."""

		testCases = [
			(2.0, 1.0, (100, 100), (400, 400)),
			(1.0, 4.0, (200, 200), (500, 500)),
		]

		for currentZoom, targetZoom, currentCoords, targetCoords in testCases:
			animationSteps = self.spotlightManager._computeAnimationSteps(
				currentZoom, targetZoom, currentCoords, targetCoords
			)
			self.assertIsInstance(animationSteps, list)
			self.assertEqual(len(animationSteps), self.spotlightManager._animationSteps)
			for step in animationSteps:
				self.assertIsInstance(step, tuple)
				self.assertEqual(len(step), 2)
				self.assertIsInstance(step[0], float)
				self.assertIsInstance(step[1], tuple)
				self.assertEqual(len(step[1]), 2)
				self.assertIsInstance(step[1][0], int)
				self.assertIsInstance(step[1][1], int)
