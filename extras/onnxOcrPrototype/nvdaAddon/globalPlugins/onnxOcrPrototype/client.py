# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Asynchronous, cancellable client for the isolated OCR worker process."""

import json
import subprocess
import tempfile
import threading
import uuid
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_PROTOCOL_VERSION = 1
_STDERR_TAIL_LINES = 30


class WorkerError(RuntimeError):
	"""An error reported by, or while communicating with, the OCR worker."""


@dataclass(frozen=True)
class OcrWorkerResult:
	"""Recognition data and worker-side performance measurements."""

	lines: list[list[dict[str, Any]]]
	metrics: dict[str, int | float | str]


@dataclass
class _RequestState:
	requestId: str
	onResult: Callable[[OcrWorkerResult | Exception], None]
	cancelled: bool = False
	framePath: Path | None = None
	process: subprocess.Popen[str] | None = None


class OcrWorkerClient:
	"""Run OCR outside NVDA while retaining a warm worker between requests.

	Only one request is active at a time. Cancellation terminates the worker,
	which interrupts native inference and prevents a stale callback. A successful
	worker remains available until the configurable idle timeout expires.
	"""

	def __init__(
		self,
		*,
		workerMain: Path,
		manifestPath: Path,
		modelDirectory: Path,
		workerPython: Path | None = None,
		workerExecutable: Path | None = None,
		useTestDouble: bool = False,
		testDoubleDelaySeconds: float = 0,
		idleTimeoutSeconds: float = 120,
	) -> None:
		if (workerPython is None) == (workerExecutable is None):
			raise ValueError("Configure exactly one of workerPython or workerExecutable")
		if not 0 <= idleTimeoutSeconds <= 3600:
			raise ValueError("idleTimeoutSeconds must be between 0 and 3600")
		self._workerPython = workerPython
		self._workerExecutable = workerExecutable
		self._workerMain = workerMain
		self._manifestPath = manifestPath
		self._modelDirectory = modelDirectory
		self._useTestDouble = useTestDouble
		self._testDoubleDelaySeconds = testDoubleDelaySeconds
		self._idleTimeoutSeconds = idleTimeoutSeconds
		self._lock = threading.RLock()
		self._active: _RequestState | None = None
		self._process: subprocess.Popen[str] | None = None
		self._idleTimer: threading.Timer | None = None
		self._stderrTail: deque[str] = deque(maxlen=_STDERR_TAIL_LINES)

	@property
	def isBusy(self) -> bool:
		"""Return whether a recognition request is active."""
		with self._lock:
			return self._active is not None

	@property
	def isWorkerRunning(self) -> bool:
		"""Return whether a warm worker process is available."""
		with self._lock:
			return self._process is not None and self._process.poll() is None

	def recognize(
		self,
		frame: bytes,
		*,
		width: int,
		height: int,
		stride: int,
		onResult: Callable[[OcrWorkerResult | Exception], None],
	) -> str:
		"""Submit a BGRA frame without blocking the caller."""
		if width <= 0 or height <= 0 or stride < width * 4:
			raise ValueError("Invalid BGRA frame dimensions")
		if len(frame) != stride * height:
			raise ValueError("BGRA frame length does not match stride and height")
		requestState = _RequestState(requestId=uuid.uuid4().hex, onResult=onResult)
		with self._lock:
			if self._active is not None:
				raise RuntimeError("Only one OCR request can be active")
			self._cancelIdleTimerLocked()
			self._active = requestState
		threading.Thread(
			target=self._runRequest,
			name="onDeviceOcrWorkerClient",
			args=(requestState, frame, width, height, stride),
			daemon=True,
		).start()
		return requestState.requestId

	def cancel(self) -> None:
		"""Cancel the active request, terminate inference and suppress its callback."""
		with self._lock:
			requestState = self._active
			if requestState is not None:
				requestState.cancelled = True
				self._active = None
			process = self._detachProcessLocked()
		self._terminateProcess(process)

	def terminate(self) -> None:
		"""Release worker resources."""
		self.cancel()

	def _runRequest(
		self,
		requestState: _RequestState,
		frame: bytes,
		width: int,
		height: int,
		stride: int,
	) -> None:
		try:
			framePath = self._writeFrame(frame)
			requestState.framePath = framePath
			if self._isCancelled(requestState):
				return
			process = self._ensureProcess()
			requestState.process = process
			if self._isCancelled(requestState):
				self._discardProcess(process)
				return
			request = {
				"protocolVersion": _PROTOCOL_VERSION,
				"type": "recognize",
				"requestId": requestState.requestId,
				"image": {
					"path": str(framePath),
					"width": width,
					"height": height,
					"stride": stride,
				},
				"manifestPath": str(self._manifestPath),
				"modelDirectory": str(self._modelDirectory),
				"testDoubleDelaySeconds": self._testDoubleDelaySeconds,
			}
			assert process.stdin is not None
			assert process.stdout is not None
			process.stdin.write(json.dumps(request, separators=(",", ":")) + "\n")
			process.stdin.flush()
			responseLine = process.stdout.readline()
			if self._isCancelled(requestState):
				return
			if not responseLine:
				detail = self._formatProcessFailure(process)
				raise WorkerError(f"OCR worker exited without a response: {detail}")
			response = self._parseResponse(responseLine, requestState.requestId)
			self._finish(requestState, response)
		except Exception as error:  # noqa: BLE001 - This is the worker-thread error boundary.
			self._discardProcess(requestState.process)
			if not self._isCancelled(requestState):
				self._finish(requestState, error)
		finally:
			if requestState.framePath is not None:
				requestState.framePath.unlink(missing_ok=True)

	def _ensureProcess(self) -> subprocess.Popen[str]:
		with self._lock:
			process = self._process
			if process is not None and process.poll() is None:
				return process
			self._process = None
			self._stderrTail.clear()
			process = subprocess.Popen(
				self._buildCommand(),
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
				encoding="utf-8",
				bufsize=1,
				cwd=str(self._workerMain.parent),
				creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
			)
			self._process = process
			threading.Thread(
				target=self._drainStderr,
				name="onDeviceOcrWorkerStderr",
				args=(process,),
				daemon=True,
			).start()
			return process

	def _buildCommand(self) -> list[str]:
		if self._workerExecutable is not None:
			command = [str(self._workerExecutable), "--serve"]
		else:
			assert self._workerPython is not None
			command = [str(self._workerPython), str(self._workerMain), "--serve"]
		if self._useTestDouble:
			command.append("--test-double")
		return command

	def _drainStderr(self, process: subprocess.Popen[str]) -> None:
		assert process.stderr is not None
		try:
			for line in process.stderr:
				with self._lock:
					if process is self._process:
						self._stderrTail.append(line.rstrip())
		except (OSError, ValueError):
			# The owner closes the pipe while terminating a cancelled worker.
			pass

	def _finish(self, requestState: _RequestState, result: OcrWorkerResult | Exception) -> None:
		with self._lock:
			if requestState.cancelled or self._active is not requestState:
				return
			self._active = None
			self._scheduleIdleTimerLocked()
		requestState.onResult(result)

	def _discardProcess(self, expectedProcess: subprocess.Popen[str] | None) -> None:
		with self._lock:
			if expectedProcess is None or self._process is expectedProcess:
				process = self._detachProcessLocked()
			else:
				process = None
		self._terminateProcess(process)

	def _scheduleIdleTimerLocked(self) -> None:
		self._cancelIdleTimerLocked()
		if self._idleTimeoutSeconds == 0:
			process = self._detachProcessLocked()
			threading.Thread(target=self._terminateProcess, args=(process,), daemon=True).start()
			return
		self._idleTimer = threading.Timer(self._idleTimeoutSeconds, self._expireIdleWorker)
		self._idleTimer.daemon = True
		self._idleTimer.start()

	def _expireIdleWorker(self) -> None:
		with self._lock:
			if self._active is not None:
				return
			process = self._detachProcessLocked()
		self._terminateProcess(process)

	def _cancelIdleTimerLocked(self) -> None:
		if self._idleTimer is not None:
			self._idleTimer.cancel()
			self._idleTimer = None

	def _detachProcessLocked(self) -> subprocess.Popen[str] | None:
		self._cancelIdleTimerLocked()
		process = self._process
		self._process = None
		return process

	@staticmethod
	def _terminateProcess(process: subprocess.Popen[str] | None) -> None:
		if process is None:
			return
		try:
			if process.poll() is None:
				try:
					process.terminate()
				except OSError:
					return
				try:
					process.wait(timeout=1)
				except subprocess.TimeoutExpired:
					try:
						process.kill()
						process.wait(timeout=1)
					except (OSError, subprocess.TimeoutExpired):
						pass
		finally:
			for stream in (process.stdin, process.stdout, process.stderr):
				if stream is not None:
					try:
						stream.close()
					except OSError:
						pass

	def _formatProcessFailure(self, process: subprocess.Popen[str]) -> str:
		with self._lock:
			detail = "\n".join(self._stderrTail)[-2000:]
		return detail or f"exit code {process.poll()}"

	def _isCancelled(self, requestState: _RequestState) -> bool:
		with self._lock:
			return requestState.cancelled

	@staticmethod
	def _writeFrame(frame: bytes) -> Path:
		with tempfile.NamedTemporaryFile(
			prefix="nvda-on-device-ocr-",
			suffix=".bgra",
			delete=False,
		) as frameFile:
			frameFile.write(frame)
			return Path(frameFile.name)

	@staticmethod
	def _parseResponse(responseLine: str, expectedRequestId: str) -> OcrWorkerResult:
		try:
			response = json.loads(responseLine)
		except json.JSONDecodeError as error:
			raise WorkerError("OCR worker returned invalid JSON") from error
		if response.get("protocolVersion") != _PROTOCOL_VERSION:
			raise WorkerError("OCR worker protocol version did not match")
		if response.get("requestId") != expectedRequestId:
			raise WorkerError("OCR worker response request ID did not match")
		if "error" in response:
			error = response["error"]
			if not isinstance(error, dict):
				raise WorkerError("OCR worker returned an invalid error response")
			raise WorkerError(f"{error.get('type', 'WorkerError')}: {error.get('message', 'Unknown error')}")
		result = response.get("result")
		if not isinstance(result, dict) or not isinstance(result.get("lines"), list):
			raise WorkerError("OCR worker response did not contain result lines")
		metrics = result.get("metrics", {})
		if not isinstance(metrics, dict):
			raise WorkerError("OCR worker response metrics were invalid")
		return OcrWorkerResult(lines=result["lines"], metrics=metrics)
