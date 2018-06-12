import sys
import os
from robot.libraries.BuiltIn import BuiltIn
import sendKey

builtIn = BuiltIn()
process = builtIn.get_library_instance('Process')

nvdaProfileDir=os.path.abspath("tests/system/nvdaProfile")

class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None


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
		"""send quit NVDA keys"""
		process.run_process(
			"pythonw nvda.pyw -q",
			cwd='source',
			shell=True,
		)
		process.wait_for_process(self.nvdaHandle)
