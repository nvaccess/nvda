# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from unittest.mock import MagicMock, patch
from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from _magnifier.utils.types import Coordinates
from tests.unit.test_magnifier.test_magnifier import _TestMagnifier


class TestMouseHookLifecycle(_TestMagnifier):
	"""Tests for the WH_MOUSE_LL hook lifecycle managed by the base Magnifier class."""

	def testHookStartedWithMagnifier(self):
		"""Mouse hook is started when the magnifier starts."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		self.MockMouseHook.assert_called_once_with(magnifier._onMouseMove)
		self.mock_hook_instance.start.assert_called_once()

		magnifier._stopMagnifier()

	def testHookStoppedWithMagnifier(self):
		"""Mouse hook is stopped and cleared when the magnifier stops."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._stopMagnifier()

		self.mock_hook_instance.stop.assert_called_once()
		self.assertIsNone(magnifier._mouseHook)

	def testHookNotStartedIfAlreadyActive(self):
		"""Calling _startMagnifier twice does not create a second hook."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._startMagnifier()

		self.assertEqual(self.MockMouseHook.call_count, 1)

		magnifier._stopMagnifier()

	def testHookNotStartedIfInitFails(self):
		"""Hook is not left running when API initialisation fails."""
		self.mock_mag_fs.MagInitialize.side_effect = OSError("init failed")

		with patch("_magnifier.fullscreenMagnifier.ui.message"):
			magnifier = FullScreenMagnifier()
			magnifier._startMagnifier()

		self.mock_hook_instance.stop.assert_called_once()
		self.assertIsNone(magnifier._mouseHook)


class TestOnMouseMove(_TestMagnifier):
	"""Tests for FullScreenMagnifier._onMouseMove — the hook callback."""

	def testIgnoredWhenInactive(self):
		"""_onMouseMove does nothing when magnifier is not active."""
		magnifier = FullScreenMagnifier()
		magnifier._fullscreenMagnifier = MagicMock()
		magnifier._isActive = False

		magnifier._onMouseMove(500, 400)

		magnifier._fullscreenMagnifier.assert_not_called()

	def testIgnoredDuringManualPan(self):
		"""_onMouseMove does nothing while the user is manually panning."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._fullscreenMagnifier = MagicMock()
		magnifier._isManualPanning = True

		magnifier._onMouseMove(500, 400)

		magnifier._fullscreenMagnifier.assert_not_called()
		magnifier._stopMagnifier()

	def testIgnoredWhenMouseFollowDisabled(self):
		"""_onMouseMove does nothing when follow-mouse is off."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._fullscreenMagnifier = MagicMock()

		with patch("_magnifier.magnifier.getFollowState", return_value=False):
			magnifier._onMouseMove(500, 400)

		magnifier._fullscreenMagnifier.assert_not_called()
		magnifier._stopMagnifier()

	def testUpdatesMagnifier(self):
		"""_onMouseMove calls _fullscreenMagnifier when all conditions are met."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._fullscreenMagnifier = MagicMock()

		with patch("_magnifier.magnifier.getFollowState", return_value=True):
			magnifier._onMouseMove(500, 400)

		magnifier._fullscreenMagnifier.assert_called_once()
		magnifier._stopMagnifier()

	def testSilencesOSError(self):
		"""_onMouseMove swallows OSError from the magnification API."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._fullscreenMagnifier = MagicMock(side_effect=OSError("API failure"))

		with patch("_magnifier.magnifier.getFollowState", return_value=True):
			magnifier._onMouseMove(500, 400)  # must not raise

		magnifier._stopMagnifier()
