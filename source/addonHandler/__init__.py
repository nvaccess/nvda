# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2023 Rui Batista, NV Access Limited, Noelia Ruiz Martínez,
# Joseph Lee, Babbage B.V., Arnold Loubriat, Łukasz Golonka, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from abc import abstractmethod, ABC
import glob
import sys
import os.path
import gettext
import tempfile
import inspect
import itertools
import collections
import shutil
from io import StringIO
import pickle
from six import string_types
from typing import (
	Callable,
	Dict,
	Optional,
	Set,
	TYPE_CHECKING,
	Tuple,
	Union,
)
import zipfile
from configobj import ConfigObj
from configobj.validate import Validator
import config
import languageHandler
from logHandler import log
import winKernel
import addonAPIVersion
import importlib
import NVDAState
from NVDAState import WritePaths
from types import ModuleType

from addonStore.models.status import AddonStateCategory, SupportsAddonState
from addonStore.models.version import MajorMinorPatch, SupportsVersionCheck
import extensionPoints
from utils.caseInsensitiveCollections import CaseInsensitiveSet

from .addonVersionCheck import (
	isAddonCompatible,
)
from .packaging import (
	initializeModulePackagePaths,
	isModuleName,
)

if TYPE_CHECKING:
	from addonStore.models.addon import (  # noqa: F401
		AddonManifestModel,
		AddonHandlerModelGeneratorT,
		InstalledAddonStoreModel,
	)

MANIFEST_FILENAME = "manifest.ini"
stateFilename="addonsState.pickle"
BUNDLE_EXTENSION = "nvda-addon"
BUNDLE_MIMETYPE = "application/x-nvda-addon"
NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
ADDON_PENDINGINSTALL_SUFFIX=".pendingInstall"
DELETEDIR_SUFFIX=".delete"


# Allows add-ons to process additional command line arguments when NVDA starts.
# Each handler is called with one keyword argument `cliArgument`
# and should return `False` if it is not interested in it, `True` otherwise.
# For more details see appropriate section of the developer guide.
isCLIParamKnown = extensionPoints.AccumulatingDecider(defaultDecision=False)


AddonStateDictT = Dict[AddonStateCategory, CaseInsensitiveSet[str]]


class AddonsState(collections.UserDict[AddonStateCategory, CaseInsensitiveSet[str]]):
	"""
	Subclasses `collections.UserDict` to preserve backwards compatibility.
	AddonStateCategory string enums mapped to a set of the add-on "name/id" currently in that state.
	Add-ons that have the same ID except differ in casing cause a path collision,
	as add-on IDs are installed to a case insensitive path.
	Therefore add-on IDs should be treated as case insensitive.
	"""

	@staticmethod
	def _generateDefaultStateContent() -> AddonStateDictT:
		return {
			category: CaseInsensitiveSet() for category in AddonStateCategory
		}

	data: AddonStateDictT
	manualOverridesAPIVersion: MajorMinorPatch

	@property
	def statePath(self) -> os.PathLike:
		"""Returns path to the state file. """
		return WritePaths.addonStateFile

	def setDefaultStateValues(self) -> None:
		self.update(self._generateDefaultStateContent())

		# Set default value for manualOverridesAPIVersion.
		# The ability to override add-ons only appeared in 2023.2,
		# where the BACK_COMPAT_TO API version was 2023.1.0.
		self.manualOverridesAPIVersion = MajorMinorPatch(2023, 1, 0)

	def fromPickledDict(
			self,
			pickledState: Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT, MajorMinorPatch]]
	) -> None:
		# Load from pickledState
		if "backCompatToAPIVersion" in pickledState:
			self.manualOverridesAPIVersion = MajorMinorPatch(*pickledState["backCompatToAPIVersion"])
		for category in AddonStateCategory:
			# Make pickles case insensitive
			self[AddonStateCategory(category)] = CaseInsensitiveSet(pickledState.get(category, set()))

	def toDict(self) -> Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT]]:
		# We cannot pickle instance of `AddonsState` directly
		# since older versions of NVDA aren't aware about this class and they're expecting
		# the state to be using inbuilt data types only.
		picklableState: Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT]] = dict()
		for category in self.data:
			picklableState[category.value] = set(self.data[category])
		picklableState["backCompatToAPIVersion"] = tuple(self.manualOverridesAPIVersion)
		return picklableState

	def load(self) -> None:
		"""Populates state with the default content and then loads values from the config."""
		self.setDefaultStateValues()
		try:
			# #9038: Python 3 requires binary format when working with pickles.
			with open(self.statePath, "rb") as f:
				pickledState: Dict[str, Union[Set[str], addonAPIVersion.AddonApiVersionT]] = pickle.load(f)
		except FileNotFoundError:
			pass  # Clean config - no point logging in this case
		except IOError:
			log.debug("Error when reading state file", exc_info=True)
		except pickle.UnpicklingError:
			log.debugWarning("Failed to unpickle state", exc_info=True)
		except Exception:
			log.exception()
		else:
			self.fromPickledDict(pickledState)
		if self.manualOverridesAPIVersion != addonAPIVersion.BACK_COMPAT_TO:
			log.debug(
				"BACK_COMPAT_TO API version for manual compatibility overrides has changed. "
				f"NVDA API has been upgraded: from {self.manualOverridesAPIVersion} to {addonAPIVersion.BACK_COMPAT_TO}"
			)
		if self.manualOverridesAPIVersion < addonAPIVersion.BACK_COMPAT_TO:
			# Reset compatibility overrides as the API version has upgraded.
			# For the installer, this is not written to disk.
			# Portable/temporary copies will write this on the first run.
			# Mark overridden compatible add-ons as blocked.
			self[AddonStateCategory.BLOCKED].update(self[AddonStateCategory.OVERRIDE_COMPATIBILITY])
			# Reset overridden compatibility for add-ons that were overridden by older versions of NVDA.
			self[AddonStateCategory.OVERRIDE_COMPATIBILITY].clear()
			self[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].clear()
		self.manualOverridesAPIVersion = MajorMinorPatch(*addonAPIVersion.BACK_COMPAT_TO)

	def removeStateFile(self) -> None:
		if not NVDAState.shouldWriteToDisk():
			log.debugWarning("NVDA should not write to disk from secure mode or launcher", stack_info=True)
			return
		try:
			os.remove(self.statePath)
		except FileNotFoundError:
			pass  # Probably clean config - no point in logging in this case.
		except OSError:
			log.error(f"Failed to remove state file {self.statePath}", exc_info=True)

	def save(self) -> None:
		"""Saves content of the state to a file unless state is empty in which case this would be pointless."""
		if not NVDAState.shouldWriteToDisk():
			log.error("NVDA should not write to disk from secure mode or launcher", stack_info=True)
			return

		if any(self.values()):
			try:
				# #9038: Python 3 requires binary format when working with pickles.
				with open(self.statePath, "wb") as f:
					pickle.dump(self.toDict(), f, protocol=0)
			except (IOError, pickle.PicklingError):
				log.debugWarning("Error saving state", exc_info=True)
		else:
			# Empty state - just delete state file and don't save anything.
			self.removeStateFile()

	def cleanupRemovedDisabledAddons(self) -> None:
		"""Versions of NVDA before #12792 failed to remove add-on from list of disabled add-ons
		during uninstallation. As a result after reinstalling add-on with the same name it was disabled
		by default confusing users. Fix this by removing all add-ons no longer present in the config
		from the list of disabled add-ons in the state."""
		installedAddonNames = CaseInsensitiveSet(a.name for a in getAvailableAddons())
		for disabledAddonName in CaseInsensitiveSet(self[AddonStateCategory.DISABLED]):
			# Iterate over copy of set to prevent updating the set while iterating over it.
			if disabledAddonName not in installedAddonNames:
				log.debug(f"Discarding {disabledAddonName} from disabled add-ons as it has been uninstalled.")
				self[AddonStateCategory.DISABLED].discard(disabledAddonName)

	def _cleanupInstalledAddons(self) -> None:
		# There should be no pending installs after add-ons have been loaded during initialization.
		for path in _getDefaultAddonPaths():
			pendingInstallPaths = glob.glob(f"{path}/*.{ADDON_PENDINGINSTALL_SUFFIX}")
			for pendingInstallPath in pendingInstallPaths:
				if os.path.exists(pendingInstallPath):
					try:
						log.error(f"Removing failed install of {pendingInstallPath}")
						shutil.rmtree(pendingInstallPath, ignore_errors=True)
					except OSError:
						log.error(f"Failed to remove {pendingInstallPath}", exc_info=True)

		if self[AddonStateCategory.PENDING_INSTALL]:
			log.error(
				f"Discarding {self[AddonStateCategory.PENDING_INSTALL]} from pending install add-ons "
				"as their install failed."
			)
			self[AddonStateCategory.PENDING_INSTALL].clear()

	def _cleanupCompatibleAddonsFromDowngrade(self) -> None:
		from addonStore.dataManager import addonDataManager
		installedAddons = addonDataManager._installedAddonsCache.installedAddons
		for blockedAddon in CaseInsensitiveSet(
			self[AddonStateCategory.BLOCKED].union(
				self[AddonStateCategory.OVERRIDE_COMPATIBILITY]
			)
		):
			# Iterate over copy of set to prevent updating the set while iterating over it.
			if blockedAddon not in installedAddons and blockedAddon not in self[AddonStateCategory.PENDING_INSTALL]:
				log.debug(f"Discarding {blockedAddon} from blocked add-ons as it has been uninstalled.")
				self[AddonStateCategory.BLOCKED].discard(blockedAddon)
				self[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(blockedAddon)
			elif installedAddons[blockedAddon].isCompatible:
				log.debug(f"Discarding {blockedAddon} from blocked add-ons as it has become compatible.")
				self[AddonStateCategory.BLOCKED].discard(blockedAddon)
				self[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(blockedAddon)


state = AddonsState()


def getRunningAddons() -> "AddonHandlerModelGeneratorT":
	""" Returns currently loaded add-ons.
	"""
	return getAvailableAddons(filterFunc=lambda addon: addon.isRunning)


def getIncompatibleAddons(
		currentAPIVersion=addonAPIVersion.CURRENT,
		backCompatToAPIVersion=addonAPIVersion.BACK_COMPAT_TO
) -> "AddonHandlerModelGeneratorT":
	""" Returns a generator of the add-ons that are not compatible.
	"""
	return getAvailableAddons(
		filterFunc=lambda addon: (
			not isAddonCompatible(
				addon,
				currentAPIVersion=currentAPIVersion,
				backwardsCompatToVersion=backCompatToAPIVersion
			)
			and (
				# Add-ons that override incompatibility are not considered incompatible.
				not addon.overrideIncompatibility
				# If we are upgrading NVDA API versions,
				# then the add-on compatibility override will be reset
				or backCompatToAPIVersion > addonAPIVersion.BACK_COMPAT_TO
			)
		)
	)


def removeFailedDeletion(path: os.PathLike):
	shutil.rmtree(path, ignore_errors=True)
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
	""" Initializes the add-ons subsystem. """
	if config.isAppX:
		log.info("Add-ons not supported when running as a Windows Store application")
		return
	state.load()
	# #3090: Are there add-ons that are supposed to not run for this session?
	disableAddonsIfAny()
	getAvailableAddons(refresh=True, isFirstLoad=True)
	state.cleanupRemovedDisabledAddons()
	state._cleanupCompatibleAddonsFromDowngrade()
	state._cleanupInstalledAddons()
	if NVDAState.shouldWriteToDisk():
		state.save()
	initializeModulePackagePaths()
	if state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY]:
		log.error(
			"The following add-ons which were marked as compatible are no longer installed: "
			f"{', '.join(state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY])}"
		)
		state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].clear()


def terminate():
	""" Terminates the add-ons subsystem. """
	pass


def _getDefaultAddonPaths() -> list[str]:
	r""" Returns paths where addons can be found.
	For now, only <userConfig>\addons is supported.
	"""
	addon_paths = []
	if os.path.isdir(WritePaths.addonsDir):
		addon_paths.append(WritePaths.addonsDir)
	return addon_paths


def _getAvailableAddonsFromPath(
		path: str,
		isFirstLoad: bool = False
) -> "AddonHandlerModelGeneratorT":
	""" Gets available add-ons from path.
	An addon is only considered available if the manifest file is loaded with no errors.
	@param path: path from where to find addon directories.
	"""
	log.debug("Listing add-ons from %s", path)
	for p in os.listdir(path):
		if p.endswith(DELETEDIR_SUFFIX):
			if isFirstLoad:
				removeFailedDeletion(os.path.join(path, p))
			continue
		addon_path = os.path.join(path, p)
		if os.path.isdir(addon_path) and addon_path not in ('.', '..'):
			if not len(os.listdir(addon_path)):
				log.error("Error loading Addon from path: %s", addon_path)
			else:
				log.debug("Loading add-on from %s", addon_path)
				try:
					a = Addon(addon_path)
					name = a.manifest['name']
					if (
						isFirstLoad
						and name in state[AddonStateCategory.PENDING_REMOVE]
						and not a.path.endswith(ADDON_PENDINGINSTALL_SUFFIX)
					):
						try:
							a.completeRemove()
						except RuntimeError:
							log.exception(f"Failed to remove {name} add-on")
						continue
					if(
						isFirstLoad
						and (
							name in state[AddonStateCategory.PENDING_INSTALL]
							or a.path.endswith(ADDON_PENDINGINSTALL_SUFFIX)
						)
					):
						newPath = a.completeInstall()
						if newPath:
							a = Addon(newPath)
					if isFirstLoad and name in state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY]:
						state[AddonStateCategory.OVERRIDE_COMPATIBILITY].add(name)
						state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].remove(name)
					log.debug(
						"Found add-on {name} - {a.version}."
						" Requires API: {a.minimumNVDAVersion}."
						" Last-tested API: {a.lastTestedNVDAVersion}".format(
							name=name,
							a=a
						))
					if a.isDisabled:
						log.debug("Disabling add-on %s", name)
					if not (
						isAddonCompatible(a)
						or a.overrideIncompatibility
					):
						log.debugWarning("Add-on %s is considered incompatible", name)
						state[AddonStateCategory.BLOCKED].add(a.name)
					yield a
				except:
					log.error("Error loading Addon from path: %s", addon_path, exc_info=True)

_availableAddons = collections.OrderedDict()


def getAvailableAddons(
		refresh: bool = False,
		filterFunc: Optional[Callable[["Addon"], bool]] = None,
		isFirstLoad: bool = False
) -> "AddonHandlerModelGeneratorT":
	""" Gets all available addons on the system.
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


def installAddonBundle(bundle: "AddonBundle") -> "Addon":
	""" Extracts an Addon bundle in to a unique subdirectory of the user addons directory,
	marking the addon as needing 'install completion' on NVDA restart.
	"""
	bundle.extract()
	addon = Addon(bundle.pendingInstallPath)
	# #2715: The add-on must be added to _availableAddons here so that
	# translations can be used in installTasks module.
	_availableAddons[addon.path]=addon
	try:
		addon.runInstallTask("onInstall")
	except:
		log.error("task 'onInstall' on addon '%s' failed"%addon.name,exc_info=True)
		del _availableAddons[addon.path]
		addon.completeRemove(runUninstallTask=False)
		raise AddonError("Installation failed")
	state[AddonStateCategory.PENDING_INSTALL].add(bundle.manifest['name'])
	state.save()
	return addon

class AddonError(Exception):
	""" Represents an exception coming from the addon subsystem. """


class AddonBase(SupportsAddonState, SupportsVersionCheck, ABC):
	"""The base class for functionality that is available both for add-on bundles and add-ons on the file system.
	Subclasses should at least implement L{manifest}.
	"""

	@property
	def name(self) -> str:
		"""A unique name, the id of the add-on.
		"""
		return self.manifest['name']

	@property
	def version(self) -> str:
		"""A display version. Not necessarily semantic
		"""
		return self.manifest['version']

	@property
	def minimumNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		return self.manifest.get('minimumNVDAVersion')

	@property
	def lastTestedNVDAVersion(self) -> addonAPIVersion.AddonApiVersionT:
		return self.manifest.get('lastTestedNVDAVersion')

	@property
	@abstractmethod
	def manifest(self) -> "AddonManifest":
		...

	@property
	def _addonStoreData(self) -> Optional["InstalledAddonStoreModel"]:
		from addonStore.dataManager import addonDataManager
		assert addonDataManager
		return addonDataManager._getCachedInstalledAddonData(self.name)

	@property
	def _addonGuiModel(self) -> "AddonManifestModel":
		from addonStore.models.addon import _createGUIModelFromManifest
		return _createGUIModelFromManifest(self)


class Addon(AddonBase):
	""" Represents an Add-on available on the file system."""

	@property
	def manifest(self) -> "AddonManifest":
		return self._manifest

	def __init__(self, path: str):
		""" Constructs an L{Addon} from.
		@param path: the base directory for the addon data.
		"""
		self.path = path
		self._extendedPackages = set()
		manifest_path = os.path.join(path, MANIFEST_FILENAME)
		with open(manifest_path, 'rb') as f:
			translatedInput = None
			for translatedPath in _translatedManifestPaths():
				p = os.path.join(self.path, translatedPath)
				if os.path.exists(p):
					log.debug("Using manifest translation from %s", p)
					translatedInput = open(p, 'rb')
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
			os.rename(self.pendingInstallPath, self.installPath)
			state[AddonStateCategory.PENDING_INSTALL].discard(self.name)
			return self.installPath
		except OSError:
			log.error(f"Failed to complete addon installation for {self.name}", exc_info=True)

		# Remove pending install folder
		try:
			log.error(f"Removing failed install of {self.pendingInstallPath}")
			shutil.rmtree(self.pendingInstallPath, ignore_errors=True)
			state[AddonStateCategory.PENDING_INSTALL].discard(self.name)
		except OSError:
			log.error(f"Failed to remove {self.pendingInstallPath}", exc_info=True)

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
			except:
				log.error("task 'onUninstall' on addon '%s' failed"%self.name,exc_info=True)
			finally:
				del _availableAddons[self.path]
		tempPath=tempfile.mktemp(suffix=DELETEDIR_SUFFIX,dir=os.path.dirname(self.path))
		try:
			os.rename(self.path,tempPath)
		except (WindowsError,IOError):
			raise RuntimeError("Cannot rename add-on path for deletion")
		shutil.rmtree(tempPath,ignore_errors=True)
		if os.path.exists(tempPath):
			log.error("Error removing addon directory %s, deferring until next NVDA restart"%self.path)
		# clean up the addons state. If an addon with the same name is installed, it should not be automatically
		# disabled / blocked.
		log.debug(f"removing addon {self.name} from the list of disabled / blocked add-ons")
		state[AddonStateCategory.DISABLED].discard(self.name)
		state[AddonStateCategory.PENDING_REMOVE].discard(self.name)
		state[AddonStateCategory.OVERRIDE_COMPATIBILITY].discard(self.name)
		state[AddonStateCategory.BLOCKED].discard(self.name)
		state.save()

	def addToPackagePath(self, package):
		""" Adds this L{Addon} extensions to the specific package path if those exist.
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
		if self.isDisabled or self.isBlocked or self.isPendingInstall:
			return

		extension_path = os.path.join(self.path, package.__name__)
		if not os.path.isdir(extension_path):
			# This addon does not have extension points for this package
			return
		converted_path = self._getPathForInclusionInPackage(package)
		package.__path__.insert(0, converted_path)
		self._extendedPackages.add(package)
		log.debug("Addon %s added to %s package path", self.manifest['name'], package.__name__)

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
						self.manifest['minimumNVDAVersion'],
						self.manifest['lastTestedNVDAVersion'],
						addonAPIVersion.CURRENT,
						addonAPIVersion.BACK_COMPAT_TO
					)
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
		""" loads a python module from the addon directory
		@param name: the module name
		@raises: Any exception that can be raised when importing a module,
			such as NameError, AttributeError, ImportError, etc.
			a ValueError is raised when the module name is invalid.
		"""
		if not isModuleName(name):
			raise ValueError(f"{name} is an invalid python module name")
		log.debug(f"Importing module {name} from plugin {self!r}")
		# Create a qualified full name to avoid modules with the same name on sys.modules.
		fullName = f"addons.{self.name}.{name}"
		# If the given name contains dots (i.e. it is a submodule import),
		# ensure the module at the top of the hierarchy is created correctly.
		# After that, the import mechanism will be able to resolve the submodule automatically.
		splitName = name.split('.')
		fullNameTop = f"addons.{self.name}.{splitName[0]}"
		if fullNameTop in sys.modules:
			# The module can safely be imported, since the top level module is known.
			return importlib.import_module(fullName)
		# Ensure the new module is resolvable by the import system.
		# For this, all packages in the tree have to be available in sys.modules.
		# We add mock modules for the addons package and the addon itself.
		# If we don't do this, namespace packages can't be imported correctly.
		for parentName in ("addons", f"addons.{self.name}"):
			if parentName in sys.modules:
				# Parent package already initialized
				continue
			parentSpec = importlib._bootstrap.ModuleSpec(parentName, None, is_package=True)
			parentModule = importlib.util.module_from_spec(parentSpec)
			sys.modules[parentModule.__name__] = parentModule
		spec = importlib.machinery.PathFinder.find_spec(fullNameTop, [self.path])
		if not spec:
			raise ModuleNotFoundError(f"No module named {name!r}", name=name)
		mod = importlib.util.module_from_spec(spec)
		sys.modules[fullNameTop] = mod
		if spec.loader:
			spec.loader.exec_module(mod)
		return mod if fullNameTop == fullName else importlib.import_module(fullName)

	def getTranslationsInstance(self, domain='nvda'):
		""" Gets the gettext translation instance for this add-on.
		<addon-path>\\locale will be used to find .mo files, if exists.
		If a translation file is not found the default fallback null translation is returned.
		@param domain: the translation domain to retrieve. The 'nvda' default should be used in most cases.
		@returns: the gettext translation class.
		"""
		localedir = os.path.join(self.path, "locale")
		return gettext.translation(domain, localedir=localedir, languages=[languageHandler.getLanguage()], fallback=True)

	def runInstallTask(self,taskName,*args,**kwargs):
		"""
		Executes the function having the given taskName with the given args and kwargs,
		in the add-on's installTasks module if it exists.
		"""
		if not hasattr(self,'_installTasksModule'):
			try:
				installTasksModule = self.loadModule('installTasks')
			except ModuleNotFoundError:
				installTasksModule = None
			self._installTasksModule = installTasksModule
		if self._installTasksModule:
			func=getattr(self._installTasksModule,taskName,None)
			if func:
				func(*args,**kwargs)

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

	def __repr__(self):
		return f"{self.__class__.__name__} ({self.name!r}, running={self.isRunning!r})"


def getCodeAddon(obj=None, frameDist=1):
	""" Returns the L{Addon} where C{obj} is defined. If obj is None the caller code frame is assumed to allow simple retrieval of "current calling addon".
	@param obj: python object or None for default behaviour.
	@param frameDist: how many frames is the caller code. Only change this for functions in this module.
	@return: L{Addon} instance or None if no code does not belong to a add-on package.
	@rtype: C{Addon}
	"""
	if obj is None:
		obj = sys._getframe(frameDist)
	fileName  = inspect.getfile(obj)
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
	addon = getCodeAddon(frameDist=2)
	translations = addon.getTranslationsInstance()
	_TRANSLATION_FUNCTIONS = {
		translations.gettext: "_",
		translations.ngettext: "ngettext",
		translations.pgettext: "pgettext",
		translations.npgettext: "npgettext"
	}
	# Point _ to the translation object in the globals namespace of the caller frame
	try:
		callerFrame = inspect.currentframe().f_back
		module = inspect.getmodule(callerFrame)
		for funcName, installAs in _TRANSLATION_FUNCTIONS.items():
			setattr(module, installAs, funcName)
	finally:
		del callerFrame # Avoid reference problems with frames (per python docs)

def _translatedManifestPaths(lang=None, forBundle=False):
	if lang is None:
		lang = languageHandler.getLanguage() # can't rely on default keyword arguments here.
	langs=[lang]
	if '_' in lang:
		langs.append(lang.split('_')[0])
		if lang!='en' and not lang.startswith('en_'):
			langs.append('en')
	sep = "/" if forBundle else os.path.sep
	return [sep.join(("locale", lang, MANIFEST_FILENAME)) for lang in langs]


class AddonBundle(AddonBase):
	""" Represents the contents of an NVDA addon suitable for distribution.
	The bundle is compressed using the zip file format. Manifest information
	is available without the need for extraction."""
	def __init__(self, bundlePath: str):
		""" Constructs an L{AddonBundle} from a filename.
		@param bundlePath: The path for the bundle file.
		"""
		self._path = bundlePath
		# Read manifest:
		translatedInput=None
		try:
			z = zipfile.ZipFile(self._path, "r")
		except (zipfile.BadZipfile, FileNotFoundError) as e:
			raise AddonError(f"Invalid bundle file: {self._path}") from e
		with z:
			for translationPath in _translatedManifestPaths(forBundle=True):
				try:
					# ZipFile.open opens every file in binary mode.
					# decoding is handled by configobj.
					translatedInput = z.open(translationPath, 'r')
					break
				except KeyError:
					pass
			self._manifest = AddonManifest(
				# ZipFile.open opens every file in binary mode.
				# decoding is handled by configobj.
				z.open(MANIFEST_FILENAME, 'r'),
				translatedInput=translatedInput
			)
			if self.manifest.errors is not None:
				_report_manifest_errors(self.manifest)
				raise AddonError("Manifest file has errors.")

	def extract(self, addonPath: Optional[str] = None):
		""" Extracts the bundle content to the specified path.
		The addon will be extracted to L{addonPath}
		@param addonPath: Path where to extract contents.
		"""
		if addonPath is None:
			addonPath = self.pendingInstallPath

		with zipfile.ZipFile(self._path, 'r') as z:
			for info in z.infolist():
				if isinstance(info.filename, bytes):
					# #2505: Handle non-Unicode file names.
					# Most archivers seem to use the local OEM code page, even though the spec says only cp437.
					# HACK: Overriding info.filename is a bit ugly, but it avoids a lot of code duplication.
					info.filename = info.filename.decode("cp%d" % winKernel.kernel32.GetOEMCP())
				z.extract(info, addonPath)

	@property
	def manifest(self) -> "AddonManifest":
		""" Gets the manifest for the represented Addon.
		"""
		return self._manifest

	def __repr__(self):
		return "<AddonBundle at %s>" % self._path

def createAddonBundleFromPath(path, destDir=None):
	""" Creates a bundle from a directory that contains a a addon manifest file."""
	basedir = path
	# If  caller did not provide a destination directory name
	# Put the bundle at the same level as the add-on's top-level directory,
	# That is, basedir/..
	if destDir is None:
		destDir = os.path.dirname(basedir)
	manifest_path = os.path.join(basedir, MANIFEST_FILENAME)
	if not os.path.isfile(manifest_path):
		raise AddonError("Can't find %s manifest file." % manifest_path)
	with open(manifest_path, 'rb') as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		raise AddonError("Manifest file has errors.")
	bundleFilename = "%s-%s.%s" % (manifest['name'], manifest['version'], BUNDLE_EXTENSION)
	bundleDestination = os.path.join(destDir, bundleFilename)
	with zipfile.ZipFile(bundleDestination, 'w') as z:
		# FIXME: the include/exclude feature may or may not be useful. Also python files can be pre-compiled.
		for dir, dirnames, filenames in os.walk(basedir):
			relativePath = os.path.relpath(dir, basedir)
			for filename in filenames:
				pathInBundle = os.path.join(relativePath, filename)
				absPath = os.path.join(dir, filename)
				z.write(absPath, pathInBundle)
	return AddonBundle(bundleDestination)


def _report_manifest_errors(manifest):
	log.warning("Error loading manifest:\n%s", manifest.errors)


class AddonManifest(ConfigObj):
	""" Add-on manifest file. It contains metadata about an NVDA add-on package. """
	configspec = ConfigObj(StringIO(
	"""
# NVDA Add-on Manifest configuration specification
# Add-on unique name
# Suggested convention is lowerCamelCase.
name = string()

# short summary (label) of the add-on to show to users.
summary = string()

# Long description with further information and instructions
description = string(default=None)

# Name of the author or entity that created the add-on
author = string()

# Version of the add-on.
# Suggested convention is <major>.<minor>.<patch> format.
version = string()

# The minimum required NVDA version for this add-on to work correctly.
# Should be less than or equal to lastTestedNVDAVersion
minimumNVDAVersion = apiVersion(default="0.0.0")

# Must be greater than or equal to minimumNVDAVersion
lastTestedNVDAVersion = apiVersion(default="0.0.0")

# URL for more information about the add-on, e.g. a homepage.
# Should begin with https://
url = string(default=None)

# Name of default documentation file for the add-on.
docFileName = string(default=None)

# NOTE: apiVersion:
# EG: 2019.1.0 or 0.0.0
# Must have 3 integers separated by dots.
# The first integer must be a Year (4 characters)
# "0.0.0" is also valid.
# The final integer can be left out, and in that case will default to 0. E.g. 2019.1

"""))

	def __init__(self, input, translatedInput=None):
		""" Constructs an L{AddonManifest} instance from manifest string data
		@param input: data to read the manifest information
		@type input: a fie-like object.
		@param translatedInput: translated manifest input
		@type translatedInput: file-like object
		"""
		super(AddonManifest, self).__init__(input, configspec=self.configspec, encoding='utf-8', default_encoding='utf-8')
		self._errors = None
		val = Validator({"apiVersion":validate_apiVersionString})
		result = self.validate(val, copy=True, preserve_errors=True)
		if result != True:
			self._errors = result
		elif True != self._validateApiVersionRange():
			self._errors = "Constraint not met: minimumNVDAVersion ({}) <= lastTestedNVDAVersion ({})".format(
				self.get("minimumNVDAVersion"),
				self.get("lastTestedNVDAVersion")
			)
		self._translatedConfig = None
		if translatedInput is not None:
			self._translatedConfig = ConfigObj(translatedInput, encoding='utf-8', default_encoding='utf-8')
			for k in ('summary','description'):
				val=self._translatedConfig.get(k)
				if val:
					self[k]=val

	@property
	def errors(self):
		return self._errors

	def _validateApiVersionRange(self):
		lastTested = self.get("lastTestedNVDAVersion")
		minRequiredVersion = self.get("minimumNVDAVersion")
		return minRequiredVersion <= lastTested


def validate_apiVersionString(value: str) -> Tuple[int, int, int]:
	"""
	@raises: configobj.validate.ValidateError on validation error
	"""
	from configobj.validate import ValidateError
	if not value or value == "None":
		return (0, 0, 0)
	if not isinstance(value, string_types):
		raise ValidateError('Expected an apiVersion in the form of a string. EG "2019.1.0"')
	try:
		return addonAPIVersion.getAPIVersionTupleFromString(value)
	except ValueError as e:
		raise ValidateError('"{}" is not a valid API Version string: {}'.format(value, e))
