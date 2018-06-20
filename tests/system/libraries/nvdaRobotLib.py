import os
from timeit import default_timer as timer
from robotremoteserver import test_remote_server, stop_remote_server
from robot.libraries.BuiltIn import BuiltIn


builtIn = BuiltIn()
process = builtIn.get_library_instance('Process')
opSys = builtIn.get_library_instance('OperatingSystem')

spyServerPort = 8270  # is `registered by IANA` for remote server usage. Two ASCII values:'RF'
spyServerURI = 'http://127.0.0.1:{}'.format(spyServerPort)
spyAlias = "nvdaSpy"

systemTestSpyFileName = "systemTestSpy.py"
systemTestSourceDir = os.path.abspath("tests/system")
nvdaProfileWorkingDir = os.path.join(systemTestSourceDir, "nvdaProfile")
nvdaSettingsSourceDir = os.path.join(systemTestSourceDir, "nvdaSettingsFiles")
systemTestSpySource = os.path.join(systemTestSourceDir, "libraries", systemTestSpyFileName)
systemTestSpyInstallDir = os.path.join(nvdaProfileWorkingDir, "globalPlugins")
systemTestSpyInstalled = os.path.join(systemTestSpyInstallDir, systemTestSpyFileName)

class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None

	def setup_nvda_profile(self, settingsFileName):
		opSys.copy_file(systemTestSpySource, systemTestSpyInstallDir)
		opSys.copy_file(
			os.path.join(nvdaSettingsSourceDir, settingsFileName),
			os.path.join(nvdaProfileWorkingDir, "nvda.ini")
		)

	def teardown_nvda_profile(self):
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

	def _blockUntilReturnsTrue(self, giveUpAfterSeconds, intervalBetweenSeconds, errorMessage, func):
		startTime = timer()
		lastRunTime = startTime - intervalBetweenSeconds+1  # ensure we start trying immediately
		while (timer() - startTime) < giveUpAfterSeconds:
			if (timer() - lastRunTime) > intervalBetweenSeconds:
				lastRunTime = timer()
				if func():
					break
		else:
			raise RuntimeError(errorMessage)

	def _connectToRemoteServer(self):
		"""Connects to the nvdaSpyServer
		Because we do not know how far through the startup NVDA is, we have to poll
		to check that the server is available. Importing the library immediately seems
		to succeed, but then calling a keyword later fails with RuntimeError:
			"Connection to remote server broken: [Errno 10061]
				No connection could be made because the target machine actively refused it"
		Instead we wait until the remote server is available before importing the library and continuing.
		"""

		# Importing the 'Remote' library always succeeds, even when a connection can not be made.
		# If that happens, then some 'Remote' keyword will fail at some later point.
		# therefore we use 'test_remote_server' to ensure that we can in fact connect before proceeding.
		self._blockUntilReturnsTrue(
			giveUpAfterSeconds=10,
			intervalBetweenSeconds=0.1,
			errorMessage="Unable to connect to nvdaSpy",
			func=lambda: test_remote_server(spyServerURI, log=False)
		)

		builtIn.import_library(
			"Remote",  # name of library to import
			# Arguments to construct the library instance:
			"uri={}".format(spyServerURI),
			"timeout=2",  # seconds
			# Set an alias for the imported library instance
			"WITH NAME",
			"nvdaSpy",
		)
		self.nvdaSpy = builtIn.get_library_instance(spyAlias)

	def _runNvdaSpyKeyword(self, keyword, *args, **kwargs):
		if not args: args = []
		if not kwargs: kwargs = {}
		return self.nvdaSpy.run_keyword(keyword, args, kwargs)

	def start_NVDA(self, settingsFileName):
		self.setup_nvda_profile(settingsFileName)
		nvdaProcessHandle = self._startNVDAProcess()
		process.process_should_be_running(nvdaProcessHandle)
		self._connectToRemoteServer()
		self.wait_for_NVDA_startup_to_complete()
		return nvdaProcessHandle

	def wait_for_NVDA_startup_to_complete(self):
		self._blockUntilReturnsTrue(
			giveUpAfterSeconds=10,
			intervalBetweenSeconds=0.1,
			errorMessage="Unable to connect to nvdaSpy",
			func=lambda: self._runNvdaSpyKeyword("is_NVDA_startup_complete")
		)

	def quit_NVDA(self):
		stop_remote_server(spyServerURI, log=False)
		# remove the spy so that if nvda is run manually against this config it does not interfere.
		self.teardown_nvda_profile()
		process.run_process(
			"pythonw nvda.pyw -q --disable-addons",
			cwd='source',
			shell=True,
		)
		process.wait_for_process(self.nvdaHandle)

	def assert_last_speech(self, expectedSpeech):
		actualLastSpeech = self._runNvdaSpyKeyword("get_last_speech")
		builtIn.should_be_equal_as_strings(actualLastSpeech, expectedSpeech)

	def assert_all_speech(self, expectedSpeech):
			actualSpeech = self._runNvdaSpyKeyword("get_all_speech")
			builtIn.should_be_equal_as_strings(
				actualSpeech,
				expectedSpeech,
				msg="Actual speech != to expected speech.",
			)
