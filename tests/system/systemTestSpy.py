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
		self._nvdaSpeech = [
			[""],  # initialise with an empty string, this allows for access via [-1]. This is equiv to no speech.
		]

	def _onNvdaStartupComplete(self):
		self._nvdaStartupComplete = True

	def _onNvdaSpeech(self, speechSequence=None):
		if not speechSequence: return
		self._nvdaSpeech.append(speechSequence)

	def is_NVDA_startup_complete(self):
		log.debug("Got startup complete action")
		return self._nvdaStartupComplete

	def get_last_speech(self):
		baseStrings = [s.strip() for s in self._nvdaSpeech[-1] if isinstance(s, basestring)]
		lastSpeech = ' '.join(baseStrings)
		log.debug("last speech: {}".format(lastSpeech))
		return lastSpeech


class SystemTestSpyServer(object):
	def __init__(self):
		self._server = None

	def start(self):
		log.debug("TestSpyPlugin started")
		server = self._server = RobotRemoteServer(
			SystemTestSpy(),  # provides actual spy behaviour
			port=8270,  # Could use 0 for auto port selection, which can be written out to a file / command line
			serve=False  # we want to start this serving on another thread so as not to block.
		)
		log.debug("Server address: {}".format(server.server_address))
		signal.signal(signal.SIGINT, lambda signum, frame: server.stop())
		server_thread = threading.Thread(target=server.serve)
		server_thread.start()

	def stop(self):
		self._server.stop()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self._testSpy = SystemTestSpyServer()
		self._testSpy.start()

	__gestures = {
	}