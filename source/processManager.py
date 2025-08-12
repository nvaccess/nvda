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
	sandbox_enabled: bool = False  # Whether to run process in sandbox
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
		self._sandbox_temp_dir = None
		self._lock = Lock()

	def ensureProcessRunning(self):
		"""Ensures process is running, starts if needed. Thread-safe."""
		log.debug(f"Acquiring lock to ensure {self._config.name} process is running")
		with self._lock:
			log.debug(f"Lock acquired for {self._config.name}, checking if running")
			if not self._isRunningUnsafe():
				log.debug(f"Process {self._config.name} not running, starting")
				self._startProcess()
			else:
				log.debug(f"Process {self._config.name} already running")

	def _isRunningUnsafe(self) -> bool:
		"""Check if process is running. NOT thread-safe - assumes lock is held."""
		return self.subprocess is not None and self.subprocess.poll() is None

	def isRunning(self) -> bool:
		"""Check if process is running. Thread-safe."""
		with self._lock:
			return self._isRunningUnsafe()

	def _startProcess(self):
		"""Internal method to start process using config."""
		if NVDAState.isRunningAsSource():
			command = self._config.getSourceCommand()
		else:
			command = self._config.getBuiltCommand()
		log.debug(f"Starting {self._config.name} process with command: {command}")

		# Use sandboxing if enabled
		if self._config.sandbox_enabled:
			log.info(f"ART process launching WITH sandbox restrictions enabled")
			from sandbox import SandboxConfig, SandboxPopen
			import tempfile

			# Create temp dir for process communication
			self._sandbox_temp_dir = tempfile.mkdtemp(prefix="nvda_sandbox_")
			log.info(f"Created sandbox temp directory: {self._sandbox_temp_dir}")

			# Create sandbox config for ART process
			sandbox_config = SandboxConfig()
			sandbox_config.enable_sid_restrictions = True
			sandbox_config.restrict_user_sid = False
			sandbox_config.enable_restricted_token = True
			sandbox_config.enable_low_integrity = False
			sandbox_config.enable_ui_restrictions = True
			sandbox_config.enable_process_limits = False  # Allow subprocess creation for ART


			self.subprocess = SandboxPopen(
				command,
				config=sandbox_config,
				allowed_directory=self._sandbox_temp_dir,
				**self._config.popenFlags
			)
			log.info(f"Successfully started {self._config.name} in sandbox with PID: {self.subprocess.pid}")
		else:
			log.info(f"ART process launching WITHOUT sandbox restrictions (regular subprocess)")
			self.subprocess = subprocess.Popen(command, **self._config.popenFlags)
			log.info(f"Successfully started {self._config.name} process with PID: {self.subprocess.pid}")

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

			# Clean up sandbox temp directory
			if self._sandbox_temp_dir:
				import shutil
				try:
					shutil.rmtree(self._sandbox_temp_dir)
					log.debug(f"Cleaned up sandbox temp directory: {self._sandbox_temp_dir}")
				except Exception:
					log.warning(f"Failed to clean up sandbox temp directory: {self._sandbox_temp_dir}")
				finally:
					self._sandbox_temp_dir = None
