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
opSys: _OpSysLib = _getLib('OperatingSystem')
process: _Process = _getLib('Process')


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
	""" Assembles the required files for the system test spy.
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
		libsDest=spyPackageLibsDir
	)

	try:
		opSys.directory_should_exist(_pJoin(spyPackageLibsDir, "xmlrpc"))
	except AssertionError:
		# installed copies of NVDA <= 2020.4 don't copy this over
		_copyPythonLibs(
			pythonImports=[  # relative to the python path
				"xmlrpc",
			],
			libsDest=spyPackageLibsDir
		)

	# install the global plugin
	# Despite duplication, specify full paths for clarity.
	opSys.copy_file(
		_pJoin(repoRoot, "tests", "system", "libraries", "SystemTestSpy", "speechSpyGlobalPlugin.py"),
		_pJoin(scratchPadDir, "globalPlugins", "speechSpyGlobalPlugin", "__init__.py")
	)
	opSys.copy_file(
		_pJoin(repoRoot, "tests", "system", "libraries", "SystemTestSpy", "blockUntilConditionMet.py"),
		_pJoin(scratchPadDir, "globalPlugins", "speechSpyGlobalPlugin")
	)
	# install the test spy speech synth
	opSys.copy_file(
		_pJoin(repoRoot, "tests", "system", "libraries", "SystemTestSpy", "speechSpySynthDriver.py"),
		_pJoin(scratchPadDir, "synthDrivers", "speechSpySynthDriver.py")
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
	builtIn.log("Copying files into NVDA profile", level='DEBUG')
	opSys.copy_file(
		# Despite duplication, specify full paths for clarity.
		_pJoin(repoRoot, "tests", "system", "nvdaSettingsFiles", settingsFileName),
		_pJoin(stagingDir, "nvdaProfile", "nvda.ini")
	)
	if gesturesFileName is not None:
		opSys.copy_file(
			# Despite duplication, specify full paths for clarity.
			_pJoin(repoRoot, "tests", "system", "nvdaSettingsFiles", gesturesFileName),
			_pJoin(stagingDir, "nvdaProfile", "gestures.ini")
		)
	# create a package to use as the globalPlugin
	_installSystemTestSpyToScratchPad(
		repoRoot,
		_pJoin(stagingDir, "nvdaProfile", "scratchpad")
	)


def teardownProfile(stagingDir: str):
	""" Cleans up the profile directory
	@todo: this could have an option to preserve the profile for debugging purposes.
	@param stagingDir: Where the profile was constructed
	"""
	builtIn.log("Cleaning up NVDA profile", level='DEBUG')
	opSys.remove_directory(
		_pJoin(stagingDir, "nvdaProfile"),
		recursive=True
	)
