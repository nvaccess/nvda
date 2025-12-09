import rpyc
import logHandler


class LogHandlerService(rpyc.Service):

	def exposed_logMessage(self, level: int, msg: str, exc_info: bool = False, stack_info: bool = False, codepath: str | None = None):
		fullCodepath = "External synthDriverHost"
		if codepath:
			fullCodepath += f": {codepath}"
		logHandler.log._log(level, msg, {}, exc_info=exc_info, stack_info=stack_info, codepath=fullCodepath)

	def exposed_getEffectiveLevel(self):
		return logHandler.log.getEffectiveLevel()
