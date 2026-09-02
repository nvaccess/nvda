# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sys
import unittest
from pathlib import Path

_PLUGIN_DIRECTORY = Path(__file__).resolve().parents[1] / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype"
sys.path.insert(0, str(_PLUGIN_DIRECTORY))

from capture import getAdaptiveResizeFactor, isCaptureSizeSupported


class TestCaptureSizing(unittest.TestCase):
	def test_normalCaptureIsNotResized(self) -> None:
		self.assertEqual(getAdaptiveResizeFactor(1280, 720), 1)
		self.assertEqual(getAdaptiveResizeFactor(100, 100), 1)

	def test_smallCaptureUsesBoundedUpscaling(self) -> None:
		self.assertEqual(getAdaptiveResizeFactor(300, 80), 4)
		self.assertEqual(getAdaptiveResizeFactor(500, 80), 2.56)
		self.assertEqual(getAdaptiveResizeFactor(1600, 80), 1)

	def test_invalidCaptureIsNotResized(self) -> None:
		for dimensions in ((0, 10), (-1, 10), (True, 10), (10.0, 10)):
			with self.subTest(dimensions=dimensions):
				self.assertEqual(getAdaptiveResizeFactor(*dimensions), 1)

	def test_captureLimitAccepts4kAnd8k(self) -> None:
		self.assertTrue(isCaptureSizeSupported(3840, 2160))
		self.assertTrue(isCaptureSizeSupported(7680, 4320))

	def test_captureLimitRejectsPathologicalOrInvalidSizes(self) -> None:
		for dimensions in (
			(7681, 4320),
			(16385, 1),
			(0, 10),
			(-1, 10),
			(True, 10),
			(10.0, 10),
		):
			with self.subTest(dimensions=dimensions):
				self.assertFalse(isCaptureSizeSupported(*dimensions))


if __name__ == "__main__":
	unittest.main()
