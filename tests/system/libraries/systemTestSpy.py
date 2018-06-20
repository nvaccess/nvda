import globalPluginHandler
import signal
import threading
from robotremoteserver import RobotRemoteServer
from logHandler import log

class SystemTestSpy:
	def __init__(self):
		self._nvdaStartupComplete = False
		from core import postNvdaStartup
		from speech import preSpeech
		postNvdaStartup.register(self._onNvdaStartupComplete)
		preSpeech.register(self._onNvdaSpeech)
		self.clear_speech_cache()  # set self._nvdaSpeech

	def _onNvdaStartupComplete(self):
		self._nvdaStartupComplete = True
		self.clear_speech_cache()

	def _onNvdaSpeech(self, speechSequence=None):
		if not speechSequence: return
		self._nvdaSpeech.append(speechSequence)

	def is_NVDA_startup_complete(self):
		return self._nvdaStartupComplete

	def _getJoinedBaseStringsFromCommands(self, speechCommandArray):
		baseStrings = [c.strip() for c in speechCommandArray if isinstance(c, basestring)]
		return ' '.join(baseStrings).replace("  ", "\n").strip()

	def get_last_speech(self):
		return self._getJoinedBaseStringsFromCommands(self._nvdaSpeech[-1])

	def get_all_speech(self):
		speechCommands = [c for commands in self._nvdaSpeech for c in commands]
		return self._getJoinedBaseStringsFromCommands(speechCommands)

	def clear_speech_cache(self):
		self._nvdaSpeech = [
			[""],  # initialise with an empty string, this allows for access via [-1]. This is equiv to no speech.
		]


class SystemTestSpyServer(object):
	def __init__(self):
		self._server = None

	def start(self):
		log.debug("TestSpyPlugin started")
		server = self._server = RobotRemoteServer(
			SystemTestSpy(),  # provides actual spy behaviour
			port=8270,  # default:8270 is `registered by IANA` for remote server usage. Two ASCII values, RF.
			serve=False  # we want to start this serving on another thread so as not to block.
		)
		log.debug("Server address: {}".format(server.server_address))
		server_thread = threading.Thread(target=server.serve)
		server_thread.start()

	def stop(self):
		self._server.stop()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self._testSpy = SystemTestSpyServer()
		self._testSpy.start()

	def terminate(self):
		log.debug("Terminating the systemTestSpy")
		self._testSpy.stop()

	__gestures = {
	}