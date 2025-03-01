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
import zipfile
from typing import TYPE_CHECKING, Callable, Optional

import addonAPIVersion
import config
import extensionPoints
import NVDAState
from logHandler import log
from NVDAState import WritePaths
from utils.caseInsensitiveCollections import CaseInsensitiveSet

from .addon import Addon
from .addonBase import AddonError
from .AddonBundle import AddonBundle
from .AddonManifest import MANIFEST_FILENAME, AddonManifest, _report_manifest_errors
from .addonState import AddonStateCategory, state
from .addonVersionCheck import isAddonCompatible
from .packaging import initializeModulePackagePaths

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
