import inspect
import time
import logging
import logHandler
from ...base import Proxy


class LogHandlerProxy(Proxy, logging.Logger):
	from logging import DEBUG, INFO, WARNING, WARN, ERROR, CRITICAL

	# Our custom levels.
	IO = 12
	DEBUGWARNING = 15
	OFF = 100

	disabled = False

	def __init__(self, remoteService):
		super().__init__(remoteService)
		self._effectiveLevelCache = 0
		self._effectiveLevelCacheTime = 0

	def _log(self, level: int, msg: str, args: dict, exc_info: bool = False, stack_info: bool = False, codepath: str | None = None):
		if not codepath:
			f = inspect.currentframe().f_back.f_back
			codepath = logHandler.getCodePath(f)
		self._remoteService.logMessage(level, msg, exc_info=exc_info, stack_info=stack_info, codepath=codepath)

	def debugWarning(self, msg, *args, **kwargs):
		if not self.isEnabledFor(self.DEBUGWARNING):
			return
		self._log(self.DEBUGWARNING, msg, args, **kwargs)

	def io(self, msg, *args, **kwargs):
		if not self.isEnabledFor(self.IO):
			return
		self._log(self.IO, msg, args, **kwargs)

	def getEffectiveLevel(self):
		curTime = time.time()
		if curTime - self._effectiveLevelCacheTime > 5:
			self._effectiveLevelCacheTime = curTime
			self._effectiveLevelCache = self._remoteService.getEffectiveLevel()
		return self._effectiveLevelCache

	def isEnabledFor(self, level):
		return level >= self.getEffectiveLevel()
