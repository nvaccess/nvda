# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# ruff: noqa: I001

from pathlib import Path
import sys
import unittest

try:
	import numpy
except ImportError:
	numpy = None

_PLUGIN_DIRECTORY = Path(__file__).resolve().parents[1] / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype"
sys.path.insert(0, str(_PLUGIN_DIRECTORY))

from worker.adapter import _Box, OnnxPaddleOcrAdapter


class TestAdapterGeometry(unittest.TestCase):
	def test_groupsAndSortsDetectedBoxesIntoLines(self) -> None:
		boxes = [
			(_Box(50, 5, 80, 15), "second", 0.8),
			(_Box(5, 30, 40, 42), "third", 0.7),
			(_Box(5, 4, 40, 16), "first", 0.9),
		]
		lines = OnnxPaddleOcrAdapter._toLines(boxes)
		self.assertEqual(
			[[word["text"] for word in line] for line in lines],
			[["first", "second"], ["third"]],
		)

	@unittest.skipIf(numpy is None, "NumPy is not installed")
	def test_connectedComponentsUsesForegroundAreaAndScore(self) -> None:
		adapter = object.__new__(OnnxPaddleOcrAdapter)
		adapter._numpy = numpy
		mask = numpy.asarray(
			[
				[False, True, True, False, False, False],
				[False, False, True, True, False, False],
				[False, False, False, False, False, True],
			],
		)
		probabilities = numpy.where(mask, 0.9, 0.0)
		components = adapter._connectedComponents(
			mask,
			probabilities,
			minimumArea=2,
			minimumScore=0.5,
		)
		self.assertEqual(components, [(1, 0, 3, 1)])


if __name__ == "__main__":
	unittest.main()
