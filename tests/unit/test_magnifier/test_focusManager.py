# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from dataclasses import dataclass
from _magnifier.utils.focusManager import FocusManager
from _magnifier.utils.types import Coordinates, FocusType
import unittest
from unittest.mock import MagicMock, Mock, patch
import mouseHandler
import winUser


@dataclass(frozen=True)
class FocusTestParam:
	"""Parameters for focus coordinate testing."""

	navigatorObjectPos: Coordinates
	systemFocusPos: Coordinates
	mousePos: tuple
	leftPressed: bool
	expectedCoords: Coordinates
	expectedFocus: FocusType
	description: str = ""
	lastFocusedObject: FocusType | None = None


class TestFocusManager(unittest.TestCase):
	"""Tests for the FocusManager class."""

	def setUp(self):
		"""Setup before each test."""
		self.focusManager = FocusManager()

	def testFocusManagerCreation(self):
		"""Can we create a FocusManager with initialized values?"""
		self.assertIsNone(self.focusManager._lastFocusedObject)
		self.assertEqual(self.focusManager._lastSystemFocusPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastNavigatorObjectPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastMousePosition, Coordinates(0, 0))

	def testGetNavigatorObjectPosition(self):
		"""Getting navigator object position with different API responses."""
		# Case 1: Review position successful
		with patch("_magnifier.utils.focusManager.api.getReviewPosition") as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point

			coords = self.focusManager._getNavigatorObjectPosition()
			self.assertEqual(coords, Coordinates(300, 400))

		# Case 2: Review position fails, navigator object works
		with patch("_magnifier.utils.focusManager.api.getReviewPosition", return_value=None):
			with patch("_magnifier.utils.focusManager.api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = (100, 150, 200, 300)

				coords = self.focusManager._getNavigatorObjectPosition()
				# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
				self.assertEqual(coords, Coordinates(200, 300))

		# Case 3: Everything fails - should return last valid position from Case 2
		with patch("_magnifier.utils.focusManager.api.getReviewPosition", return_value=None):
			with patch("_magnifier.utils.focusManager.api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = Mock(side_effect=Exception())

				coords = self.focusManager._getNavigatorObjectPosition()
				# Should return last valid position (200, 300)
				self.assertEqual(coords, Coordinates(200, 300))

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
				expectedFocus=FocusType.MOUSE,
				description="Left click is pressed should return mouse position",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(10, 10),
				leftPressed=False,
				expectedCoords=Coordinates(10, 10),
				expectedFocus=FocusType.MOUSE,
				description="Mouse moving (not dragging)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(15, 15),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(15, 15),
				expectedFocus=FocusType.SYSTEM_FOCUS,
				description="System focus changed",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(20, 20),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=FocusType.NAVIGATOR,
				description="Navigator object changed (NumPad navigation)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=FocusType.MOUSE,
				description="Nothing changed, last was Mouse",
				lastFocusedObject=FocusType.MOUSE,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(0, 0),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(0, 0),
				leftPressed=False,
				expectedCoords=Coordinates(0, 0),
				expectedFocus=FocusType.NAVIGATOR,
				description="Nothing changed, last was NAVIGATOR",
				lastFocusedObject=FocusType.NAVIGATOR,
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(10, 10),
				systemFocusPos=Coordinates(0, 0),
				mousePos=(20, 20),
				leftPressed=False,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=FocusType.MOUSE,
				description="Both mouse and navigator object moved (mouse has priority)",
			),
			FocusTestParam(
				navigatorObjectPos=Coordinates(10, 10),
				systemFocusPos=Coordinates(15, 15),
				mousePos=(20, 20),
				leftPressed=True,
				expectedCoords=Coordinates(20, 20),
				expectedFocus=FocusType.MOUSE,
				description="All three moved while dragging (mouse drag has highest priority)",
			),
		]

		for param in subTestParams:
			with self.subTest(description=param.description):
				# Reset focus manager state
				self.focusManager._lastNavigatorObjectPosition = Coordinates(0, 0)
				self.focusManager._lastSystemFocusPosition = Coordinates(0, 0)
				self.focusManager._lastMousePosition = Coordinates(0, 0)

				# Set lastFocusedObject if specified
				if param.lastFocusedObject is not None:
					self.focusManager._lastFocusedObject = param.lastFocusedObject

				# Mock methods
				self.focusManager._getNavigatorObjectPosition = MagicMock(
					return_value=param.navigatorObjectPos,
				)
				self.focusManager._getSystemFocusPosition = MagicMock(return_value=param.systemFocusPos)
				mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=param.leftPressed)
				winUser.getCursorPos = MagicMock(return_value=param.mousePos)

				# Execute
				focusCoordinates = self.focusManager.getCurrentFocusCoordinates()

				# Assert
				self.assertEqual(focusCoordinates, param.expectedCoords)
				self.assertEqual(self.focusManager.getLastFocusType(), param.expectedFocus)

	def testGetLastFocusType(self):
		"""Test getting the last focus type."""
		self.assertIsNone(self.focusManager.getLastFocusType())

		self.focusManager._lastFocusedObject = FocusType.MOUSE
		self.assertEqual(self.focusManager.getLastFocusType(), FocusType.MOUSE)

		self.focusManager._lastFocusedObject = FocusType.NAVIGATOR
		self.assertEqual(self.focusManager.getLastFocusType(), FocusType.NAVIGATOR)

		self.focusManager._lastFocusedObject = FocusType.SYSTEM_FOCUS
		self.assertEqual(self.focusManager.getLastFocusType(), FocusType.SYSTEM_FOCUS)
