# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the wx.CallAfter monkey patch."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from monkeyPatches import wxMonkeyPatches


class TestCallAfterWakeUp(unittest.TestCase):
	def setUp(self):
		self.queuedCalls = []
		self.wx = SimpleNamespace(CallAfter=self._queueCall)
		self.winUser = SimpleNamespace(WM_NULL=0, PostMessage=MagicMock())
		wxMonkeyPatches.apply(SimpleNamespace(Handle=1234), self.winUser, self.wx)
		self.quotaError = OSError("Not enough quota is available to process this command.")

	def _queueCall(self, func, /, *args, **kwargs):
		self.queuedCalls.append((func, args, kwargs))

	def _runQueuedCalls(self):
		while self.queuedCalls:
			func, args, kwargs = self.queuedCalls.pop(0)
			func(*args, **kwargs)

	def test_wakeUpFailureDoesNotRaise(self):
		"""The call is still made if the main thread's message queue is full (#20846)."""
		self.winUser.PostMessage.side_effect = self.quotaError
		func = MagicMock()
		self.wx.CallAfter(func, 1, kwarg=2)
		self._runQueuedCalls()
		func.assert_called_once_with(1, kwarg=2)

	def test_oneWakeUpPendingAtATime(self):
		funcs = [MagicMock() for _ in range(3)]
		for func in funcs:
			self.wx.CallAfter(func)
		self.winUser.PostMessage.assert_called_once_with(1234, 0, 0, 0)
		self._runQueuedCalls()
		for func in funcs:
			func.assert_called_once_with()
		self.wx.CallAfter(MagicMock())
		self.assertEqual(self.winUser.PostMessage.call_count, 2)

	def test_wakeUpFailureLoggedOncePerEpisode(self):
		with patch("logHandler.log") as log:
			self.winUser.PostMessage.side_effect = self.quotaError
			self.wx.CallAfter(MagicMock())
			self._runQueuedCalls()
			self.wx.CallAfter(MagicMock())
			self._runQueuedCalls()
			self.assertEqual(log.warning.call_count, 1)
			self.winUser.PostMessage.side_effect = None
			self.wx.CallAfter(MagicMock())
			self._runQueuedCalls()
			self.winUser.PostMessage.side_effect = self.quotaError
			self.wx.CallAfter(MagicMock())
			self.assertEqual(log.warning.call_count, 2)

	def test_keywordArgumentNamedFunc(self):
		func = MagicMock()
		self.wx.CallAfter(func, func="value")
		self._runQueuedCalls()
		func.assert_called_once_with(func="value")
