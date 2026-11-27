# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the winInputHook module."""

import ctypes
import unittest
from unittest.mock import patch

import winInputHook


class TestGetCurrentKeyEventDelay(unittest.TestCase):
	"""Tests for winInputHook._getCurrentKeyEventDelay."""

	def _delay(self, eventTime: int | None, tickCount: int) -> int | None:
		with (
			patch.object(winInputHook, "_currentKeyEventTime", eventTime),
			patch.object(winInputHook.kernel32, "GetTickCount", return_value=tickCount),
		):
			return winInputHook._getCurrentKeyEventDelay()

	def test_noEventBeingHandled(self) -> None:
		self.assertIsNone(self._delay(None, 5000))

	def test_delay(self) -> None:
		self.assertEqual(self._delay(5000, 7400), 2400)

	def test_tickCountWrappedAround(self) -> None:
		self.assertEqual(self._delay(0xFFFFFF00, 0x100), 0x200)

	def test_eventTimeClearedAfterCallback(self) -> None:
		"""Both blocked and passed key events leave no timestamp behind for direct callers."""

		def callback(*args) -> bool:
			delays.append(winInputHook._getCurrentKeyEventDelay())
			return passThrough

		for flags in (0, winInputHook.LLKHF_UP):
			for passThrough in (False, True):
				with self.subTest(flags=flags, passThrough=passThrough):
					event = winInputHook.KBDLLHOOKSTRUCT(vkCode=ord("A"), flags=flags, time=5000)
					delays = []

					with (
						patch.object(winInputHook, "keyDownCallback", callback),
						patch.object(winInputHook, "keyUpCallback", callback),
						patch.object(winInputHook.kernel32, "GetTickCount", return_value=5010),
						patch.object(winInputHook.user32, "CallNextHookEx", return_value=0) as callNext,
					):
						result = winInputHook.keyboardHook(winInputHook.HC_ACTION, 0, ctypes.addressof(event))
					self.assertEqual(result, 0 if passThrough else 1)
					self.assertEqual(delays, [10])
					self.assertEqual(callNext.call_count, int(passThrough))
					self.assertIsNone(winInputHook._getCurrentKeyEventDelay())
