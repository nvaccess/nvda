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
		builtIn.import_library(
				"Remote",
				'http://127.0.0.1:8270',
				"WITH NAME",
				"nvdaSpy"
			)
		self.nvdaSpy = builtIn.get_library_instance("nvdaSpy")


	def start_NVDA(self):
		self.copy_in_system_test_spy()
		nvdaProcessHandle = self._startNVDAProcess()
		process.process_should_be_running(nvdaProcessHandle)
		builtIn.sleep(4.0)
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
