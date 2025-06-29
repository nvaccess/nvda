# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""LogHandler module proxy for add-ons running in ART."""

import traceback
from .base import ServiceProxyMixin


_addonName = ""


def setAddonName(name: str):
	"""Set the add-on name for logging context.
	This should be called when an add-on is loaded.
	"""
	global _addonName
	_addonName = name


class LogProxy(ServiceProxyMixin):
	"""Proxy for log that forwards to LoggingService."""

	_service_env_var = "NVDA_ART_LOGGING_SERVICE_URI"

	DEBUG = 10
	INFO = 20
	WARNING = 30
	WARN = WARNING
	ERROR = 40
	CRITICAL = 50

	IO = 12
	DEBUGWARNING = 15
	OFF = 100

	def debug(self, message: str):
		"""Log a debug message."""
		self._call_service("logMessage", self.DEBUG, str(message), _addonName)

	def info(self, message: str):
		"""Log an info message."""
		self._call_service("logMessage", self.INFO, str(message), _addonName)

	def warning(self, message: str):
		"""Log a warning message."""
		self._call_service("logMessage", self.WARNING, str(message), _addonName)

	def warn(self, message: str):
		"""Alias for warning."""
		self.warning(message)

	def error(self, message: str, exc_info=False):
		"""Log an error message."""
		if exc_info:
			# Include traceback in message
			tb = traceback.format_exc()
			message = f"{message}\n{tb}"
		self._call_service("logMessage", self.ERROR, str(message), _addonName)

	def critical(self, message: str):
		"""Log a critical message."""
		self._call_service("logMessage", self.CRITICAL, str(message), _addonName)

	def exception(self, message: str = "", exc_info=True):
		"""Log an exception with traceback."""
		# Get the traceback
		if exc_info is True:
			tb = traceback.format_exc()
		elif exc_info:
			tb = "".join(traceback.format_exception(*exc_info))
		else:
			tb = ""

		self._call_service("logException", str(message), tb, _addonName)

	def debugWarning(self, message: str, exc_info=False):
		"""Log a debug warning (NVDA custom level)."""
		if exc_info:
			# Include traceback in message
			tb = traceback.format_exc()
			message = f"{message}\n{tb}"
		self._call_service("logDebugWarning", str(message), _addonName)

	def io(self, message: str):
		"""Log an IO message (NVDA custom level)."""
		self._call_service("logIO", str(message), _addonName)


# Create the main log object
log = LogProxy()
