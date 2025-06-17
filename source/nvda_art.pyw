import argparse
import concurrent.futures
import json
import logging
import os
import sys
import threading
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Configure Pyro5 before any imports
import Pyro5.config
Pyro5.config.SERIALIZER = "json"
Pyro5.config.COMMTIMEOUT = 2.0
Pyro5.config.HOST = "127.0.0.1"
Pyro5.config.MAX_MESSAGE_SIZE = 1024 * 1024

import Pyro5.api
import wx

# Import ART logging configuration
from art.runtime.services.addons import AddOnLifecycleService

__version__ = "0.1.0"
# Logger will be configured after we know the addon name
logger = None

global wxApp
global mainWindow
global artRuntime

wxApp: wx.App


class ExtensionPointType(Enum):
	ACTION = "action"
	FILTER = "filter"
	DECIDER = "decider"
	ACCUMULATING_DECIDER = "accumulating_decider"
	CHAIN = "chain"


@Pyro5.api.expose
class ExtensionPointHandlerService:
	"""Service for executing extension point handlers in ART."""

	def __init__(self):
		self._handlers: Dict[str, List[Tuple[str, Callable]]] = {}
		self.logger = logging.getLogger("ART.ExtensionPointHandlerService")
		self._runtime = None  # Will be set when registered

	@property
	def extensionPointService(self):
		"""Get the extension point service from runtime."""
		if self._runtime and hasattr(self._runtime, "services"):
			return self._runtime.services.get("extension_points")
		return None

	def registerHandler(self, extPointName: str, handlerFunc: Callable, epType: str) -> str:
		"""Register a handler function for an extension point."""
		# Get addon name from runtime
		addonId = artRuntime.addon_spec["name"] if artRuntime and artRuntime.addon_spec else "unknown"
		handlerID = f"{addonId}_{id(handlerFunc)}"

		if extPointName not in self._handlers:
			self._handlers[extPointName] = []

		self._handlers[extPointName].append((handlerID, handlerFunc))

		if self.extensionPointService:
			self.extensionPointService.registerHandler(addonId, extPointName, handlerID, epType)

		self.logger.info(f"Registered handler {handlerID} for {extPointName}")
		return handlerID

	def executeHandlers(self, extPointName: str, epType: str, *args: Any, **kwargs: Any) -> Any:
		"""Execute all handlers for an extension point."""
		if extPointName not in self._handlers:
			return self._getDefaultResult(epType, *args)

		results = []
		for handlerId, handlerFunc in self._handlers[extPointName]:
			try:
				result = handlerFunc(*args, **kwargs)
				results.append(result)
			except Exception:
				self.logger.exception(f"Error in handler {handlerId}")

		return self._combineResults(epType, results)

	def _getDefaultResult(self, epType: str, *args: Any) -> Any:
		"""Get default result for extension point type."""
		if epType == "action":
			return None
		elif epType == "decider":
			return True
		elif epType == "accumulating_decider":
			return True
		elif epType == "filter":
			return args[0] if args else None
		elif epType == "chain":
			return []
		return None

	def _combineResults(self, epType: str, results: List[Any]) -> Any:
		"""Combine results based on extension point type."""
		if epType == "action":
			return None
		elif epType == "decider":
			return all(results) if results else True
		elif epType == "accumulating_decider":
			return not any(not r for r in results)
		elif epType == "filter":
			if not results:
				return None
			value = results[0]
			for result in results[1:]:
				if result is not None:
					value = result
			return value
		elif epType == "chain":
			flattened = []
			for result in results:
				if isinstance(result, list):
					flattened.extend(result)
				else:
					flattened.append(result)
			return flattened
		return results


@Pyro5.api.expose
class ExtensionPointService:
	def __init__(self):
		self._addonHandlers: Dict[str, set] = {}

	def registerHandler(self, addonID: str, extPointName: str, handlerId: str, extPointType: str) -> bool:
		try:
			ExtensionPointType(extPointType)  # Validate the type
		except ValueError:
			return False

		if addonID not in self._addonHandlers:
			self._addonHandlers[addonID] = set()
		self._addonHandlers[addonID].add(f"{extPointName}:{handlerId}")

		return True

	def unregisterHandler(self, addonId: str, extPointName: str, handlerId: str) -> bool:
		if addonId in self._addonHandlers:
			self._addonHandlers[addonId].discard(f"{extPointName}:{handlerId}")
			return True
		return False


class ARTRuntime:
	"""Main runtime manager for the ART process."""

	def __init__(self, addon_spec=None):
		self.addon_spec = addon_spec
		addon_name = addon_spec["name"] if addon_spec else "unknown"
		self.logger = logging.getLogger(f"ART.ARTRuntime.{addon_name}")
		self.daemon: Optional[Pyro5.api.Daemon] = None
		self.services: Dict[str, Any] = {}  # Store all services
		self.service_uris: Dict[str, str] = {}  # Store all URIs
		self.executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
		self.daemonFuture: Optional[concurrent.futures.Future] = None
		self._shutdownEvent = threading.Event()

	def _register_service(self, service_name: str, service_instance: Any, pyro_name: str) -> None:
		"""Register a service with Pyro and store its URI."""
		uri = self.daemon.register(service_instance, pyro_name)
		self.services[service_name] = service_instance
		self.service_uris[service_name] = str(uri)
		self.logger.info(f"{service_name} registered at: {uri}")

	def start(self) -> Dict[str, str]:
		"""Start the ART runtime services."""
		self.daemon = Pyro5.api.Daemon(host="127.0.0.1", port=0)
		self.logger.info(f"Pyro5 daemon created at: {self.daemon.locationStr}")

		# Define services to register
		service_definitions = [
			("addon_lifecycle", AddOnLifecycleService(self.addon_spec), "nvda.art.addon_lifecycle"),
			("extension_points", ExtensionPointService(), "nvda.art.extension_points"),
			("handlers", ExtensionPointHandlerService(), "nvda.art.handlers"),
		]

		# Import and add synth service
		from art.runtime.services.synth import SynthService

		service_definitions.append(("synth", SynthService(), "nvda.art.synth"))

		# Register all services
		for service_name, service_instance, pyro_name in service_definitions:
			# Set runtime reference for services that need it
			if hasattr(service_instance, "_runtime"):
				service_instance._runtime = self
			self._register_service(service_name, service_instance, pyro_name)

		self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="ARTDaemon")
		self.daemonFuture = self.executor.submit(self._daemonLoop)
		self.logger.info("ART runtime started successfully")

		# Load the addon now that services are ready
		addon_service = self.services.get("addon_lifecycle")
		if self.addon_spec and addon_service:
			if not addon_service.loadAddonIfNeeded():
				self.logger.error("Failed to load addon after services were ready")
				# Continue anyway - services are still available

		return self.service_uris

	def _daemonLoop(self):
		"""Run the Pyro5 daemon request loop."""
		self.logger.info("Starting Pyro5 daemon request loop")
		self.logger.debug(f"Daemon location: {self.daemon.locationStr}")

		try:
			self.daemon.requestLoop(lambda: not self._shutdownEvent.is_set())
		except Exception:
			self.logger.exception("Exception in daemon request loop")
			raise
		finally:
			self.logger.info("Pyro5 daemon request loop finished")

	def shutdown(self):
		"""Shutdown the ART runtime."""
		self.logger.info("Shutting down ART runtime")
		self._shutdownEvent.set()

		if self.daemon:
			self.daemon.shutdown()

		if self.daemonFuture:
			try:
				self.daemonFuture.result(timeout=5.0)
			except concurrent.futures.TimeoutError:
				self.logger.warning("Daemon did not shutdown within timeout")
			except Exception as e:
				self.logger.warning(f"Exception during daemon shutdown: {e}")

		if self.executor:
			self.executor.shutdown(wait=True)


class MainWindow(wx.Frame):
	"""Main window for the NVDA ART application."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.SetTitle("NVDA ART")
		self.Bind(wx.EVT_CLOSE, self.onClose)

	def onClose(self, event):
		if logger:
			logger.info("Closing NVDA ART main window.")
		if artRuntime:
			artRuntime.shutdown()
		self.Destroy()
		wxApp.ExitMainLoop()


mainWindow: MainWindow
artRuntime: ARTRuntime


def handleStartupError(error: Exception, addon_name: str = "unknown") -> None:
	"""Common error handling for startup failures."""
	error_msg = f"ERROR: Startup failed: {error}"

	if logger:
		logger.exception("Startup failed")
	else:
		print(error_msg, file=sys.stderr)
		import traceback

		traceback.print_exc()

	# If we're in handshake mode (stdin available), send error response
	if not sys.stdin.isatty():
		try:
			error_response = {
				"status": "error",
				"error": str(error),
				"details": f"Exception during ART startup: {type(error).__name__}",
				"addon_name": addon_name,
			}
			error_json = json.dumps(error_response) + "\n"
			sys.stdout.write(error_json)
			sys.stdout.flush()
		except Exception:
			print("ERROR: Failed to send error response", file=sys.stderr)


def _set_core_service_uris(core_services: Dict[str, str]) -> None:
	"""Set environment variables for core service URIs."""
	for service_name, uri in core_services.items():
		env_var = f"NVDA_ART_{service_name.upper()}_SERVICE_URI"
		os.environ[env_var] = uri


def getStartupInfo() -> Tuple[Optional[dict], bool]:
	"""Get addon spec and mode from either CLI args or stdin handshake.
	
	Returns:
		(addon_spec, is_cli_mode) or (None, is_cli_mode) on error
	"""
	is_cli_mode = len(sys.argv) > 1
	
	if is_cli_mode:
		# CLI mode - parse arguments
		try:
			parser = argparse.ArgumentParser()
			parser.add_argument("--addon-path", required=True)
			parser.add_argument("--addon-name")
			parser.add_argument("--debug", action="store_true")
			args = parser.parse_args()

			addon_path = Path(args.addon_path).resolve()
			addon_name = args.addon_name or addon_path.name

			# Set debug mode if specified
			if args.debug:
				os.environ["NVDA_ART_DEBUG"] = "1"

			addon_spec = {
				"name": addon_name,
				"path": str(addon_path),
				"manifest": {},  # Don't care about manifest details for now
			}
			
			return addon_spec, is_cli_mode
			
		except Exception as e:
			handleStartupError(e)
			return None, is_cli_mode
	else:
		# Handshake mode - read from stdin
		try:
			startup_line = sys.stdin.readline().strip()
			if not startup_line:
				# Can't log yet, just print to stderr
				print("ERROR: No startup data received from NVDA Core", file=sys.stderr)
				return None, is_cli_mode

			startup_data = json.loads(startup_line)

			# Extract and apply configuration
			config = startup_data.get("config", {})
			if config.get("debug", False):
				os.environ["NVDA_ART_DEBUG"] = "1"

			if config_path := config.get("configPath"):
				os.environ["NVDA_ART_CONFIG_PATH"] = config_path

			# Set core service URIs
			_set_core_service_uris(startup_data.get("core_services", {}))

			# Get addon spec
			addon_spec = startup_data.get("addon")
			if not addon_spec:
				raise ValueError("No addon specified")
				
			return addon_spec, is_cli_mode

		except Exception as e:
			addon_name = startup_data.get("addon", {}).get("name", "unknown") if "startup_data" in locals() else "unknown"
			handleStartupError(e, addon_name)
			return None, is_cli_mode


def performStartup(addon_spec: dict, is_cli_mode: bool) -> Optional[Dict[str, str]]:
	"""Perform startup with the given addon spec."""
	try:
		# Start services
		service_uris = startWithAddonSpec(addon_spec)
		
		# Send handshake response if not in CLI mode
		if not is_cli_mode:
			response_data = {"status": "ready", "addon_name": addon_spec["name"], "art_services": service_uris}
			response_json = json.dumps(response_data) + "\n"
			sys.stdout.write(response_json)
			sys.stdout.flush()
			
		return service_uris
		
	except Exception as e:
		handleStartupError(e, addon_spec.get("name", "unknown"))
		return None


def startWithAddonSpec(addon_spec: dict) -> Dict[str, str]:
	"""Common startup logic for both CLI and handshake."""
	global logger

	# Set addon name in environment for components that need it
	os.environ["NVDA_ART_ADDON_NAME"] = addon_spec["name"]

	# Configure logging for this ART instance - send to stdout
	debug_mode = os.environ.get("NVDA_ART_DEBUG", "").lower() in ("1", "true", "yes")

	# Set up stdout logging instead of using art.runtime.logging
	log_level = logging.DEBUG if debug_mode else logging.INFO
	logging.basicConfig(
		level=log_level,
		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
		stream=sys.stdout,
		force=True,  # Override any existing configuration
	)

	logger = logging.getLogger(f"ART.{addon_spec['name']}")

	# Log startup information
	logger.info(f"Starting ART for addon: {addon_spec['name']}")
	logger.info(f"Addon path: {addon_spec.get('path', 'Unknown')}")
	logger.debug(f"Full addon spec: {addon_spec}")

	# Set up proxies - add the art directory so we can import art.runtime.proxies
	art_path = Path(__file__).parent / "art"
	sys.path.insert(0, str(art_path))
	logger.debug(f"Added art to path: {art_path}")

	# Import and set up proxy modules in sys.modules so addons can import them directly
	try:
		# Import all proxy modules
		from art.runtime.proxies import (
			ui,
			config,
			logHandler,
			globalVars,
			addonHandler,
			languageHandler,
			nvwave,
			extensionPoints,
			appModules,
			brailleDisplayDrivers,
			globalPlugins,
			synthDrivers,
			visionEnhancementProviders,
			synthDriverHandler,
			speech,
		)

		# Define module mappings with any special submodules
		PROXY_MODULE_REGISTRY = {
			# Main modules
			"ui": ui,
			"config": config,
			"logHandler": logHandler,
			"globalVars": globalVars,
			"addonHandler": addonHandler,
			"languageHandler": languageHandler,
			"nvwave": nvwave,
			"extensionPoints": extensionPoints,
			"appModules": appModules,
			"brailleDisplayDrivers": brailleDisplayDrivers,
			"globalPlugins": globalPlugins,
			"synthDrivers": synthDrivers,
			"visionEnhancementProviders": visionEnhancementProviders,
			"synthDriverHandler": synthDriverHandler,
			"speech": speech,
			# Submodules
			"speech.commands": speech.commands,
			"speech.types": speech.types,
		}

		# Register all modules in sys.modules
		for module_name, module_obj in PROXY_MODULE_REGISTRY.items():
			sys.modules[module_name] = module_obj
			logger.debug(f"Registered proxy module: {module_name}")

		# Initialize addonHandler proxy with addon info
		addonHandler.initialize(addon_spec)
		logger.info(f"Initialized addonHandler proxy for addon: {addon_spec['name']}")
	except Exception:
		logger.exception("Failed to set up proxy modules")

	global artRuntime
	artRuntime = ARTRuntime(addon_spec)  # Pass addon spec to runtime
	return artRuntime.start()


def main():
	"""Initialize the NVDA ART Runtime."""
	global wxApp, mainWindow

	# Get startup info
	addon_spec, is_cli_mode = getStartupInfo()
	if not addon_spec:
		sys.exit(1)
		
	# Perform startup
	service_uris = performStartup(addon_spec, is_cli_mode)
	if not service_uris:
		sys.exit(1)

	# Initialize wx application
	wxApp = wx.App(False, useBestVisual=False)
	wxApp.SetAppName("NVDA ART")
	wxApp.SetVendorName("NV Access")

	# Create main window (visible only in CLI mode)
	mainWindow = MainWindow(None, title="NVDA ART")
	if is_cli_mode:
		mainWindow.Show()
	else:
		mainWindow.Hide()

	if logger:
		logger.info(f"Starting NVDA ART version {__version__}")

	try:
		wxApp.MainLoop()
	finally:
		if artRuntime:
			artRuntime.shutdown()


if __name__ == "__main__":
	main()
