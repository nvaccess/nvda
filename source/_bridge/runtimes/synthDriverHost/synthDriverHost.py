import types
import logging
import time
import importlib
import rpyc

# Monkeypatch RPYC to force it to use builtins for its exceptions module.
# On Python 3 it normally would, but
# as we have an `exceptions` module in NVDA, it picks that up instead,
# thinking it is the old Python 2 exceptions module.
import builtins
import rpyc.core.vinegar
rpyc.core.vinegar.exceptions_module = builtins

log = logging.getLogger()


class FakeConfDict(dict):
	getConfigValidation = staticmethod(lambda path: types.SimpleNamespace(default='default') if path[0] == 'audio' and path[1] == 'outputDevice' else None)
fakeConf = FakeConfDict()
fakeConf.update({
	'audio': {
		'outputDevice': 'default',
	},
	'speech': {
		'useWASAPIForSAPI4': True,
	},
	'debugLog': {
		'synthDriver': False,
	},
})


class HostService(rpyc.Service):

	def exposed_installProxies(self, remoteService):
		global log
		log.info("Injecting fake config")
		import config
		config.conf = fakeConf
		log.info("Injecting log into logHandler")
		from _bridge.components.proxies.logHandler import LogHandlerProxy
		log = LogHandlerProxy(remoteService.LogHandler())
		import logHandler
		logHandler.log = log
		log.info("Injecting languageHandler.getLanguage")
		import languageHandler
		languageHandler.getLanguage = remoteService.getLanguage
		log.info("Injecting WavePlayerProxy into nvwave module")
		from _bridge.components.proxies.nvwave import WavePlayerProxy
		import nvwave
		nvwave.WavePlayer = WavePlayerProxy._createBoundProxyClass(remoteService.WavePlayer)

	def exposed_registerSynthDriversPath(self, path):
		import synthDrivers
		synthDrivers.__path__.insert(0, path)

	def exposed_SynthDriver(self, name):
		from _bridge.components.services.synthDriver import SynthDriverService
		return SynthDriverService(name)


def main():
	global log
	log.info("Connecting to RPYC server over standard pipes")
	conn = rpyc.connect_stdpipes(HostService, config={'allowpublic_attrs': False, 'allow_safe_attrs': False})
	log.info("Connected to remote service")
	log.info("Entering service loop.")
	conn.serve_all()
