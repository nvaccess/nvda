# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest

from winAPI import displayTracking
from winAPI.displayTracking import (
	_getNewOrientationState,
	Orientation,
	OrientationState,
)


class Test_UpdateOrientationState(unittest.TestCase):

	def test_landscapeInitiallySet(self):
		newStyle = _getNewOrientationState(
			previousState=OrientationState(),  # simulates initialization
			height=1,
			width=2,
		)
		self.assertEqual(
			newStyle,
			Orientation.LANDSCAPE
		)

	def test_portraitInitiallySet(self):
		newStyle = _getNewOrientationState(
			previousState=OrientationState(),  # simulates initialization
			height=2,
			width=1,
		)
		self.assertEqual(
			newStyle,
			Orientation.PORTRAIT
		)

	def test_orientationChange(self):
		# simulate a 90deg rotation
		newStyle = _getNewOrientationState(
			previousState=OrientationState(
				height=2,
				width=1,
				style=Orientation.PORTRAIT,
			),
			height=1,
			width=2,
		)
		self.assertEqual(
			newStyle,
			Orientation.LANDSCAPE
		)

	def test_screenFlip(self):
		# simulate a 180deg rotation
		newStyle = _getNewOrientationState(
			previousState=OrientationState(
				height=1,
				width=2,
				style=Orientation.LANDSCAPE,
			),
			height=1,
			width=2,
		)
		self.assertEqual(
			newStyle,
			Orientation.LANDSCAPE
		)

	def test_monitorChangeNoOrientationChange(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationState(
			previousState=OrientationState(
				height=1,
				width=2,
				style=Orientation.LANDSCAPE,
			),
			height=1,
			width=3,
		)
		self.assertIsNone(newStyle)

	def test_monitorChangeOrientationChange(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationState(
			previousState=OrientationState(
				height=1,
				width=2,
				style=Orientation.LANDSCAPE,
			),
			height=2,
			width=1,
		)
		self.assertEqual(
			newStyle,
			Orientation.PORTRAIT
		)

