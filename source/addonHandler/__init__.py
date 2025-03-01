# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2025 Rui Batista, NV Access Limited, Noelia Ruiz Martínez, Joseph Lee, Babbage B.V.,
# Arnold Loubriat, Łukasz Golonka, Leonard de Ruijter, Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from __future__ import annotations  # Avoids quoting of forward references

import collections
import gettext
import importlib
import inspect
import itertools
import os.path
import shutil
import sys
import zipfile
from types import ModuleType
from typing import (
	TYPE_CHECKING,
	Callable,
	Literal,
	Optional,
)

import addonAPIVersion
import config
import extensionPoints
import languageHandler
import NVDAState
from addonStore.models.status import AddonStateCategory
from logHandler import log
from NVDAState import WritePaths
from utils.caseInsensitiveCollections import CaseInsensitiveSet
from utils.tempFile import _createEmptyTempFileForDeletingFile

from .addonBase import AddonBase, AddonError
from .AddonBundle import AddonBundle
from .AddonManifest import MANIFEST_FILENAME, AddonManifest, _report_manifest_errors, _translatedManifestPaths
from .addonState import AddonsState
from .addonVersionCheck import isAddonCompatible
from .packaging import initializeModulePackagePaths, isModuleName

if TYPE_CHECKING:
	from addonStore.models.addon import AddonHandlerModelGeneratorT  # noqa: F401

stateFilename = "addonsState.pickle"
BUNDLE_EXTENSION = "nvda-addon"
BUNDLE_MIMETYPE = "application/x-nvda-addon"
NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
ADDON_PENDINGINSTALL_SUFFIX = ".pendingInstall"
DELETEDIR_SUFFIX = ".delete"


# Allows add-ons to process additional command line arguments when NVDA starts.
# Each handler is called with one keyword argument `cliArgument`
# and should return `False` if it is not interested in it, `True` otherwise.
# For more details see appropriate section of the developer guide.
isCLIParamKnown = extensionPoints.AccumulatingDecider(defaultDecision=False)

_failedPendingRemovals: CaseInsensitiveSet[str] = CaseInsensitiveSet()
_failedPendingInstalls: CaseInsensitiveSet[str] = CaseInsensitiveSet()


state = AddonsState()


def getRunningAddons() -> "AddonHandlerModelGeneratorT":
	"""Returns currently loaded add-ons."""
	return getAvailableAddons(filterFunc=lambda addon: addon.isRunning)


def getIncompatibleAddons(
	currentAPIVersion=addonAPIVersion.CURRENT,
	backCompatToAPIVersion=addonAPIVersion.BACK_COMPAT_TO,
) -> "AddonHandlerModelGeneratorT":
	"""Returns a generator of the add-ons that are not compatible."""
	return getAvailableAddons(
		filterFunc=lambda addon: (
			not isAddonCompatible(
				addon,
				currentAPIVersion=currentAPIVersion,
				backwardsCompatToVersion=backCompatToAPIVersion,
			)
			and (
				# Add-ons that override incompatibility are not considered incompatible.
				not addon.overrideIncompatibility
				# If we are upgrading NVDA API versions,
				# then the add-on compatibility override will be reset
				or backCompatToAPIVersion > addonAPIVersion.BACK_COMPAT_TO
			)
		),
	)


def removeFailedDeletion(path: os.PathLike):
	shutil.rmtree(path, ignore_errors=True)
	if os.path.exists(path):
		try:
			os.remove(path)
		except Exception:
			pass
	if os.path.exists(path):
		log.error(f"Failed to delete path {path}, try removing manually")


def disableAddonsIfAny():
	"""
	Disables add-ons if told to do so by the user from add-on store.
	This is usually executed before refreshing the list of available add-ons.
	"""
	# Pull in and enable add-ons that should be disabled and enabled, respectively.
	state[AddonStateCategory.DISABLED] |= state[AddonStateCategory.PENDING_DISABLE]
	state[AddonStateCategory.DISABLED] -= state[AddonStateCategory.PENDING_ENABLE]
	# Remove disabled add-ons from having overridden compatibility
	state[AddonStateCategory.OVERRIDE_COMPATIBILITY] -= state[AddonStateCategory.DISABLED]
	# Clear pending disables and enables
	state[AddonStateCategory.PENDING_DISABLE].clear()
	state[AddonStateCategory.PENDING_ENABLE].clear()


def initialize():
	"""Initializes the add-ons subsystem."""
	if config.isAppX:
		log.info("Add-ons not supported when running as a Windows Store application")
		return
	state.load()
	# #3090: Are there add-ons that are supposed to not run for this session?
	disableAddonsIfAny()
	getAvailableAddons(refresh=True, isFirstLoad=True)
	state.cleanupRemovedDisabledAddons()
	state._cleanupCompatibleAddonsFromDowngrade()
	if missingPendingInstalls := state[AddonStateCategory.PENDING_INSTALL] - _failedPendingInstalls:
		log.error(
			"The following add-ons should be installed, "
			f"but are no longer present on disk: {', '.join(missingPendingInstalls)}",
		)
		state[AddonStateCategory.PENDING_INSTALL] -= missingPendingInstalls
	if missingPendingOverrideCompat := (
		state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY] - _failedPendingInstalls
	):
		log.error(
			"The following add-ons which were marked as compatible are no longer installed: "
			f"{', '.join(missingPendingOverrideCompat)}",
		)
		state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY] -= missingPendingOverrideCompat
	if NVDAState.shouldWriteToDisk():
		state.save()
	initializeModulePackagePaths()


def terminate():
	"""Terminates the add-ons subsystem."""
	pass


def _getDefaultAddonPaths() -> list[str]:
	r"""Returns paths where addons can be found.
	For now, only <userConfig>\addons is supported.
	"""
	addon_paths = []
	if os.path.isdir(WritePaths.addonsDir):
		addon_paths.append(WritePaths.addonsDir)
	return addon_paths


def _getAvailableAddonsFromPath(
	path: str,
	isFirstLoad: bool = False,
) -> "AddonHandlerModelGeneratorT":
	"""Gets available add-ons from path.
	An addon is only considered available if the manifest file is loaded with no errors.
	@param path: path from where to find addon directories.
	"""
	log.debug("Listing add-ons from %s", path)
	for p in os.listdir(path):
		if p.endswith(DELETEDIR_SUFFIX):
			if isFirstLoad and NVDAState.shouldWriteToDisk():
				removeFailedDeletion(os.path.join(path, p))
			continue
		addon_path = os.path.join(path, p)
		if os.path.isdir(addon_path) and addon_path not in (".", ".."):
			if not len(os.listdir(addon_path)):
				log.error("Error loading Addon from path: %s", addon_path)
			else:
				log.debug("Loading add-on from %s", addon_path)
				try:
					a = Addon(addon_path)
					name = a.manifest["name"]
					if (
						isFirstLoad
						and NVDAState.shouldWriteToDisk()
						and name in state[AddonStateCategory.PENDING_REMOVE]
						and not a.path.endswith(ADDON_PENDINGINSTALL_SUFFIX)
					):
						try:
							a.completeRemove()
							continue
						except RuntimeError:
							log.exception(f"Failed to remove {name} add-on")
							_failedPendingRemovals.add(name)
					if (
						isFirstLoad
						and NVDAState.shouldWriteToDisk()
						and (
							name in state[AddonStateCategory.PENDING_INSTALL]
							or a.path.endswith(ADDON_PENDINGINSTALL_SUFFIX)
						)
					):
						newPath = a.completeInstall()
						if newPath:
							a = Addon(newPath)
						else:  # installation failed
							_failedPendingInstalls.add(name)
					if (
						isFirstLoad
						and name in state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY]
						and name not in _failedPendingInstalls
					):
						state[AddonStateCategory.OVERRIDE_COMPATIBILITY].add(name)
						state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].remove(name)
					log.debug(
						"Found add-on {name} - {a.version}."
						" Requires API: {a.minimumNVDAVersion}."
						" Last-tested API: {a.lastTestedNVDAVersion}".format(
							name=name,
							a=a,
						),
					)
					if a.isDisabled:
						log.debug("Disabling add-on %s", name)
					if not (isAddonCompatible(a) or a.overrideIncompatibility):
						log.debugWarning("Add-on %s is considered incompatible", name)
						state[AddonStateCategory.BLOCKED].add(a.name)
					yield a
				except:  # noqa: E722
					log.error("Error loading Addon from path: %s", addon_path, exc_info=True)


_availableAddons = collections.OrderedDict()


def getAvailableAddons(
	refresh: bool = False,
	filterFunc: Optional[Callable[["Addon"], bool]] = None,
	isFirstLoad: bool = False,
) -> "AddonHandlerModelGeneratorT":
	"""Gets all available addons on the system.
	@param refresh: Whether or not to query the file system for available add-ons.
	@param filterFunc: A function that allows filtering of add-ons.
	It takes an L{Addon} as its only argument
	and returns a C{bool} indicating whether the add-on matches the provided filter.
	: isFirstLoad: Should add-ons that are pending installations / removal from the file system
	be installed / removed.
	"""
	if filterFunc and not callable(filterFunc):
		raise TypeError("The provided filterFunc is not callable")
	if refresh:
		_availableAddons.clear()
		generators = [_getAvailableAddonsFromPath(path, isFirstLoad) for path in _getDefaultAddonPaths()]
		for addon in itertools.chain(*generators):
			_availableAddons[addon.path] = addon
	return (addon for addon in _availableAddons.values() if not filterFunc or filterFunc(addon))


def installAddonBundle(bundle: AddonBundle) -> Addon | None:
	"""Extracts an Addon bundle in to a unique subdirectory of the user addons directory,
	marking the addon as needing 'install completion' on NVDA restart.

	:param bundle: The add-on bundle to install.
	The bundle._installExceptions property is modified to store any raised exceptions
	during the installation process.

	:return: The extracted add-on object, or None if the add-on bundle fails to be extracted.
	Regardless if the add-on installation failed, the created add-on object from the bundle should be returned
	to give caller a chance to clean-up modules imported as part of install tasks.
	This clean-up cannot be done here, as install tasks are blocking,
	and this function returns as soon as they're started,
	so removing modules before they're done may cause unpredictable effects.
	"""
	try:
		bundle.extract()
		addon = Addon(bundle.pendingInstallPath)
	except Exception as extractException:
		bundle._installExceptions.append(extractException)
		log.error(f"Error extracting add-on bundle {bundle}", exc_info=True)
		return None

	# #2715: The add-on must be added to _availableAddons here so that
	# translations can be used in installTasks module.
	_availableAddons[addon.path] = addon
	try:
		addon.runInstallTask("onInstall")
	except Exception as onInstallException:
		bundle._installExceptions.append(onInstallException)
		# Broad except used, since we can not know what exceptions might be thrown by the install tasks.
		log.error(f"task 'onInstall' on addon '{addon.name}' failed", exc_info=True)
		del _availableAddons[addon.path]
		try:
			addon.completeRemove(runUninstallTask=False)
		except Exception as removeException:
			log.error(f"Failed to remove add-on {addon.name}", exc_info=True)
			bundle._installExceptions.append(removeException)
	else:
		state[AddonStateCategory.PENDING_INSTALL].add(bundle.manifest["name"])
		state.save()
	return addon


class Addon(AddonBase):
	"""Represents an Add-on available on the file system."""

	@property
	def manifest(self) -> "AddonManifest":
		return self._manifest

	def __init__(self, path: str):
		"""Constructs an L{Addon} from.
		@param path: the base directory for the addon data.
		"""
		self.path = path
		self._extendedPackages = set()
		self._importedAddonModules: list[str] = []
		self._modulesBeforeInstall: set[str] = set()
		manifest_path = os.path.join(path, MANIFEST_FILENAME)
		with open(manifest_path, "rb") as f:
			translatedInput = None
			for translatedPath in _translatedManifestPaths():
				p = os.path.join(self.path, translatedPath)
				if os.path.exists(p):
					log.debug("Using manifest translation from %s", p)
					translatedInput = open(p, "rb")
					break
			self._manifest = AddonManifest(f, translatedInput)
			if self.manifest.errors is not None:
				_report_manifest_errors(self.manifest)
				raise AddonError("Manifest file has errors.")

	def completeInstall(self) -> Optional[str]:
		if not os.path.exists(self.pendingInstallPath):
			log.error(f"Pending install path {self.pendingInstallPath} does not exist")
			return None

		try:
			os.replace(self.pendingInstallPath, self.installPath)
			state[AddonStateCategory.PENDING_INSTALL].discard(self.name)
			return self.installPath
		except OSError:
			log.error(f"Failed to complete addon installation for {self.name}", exc_info=True)
			return None

	def requestRemove(self):
		"""Marks this addon for removal on NVDA restart."""
		if self.isPendingInstall and not self.isInstalled:
			# Handle removal of an add-on not yet installed
			self.completeRemove()
			state[AddonStateCategory.PENDING_INSTALL].discard(self.name)
			state[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(self.name)
			state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].discard(self.name)
			# Force availableAddons to be updated
			getAvailableAddons(refresh=True)
		else:
			# Upgrade to existing add-on or installation of new add-on
			state[AddonStateCategory.PENDING_REMOVE].add(self.name)
			# There's no point keeping a record of this add-on pending being disabled now.
			# However, if the addon is disabled, then it needs to remain disabled so that
			# the status in add-on store continues to say "disabled"
			state[AddonStateCategory.PENDING_DISABLE].discard(self.name)
		state.save()

	def completeRemove(self, runUninstallTask: bool = True) -> None:
		if runUninstallTask:
			try:
				# #2715: The add-on must be added to _availableAddons here so that
				# translations can be used in installTasks module.
				_availableAddons[self.path] = self
				self.runInstallTask("onUninstall")
			except:  # noqa: E722
				log.error("task 'onUninstall' on addon '%s' failed" % self.name, exc_info=True)
			finally:
				del _availableAddons[self.path]
				self._cleanupAddonImports()
		tempPath = _createEmptyTempFileForDeletingFile(
			suffix=DELETEDIR_SUFFIX,
			dir=os.path.dirname(self.path),
		)
		try:
			os.replace(self.path, tempPath)
		except (WindowsError, IOError):
			raise RuntimeError("Cannot rename add-on path for deletion")
		shutil.rmtree(tempPath, ignore_errors=True)
		if os.path.exists(tempPath):
			log.error("Error removing addon directory %s, deferring until next NVDA restart" % self.path)
		# clean up the addons state. If an addon with the same name is installed, it should not be automatically
		# disabled / blocked.
		log.debug(f"removing addon {self.name} from the list of disabled / blocked add-ons")
		state[AddonStateCategory.DISABLED].discard(self.name)
		state[AddonStateCategory.PENDING_REMOVE].discard(self.name)
		state[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(self.name)
		state[AddonStateCategory.BLOCKED].discard(self.name)
		state.save()

	def addToPackagePath(self, package):
		"""Adds this L{Addon} extensions to the specific package path if those exist.
		This allows the addon to "run" / be available because the package is able to search its path,
		looking for particular modules. This is used by the following:
		- `globalPlugins`
		- `appModules`
		- `synthDrivers`
		- `brailleDisplayDrivers`
		@param package: the python module representing the package.
		@type package: python module.
		"""
		# #3090: Ensure that we don't add disabled / blocked add-ons to package path.
		# By returning here the addon does not "run"/ become active / registered.
		if self.isDisabled or self.isBlocked or self.isPendingInstall or self.name in _failedPendingRemovals:
			return

		extension_path = os.path.join(self.path, package.__name__)
		if not os.path.isdir(extension_path):
			# This addon does not have extension points for this package
			return
		converted_path = self._getPathForInclusionInPackage(package)
		package.__path__.insert(0, converted_path)
		self._extendedPackages.add(package)
		log.debug("Addon %s added to %s package path", self.manifest["name"], package.__name__)

	@property
	def _canBeEnabled(self) -> bool:
		return (
			self.isCompatible  # Incompatible add-ons cannot be enabled
			or (
				self.canOverrideCompatibility  # Theoretically possible to mark it as compatible
				# Its compatibility has either been overridden, or would be on the next restart
				and self._hasOverriddenCompat
			)
		)

	def enable(self, shouldEnable: bool) -> None:
		"""
		Sets this add-on to be disabled or enabled when NVDA restarts.
		@raises: AddonError on failure.
		"""
		if shouldEnable:
			if not self._canBeEnabled:
				raise AddonError(
					"Add-on is not compatible:"
					" minimum NVDA version {}, last tested version {},"
					" NVDA current {}, NVDA backwards compatible to {}".format(
						self.manifest["minimumNVDAVersion"],
						self.manifest["lastTestedNVDAVersion"],
						addonAPIVersion.CURRENT,
						addonAPIVersion.BACK_COMPAT_TO,
					),
				)
			if self.name in state[AddonStateCategory.PENDING_DISABLE]:
				# Undoing a pending disable.
				state[AddonStateCategory.PENDING_DISABLE].discard(self.name)
			else:
				state[AddonStateCategory.PENDING_ENABLE].add(self.name)
		else:
			if self.name in state[AddonStateCategory.PENDING_ENABLE]:
				# Undoing a pending enable.
				state[AddonStateCategory.PENDING_ENABLE].discard(self.name)
			# No need to disable an addon that is already disabled.
			# This also prevents the status in the add-ons dialog from saying "disabled, pending disable"
			elif self.name not in state[AddonStateCategory.DISABLED]:
				state[AddonStateCategory.PENDING_DISABLE].add(self.name)
			if not self.isCompatible:
				state[AddonStateCategory.BLOCKED].add(self.name)
				state[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(self.name)
		# Record enable/disable flags as a way of preparing for disaster such as sudden NVDA crash.
		state.save()

	def _getPathForInclusionInPackage(self, package):
		extension_path = os.path.join(self.path, package.__name__)
		return extension_path

	def loadModule(self, name: str) -> ModuleType:
		"""loads a python module from the addon directory
		@param name: the module name
		@raises: Any exception that can be raised when importing a module,
			such as NameError, AttributeError, ImportError, etc.
			a ValueError is raised when the module name is invalid.
		"""
		if not isModuleName(name):
			raise ValueError(f"{name} is an invalid python module name")
		log.debug(f"Importing module {name} from plugin {self!r}")
		# Create a qualified full name to avoid modules with the same name on sys.modules.
		# Since the same add-on can be installed and its new version can be pending installation
		# we cannot rely on add-on name being unique.
		# To avoid conflicts, last part of the add-on's path is used
		# i.e. the directory name whose suffix is different between add-ons installed and add-ons pending install.
		# Since dot is used as a separator between add-on name and state suffix,
		# all dots in the name are replaced with underscores.
		addonPkgName = f"addons.{os.path.split(self.path)[-1].replace('.', '_')}"
		fullName = f"{addonPkgName}.{name}"
		# If the given name contains dots (i.e. it is a submodule import),
		# ensure the module at the top of the hierarchy is created correctly.
		# After that, the import mechanism will be able to resolve the submodule automatically.
		splitName = name.split(".")
		fullNameTop = f"{addonPkgName}.{splitName[0]}"
		if fullNameTop in sys.modules:
			# The module can safely be imported, since the top level module is known.
			mod = importlib.import_module(fullName)
			self._importedAddonModules.append(fullName)
			return mod
		# Ensure the new module is resolvable by the import system.
		# For this, all packages in the tree have to be available in sys.modules.
		# We add mock modules for the addons package and the addon itself.
		# If we don't do this, namespace packages can't be imported correctly.
		for parentName in ("addons", addonPkgName):
			if parentName in sys.modules:
				# Parent package already initialized
				continue
			parentSpec = importlib.machinery.ModuleSpec(parentName, None, is_package=True)
			parentModule = importlib.util.module_from_spec(parentSpec)
			sys.modules[parentModule.__name__] = parentModule
			self._importedAddonModules.append(parentModule.__name__)
		spec = importlib.machinery.PathFinder.find_spec(fullNameTop, [self.path])
		if not spec:
			raise ModuleNotFoundError(f"No module named {name!r}", name=name)
		mod = importlib.util.module_from_spec(spec)
		sys.modules[fullNameTop] = mod
		self._importedAddonModules.append(fullNameTop)
		if spec.loader:
			spec.loader.exec_module(mod)
		if fullNameTop == fullName:
			return mod
		importedMod = importlib.import_module(fullName)
		self._importedAddonModules.append(fullName)
		return importedMod

	def getTranslationsInstance(self, domain="nvda"):
		"""Gets the gettext translation instance for this add-on.
		<addon-path>\\locale will be used to find .mo files, if exists.
		If a translation file is not found the default fallback null translation is returned.
		@param domain: the translation domain to retrieve. The 'nvda' default should be used in most cases.
		@returns: the gettext translation class.
		"""
		localedir = os.path.join(self.path, "locale")
		return gettext.translation(
			domain,
			localedir=localedir,
			languages=[languageHandler.getLanguage()],
			fallback=True,
		)

	def runInstallTask(
		self,
		taskName: Literal["onInstall", "onUninstall"],
		*args,
		**kwargs,
	) -> None:
		"""
		Executes the function having the given taskName with the given args and kwargs,
		in the add-on's installTasks module if it exists.
		"""
		self._modulesBeforeInstall = set(sys.modules.keys())
		if not hasattr(self, "_installTasksModule"):
			try:
				installTasksModule = self.loadModule("installTasks")
			except ModuleNotFoundError:
				installTasksModule = None
			self._installTasksModule = installTasksModule
		if self._installTasksModule:
			func = getattr(self._installTasksModule, taskName, None)
			if func:
				func(*args, **kwargs)

	def _cleanupAddonImports(self) -> None:
		for modName in self._importedAddonModules:
			log.debug(f"removing imported add-on module {modName}")
			del sys.modules[modName]
		self._importedAddonModules.clear()
		for modName in set(sys.modules.keys()) - self._modulesBeforeInstall:
			module = sys.modules[modName]
			if module.__file__ and module.__file__.startswith(self.path):
				log.debug(f"Removing module {module} from cache of imported modules")
				del sys.modules[modName]

	def getDocFilePath(self, fileName: Optional[str] = None) -> Optional[str]:
		r"""Get the path to a documentation file for this add-on.
		The file should be located in C{doc\lang\file} inside the add-on,
		where C{lang} is the language code and C{file} is the requested file name.
		Failing that, the language without country is tried.
		English is tried as a last resort.
		An add-on can specify a default documentation file name
		via the docFileName parameter in its manifest.
		@param fileName: The requested file name or C{None} for the add-on's default.
		@return: The path to the requested file or C{None} if it wasn't found.
		"""
		if not fileName:
			fileName = self.manifest["docFileName"]
			if not fileName:
				return None
		docRoot = os.path.join(self.path, "doc")
		lang = languageHandler.getLanguage()
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

	@property
	def isPendingInstall(self) -> bool:
		return super().isPendingInstall and self.pendingInstallPath == self.path

	def __repr__(self) -> str:
		return f"{self.__class__.__name__} ({self.name!r} at path {self.path!r}, running={self.isRunning!r})"


def getCodeAddon(obj=None, frameDist=1):
	"""Returns the L{Addon} where C{obj} is defined. If obj is None the caller code frame is assumed to allow simple retrieval of "current calling addon".
	@param obj: python object or None for default behaviour.
	@param frameDist: how many frames is the caller code. Only change this for functions in this module.
	@return: L{Addon} instance or None if no code does not belong to a add-on package.
	@rtype: C{Addon}
	"""
	if obj is None:
		obj = sys._getframe(frameDist)
	fileName = inspect.getfile(obj)
	assert os.path.isabs(fileName), f"Module file name {fileName} is not absolute"
	dir = os.path.normpath(os.path.dirname(fileName))
	# if fileName is not a subdir of one of the addon paths
	# It does not belong to an addon.
	addonsPath = None
	for addonsPath in _getDefaultAddonPaths():
		addonsPath = os.path.normpath(addonsPath)
		if dir.startswith(addonsPath):
			break
	else:
		raise AddonError("Code does not belong to an addon package.")
	assert addonsPath is not None
	curdir = dir
	while curdir.startswith(addonsPath) and len(curdir) > len(addonsPath):
		if curdir in _availableAddons:
			return _availableAddons[curdir]
		curdir = os.path.normpath(os.path.join(curdir, ".."))
	# Not found!
	raise AddonError("Code does not belong to an addon")


def initTranslation():
	"""Initializes the translation of an add-on so that the Gettext functions (_, ngettext, npgettext and
	pgettext) point to the add-on's translation rather than to NVDA's one.
	This function should be called at the top of any module containing translatable strings and belonging to
	an add-on. It cannot be called in a module that does not belong to an add-on (e.g. in a subdirectory of the
	scratchpad).
	"""

	addon = getCodeAddon(frameDist=2)
	translations = addon.getTranslationsInstance()
	_TRANSLATION_FUNCTIONS = {
		translations.gettext: "_",
		translations.ngettext: "ngettext",
		translations.pgettext: "pgettext",
		translations.npgettext: "npgettext",
	}
	# Point _ to the translation object in the globals namespace of the caller frame
	try:
		callerFrame = inspect.currentframe().f_back
		module = inspect.getmodule(callerFrame)
		for funcName, installAs in _TRANSLATION_FUNCTIONS.items():
			setattr(module, installAs, funcName)
	finally:
		del callerFrame  # Avoid reference problems with frames (per python docs)


def createAddonBundleFromPath(path, destDir=None):
	"""Creates a bundle from a directory that contains a a addon manifest file."""
	basedir = path
	# If  caller did not provide a destination directory name
	# Put the bundle at the same level as the add-on's top-level directory,
	# That is, basedir/..
	if destDir is None:
		destDir = os.path.dirname(basedir)
	manifest_path = os.path.join(basedir, MANIFEST_FILENAME)
	if not os.path.isfile(manifest_path):
		raise AddonError("Can't find %s manifest file." % manifest_path)
	with open(manifest_path, "rb") as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		raise AddonError("Manifest file has errors.")
	bundleFilename = "%s-%s.%s" % (manifest["name"], manifest["version"], BUNDLE_EXTENSION)
	bundleDestination = os.path.join(destDir, bundleFilename)
	with zipfile.ZipFile(bundleDestination, "w") as z:
		# FIXME: the include/exclude feature may or may not be useful. Also python files can be pre-compiled.
		for dir, dirnames, filenames in os.walk(basedir):
			relativePath = os.path.relpath(dir, basedir)
			for filename in filenames:
				pathInBundle = os.path.join(relativePath, filename)
				absPath = os.path.join(dir, filename)
				z.write(absPath, pathInBundle)
	return AddonBundle(bundleDestination)
