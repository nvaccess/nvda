import os
from os.path import join as pathJoin
from os.path import abspath
from timeit import default_timer as timer
from robotremoteserver import test_remote_server, stop_remote_server
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

systemTestSpyFileName = "systemTestSpy.py"
systemTestSpySource = pathJoin(systemTestSourceDir, "libraries", systemTestSpyFileName)
systemTestSpyInstallDir = pathJoin(nvdaProfileWorkingDir, "globalPlugins")
systemTestSpyInstalled = pathJoin(systemTestSpyInstallDir, systemTestSpyFileName)

class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None

	def setup_nvda_profile(self, settingsFileName):
		opSys.create_directory(systemTestSpyInstallDir)
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

	def _blockUntilReturnsTrue(self, func, giveUpAfterSeconds, intervalBetweenSeconds=0.1, errorMessage=None):
		"""Call 'func' every 'intervalBetweenSeconds' seconds until 'func' returns True until
		'giveUpAfterSeconds' is reached.
		If 'func' does not return true and 'errorMessage' is provided, a RuntimeError is raised
		using the provided errorMessage.
		@return True if 'func' returns True before 'giveUpAfterSeconds' is reached, else False
		"""
		startTime = timer()
		lastRunTime = startTime - intervalBetweenSeconds+1  # ensure we start trying immediately
		while (timer() - startTime) < giveUpAfterSeconds:
			if (timer() - lastRunTime) > intervalBetweenSeconds:
				lastRunTime = timer()
				if func():
					return True
		else:
			if errorMessage:
				raise RuntimeError(errorMessage)
			return False

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
			func=lambda: test_remote_server(spyServerURI, log=False),
			giveUpAfterSeconds=10,
			errorMessage="Unable to connect to nvdaSpy",
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
			func=lambda: self._runNvdaSpyKeyword("is_NVDA_startup_complete"),
			giveUpAfterSeconds=10,
			errorMessage="Unable to connect to nvdaSpy",
		)

	def save_NVDA_log(self):
		"""NVDA logs are saved to the ${OUTPUT DIR}/nvdaTestRunLogs/${SUITE NAME}-${TEST NAME}-nvda.log"""
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
		stop_remote_server(spyServerURI, log=False)
		# remove the spy so that if nvda is run manually against this config it does not interfere.
		self.teardown_nvda_profile()
		process.run_process(
			"pythonw nvda.pyw -q --disable-addons",
			cwd='source',
			shell=True,
		)
		process.wait_for_process(self.nvdaHandle)
		self.save_NVDA_log()

	def assert_last_speech(self, expectedSpeech):
		actualLastSpeech = self._runNvdaSpyKeyword("get_last_speech")
		builtIn.should_be_equal_as_strings(
			actualLastSpeech,
			expectedSpeech,
			msg="Actual speech != Expected speech"
		)

	def assert_all_speech(self, expectedSpeech):
		actualSpeech = self._runNvdaSpyKeyword("get_all_speech")
		builtIn.should_be_equal_as_strings(
			actualSpeech,
			expectedSpeech,
			msg="Actual speech != Expected speech",
		)

	def assert_speech_since_index(self, index, expectedSpeech):
		actualSpeech = self._runNvdaSpyKeyword("get_speech_since_index", index)
		builtIn.should_be_equal_as_strings(
			actualSpeech,
			expectedSpeech,
			msg="Actual speech != Expected speech",
		)

	def wait_for_next_speech(self, maxWaitSeconds=5, raiseErrorOnTimeout=True):
		return self._blockUntilReturnsTrue(
			func=lambda: self._runNvdaSpyKeyword("has_speech_occurred_since_last_check"),
			giveUpAfterSeconds=maxWaitSeconds,
			errorMessage="Speech did not start before timeout" if raiseErrorOnTimeout else None
		)

	def has_speech_finished(self):
		speechOccurred = self.wait_for_next_speech(maxWaitSeconds=2, raiseErrorOnTimeout=False)
		return not speechOccurred

	def wait_for_speech_to_finish(self, maxWaitSeconds=5):
		self._blockUntilReturnsTrue(
			func=self.has_speech_finished,
			giveUpAfterSeconds=maxWaitSeconds,
			errorMessage="Speech did not finish before timeout"
		)

	def wait_for_speech_to_start_and_finish(self):
		self.wait_for_next_speech()
		self.wait_for_speech_to_finish()

	def reset_get_all_speech(self):
		self._runNvdaSpyKeyword("reset_all_speech_index")

	def wait_for_specific_speech(self, speech, sinceIndex=None, maxWaitSeconds=5):
		sinceIndex = 0 if not sinceIndex else sinceIndex
		def trueIfSpeechIndex():
			index = self._runNvdaSpyKeyword("get_index_of_speech", speech, sinceIndex)
			builtIn.log_to_console("value of index: ".format(index))
			return index > 0

		self._blockUntilReturnsTrue(
			func=trueIfSpeechIndex,
			giveUpAfterSeconds=maxWaitSeconds,
			errorMessage="Specific speech did not occur before timeout: {}".format(speech)
		)

	def wait_for_specific_speech_after_action(self, speech, action, *args):
		self.wait_for_speech_to_finish()
		index = self._runNvdaSpyKeyword("get_speech_index")
		builtIn.run_keyword(action, *args)
		self.wait_for_specific_speech(speech, index)
		return self._runNvdaSpyKeyword("get_index_of_speech", speech, index)

	def wait_for_any_speech_after_action(self, action, *args):
		self.wait_for_speech_to_finish()
		builtIn.run_keyword(action, *args)
		self.wait_for_next_speech()