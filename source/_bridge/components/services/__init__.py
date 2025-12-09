import time
import rpyc
from logHandler import log
import languageHandler
from . import nvwave

class NVDACoreService(rpyc.Service):

	exposed_WavePlayer = nvwave.WavePlayerService

	def exposed_getLanguage(self) -> str:
		return languageHandler.getLanguage()
