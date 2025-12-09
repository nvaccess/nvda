import threading
import subprocess
import rpyc
from rpyc.core.stream import PipeStream
import secureProcess
from logHandler import log


class NVDAService(rpyc.Service):

	def exposed_LogHandler(self):
		from ..components.services.logHandler import LogHandlerService
		return LogHandlerService()

	def exposed_getLanguage(self):
		import languageHandler
		return languageHandler.getLanguage()

	def exposed_WavePlayer(self, *args, **kwargs):
		from ..components.services.nvwave import WavePlayerService
		return WavePlayerService(*args, **kwargs)


_hostExe = "lib/x86/synthDriverHost-runtime/nvda_synthDriverHost.exe"

def createSynthDriverHost32():
	global stream, conn
	log.info(f"Starting synthDriverHost32 process: {_hostExe}")
	hostProc = secureProcess.SecurePopen([_hostExe], restrictToken=False,integrityLevel=None, killOnDelete=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	log.info("Creating PipeStream over host process std pipes")
	stream = PipeStream(hostProc.stdout, hostProc.stdin)
	log.info("Connecting to synthDriverHost32 process RPYC service over PipeStream")
	conn = rpyc.connect_stream(stream, config={'allow_public_attrs': False, 'allow_safe_attrs': False})
	conn._hostProc = hostProc
	log.info("Starting background thread to service synthDriverHost32 process RPYC requests")
	t = threading.Thread(target=conn.serve_all, daemon=True)
	t.start()
	conn.root.installProxies(NVDAService())
	return conn.root
