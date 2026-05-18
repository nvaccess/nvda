# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest.mock import MagicMock, patch
from _magnifier.commands import zoom, cycleMagnifiedView
from _magnifier.utils.types import Direction, MagnifiedView


class TestZoomCommand(unittest.TestCase):
	"""Tests for the zoom command's handling of magnifier state."""

	def setUp(self):
		self.mockMessage = patch("_magnifier.commands.ui.message").start()
		self.mockGetMagnifier = patch("_magnifier.commands.getMagnifier").start()
		self.mockToggle = patch("_magnifier.commands.toggleMagnifier").start()

	def tearDown(self):
		patch.stopall()

	def _makeMockMagnifier(self, isActive: bool):
		magnifier = MagicMock()
		magnifier.configure_mock(**{"_isActive": isActive})
		magnifier.zoomLevel = 2.0
		return magnifier

	def testInactiveZoomIn(self):
		mag = self._makeMockMagnifier(isActive=False)
		self.mockGetMagnifier.return_value = mag
		zoom(Direction.IN)
		self.mockToggle.assert_called_once()
		mag._zoom.assert_not_called()

	@patch("_magnifier.commands.magnifierIsActiveVerify")
	def testInactiveZoomOut(self, mockVerify):
		self.mockGetMagnifier.return_value = self._makeMockMagnifier(isActive=False)
		zoom(Direction.OUT)
		self.mockToggle.assert_not_called()
		mockVerify.assert_called_once()

	def testActiveZoomIn(self):
		mag = self._makeMockMagnifier(isActive=True)
		self.mockGetMagnifier.return_value = mag
		zoom(Direction.IN)
		self.mockToggle.assert_not_called()
		mag._zoom.assert_called_once_with(Direction.IN)

	def testActiveZoomOut(self):
		mag = self._makeMockMagnifier(isActive=True)
		self.mockGetMagnifier.return_value = mag
		zoom(Direction.OUT)
		self.mockToggle.assert_not_called()
		mag._zoom.assert_called_once_with(Direction.OUT)


class TestCycleMagnifiedView(unittest.TestCase):
	"""Tests for cycleMagnifiedView command."""

	def setUp(self):
		self.mockMessage = patch("_magnifier.commands.ui.message").start()
		self.mockGetMagnifier = patch("_magnifier.commands.getMagnifier").start()
		self.mockChangeMagnifiedView = patch("_magnifier.commands.changeMagnifiedView").start()
		self.mockSetMagnifiedView = patch("_magnifier.commands.setMagnifiedView").start()

	def tearDown(self):
		patch.stopall()

	def _makeMockMagnifier(self, magnifiedView: MagnifiedView):
		magnifier = MagicMock()
		magnifier._isActive = True
		magnifier._MAGNIFIED_VIEW = magnifiedView
		return magnifier

	def testFullCycle(self):
		"""All four types cycle in order and wrap back to FULLSCREEN."""
		expectedCycle = [
			(MagnifiedView.FULLSCREEN, MagnifiedView.FIXED),
			(MagnifiedView.FIXED, MagnifiedView.DOCKED),
			(MagnifiedView.DOCKED, MagnifiedView.LENS),
			(MagnifiedView.LENS, MagnifiedView.FULLSCREEN),
		]
		for currentType, expectedNext in expectedCycle:
			with self.subTest(currentType=currentType):
				self.mockGetMagnifier.side_effect = [
					self._makeMockMagnifier(currentType),
					self._makeMockMagnifier(expectedNext),
				]
				cycleMagnifiedView()
				self.mockChangeMagnifiedView.assert_called_once_with(expectedNext)
				self.mockChangeMagnifiedView.reset_mock()
