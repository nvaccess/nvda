# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from dataclasses import dataclass
from _magnifier.utils.trackingManager import TrackingManager
from _magnifier.utils.types import Coordinates, MagnifierTrackingType
import unittest
from unittest.mock import MagicMock, Mock, patch
import _ctypes


def _makeFollowStateSideEffect(
	followMouse: bool = True,
	followSystemFocus: bool = True,
	followReview: bool = True,
	followNavigatorObject: bool = True,
):
	"""Return a side_effect function for patching getTrackingState."""
	states = {
		MagnifierTrackingType.MOUSE: followMouse,
		MagnifierTrackingType.SYSTEM_FOCUS: followSystemFocus,
		MagnifierTrackingType.REVIEW: followReview,
		MagnifierTrackingType.NAVIGATOR_OBJECT: followNavigatorObject,
	}
	return states.__getitem__


@dataclass(frozen=True)
class FocusTestParam:
	"""Parameters for focus coordinate testing."""

	navigatorObjectPos: Coordinates
	systemFocusPos: Coordinates
	mousePos: tuple
	leftPressed: bool
	expectedCoords: Coordinates
	expectedFocus: MagnifierTrackingType | None
	description: str = ""
	lastFocusedObject: MagnifierTrackingType | None = None
	reviewPos: Coordinates | None = None
	followMouse: bool = True
	followSystemFocus: bool = True
	followReview: bool = True
	followNavigatorObject: bool = True


class TestTrackingManager(unittest.TestCase):
	"""Tests for the TrackingManager class."""

	def setUp(self):
		"""Setup before each test."""
		self.trackingManager = TrackingManager()

	def testTrackingManagerCreation(self):
		"""Can we create a TrackingManager with initialized values?"""
		self.assertIsNone(self.trackingManager._lastTrackedObject)
		self.assertEqual(self.trackingManager._lastReportedCoordinates, Coordinates(0, 0))
		self.assertIsNone(self.trackingManager._lastReviewPosition)
		self.assertEqual(self.trackingManager._lastMousePosition, Coordinates(0, 0))
		self.assertEqual(self.trackingManager._lastSystemFocusPosition, Coordinates(0, 0))
		self.assertEqual(self.trackingManager._lastNavigatorObjectPosition, Coordinates(0, 0))
		self.assertEqual(self.trackingManager._lastValidSystemFocusPosition, Coordinates(0, 0))
		self.assertEqual(self.trackingManager._lastValidReviewPosition, Coordinates(0, 0))
		self.assertEqual(self.trackingManager._lastValidNavigatorObjectPosition, Coordinates(0, 0))

	def testGetNavigatorObjectPosition(self):
		"""Getting navigator object position with different API responses."""
		# Case 1: Navigator object location available
		with patch("_magnifier.utils.trackingManager.api.getNavigatorObject") as mock_navigator:
			mock_navigator.return_value.location = (100, 150, 200, 300)

			coords = self.trackingManager._getNavigatorObjectPosition()
			# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
			self.assertEqual(coords, Coordinates(200, 300))

		# Case 2: Navigator object fails - should return last valid position from Case 1
		with patch("_magnifier.utils.trackingManager.api.getNavigatorObject") as mock_navigator:
			mock_navigator.return_value.location = Mock(side_effect=Exception())

			coords = self.trackingManager._getNavigatorObjectPosition()
			# Should return last valid position (200, 300)
			self.assertEqual(coords, Coordinates(200, 300))

		# Case 3: Navigator object is None - should return last valid position
		with patch("_magnifier.utils.trackingManager.api.getNavigatorObject", return_value=None):
			coords = self.trackingManager._getNavigatorObjectPosition()
			self.assertEqual(coords, Coordinates(200, 300))

	def testGetReviewPosition(self):
		"""Getting review cursor position with different API responses."""
		# Case 1: Review position available
		with patch("_magnifier.utils.trackingManager.api.getReviewPosition") as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point

			coords = self.trackingManager._getReviewPosition()
			self.assertEqual(coords, Coordinates(300, 400))
			# _lastValidReviewPosition must be updated
			self.assertEqual(self.trackingManager._lastValidReviewPosition, Coordinates(300, 400))

		# Case 2: pointAtStart raises NotImplementedError → returns None
		with patch("_magnifier.utils.trackingManager.api.getReviewPosition") as mock_review:
			type(mock_review.return_value).pointAtStart = property(
				fget=Mock(side_effect=NotImplementedError),
			)

			coords = self.trackingManager._getReviewPosition()
			self.assertIsNone(coords)
			# _lastValidReviewPosition must NOT change
			self.assertEqual(self.trackingManager._lastValidReviewPosition, Coordinates(300, 400))

		# Case 3: getReviewPosition returns None → returns None
		with patch("_magnifier.utils.trackingManager.api.getReviewPosition", return_value=None):
			coords = self.trackingManager._getReviewPosition()
			self.assertIsNone(coords)

	def testGetReviewPositionSurvivesCOMError(self):
		"""_getReviewPosition catches COMError from pointAtStart."""

		comError = _ctypes.COMError(-2147418113, "Défaillance irrémédiable", None)
		mockReviewPos = Mock()
		type(mockReviewPos).pointAtStart = property(lambda self: (_ for _ in ()).throw(comError))

		with patch("_magnifier.utils.trackingManager.api.getReviewPosition", return_value=mockReviewPos):
			result = self.trackingManager._getReviewPosition()
			self.assertIsNone(result)

	def testGetSystemFocusPosition(self):
		"""Getting system focus position with different API responses."""
		# Case 1: Caret position successful (browse mode)
		with patch("_magnifier.utils.trackingManager.api.getCaretPosition") as mock_caret:
			mock_point = Mock()
			mock_point.x = 500
			mock_point.y = 600
			mock_caret.return_value.pointAtStart = mock_point

			coords = self.trackingManager._getSystemFocusPosition()
			self.assertEqual(coords, Coordinates(500, 600))

		# Case 2: Caret fails, focus object works
		with patch("_magnifier.utils.trackingManager.api.getCaretPosition", side_effect=RuntimeError):
			with patch("_magnifier.utils.trackingManager.api.getFocusObject") as mock_focus:
				mock_focus.return_value.location = (200, 300, 100, 80)

				coords = self.trackingManager._getSystemFocusPosition()
				# Center: (200 + 100//2, 300 + 80//2) = (250, 340)
				self.assertEqual(coords, Coordinates(250, 340))

		# Case 3: Everything fails - should return last valid position from Case 2
		with patch("_magnifier.utils.trackingManager.api.getCaretPosition", side_effect=RuntimeError):
			with patch("_magnifier.utils.trackingManager.api.getFocusObject", return_value=None):
				coords = self.trackingManager._getSystemFocusPosition()
				# Should return last valid position (250, 340)
				self.assertEqual(coords, Coordinates(250, 340))

	def testGetSystemFocusPositionSurvivesOSError(self):
		"""OSError from magnification API calls must be caught."""
		with patch(
			"_magnifier.utils.trackingManager.api.getCaretPosition",
			side_effect=OSError("WinError"),
		):
			with patch("_magnifier.utils.trackingManager.api.getFocusObject") as mock_focus:
				mock_focus.return_value.location = (10, 20, 30, 40)

				coords = self.trackingManager._getSystemFocusPosition()
				self.assertEqual(coords, Coordinates(25, 40))

	def testGetMousePosition(self):
		"""Getting mouse position."""
		with patch("_magnifier.utils.trackingManager.winUser.getCursorPos", return_value=(123, 456)):
			coords = self.trackingManager._getMousePosition()
			self.assertEqual(coords, Coordinates(123, 456))

	def testGetCurrentFocusCoordinates(self):
		"""All priority scenarios for focus coordinates."""
		subTestParams = [
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=Coordinates(0, 0),
				leftPressed=True,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=MagnifierTrackingType.MOUSE,
				description="Left click is pressed should return mouse position",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=Coordinates(10, 10),
				leftPressed=False,
				expectedCoords=Coordinates(10, 10),
				expectedFocus=MagnifierTrackingType.MOUSE,
				description="Mouse moving (not dragging)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(15, 15),
				mousePos=Coordinates(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(15, 15),
				expectedFocus=MagnifierTrackingType.SYSTEM_FOCUS,
				description="System focus changed alone (navigator did not move)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(20, 20),
				systemFocusPos=Coordinates(0, 0),
				mousePos=Coordinates(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierTrackingType.NAVIGATOR_OBJECT,
				description="Navigator object changed (NumPad navigation)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(30, 30),
				systemFocusPos=Coordinates(15, 15),
				mousePos=Coordinates(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierTrackingType.NAVIGATOR_OBJECT,
				description="Both system focus and navigator changed (table cell navigation): navigator wins",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=Coordinates(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierTrackingType.REVIEW,
				description="Review cursor changed with followReview enabled",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(20, 20),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierTrackingType.REVIEW,
				description="Review has higher priority than navigator",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(20, 20),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				followReview=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierTrackingType.NAVIGATOR_OBJECT,
				description="Review cursor ignored when followReview=False",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=Coordinates(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=MagnifierTrackingType.MOUSE,
				description="Nothing changed, last was Mouse",
				lastFocusedObject=MagnifierTrackingType.MOUSE,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=MagnifierTrackingType.NAVIGATOR_OBJECT,
				description="Nothing changed, last was NAVIGATOR",
				lastFocusedObject=MagnifierTrackingType.NAVIGATOR_OBJECT,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierTrackingType.REVIEW,
				description="Nothing changed, last was REVIEW - returns current review position",
				lastFocusedObject=MagnifierTrackingType.REVIEW,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(10, 10),
				systemFocusPos=Coordinates(0, 0),
				mousePos=Coordinates(20, 20),
				leftPressed=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierTrackingType.MOUSE,
				description="Both mouse and navigator object moved (mouse has priority)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(10, 10),
				systemFocusPos=Coordinates(15, 15),
				mousePos=Coordinates(20, 20),
				leftPressed=True,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierTrackingType.MOUSE,
				description="All three moved while dragging (mouse drag has highest priority)",
			),
		]

		for param in subTestParams:
			with self.subTest(description=param.description):
				# Reset focus manager state
				self.trackingManager._lastNavigatorObjectPosition = Coordinates(0, 0)
				self.trackingManager._lastSystemFocusPosition = Coordinates(0, 0)
				self.trackingManager._lastMousePosition = Coordinates(0, 0)
				self.trackingManager._lastReviewPosition = None
				self.trackingManager._lastSystemFocusChangeTime = 0.0
				self.trackingManager._lastTrackedObject = param.lastFocusedObject

				# Mock instance methods
				self.trackingManager._getNavigatorObjectPosition = MagicMock(
					return_value=param.navigatorObjectPos,
				)
				self.trackingManager._getSystemFocusPosition = MagicMock(return_value=param.systemFocusPos)
				self.trackingManager._getReviewPosition = MagicMock(return_value=param.reviewPos)

				followStateSideEffect = _makeFollowStateSideEffect(
					followMouse=param.followMouse,
					followSystemFocus=param.followSystemFocus,
					followReview=param.followReview,
					followNavigatorObject=param.followNavigatorObject,
				)

				with (
					patch(
						"_magnifier.utils.trackingManager.getTrackingState",
						side_effect=followStateSideEffect,
					),
					patch(
						"_magnifier.utils.trackingManager.winUser.getAsyncKeyState",
						side_effect=lambda _key: -1 if param.leftPressed else 0,
					),
					patch(
						"_magnifier.utils.trackingManager.winUser.getCursorPos",
						return_value=param.mousePos,
					),
				):
					# Execute
					focusCoordinates = self.trackingManager.getCurrentTrackedCoordinates()

				# Assert
				self.assertEqual(focusCoordinates, param.expectedCoords)
				self.assertEqual(self.trackingManager.getLastTrackedType(), param.expectedFocus)

	def testGetLastFocusType(self):
		"""Test getting the last focus type."""
		self.assertIsNone(self.trackingManager.getLastTrackedType())

		for focusType in MagnifierTrackingType:
			self.trackingManager._lastTrackedObject = focusType
			self.assertEqual(self.trackingManager.getLastTrackedType(), focusType)


class TestFollowSettings(unittest.TestCase):
	"""Verify that each follow* setting actually gates its source."""

	def setUp(self):
		self.trackingManager = TrackingManager()
		self.trackingManager._lastMousePosition = Coordinates(0, 0)
		self.trackingManager._lastSystemFocusPosition = Coordinates(0, 0)
		self.trackingManager._lastReviewPosition = None
		self.trackingManager._lastNavigatorObjectPosition = Coordinates(0, 0)

	def _run(self, *, followMouse, followSystemFocus, followReview, followNavigatorObject):
		"""Run getCurrentTrackedCoordinates with all sources moved and the given settings."""
		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.trackingManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=followMouse,
			followSystemFocus=followSystemFocus,
			followReview=followReview,
			followNavigatorObject=followNavigatorObject,
		)

		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followStateSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=0),
		):
			return self.trackingManager.getCurrentTrackedCoordinates()

	def testFollowMouseDisabled(self):
		"""When followMouse=False, mouse changes are ignored and system focus wins."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)
		self.assertEqual(coords, Coordinates(20, 20))
		self.assertEqual(self.trackingManager.getLastTrackedType(), MagnifierTrackingType.SYSTEM_FOCUS)

	def testFollowSystemFocusDisabled(self):
		"""When followSystemFocus=False, system focus changes are ignored and review wins."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=False,
			followReview=True,
			followNavigatorObject=True,
		)
		self.assertEqual(coords, Coordinates(30, 30))
		self.assertEqual(self.trackingManager.getLastTrackedType(), MagnifierTrackingType.REVIEW)

	def testFollowReviewDisabled(self):
		"""When followReview=False, review changes are ignored and navigator wins."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=False,
			followReview=False,
			followNavigatorObject=True,
		)
		self.assertEqual(coords, Coordinates(40, 40))
		self.assertEqual(self.trackingManager.getLastTrackedType(), MagnifierTrackingType.NAVIGATOR_OBJECT)

	def testAllFollowDisabled(self):
		"""When all settings are False, no source fires and focus remains frozen."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=False,
			followReview=False,
			followNavigatorObject=False,
		)
		# No previous focus -> freeze at initial tracked coordinates.
		self.assertEqual(coords, Coordinates(0, 0))

	def testAllFollowDisabledKeepsLastTrackedPosition(self):
		"""Disabling all follow modes keeps the most recently tracked coordinates."""
		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.trackingManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))

		followEnabledSideEffect = _makeFollowStateSideEffect(
			followMouse=True,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)
		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followEnabledSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=0),
		):
			coords = self.trackingManager.getCurrentTrackedCoordinates()
		self.assertEqual(coords, Coordinates(10, 10))

		# Move all sources, but disable every follow setting.
		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(99, 99))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(88, 88))
		self.trackingManager._getReviewPosition = MagicMock(return_value=Coordinates(77, 77))
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(66, 66))
		followDisabledSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=False,
			followReview=False,
			followNavigatorObject=False,
		)
		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followDisabledSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=0),
		):
			coords = self.trackingManager.getCurrentTrackedCoordinates()

		self.assertEqual(coords, Coordinates(10, 10))
		self.assertIsNone(self.trackingManager.getLastTrackedType())

	def testFollowMouseDragIgnoresSettings(self):
		"""Mouse drag (left click held) with followMouse=True always wins regardless of others."""
		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.trackingManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=True,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)

		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followStateSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=-1),
		):
			coords = self.trackingManager.getCurrentTrackedCoordinates()

		self.assertEqual(coords, Coordinates(10, 10))
		self.assertEqual(self.trackingManager.getLastTrackedType(), MagnifierTrackingType.MOUSE)

	def testDisableFollowMouseKeepsViewFrozen(self):
		"""When followMouse is disabled, view remains frozen until a followed source changes."""
		# Simulate: mouse was previously the active focus source
		self.trackingManager._lastTrackedObject = MagnifierTrackingType.MOUSE
		self.trackingManager._lastReportedCoordinates = Coordinates(10, 10)
		# Positions haven't changed from last recorded values (no "change" detected)
		self.trackingManager._lastMousePosition = Coordinates(10, 10)
		self.trackingManager._lastSystemFocusPosition = Coordinates(20, 20)
		self.trackingManager._lastNavigatorObjectPosition = Coordinates(40, 40)

		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.trackingManager._getReviewPosition = MagicMock(return_value=None)
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)

		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followStateSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=0),
		):
			coords = self.trackingManager.getCurrentTrackedCoordinates()

		self.assertEqual(coords, Coordinates(10, 10))
		self.assertIsNone(self.trackingManager.getLastTrackedType())

	def testDisableFollowMouseWhileMouseMovingKeepsViewFrozen(self):
		"""When followMouse is disabled, mouse movement alone does not move the view."""
		self.trackingManager._lastTrackedObject = MagnifierTrackingType.MOUSE
		self.trackingManager._lastReportedCoordinates = Coordinates(10, 10)
		self.trackingManager._lastMousePosition = Coordinates(10, 10)
		self.trackingManager._lastSystemFocusPosition = Coordinates(20, 20)
		self.trackingManager._lastNavigatorObjectPosition = Coordinates(40, 40)

		# Mouse has moved but followMouse is False
		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(15, 15))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.trackingManager._getReviewPosition = MagicMock(return_value=None)
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)

		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followStateSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=0),
		):
			coords = self.trackingManager.getCurrentTrackedCoordinates()

		self.assertEqual(coords, Coordinates(10, 10))
		self.assertIsNone(self.trackingManager.getLastTrackedType())

	def testDisableFollowSystemFocusKeepsViewFrozen(self):
		"""When followSystemFocus is disabled, view remains frozen until a followed source changes."""
		self.trackingManager._lastTrackedObject = MagnifierTrackingType.SYSTEM_FOCUS
		self.trackingManager._lastReportedCoordinates = Coordinates(20, 20)
		self.trackingManager._lastMousePosition = Coordinates(10, 10)
		self.trackingManager._lastSystemFocusPosition = Coordinates(20, 20)
		self.trackingManager._lastReviewPosition = Coordinates(30, 30)
		self.trackingManager._lastNavigatorObjectPosition = Coordinates(40, 40)

		self.trackingManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.trackingManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.trackingManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.trackingManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=False,
			followReview=True,
			followNavigatorObject=True,
		)

		with (
			patch(
				"_magnifier.utils.trackingManager.getTrackingState",
				side_effect=followStateSideEffect,
			),
			patch("_magnifier.utils.trackingManager.winUser.getAsyncKeyState", return_value=0),
		):
			coords = self.trackingManager.getCurrentTrackedCoordinates()

		self.assertEqual(coords, Coordinates(20, 20))
		self.assertIsNone(self.trackingManager.getLastTrackedType())
