# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest.mock import MagicMock, patch
from _magnifier.commands import zoom, cycleMagnifiedView, moveMouseToView, toggleMagnifier
from _magnifier.utils.errorHandling import MagnifierStartError
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
		magnifier.zoomLevel = 200
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


class TestToggleMagnifier(unittest.TestCase):
	"""Tests for toggleMagnifier's handling of start success and failure."""

	def setUp(self):
		self.mockMessage = patch("_magnifier.commands.ui.message").start()
		self.mockGetMagnifier = patch("_magnifier.commands.getMagnifier").start()
		self.mockStart = patch("_magnifier.commands.start").start()
		self.mockStop = patch("_magnifier.commands.stop").start()

	def tearDown(self):
		patch.stopall()

	def testStartSuccessAnnouncesEnabled(self):
		"""A successful start announces the magnifier is enabled and does not call onStartError."""
		self.mockGetMagnifier.return_value = None
		onStartError = MagicMock()

		toggleMagnifier(onStartError=onStartError)

		self.mockStart.assert_called_once()
		onStartError.assert_not_called()
		self.mockMessage.assert_called_once()

	def testStartFailurePresentsErrorAndNoSuccessMessage(self):
		"""When start fails, the failure is presented and success is NOT announced."""
		self.mockGetMagnifier.return_value = None
		self.mockStart.side_effect = MagnifierStartError("boom")
		onStartError = MagicMock()

		toggleMagnifier(onStartError=onStartError)

		onStartError.assert_called_once_with("boom")
		# The success message must not be spoken when the magnifier failed to start.
		self.mockMessage.assert_not_called()

	def testDefaultStartErrorIsSpoken(self):
		"""The default error presentation speaks the message via ui.message."""
		self.mockGetMagnifier.return_value = None
		self.mockStart.side_effect = MagnifierStartError("boom")

		toggleMagnifier()

		# ui.message is used to speak the error, and only the error (no success message).
		self.mockMessage.assert_called_once()
		self.assertEqual(self.mockMessage.call_args.args[0], "boom")

	def testActiveMagnifierIsStopped(self):
		"""Toggling while active stops the magnifier and announces it, without starting."""
		magnifier = MagicMock()
		magnifier._isActive = True
		self.mockGetMagnifier.return_value = magnifier

		toggleMagnifier()

		self.mockStop.assert_called_once()
		self.mockStart.assert_not_called()
		self.mockMessage.assert_called_once()


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


class TestMoveMouseToView(unittest.TestCase):
	"""Tests for the moveMouseToView command."""

	def setUp(self):
		self.mockMessage = patch("_magnifier.commands.ui.message").start()
		self.mockGetMagnifier = patch("_magnifier.commands.getMagnifier").start()

	def tearDown(self):
		patch.stopall()

	def _makeMockMagnifier(self, isActive: bool):
		magnifier = MagicMock()
		magnifier._isActive = isActive
		return magnifier

	def testInactiveMagnifier(self):
		"""moveMouseToViewCenter is not called and a message is emitted when magnifier is inactive."""
		mag = self._makeMockMagnifier(isActive=False)
		self.mockGetMagnifier.return_value = mag
		moveMouseToView()
		mag.moveMouseToViewCenter.assert_not_called()
		self.mockMessage.assert_called_once()

	def testActiveMagnifier(self):
		"""moveMouseToViewCenter is called when magnifier is active."""
		mag = self._makeMockMagnifier(isActive=True)
		self.mockGetMagnifier.return_value = mag
		moveMouseToView()
		mag.moveMouseToViewCenter.assert_called_once()
