# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""AddonHandler module proxy for add-ons running in ART."""

import gettext
import os
from typing import Any, Dict, Optional

from .base import ServiceProxyMixin

# Global addon instance for this ART process
_currentAddon: Optional["AddonProxy"] = None


class AddonProxy:
	"""Simplified addon object for use in ART."""

	def __init__(self, addon_spec: Dict[str, Any]):
		self.name = addon_spec["name"]
		self.path = addon_spec["path"]
		self._manifest = addon_spec.get("manifest", {})
		self._translations = None

	@property
	def manifest(self) -> Dict[str, Any]:
		"""Get the addon manifest."""
		return self._manifest

	@property
	def version(self) -> str:
		"""Get addon version."""
		return self._manifest.get("version", "unknown")

	@property
	def minimumNVDAVersion(self) -> tuple:
		"""Get minimum NVDA version."""
		return self._manifest.get("minimumNVDAVersion", (0, 0, 0))

	@property
	def lastTestedNVDAVersion(self) -> tuple:
		"""Get last tested NVDA version."""
		return self._manifest.get("lastTestedNVDAVersion", (0, 0, 0))

	def getDocFilePath(self, fileName: Optional[str] = None) -> Optional[str]:
		"""Get the path to a documentation file for this add-on."""
		if not fileName:
			fileName = self._manifest.get("docFileName")
			if not fileName:
				return None

		docRoot = os.path.join(self.path, "doc")
		# Try to get language from config service
		lang = _getLanguage()
		langs = [lang]
		if "_" in lang:
			lang = lang.split("_", 1)[0]
			langs.append(lang)
		if lang != "en":
			langs.append("en")

		for lang in langs:
			docFile = os.path.join(docRoot, lang, fileName)
			if os.path.isfile(docFile):
				return docFile
		return None

	def getTranslationsInstance(self, domain: str = "nvda") -> gettext.GNUTranslations:
		"""Gets the gettext translation instance for this add-on."""
		if self._translations is None:
			localedir = os.path.join(self.path, "locale")
			lang = _getLanguage()
			self._translations = gettext.translation(
				domain,
				localedir=localedir,
				languages=[lang],
				fallback=True,
			)
		return self._translations

	def __repr__(self) -> str:
		return f"AddonProxy({self.name!r} at {self.path!r})"


def _getLanguage() -> str:
	"""Get the current language from config."""
	# Try to get from config service
	service = _ConfigProxy._get_service()
	if service:
		try:
			lang = service.getConfigValue("general", "language", "en")
			return lang
		except Exception:
			pass
	return "en"


class _ConfigProxy(ServiceProxyMixin):
	"""Internal proxy for getting config values."""

	_service_env_var = "NVDA_ART_CONFIG_SERVICE_URI"


def initialize(addon_spec: Dict[str, Any]) -> None:
	"""Initialize the addonHandler proxy with addon information.
	This should be called when the ART process starts.
	"""
	global _currentAddon
	_currentAddon = AddonProxy(addon_spec)

	# Also set the addon name in logHandler for context
	try:
		from . import logHandler

		logHandler.setAddonName(addon_spec["name"])
	except ImportError:
		pass

	# Initialize module package paths for this addon
	initializeModulePackagePaths()


def getCodeAddon(obj=None, frameDist: int = 1) -> Optional[AddonProxy]:
	"""Returns the addon where obj is defined.
	In ART, this always returns the single addon running in this process.

	@param obj: Ignored in ART (kept for API compatibility)
	@param frameDist: Ignored in ART (kept for API compatibility)
	@return: The current addon or None
	"""
	return _currentAddon


def initTranslation() -> None:
	"""Initialize translation for the current addon.
	This sets up the gettext functions (_, ngettext, pgettext, npgettext)
	to use the addon's translations.
	"""
	if not _currentAddon:
		raise RuntimeError("No addon loaded in this ART process")

	translations = _currentAddon.getTranslationsInstance()

	# Get the calling module
	import inspect

	try:
		callerFrame = inspect.currentframe().f_back
		module = inspect.getmodule(callerFrame)

		# Set translation functions in the module
		setattr(module, "_", translations.gettext)
		setattr(module, "ngettext", translations.ngettext)
		setattr(module, "pgettext", translations.pgettext)
		setattr(module, "npgettext", translations.npgettext)
	finally:
		del callerFrame
	
	# Also install translation functions globally for compatibility
	# with code that expects them in builtins (like core NVDA modules)
	from . import languageHandler
	languageHandler.setGlobalTranslation(translations)


# Constants from addonHandler
ADDON_PENDINGINSTALL_SUFFIX = ".pendingInstall"
DELETEDIR_SUFFIX = ".delete"
BUNDLE_EXTENSION = "nvda-addon"
BUNDLE_MIMETYPE = "application/x-nvda-addon"
NVDA_ADDON_PROG_ID = "NVDA.Addon.1"


# Stub functions that don't make sense in ART but might be imported
def getAvailableAddons(*args, **kwargs):
	"""Not available in ART - returns empty generator."""
	return iter([])


def getRunningAddons(*args, **kwargs):
	"""Returns just the current addon if it's running."""
	if _currentAddon:
		return iter([_currentAddon])
	return iter([])


def initializeModulePackagePaths() -> None:
	"""Initialize the module package paths for drivers and plugins.
	This ensures that drivers (such as braille display drivers) or plugins (such as app modules)
	can be discovered by NVDA.
	"""
	if not _currentAddon:
		return

	# Import the proxy modules which act as packages
	try:
		from . import (
			appModules,
			brailleDisplayDrivers,
			globalPlugins,
			synthDrivers,
			visionEnhancementProviders,
		)
	except ImportError:
		# If running outside of the proxies directory, import directly
		import appModules
		import brailleDisplayDrivers
		import globalPlugins
		import synthDrivers
		import visionEnhancementProviders

	modules = [
		appModules,
		brailleDisplayDrivers,
		globalPlugins,
		synthDrivers,
		visionEnhancementProviders,
	]

	for module in modules:
		_addAddonPathToPackage(module)


def _addAddonPathToPackage(package) -> None:
	"""Add the current addon's extension path to a package's __path__.

	@param package: The python module representing the package.
	"""
	if not _currentAddon:
		return

	extension_path = os.path.join(_currentAddon.path, package.__name__)
	if not os.path.isdir(extension_path):
		# This addon does not have extension points for this package
		return

	# Ensure __path__ is a list (it might be _NamespacePath or similar)
	if not isinstance(package.__path__, list):
		package.__path__ = list(package.__path__) if package.__path__ else []

	# Add the addon's extension path if not already present
	if extension_path not in package.__path__:
		package.__path__.insert(0, extension_path)
