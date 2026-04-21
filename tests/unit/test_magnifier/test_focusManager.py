# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from dataclasses import dataclass
from _magnifier.utils.focusManager import FocusManager
from _magnifier.utils.types import Coordinates, MagnifierFollowFocusType
import unittest
from unittest.mock import MagicMock, Mock, patch
import mouseHandler
import winUser


def _makeFollowStateSideEffect(
	followMouse: bool = True,
	followSystemFocus: bool = True,
	followReview: bool = True,
	followNavigatorObject: bool = True,
):
	"""Return a side_effect function for patching getFollowState."""
	states = {
		MagnifierFollowFocusType.MOUSE: followMouse,
		MagnifierFollowFocusType.SYSTEM_FOCUS: followSystemFocus,
		MagnifierFollowFocusType.REVIEW: followReview,
		MagnifierFollowFocusType.NAVIGATOR_OBJECT: followNavigatorObject,
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
	expectedFocus: MagnifierFollowFocusType | None
	description: str = ""
	lastFocusedObject: MagnifierFollowFocusType | None = None
	reviewPos: Coordinates | None = None
	followMouse: bool = True
	followSystemFocus: bool = True
	followReview: bool = True
	followNavigatorObject: bool = True


class TestFocusManager(unittest.TestCase):
	"""Tests for the FocusManager class."""

	def setUp(self):
		"""Setup before each test."""
		self.focusManager = FocusManager()

	def testFocusManagerCreation(self):
		"""Can we create a FocusManager with initialized values?"""
		self.assertIsNone(self.focusManager._lastFocusedObject)
		self.assertIsNone(self.focusManager._lastReviewPosition)
		self.assertEqual(self.focusManager._lastMousePosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastSystemFocusPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastNavigatorObjectPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastValidSystemFocusPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastValidReviewPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastValidNavigatorObjectPosition, Coordinates(0, 0))

	def testGetNavigatorObjectPosition(self):
		"""Getting navigator object position with different API responses."""
		# Case 1: Navigator object location available
		with patch("_magnifier.utils.focusManager.api.getNavigatorObject") as mock_navigator:
			mock_navigator.return_value.location = (100, 150, 200, 300)

			coords = self.focusManager._getNavigatorObjectPosition()
			# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
			self.assertEqual(coords, Coordinates(200, 300))

		# Case 2: Navigator object fails - should return last valid position from Case 1
		with patch("_magnifier.utils.focusManager.api.getNavigatorObject") as mock_navigator:
			mock_navigator.return_value.location = Mock(side_effect=Exception())

			coords = self.focusManager._getNavigatorObjectPosition()
			# Should return last valid position (200, 300)
			self.assertEqual(coords, Coordinates(200, 300))

		# Case 3: Navigator object is None - should return last valid position
		with patch("_magnifier.utils.focusManager.api.getNavigatorObject", return_value=None):
			coords = self.focusManager._getNavigatorObjectPosition()
			self.assertEqual(coords, Coordinates(200, 300))

	def testGetReviewPosition(self):
		"""Getting review cursor position with different API responses."""
		# Case 1: Review position available
		with patch("_magnifier.utils.focusManager.api.getReviewPosition") as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point

			coords = self.focusManager._getReviewPosition()
			self.assertEqual(coords, Coordinates(300, 400))
			# _lastValidReviewPosition must be updated
			self.assertEqual(self.focusManager._lastValidReviewPosition, Coordinates(300, 400))

		# Case 2: pointAtStart raises NotImplementedError → returns None
		with patch("_magnifier.utils.focusManager.api.getReviewPosition") as mock_review:
			type(mock_review.return_value).pointAtStart = property(
				fget=Mock(side_effect=NotImplementedError),
			)

			coords = self.focusManager._getReviewPosition()
			self.assertIsNone(coords)
			# _lastValidReviewPosition must NOT change
			self.assertEqual(self.focusManager._lastValidReviewPosition, Coordinates(300, 400))

		# Case 3: getReviewPosition returns None → returns None
		with patch("_magnifier.utils.focusManager.api.getReviewPosition", return_value=None):
			coords = self.focusManager._getReviewPosition()
			self.assertIsNone(coords)

	def testGetSystemFocusPosition(self):
		"""Getting system focus position with different API responses."""
		# Case 1: Caret position successful (browse mode)
		with patch("_magnifier.utils.focusManager.api.getCaretPosition") as mock_caret:
			mock_point = Mock()
			mock_point.x = 500
			mock_point.y = 600
			mock_caret.return_value.pointAtStart = mock_point

			coords = self.focusManager._getSystemFocusPosition()
			self.assertEqual(coords, Coordinates(500, 600))

		# Case 2: Caret fails, focus object works
		with patch("_magnifier.utils.focusManager.api.getCaretPosition", side_effect=RuntimeError):
			with patch("_magnifier.utils.focusManager.api.getFocusObject") as mock_focus:
				mock_focus.return_value.location = (200, 300, 100, 80)

				coords = self.focusManager._getSystemFocusPosition()
				# Center: (200 + 100//2, 300 + 80//2) = (250, 340)
				self.assertEqual(coords, Coordinates(250, 340))

		# Case 3: Everything fails - should return last valid position from Case 2
		with patch("_magnifier.utils.focusManager.api.getCaretPosition", side_effect=RuntimeError):
			with patch("_magnifier.utils.focusManager.api.getFocusObject", return_value=None):
				coords = self.focusManager._getSystemFocusPosition()
				# Should return last valid position (250, 340)
				self.assertEqual(coords, Coordinates(250, 340))

	def testGetMousePosition(self):
		"""Getting mouse position."""
		with patch("_magnifier.utils.focusManager.winUser.getCursorPos", return_value=(123, 456)):
			coords = self.focusManager._getMousePosition()
			self.assertEqual(coords, Coordinates(123, 456))

	def testGetCurrentFocusCoordinates(self):
		"""All priority scenarios for focus coordinates."""
		subTestParams = [
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=True,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=MagnifierFollowFocusType.MOUSE,
				description="Left click is pressed should return mouse position",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(10, 10),
				leftPressed=False,
				expectedCoords=Coordinates(10, 10),
				expectedFocus=MagnifierFollowFocusType.MOUSE,
				description="Mouse moving (not dragging)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(15, 15),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(15, 15),
				expectedFocus=MagnifierFollowFocusType.SYSTEM_FOCUS,
				description="System focus changed alone (navigator did not move)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(20, 20),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierFollowFocusType.NAVIGATOR_OBJECT,
				description="Navigator object changed (NumPad navigation)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(30, 30),
				systemFocusPos=Coordinates(15, 15),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierFollowFocusType.NAVIGATOR_OBJECT,
				description="Both system focus and navigator changed (table cell navigation): navigator wins",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierFollowFocusType.REVIEW,
				description="Review cursor changed with followReview enabled",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(20, 20),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierFollowFocusType.REVIEW,
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
				expectedFocus=MagnifierFollowFocusType.NAVIGATOR_OBJECT,
				description="Review cursor ignored when followReview=False",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=MagnifierFollowFocusType.MOUSE,
				description="Nothing changed, last was Mouse",
				lastFocusedObject=MagnifierFollowFocusType.MOUSE,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=MagnifierFollowFocusType.NAVIGATOR_OBJECT,
				description="Nothing changed, last was NAVIGATOR",
				lastFocusedObject=MagnifierFollowFocusType.NAVIGATOR_OBJECT,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				reviewPos=Coordinates(30, 30),
				expectedCoords=Coordinates(30, 30),
				expectedFocus=MagnifierFollowFocusType.REVIEW,
				description="Nothing changed, last was REVIEW - returns current review position",
				lastFocusedObject=MagnifierFollowFocusType.REVIEW,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(10, 10),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(20, 20),
				leftPressed=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierFollowFocusType.MOUSE,
				description="Both mouse and navigator object moved (mouse has priority)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(10, 10),
				systemFocusPos=Coordinates(15, 15),
				mousePos=(20, 20),
				leftPressed=True,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=MagnifierFollowFocusType.MOUSE,
				description="All three moved while dragging (mouse drag has highest priority)",
			),
		]

		for param in subTestParams:
			with self.subTest(description=param.description):
				# Reset focus manager state
				self.focusManager._lastNavigatorObjectPosition = Coordinates(0, 0)
				self.focusManager._lastSystemFocusPosition = Coordinates(0, 0)
				self.focusManager._lastMousePosition = Coordinates(0, 0)
				self.focusManager._lastReviewPosition = None
				self.focusManager._lastSystemFocusChangeTime = 0.0
				self.focusManager._lastFocusedObject = param.lastFocusedObject

				# Mock instance methods
				self.focusManager._getNavigatorObjectPosition = MagicMock(
					return_value=param.navigatorObjectPos,
				)
				self.focusManager._getSystemFocusPosition = MagicMock(return_value=param.systemFocusPos)
				self.focusManager._getReviewPosition = MagicMock(return_value=param.reviewPos)
				mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=param.leftPressed)
				winUser.getCursorPos = MagicMock(return_value=param.mousePos)

				followStateSideEffect = _makeFollowStateSideEffect(
					followMouse=param.followMouse,
					followSystemFocus=param.followSystemFocus,
					followReview=param.followReview,
					followNavigatorObject=param.followNavigatorObject,
				)

				with patch(
					"_magnifier.utils.focusManager.getFollowState",
					side_effect=followStateSideEffect,
				):
					# Execute
					focusCoordinates = self.focusManager.getCurrentFocusCoordinates()

				# Assert
				self.assertEqual(focusCoordinates, param.expectedCoords)
				self.assertEqual(self.focusManager.getLastFocusType(), param.expectedFocus)

	def testGetLastFocusType(self):
		"""Test getting the last focus type."""
		self.assertIsNone(self.focusManager.getLastFocusType())

		for focusType in MagnifierFollowFocusType:
			self.focusManager._lastFocusedObject = focusType
			self.assertEqual(self.focusManager.getLastFocusType(), focusType)


class TestFollowSettings(unittest.TestCase):
	"""Verify that each follow* setting actually gates its source."""

	def setUp(self):
		self.focusManager = FocusManager()
		self.focusManager._lastMousePosition = Coordinates(0, 0)
		self.focusManager._lastSystemFocusPosition = Coordinates(0, 0)
		self.focusManager._lastReviewPosition = None
		self.focusManager._lastNavigatorObjectPosition = Coordinates(0, 0)

	def _run(self, *, followMouse, followSystemFocus, followReview, followNavigatorObject):
		"""Run getCurrentFocusCoordinates with all sources moved and the given settings."""
		self.focusManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.focusManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.focusManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.focusManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))
		mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=False)

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=followMouse,
			followSystemFocus=followSystemFocus,
			followReview=followReview,
			followNavigatorObject=followNavigatorObject,
		)

		with patch(
			"_magnifier.utils.focusManager.getFollowState",
			side_effect=followStateSideEffect,
		):
			return self.focusManager.getCurrentFocusCoordinates()

	def testFollowMouseDisabled(self):
		"""When followMouse=False, mouse changes are ignored and system focus wins."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)
		self.assertEqual(coords, Coordinates(20, 20))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.SYSTEM_FOCUS)

	def testFollowSystemFocusDisabled(self):
		"""When followSystemFocus=False, system focus changes are ignored and review wins."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=False,
			followReview=True,
			followNavigatorObject=True,
		)
		self.assertEqual(coords, Coordinates(30, 30))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.REVIEW)

	def testFollowReviewDisabled(self):
		"""When followReview=False, review changes are ignored and navigator wins."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=False,
			followReview=False,
			followNavigatorObject=True,
		)
		self.assertEqual(coords, Coordinates(40, 40))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.NAVIGATOR_OBJECT)

	def testAllFollowDisabled(self):
		"""When all settings are False, no source fires and we fall back to default mouse."""
		coords = self._run(
			followMouse=False,
			followSystemFocus=False,
			followReview=False,
			followNavigatorObject=False,
		)
		# No previous focus → default branch returns current mouse position
		self.assertEqual(coords, Coordinates(10, 10))

	def testFollowMouseDragIgnoresSettings(self):
		"""Mouse drag (left click held) with followMouse=True always wins regardless of others."""
		self.focusManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.focusManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.focusManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.focusManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))
		mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=True)

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=True,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)

		with patch(
			"_magnifier.utils.focusManager.getFollowState",
			side_effect=followStateSideEffect,
		):
			coords = self.focusManager.getCurrentFocusCoordinates()

		self.assertEqual(coords, Coordinates(10, 10))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.MOUSE)

	def testDisableFollowMouseFallsToSystemFocus(self):
		"""When followMouse is disabled after mouse was the last focus, should fall back to system focus."""
		# Simulate: mouse was previously the active focus source
		self.focusManager._lastFocusedObject = MagnifierFollowFocusType.MOUSE
		# Positions haven't changed from last recorded values (no "change" detected)
		self.focusManager._lastMousePosition = Coordinates(10, 10)
		self.focusManager._lastSystemFocusPosition = Coordinates(20, 20)
		self.focusManager._lastNavigatorObjectPosition = Coordinates(40, 40)

		self.focusManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.focusManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.focusManager._getReviewPosition = MagicMock(return_value=None)
		self.focusManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))
		mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=False)

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)

		with patch(
			"_magnifier.utils.focusManager.getFollowState",
			side_effect=followStateSideEffect,
		):
			coords = self.focusManager.getCurrentFocusCoordinates()

		self.assertEqual(coords, Coordinates(20, 20))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.SYSTEM_FOCUS)

	def testDisableFollowMouseWhileMouseMovingFallsToSystemFocus(self):
		"""When followMouse is disabled and mouse is still moving, should not follow mouse."""
		self.focusManager._lastFocusedObject = MagnifierFollowFocusType.MOUSE
		self.focusManager._lastMousePosition = Coordinates(10, 10)
		self.focusManager._lastSystemFocusPosition = Coordinates(20, 20)
		self.focusManager._lastNavigatorObjectPosition = Coordinates(40, 40)

		# Mouse has moved but followMouse is False
		self.focusManager._getMousePosition = MagicMock(return_value=Coordinates(15, 15))
		self.focusManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.focusManager._getReviewPosition = MagicMock(return_value=None)
		self.focusManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))
		mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=False)

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=True,
			followReview=True,
			followNavigatorObject=True,
		)

		with patch(
			"_magnifier.utils.focusManager.getFollowState",
			side_effect=followStateSideEffect,
		):
			coords = self.focusManager.getCurrentFocusCoordinates()

		self.assertEqual(coords, Coordinates(20, 20))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.SYSTEM_FOCUS)

	def testDisableFollowSystemFocusFallsToReview(self):
		"""When last focus was system focus and its setting is disabled, should fall to review."""
		self.focusManager._lastFocusedObject = MagnifierFollowFocusType.SYSTEM_FOCUS
		self.focusManager._lastMousePosition = Coordinates(10, 10)
		self.focusManager._lastSystemFocusPosition = Coordinates(20, 20)
		self.focusManager._lastReviewPosition = Coordinates(30, 30)
		self.focusManager._lastNavigatorObjectPosition = Coordinates(40, 40)

		self.focusManager._getMousePosition = MagicMock(return_value=Coordinates(10, 10))
		self.focusManager._getSystemFocusPosition = MagicMock(return_value=Coordinates(20, 20))
		self.focusManager._getReviewPosition = MagicMock(return_value=Coordinates(30, 30))
		self.focusManager._getNavigatorObjectPosition = MagicMock(return_value=Coordinates(40, 40))
		mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=False)

		followStateSideEffect = _makeFollowStateSideEffect(
			followMouse=False,
			followSystemFocus=False,
			followReview=True,
			followNavigatorObject=True,
		)

		with patch(
			"_magnifier.utils.focusManager.getFollowState",
			side_effect=followStateSideEffect,
		):
			coords = self.focusManager.getCurrentFocusCoordinates()

		self.assertEqual(coords, Coordinates(30, 30))
		self.assertEqual(self.focusManager.getLastFocusType(), MagnifierFollowFocusType.REVIEW)
