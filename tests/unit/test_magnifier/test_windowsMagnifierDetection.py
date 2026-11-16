# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for refusing to start the full-screen magnifier while Windows Magnifier is running."""

from unittest.mock import patch

from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from _magnifier.utils.errorHandling import MagnifierStartError

from .test_magnifier import _TestMagnifier

# Captured before any test patches it.
_isWindowsMagnifierRunning = FullScreenMagnifier._isWindowsMagnifierRunning


class TestWindowsMagnifierDetection(_TestMagnifier):
	def setUp(self):
		super().setUp()
		self.fullscreen = FullScreenMagnifier()
		self.addCleanup(self._cleanUpFullscreen)
		self.mock_mag_fs.reset_mock()

	def _cleanUpFullscreen(self) -> None:
		if self.fullscreen._isActive:
			self.fullscreen._stopMagnifier()

	def test_windowsMagnifierRunning_refusesToStartWithoutTouchingTheApi(self):
		# The probe succeeds, as it does when Windows Magnifier is at 100%.
		self.mockIsWindowsMagnifierRunning.return_value = True
		with self.assertRaises(MagnifierStartError):
			self.fullscreen._startMagnifier()
		self.assertFalse(self.fullscreen._isActive)
		self.mock_mag_fs.MagInitialize.assert_not_called()
		self.mock_mag_fs.MagSetFullscreenTransform.assert_not_called()
		self.mock_mag_fs.MagSetFullscreenColorEffect.assert_not_called()
		self.MockMouseHook.assert_not_called()

	def test_windowsMagnifierNotRunning_starts(self):
		self.fullscreen._startMagnifier()
		self.assertTrue(self.fullscreen._isActive)
		self.mock_mag_fs.MagInitialize.assert_called()

	def test_alreadyActive_isNotCheckedAgain(self):
		self.fullscreen._startMagnifier()
		self.mockIsWindowsMagnifierRunning.reset_mock()
		self.fullscreen._startMagnifier()
		self.mockIsWindowsMagnifierRunning.assert_not_called()
		self.assertTrue(self.fullscreen._isActive)


class TestIsWindowsMagnifierRunning(_TestMagnifier):
	def setUp(self):
		super().setUp()
		patcher = patch("_magnifier.fullscreenMagnifier.user32.FindWindow")
		self.mockFindWindow = patcher.start()
		self.addCleanup(patcher.stop)

	def test_mainWindowFound_isRunning(self):
		self.mockFindWindow.return_value = 0x1234
		self.assertTrue(_isWindowsMagnifierRunning())
		self.mockFindWindow.assert_called_once_with("MagUIClass", None)

	def test_mainWindowNotFound_isNotRunning(self):
		self.mockFindWindow.return_value = None
		self.assertFalse(_isWindowsMagnifierRunning())
