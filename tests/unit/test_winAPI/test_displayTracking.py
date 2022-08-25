# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest

from winAPI import displayTracking
from winAPI.displayTracking import (
	_updateOrientationState,
	Orientation,
	OrientationState,
)


class Test_UpdateOrientationState(unittest.TestCase):
	def setUp(self) -> None:
		displayTracking._orientationState = OrientationState()

	def tearDown(self) -> None:
		displayTracking._orientationState = OrientationState()

	def test_landscapeInitiallySet(self):
		monitorSet = _updateOrientationState(1, 2)
		self.assertTrue(monitorSet)
		self.assertEqual(
			displayTracking._orientationState.style,
			Orientation.LANDSCAPE
		)

	def test_portraitInitiallySet(self):
		monitorSet = _updateOrientationState(2, 1)
		self.assertTrue(monitorSet)
		self.assertEqual(
			displayTracking._orientationState.style,
			Orientation.PORTRAIT
		)

	def test_orientationChange(self):
		monitorSet = _updateOrientationState(2, 1)
		self.assertTrue(monitorSet)
		self.assertEqual(
			displayTracking._orientationState.style,
			Orientation.PORTRAIT
		)

		# simulate a 90deg rotation
		monitorSet = _updateOrientationState(1, 2)
		self.assertTrue(monitorSet)
		self.assertEqual(
			displayTracking._orientationState.style,
			Orientation.LANDSCAPE
		)

	def test_screenFlip(self):
		monitorSet = _updateOrientationState(1, 2)
		self.assertTrue(monitorSet)
		self.assertEqual(
			displayTracking._orientationState.style,
			Orientation.LANDSCAPE
		)

		# no change of orientation indicates a screen flip (180deg rotation)
		monitorSet = _updateOrientationState(1, 2)
		self.assertTrue(monitorSet)
		self.assertEqual(
			displayTracking._orientationState.style,
			Orientation.LANDSCAPE
		)

	def test_monitorChangeNoOrientationChange(self):
		landscapeMonitorSet = _updateOrientationState(1, 2)
		self.assertTrue(landscapeMonitorSet)
		changeToOtherLandscapeMonitorChangedState = _updateOrientationState(1, 3)
		self.assertFalse(changeToOtherLandscapeMonitorChangedState)

	def test_monitorChangeOrientationChange(self):
		landscapeMonitorSet = _updateOrientationState(1, 2)
		self.assertTrue(landscapeMonitorSet)
		changeToOtherLandscapeMonitorChangedState = _updateOrientationState(2, 1)
		self.assertTrue(changeToOtherLandscapeMonitorChangedState)

