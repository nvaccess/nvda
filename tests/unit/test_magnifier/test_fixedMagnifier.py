# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest.mock import MagicMock, patch
from _magnifier.utils.types import (
	Coordinates,
	FixedWindowPosition,
)
from _magnifier.fixedMagnifier import FixedMagnifier
from _magnifier.utils.windowCreator import MagnifierFrame, WindowedMagnifier
import wx


class TestFixedMagnifier(unittest.TestCase):
	"""Tests for the FixedMagnifier class."""

	@classmethod
	def setUpClass(cls):
		"""Setup that runs once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""
		# Mock config functions to avoid dependencies
		with patch("_magnifier.fixedMagnifier.getDefaultFixedWindowWidth", return_value=400):
			with patch("_magnifier.fixedMagnifier.getDefaultFixedWindowHeight", return_value=300):
				with patch(
					"_magnifier.fixedMagnifier.getDefaultFixedWindowPosition",
					return_value=FixedWindowPosition.TOP_LEFT,
				):
					# Mock Show to prevent window from being displayed during tests
					with patch.object(MagnifierFrame, "Show"):
						self.magnifier = FixedMagnifier()

	def tearDown(self):
		"""Cleanup after each test."""
		if hasattr(self, "magnifier") and self.magnifier._frame:
			self.magnifier._frame.Destroy()

	def test_init(self):
		"""Test initialization of FixedMagnifier."""
		self.assertIsNotNone(self.magnifier._frame)
		self.assertIsNotNone(self.magnifier._panel)
		self.assertIsNotNone(self.magnifier._windowParameters)
		self.assertEqual(self.magnifier._currentCoordinates.x, 0)
		self.assertEqual(self.magnifier._currentCoordinates.y, 0)

	def test_startMagnifier(self):
		"""Test starting the FixedMagnifier."""
		with patch.object(self.magnifier, "_startTimer") as mock_timer:
			self.magnifier._startMagnifier()

			self.assertTrue(self.magnifier._isActive)
			mock_timer.assert_called_once()

	def test_doUpdate(self):
		"""Test the update magnifier functionality."""
		self.magnifier._currentCoordinates = Coordinates(100, 200)

		with patch.object(WindowedMagnifier, "_setContent") as mock_setContent:
			with patch.object(self.magnifier, "_getMagnifierParameters") as mock_getParams:
				mock_params = MagicMock()
				mock_getParams.return_value = mock_params

				self.magnifier._doUpdate()

				mock_getParams.assert_called_once_with(
					self.magnifier._currentCoordinates,
					self.magnifier._windowParameters.windowSize,
				)
				mock_setContent.assert_called_once_with(mock_params, self.magnifier.zoomLevel)

	def test_stopMagnifier(self):
		"""Test stopping the FixedMagnifier."""
		# Start magnifier first
		with patch.object(self.magnifier, "_startTimer"):
			self.magnifier._startMagnifier()

		self.assertTrue(self.magnifier._isActive)

		with patch.object(WindowedMagnifier, "_destroyWindow") as mock_destroy:
			self.magnifier._stopMagnifier()

			mock_destroy.assert_called_once()
			self.assertFalse(self.magnifier._isActive)

	def test_getWindowParameters(self):
		"""Test retrieving window parameters."""
		with patch("_magnifier.fixedMagnifier.getDefaultFixedWindowWidth", return_value=400):
			with patch("_magnifier.fixedMagnifier.getDefaultFixedWindowHeight", return_value=300):
				with patch(
					"_magnifier.fixedMagnifier.getDefaultFixedWindowPosition",
					return_value=FixedWindowPosition.TOP_LEFT,
				):
					params = self.magnifier._getWindowParameters()

					self.assertEqual(params.windowSize.width, 400)
					self.assertEqual(params.windowSize.height, 300)
					self.assertEqual(params.windowPosition.x, 0)
					self.assertEqual(params.windowPosition.y, 0)
					self.assertEqual(params.title, "NVDA Fixed Magnifier")
