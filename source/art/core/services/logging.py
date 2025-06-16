# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Logging service for ART - receives log messages from add-ons."""

import Pyro5.api
from logHandler import log
from .base import BaseService


@Pyro5.api.expose
class LoggingService(BaseService):
	"""Receives log messages from add-ons running in ART."""
	
	def __init__(self):
		super().__init__("LoggingService")
	
	def logMessage(self, level: int, message: str, addonName: str = ""):
		"""Log a message from an add-on."""
		if addonName:
			message = f"[ART:{addonName}] {message}"
		else:
			message = f"[ART] {message}"
		
		if level <= 10:
			log.debug(message)
		elif level <= 20:
			log.info(message)
		elif level <= 30:
			log.warning(message)
		elif level <= 40:
			log.error(message)
		else:
			log.critical(message)
	
	def logException(self, message: str, tracebackText: str = "", addonName: str = ""):
		"""Log an exception from an add-on."""
		if addonName:
			prefix = f"[ART:{addonName}] "
		else:
			prefix = "[ART] "
		
		full_message = f"{prefix}{message}"
		if tracebackText:
			full_message += f"\n{tracebackText}"
		
		log.error(full_message)
	
	def logDebugWarning(self, message: str, addonName: str = ""):
		"""Log a debug warning from an add-on."""
		if addonName:
			message = f"[ART:{addonName}] {message}"
		else:
			message = f"[ART] {message}"
		
		log.debugWarning(message)
	
	def logIO(self, message: str, addonName: str = ""):
		"""Log an IO message from an add-on."""
		if addonName:
			message = f"[ART:{addonName}] {message}"
		else:
			message = f"[ART] {message}"
		
		log.io(message)
