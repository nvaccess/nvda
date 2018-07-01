import os
from os.path import join as pathJoin
from os.path import abspath
from robotremoteserver import test_remote_server, stop_remote_server
from testutils import blockUntilConditionMet
from robot.libraries.BuiltIn import BuiltIn

builtIn = BuiltIn()
process = builtIn.get_library_instance('Process')
opSys = builtIn.get_library_instance('OperatingSystem')

spyServerPort = 8270  # is `registered by IANA` for remote server usage. Two ASCII values:'RF'
spyServerURI = 'http://127.0.0.1:{}'.format(spyServerPort)
spyAlias = "nvdaSpy"

nvdaLogFilePath = abspath("source/nvda.log")

systemTestSourceDir = abspath("tests/system")
nvdaProfileWorkingDir = pathJoin(systemTestSourceDir, "nvdaProfile")
nvdaSettingsSourceDir = pathJoin(systemTestSourceDir, "nvdaSettingsFiles")

# TODO: find a better way to share this testutils code!!
systemTestUtilsFileName = "testutils.py"
systemTestUtilsSource = pathJoin(systemTestSourceDir, "libraries", systemTestUtilsFileName)
systemTestSpyFileName = "systemTestSpy.py"
systemTestSpySource = pathJoin(systemTestSourceDir, "libraries", systemTestSpyFileName)
systemTestSpyInstallDir = pathJoin(nvdaProfileWorkingDir, "globalPlugins")
systemTestSpyInstalled = pathJoin(systemTestSpyInstallDir, systemTestSpyFileName)
systemTestUtilsInstalled = pathJoin(nvdaProfileWorkingDir, "systemTestLibs", systemTestUtilsFileName)


class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None

	def setup_nvda_profile(self, settingsFileName):
		builtIn.log("Copying files into NVDA profile")
		opSys.create_directory(systemTestSpyInstallDir)
		opSys.copy_file(systemTestSpySource, systemTestSpyInstallDir)
		opSys.copy_file(
			os.path.join(nvdaSettingsSourceDir, settingsFileName),
			os.path.join(nvdaProfileWorkingDir, "nvda.ini")
		)

	def teardown_nvda_profile(self):
		builtIn.log("Removing files from NVDA profile")
		# TODO: probably dont need to remove the raw python file?
		opSys.remove_file(systemTestSpyInstalled)
		opSys.remove_file(systemTestSpyInstalled+"c")  # also remove the .pyc
		opSys.remove_file(
			os.path.join(nvdaProfileWorkingDir, "nvda.ini")
		)

	def _startNVDAProcess(self):
		"""Start NVDA.
		Use debug logging, replacing any current instance, using the system test profile directory
		"""
		self.nvdaHandle = handle = process.start_process(
			"pythonw nvda.pyw --debug-logging -r -c \"{nvdaProfileDir}\"".format(nvdaProfileDir=nvdaProfileWorkingDir),
			cwd='source',
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
		# therefore we use 'test_remote_server' to ensure that we can in fact connect before proceeding.
		blockUntilConditionMet(
			getValue=lambda: test_remote_server(spyServerURI, log=False),
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
			pathJoin(outDir, "nvdaTestRunLogs", outputFileName)
		)

	def quit_NVDA(self):
		builtIn.log("Stopping nvdaSpy server: {}".format(spyServerURI))
		# remove the spy so that if nvda is run manually against this config it does not interfere.
		self.teardown_nvda_profile()
		process.run_process(
			"pythonw nvda.pyw -q --disable-addons",
			cwd='source',
			shell=True,
		)
		process.wait_for_process(self.nvdaHandle)
		self.save_NVDA_log()

# TODO: this shouldn't be a member function, but it is not available from robot if it is not??
	def assert_strings_are_equal(self, actual, expected, ignore_case=False):
		try:
			builtIn.should_be_equal_as_strings(
				actual,
				expected,
				msg="Actual speech != Expected speech",
				ignore_case=ignore_case
			)
		except AssertionError:
			builtIn.log(
				"repr of actual vs expected (ignore_case={}):\n{}\nvs\n{}".format(
					ignore_case,
					repr(actual),
					repr(expected)
				)
			)
			raise