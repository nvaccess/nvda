# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides robot library functions for NVDA system tests.
It contains helper methods for system tests, most specifically related to NVDA
- setup config,
- starting
- quiting
- config cleanup
This is in contrast with the `SystemTestSpy/speechSpy*.py files,
which provide library functions related to monitoring NVDA and asserting NVDA output.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from os.path import join as _pJoin, abspath as _abspath, expandvars as _expandvars
import tempfile as _tempFile
from typing import Optional

from robotremoteserver import (
	test_remote_server as _testRemoteServer,
	stop_remote_server as _stopRemoteServer,
)
from SystemTestSpy import (
	_blockUntilConditionMet,
	_getLib,
	_nvdaSpyAlias,
	configManager
)

# Imported for type information
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem as _OpSysLib
from robot.libraries.Process import Process as _Process
from robot.libraries.Remote import Remote as _Remote

builtIn: BuiltIn = BuiltIn()
opSys: _OpSysLib = _getLib('OperatingSystem')
process: _Process = _getLib('Process')


class _NvdaLocationData:

	def __init__(self):
		# robot is expected to be run from the NVDA repo root directory. We want all repo specific
		# paths to be relative to this. This would allow us to change where it is run from if we decided to.
		self.repoRoot = _abspath("./")
		self.stagingDir = _tempFile.gettempdir()
		opSys.directory_should_exist(self.stagingDir)

		self.whichNVDA = builtIn.get_variable_value("${whichNVDA}", "source")
		if self.whichNVDA == "source":
			self._runNVDAFilePath = _pJoin(self.repoRoot, "source/nvda.pyw")
			self.baseNVDACommandline = f"pyw -3.7-32 {self._runNVDAFilePath}"
		elif self.whichNVDA == "installed":
			self._runNVDAFilePath = _pJoin(_expandvars('%PROGRAMFILES%'), 'nvda', 'nvda.exe')
			self.baseNVDACommandline = f'"{str(self._runNVDAFilePath)}"'
		else:
			raise AssertionError("RobotFramework should be run with argument: '-v whichNVDA [source|installed]'")

		self.profileDir = _pJoin(self.stagingDir, "nvdaProfile")
		self.logPath = _pJoin(self.profileDir, 'nvda.log')
		self.preservedLogsDir = _pJoin(
			builtIn.get_variable_value("${OUTPUT DIR}"),
			"nvdaTestRunLogs"
		)

	def ensurePathsExist(self):
		opSys.file_should_exist(self._runNVDAFilePath, "Unable to start NVDA unless path exists.")
		opSys.create_directory(self.profileDir)
		opSys.create_directory(self.preservedLogsDir)


_locations = _NvdaLocationData()


class NvdaLib:
	"""Robot Framework library for interacting with NVDA.
	Notable:
	- NvdaLib.nvdaSpy is a library instance for getting speech and other information out of NVDA
	"""
	def __init__(self):
		self.nvdaSpy = None  #: Optional[SystemTestSpy.speechSpyGlobalPlugin.NVDASpyLib]
		self.nvdaHandle: Optional[int] = None

	@staticmethod
	def _createTestIdFileName(name):
		suiteName = builtIn.get_variable_value("${SUITE NAME}")
		testName = builtIn.get_variable_value("${TEST NAME}")
		outputFileName = f"{suiteName}-{testName}-{name}".replace(" ", "_")
		return outputFileName

	@staticmethod
	def setup_nvda_profile(configFileName):
		configManager.setupProfile(
			_locations.repoRoot,
			configFileName,
			_locations.stagingDir
		)

	@staticmethod
	def teardown_nvda_profile():
		configManager.teardownProfile(
			_locations.stagingDir
		)

	nvdaProcessAlias = 'nvdaAlias'
	_spyServerPort = 8270  # is `registered by IANA` for remote server usage. Two ASCII values:'RF'
	_spyServerURI = f'http://127.0.0.1:{_spyServerPort}'
	_spyAlias = _nvdaSpyAlias

	def _startNVDAProcess(self):
		"""Start NVDA.
		Use debug logging, replacing any current instance, using the system test profile directory
		"""
		_locations.ensurePathsExist()
		command = (
			f"{_locations.baseNVDACommandline}"
			f" --debug-logging"
			f" -r"
			f" -c \"{_locations.profileDir}\""
			f" --log-file \"{_locations.logPath}\""
		)
		self.nvdaHandle = handle = process.start_process(
			command,
			shell=True,
			alias=self.nvdaProcessAlias,
			stdout=_pJoin(_locations.preservedLogsDir, self._createTestIdFileName("stdout.txt")),
			stderr=_pJoin(_locations.preservedLogsDir, self._createTestIdFileName("stderr.txt")),
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

		builtIn.log(f"Waiting for {self._spyAlias} to be available at: {self._spyServerURI}", level='DEBUG')
		# Importing the 'Remote' library always succeeds, even when a connection can not be made.
		# If that happens, then some 'Remote' keyword will fail at some later point.
		# therefore we use '_testRemoteServer' to ensure that we can in fact connect before proceeding.
		_blockUntilConditionMet(
			getValue=lambda: _testRemoteServer(self._spyServerURI, log=False),
			giveUpAfterSeconds=10,
			errorMessage=f"Unable to connect to {self._spyAlias}",
		)
		builtIn.log(f"Connecting to {self._spyAlias}", level='DEBUG')
		# If any remote call takes longer than this, the connection will be closed!
		maxRemoteKeywordDurationSeconds = 30
		builtIn.import_library(
			"Remote",  # name of library to import
			# Arguments to construct the library instance:
			f"uri={self._spyServerURI}",
			f"timeout={maxRemoteKeywordDurationSeconds}",
			# Set an alias for the imported library instance
			"WITH NAME",
			self._spyAlias,
		)
		builtIn.log(f"Getting {self._spyAlias} library instance", level='DEBUG')
		self.nvdaSpy = self._addMethodsToSpy(builtIn.get_library_instance(self._spyAlias))
		# Ensure that keywords timeout before `timeout` given to `Remote` library,
		# otherwise we lose control over NVDA.
		self.nvdaSpy.init_max_keyword_duration(maxSeconds=maxRemoteKeywordDurationSeconds)

	@staticmethod
	def _addMethodsToSpy(remoteLib: _Remote):
		""" Adds a method for each keywords on the remote library.
		@param remoteLib: the library to augment with methods.
		@rtype: SystemTestSpy.speechSpyGlobalPlugin.NVDASpyLib
		@return: The library augmented with methods for all keywords.
		"""
		# Add methods back onto the lib so they can be called directly rather than manually calling run_keyword
		def _makeKeywordCaller(lib, keyword):
			def runKeyword(*args, **kwargs):
				builtIn.log(
					f"{keyword}"
					f"{f' {args}' if args else ''}"
					f"{f' {kwargs}' if kwargs else ''}"
				)
				return lib.run_keyword(keyword, args, kwargs)
			return runKeyword

		for name in remoteLib.get_keyword_names():
			setattr(
				remoteLib,
				name,
				_makeKeywordCaller(remoteLib, name)
			)
		return remoteLib

	def start_NVDA(self, settingsFileName):
		builtIn.log(f"Starting NVDA with config: {settingsFileName}")
		self.setup_nvda_profile(settingsFileName)
		nvdaProcessHandle = self._startNVDAProcess()
		process.process_should_be_running(nvdaProcessHandle)
		self._connectToRemoteServer()
		self.nvdaSpy.wait_for_NVDA_startup_to_complete()
		return nvdaProcessHandle

	def save_NVDA_log(self):
		"""NVDA logs are saved to the ${OUTPUT DIR}/nvdaTestRunLogs/${SUITE NAME}-${TEST NAME}-nvda.log"""
		builtIn.log("Saving NVDA log")
		saveToPath = self.create_preserved_test_output_filename("nvda.log")
		opSys.copy_file(
			_locations.logPath,
			saveToPath
		)
		builtIn.log(f"Log saved to: {saveToPath}", level='DEBUG')

	def create_preserved_test_output_filename(self, fileName):
		"""EG for nvda.log path will become:
			${OUTPUT DIR}/nvdaTestRunLogs/${SUITE NAME}-${TEST NAME}-nvda.log
		"""
		return _pJoin(_locations.preservedLogsDir, self._createTestIdFileName(fileName))

	def quit_NVDA(self):
		builtIn.log("Stopping nvdaSpy server: {}".format(self._spyServerURI))
		try:
			_stopRemoteServer(self._spyServerURI, log=False)
			process.run_process(
				f"{_locations.baseNVDACommandline} -q --disable-addons",
				shell=True,
			)
			process.wait_for_process(self.nvdaHandle)
		except Exception:
			raise
		finally:
			self.save_NVDA_log()
			# remove the spy so that if nvda is run manually against this config it does not interfere.
			self.teardown_nvda_profile()


def getSpyLib():
	""" Gets the spy library instance. This has been augmented with methods for all supported keywords.
	Requires NvdaLib and nvdaSpy (remote library - see speechSpyGlobalPlugin) to be initialised.
	On failure check order of keywords in Robot log and NVDA log for failures.
	@rtype: SystemTestSpy.speechSpyGlobalPlugin.NVDASpyLib
	@return: Remote NVDA spy Robot Framework library.
	"""
	nvdaLib = _getLib("NvdaLib")
	spy = nvdaLib.nvdaSpy
	if spy is None:
		raise AssertionError("Spy not yet available, check order of keywords and NVDA log for errors.")
	return spy
