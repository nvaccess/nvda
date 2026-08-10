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


class TestOnMouseMove(_TestMagnifier):
	"""Tests for FullScreenMagnifier._onMouseMove — the hook callback.

	_onMouseMove runs synchronously inside a global WH_MOUSE_LL hook chain (see
	utils/mouseHook.py), so it must never call into the Magnification API directly:
	doing so would delay delivery of the real WM_MOUSEMOVE to whatever window is
	under the cursor, for every mouse move on the system. It should only record
	the latest coordinates and defer the actual update to the main thread via
	wx.CallAfter (_applyPendingMousePosition).
	"""

	def testDoesNotUpdateMagnifierSynchronously(self):
		"""_onMouseMove must not touch the Magnification API from the hook thread."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._fullscreenMagnifier = MagicMock()

		with (
			patch("_magnifier.magnifier.getFollowState", return_value=True),
			patch("_magnifier.magnifier.wx.CallAfter"),
		):
			magnifier._onMouseMove(500, 400)

		magnifier._fullscreenMagnifier.assert_not_called()
		self.assertEqual(magnifier._pendingMouseCoordinates, Coordinates(500, 400))
		magnifier._stopMagnifier()

	def testSchedulesMainThreadUpdate(self):
		"""_onMouseMove schedules exactly one wx.CallAfter, even for bursts of moves."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()

		with (
			patch("_magnifier.magnifier.getFollowState", return_value=True),
			patch("_magnifier.magnifier.wx.CallAfter") as mockCallAfter,
		):
			magnifier._onMouseMove(500, 400)
			magnifier._onMouseMove(510, 410)
			magnifier._onMouseMove(520, 420)

		mockCallAfter.assert_called_once_with(magnifier._applyPendingMousePosition)
		self.assertEqual(magnifier._pendingMouseCoordinates, Coordinates(520, 420))
		magnifier._stopMagnifier()

	def testApplyPendingMousePositionUpdatesMagnifier(self):
		"""_applyPendingMousePosition (run on the main thread) performs the real update."""
		magnifier = FullScreenMagnifier()
		magnifier._startMagnifier()
		magnifier._fullscreenMagnifier = MagicMock()

		with (
			patch("_magnifier.magnifier.getFollowState", return_value=True),
			patch("_magnifier.magnifier.wx.CallAfter", side_effect=lambda func, *a, **kw: func(*a, **kw)),
		):
			magnifier._onMouseMove(500, 400)

		magnifier._fullscreenMagnifier.assert_called_once()
		self.assertEqual(magnifier.currentCoordinates, Coordinates(500, 400))
		self.assertFalse(magnifier._mouseUpdatePending)
		magnifier._stopMagnifier()
