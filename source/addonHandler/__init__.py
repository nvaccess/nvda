# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2025 Rui Batista, NV Access Limited, Noelia Ruiz Martínez, Joseph Lee, Babbage B.V.,
# Arnold Loubriat, Łukasz Golonka, Leonard de Ruijter, Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from __future__ import annotations  # Avoids quoting of forward references

import collections
import inspect
import itertools
import os.path
import shutil
import sys
from typing import TYPE_CHECKING, Callable, Optional

import addonAPIVersion
import config
import extensionPoints
import NVDAState
from logHandler import log
from NVDAState import WritePaths
from utils.caseInsensitiveCollections import CaseInsensitiveSet

from .addon import Addon
from .addonBase import AddonError, AddonBase
from .AddonBundle import AddonBundle, BUNDLE_EXTENSION
from .addonState import AddonStateCategory, state
from .addonVersionCheck import isAddonCompatible
from .packaging import initializeModulePackagePaths

if TYPE_CHECKING:
	from addonStore.models.addon import AddonHandlerModelGeneratorT  # noqa: F401

stateFilename = "addonsState.pickle"
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


def getRunningAddons() -> "AddonHandlerModelGeneratorT":
	"""Returns currently loaded add-ons.

	:return: Generator of currently loaded add-ons
	"""
	return getAvailableAddons(filterFunc=lambda addon: addon.isRunning)


def getIncompatibleAddons(
	currentAPIVersion=addonAPIVersion.CURRENT,
	backCompatToAPIVersion=addonAPIVersion.BACK_COMPAT_TO,
) -> "AddonHandlerModelGeneratorT":
	"""Returns a generator of the add-ons that are not compatible.

	:param currentAPIVersion: The current API version to check compatibility against
	:param backCompatToAPIVersion: The oldest API version to consider compatible
	:return: Generator of incompatible add-ons
	"""
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


def removeFailedDeletion(path: os.PathLike) -> None:
	"""Attempts to remove a path that failed to be deleted.

	First tries to remove the directory tree, then attempts to remove the file directly.
	Logs an error if removal fails.

	:param path: The path to remove
	"""
	shutil.rmtree(path, ignore_errors=True)
	if os.path.exists(path):
		try:
			os.remove(path)
		except Exception:
			pass
	if os.path.exists(path):
		log.error(f"Failed to delete path {path}, try removing manually")


def disableAddonsIfAny() -> None:
	"""Disables add-ons if told to do so by the user from add-on store.

	This is usually executed before refreshing the list of available add-ons.
	Updates the state categories for disabled, pending disable/enable, and compatibility override.
	"""
	# Pull in and enable add-ons that should be disabled and enabled, respectively.
	state[AddonStateCategory.DISABLED] |= state[AddonStateCategory.PENDING_DISABLE]
	state[AddonStateCategory.DISABLED] -= state[AddonStateCategory.PENDING_ENABLE]
	# Remove disabled add-ons from having overridden compatibility
	state[AddonStateCategory.OVERRIDE_COMPATIBILITY] -= state[AddonStateCategory.DISABLED]
	# Clear pending disables and enables
	state[AddonStateCategory.PENDING_DISABLE].clear()
	state[AddonStateCategory.PENDING_ENABLE].clear()


def initialize() -> None:
	"""Initializes the add-ons subsystem.

	Loads add-on state, processes pending installations/removals, and initializes module package paths.
	"""
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


def terminate() -> None:
	"""Terminates the add-ons subsystem.

	Currently does nothing, but exists for symmetry with initialize().
	"""
	pass


def _getDefaultAddonPaths() -> list[str]:
	r"""Returns paths where addons can be found.

	For now, only <userConfig>\addons is supported.

	:return: List of directory paths where add-ons can be found
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

	:param path: Path from where to find addon directories
	:param isFirstLoad: Whether this is the first load of add-ons during NVDA startup
	:return: Generator of available add-ons from the specified path
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

	:param refresh: Whether or not to query the file system for available add-ons
	:param filterFunc: A function that allows filtering of add-ons.
	   It takes an Addon as its only argument and returns a bool indicating
	   whether the add-on matches the provided filter
	:param isFirstLoad: Should add-ons that are pending installations/removal
	   from the file system be installed/removed
	:return: Generator of available add-ons that match the filter criteria
	:raises TypeError: If filterFunc is provided but is not callable
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
	"""Extracts an Addon bundle into a unique subdirectory of the user addons directory,
	marking the addon as needing 'install completion' on NVDA restart.

	:param bundle: The add-on bundle to install.
	   The bundle._installExceptions property is modified to store any raised exceptions
	   during the installation process
	:return: The extracted add-on object, or None if the add-on bundle fails to be extracted.
	   Regardless if the add-on installation failed, the created add-on object from the bundle should be returned
	   to give caller a chance to clean-up modules imported as part of install tasks.
	   This clean-up cannot be done here, as install tasks are blocking,
	   and this function returns as soon as they're started,
	   so removing modules before they're done may cause unpredictable effects
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


def getCodeAddon(obj=None, frameDist=1):
	"""Returns the Addon where obj is defined.

	If obj is None the caller code frame is assumed to allow simple retrieval of "current calling addon".

	:param obj: Python object or None for default behavior
	:param frameDist: How many frames is the caller code. Only change this for functions in this module
	:return: Addon instance
	:raises AddonError: If code does not belong to an add-on package
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


def initTranslation() -> None:
	"""Initializes the translation of an add-on.

	Sets up Gettext functions (_, ngettext, npgettext and pgettext) to point to
	the add-on's translation rather than to NVDA's one.

	This function should be called at the top of any module containing translatable strings
	and belonging to an add-on. It cannot be called in a module that does not belong to
	an add-on (e.g. in a subdirectory of the scratchpad).

	:raises AddonError: If called from a module that doesn't belong to an add-on
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


__all__ = [
	"state",
	"Addon",
	"AddonBase",
	"AddonError",
	"AddonStateCategory",
	"AddonBundle",
	"BUNDLE_EXTENSION",
	"createAddonBundleFromPath",
	"getRunningAddons",
	"getIncompatibleAddons",
	"removeFailedDeletion",
	"disableAddonsIfAny",
	"initialize",
	"terminate",
	"getAvailableAddons",
	"installAddonBundle",
	"getCodeAddon",
	"initTranslation",
]
