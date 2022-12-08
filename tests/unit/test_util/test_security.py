# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule.
"""

from dataclasses import dataclass
from typing import (
	List,
	Optional,
)
import unittest
from unittest.mock import patch

from utils.security import (
	_WindowNotFoundError,
	_isWindowAboveWindowMatchesCond,
)
import winUser


@dataclass
class _MoveWindow:
	"""Used to move a window from one index to another when a specific index is reached."""
	startIndex: int  # A window at this index
	endIndex: int  # is moved to this index
	triggerIndex: int  # when this index is reached
	triggered = False  # If the move has been triggered


class _Test_isWindowAboveWindowMatchesCond(unittest.TestCase):
	"""
	Base class to patch winUser functions used in _isWindowAboveWindowMatchesCond.

	Navigating windows is replaced by a list of fake HWNDs.
	HWNDs are represented by integers (1-10).
	The initial relative z-order of HWNDs is defined by the order of the HWND value in the self._windows list.
	A HWND value at index 0, should be considered to have a z-order "above" a HWND value at index 1.
	"""
	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		"""Fetch current window, find adjacent window by relation."""
		currentWindowIndex = self._windows.index(hwnd)
		if relation == winUser.GW_HWNDNEXT:
				nextIndex = currentWindowIndex + 1
		elif relation == winUser.GW_HWNDPREV:
				nextIndex = currentWindowIndex - 1
		else:
			return winUser.GW_RESULT_NOT_FOUND
		if nextIndex >= len(self._windows) or nextIndex < 0:
			return winUser.GW_RESULT_NOT_FOUND
		return self._windows[nextIndex]

	def _windowMatches(self, expectedWindow: int):
		def _helper(hwnd: int) -> bool:
			return hwnd == expectedWindow
		return _helper

	def setUp(self) -> None:
		self._getWindowPatch = patch("winUser.getWindow", self._getWindow_patched)
		self._getWindowPatch.start()
		self._windows: List[winUser.HWNDVal] = list(range(1, 11))
		"""
		List of fake HWNDs, given an ordered index to make testing easier.
		Must be 1 indexed as a HWND of 0 is treated an error.
		"""
		return super().setUp()

	def tearDown(self) -> None:
		self._getWindowPatch.stop()
		return super().tearDown()


class Test_isWindowAboveWindowMatchesCond_static(_Test_isWindowAboveWindowMatchesCond):
	"""Test fetching a z-index when the order of window does not change"""
	def test_windowNotFound(self):
		startWindow = len(self._windows) // 2
		with self.assertRaises(_WindowNotFoundError):
			_isWindowAboveWindowMatchesCond(startWindow, lambda x: False)

	def test_isAbove(self):
		aboveIndex = 1
		belowIndex = 2
		self.assertTrue(_isWindowAboveWindowMatchesCond(aboveIndex, self._windowMatches(belowIndex)))

	def test_isBelow(self):
		aboveIndex = 1
		belowIndex = 2
		self.assertFalse(_isWindowAboveWindowMatchesCond(belowIndex, self._windowMatches(aboveIndex)))


class Test_isWindowAboveWindowMatchesCond_dynamic(_Test_isWindowAboveWindowMatchesCond):
	"""
	Test fetching comparing the relative order of 2 windows,
	where a window moves during the operation.

	This test models changes when performing a bi-direction search that expects the
	start window to be before/above the end window.
	By symmetry, the same test results are expected if the search goes the other way,
	expecting it to return False, rather than True.

	To model changes in z-order, a _MoveWindow is used to describe the change.
	When the getWindow is called with the triggerIndex, the value at start index is moved
	"in front" of the window at end index.
	Effectively this means that before getting the window at the triggerIndex, the order of
	windows will change.
	"""
	_queuedMove: Optional[_MoveWindow] = None

	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		self._moveIndexToNewIndexAtIndexOnce(self._windows.index(hwnd))
		result = super()._getWindow_patched(hwnd, relation)
		return result

	def _moveIndexToNewIndexAtIndexOnce(self, currentIndex: int):
		from logging import getLogger
		
		getLogger().error(f"Current index {currentIndex}, {self._windows}")
		if (
			self._queuedMove
			and currentIndex == self._queuedMove.triggerIndex
			and not self._queuedMove.triggered
		):
			self._queuedMove.triggered = True
			window = self._windows.pop(self._queuedMove.startIndex)
			self._windows.insert(self._queuedMove.endIndex, window)

	def test_visited_windowMoves_pastTarget(self):
		"""
		A visited window is moved past the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 5
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=6,
			triggerIndex=4
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_visited_windowMoves_beforeTarget(self):
		"""
		A visited window is moved towards but before the target window.
		It is counted twice.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 6
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=5,
			triggerIndex=4
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_visited_windowMoves_awayFromTarget(self):
		"""
		A visited window is moved in the opposite direction from the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 6
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=1,
			triggerIndex=4
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_active_windowMoves_pastTarget(self):
		"""
		A window we are currently visiting moves past the target window.
		This causes the search to skip the target window.
		"""
		startWindow = 2
		targetWindow = 5
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=7,
			triggerIndex=3
		)
		with self.assertRaises(_WindowNotFoundError):
			_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow))

	def test_active_windowMoves_beforeTarget(self):
		"""
		A window we are currently visiting moves towards but before the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 10
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=5,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_active_windowMoves_awayFromTarget(self):
		"""
		A window we are currently visiting moves in the opposite direction to the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 10
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=1,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_unvisited_windowMoves_pastTarget(self):
		"""
		An unvisited window moves towards, and past the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 6
		self._queuedMove = _MoveWindow(
			startIndex=4,
			endIndex=8,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_unvisited_windowMoves_beforeTarget(self):
		"""
		An unvisited window moves towards, but before the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 8
		self._queuedMove = _MoveWindow(
			startIndex=4,
			endIndex=6,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_unvisited_windowMoves_awayFromTarget(self):
		"""
		An unvisited window moves in the opposite direction the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 8
		self._queuedMove = _MoveWindow(
			startIndex=4,
			endIndex=1,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_startWindow_windowMoves_pastTarget(self):
		"""
		Start window moves towards, and past the target window.
		This means the relative z-order has changed, but the change is not detected.
		The relative z-order of the start of the search is returned.
		"""
		startWindow = 2
		targetWindow = 6
		self._queuedMove = _MoveWindow(
			startIndex=startWindow - 1,
			endIndex=8,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_startWindow_windowMoves_beforeTarget(self):
		"""
		Start window moves towards, but before the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 8
		self._queuedMove = _MoveWindow(
			startIndex=startWindow - 1,
			endIndex=6,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))

	def test_StartWindow_windowMoves_awayFromTarget(self):
		"""
		Start window moves in the opposite direction the target window.
		This does not affect the relative z-order.
		"""
		startWindow = 2
		targetWindow = 8
		self._queuedMove = _MoveWindow(
			startIndex=startWindow - 1,
			endIndex=1,
			triggerIndex=3
		)
		self.assertTrue(_isWindowAboveWindowMatchesCond(startWindow, self._windowMatches(targetWindow)))
