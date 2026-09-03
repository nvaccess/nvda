# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited.

"""Unit tests for the Screen Curtain enable retry backoff."""

import unittest
from unittest.mock import patch

from screenCurtain._screenCurtain import ScreenCurtain


class Test_EnableRetryBackoff(unittest.TestCase):
	"""Tests that failed attempts to enable Screen Curtain back off exponentially.

	When NVDA starts immediately after sign-in, the screen may still be being
	painted, so verifying that it is black fails. Retrying without any delay
	fails for the same reason each time (#20688).
	"""

	def _enableWithBlackScreenCheck(self, isBlackResults: list[bool]) -> list[float]:
		"""Call ScreenCurtain.enable, returning the delays it slept between attempts.

		:param isBlackResults: The value isScreenFullyBlack should return per attempt.
		:return: The arguments passed to time.sleep, in order.
		"""
		curtain = ScreenCurtain.__new__(ScreenCurtain)
		curtain._enabled = False
		curtain._settings = {"playToggleSounds": False, "enabled": False}
		delays: list[float] = []
		with (
			patch("screenCurtain._screenCurtain.magnification"),
			patch("screenCurtain._screenCurtain.isScreenFullyBlack", side_effect=isBlackResults),
			patch("screenCurtain._screenCurtain.time.sleep", side_effect=delays.append),
			patch.dict("sys.modules", {"_magnifier": unittest.mock.MagicMock(getMagnifier=lambda: None)}),
		):
			try:
				curtain.enable(persist=False)
			except RuntimeError:
				pass
		curtain._enabled = False
		return delays

	def test_noDelayWhenFirstAttemptSucceeds(self):
		"""A successful first attempt should not sleep at all."""
		self.assertEqual(self._enableWithBlackScreenCheck([True]), [])

	def test_delaysDoubleBetweenAttempts(self):
		"""Each retry should wait twice as long as the previous one."""
		delays = self._enableWithBlackScreenCheck([False, False, False])
		self.assertEqual(len(delays), ScreenCurtain._MAX_ENABLE_RETRIES - 1)
		for i, delay in enumerate(delays):
			self.assertAlmostEqual(delay, ScreenCurtain._INITIAL_ENABLE_RETRY_DELAY * 2**i)

	def test_noDelayAfterFinalAttempt(self):
		"""Giving up should not sleep after the last attempt."""
		delays = self._enableWithBlackScreenCheck([False, False, False])
		self.assertLess(len(delays), ScreenCurtain._MAX_ENABLE_RETRIES)

	def test_stopsRetryingOnceScreenIsBlack(self):
		"""A retry that succeeds should not be followed by further delays."""
		self.assertEqual(
			self._enableWithBlackScreenCheck([False, True]),
			[ScreenCurtain._INITIAL_ENABLE_RETRY_DELAY],
		)
