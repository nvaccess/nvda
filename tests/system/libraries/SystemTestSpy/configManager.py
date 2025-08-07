# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""
This module is designed to construct and install the speechSpyGlobalPlugin, speechSpySynthDriver, and NVDA
NVDA config before NVDA is started by the system tests.
"""

from os.path import join as _pJoin
from .getLib import _getLib
import sys
from typing import Optional

# Imported for type information
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem as _OpSysLib
from robot.libraries.Process import Process as _Process

builtIn: BuiltIn = BuiltIn()
opSys: _OpSysLib = _getLib("OperatingSystem")
process: _Process = _getLib("Process")


def _findDepPath(depFileName, searchPaths):
	import os

	for path in searchPaths:
		filePath = _pJoin(path, f"{depFileName}.py")
		if os.path.isfile(filePath):
			return filePath
		elif os.path.isfile(_pJoin(path, depFileName, "__init__.py")):
			return _pJoin(path, depFileName)
	raise AssertionError("Unable to find required system test spy dependency: {}".format(depFileName))


def _installSystemTestSpyToScratchPad(repoRoot: str, scratchPadDir: str):
	"""Assembles the required files for the system test spy.
	Most notably this includes:
	- speechSpyGlobalPlugin - The actual remote Robot library used to get information out of NVDA
	- speechSpySynthDriver - A synth driver that captures and caches speech to provide to speechSpyGlobalPlugin
	"""

	# The globalPlugin will modify the python path to include to this sub dir
	spyPackageLibsDir = _pJoin(scratchPadDir, "globalPlugins", "speechSpyGlobalPlugin", "libs")
	opSys.create_directory(spyPackageLibsDir)
	# copy in required dependencies for global plugin
	_copyPythonLibs(
		pythonImports=[  # relative to the python path
			r"robotremoteserver",
		],
		libsDest=spyPackageLibsDir,
	)

	try:
		opSys.directory_should_exist(_pJoin(spyPackageLibsDir, "xmlrpc"))
	except AssertionError:
		# installed copies of NVDA <= 2020.4 don't copy this over
		_copyPythonLibs(
			pythonImports=[  # relative to the python path
				"xmlrpc",
			],
			libsDest=spyPackageLibsDir,
		)

	# install the global plugin
	# Despite duplication, specify full paths for clarity.
	opSys.copy_file(
		_pJoin(repoRoot, "tests", "system", "libraries", "SystemTestSpy", "speechSpyGlobalPlugin.py"),
		_pJoin(scratchPadDir, "globalPlugins", "speechSpyGlobalPlugin", "__init__.py"),
	)
	opSys.copy_file(
		_pJoin(repoRoot, "tests", "system", "libraries", "SystemTestSpy", "blockUntilConditionMet.py"),
		_pJoin(scratchPadDir, "globalPlugins", "speechSpyGlobalPlugin"),
	)
	# install the test spy speech synth
	opSys.copy_file(
		_pJoin(repoRoot, "tests", "system", "libraries", "SystemTestSpy", "speechSpySynthDriver.py"),
		_pJoin(scratchPadDir, "synthDrivers", "speechSpySynthDriver.py"),
	)


def _copyPythonLibs(pythonImports, libsDest):
	import os

	searchPaths = sys.path
	for lib in pythonImports:
		libSource = _findDepPath(lib, searchPaths)
		if os.path.isdir(libSource):
			opSys.copy_directory(libSource, libsDest)
		elif os.path.isfile(libSource):
			opSys.copy_file(libSource, libsDest)


def setupProfile(
	repoRoot: str,
	settingsFileName: str,
	stagingDir: str,
	gesturesFileName: Optional[str] = None,
):
	builtIn.log("Copying files into NVDA profile", level="DEBUG")
	opSys.copy_file(
		# Despite duplication, specify full paths for clarity.
		_pJoin(repoRoot, "tests", "system", "nvdaSettingsFiles", settingsFileName),
		_pJoin(stagingDir, "nvdaProfile", "nvda.ini"),
	)
	if settingsFileName == "standard-doLoadMockModel.ini":
		_configModels()

	if gesturesFileName is not None:
		opSys.copy_file(
			# Despite duplication, specify full paths for clarity.
			_pJoin(repoRoot, "tests", "system", "nvdaSettingsFiles", gesturesFileName),
			_pJoin(stagingDir, "nvdaProfile", "gestures.ini"),
		)
	# create a package to use as the globalPlugin
	_installSystemTestSpyToScratchPad(
		repoRoot,
		_pJoin(stagingDir, "nvdaProfile", "scratchpad"),
	)


def teardownProfile(stagingDir: str):
	"""Cleans up the profile directory
	@todo: this could have an option to preserve the profile for debugging purposes.
	@param stagingDir: Where the profile was constructed
	"""
	builtIn.log("Cleaning up NVDA profile", level="DEBUG")
	opSys.remove_directory(
		_pJoin(stagingDir, "nvdaProfile"),
		recursive=True,
	)


def _configModels():
	import tempfile
	import os
	from .mockModels import MockVisionEncoderDecoderGenerator

	generator = MockVisionEncoderDecoderGenerator(random_seed=8)
	# Generate all files relative to repo root
	tempDir = tempfile.gettempdir()
	ini_path = os.path.join(tempDir, "nvdaProfile", "nvda.ini")
	models_directory = os.path.join(tempDir, "nvdaProfile", "models", "mock", "vit-gpt2-image-captioning")
	generator.generateAllFiles(models_directory)
	# The location of the temp folder can notbe determined in the nvda.ini file, so change it manually
	_updateIniForModels(ini_path, models_directory)


def _updateIniForModels(ini_path, output_dir):
	"""
	Update only the value of 'defaultModelPath' under [automatedImageDescriptions] section
	in the INI file, preserving original formatting, indentation, and casing.
	"""
	import os

	# Normalize the path for Windows (e.g., use backslashes)
	new_path = os.path.normpath(output_dir)

	# Read original lines
	with open(ini_path, "r", encoding="utf-8") as f:
		lines = f.readlines()

	# Flags to track if we are in the [automatedImageDescriptions] section
	in_caption_section = False

	# Updated lines will be stored here
	updated_lines = []

	for line in lines:
		# Detect section headers
		strip_line = line.strip()
		if strip_line.startswith("[") and strip_line.endswith("]"):
			in_caption_section = strip_line.lower() == "[automatedimagedescriptions]"

		# If inside automatedImageDescriptions section, and line contains defaultModelPath (case-insensitive)
		if in_caption_section and "defaultModelPath" in line:
			# Preserve original indentation and formatting
			prefix, sep, _ = line.partition("=")
			updated_line = f"{prefix}{sep} {new_path}\n"
			updated_lines.append(updated_line)
		else:
			# Keep line as is
			updated_lines.append(line)

	# Write back the updated lines
	with open(ini_path, "w", encoding="utf-8") as f:
		f.writelines(updated_lines)
