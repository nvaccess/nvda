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


if __name__ == "__main__":
	unittest.main()
