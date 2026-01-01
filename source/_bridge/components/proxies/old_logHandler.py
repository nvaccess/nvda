# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import typing
import inspect
import traceback
import time
import logHandler
from ...base import Proxy

if typing.TYPE_CHECKING:
	from ..services.logHandler import LogHandlerService


class LogHandlerProxy(Proxy, logHandler.Logger):
	"""Wraps a remote LogHandlerService, providing the same interface as the local logHandler.log."""

	_remoteService: LogHandlerService
	disabled = False

	def __init__(self, remoteService):
		super().__init__(remoteService)
		self._effectiveLevelCache = 0
		self._effectiveLevelCacheTime = 0

	def _log(
		self,
		level,
		msg,
		args,
		exc_info=None,
		extra=None,
		codepath=None,
		activateLogViewer=False,
		stack_info=None,
	):
		if not codepath or stack_info:
			frame = inspect.currentframe()
			count = 2
			while count > 0 and frame:
				parentFrame = frame.f_back
				if not parentFrame:
					break
				frame = parentFrame
				count -= 1
			if not codepath:
				codepath = logHandler.getCodePath(frame)
			if stack_info is True:
				stack_info = traceback.extract_stack(frame)
				msg += "\nStack trace:\n" + ("".join(traceback.format_list(stack_info)).rstrip())
		self._remoteService.logMessage(
			level,
			msg,
			exc_info=bool(exc_info),
			stack_info=bool(stack_info),
			codepath=codepath,
		)

	def getEffectiveLevel(self):
		curTime = time.time()
		if curTime - self._effectiveLevelCacheTime > 5:
			self._effectiveLevelCacheTime = curTime
			self._effectiveLevelCache = self._remoteService.getEffectiveLevel()
		return self._effectiveLevelCache

	def isEnabledFor(self, level):
		return level >= self.getEffectiveLevel()
