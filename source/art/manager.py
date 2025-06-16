# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import json
import subprocess
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Optional

import Pyro5.api
from logHandler import log
from processManager import ProcessConfig, SubprocessManager

from .core.services.config import ConfigService
from .core.services.globalVars import GlobalVarsService
from .core.services.languageHandler import LanguageHandlerService
from .core.services.logging import LoggingService
from .core.services.nvwave import NVWaveService
from .core.services.speech import SpeechService
from .core.services.ui import UIService

if TYPE_CHECKING:
	from .services.extensionPoints import ExtensionPointProxy

# Global ART manager instance
_artManager: Optional["ARTManager"] = None


def getARTManager() -> Optional["ARTManager"]:
	"""Get the global ART manager instance, if available."""
	return _artManager


def setARTManager(manager: Optional["ARTManager"]) -> None:
	"""Set the global ART manager instance."""
	global _artManager
	_artManager = manager


ART_CONFIG = ProcessConfig(
	name="NVDA ART",
	sourceScriptPath=Path("nvda_art.pyw"),
	builtExeName="nvda_art.pyw",
	popenFlags={
		"creationflags": subprocess.CREATE_NO_WINDOW,
		"bufsize": 0,
		"stdin": subprocess.PIPE,
		"stdout": subprocess.PIPE,
		"stderr": subprocess.PIPE,
	},
)


class ARTAddonProcess:
	"""Manages a single ART process for one addon."""

	def __init__(self, addon_spec: dict, core_service_uris: Dict[str, str]):
		self.addon_spec = addon_spec
		self.addon_name = addon_spec["name"]
		self.core_service_uris = core_service_uris
		self.subprocessManager = SubprocessManager(ART_CONFIG)
		self.artServices: Dict[str, Pyro5.api.Proxy] = {}
		self._shutdownEvent = threading.Event()

	def start(self) -> bool:
		"""Start the ART process for this addon."""
		log.info(f"Starting ART process for addon: {self.addon_name}")

		try:
			self._startProcessWithHandshake()
			return True
		except Exception:
			log.exception(f"Failed to start ART process for addon {self.addon_name}")
			self.subprocessManager.terminate()
			return False

	def _startProcessWithHandshake(self):
		"""Start ART process and perform JSON handshake."""
		self.subprocessManager.ensureProcessRunning()

		if not self.subprocessManager.subprocess:
			raise RuntimeError(f"Failed to start ART subprocess for {self.addon_name}")

		# Send startup data
		startup_data = {
			"addon": self.addon_spec,
			"core_services": self.core_service_uris,
			"config": {
				"debug": getattr(__import__("globalVars").appArgs, "debugLogging", False),
			},
		}

		startup_json = json.dumps(startup_data) + "\n"
		self.subprocessManager.subprocess.stdin.write(startup_json.encode("utf-8"))
		self.subprocessManager.subprocess.stdin.flush()

		# Read response
		response_line = self.subprocessManager.subprocess.stdout.readline().decode("utf-8")
		response_data = json.loads(response_line.strip())

		if response_data.get("status") == "ready":
			self._connectToARTServices(response_data.get("art_services", {}))
			log.info(f"ART process started successfully for {self.addon_name}")
		else:
			raise RuntimeError(f"ART startup failed for {self.addon_name}")


	def _connectToARTServices(self, service_uris: Dict[str, str]):
		"""Connect to ART services using provided URIs."""
		for service_name, uri in service_uris.items():
			try:
				proxy = Pyro5.api.Proxy(uri)
				proxy._pyroTimeout = 2.0
				self.artServices[service_name] = proxy
				log.info(f"Connected to ART service for {self.addon_name}: {service_name}")
			except Exception:
				log.exception(f"Failed to connect to ART service for {self.addon_name}: {service_name}")

	def stop(self):
		"""Stop this ART process."""
		log.info(f"Stopping ART process for addon {self.addon_name}")

		for proxy in self.artServices.values():
			try:
				proxy._pyroRelease()
			except Exception:
				pass

		self.artServices.clear()
		self.subprocessManager.terminate()

	def getService(self, name: str) -> Optional[Pyro5.api.Proxy]:
		"""Get a proxy to an ART service."""
		return self.artServices.get(name)


class ARTManager:
	"""Manages multiple NVDA Add-on Runtime processes."""

	def __init__(self):
		self.addonProcesses: Dict[str, ARTAddonProcess] = {}
		self.coreDaemon: Optional[Pyro5.api.Daemon] = None
		self.coreDaemonThread: Optional[threading.Thread] = None
		self.configService: Optional[ConfigService] = None
		self.loggingService: Optional[LoggingService] = None
		self.globalVarsService: Optional[GlobalVarsService] = None
		self.nvwaveService: Optional[NVWaveService] = None
		self.languageHandlerService: Optional[LanguageHandlerService] = None
		self.uiService = None  # Will be initialized in _registerCoreServices
		self.speechService: Optional[SpeechService] = None
		self._shutdownEvent = threading.Event()

	def start(self):
		"""Start the ART manager and register core services."""
		log.info("Starting NVDA ART manager")

		# Register as global instance
		setARTManager(self)

		# Register core services first
		self._registerCoreServices()

	def _registerCoreServices(self):
		"""Register core services that run in NVDA process."""
		self.coreDaemon = Pyro5.api.Daemon(host="127.0.0.1", port=0)

		self.configService = ConfigService()
		self.loggingService = LoggingService()
		self.globalVarsService = GlobalVarsService()
		self.nvwaveService = NVWaveService()
		self.languageHandlerService = LanguageHandlerService()
		self.uiService = UIService()
		self.speechService = SpeechService()  # Add this line

		config_uri = self.coreDaemon.register(self.configService, "nvda.core.config")
		logging_uri = self.coreDaemon.register(self.loggingService, "nvda.core.logging")
		globalvars_uri = self.coreDaemon.register(self.globalVarsService, "nvda.core.globalvars")
		nvwave_uri = self.coreDaemon.register(self.nvwaveService, "nvda.core.nvwave")
		language_uri = self.coreDaemon.register(self.languageHandlerService, "nvda.core.language")
		ui_uri = self.coreDaemon.register(self.uiService, "nvda.core.ui")
		speech_uri = self.coreDaemon.register(self.speechService, "nvda.core.speech")  # Add this line

		log.info(f"ConfigService registered at: {config_uri}")
		log.info(f"LoggingService registered at: {logging_uri}")
		log.info(f"GlobalVarsService registered at: {globalvars_uri}")
		log.info(f"NVWaveService registered at: {nvwave_uri}")
		log.info(f"LanguageHandlerService registered at: {language_uri}")
		log.info(f"UIService registered at: {ui_uri}")
		log.info(f"SpeechService registered at: {speech_uri}")  # Add this line

		self.coreDaemonThread = threading.Thread(target=self._runCoreDaemon, name="ARTCoreDaemon")
		self.coreDaemonThread.daemon = True
		self.coreDaemonThread.start()

	def _runCoreDaemon(self):
		"""Run the core daemon request loop."""
		log.debug("Starting core daemon request loop")
		self.coreDaemon.requestLoop(lambda: not self._shutdownEvent.is_set())
		log.debug("Core daemon request loop finished")

	def _getCoreServiceURIs(self) -> Dict[str, str]:
		"""Get URIs for all registered core services."""
		uris = {}
		for obj_id, (obj, _) in self.coreDaemon.objectsById.items():
			if obj_id.startswith("nvda.core."):
				service_name = obj_id.split(".", 2)[2]
				uri = f"PYRO:{obj_id}@{self.coreDaemon.locationStr.split('@')[1]}"
				uris[service_name] = uri
		return uris

	def startAddonProcess(self, addon_spec: dict) -> bool:
		"""Start an ART process for a specific addon."""
		addon_name = addon_spec["name"]

		if addon_name in self.addonProcesses:
			log.warning(f"ART process for addon {addon_name} already exists")
			return True

		process = ARTAddonProcess(addon_spec, self._getCoreServiceURIs())
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

		if self.coreDaemon:
			self.coreDaemon.shutdown()

		if self.coreDaemonThread:
			self.coreDaemonThread.join(timeout=5.0)

	def stopAddonProcess(self, addon_name: str):
		"""Stop a specific addon's ART process."""
		if addon_name in self.addonProcesses:
			self.addonProcesses[addon_name].stop()
			del self.addonProcesses[addon_name]

	def getAddonProcess(self, addon_name: str) -> Optional[ARTAddonProcess]:
		"""Get the ART process for a specific addon."""
		return self.addonProcesses.get(addon_name)

	def getExtensionPointProxy(self) -> Optional["ExtensionPointProxy"]:
		"""Get the extension point proxy for invoking ART handlers."""
		if not hasattr(self, "_extensionPointProxy"):
			from .services.extensionPoints import ExtensionPointProxy

			self._extensionPointProxy = ExtensionPointProxy(self)
		return self._extensionPointProxy

	def isAddonRunning(self, addon_name: str) -> bool:
		"""Check if an addon's ART process is running."""
		process = self.addonProcesses.get(addon_name)
		return process is not None and process.subprocessManager.isRunning()
