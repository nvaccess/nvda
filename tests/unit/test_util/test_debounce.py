# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited.

import unittest
from unittest.mock import patch

from utils.debounce import debounceLimiter


class _FakeClock:
	def __init__(self):
		self.now = 0.0

	def monotonic(self) -> float:
		return self.now


class _FakeCallLaterHandle:
	def __init__(self, delay: int, callback, args, kwargs):
		self.delay = delay
		self._callback = callback
		self._args = args
		self._kwargs = kwargs
		self._stopped = False
		self._ran = False

	def Stop(self) -> None:
		self._stopped = True

	def run(self) -> None:
		if self._stopped or self._ran:
			return
		self._ran = True
		self._callback(*self._args, **self._kwargs)


class _FakeCallLater:
	def __init__(self):
		self.handles = []

	def __call__(self, delay: int, callback, *args, **kwargs):
		handle = _FakeCallLaterHandle(delay, callback, args, kwargs)
		self.handles.append(handle)
		return handle

	def runPending(self) -> None:
		for handle in self.handles:
			handle.run()


class _Target:
	def __init__(self):
		self.calls = []


class TestDebounceLimiter(unittest.TestCase):
	def setUp(self) -> None:
		self.clock = _FakeClock()
		self.callLater = _FakeCallLater()
		self.monotonicPatch = patch("utils.debounce.monotonic", new=self.clock.monotonic)
		self.deciderPatch = patch("utils.debounce._debounceThreadDecider", return_value=self.callLater)
		self.monotonicPatch.start()
		self.deciderPatch.start()

	def tearDown(self) -> None:
		self.monotonicPatch.stop()
		self.deciderPatch.stop()

	def test_firstCallImmediate_thenDelayedWithinCooldown(self):
		calls = []

		@debounceLimiter(cooldownTimeMs=300, delayTimeMs=200)
		def limited(value):
			calls.append(value)

		self.clock.now = 0.0
		limited("first")
		self.assertEqual(["first"], calls)

		self.clock.now = 0.1
		limited("second")
		self.assertEqual(["first"], calls)

		self.clock.now = 0.4
		self.callLater.runPending()
		self.assertEqual(["first", "second"], calls)

	def test_subsequentCallsWithinCooldown_areCoalesced(self):
		calls = []

		@debounceLimiter(cooldownTimeMs=300, delayTimeMs=200)
		def limited(value):
			calls.append(value)

		self.clock.now = 0.0
		limited("first")
		self.clock.now = 0.1
		limited("second")
		self.clock.now = 0.2
		limited("third")

		self.assertEqual(["first"], calls)
		self.clock.now = 0.5
		self.callLater.runPending()
		self.assertEqual(["first", "third"], calls)

	def test_callAfterCooldown_executesImmediately(self):
		calls = []

		@debounceLimiter(cooldownTimeMs=300, delayTimeMs=200)
		def limited(value):
			calls.append(value)

		self.clock.now = 0.0
		limited("first")
		self.clock.now = 0.4
		limited("second")

		self.assertEqual(["first", "second"], calls)

	def test_methodCalls_areLimitedPerInstance(self):
		@debounceLimiter(cooldownTimeMs=300, delayTimeMs=200)
		def limited(target: _Target, value: str):
			target.calls.append(value)

		target1 = _Target()
		target2 = _Target()

		self.clock.now = 0.0
		limited(target1, "target1-first")
		self.clock.now = 0.1
		limited(target2, "target2-first")

		self.assertEqual(["target1-first"], target1.calls)
		self.assertEqual(["target2-first"], target2.calls)
