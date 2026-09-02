# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""JSON-lines entry point for the isolated on-device OCR worker."""

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any

from worker.adapter import OnnxPaddleOcrAdapter, TestDoubleAdapter
from worker.modelManager import ModelManager


def _parseArguments() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--test-double",
		action="store_true",
		help="Return deterministic OCR output without importing NumPy or ONNX Runtime.",
	)
	parser.add_argument(
		"--serve",
		action="store_true",
		help="Keep the worker alive and process requests until stdin closes.",
	)
	return parser.parse_args()


def _readRequest(requestLine: str) -> dict[str, Any]:
	request = json.loads(requestLine)
	if not isinstance(request, dict):
		raise TypeError("Worker request must be an object")
	return request


def _handleRequest(
	request: dict[str, Any],
	*,
	useTestDouble: bool,
	adapterCache: dict[tuple[str, str], OnnxPaddleOcrAdapter],
) -> tuple[list[list[dict[str, int | str | float]]], dict[str, int | float | str]]:
	preparationStartedAt = time.perf_counter()
	if request.get("protocolVersion") != 1:
		raise ValueError("Unsupported worker protocol version")
	if request.get("type") != "recognize":
		raise ValueError("Worker request type must be 'recognize'")
	image = request.get("image")
	if not isinstance(image, dict):
		raise TypeError("Worker request image must be an object")
	framePath = Path(_requiredString(image, "path"))
	width = _requiredPositiveInt(image, "width")
	height = _requiredPositiveInt(image, "height")
	stride = _requiredPositiveInt(image, "stride")
	if useTestDouble:
		delay = request.get("testDoubleDelaySeconds", 0)
		if not isinstance(delay, (int, float)) or delay < 0 or delay > 10:
			raise ValueError("testDoubleDelaySeconds must be between 0 and 10")
		adapter = TestDoubleAdapter(float(delay))
		sessionCacheHit = True
	else:
		manifestPath = Path(_requiredString(request, "manifestPath"))
		modelDirectory = Path(_requiredString(request, "modelDirectory"))
		cacheKey = (str(manifestPath.resolve()), str(modelDirectory.resolve()))
		adapter = adapterCache.get(cacheKey)
		sessionCacheHit = adapter is not None
		if adapter is None:
			modelBundle = ModelManager(modelDirectory).ensureModels(manifestPath)
			adapter = OnnxPaddleOcrAdapter(modelBundle)
			adapterCache[cacheKey] = adapter
	preparationSeconds = time.perf_counter() - preparationStartedAt
	lines = adapter.recognizeFrame(
		framePath,
		width=width,
		height=height,
		stride=stride,
	)
	metrics = dict(adapter.lastMetrics)
	metrics.update(
		{
			"preparationSeconds": preparationSeconds,
			"sessionCacheHit": sessionCacheHit,
			"workerProcessId": os.getpid(),
		},
	)
	return lines, metrics


def _requiredString(value: dict[str, Any], key: str) -> str:
	result = value.get(key)
	if not isinstance(result, str) or not result:
		raise ValueError(f"{key} must be a non-empty string")
	return result


def _requiredPositiveInt(value: dict[str, Any], key: str) -> int:
	result = value.get(key)
	if not isinstance(result, int) or result <= 0:
		raise ValueError(f"{key} must be a positive integer")
	return result


def _processRequestLine(
	requestLine: str,
	*,
	useTestDouble: bool,
	adapterCache: dict[tuple[str, str], OnnxPaddleOcrAdapter],
) -> bool:
	"""Process one request line. Return ``False`` after a shutdown request."""
	requestId: str | None = None
	try:
		request = _readRequest(requestLine)
		if request.get("type") == "shutdown":
			print(
				json.dumps(
					{"protocolVersion": 1, "requestId": request.get("requestId"), "result": "shutdown"},
					separators=(",", ":"),
				),
				flush=True,
			)
			return False
		rawRequestId = request.get("requestId")
		if not isinstance(rawRequestId, str) or not rawRequestId:
			raise ValueError("requestId must be a non-empty string")
		requestId = rawRequestId
		lines, metrics = _handleRequest(
			request,
			useTestDouble=useTestDouble,
			adapterCache=adapterCache,
		)
		response: dict[str, Any] = {
			"protocolVersion": 1,
			"requestId": requestId,
			"result": {"lines": lines, "metrics": metrics},
		}
	except Exception as error:  # noqa: BLE001 - This is the protocol error boundary.
		traceback.print_exc(file=sys.stderr)
		response = {
			"protocolVersion": 1,
			"requestId": requestId,
			"error": {
				"type": type(error).__name__,
				"message": str(error),
			},
		}
	print(json.dumps(response, ensure_ascii=False, separators=(",", ":")), flush=True)
	return True


def main() -> int:
	"""Process one request, or serve requests until stdin closes."""
	arguments = _parseArguments()
	adapterCache: dict[tuple[str, str], OnnxPaddleOcrAdapter] = {}
	if arguments.serve:
		for requestLine in sys.stdin:
			if requestLine.strip() and not _processRequestLine(
				requestLine,
				useTestDouble=arguments.test_double,
				adapterCache=adapterCache,
			):
				break
	else:
		requestLine = sys.stdin.readline()
		if not requestLine:
			raise ValueError("No worker request was provided")
		_processRequestLine(
			requestLine,
			useTestDouble=arguments.test_double,
			adapterCache=adapterCache,
		)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
