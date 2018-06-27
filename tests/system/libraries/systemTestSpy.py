import globalPluginHandler
import signal
import threading
from robotremoteserver import RobotRemoteServer
from logHandler import log
whitespaceMinusSlashN = '\t\x0b\x0c\r '

class SystemTestSpy(object):
	def __init__(self):
		self._nvdaStartupComplete = False
		from core import postNvdaStartup
		postNvdaStartup.register(self._onNvdaStartupComplete)
		from speech import preSpeech
		preSpeech.register(self._onNvdaSpeech)
		self._nvdaSpeech = [
			[""],  # initialise with an empty string, this allows for access via [-1]. This is equiv to no speech.
		]
		self._allSpeechStartIndex = 0
		self._speechOccurred = False

	def _onNvdaStartupComplete(self):
		self._nvdaStartupComplete = True
		self.reset_all_speech_index()

	def _onNvdaSpeech(self, speechSequence=None):
		if not speechSequence: return
		self._speechOccurred = True
		self._nvdaSpeech.append(speechSequence)

	def _getJoinedBaseStringsFromCommands(self, speechCommandArray):
		wsChars = whitespaceMinusSlashN
		baseStrings = [c.strip(wsChars) for c in speechCommandArray if isinstance(c, basestring)]
		return ''.join(baseStrings).strip()

	# Start of Robot library API

	def is_NVDA_startup_complete(self):
		return self._nvdaStartupComplete

	def has_speech_occurred_since_last_check(self):
		speechOccurred = self._speechOccurred
		self._speechOccurred = False
		return speechOccurred

	def get_last_speech(self):
		return self._getJoinedBaseStringsFromCommands(self._nvdaSpeech[-1])

	def get_all_speech(self):
		return self.get_speech_since_index(self._allSpeechStartIndex)

	def _flattenCommandsSeparatingWithNewline(self, commandArray):
		f = [c for commands in commandArray for newlineJoined in [commands, [u"\n"]] for c in newlineJoined]
		log.debug("f: {}".format(repr(f)))
		return f

	def get_speech_since_index(self, speechIndex):
		speechCommands = self._flattenCommandsSeparatingWithNewline(
			self._nvdaSpeech[speechIndex:]
		)
		joined = self._getJoinedBaseStringsFromCommands(speechCommands)
		log.debug("joined: {}".format(joined))
		return joined

	def get_speech_index(self):
		return len(self._nvdaSpeech) - 1

	def reset_all_speech_index(self):
		self._allSpeechStartIndex = self.get_speech_index()

	def get_index_of_speech(self, speech, indexHint=0):
		log.debug("indexHint is: {}, speech is: {}".format(indexHint, speech))
		for index, commands in enumerate(self._nvdaSpeech[indexHint:]):
			index = index+indexHint
			baseStrings = [c.strip() for c in commands if isinstance(c, basestring)]
			log.debug("baseStrings: \n{}".format(repr(baseStrings)))
			if speech in baseStrings:
				log.debug("at index: {}, Found: {}".format(index, speech))
				return index
		return -1



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