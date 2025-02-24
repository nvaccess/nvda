import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Tuple

import globalVars
import NVDAState
from logHandler import log


@dataclass
class ProcessConfig:
	name: str  # Process name for logging/debugging
	sourceScriptPath: Path  # Path relative to include dir
	builtExeName: str  # e.g. "nvdaDmp.pyw"
	popenFlags: Dict[str, Any] = field(
		default_factory=lambda: {
			"creationflags": subprocess.CREATE_NO_WINDOW,
			"bufsize": 0,
			"stdin": subprocess.PIPE,
			"stdout": subprocess.PIPE,
		}
	)

	def getSourceCommand(self) -> Tuple[str, str]:
		return (sys.executable, os.path.join(globalVars.appDir, "..", "include", str(self.sourceScriptPath)))

	def getBuiltCommand(self) -> Tuple[str]:
		return (os.path.join(globalVars.appDir, self.builtExeName),)


class SubprocessManager:
	def __init__(self, config: ProcessConfig):
		self._config = config
		self.subprocess = None
		self._lock = Lock()

	def ensureProcessRunning(self):
		"""Ensures process is running, starts if needed. Thread-safe."""
		with self._lock:
			if not self.isRunning():
				self._startProcess()

	def isRunning(self) -> bool:
		"""Check if process is running. Thread-safe."""
		with self._lock:
			return self.subprocess is not None and self.subprocess.poll() is None

	def _startProcess(self):
		"""Internal method to start process using config."""
		if NVDAState.isRunningAsSource():
			command = self._config.getSourceCommand()
		else:
			command = self._config.getBuiltCommand()

		self.subprocess = subprocess.Popen(command, **self._config.popenFlags)

	def terminate(self):
		"""Gracefully terminate process. Thread-safe."""
		with self._lock:
			if self.subprocess:
				try:
					self.subprocess.terminate()
					self.subprocess.wait(timeout=5)
				except Exception:
					log.exception(f"Error terminating {self._config.name} process")
				finally:
					self.subprocess = None
