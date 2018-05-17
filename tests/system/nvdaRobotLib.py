from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.Process import Process
import sendKey

builtIn = BuiltIn()
os = OperatingSystem()
process = Process()

class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None


	def copy_in_system_test_spy(self):
		"""Equiv robot text:
		Copy File  tests/system/systemTestSpy.py  source/globalPlugins/
		"""
		os.copy_file("tests/system/systemTestSpy.py", "source/globalPlugins/")


	def _startNVDAProcess(self):
		"""Equiv robot text:
		Start Process  pythonw nvda.pyw --debug-logging  cwd=source  shell=true  alias=nvdaAlias
		"""
		self.nvdaHandle = handle = process.start_process(
			"pythonw nvda.pyw --debug-logging",
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
		self._connectToRemoteServer()
		self.wait_for_NVDA_startup_to_complete()
		return nvdaProcessHandle


	def wait_for_NVDA_startup_to_complete(self):
		while not self.nvdaSpy.run_keyword("is_NVDA_startup_complete", [], {}):
			builtIn.sleep(0.1)

	def quit_NVDA(self):
		"""send quit NVDA keys
			sleep  1
			send enter key
			nvdaSpy.Stop Remote Server
			Wait For Process  nvdaAlias
		"""
		sendKey.send_quit_NVDA_keys()
		builtIn.sleep(1.0)
		sendKey.send_enter_key()
		self.nvdaSpy.run_keyword("stop_remote_server", [], {})
		return process.wait_for_process(self.nvdaHandle)
