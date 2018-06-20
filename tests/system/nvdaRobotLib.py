import os
import sys
from timeit import default_timer as timer

from robot.libraries.BuiltIn import BuiltIn
builtIn = BuiltIn()
process = builtIn.get_library_instance('Process')
opSys = builtIn.get_library_instance('OperatingSystem')

systemTestSpyFileName = "systemTestSpy.py"
systemTestSourceDir = os.path.abspath("tests/system")
nvdaProfileDir = os.path.join(systemTestSourceDir, "nvdaProfile")
systemTestSpySource = os.path.join(systemTestSourceDir, systemTestSpyFileName)
systemTestSpyInstallDir = os.path.join(nvdaProfileDir, "globalPlugins")
systemTestSpyInstalled = os.path.join(systemTestSpyInstallDir, systemTestSpyFileName)

class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None

	def copy_in_system_test_spy(self):
		"""Equiv robot text:
		Copy File  tests/system/systemTestSpy.py  {nvdaProfile}/globalPlugins/
		"""
		opSys.copy_file(systemTestSpySource, systemTestSpyInstallDir)

	def remove_system_test_spy(self):
		opSys.remove_file(systemTestSpyInstalled)

	def _startNVDAProcess(self):
		"""Equiv robot text:
		Start Process  pythonw nvda.pyw --debug-logging  cwd=source  shell=true  alias=nvdaAlias
		"""
		self.nvdaHandle = handle = process.start_process(
			"pythonw nvda.pyw --debug-logging -r -c \"{nvdaProfileDir}\"".format(nvdaProfileDir=nvdaProfileDir),
			cwd='source',
			shell=True,
			alias='nvdaAlias'
		)
		return handle

	def _connectToRemoteServer(self):
		"""Equiv robot text:
		Import Library  Remote         WITH NAME    nvdaSpy
		"""
		port = 8270  # default:8270 is `registered by IANA` for remote server usage. Two ASCII values, RF.
		uri = 'http://127.0.0.1:{}'.format(port)
		spyAlias = "nvdaSpy"

		startTime = timer()
		giveUpAfter = 10  # seconds
		intervalBetweenTries = 0.1  # seconds
		lastRunTime = startTime - intervalBetweenTries+1  # ensure we start trying immediately
		canConnect=False
		from robotremoteserver import test_remote_server
		while not canConnect and (timer() - startTime) < giveUpAfter:
			if (timer() - lastRunTime) > intervalBetweenTries:
				lastRunTime = timer()

				# Importing the 'Remote' library always succeeds, even when a connection can not be made.
				# If that happens, then some 'Remote' keyword will fail at some later point.
				# therefore we use 'test_remote_server' to ensure that we can in fact connect before proceeding.
				canConnect = test_remote_server(uri)

		if not canConnect:
			raise RuntimeError("Unable to connect to nvdaSpy")
		else:
			builtIn.import_library(
				"Remote",  # name of library to import
				# Arguments to construct the library instance:
				"uri={}".format(uri),
				"timeout=2",  # seconds
				# Set an alias for the imported library instance
				"WITH NAME",
				"nvdaSpy",
			)
			self.nvdaSpy = builtIn.get_library_instance(spyAlias)

	def start_NVDA(self):
		self.copy_in_system_test_spy()
		nvdaProcessHandle = self._startNVDAProcess()
		process.process_should_be_running(nvdaProcessHandle)
		self._connectToRemoteServer()
		self.wait_for_NVDA_startup_to_complete()
		return nvdaProcessHandle

	def wait_for_NVDA_startup_to_complete(self):
		while not self.nvdaSpy.run_keyword("is_NVDA_startup_complete", [], {}):
			builtIn.sleep(0.1)


	def quit_NVDA(self):
		try:
			self.nvdaSpy.run_keyword("stop_remote_server", [], {})
		except RuntimeError:
			pass  # if the test manually exits, then we are unable to run this keyword.
		self.remove_system_test_spy()
		process.run_process(
			"pythonw nvda.pyw -q --disable-addons",
			cwd='source',
			shell=True,
		)
		process.wait_for_process(self.nvdaHandle)

	def assert_last_speech(self, expectedSpeech):
		actualLastSpeech = self.nvdaSpy.run_keyword("get_last_speech", [], {})
		builtIn.should_be_equal_as_strings(actualLastSpeech, expectedSpeech)
