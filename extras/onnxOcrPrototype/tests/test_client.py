# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# ruff: noqa: I001

from pathlib import Path
import json
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

_PLUGIN_DIRECTORY = Path(__file__).resolve().parents[1] / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype"
sys.path.insert(0, str(_PLUGIN_DIRECTORY))

from client import OcrWorkerClient, OcrWorkerResult, WorkerError


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

	def test_callbackCanSubmitAReplacementRequest(self) -> None:
		completed = threading.Event()
		results = []

		def firstCompleted(result) -> None:
			results.append(result)
			self._client.recognize(
				bytes(range(32)),
				width=4,
				height=2,
				stride=16,
				onResult=lambda replacement: (results.append(replacement), completed.set()),
			)

		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=firstCompleted,
		)
		self.assertTrue(completed.wait(10), "replacement callback timed out")
		self.assertEqual(len(results), 2)
		self.assertTrue(all(isinstance(result, OcrWorkerResult) for result in results))
		self.assertEqual(results[0].metrics["workerProcessId"], results[1].metrics["workerProcessId"])

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

	def test_rejectsUnalignedStride(self) -> None:
		with self.assertRaises(ValueError):
			self._client.recognize(
				bytes(34),
				width=4,
				height=2,
				stride=17,
				onResult=lambda result: None,
			)

	def test_rejectsBooleanAndNonIntegerFrameDimensions(self) -> None:
		for width, height, stride in (
			(True, 2, 16),
			(4, False, 16),
			(4, 2, True),
			(4.0, 2, 16),
		):
			with self.subTest(width=width, height=height, stride=stride), self.assertRaises(ValueError):
				self._client.recognize(
					bytes(range(32)),
					width=width,
					height=height,
					stride=stride,
					onResult=lambda result: None,
				)

	def test_rejectsBooleanTimeoutsAndInvalidTestDelay(self) -> None:
		commonArguments = {
			"workerPython": Path(sys.executable),
			"workerMain": _PLUGIN_DIRECTORY / "workerMain.py",
			"manifestPath": Path("unused"),
			"modelDirectory": Path(self._temporaryDirectory.name),
			"useTestDouble": True,
		}
		for overrides in (
			{"idleTimeoutSeconds": True},
			{"requestTimeoutSeconds": True},
			{"testDoubleDelaySeconds": True},
			{"testDoubleDelaySeconds": float("nan")},
			{"testDoubleDelaySeconds": 11},
		):
			with self.subTest(overrides=overrides), self.assertRaises(ValueError):
				OcrWorkerClient(**commonArguments, **overrides)

	def test_rejectsSecondActiveRequest(self) -> None:
		self._client._testDoubleDelaySeconds = 1
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: None,
		)
		with self.assertRaises(RuntimeError):
			self._client.recognize(
				bytes(range(32)),
				width=4,
				height=2,
				stride=16,
				onResult=lambda result: None,
			)

	def test_idleTimeoutStopsWarmWorker(self) -> None:
		self._client.terminate()
		self._client = OcrWorkerClient(
			workerPython=Path(sys.executable),
			workerMain=_PLUGIN_DIRECTORY / "workerMain.py",
			manifestPath=Path("unused"),
			modelDirectory=Path(self._temporaryDirectory.name),
			useTestDouble=True,
			idleTimeoutSeconds=0.05,
		)
		completed = threading.Event()
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: completed.set(),
		)
		self.assertTrue(completed.wait(10), "worker callback timed out")
		deadline = time.monotonic() + 2
		while self._client.isWorkerRunning and time.monotonic() < deadline:
			time.sleep(0.01)
		self.assertFalse(self._client.isWorkerRunning)

	def test_requestTimeoutReportsErrorAndAllowsRestart(self) -> None:
		self._client._testDoubleDelaySeconds = 1
		self._client._requestTimeoutSeconds = 0.05
		completed = threading.Event()
		results = []
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: (results.append(result), completed.set()),
		)
		self.assertTrue(completed.wait(10), "timeout callback did not run")
		self.assertIsInstance(results[0], WorkerError)
		self.assertIn("timed out", str(results[0]))
		self.assertFalse(self._client.isBusy)
		self.assertFalse(self._client.isWorkerRunning)

		self._client._testDoubleDelaySeconds = 0
		self._client._requestTimeoutSeconds = 10
		restarted = threading.Event()
		restartResults = []
		self._client.recognize(
			bytes(range(32)),
			width=4,
			height=2,
			stride=16,
			onResult=lambda result: (restartResults.append(result), restarted.set()),
		)
		self.assertTrue(restarted.wait(10), "replacement worker callback timed out")
		self.assertIsInstance(restartResults[0], OcrWorkerResult)

	def test_temporaryFrameIsRemovedBeforeCallback(self) -> None:
		writtenFramePaths = []
		originalWriteFrame = self._client._writeFrame

		def recordFrame(frame):
			path = originalWriteFrame(frame)
			writtenFramePaths.append(path)
			return path

		completed = threading.Event()
		callbackSawFrame = []
		with mock.patch.object(self._client, "_writeFrame", side_effect=recordFrame):
			self._client.recognize(
				bytes(range(32)),
				width=4,
				height=2,
				stride=16,
				onResult=lambda result: (
					callbackSawFrame.append(writtenFramePaths[0].exists()),
					completed.set(),
				),
			)
			self.assertTrue(completed.wait(10), "worker callback timed out")
		self.assertEqual(callbackSawFrame, [False])

	def test_parseResponseRejectsMalformedPayloads(self) -> None:
		malformedResults = [
			[],
			{"protocolVersion": 1, "requestId": "id", "result": {"lines": ["not-a-line"]}},
			{
				"protocolVersion": 1,
				"requestId": "id",
				"result": {
					"lines": [[{"x": 0, "y": 0, "width": True, "height": 1, "text": "bad"}]],
				},
			},
			{
				"protocolVersion": 1,
				"requestId": "id",
				"result": {"lines": [], "metrics": {"totalSeconds": float("nan")}},
			},
			{
				"protocolVersion": 1,
				"requestId": "id",
				"result": {
					"lines": [[{"x": 3, "y": 0, "width": 2, "height": 1, "text": "outside"}]],
				},
			},
		]
		for response in malformedResults:
			with self.subTest(response=response), self.assertRaises(WorkerError):
				OcrWorkerClient._parseResponse(
					json.dumps(response),
					"id",
					frameWidth=4,
					frameHeight=2,
				)


if __name__ == "__main__":
	unittest.main()
