# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os
import re
import zipfile

import SCons


def _generateModuleList(
		target: list[SCons.Node.FS.File],
		source: list[SCons.Node.FS.Dir],
		env: SCons.Environment.Environment
) -> None:
	"""
	Generate a list of Python modules from compiled '.pyc' files within `library.zip` in the source folder.

	This function lists all '.pyc' files contained in `library.zip`, converts their paths to Python module
	format, performs a sanity check to ensure a specific module is present, and then writes the list of
	modules to a specified output file for packaging as an AppVeyor artefact.

	:param target: A single element list containing the target file node where the list of modules will be
				written.
	:param source: A single element list containing the source NVDA dist folder to be processed.
				The folder should contain `library.zip` from which the '.pyc' files will be listed.
	:param env: The SCons environment context under which this function is executed. This parameter provides
				access to SCons construction variables, methods, and tools.
	:return: None. The function does not return anything but writes the list of modules to the target file.
	:raises ValueError: If the specified sanity check module (e.g., 'NVDAObjects.UIA') is not found in the
						list of modules extracted from the zipfile.
	:raises FileNotFoundError: If the specified zipfile in `source` does not exist.
	"""
	# List all .pyc files in the library.zip
	libraryZipPath = os.path.join(source[0].path, "library.zip")
	if not os.path.exists(libraryZipPath):
		raise FileNotFoundError(f"The zipfile {libraryZipPath} does not exist.")
	pycFiles = [f for f in zipfile.ZipFile(libraryZipPath, "r").namelist() if f.endswith(".pyc")]

	# Convert the file paths to python module format
	# eg: NVDAObjects/IAccessible/__init__.pyc --> NVDAObjects.IAccessible
	importedModules = sorted({
		re.sub(r"(.__init__|.__version__|._version)?\.pyc$", "", module_path).replace("/", ".")
		for module_path in pycFiles
	})

	# Sanity check for something guaranteed to be in library.zip
	if "NVDAObjects.UIA" not in importedModules:
		raise ValueError("Expected module NVDAObjects.UIA not found in the zipfile.")

	# Store the list to file
	with open(str(target[0]), "w", encoding="utf-8") as file:
		file.write("\n".join(importedModules))


def generate(env: SCons.Environment.Environment):
	env["BUILDERS"]["GenerateModuleList"] = SCons.Builder.Builder(
		action=SCons.Action.Action(_generateModuleList))


def exists(env: SCons.Environment.Environment) -> bool:
	return True
