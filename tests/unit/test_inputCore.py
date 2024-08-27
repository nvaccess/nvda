# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the inputCore module."""

import unittest
import inputCore
import keyboardHandler
from .extensionPointTestHelpers import deciderTester


class TestInputManagerExtensionPoints(unittest.TestCase):
	"""A test for the extension points on the input manager."""

	def setUp(self) -> None:
		inputCore.initialize()

	def tearDown(self) -> None:
		inputCore.terminate()

	def test_decide_executeGesture(self):
		gesture = keyboardHandler.KeyboardInputGesture.fromName("NVDA+T")
		with deciderTester(
			self,
			inputCore.decide_executeGesture,
			expectedDecision=False,
			gesture=gesture,
		):
			inputCore.manager.executeGesture(gesture)


class TestGlobalGestureMap(unittest.TestCase):
	"""Test to ensure that importing an exported global gesture map results in the same map.
	The gesture map for the Hims braille display driver is used for reference."""

	def test_exportAndUpdateAreEqual(self):
		from brailleDisplayDrivers.hims import BrailleDisplayDriver as HimsDriver

		exported = HimsDriver.gestureMap.export()
		newMap = inputCore.GlobalGestureMap(exported)
		self.assertEqual(HimsDriver.gestureMap, newMap)
		self.assertDictEqual(HimsDriver.gestureMap._map, newMap._map)
