# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule."""

from dataclasses import dataclass
from typing import (
	List,
	Optional,
	Type,
)
import unittest
from unittest.mock import patch

from utils.security import (
	_UnexpectedWindowCountError,
	_isWindowBelowWindowMatchesCond,
)
import winUser


@dataclass
class _MoveWindow:
	"""Used to move a window from one spot to another when a specific window is reached."""

	HWNDToMove: winUser.HWNDVal  # This window
	insertBelowHWND: winUser.HWNDVal  # is moved to below this window
	triggerHWND: winUser.HWNDVal  # when this window is reached
	triggered = False  # If the move has been triggered


class _Test_isWindowAboveWindowMatchesCond(unittest.TestCase):
	"""
	Base class to patch winUser functions used in _isWindowBelowWindowMatchesCond.

	Navigating windows is replaced by a list of fake HWNDs.
	HWNDs are represented by integers (1-10).
	The initial relative z-order of HWNDs is defined by the order of the HWND value in the self._windows list.
	A HWND value at index 0, should be considered to have a z-order "above" a HWND value at index 1.
	"""

	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		"""
		Fetch current window, find adjacent window by relation.
		The top level window has the highest index.
		"""
		currentWindowIndex = self._windows.index(hwnd)
		if relation == winUser.GW_HWNDNEXT:
			nextIndex = currentWindowIndex - 1
		elif relation == winUser.GW_HWNDPREV:
			nextIndex = currentWindowIndex + 1
		elif relation == winUser.GW_HWNDFIRST:
			nextIndex = len(self._windows) - 1
		elif relation == winUser.GW_HWNDLAST:
			nextIndex = 0
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
		self._getDesktopWindowPatch = patch("winUser.getDesktopWindow", lambda: 0)
		self._getTopWindowPatch = patch("winUser.getTopWindow", lambda _: self._windows[0])
		self._getWindowPatch.start()
		self._getTopWindowPatch.start()
		self._getDesktopWindowPatch.start()
		self._generateWindows()
		return super().setUp()

	def _generateWindows(self):
		"""
		List of fake HWNDs, given an ordered index to make testing easier.
		Must be 1 indexed as a HWND of 0 is treated an error.
		"""
		self._windows: List[winUser.HWNDVal] = list(range(1, 11))

	def tearDown(self) -> None:
		self._getWindowPatch.stop()
		self._getTopWindowPatch.stop()
		self._getDesktopWindowPatch.stop()
		return super().tearDown()


class Test_isWindowAboveWindowMatchesCond_static(_Test_isWindowAboveWindowMatchesCond):
	"""Test fetching a z-index when the order of window does not change"""

	def test_secondWindowNotFound(self):
		with self.assertRaises(_UnexpectedWindowCountError):
			# Errors are handled as if window is above
			_isWindowBelowWindowMatchesCond(5, lambda x: False)

	def test_firstWindowNotFound(self):
		self.assertFalse(_isWindowBelowWindowMatchesCond(-1, lambda x: x == 5))

	def test_isAbove(self):
		aboveIndex = 2
		belowIndex = 1
		self.assertFalse(_isWindowBelowWindowMatchesCond(aboveIndex, self._windowMatches(belowIndex)))

	def test_isBelow(self):
		aboveIndex = 2
		belowIndex = 1
		self.assertTrue(_isWindowBelowWindowMatchesCond(belowIndex, self._windowMatches(aboveIndex)))


class Test_isWindowAboveWindowMatchesCond_dynamic(_Test_isWindowAboveWindowMatchesCond):
	"""
	Test fetching comparing the relative order of 2 windows,
	where a window moves during the operation.

	To model changes in z-order, a _MoveWindow is used to describe the change.
	Effectively this means that before getting the window at the triggerIndex, the order of
	windows will change.
	"""

	_queuedMove: Optional[_MoveWindow] = None

	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		self._triggerQueuedMove(hwnd)
		result = super()._getWindow_patched(hwnd, relation)
		return result

	def _triggerQueuedMove(self, currentHWND: winUser.HWNDVal):
		from logging import getLogger

		getLogger().debug(f"Current HWND {currentHWND}, {self._windows}")
		if (
			self._queuedMove
			and currentHWND == self._queuedMove.triggerHWND
			and not self._queuedMove.triggered
		):
			self._queuedMove.triggered = True
			self._windows.remove(self._queuedMove.HWNDToMove)
			insertIndex = self._windows.index(self._queuedMove.insertBelowHWND)
			self._windows.insert(insertIndex, self._queuedMove.HWNDToMove)

	def _test_windowWithMove(
		self,
		move: _MoveWindow,
		aboveWindow: winUser.HWNDVal,
		belowWindow: winUser.HWNDVal,
		aboveRaises: Optional[Type[Exception]] = None,
		belowRaises: Optional[Type[Exception]] = None,
		aboveExpectFailure: bool = False,
		belowExpectFailure: bool = False,
	):
		"""
		Compares the relative z-order of two windows.
		Checks the inverse behaviour:
		i.e. swaps the order of the window, expect the result to be the opposite.
		For the expected "above is true" case, if aboveRaises is provided, expect the exception.
		If aboveExpectFailure is provided, expect the "above is false", i.e. an incorrect result.
		Similarly is true for the "below is true" case.
		@param move: move a window when another window is reached
		@param aboveWindow: expected above window
		@param belowWindow: expected below window
		@param aboveRaises: if provided, expect the exception to be raised when checking the "above is true"
		@param belowRaises: if provided, expect the exception to be raised when checking the "below is true"
		@param aboveExpectFailure: if True, expect a failure when checking the "above is true"
		@param belowExpectFailure: if True, expect a failure when checking the "below is true"
		"""
		self._queuedMove = move

		# Check aboveWindow is above belowWindow
		isBelow = False
		if aboveExpectFailure:
			isBelow = not isBelow
		if aboveRaises is None:
			self.assertEqual(
				isBelow,
				_isWindowBelowWindowMatchesCond(aboveWindow, self._windowMatches(belowWindow)),
			)
		else:
			with self.assertRaises(aboveRaises):
				_isWindowBelowWindowMatchesCond(aboveWindow, self._windowMatches(belowWindow))

		# Reset the window list
		self._generateWindows()
		# Reset the move
		self._queuedMove.triggered = False

		# Check belowWindow is below aboveWindow
		isBelow = True
		if belowExpectFailure:
			isBelow = not isBelow
		if belowRaises is None:
			self.assertEqual(
				isBelow,
				_isWindowBelowWindowMatchesCond(belowWindow, self._windowMatches(aboveWindow)),
			)
		else:
			with self.assertRaises(belowRaises):
				_isWindowBelowWindowMatchesCond(belowWindow, self._windowMatches(aboveWindow))

	def test_visited_windowMoves_aboveTargets(self):
		"""
		A visited window is moved above the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=3,
				insertBelowHWND=6,
				triggerHWND=4,
			),
			aboveWindow=5,
			belowWindow=2,
		)

	def test_visited_windowMoves_betweenTargets(self):
		"""
		A visited window is moved between the target windows.
		It is counted twice.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=3,
				insertBelowHWND=5,
				triggerHWND=4,
			),
			aboveWindow=6,
			belowWindow=2,
		)

	def test_visited_windowMoves_belowTargets(self):
		"""
		A visited window is moved in the opposite direction from the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=3,
				insertBelowHWND=1,
				triggerHWND=4,
			),
			aboveWindow=5,
			belowWindow=2,
		)

	def test_active_windowMoves_betweenTargets(self):
		"""
		A window we are currently visiting moves between target windows.
		This causes the search to skip the first window.
		This can cause a false negative (i.e. content becomes accessible when it should be secure).
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=3,
				insertBelowHWND=8,
				triggerHWND=3,
			),
			aboveWindow=10,
			belowWindow=6,
			aboveRaises=_UnexpectedWindowCountError,  # handled as if window is above
			belowExpectFailure=True,  # handled as if window is above
		)

	def test_active_windowMoves_beforeTargets(self):
		"""
		A window we are currently visiting moves before the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=3,
				insertBelowHWND=5,
				triggerHWND=3,
			),
			aboveWindow=10,
			belowWindow=6,
		)

	def test_active_windowMoves_belowTargets(self):
		"""
		A window we are currently visiting moves in the opposite direction
		from the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			_MoveWindow(
				HWNDToMove=3,
				insertBelowHWND=1,
				triggerHWND=3,
			),
			aboveWindow=10,
			belowWindow=6,
		)

	def test_unvisited_windowMoves_aboveTargets(self):
		"""
		An unvisited window moves above the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=5,
				insertBelowHWND=8,
				triggerHWND=3,
			),
			aboveWindow=6,
			belowWindow=2,
		)

	def test_unvisited_windowMoves_betweenTargets(self):
		"""
		An unvisited window moves between the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=4,
				insertBelowHWND=6,
				triggerHWND=3,
			),
			aboveWindow=8,
			belowWindow=2,
		)

	def test_unvisited_windowMoves_belowTargets(self):
		"""
		An unvisited window moves in the opposite direction from the target windows.
		This does not affect the relative z-order of the target windows.
		"""
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=4,
				insertBelowHWND=1,
				triggerHWND=3,
			),
			aboveWindow=8,
			belowWindow=2,
		)

	def test_belowWindow_windowMoves_aboveAboveWindow(self):
		"""
		Below window moves above the above window.
		This means the relative z-order has changed, but the change is not detected.
		The initial relative z-order is returned.
		"""
		belowWindow = 2
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=belowWindow,
				insertBelowHWND=8,
				triggerHWND=3,
			),
			aboveWindow=6,
			belowWindow=belowWindow,
		)

	def test_belowWindow_windowMoves_towardsAboveWindow(self):
		"""
		Below window moves towards the above window.
		This causes the window to be counted twice.
		This does not affect the relative z-order of the target windows.
		"""
		belowWindow = 2
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=belowWindow,
				insertBelowHWND=6,
				triggerHWND=3,
			),
			aboveWindow=8,
			belowWindow=belowWindow,
			belowRaises=_UnexpectedWindowCountError,  # handled as if window is above
		)

	def test_belowWindow_windowMoves_furtherBelow(self):
		"""
		The below window moves away from the above window.
		This does not affect the relative z-order of the target windows.
		"""
		belowWindow = 2
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=belowWindow,
				insertBelowHWND=1,
				triggerHWND=3,
			),
			aboveWindow=8,
			belowWindow=belowWindow,
		)

	def test_aboveWindow_windowMoves_furtherAbove(self):
		"""
		Above window moves further above
		This does not affect the relative z-order of the target windows.
		"""
		aboveWindow = 6
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=aboveWindow,
				insertBelowHWND=8,
				triggerHWND=3,
			),
			aboveWindow=aboveWindow,
			belowWindow=2,
		)

	def test_aboveWindow_windowMoves_towardsBelowWindow(self):
		"""
		Above window moves towards, but above the below window.
		This does not affect the relative z-order of the target windows.
		"""
		aboveWindow = 8
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=aboveWindow,
				insertBelowHWND=6,
				triggerHWND=3,
			),
			aboveWindow=aboveWindow,
			belowWindow=2,
		)

	def test_aboveWindow_windowMoves_belowBelowWindow(self):
		"""
		Above window moves in the opposite direction of the above window.
		This means the relative z-order has changed, but the change is not detected.
		The initial relative z-order is returned.
		"""
		aboveWindow = 8
		self._test_windowWithMove(
			move=_MoveWindow(
				HWNDToMove=aboveWindow,
				insertBelowHWND=1,
				triggerHWND=3,
			),
			aboveWindow=aboveWindow,
			belowWindow=2,
			belowRaises=_UnexpectedWindowCountError,  # handled as if window is above
		)
