# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the nvwave module."""

import unittest
import nvwave
from .extensionPointTestHelpers import deciderTester
import os.path
import globalVars


class TestNVWaveExtensionPoints(unittest.TestCase):
	"""A test for the extension points on the nvwave module."""

	def test_decide_playWaveFile(self):
		kwargs = {
			"fileName": os.path.join(globalVars.appDir, "waves", "start.wav"),
			"asynchronous": False,
			"isSpeechWaveFileCommand": False,
		}
		with deciderTester(
			self,
			nvwave.decide_playWaveFile,
			expectedDecision=False,
			**kwargs,
		):
			nvwave.playWaveFile(**kwargs)
