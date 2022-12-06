# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule.
"""

from dataclasses import dataclass
from typing import (
	Optional,
)
import unittest
from unittest.mock import patch

from utils.security import (
	_getWindowZIndex,
)
import winUser


@dataclass
class _MoveWindow:
	startIndex: int  # A window at this index
	endIndex: int  # is moved to this index
	triggerIndex: int  # when this index is reached
	triggered = False


class _Test_getWindowZIndex(unittest.TestCase):
	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		"""Fetch current window, find adjacent window by relation."""
		currentWindowIndex = self._windows.index(hwnd)
		if relation == winUser.GW_HWNDNEXT:
			try:
				return self._windows[currentWindowIndex + 1]
			except IndexError:
				return 0
		elif relation == winUser.GW_HWNDPREV:
			try:
				return self._windows[currentWindowIndex - 1]
			except IndexError:
				return 0
		else:
			return 0

	def _windowMatches(self, expectedWindow: int):
		def _helper(hwnd: int) -> bool:
			return hwnd == expectedWindow
		return _helper

	def setUp(self) -> None:
		# value from _getDesktopWindowPatch is discarded by _getTopWindowPatch
		self._getDesktopWindowPatch = patch("winUser.getDesktopWindow", lambda: 0)
		self._getTopWindowPatch = patch("winUser.getTopWindow", lambda _hwnd: self._windows[0])
		self._getWindowPatch = patch("winUser.getWindow", self._getWindow_patched)
		self._getDesktopWindowPatch.start()
		self._getTopWindowPatch.start()
		self._getWindowPatch.start()
		self._windows = list(range(1, 11))  # must be 1 indexed
		return super().setUp()

	def tearDown(self) -> None:
		self._getDesktopWindowPatch.stop()
		self._getTopWindowPatch.stop()
		self._getWindowPatch.stop()
		return super().tearDown()


class Test_getWindowZIndex_static(_Test_getWindowZIndex):
	def test_noMatch(self):
		self.assertIsNone(_getWindowZIndex(lambda x: False))

	def test_firstWindowMatch_noChanges(self):
		targetWindow = 1
		expectedIndex = targetWindow - 1
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_lastWindowMatch_noChanges(self):
		targetWindow = len(self._windows)
		expectedIndex = targetWindow - 1
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))


class Test_getWindowZIndex_dynamic(_Test_getWindowZIndex):
	_queuedMove: Optional[_MoveWindow] = None

	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		self._moveIndexToNewIndexAtIndexOnce(self._windows.index(hwnd))
		result = super()._getWindow_patched(hwnd, relation)
		return result

	def _moveIndexToNewIndexAtIndexOnce(self, currentIndex: int):
		from logging import getLogger
		
		getLogger().error(f"{currentIndex}")
		if (
			self._queuedMove
			and currentIndex == self._queuedMove.triggerIndex
			and not self._queuedMove.triggered
		):
			self._queuedMove.triggered = True
			window = self._windows.pop(self._queuedMove.startIndex)
			self._windows.insert(self._queuedMove.endIndex, window)

	def test_prev_windowMoves_pastTarget(self):
		"""A previous window is moved past the target window. This does not affect the z-order."""
		self._queuedMove = _MoveWindow(
			startIndex=2,
			endIndex=9,
			triggerIndex=5
		)
		targetWindow = 7
		expectedIndex = targetWindow - 1
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_prev_windowMoves_beforeTarget(self):
		"""A previous window is moved before the target window. It is counted twice."""
		self._queuedMove = _MoveWindow(
			startIndex=2,
			endIndex=5,
			triggerIndex=3
		)
		targetWindow = 7
		expectedIndex = targetWindow  # difference is normally 1, however a window is counted twice
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_active_windowMoves_pastTarget(self):
		"""A window we are looking at moves past the match, skipping our target window."""
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=8,
			triggerIndex=3
		)
		targetWindow = 6
		self.assertEqual(None, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_active_windowMoves_beforeTarget(self):
		"""A future window we are looking at moves forward, but before the match, decreasing our z-index."""
		self._queuedMove = _MoveWindow(
			startIndex=3,
			endIndex=4,
			triggerIndex=3
		)
		targetWindow = 7
		# difference is normally 1, however a window is skipped due to the move
		expectedIndex = targetWindow - 2
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_future_windowMoves_pastTarget(self):
		"""A future window moves forward, and past the match.
		This does not change anything in practice, the windows affected are yet to be indexed.
		However, during the move, the z-index to target is decreased,
		as a window is moved past the match."""
		self._queuedMove = _MoveWindow(
			startIndex=5,
			endIndex=9,
			triggerIndex=3
		)
		targetWindow = 7
		# difference is normally 1, however a window is skipped due to the move
		expectedIndex = targetWindow - 2
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_future_windowMoves_beforeTarget(self):
		"""A future window moves forward, and past the match.
		This does not change anything in practice, the windows affected are yet to be indexed."""
		self._queuedMove = _MoveWindow(
			startIndex=5,
			endIndex=7,
			triggerIndex=3
		)
		targetWindow = 9
		# difference is normally 1
		expectedIndex = targetWindow - 1
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))
