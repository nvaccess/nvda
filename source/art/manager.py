# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sysconfig
import base64
import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import NVDAState
from logHandler import log
from secureProcess import SecurePopen


# Global ART manager instance
_artManager: Optional["ARTManager"] = None


def getARTManager() -> Optional["ARTManager"]:
	"""Get the global ART manager instance, if available."""
	return _artManager


def setARTManager(manager: Optional["ARTManager"]) -> None:
	"""Set the global ART manager instance."""
	global _artManager
	_artManager = manager

launchConfig_standard = {
	"removeElevation": True,
	"removePrivileges": True,
	"integrityLevel": "low",
	"applyUIRestrictions": True,
	"restrictToken": True,
	"retainUserInRestrictedToken": True,
}
launchConfig_secure = {
	"username": "local service",
	"domain": "nt authority",
	"logonType": "service",
	"appContainerName": "nvdaSecureART",
	"appContainerCapabilities": [],
	"isolateWindowStation": True,
	"applyUIRestrictions": True,
}


class ARTAddonProcess:
	"""Manages a single ART process for one addon."""

	def _getRuntimeArgv(self, runtimeName: str):
		if NVDAState.isRunningAsSource():
			if (
				(runtimeName =='amd64' and sysconfig.get_platform() == 'win-amd64')
				or (runtimeName == 'x86' and sysconfig.get_platform() == 'win32')
			):
				# Running from source, use the current Python interpreter
				return [sys.executable, "nvda_art.pyw"]
		runtimeExe = _runtimeRegistry.get(runtimeName)
		if not runtimeExe:
			raise RuntimeError(f"Runtime {runtimeName} not registered")
		return [runtimeExe]

	def __init__(self, addon_spec: dict, core_service_uris: Dict[str, str]):
		self.addon_spec = addon_spec
		self.addon_name = addon_spec["name"]
		runtime = addon_spec['manifest']['runtime']
		self._runtimeArgv = self._getRuntimeArgv(runtime)
		if not self._runtimeArgv:
			raise RuntimeError(f"Runtime {runtime} not registered")
		log.debug(f"using runtime {runtime}: {self._runtimeArgv}")
		self._shutdownEvent = threading.Event()

	def _isRunningOnSecureDesktop(self) -> bool:
		"""Check if we're running on Windows secure desktop."""
		try:
			from utils.security import isRunningOnSecureDesktop

			return isRunningOnSecureDesktop()
		except ImportError:
			# Fallback if import fails
			return False

	def start(self) -> bool:
		"""Start the ART process for this addon."""
		log.info(f"Starting ART process for addon: {self.addon_name}")

		try:
			self._startProcessWithHandshake()
			return True
		except Exception:
			log.exception(f"Failed to start ART process for addon {self.addon_name}")
			self.sp.terminate()
			return False

	def _startProcessWithHandshake(self):
		"""Start ART process and perform JSON handshake."""
		log.debug(f"Starting ART subprocess for {self.addon_name}")
		isSecure = self._isRunningOnSecureDesktop()
		launch
		self.sp = SecurePopen(
			self._runtimeArgv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, killOnDelete=True,
			**(launchConfig_secure if isSecure else launchConfig_standard)
		)
		# Log subprocess details
		log.info(f"ART subprocess started for {self.addon_name}: PID={self.sp.pid}")
		log.debug(f"ART subprocess command line: {self.sp.args}")

	def stop(self):
		"""Stop this ART process."""
		log.info(f"Stopping ART process for addon {self.addon_name}")

		self.sp.terminate()


class ARTManager:
	"""Manages multiple NVDA Add-on Runtime processes."""

	def __init__(self):
		self.addonProcesses: Dict[str, ARTAddonProcess] = {}
		self._shutdownEvent = threading.Event()

	def start(self):
		"""Start the ART manager and register core services."""
		log.info("Starting NVDA ART manager")

		# Register as global instance
		setARTManager(self)

	def startAddonProcess(self, addon_spec: dict) -> bool:
		"""Start an ART process for a specific addon."""
		addon_name = addon_spec["name"]

		if addon_name in self.addonProcesses:
			log.warning(f"ART process for addon {addon_name} already exists")
			return True

		process = ARTAddonProcess(addon_spec)
		if process.start():
			self.addonProcesses[addon_name] = process
			return True
		return False

	def stop(self):
		"""Stop all ART processes."""
		log.info("Stopping NVDA ART manager")

		setARTManager(None)

		self._shutdownEvent.set()

		# Stop all addon processes
		for addon_name, process in list(self.addonProcesses.items()):
			try:
				process.stop()
			except Exception:
				log.exception(f"Error stopping ART process for {addon_name}")
		self.addonProcesses.clear()

	def stopAddonProcess(self, addon_name: str):
		"""Stop a specific addon's ART process."""
		if addon_name in self.addonProcesses:
			self.addonProcesses[addon_name].stop()
			del self.addonProcesses[addon_name]

	def getAddonProcess(self, addon_name: str) -> Optional[ARTAddonProcess]:
		"""Get the ART process for a specific addon."""
		return self.addonProcesses.get(addon_name)

	def isAddonRunning(self, addon_name: str) -> bool:
		"""Check if an addon's ART process is running."""
		process = self.addonProcesses.get(addon_name)
		return process is not None and process.sp.isRunning()

	def getAvailableSynthList(self) -> List[Tuple[str, str]]:
		"""Get list of available ART synthesizers.

		@return: List of (name, description) tuples for ART synths
		"""
		log.debug("ARTManager.getAvailableSynthList() called")
		synth_list = []

		# Scan sys.modules for ART-generated synthesizer proxy modules
		log.debug(f"Scanning {len(sys.modules)} modules for ART synth proxies")
		art_proxy_modules = []
		for module_name, module in sys.modules.copy().items():
			if module_name.startswith("synthDrivers.") and hasattr(module, "SynthDriver"):
				synth_name = module_name.split(".", 1)[1]  # Remove "synthDrivers." prefix
				synth_class = module.SynthDriver
				log.debug(f"Found synthDrivers module: {module_name}, class: {synth_class}")

				# Check if this is an ART proxy synthesizer
				if hasattr(synth_class, "_artAddonName") and hasattr(synth_class, "_artSynthName"):
					art_proxy_modules.append(module_name)
					log.debug(f"Found ART proxy synth: {synth_name} from addon {synth_class._artAddonName}")

					# Verify the addon is still running
					addon_running = self.isAddonRunning(synth_class._artAddonName)
					log.debug(f"Addon {synth_class._artAddonName} running: {addon_running}")
					if addon_running:
						try:
							# Use the class check() method to verify availability
							check_result = synth_class.check()
							log.debug(f"Synth {synth_name} check() result: {check_result}")
							if check_result:
								description = getattr(synth_class, "description", synth_name)
								synth_list.append((synth_name, description))
								log.debug(f"Added {synth_name} to available synth list")
							else:
								log.debug(f"ART synth {synth_name} failed check(), excluding from list")
						except Exception:
							# If check() fails, skip this synth
							log.debug(
								f"ART synth {synth_name} failed check() with exception, excluding from list",
								exc_info=True,
							)
					else:
						log.debug(f"ART synth {synth_name} excluded - addon not running")

		log.debug(f"Found {len(art_proxy_modules)} ART proxy modules: {art_proxy_modules}")
		log.debug(f"Returning {len(synth_list)} available ART synths: {synth_list}")
		return synth_list

_runtimeRegistry = {
	'amd64': 'nvda_art.exe',
	'x86': os.path.join(NVDAState.ReadPaths.versionedLibX86Path, "art-runtime", "nvda_art.exe"),
}
