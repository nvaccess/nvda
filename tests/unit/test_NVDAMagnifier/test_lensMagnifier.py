import unittest
from unittest.mock import MagicMock, Mock, patch
import wx

from NVDAMagnifier import ColorFilter, MagnifierType, LensMagnifier, LensFrame

class TestLensMagnifier(unittest.TestCase):


	@classmethod
	def setUpClass(cls):
		"""
		Setup qui s'exécute une fois au début.
		"""
		if not wx.GetApp():
			cls.app = wx.App(False)


	@patch.object(LensMagnifier, '_startMagnifier')
	def testLensMagnifierCreation(self, mock_start_magnifier):
		"""Test : Creating the fullscreen magnifier."""
		zoomDefault = 2.0
		colorDefault = ColorFilter.NORMAL
		
		def testValues(magnifier: LensMagnifier, zoomPassed: float = zoomDefault, colorFilterPassed: ColorFilter = colorDefault):
			self.assertEqual(magnifier.zoomLevel, zoomPassed)
			self.assertEqual(magnifier.colorFilter, colorFilterPassed)
			self.assertIsInstance(magnifier, LensMagnifier)
			self.assertEqual(magnifier.magnifierType, MagnifierType.LENS)
			self.assertIsInstance(magnifier._lensFrame, LensFrame)
			mock_start_magnifier.assert_called_once()

			# reseting instance

			mock_start_magnifier.reset_mock()


		# Case 1: No parameters

		magnifier = LensMagnifier()
		testValues(magnifier)

		# Case 2: Only zoom
		magnifier = LensMagnifier(zoomLevel=4.0)
		testValues(magnifier, zoomPassed=4.0)

		# Case 3: Only color filter
		magnifier = LensMagnifier(colorFilter=ColorFilter.INVERTED)
		testValues(magnifier, colorFilterPassed=ColorFilter.INVERTED)

		# case 4: all parameters
		magnifier = LensMagnifier(zoomLevel=4.0, colorFilter=ColorFilter.GREYSCALE)
		testValues(magnifier, zoomPassed=4.0, colorFilterPassed=ColorFilter.GREYSCALE)


	def testStartLensMagnifier(self):
		"""Test : Activating and deactivating the fullscreen magnifier."""
		with patch.object(LensMagnifier, '_startMagnifier'):
			magnifier = LensMagnifier()

		magnifier._startTimer = MagicMock()
		magnifier._lensFrame.Show = MagicMock()
		magnifier._lensFrame.startMagnifying = MagicMock()

		magnifier._startMagnifier()
		magnifier._startTimer.assert_called_once()
		magnifier._lensFrame.Show.assert_called_once()
		magnifier._lensFrame.startMagnifying.assert_called_once()
		self.assertTrue(magnifier.isActive)

	def testLensDoUpdate(self):
		"""Test : Updating the magnifier"""
		with patch.object(LensMagnifier, '_startMagnifier'):
			magnifier = LensMagnifier()

		magnifier._lensFrame.updateMagnifier = MagicMock()

		magnifier._doUpdate()
		magnifier._lensFrame.updateMagnifier.assert_called_once()


	def testStopMagnifier(self):
		"""Test : Stopping the Lens magnifier."""
		with patch.object(LensMagnifier, '_startMagnifier'):
			magnifier = LensMagnifier()

		magnifier._lensFrame.stopMagnifying = MagicMock()
		magnifier._stopMagnifier()

		magnifier._lensFrame.stopMagnifying.assert_called_once()
