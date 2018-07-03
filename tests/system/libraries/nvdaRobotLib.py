# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides robot library functions for NVDA system tests. It contains helper methods for system tests,
most specifically related to the setup for, starting of, quiting of, and cleanup of, NVDA. This is in contrast with
the systemTestSpy.py file, which provides library functions related to monitoring / asserting NVDA output.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from os.path import join as _pJoin, abspath as _abspath, expandvars as _expandvars
import sys
from robotremoteserver import test_remote_server as _testRemoteServer, stop_remote_server as _stopRemoteServer
from systemTestUtils import _blockUntilConditionMet
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.Process import Process

builtIn = BuiltIn()  # type: BuiltIn
process = builtIn.get_library_instance('Process')  # type: Process
opSys = builtIn.get_library_instance('OperatingSystem')  # type: OperatingSystem

spyServerPort = 8270  # is `registered by IANA` for remote server usage. Two ASCII values:'RF'
spyServerURI = 'http://127.0.0.1:{}'.format(spyServerPort)
spyAlias = "nvdaSpy"


whichNVDA=builtIn.get_variable_value("${whichNVDA}", "source")
if whichNVDA=="source":
	baseNVDACommandline="pythonw source/nvda.pyw"
elif whichNVDA=="installed":
	baseNVDACommandline='"%s"'%_pJoin(_expandvars('%PROGRAMFILES%'),'nvda','nvda.exe')
print baseNVDACommandline

# Paths
systemTestSourceDir = _abspath("tests/system")
nvdaProfileWorkingDir = _pJoin(systemTestSourceDir, "nvdaProfile")
nvdaLogFilePath = _pJoin(nvdaProfileWorkingDir,'nvda.log')
systemTestSpyAddonName = "systemTestSpy"
testSpyPackageDest = _pJoin(nvdaProfileWorkingDir, "globalPlugins")


def _findDepPath(depFileName, searchPaths):
	import os
	print searchPaths
	for path in searchPaths:
		filePath = _pJoin(path, depFileName+".py")
		print filePath
		if os.path.isfile(filePath):
			return filePath
		elif os.path.isfile(_pJoin(path, depFileName, "__init__.py")):
			return _pJoin(path, depFileName)
	raise AssertionError("Unable to find required system test spy dependency: {}".format(depFileName))

# relative to the python path
requiredPythonImports = [
	r"robotremoteserver",
	r"SimpleXMLRPCServer",
	r"xmlrpclib",
]

def _createNvdaSpyPackage():
	import os
	searchPaths = sys.path
	profileSysTestSpyPackageStagingDir = _pJoin(systemTestSourceDir, systemTestSpyAddonName)
	# copy in required dependencies, the addon will modify the python path
	# to point to this sub dir
	spyPackageLibsDir = _pJoin(profileSysTestSpyPackageStagingDir, "libs")
	opSys.create_directory(spyPackageLibsDir)
	for lib in requiredPythonImports:
		libSource = _findDepPath(lib, searchPaths)
		if os.path.isdir(libSource):
			opSys.copy_directory(libSource, spyPackageLibsDir)
		elif os.path.isfile(libSource):
			opSys.copy_file(libSource, spyPackageLibsDir)

	opSys.copy_file(
		_pJoin(systemTestSourceDir, "libraries", systemTestSpyAddonName+".py"),
		_pJoin(profileSysTestSpyPackageStagingDir, "__init__.py")
	)
	opSys.copy_file(
		_pJoin(systemTestSourceDir, "libraries", "systemTestUtils.py"),
		profileSysTestSpyPackageStagingDir
	)
	return profileSysTestSpyPackageStagingDir


class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None

	def setup_nvda_profile(self, settingsFileName):
		builtIn.log("Copying files into NVDA profile")
		opSys.copy_file(
			_pJoin(systemTestSourceDir, "nvdaSettingsFiles", settingsFileName),
			_pJoin(nvdaProfileWorkingDir, "nvda.ini")
		)
		# create a package to use as the globalPlugin
		opSys.copy_directory(
			_createNvdaSpyPackage(),
			_pJoin(testSpyPackageDest, systemTestSpyAddonName)
		)

	def teardown_nvda_profile(self):
		builtIn.log("Removing files from NVDA profile")
		opSys.remove_file(
			_pJoin(nvdaProfileWorkingDir, "nvda.ini")
		)
		opSys.remove_directory(
			testSpyPackageDest,
			recursive=True
		)

	def _startNVDAProcess(self):
		"""Start NVDA.
		Use debug logging, replacing any current instance, using the system test profile directory
		"""
		self.nvdaHandle = handle = process.start_process(
			"{baseNVDACommandline} --debug-logging -r -c \"{nvdaProfileDir}\" --log-file \"{nvdaLogFilePath}\"".format(
				baseNVDACommandline=baseNVDACommandline,
				nvdaProfileDir=nvdaProfileWorkingDir,
				nvdaLogFilePath=nvdaLogFilePath
			),
			shell=True,
			alias='nvdaAlias'
		)
		return handle


	def _connectToRemoteServer(self):
		"""Connects to the nvdaSpyServer
		Because we do not know how far through the startup NVDA is, we have to poll
		to check that the server is available. Importing the library immediately seems
		to succeed, but then calling a keyword later fails with RuntimeError:
			"Connection to remote server broken: [Errno 10061]
				No connection could be made because the target machine actively refused it"
		Instead we wait until the remote server is available before importing the library and continuing.
		"""

		builtIn.log("Waiting for nvdaSpy to be available at: {}".format(spyServerURI))
		# Importing the 'Remote' library always succeeds, even when a connection can not be made.
		# If that happens, then some 'Remote' keyword will fail at some later point.
		# therefore we use '_testRemoteServer' to ensure that we can in fact connect before proceeding.
		_blockUntilConditionMet(
			getValue=lambda: _testRemoteServer(spyServerURI, log=False),
			giveUpAfterSeconds=10,
			errorMessage="Unable to connect to nvdaSpy",
		)
		builtIn.log("Connecting to nvdaSpy")
		maxRemoteKeywordDurationSeconds = 30  # If any remote call takes longer than this, the connection will be closed!
		builtIn.import_library(
			"Remote",  # name of library to import
			# Arguments to construct the library instance:
			"uri={}".format(spyServerURI),
			"timeout={}".format(maxRemoteKeywordDurationSeconds),
			# Set an alias for the imported library instance
			"WITH NAME",
			"nvdaSpy",
		)
		builtIn.log("Getting nvdaSpy library instance")
		self.nvdaSpy = builtIn.get_library_instance(spyAlias)
		self._runNvdaSpyKeyword("set_max_keyword_duration", maxSeconds=maxRemoteKeywordDurationSeconds)

	def _runNvdaSpyKeyword(self, keyword, *args, **kwargs):
		if not args: args = []
		if not kwargs: kwargs = {}
		builtIn.log("nvdaSpy keyword: {} args: {}, kwargs: {}".format(keyword, args, kwargs))
		return self.nvdaSpy.run_keyword(keyword, args, kwargs)

	def start_NVDA(self, settingsFileName):
		self.setup_nvda_profile(settingsFileName)
		nvdaProcessHandle = self._startNVDAProcess()
		process.process_should_be_running(nvdaProcessHandle)
		self._connectToRemoteServer()
		self._runNvdaSpyKeyword("wait_for_NVDA_startup_to_complete")
		return nvdaProcessHandle

	def save_NVDA_log(self):
		"""NVDA logs are saved to the ${OUTPUT DIR}/nvdaTestRunLogs/${SUITE NAME}-${TEST NAME}-nvda.log"""
		builtIn.log("saving NVDA log")
		outDir = builtIn.get_variable_value("${OUTPUT DIR}", )
		suiteName = builtIn.get_variable_value("${SUITE NAME}")
		testName = builtIn.get_variable_value("${TEST NAME}")
		outputFileName = "{suite}-{test}-nvda.log"\
			.format(
				suite=suiteName,
				test=testName,
			).replace(" ", "_")
		opSys.copy_file(
			nvdaLogFilePath,
			_pJoin(outDir, "nvdaTestRunLogs", outputFileName)
		)

	def quit_NVDA(self):
		builtIn.log("Stopping nvdaSpy server: {}".format(spyServerURI))
		_stopRemoteServer(spyServerURI, log=False)
		# remove the spy so that if nvda is run manually against this config it does not interfere.
		self.teardown_nvda_profile()
		process.run_process(
			"{baseNVDACommandline} -q --disable-addons".format(baseNVDACommandline=baseNVDACommandline),
			shell=True,
		)
		process.wait_for_process(self.nvdaHandle)
		self.save_NVDA_log()
