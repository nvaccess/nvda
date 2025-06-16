# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""GlobalVars service for ART - provides access to globalVars.appArgs."""

import Pyro5.api
import globalVars
from .base import BaseService


@Pyro5.api.expose
class GlobalVarsService(BaseService):
	"""Provides access to NVDA globalVars.appArgs for add-ons running in ART."""
	
	def __init__(self):
		super().__init__("GlobalVarsService")
	
	def getAppArgs(self) -> dict:
		"""Get globalVars.appArgs as a dictionary."""
		try:
			# Convert appArgs to a simple dict for serialization
			return {
				'secure': globalVars.appArgs.secure,
				'configPath': str(globalVars.appArgs.configPath or ""),
				'launcher': globalVars.appArgs.launcher,
				'debugLogging': globalVars.appArgs.debugLogging,
			}
		except Exception:
			self._log_error("getAppArgs")
			return {
				'secure': False,
				'configPath': "",
				'launcher': False,
				'debugLogging': False,
			}
