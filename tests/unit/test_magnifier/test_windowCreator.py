# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest.mock import MagicMock, patch
from _magnifier.utils.types import Coordinates, Size, WindowMagnifierParameters, Filter, MagnifierParameters
import wx
from _magnifier.utils.windowCreator import MagnifierPanel, MagnifierFrame, WindowedMagnifier


class TestMagnifierPanel(unittest.TestCase):
	"""Tests for the MagnifierPanel class."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Set up test fixtures."""
		self.frame = wx.Frame(None)
		self.panelType = "testPanel"
		self.panel = MagnifierPanel(self.frame, self.panelType)

	def tearDown(self):
		"""Clean up after tests."""
		if self.frame:
			self.frame.Destroy()

	def test_init(self):
		"""Test MagnifierPanel initialization."""
		self.assertEqual(self.panel.panelType, self.panelType)
		self.assertEqual(self.panel.GetName(), self.panelType)
		self.assertIsNone(self.panel.contentBitmap)

	def test_setContent_with_valid_bitmap(self):
		"""Test setContent with a valid wx.Bitmap."""
		bitmap = wx.Bitmap(100, 100)
		self.panel.setContent(bitmap)

		self.assertIsNotNone(self.panel.contentBitmap)
		self.assertEqual(self.panel.contentBitmap, bitmap)

	def test_setContent_with_valid_image(self):
		"""Test setContent with a valid wx.Image."""
		image = wx.Image(100, 100)
		self.panel.setContent(image)

		self.assertIsNotNone(self.panel.contentBitmap)
		self.assertIsInstance(self.panel.contentBitmap, wx.Bitmap)

	def test_setContent_with_none(self):
		"""Test setContent with None to clear content."""
		bitmap = wx.Bitmap(100, 100)
		self.panel.setContent(bitmap)
		self.assertIsNotNone(self.panel.contentBitmap)
		self.panel.setContent(None)
		self.assertIsNone(self.panel.contentBitmap)

	def test_setContent_with_invalid_bitmap(self):
		"""Test setContent with an invalid bitmap."""
		bitmap = wx.Bitmap()  # Empty/invalid bitmap
		self.panel.setContent(bitmap)

		self.assertIsNone(self.panel.contentBitmap)

	def test_setContent_with_invalid_image(self):
		"""Test setContent with an invalid image."""
		image = wx.Image()  # Empty/invalid image
		self.panel.setContent(image)

		self.assertIsNone(self.panel.contentBitmap)

	def test_onPaint_without_content(self):
		"""Test onPaint without content."""
		event = MagicMock()
		mockDC = MagicMock()

		with patch("wx.PaintDC", return_value=mockDC):
			self.panel.onPaint(event)
			mockDC.Clear.assert_called_once()
			mockDC.DrawBitmap.assert_not_called()

	def test_onPaint_with_content(self):
		"""Test onPaint with content."""
		bitmap = wx.Bitmap(100, 100)
		self.panel.setContent(bitmap)

		event = MagicMock()
		mockDC = MagicMock()

		with patch("wx.PaintDC", return_value=mockDC):
			self.panel.onPaint(event)
			mockDC.Clear.assert_called_once()
			mockDC.DrawBitmap.assert_called_once_with(bitmap, 0, 0)


class TestMagnifierFrame(unittest.TestCase):
	"""Tests for the MagnifierFrame class."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Set up test fixtures."""
		windowMagnifierParams = WindowMagnifierParameters(
			title="Test Magnifier",
			windowSize=Size(width=400, height=300),
			windowPosition=Coordinates(x=100, y=100),
			styles=wx.DEFAULT_FRAME_STYLE,
		)
		self.frame = MagnifierFrame(
			title="Test Frame",
			frameType="testFrame",
			screenSize=Size(width=1920, height=1080),
			windowMagnifierParameters=windowMagnifierParams,
		)
		# Hide the frame to prevent it from being displayed during tests
		self.frame.Hide()

	def tearDown(self):
		"""Clean up after tests."""
		if self.frame:
			self.frame.Destroy()

	def test_init(self):
		"""Test MagnifierFrame initialization."""
		self.assertEqual(self.frame.frameType, "testFrame")
		self.assertIsNotNone(self.frame.screenSize)
		self.assertEqual(self.frame.screenSize.width, 1920)
		self.assertEqual(self.frame.screenSize.height, 1080)
		self.assertIsNotNone(self.frame.windowMagnifierParameters)
		self.assertIsNotNone(self.frame.panel)
		self.assertIsInstance(self.frame.panel, MagnifierPanel)
		self.assertEqual(self.frame.GetSize().GetWidth(), 400)
		self.assertEqual(self.frame.GetSize().GetHeight(), 300)
		self.assertEqual(self.frame.GetPosition().x, 100)
		self.assertEqual(self.frame.GetPosition().y, 100)

	def test_createPanel(self):
		"""Test createPanel method."""
		panel = self.frame.createPanel()
		self.assertIsNotNone(panel)
		self.assertIsInstance(panel, MagnifierPanel)
		self.assertEqual(panel.panelType, "testFrame")

	def test_updateFrameContent(self):
		"""Test updateFrameContent method."""
		bitmap = wx.Bitmap(200, 150)
		self.frame.updateFrameContent(bitmap)
		self.assertEqual(self.frame.panel.contentBitmap, bitmap)

		image = wx.Image(200, 150)
		self.frame.updateFrameContent(image)
		self.assertIsNotNone(self.frame.panel.contentBitmap)
		self.assertIsInstance(self.frame.panel.contentBitmap, wx.Bitmap)

		self.frame.updateFrameContent(None)
		self.assertIsNone(self.frame.panel.contentBitmap)


class TestWindowedMagnifier(unittest.TestCase):
	"""Tests for the WindowedMagnifier class."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Set up test fixtures."""
		windowMagnifierParams = WindowMagnifierParameters(
			title="Test WindowedMagnifier",
			windowSize=Size(400, 300),
			windowPosition=Coordinates(100, 100),
			styles=wx.DEFAULT_FRAME_STYLE,
		)
		# Mock Show to prevent window from being displayed during tests
		with patch.object(MagnifierFrame, "Show"):
			self.magnifier = WindowedMagnifier(windowMagnifierParams)

	def tearDown(self):
		"""Clean up after tests."""
		if self.magnifier and self.magnifier._frame:
			self.magnifier._frame.Destroy()

	def test_init(self):
		"""Test WindowedMagnifier initialization."""
		self.assertIsNotNone(self.magnifier.windowMagnifierParameters)
		self.assertIsNotNone(self.magnifier._frame)
		self.assertIsNotNone(self.magnifier._panel)
		self.assertIsInstance(self.magnifier._frame, MagnifierFrame)
		self.assertIsInstance(self.magnifier._panel, MagnifierPanel)
		self.assertEqual(self.magnifier._frame.frameType, "magnifier")
		self.assertEqual(self.magnifier._panel, self.magnifier._frame.panel)

	def test_applyColorFilter_normal(self):
		"""Test _applyColorFilter with NORMAL filter."""
		image = wx.Image(100, 100)
		image.SetRGB(wx.Rect(0, 0, 100, 100), 255, 0, 0)  # Red image

		result = self.magnifier._applyColorFilter(image, Filter.NORMAL)
		self.assertEqual(result, image)  # Should return same image

	def test_applyColorFilter_grayscale(self):
		"""Test _applyColorFilter with GRAYSCALE filter."""
		image = wx.Image(100, 100)
		image.SetRGB(wx.Rect(0, 0, 100, 100), 255, 0, 0)  # Red image

		result = self.magnifier._applyColorFilter(image, Filter.GRAYSCALE)
		self.assertIsNotNone(result)
		self.assertTrue(result.IsOk())
		# Check that the first pixel is grayscale (R=G=B)
		rgb = result.GetRed(0, 0), result.GetGreen(0, 0), result.GetBlue(0, 0)
		self.assertEqual(rgb[0], rgb[1])
		self.assertEqual(rgb[1], rgb[2])

	def test_applyColorFilter_inverted(self):
		"""Test _applyColorFilter with INVERTED filter."""
		image = wx.Image(100, 100)
		image.SetRGB(wx.Rect(0, 0, 100, 100), 255, 0, 0)  # Red image

		result = self.magnifier._applyColorFilter(image, Filter.INVERTED)
		self.assertIsNotNone(result)
		self.assertTrue(result.IsOk())
		# Check that colors are inverted (255-R, 255-G, 255-B)
		rgb = result.GetRed(0, 0), result.GetGreen(0, 0), result.GetBlue(0, 0)
		self.assertEqual(rgb[0], 0)  # 255-255 = 0
		self.assertEqual(rgb[1], 255)  # 255-0 = 255
		self.assertEqual(rgb[2], 255)  # 255-0 = 255

	def test_applyColorFilter_invalid_image(self):
		"""Test _applyColorFilter with invalid image."""
		image = wx.Image()  # Invalid/empty image
		result = self.magnifier._applyColorFilter(image, Filter.GRAYSCALE)
		self.assertEqual(result, image)  # Should return same invalid image

	def test_setContent(self):
		"""Test _setContent method."""
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(0, 0),
			filter=Filter.NORMAL,
		)

		# Mock _getContent to return a bitmap
		bitmap = wx.Bitmap(100, 100)
		with patch.object(self.magnifier, "_getContent", return_value=bitmap):
			self.magnifier._setContent(magnifierParams, 2.0)
			self.assertEqual(self.magnifier._panel.contentBitmap, bitmap)

	def test_setContent_no_panel(self):
		"""Test _setContent when panel is None."""
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(0, 0),
			filter=Filter.NORMAL,
		)

		# Set panel to None
		self.magnifier._panel = None

		# Should not raise error
		self.magnifier._setContent(magnifierParams, 2.0)

	def test_destroyWindow(self):
		"""Test _destroyWindow method."""
		self.assertIsNotNone(self.magnifier._frame)
		self.assertIsNotNone(self.magnifier._panel)

		self.magnifier._destroyWindow()

		self.assertIsNone(self.magnifier._frame)
		self.assertIsNone(self.magnifier._panel)

	def test_getContent(self):
		"""Test _getContent method."""
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(0, 0),
			filter=Filter.NORMAL,
		)

		result = self.magnifier._getContent(magnifierParams, 2.0)

		# Should return a bitmap or None
		if result is not None:
			self.assertIsInstance(result, wx.Bitmap)
			self.assertTrue(result.IsOk())

	def test_getContent_no_panel(self):
		"""Test _getContent when panel is None."""
		magnifierParams = MagnifierParameters(
			magnifierSize=Size(200, 150),
			coordinates=Coordinates(0, 0),
			filter=Filter.NORMAL,
		)

		# Set panel to None
		self.magnifier._panel = None

		result = self.magnifier._getContent(magnifierParams, 2.0)
		self.assertIsNone(result)
