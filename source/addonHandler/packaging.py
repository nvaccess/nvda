# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2022 NV Access Limited, Rui Batista, Zahari Yurukov, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions to add python modules within addon directories to python module paths.
"""

import os.path
from typing import (
	List,
	Optional,
)
from types import ModuleType
import globalVars
import config
import sys
import importlib

ADDONS_MODULE_NAME = "addons"
"""The name of an importable module that nessts add-on code for every active add-on."""

def initializeModulePackagePaths():
	"""Initializes the module package paths for drivers and plugins.
	This ensures that drivers (such as braille display drivers) or plugins (such as app modules)
	can be discovered by NVDA.
	"""
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
		addDirsToPythonPackagePath(module)


def addDirsToPythonPackagePath(module: ModuleType, subdir: Optional[str] = None):
	"""Add add-on and scratchpath directories for a module to the search path (__path__) of a Python package.
	C{subdir} is added to each directory. It defaults to the name of the Python package.
	@param module: The root module of the package.
	@param subdir: The subdirectory to be used, C{None} for the name of C{module}.
	"""
	if config.isAppX or globalVars.appArgs.disableAddons:
		return
	from . import getRunningAddons
	for addon in getRunningAddons():
		addon.addToPackagePath(module)
	if globalVars.appArgs.secure or not config.conf['development']['enableScratchpadDir']:
		return
	if not subdir:
		subdir = module.__name__
	fullPath = os.path.join(config.getScratchpadDir(), subdir)
	if fullPath in module.__path__:
		return
	# Ensure this directory exists otherwise pkgutil.iter_importers may emit None for missing paths.
	if not os.path.isdir(fullPath):
		os.makedirs(fullPath)
	# Insert this path at the beginning  of the module's search paths.
	# The module's search paths may not be a mutable list, so replace it with a new one
	pathList = [fullPath]
	pathList.extend(module.__path__)
	module.__path__ = pathList


def _createModule(moduleName: str, submoduleSearchLocations: Optional[List[str]] = None):
	"""Creates a module with the given moduleName and adds it to sys.modules.
	This ensures that the module can be imported.
	@param moduleName: The name of the module, e.g. addons or addons.example.
	@param submoduleSearchLocations: Can be provided if the module has to be a python namespace package.
	"""
	if moduleName in sys.modules:
		# module already initialized
		return
	spec = importlib._bootstrap.ModuleSpec(moduleName, None)
	if submoduleSearchLocations:
		spec.submodule_search_locations = submoduleSearchLocations
	module = importlib.util.module_from_spec(spec)
	sys.modules[module.__name__] = module


def initializeAddonsNamespacePackage():
	"""Initializes the addons namespace package.
	This ensures that all python code in an add-on can be imported, even if code lives
	outside one of the standard package paths, such as appModules or globalPlugins.
	For example, if an add-on named example has a python module called lib,
	that module can be imported with `from addons.example import lib`
	"""
	# First, ensure that there is a placeholder addons module that does nothing,
	# i.e. it has no associated path but is solely there to nest add-ons under it.
	_createModule(ADDONS_MODULE_NAME)

	from . import getRunningAddons
	for addon in getRunningAddons():
		_createModule(f"{ADDONS_MODULE_NAME}.{addon.name}", [addon.path])
