# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest

from winAPI._displayTracking import (
	_getNewOrientationStyle,
	Orientation,
	OrientationState,
)


class Test_UpdateOrientationState(unittest.TestCase):

	def test_orientationChange_landscape(self):
		# Simulate a 90deg rotation
		# or a new monitor with a different orientation.
		newStyle = _getNewOrientationStyle(
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

	def test_orientationChange_portrait(self):
		# Simulate a 90deg rotation
		# or a new monitor with a different orientation.
		newStyle = _getNewOrientationStyle(
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

	def test_noChanges_screenFlip(self):
		# Test no changes in dimensions.
		# This represents a screen flip (180deg rotation),
		# and should be considered an orientation change.
		newStyle = _getNewOrientationStyle(
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

	def test_widthIncreaseLandscape(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=1,
				width=2,
				style=Orientation.LANDSCAPE,
			),
			height=1,
			width=3,
		)
		self.assertIsNone(newStyle)

	def test_widthIncreasePortrait(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=3,
				width=1,
				style=Orientation.PORTRAIT,
			),
			height=3,
			width=2,
		)
		self.assertIsNone(newStyle)

	def test_widthDecreaseLandscape(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=1,
				width=3,
				style=Orientation.LANDSCAPE,
			),
			height=1,
			width=2,
		)
		self.assertIsNone(newStyle)

	def test_widthDecreasePortrait(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=3,
				width=2,
				style=Orientation.PORTRAIT,
			),
			height=3,
			width=1,
		)
		self.assertIsNone(newStyle)

	def test_heightIncreaseLandscape(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=1,
				width=3,
				style=Orientation.LANDSCAPE,
			),
			height=2,
			width=3,
		)
		self.assertIsNone(newStyle)

	def test_heightIncreasePortrait(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=2,
				width=1,
				style=Orientation.PORTRAIT,
			),
			height=3,
			width=1,
		)
		self.assertIsNone(newStyle)

	def test_heightDecreaseLandscape(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=2,
				width=3,
				style=Orientation.LANDSCAPE,
			),
			height=1,
			width=3,
		)
		self.assertIsNone(newStyle)

	def test_heightDecreasePortrait(self):
		# simulate a display change, where the orientation doesn't update
		# this should not be considered a new orientation state
		newStyle = _getNewOrientationStyle(
			previousState=OrientationState(
				height=3,
				width=1,
				style=Orientation.PORTRAIT,
			),
			height=2,
			width=1,
		)
		self.assertIsNone(newStyle)
