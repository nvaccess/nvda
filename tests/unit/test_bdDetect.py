# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the bdDetect module.
"""

import unittest
import bdDetect
from .extensionPointTestHelpers import chainTester
import braille
from utils.blockUntilConditionMet import blockUntilConditionMet


class TestBdDetectExtensionPoints(unittest.TestCase):
	"""A test for the extension points on the bdDetect module."""

	def test_scanForDevices(self):
		with chainTester(
			self,
			bdDetect.scanForDevices,
			[("noBraille", bdDetect.DeviceMatch("", "", "", {}))],
			detectUsb=False,
			detectBluetooth=False,
			limitToDevices=["noBraille"],
		):
			braille.handler._enableDetection(usb=False, bluetooth=False, limitToDevices=["noBraille"])
			# wait for the detector to be terminated.
			success, _endTimeOrNone = blockUntilConditionMet(
				getValue=lambda: braille.handler._detector,
				giveUpAfterSeconds=3.,
				shouldStopEvaluator=lambda detector: detector is None,
			)
			self.assertTrue(success)
