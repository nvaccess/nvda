# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# ruff: noqa: I001

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

_PROTOTYPE_DIRECTORY = Path(__file__).resolve().parents[1]
_WORKER_MAIN = _PROTOTYPE_DIRECTORY / "nvdaAddon" / "globalPlugins" / "onnxOcrPrototype" / "workerMain.py"


class TestWorkerMain(unittest.TestCase):
	def test_testDoubleProtocol(self) -> None:
		with tempfile.TemporaryDirectory() as temporaryDirectory:
			framePath = Path(temporaryDirectory) / "frame.bgra"
			framePath.write_bytes(bytes(range(32)))
			request = {
				"protocolVersion": 1,
				"type": "recognize",
				"requestId": "request-1",
				"image": {
					"path": str(framePath),
					"width": 4,
					"height": 2,
					"stride": 16,
				},
				"manifestPath": "unused",
				"modelDirectory": "unused",
			}
			result = subprocess.run(
				[sys.executable, str(_WORKER_MAIN), "--test-double"],
				input=json.dumps(request) + "\n",
				text=True,
				encoding="utf-8",
				capture_output=True,
				check=True,
			)
		response = json.loads(result.stdout)
		self.assertEqual(response["protocolVersion"], 1)
		self.assertEqual(response["requestId"], "request-1")
		self.assertEqual(response["result"]["lines"][0][0]["text"], "OCR test double: 4 by 2 pixels")
		self.assertIsInstance(response["result"]["metrics"]["workerArchitecture"], str)
		self.assertTrue(response["result"]["metrics"]["workerArchitecture"])

	def test_protocolForcesUtf8WhenSystemEncodingCannotRepresentResponse(self) -> None:
		with tempfile.TemporaryDirectory() as temporaryDirectory:
			framePath = Path(temporaryDirectory) / "frame.bgra"
			framePath.write_bytes(bytes(range(32)))
			request = {
				"protocolVersion": 1,
				"type": "recognize",
				"requestId": "请求一",
				"image": {
					"path": str(framePath),
					"width": 4,
					"height": 2,
					"stride": 16,
				},
				"manifestPath": "unused",
				"modelDirectory": "unused",
			}
			environment = os.environ.copy()
			environment["PYTHONIOENCODING"] = "cp1252"
			result = subprocess.run(
				[sys.executable, str(_WORKER_MAIN), "--test-double"],
				input=json.dumps(request, ensure_ascii=False) + "\n",
				text=True,
				encoding="utf-8",
				capture_output=True,
				check=True,
				env=environment,
			)
		response = json.loads(result.stdout)
		self.assertEqual(response["requestId"], "请求一")

	def test_reportsFrameValidationErrorAsProtocolError(self) -> None:
		with tempfile.TemporaryDirectory() as temporaryDirectory:
			framePath = Path(temporaryDirectory) / "frame.bgra"
			framePath.write_bytes(b"short")
			request = {
				"protocolVersion": 1,
				"type": "recognize",
				"requestId": "request-2",
				"image": {
					"path": str(framePath),
					"width": 4,
					"height": 2,
					"stride": 16,
				},
			}
			result = subprocess.run(
				[sys.executable, str(_WORKER_MAIN), "--test-double"],
				input=json.dumps(request) + "\n",
				text=True,
				encoding="utf-8",
				capture_output=True,
				check=True,
			)
		response = json.loads(result.stdout)
		self.assertEqual(response["requestId"], "request-2")
		self.assertEqual(response["error"]["type"], "ValueError")
		self.assertIn("frame size", response["error"]["message"])

	def test_rejectsBooleanImageDimensions(self) -> None:
		with tempfile.TemporaryDirectory() as temporaryDirectory:
			framePath = Path(temporaryDirectory) / "frame.bgra"
			framePath.write_bytes(bytes(range(32)))
			request = {
				"protocolVersion": 1,
				"type": "recognize",
				"requestId": "request-bool",
				"image": {
					"path": str(framePath),
					"width": True,
					"height": 2,
					"stride": 16,
				},
			}
			result = subprocess.run(
				[sys.executable, str(_WORKER_MAIN), "--test-double"],
				input=json.dumps(request) + "\n",
				text=True,
				encoding="utf-8",
				capture_output=True,
				check=True,
			)
		response = json.loads(result.stdout)
		self.assertEqual(response["requestId"], "request-bool")
		self.assertEqual(response["error"]["type"], "ValueError")
		self.assertIn("width", response["error"]["message"])

	def test_invalidShutdownDoesNotStopServing(self) -> None:
		with tempfile.TemporaryDirectory() as temporaryDirectory:
			framePath = Path(temporaryDirectory) / "frame.bgra"
			framePath.write_bytes(bytes(range(32)))
			invalidShutdown = {
				"protocolVersion": 2,
				"type": "shutdown",
				"requestId": "invalid-shutdown",
			}
			recognize = {
				"protocolVersion": 1,
				"type": "recognize",
				"requestId": "request-after-invalid-shutdown",
				"image": {
					"path": str(framePath),
					"width": 4,
					"height": 2,
					"stride": 16,
				},
				"manifestPath": "unused",
				"modelDirectory": "unused",
			}
			result = subprocess.run(
				[sys.executable, str(_WORKER_MAIN), "--test-double", "--serve"],
				input="\n".join((json.dumps(invalidShutdown), json.dumps(recognize))) + "\n",
				text=True,
				encoding="utf-8",
				capture_output=True,
				check=True,
			)
		responses = [json.loads(line) for line in result.stdout.splitlines()]
		self.assertEqual(len(responses), 2)
		self.assertEqual(responses[0]["requestId"], "invalid-shutdown")
		self.assertIn("Unsupported", responses[0]["error"]["message"])
		self.assertEqual(responses[1]["requestId"], "request-after-invalid-shutdown")
		self.assertIn("result", responses[1])


if __name__ == "__main__":
	unittest.main()
