# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2023 NV Access Limited, Rui Batista, Zahari Yurukov, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions to add python modules within addon directories to python module paths."""

import os.path
from typing import Optional
from types import ModuleType
import globalVars
import config
from keyword import iskeyword


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
	if globalVars.appArgs.secure or not config.conf["development"]["enableScratchpadDir"]:
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


def isModuleName(name: str) -> bool:
	"""When adding a module to sys.modules, it is important to check module name validity.
	the L{str.isidentifier} method checks whether a string is a valid python identifier,
	however this includes identifiers like 'def' and 'class', which are definitely invalid module names.
	Therefore a valid module name should be an identifier but not a keyword.
	A valid module name can also contain dots, but a dot is considered invalid in identifiers.
	Therefore, use dot as a split separator and check all the name parts independently.
	@param moduleName: De module name to check for naming conventions.
	@returns: Whether the module name is valid.
	"""
	return all(n.isidentifier() and not iskeyword(n) for n in name.split("."))
