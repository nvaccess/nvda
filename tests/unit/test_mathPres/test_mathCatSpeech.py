# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for converting MathCAT speech to NVDA speech commands."""

import unittest
from unittest.mock import MagicMock, patch

from mathPres.MathCAT import speech
from speech.commands import BreakCommand


class TestConvertSSMLTextForNVDA(unittest.TestCase):
	def _convert(self, rate: int) -> list:
		synth = MagicMock()
		synth._get_rate.return_value = rate
		synth.supportedCommands = {BreakCommand}
		with (
			patch.object(speech, "getSynth", return_value=synth),
			patch.object(speech, "getLanguageToUse", return_value="en"),
			patch.object(speech, "getCurrentLanguage", return_value="en"),
		):
			return speech.convertSSMLTextForNVDA("<break time='180ms'/>")

	def test_rateZero_doesNotRaise(self):
		commands = self._convert(0)
		self.assertIsInstance(commands[0], BreakCommand)

	def test_breakScalesWithRate(self):
		testCases = [
			(1, 180 * 90),
			(50, 180 * 180 // 100),
			(100, 180 * 180 // 200),
		]
		for rate, expectedTime in testCases:
			with self.subTest(rate=rate):
				self.assertEqual(self._convert(rate)[0].time, expectedTime)

	def test_rateZeroMatchesLowestNonZeroRate(self):
		self.assertEqual(self._convert(0)[0].time, self._convert(1)[0].time)
