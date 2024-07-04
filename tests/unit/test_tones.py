# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the tones module."""

import unittest
import tones
from .extensionPointTestHelpers import deciderTester


class TestTonesExtensionPoints(unittest.TestCase):
	"""A test for the extension points on the tones module."""

	def setUp(self) -> None:
		tones.initialize()

	def tearDown(self) -> None:
		tones.terminate()

	def test_decide_beep(self):
		kwargs = {
			"hz": 440.0,
			"length": 500,
			"left": 50,
			"right": 50,
			"isSpeechBeepCommand": False,
		}
		with deciderTester(
			self,
			tones.decide_beep,
			expectedDecision=False,
			**kwargs,
		):
			tones.beep(**kwargs)
