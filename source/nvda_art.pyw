import concurrent.futures
import importlib.util
import sys
import threading
from enum import Enum
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import Pyro5.api
import wx

# NVDA ART (Add-On Runtime) main module
__version__ = "0.1.0"
logger = getLogger(__name__)
basicConfig(level=INFO)

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
class AddOnLifecycleService:
	"""Service for managing add-on lifecycle in the ART process."""

	def __init__(self):
		self.loadedAddons: Dict[str, object] = {}
		logger.info("AddOnLifecycleService initialized")

	def loadAddon(self, addonPath: str) -> bool:
		"""Load an add-on from the given path.
		@param addonPath: Path to the add-on directory
		@return: True if successful, False otherwise
		"""
		addonPathObj = Path(addonPath)
		if not addonPathObj.exists():
			logger.error(f"Add-on path does not exist: {addonPathObj}")
			return False

		# Look for __init__.py in the add-on directory
		initFile = addonPathObj / "__init__.py"
		if not initFile.exists():
			logger.error(f"Add-on __init__.py not found: {initFile}")
			return False

		# Generate a module name based on the add-on directory name
		addonId = addonPathObj.name
		moduleName = f"addon_{addonId}"

		# Load the module
		spec = importlib.util.spec_from_file_location(moduleName, initFile)
		if spec is None or spec.loader is None:
			logger.error(f"Could not create module spec for {initFile}")
			return False

		module = importlib.util.module_from_spec(spec)

		# Add the add-on directory to sys.path temporarily
		addonDirStr = str(addonPathObj)
		if addonDirStr not in sys.path:
			sys.path.insert(0, addonDirStr)

		try:
			spec.loader.exec_module(module)
			logger.info(f"Successfully loaded add-on module: {addonId}")

			# Store the loaded module
			self.loadedAddons[addonId] = module

			logger.info(f"Add-on {addonId} loaded successfully")
			return True

		except Exception:
			logger.exception(f"Error executing add-on module {addonId}")
			return False
		finally:
			# Remove from sys.path
			if addonDirStr in sys.path:
				sys.path.remove(addonDirStr)

	def getLoadedAddons(self) -> List[str]:
		"""Get a list of currently loaded add-on IDs.
		@return: List of add-on IDs that are currently loaded
		"""
		return list(self.loadedAddons.keys())


@Pyro5.api.expose
class ExtensionPointHandlerService:
	"""Service for executing extension point handlers in ART."""

	def __init__(self):
		self._handlers: Dict[str, List[Tuple[str, Callable]]] = {}
		self._currentAddon: Optional[str] = None

	def registerHandler(self, extPointName: str, handlerFunc: Callable, epType: str) -> str:
		"""Register a handler function for an extension point."""
		addonId = self._currentAddon or "unknown"
		handlerID = f"{addonId}_{id(handlerFunc)}"

		if extPointName not in self._handlers:
			self._handlers[extPointName] = []

		self._handlers[extPointName].append((handlerID, handlerFunc))

		# Also register with tracking service
		extService = artRuntime.extensionPointService
		if extService:
			extService.registerHandler(addonId, extPointName, handlerID, epType)

		logger.info(f"Registered handler {handlerID} for {extPointName}")
		return handlerID

	def executeHandlers(self, extPointName: str, epType: str, *args, **kwargs) -> Any:
		"""Execute all handlers for an extension point."""
		if extPointName not in self._handlers:
			return self._getDefaultResult(epType, **args)

		results = []
		for handlerId, handlerFunc in self._handlers[extPointName]:
			try:
				# TODO: Use callWithSupportedKwargs when available
				result = handlerFunc(*args, **kwargs)
				results.append(result)
			except Exception:
				logger.exception(f"Error in handler {handlerId}")

		return self._combineResults(epType, results)

	def _getDefaultResult(self, epType: str, *args) -> Any:
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
			# Return True if any handler returned False
			return not any(not r for r in results)
		elif epType == "filter":
			# Chain filters together
			if not results:
				return None
			value = results[0]
			for result in results[1:]:
				if result is not None:
					value = result
			return value
		elif epType == "chain":
			# Flatten all results
			flattened = []
			for result in results:
				if isinstance(result, list):
					flattened.extend(result)
				else:
					flattened.append(result)
			return flattened
		# Default case for unknown types
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

	def __init__(self):
		self.daemon: Optional[Pyro5.api.Daemon] = None
		self.addonService: Optional[AddOnLifecycleService] = None
		self.extensionPointService: Optional[ExtensionPointService] = None
		self.handlerService: Optional[ExtensionPointHandlerService] = None
		self.executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
		self.daemonFuture: Optional[concurrent.futures.Future] = None
		self._shutdownEvent = threading.Event()

	def start(self):
		"""Start the ART runtime services."""
		# Configure Pyro5 settings based on design document
		Pyro5.config.SERIALIZER = "json"
		Pyro5.config.COMMTIMEOUT = 2.0  # 2 seconds timeout
		Pyro5.config.HOST = "127.0.0.1"  # Default host for daemons
		Pyro5.config.MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit

		# Create Pyro5 daemon bound to localhost only
		self.daemon = Pyro5.api.Daemon(host="127.0.0.1", port=0)
		logger.info(f"Pyro5 daemon created at: {self.daemon.locationStr}")

		# Create and register the add-on lifecycle service
		self.addonService = AddOnLifecycleService()
		uri = self.daemon.register(self.addonService, "nvda.art.addon_lifecycle")
		logger.info(f"AddOnLifecycleService registered at: {uri}")

		# Create and register the extension point service
		self.extensionPointService = ExtensionPointService()
		extUri = self.daemon.register(self.extensionPointService, "nvda.art.extension_points")
		logger.info(f"ExtensionPointService registered at: {extUri}")

		# Create and register the handler service
		self.handlerService = ExtensionPointHandlerService()
		handlerUri = self.daemon.register(self.handlerService, "nvda.art.handlers")
		logger.info(f"ExtensionPointHandlerService registered at: {handlerUri}")

		# Print the URIs so NVDA Core can discover them
		print(f"ART_SERVICE_URI:{uri}", flush=True)
		print(f"ART_EXT_SERVICE_URI:{extUri}", flush=True)
		print(f"ART_HANDLER_SERVICE_URI:{handlerUri}", flush=True)

		# Start the daemon using ThreadPoolExecutor
		self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="ARTDaemon")
		self.daemonFuture = self.executor.submit(self._daemonLoop)
		logger.info("ART runtime started successfully")

	def _daemonLoop(self):
		"""Run the Pyro5 daemon request loop."""
		logger.info("Starting Pyro5 daemon request loop")
		self.daemon.requestLoop(lambda: not self._shutdownEvent.is_set())
		logger.info("Pyro5 daemon request loop finished")

	def shutdown(self):
		"""Shutdown the ART runtime."""
		logger.info("Shutting down ART runtime")
		self._shutdownEvent.set()

		if self.daemon:
			self.daemon.shutdown()

		if self.daemonFuture:
			try:
				# Wait for daemon to shutdown gracefully
				self.daemonFuture.result(timeout=5.0)
			except concurrent.futures.TimeoutError:
				logger.warning("Daemon did not shutdown within timeout")
			except Exception as e:
				logger.warning(f"Exception during daemon shutdown: {e}")

		if self.executor:
			self.executor.shutdown(wait=True, timeout=5.0)


class MainWindow(wx.Frame):
	"""Main window for the NVDA ART application. Only for receiving events, no UI."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.SetTitle("NVDA ART")
		self.Bind(wx.EVT_CLOSE, self.onClose)

	def onClose(self, event):
		logger.info("Closing NVDA ART main window.")
		if artRuntime:
			artRuntime.shutdown()
		self.Destroy()
		wxApp.ExitMainLoop()


mainWindow: MainWindow
artRuntime: ARTRuntime


def main():
	"""Initialize the NVDA ART Runtime."""
	global wxApp, mainWindow, artRuntime

	wxApp = wx.App(False, useBestVisual=False)
	wxApp.SetAppName("NVDA ART")
	wxApp.SetVendorName("NV Access")

	mainWindow = MainWindow(None, title="NVDA ART")
	mainWindow.Hide()

	# Initialize and start the ART runtime
	artRuntime = ARTRuntime()
	artRuntime.start()
	logger.info(f"Starting NVDA ART version {__version__}")
	# Start the wxPython event loop
	try:
		wxApp.MainLoop()
	finally:
		if artRuntime:
			artRuntime.shutdown()


if __name__ == "__main__":
	main()
