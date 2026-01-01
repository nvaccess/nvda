# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import rpyc
import logHandler


@rpyc.service
class LogHandlerService:
	"""Wraps the local logHandler.log, exposing its methods for remote access.
	When accessed remotely, this service must be wrapped in a `_bridge.components.proxies.logHandler.LogHandlerProxy` which will handle any deserialization and provide the same interface as a local SynthDriver.
	Arguments and return types on the methods here are an internal detail and not thoroughly documented, as they should not be used directly.
	"""

	@rpyc.exposed
	def logMessage(
		self,
		level: int,
		msg: str,
		exc_info: bool = False,
		stack_info: bool = False,
		codepath: str | None = None,
	):
		fullCodepath = "External synthDriverHost"
		if codepath:
			fullCodepath += f": {codepath}"
		logHandler.log._log(level, msg, {}, exc_info=exc_info, stack_info=stack_info, codepath=fullCodepath)

	@rpyc.exposed
	def getEffectiveLevel(self):
		return logHandler.log.getEffectiveLevel()
