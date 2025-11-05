import unittest
from unittest.mock import MagicMock, patch
import wx

from NVDAMagnifier import ColorFilter, MagnifierType, DockedMagnifier, DockedFrame


class TestDockedMagnifier(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""
		Setup once for all tests.
		"""
		if not wx.GetApp():
			cls.app = wx.App(False)

	@patch.object(DockedMagnifier, "_startMagnifier")
	def testDockedMagnifierCreation(self, mock_start_magnifier):
		"""Test : Creating the fullscreen magnifier."""
		zoomDefault = 2.0
		colorDefault = ColorFilter.NORMAL

		def testValues(
			magnifier: DockedMagnifier,
			zoomPassed: float = zoomDefault,
			colorFilterPassed: ColorFilter = colorDefault,
		):
			self.assertEqual(magnifier.zoomLevel, zoomPassed)
			self.assertEqual(magnifier.colorFilter, colorFilterPassed)
			self.assertIsInstance(magnifier, DockedMagnifier)
			self.assertEqual(magnifier.magnifierType, MagnifierType.DOCKED)
			self.assertIsInstance(magnifier._dockedFrame, DockedFrame)
			mock_start_magnifier.assert_called_once()

			# reseting instance

			mock_start_magnifier.reset_mock()

		# Case 1: No parameters

		magnifier = DockedMagnifier()
		testValues(magnifier)

		# Case 2: Only zoom
		magnifier = DockedMagnifier(zoomLevel=4.0)
		testValues(magnifier, zoomPassed=4.0)

		# Case 3: Only color filter
		magnifier = DockedMagnifier(colorFilter=ColorFilter.INVERTED)
		testValues(magnifier, colorFilterPassed=ColorFilter.INVERTED)

		# case 4: all parameters
		magnifier = DockedMagnifier(zoomLevel=4.0, colorFilter=ColorFilter.GREYSCALE)
		testValues(magnifier, zoomPassed=4.0, colorFilterPassed=ColorFilter.GREYSCALE)

	def testStartDockedMagnifier(self):
		"""Test : Activating and deactivating the fullscreen magnifier."""
		magnifier = DockedMagnifier()

		magnifier._startTimer = MagicMock()
		magnifier._dockedFrame.Show = MagicMock()
		magnifier._dockedFrame.startMagnifying = MagicMock()

		magnifier._startMagnifier()
		magnifier._startTimer.assert_called_once()
		magnifier._dockedFrame.Show.assert_called_once()
		magnifier._dockedFrame.startMagnifying.assert_called_once()
		self.assertTrue(magnifier.isActive)

	def testDockedDoUpdate(self):
		"""Test : Updating the magnifier"""
		with patch.object(DockedMagnifier, "_startMagnifier"):
			magnifier = DockedMagnifier()

		magnifier._dockedFrame.updateMagnifier = MagicMock()
		magnifier._mouseHandler.getMousePosition = MagicMock()

		magnifier._doUpdate()
		magnifier._dockedFrame.updateMagnifier.assert_called_once()

	def testStopMagnifier(self):
		"""Test : Stopping the docked magnifier."""
		with patch.object(DockedMagnifier, "_startMagnifier"):
			magnifier = DockedMagnifier()

		magnifier._dockedFrame.stopMagnifying = MagicMock()
		magnifier._stopMagnifier()

		magnifier._dockedFrame.stopMagnifying.assert_called_once()
