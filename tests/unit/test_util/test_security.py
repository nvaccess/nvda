# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule.
"""

import unittest
from unittest.mock import patch

from utils.security import (
	_getWindowZIndex,
)
import winUser


class _Test_getWindowZIndex(unittest.TestCase):
	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
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
		self._getDesktopWindowPatch = patch("winUser.getDesktopWindow", lambda: 0)  # value is discarded by _getTopWindowPatch
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
	_triggered = False

	def _getWindow_patched(self, hwnd: winUser.HWNDVal, relation: int) -> int:
		self._moveIndexToNewIndexAtIndexOnce(self._windows.index(hwnd))
		result = super()._getWindow_patched(hwnd, relation)
		return result

	def _moveIndexToNewIndexAtIndexOnce(self, currentIndex: int):
		from logging import getLogger
		
		getLogger().error(f"{currentIndex}")
		if currentIndex == self._triggerIndex and not self._triggered:
			self._triggered = True
			window = self._windows.pop(self._startIndex)
			self._windows.insert(self._endIndex, window)

	def test_prev_windowMoves_pastTarget(self):
		"""A previous window is moved past the target window. This does not affect the z-order."""
		self._startIndex = 2  # A window at this index
		self._endIndex = 9  # is moved to this index
		self._triggerIndex = 5  # when this index is reached
		targetWindow = 7
		expectedIndex = targetWindow - 1
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_prev_windowMoves_beforeTarget(self):
		"""A previous window is moved before the target window. It is counted twice."""
		self._startIndex = 2
		self._endIndex = 5
		self._triggerIndex = 3
		targetWindow = 7
		expectedIndex = targetWindow  # difference is normally 1, however a window is counted twice
		self.assertEqual(expectedIndex, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_active_windowMoves_pastTarget(self):
		"""A window we are looking at moves past the match, skipping our target window."""
		self._startIndex = 3
		self._endIndex = 8
		self._triggerIndex = 3
		targetWindow = 6
		self.assertEqual(None, _getWindowZIndex(self._windowMatches(targetWindow)))

	def test_active_windowMoves_beforeTarget(self):
		pass

	def test_future_windowMoves_pastTarget(self):
		pass

	def test_future_windowMoves_beforeTarget(self):
		pass
