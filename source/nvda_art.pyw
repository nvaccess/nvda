import argparse
import concurrent.futures
import datetime
import faulthandler
import json
import logging
import logging.handlers
import os
import sys
import tempfile
import threading
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import Pyro5
import Pyro5.api
import wx
from art.runtime.services.addons import AddOnLifecycleService

# Set up crash log file for faulthandler
crash_log_file = os.path.join(
	tempfile.gettempdir(), f"nvda_art_crash_{os.getpid()}_{datetime.datetime.now():%Y%m%d-%H%M%S}.log"
)


class StreamToLogger(object):
	"""Fake file-like stream object that redirects writes to a logger instance."""

	def __init__(self, handler):
		self.handler = handler

	def fileno(self):
		return self.handler.stream.fileno()

	def write(self, data):
		self.handler.stream.write(data)
		self.handler.stream.flush()

	def flush(self):
		self.handler.stream.flush()


# Set up file-based logging FIRST so we can use it for crash logging
log_file = os.path.join(
	tempfile.gettempdir(), f"nvda_art_{os.getpid()}_{datetime.datetime.now():%Y%m%d-%H%M%S}.log"
)

# Create rotating file handler
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=3, encoding="utf-8")

# Configure file logging
logging.basicConfig(
	handlers=[handler],
	level=logging.DEBUG,
	format="%(asctime)s | %(levelname)-8s | pid=%(process)d | %(name)s | %(message)s",
	force=True,
)

# Create ART logger
art_logger = logging.getLogger("ART.Main")

# Set up crash logging with faulthandler
try:
	# Enable faulthandler with file output
	crash_file_handle = open(crash_log_file, "w", buffering=1)
	faulthandler.enable(file=crash_file_handle, all_threads=True)
	art_logger.info(f"ART Crash Log: {crash_log_file}")
except Exception as e:
	art_logger.error(f"Failed to set up crash logging: {e}")
	# Fallback to stderr
	faulthandler.enable(all_threads=True)


# Keep original streams for JSON handshake
original_stdout = sys.stdout
original_stderr = sys.stderr

# Log startup information immediately
art_logger.info("=== ART PROCESS STARTED ===")
art_logger.info(f"Process ID: {os.getpid()}")
art_logger.info(f"Command line: {sys.argv}")
art_logger.info(f"Current working directory: {os.getcwd()}")
art_logger.info(f"Python executable: {sys.executable}")
art_logger.info(f"Python version: {sys.version}")
art_logger.info(f"Log file: {log_file}")
art_logger.info(f"sys.path: {sys.path}")

# Also print log file location to stderr for easy discovery
print(f"ART Debug Log: {log_file}", file=original_stderr)

# Log environment variables related to ART
art_logger.info("ART Environment variables:")
for key, value in os.environ.items():
	if "NVDA" in key or "ART" in key:
		art_logger.info(f"  {key} = {value}")

Pyro5.config.SERIALIZER = "json"
Pyro5.config.COMMTIMEOUT = 0.0
Pyro5.config.HOST = "127.0.0.1"
#Pyro5.config.MAX_MESSAGE_SIZE = 4 * 1024 * 1024  # 4MB for large audio data
Pyro5.config.THREADPOOL_SIZE = 16  # More threads to handle concurrent requests
Pyro5.config.SERVERTYPE = "thread"  # Use thread server type (not threadpool)

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

	def registerHandler(self, extPointName: str, handlerFunc: Callable, epType: ExtensionPointType) -> str:
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

	def executeHandlers(
		self, extPointName: str, epType: ExtensionPointType, *args: Any, **kwargs: Any
	) -> Any:
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

	def _getDefaultResult(self, epType: ExtensionPointType, *args: Any) -> Any:
		"""Get default result for extension point type."""
		match epType:
			case ExtensionPointType.ACTION:
				return None
			case ExtensionPointType.DECIDER:
				return True
			case ExtensionPointType.ACCUMULATING_DECIDER:
				return True
			case ExtensionPointType.FILTER:
				return args[0] if args else None
			case ExtensionPointType.CHAIN:
				return []
			case _:
				return None

	def _combineResults(self, epType: ExtensionPointType, results: List[Any]) -> Any:
		"""Combine results based on extension point type."""
		match epType:
			case ExtensionPointType.ACTION:
				return None
			case ExtensionPointType.DECIDER:
				return all(results) if results else True
			case ExtensionPointType.ACCUMULATING_DECIDER:
				return not any(not r for r in results)
			case ExtensionPointType.FILTER:
				if not results:
					return None
				value = results[0]
				for result in results[1:]:
					if result is not None:
						value = result
				return value
			case ExtensionPointType.CHAIN:
				flattened = []
				for result in results:
					if isinstance(result, list):
						flattened.extend(result)
					else:
						flattened.append(result)
				return flattened
			case _:
				return results


@Pyro5.api.expose
class ExtensionPointService:
	def __init__(self):
		self._addonHandlers: Dict[str, set] = {}

	def registerHandler(
		self, addonID: str, extPointName: str, handlerId: str, extPointType: ExtensionPointType
	) -> bool:
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

		# Create an event to signal when daemon is ready to accept connections
		daemon_ready_event = threading.Event()

		self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="ARTDaemon")
		self.daemonFuture = self.executor.submit(self._daemonLoop, daemon_ready_event)

		# Wait for daemon to signal it's ready (with timeout)
		self.logger.debug("Waiting for Pyro5 daemon to be ready...")
		ready = daemon_ready_event.wait(timeout=10.0)
		if not ready:
			self.logger.critical("Pyro5 daemon failed to initialize within timeout")
			self.shutdown()
			raise RuntimeError("Daemon startup timeout")

		self.logger.info("ART runtime started successfully - daemon is ready")

		# Load the addon now that services are ready
		addon_service = self.services.get("addon_lifecycle")
		if self.addon_spec and addon_service:
			if not addon_service.loadAddonIfNeeded():
				self.logger.error("Failed to load addon after services were ready")
				# Continue anyway - services are still available

		return self.service_uris

	def _daemonLoop(self, ready_event: threading.Event):
		"""Run the Pyro5 daemon request loop."""
		self.logger.info("Starting Pyro5 daemon request loop")
		self.logger.debug(f"Daemon location: {self.daemon.locationStr}")

		try:
			# Signal that daemon is ready to accept connections before starting the loop
			self.logger.debug("Pyro5 daemon is ready - signaling main thread")
			ready_event.set()

			# Start the request loop (this blocks until shutdown)
			self.logger.info(
				"About to enter daemon.requestLoop() - this is where ART might terminate unexpectedly"
			)
			self.daemon.requestLoop(lambda: not self._shutdownEvent.is_set())
			self.logger.info("daemon.requestLoop() exited normally")
		except Exception as e:
			self.logger.exception(
				f"CRITICAL: Exception in daemon request loop - this will terminate ART: {e}"
			)
			# Try to log some extra info before we die
			import traceback

			self.logger.error(f"Full traceback: {''.join(traceback.format_tb(e.__traceback__))}")
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
	art_logger.info(f"=== MODE DETECTION: {'CLI' if is_cli_mode else 'HANDSHAKE'} ===")
	art_logger.debug(f"Command line arguments: {sys.argv}")

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
			art_logger.info("=== HANDSHAKE MODE: Starting stdin processing ===")
			art_logger.debug("About to read startup line from stdin")

			startup_line = sys.stdin.readline().strip()
			art_logger.debug(
				f"Raw startup line received (length={len(startup_line)}): {startup_line[:200]}..."
			)

			if not startup_line:
				art_logger.error("No startup data received from NVDA Core")
				print("ERROR: No startup data received from NVDA Core", file=sys.stderr)
				return None, is_cli_mode

			art_logger.debug("About to parse JSON from startup line")
			startup_data = json.loads(startup_line)
			art_logger.info(
				f"Successfully parsed startup data: addon={startup_data.get('addon', {}).get('name', 'unknown')}"
			)
			art_logger.debug(f"Full startup data keys: {list(startup_data.keys())}")

			# Extract and apply configuration
			config = startup_data.get("config", {})
			art_logger.debug(f"Config section: {config}")

			if config.get("debug", False):
				art_logger.debug("Setting NVDA_ART_DEBUG=1 from config")
				os.environ["NVDA_ART_DEBUG"] = "1"

			if config_path := config.get("configPath"):
				art_logger.debug(f"Setting NVDA_ART_CONFIG_PATH={config_path}")
				os.environ["NVDA_ART_CONFIG_PATH"] = config_path

			# Set core service URIs
			core_services = startup_data.get("core_services", {})
			art_logger.debug(f"Setting {len(core_services)} core service environment variables")
			_set_core_service_uris(core_services)
			art_logger.debug("Core service URIs set in environment")

			# Get addon spec
			addon_spec = startup_data.get("addon")
			if not addon_spec:
				art_logger.error("No addon specification found in startup data")
				raise ValueError("No addon specified")

			art_logger.info(
				f"Successfully processed handshake for addon: {addon_spec.get('name', 'unknown')}"
			)
			art_logger.debug(f"Addon spec keys: {list(addon_spec.keys())}")

			return addon_spec, is_cli_mode

		except json.JSONDecodeError as e:
			art_logger.error(f"Failed to parse JSON from startup line: {e}")
			art_logger.debug(f"Problematic line: {startup_line}")
			handleStartupError(e, "unknown")
			return None, is_cli_mode
		except Exception as e:
			addon_name = (
				startup_data.get("addon", {}).get("name", "unknown")
				if "startup_data" in locals()
				else "unknown"
			)
			art_logger.error(f"Exception in handshake processing: {e}")
			art_logger.exception("Full handshake exception traceback")
			handleStartupError(e, addon_name)
			return None, is_cli_mode


def performStartup(addon_spec: dict, is_cli_mode: bool) -> Optional[Dict[str, str]]:
	"""Perform startup with the given addon spec."""
	try:
		art_logger.info(
			f"=== PERFORMING STARTUP: mode={'CLI' if is_cli_mode else 'HANDSHAKE'}, addon={addon_spec.get('name', 'unknown')} ==="
		)

		# Start services
		art_logger.debug("About to call startWithAddonSpec()")
		service_uris = startWithAddonSpec(addon_spec)
		art_logger.info(f"startWithAddonSpec() completed successfully, got {len(service_uris)} service URIs")

		# Send handshake response if not in CLI mode
		if not is_cli_mode:
			art_logger.debug("Preparing handshake response")
			response_data = {
				"status": "ready",
				"addon_name": addon_spec["name"],
				"art_services": service_uris,
			}
			response_json = json.dumps(response_data) + "\n"
			art_logger.debug(
				f"Handshake response prepared (length={len(response_json)}): {response_json[:200]}..."
			)

			art_logger.debug("Writing handshake response to stdout")
			sys.stdout.write(response_json)
			art_logger.debug("Flushing stdout")
			sys.stdout.flush()
			art_logger.info("Handshake response sent successfully")
			
			# Redirect stdout/stderr to prevent pipe buffer deadlock
			art_logger.debug("Redirecting stdout/stderr to prevent pipe buffer deadlock")
			import os
			sys.stdout = open(os.devnull, 'w')
			sys.stderr = open(os.devnull, 'w')

		return service_uris

	except Exception as e:
		art_logger.error(f"Exception in performStartup(): {e}")
		art_logger.exception("Full performStartup exception traceback")
		handleStartupError(e, addon_spec.get("name", "unknown"))
		return None


def startWithAddonSpec(addon_spec: dict) -> Dict[str, str]:
	"""Common startup logic for both CLI and handshake."""
	global logger

	art_logger.info("=== startWithAddonSpec() ENTRY ===")
	art_logger.debug(f"Addon spec: {addon_spec}")

	# Set addon name in environment for components that need it
	art_logger.debug("Setting NVDA_ART_ADDON_NAME environment variable")
	os.environ["NVDA_ART_ADDON_NAME"] = addon_spec["name"]
	art_logger.debug("Environment variable set successfully")

	# Don't reconfigure logging - we already have it set up
	art_logger.debug("Checking debug mode")
	debug_mode = os.environ.get("NVDA_ART_DEBUG", "").lower() in ("1", "true", "yes")
	art_logger.debug(f"Debug mode: {debug_mode}")
	art_logger.debug("Skipping logging.basicConfig - already configured")

	logger = logging.getLogger(f"ART.{addon_spec['name']}")

	# Log startup information
	logger.info(f"Starting ART for addon: {addon_spec['name']}")
	logger.info(f"Addon path: {addon_spec.get('path', 'Unknown')}")
	logger.debug(f"Full addon spec: {addon_spec}")

	# Set up proxies - add the art directory so we can import art.runtime.proxies
	if getattr(sys, "frozen", None) is None:
		# Running from source
		art_path = Path(__file__).parent / "art"
	else:
		# Running as py2exe executable
		art_path = Path(sys.prefix) / "art"
	sys.path.insert(0, str(art_path))
	logger.debug(f"Added art to path: {art_path}")

	# Import and set up proxy modules in sys.modules so addons can import them directly
	try:
		# Import all proxy modules
		from art.runtime.proxies import (
			addonHandler,
			appModules,
			brailleDisplayDrivers,
			config,
			extensionPoints,
			globalPlugins,
			globalVars,
			languageHandler,
			logHandler,
			nvwave,
			speech,
			synthDriverHandler,
			synthDrivers,
			ui,
			visionEnhancementProviders,
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

		# Set up global translation functions for compatibility
		# This ensures pgettext and other functions are available globally
		addon = addonHandler.getCodeAddon()
		if addon:
			translations = addon.getTranslationsInstance()
			languageHandler.setGlobalTranslation(translations)
			logger.info("Set up global translation functions")
	except Exception:
		logger.exception("Failed to set up proxy modules")

	global artRuntime
	artRuntime = ARTRuntime(addon_spec)  # Pass addon spec to runtime

	# Register the runtime instance with art.runtime for clean API access
	import art.runtime

	art.runtime.setRuntime(artRuntime)

	return artRuntime.start()


def main():
	"""Initialize the NVDA ART Runtime."""
	global wxApp, mainWindow

	art_logger.info("=== ART MAIN STARTING ===")
	art_logger.debug(f"Command line args: {sys.argv}")

	# Get startup info
	art_logger.debug("About to call getStartupInfo()")
	addon_spec, is_cli_mode = getStartupInfo()
	art_logger.info(
		f"getStartupInfo() returned: is_cli_mode={is_cli_mode}, addon_spec={'present' if addon_spec else 'None'}"
	)

	if not addon_spec:
		art_logger.error("No addon spec received, exiting")
		sys.exit(1)

	# Log environment variables that differ between modes
	art_logger.debug("=== ENVIRONMENT VARIABLES ===")
	for key, value in os.environ.items():
		if "NVDA" in key or "ART" in key:
			art_logger.debug(f"  {key} = {value}")

	# Log final addon spec for comparison
	art_logger.debug(f"Final addon_spec: {addon_spec}")

	# Perform startup
	art_logger.debug("About to call performStartup()")
	service_uris = performStartup(addon_spec, is_cli_mode)
	if not service_uris:
		art_logger.error("performStartup() failed, exiting")
		sys.exit(1)

	art_logger.info("=== STARTUP COMPLETED SUCCESSFULLY ===")

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
