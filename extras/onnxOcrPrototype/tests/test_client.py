# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# ruff: noqa: I001

from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest

_PLUGIN_DIRECTORY = Path(__file__).resolve().parents[1] / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype"
sys.path.insert(0, str(_PLUGIN_DIRECTORY))

from client import OcrWorkerClient, OcrWorkerResult


class TestOcrWorkerClient(unittest.TestCase):
	def setUp(self) -> None:
		self._temporaryDirectory = tempfile.TemporaryDirectory()
		self.addCleanup(self._temporaryDirectory.cleanup)
		self._client = OcrWorkerClient(
			workerPython=Path(sys.executable),
			workerMain=_PLUGIN_DIRECTORY / "workerMain.py",
			manifestPath=Path("unused"),
			modelDirectory=Path(self._temporaryDirectory.name),
			useTestDouble=True,
		)
		self.addCleanup(self._client.terminate)

	def test_recognizeReturnsAsynchronously(self) -> None:
		completed = threading.Event()
		results = []
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: (results.append(result), completed.set()),
		)
		self.assertTrue(completed.wait(10), "worker callback timed out")
		self.assertFalse(self._client.isBusy)
		self.assertIsInstance(results[0], OcrWorkerResult)
		self.assertEqual(results[0].lines[0][0]["text"], "OCR test double: 4 by 2 pixels")
		self.assertEqual(results[0].metrics["provider"], "test-double")
		self.assertTrue(self._client.isWorkerRunning)

	def test_reusesWarmWorkerForSequentialRequests(self) -> None:
		workerProcessIds = []
		for _ in range(2):
			completed = threading.Event()
			results = []

			def storeResult(result, *, resultList=results, event=completed):
				resultList.append(result)
				event.set()

			self._client.recognize(
				bytes(range(32)),
				width=4,
				height=2,
				stride=16,
				onResult=storeResult,
			)
			self.assertTrue(completed.wait(10), "worker callback timed out")
			self.assertIsInstance(results[0], OcrWorkerResult)
			workerProcessIds.append(results[0].metrics["workerProcessId"])
			self.assertTrue(self._client.isWorkerRunning)
		self.assertEqual(workerProcessIds[0], workerProcessIds[1])

	def test_cancelSuppressesCallback(self) -> None:
		self._client._testDoubleDelaySeconds = 2
		completed = threading.Event()
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: completed.set(),
		)
		time.sleep(0.1)
		self._client.cancel()
		self.assertFalse(self._client.isBusy)
		self.assertFalse(completed.wait(0.5))
		self.assertFalse(self._client.isWorkerRunning)

	def test_canRecognizeAfterCancellation(self) -> None:
		self._client._testDoubleDelaySeconds = 2
		cancelledCompleted = threading.Event()
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: cancelledCompleted.set(),
		)
		time.sleep(0.1)
		self._client.cancel()
		self._client._testDoubleDelaySeconds = 0
		completed = threading.Event()
		results = []
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: (results.append(result), completed.set()),
		)
		self.assertTrue(completed.wait(10), "replacement worker callback timed out")
		self.assertFalse(cancelledCompleted.is_set())
		self.assertIsInstance(results[0], OcrWorkerResult)

	def test_rejectsMismatchedFrameLength(self) -> None:
		with self.assertRaises(ValueError):
			self._client.recognize(
				b"short",
				width=4,
				height=2,
				stride=16,
				onResult=lambda result: None,
			)


if __name__ == "__main__":
	unittest.main()
