# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2025 Rui Batista, NV Access Limited, Noelia Ruiz Martínez, Joseph Lee, Babbage B.V.,
# Arnold Loubriat, Łukasz Golonka, Leonard de Ruijter, Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import gettext
import importlib
import os
import os.path
import shutil
import sys
from types import ModuleType
from typing import Literal, Optional

import addonAPIVersion
from .addonState import state
import languageHandler
from addonHandler.addonState import AddonStateCategory
from logHandler import log
from utils.tempFile import _createEmptyTempFileForDeletingFile

from .addonBase import AddonBase, AddonError
from .AddonManifest import MANIFEST_FILENAME, AddonManifest, _report_manifest_errors, _translatedManifestPaths
from .packaging import isModuleName


class Addon(AddonBase):
	"""Represents an Add-on available on the file system."""

	@property
	def manifest(self) -> "AddonManifest":
		return self._manifest

	def __init__(self, path: str):
		"""Constructs an Addon from a directory.

		:param path: The base directory for the addon data.
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
		"""Complete installation of a pending addon.

		:return: The installation path if successful, None otherwise.
		"""
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
		from . import getAvailableAddons

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
		"""Complete removal of an addon.

		:param runUninstallTask: Whether to run the addon's uninstall task.
		"""
		from . import _availableAddons, DELETEDIR_SUFFIX

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
		"""Adds this Addon extensions to the specific package path if those exist.

		This allows the addon to "run" / be available because the package is able to search its path,
		looking for particular modules. This is used by the following:

		- ``globalPlugins``
		- ``appModules``
		- ``synthDrivers``
		- ``brailleDisplayDrivers``

		:param package: The python module representing the package.
		"""
		from . import _failedPendingRemovals

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
		"""Sets this add-on to be disabled or enabled when NVDA restarts.

		:param shouldEnable: True to enable, False to disable.
		:raises AddonError: If the addon cannot be enabled.
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
		"""Get the path to be included in the package's search path.

		:param package: The package to get the path for.
		:return: The path to be included.
		"""
		extension_path = os.path.join(self.path, package.__name__)
		return extension_path

	def loadModule(self, name: str) -> ModuleType:
		"""Loads a python module from the addon directory.

		:param name: The module name.
		:return: The loaded module.
		:raises ValueError: When the module name is invalid.
		:raises ModuleNotFoundError: When the module cannot be found.
		:raises Exception: Any exception that can be raised when importing a module,
		    such as NameError, AttributeError, ImportError, etc.
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

		:param domain: The translation domain to retrieve. The 'nvda' default should be used in most cases.
		:return: The gettext translation class.
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
		"""Executes the function having the given taskName with the given args and kwargs.

		The function is executed in the add-on's installTasks module if it exists.

		:param taskName: The name of the task to run, either "onInstall" or "onUninstall".
		:param args: Positional arguments to pass to the task function.
		:param kwargs: Keyword arguments to pass to the task function.
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
		"""Remove imported addon modules from sys.modules."""
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

		The file should be located in ``doc\lang\file`` inside the add-on,
		where ``lang`` is the language code and ``file`` is the requested file name.
		Failing that, the language without country is tried.
		English is tried as a last resort.

		An add-on can specify a default documentation file name
		via the docFileName parameter in its manifest.

		:param fileName: The requested file name or None for the add-on's default.
		:return: The path to the requested file or None if it wasn't found.
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
