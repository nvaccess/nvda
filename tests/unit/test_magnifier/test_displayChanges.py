# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the magnifier following display resolution and orientation changes."""

from unittest.mock import patch

from _magnifier.utils.types import Coordinates
from winAPI import _displayTracking
from winAPI._displayTracking import Orientation, OrientationState

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier


class TestDisplayChanges(_TestMagnifier):
	def setUp(self):
		super().setUp()
		patcher = patch("_magnifier.magnifier.isTrueCentered", return_value=False)
		patcher.start()
		self.addCleanup(patcher.stop)
		self.addCleanup(_displayTracking.displayChanged.unregister, self.magnifier._onDisplayChanged)

	def _notify(self, width: int, height: int) -> OrientationState:
		state = OrientationState(
			width,
			height,
			Orientation.LANDSCAPE if width > height else Orientation.PORTRAIT,
		)
		_displayTracking.displayChanged.notify(orientationState=state)
		return state

	def test_displayChange_updatesTheDisplayOrientation(self):
		self.magnifier._startMagnifier()
		self._notify(1280, 800)
		self.assertEqual(
			self.magnifier._displayOrientation,
			OrientationState(1280, 800, Orientation.LANDSCAPE),
		)

	def test_displayChange_keepsACopy(self):
		self.magnifier._startMagnifier()
		state = self._notify(1280, 800)
		state.width = 640
		self.assertEqual(self.magnifier._displayOrientation.width, 1280)

	def test_displayChange_appliesTheNewSizeToTheLimits(self):
		self.magnifier._startMagnifier()
		self._notify(1000, 600)
		# Zoom 200%: the visible area is half the screen, centred.
		self.assertEqual(self.magnifier._getScreenLimits(), (250, 150, 750, 450))

	def test_displayChange_clampsTheViewToTheNewSize(self):
		self.magnifier._startMagnifier()
		self.magnifier._displayOrientation = OrientationState(4000, 3000, Orientation.LANDSCAPE)
		self.magnifier.currentCoordinates = Coordinates(3000, 2000)
		self._notify(1000, 600)
		self.assertEqual(self.magnifier.currentCoordinates, Coordinates(750, 450))
