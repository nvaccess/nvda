# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from _magnifier.utils.focusManager import FocusManager
from _magnifier.utils.types import Coordinates, FocusType
import unittest
from unittest.mock import MagicMock, Mock, patch
import mouseHandler
import winUser


class TestFocusManager(unittest.TestCase):
	"""Tests for the FocusManager class."""

	def setUp(self):
		"""Setup before each test."""
		self.focusManager = FocusManager()

	def testFocusManagerCreation(self):
		"""Can we create a FocusManager with initialized values?"""
		self.assertIsNone(self.focusManager._lastFocusedObject)
		self.assertEqual(self.focusManager._lastSystemFocusPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastNavigatorPosition, Coordinates(0, 0))
		self.assertEqual(self.focusManager._lastMousePosition, Coordinates(0, 0))

	def testGetNavigatorPosition(self):
		"""Getting navigator position with different API responses."""
		# Case 1: Review position successful
		with patch("_magnifier.utils.focusManager.api.getReviewPosition") as mock_review:
			mock_point = Mock()
			mock_point.x = 300
			mock_point.y = 400
			mock_review.return_value.pointAtStart = mock_point

			coords = self.focusManager._getNavigatorPosition()
			self.assertEqual(coords, Coordinates(300, 400))

		# Case 2: Review position fails, navigator works
		with patch("_magnifier.utils.focusManager.api.getReviewPosition", return_value=None):
			with patch("_magnifier.utils.focusManager.api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = (100, 150, 200, 300)

				coords = self.focusManager._getNavigatorPosition()
				# Center: (100 + 200//2, 150 + 300//2) = (200, 300)
				self.assertEqual(coords, Coordinates(200, 300))

		# Case 3: Everything fails - should return last valid position from Case 2
		with patch("_magnifier.utils.focusManager.api.getReviewPosition", return_value=None):
			with patch("_magnifier.utils.focusManager.api.getNavigatorObject") as mock_navigator:
				mock_navigator.return_value.location = Mock(side_effect=Exception())

				coords = self.focusManager._getNavigatorPosition()
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

		def testValues(
			navigatorPos: Coordinates,
			systemFocusPos: Coordinates,
			mousePos: tuple,
			leftPressed: bool,
			expected_coords: Coordinates,
			expected_focused: FocusType,
		):
			# Reset focus manager state
			self.focusManager._lastNavigatorPosition = Coordinates(0, 0)
			self.focusManager._lastSystemFocusPosition = Coordinates(0, 0)
			self.focusManager._lastMousePosition = Coordinates(0, 0)

			self.focusManager._getNavigatorPosition = MagicMock(return_value=navigatorPos)
			self.focusManager._getSystemFocusPosition = MagicMock(return_value=systemFocusPos)
			mouseHandler.isLeftMouseButtonLocked = MagicMock(return_value=leftPressed)
			winUser.getCursorPos = MagicMock(return_value=mousePos)

			focusCoordinates = self.focusManager.getCurrentFocusCoordinates()

			self.assertEqual(focusCoordinates, expected_coords)
			self.assertEqual(self.focusManager.getLastFocusType(), expected_focused)

		# Case 1: Left click is pressed should return mouse position
		testValues(
			Coordinates(0, 0),
			Coordinates(0, 0),
			(0, 0),
			True,
			Coordinates(0, 0),
			FocusType.MOUSE,
		)

		# Case 2: Mouse moving (not dragging)
		testValues(
			Coordinates(0, 0),
			Coordinates(0, 0),
			(10, 10),
			False,
			Coordinates(10, 10),
			FocusType.MOUSE,
		)

		# Case 3: System focus changed
		testValues(
			Coordinates(0, 0),
			Coordinates(15, 15),
			(0, 0),
			False,
			Coordinates(15, 15),
			FocusType.SYSTEM_FOCUS,
		)

		# Case 4: Navigator changed (NumPad navigation)
		testValues(
			Coordinates(20, 20),
			Coordinates(0, 0),
			(0, 0),
			False,
			Coordinates(20, 20),
			FocusType.NAVIGATOR,
		)

		# Case 5: Nothing changed, last was Mouse
		self.focusManager._lastFocusedObject = FocusType.MOUSE
		testValues(
			Coordinates(0, 0),
			Coordinates(0, 0),
			(0, 0),
			False,
			Coordinates(0, 0),
			FocusType.MOUSE,
		)

		# Case 6: Nothing changed, last was NAVIGATOR
		self.focusManager._lastFocusedObject = FocusType.NAVIGATOR
		testValues(
			Coordinates(0, 0),
			Coordinates(0, 0),
			(0, 0),
			False,
			Coordinates(0, 0),
			FocusType.NAVIGATOR,
		)

		# Case 7: Both mouse and navigator moved (mouse has priority)
		testValues(
			Coordinates(10, 10),
			Coordinates(0, 0),
			(20, 20),
			False,
			Coordinates(20, 20),
			FocusType.MOUSE,
		)

		# Case 8: All three moved while dragging (mouse drag has highest priority)
		testValues(
			Coordinates(10, 10),
			Coordinates(15, 15),
			(20, 20),
			True,
			Coordinates(20, 20),
			FocusType.MOUSE,
		)

	def testGetLastFocusType(self):
		"""Test getting the last focus type."""
		self.assertIsNone(self.focusManager.getLastFocusType())

		self.focusManager._lastFocusedObject = FocusType.MOUSE
		self.assertEqual(self.focusManager.getLastFocusType(), FocusType.MOUSE)

		self.focusManager._lastFocusedObject = FocusType.NAVIGATOR
		self.assertEqual(self.focusManager.getLastFocusType(), FocusType.NAVIGATOR)

		self.focusManager._lastFocusedObject = FocusType.SYSTEM_FOCUS
		self.assertEqual(self.focusManager.getLastFocusType(), FocusType.SYSTEM_FOCUS)
