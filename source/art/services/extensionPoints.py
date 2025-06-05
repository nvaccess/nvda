# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Any, Dict, List, Optional

import Pyro5.api

from logHandler import log


class ExtensionPointProxy:
	"""Proxy for invoking extension point handlers in ART."""
	
	def __init__(self, artManager):
		self.artManager = artManager
		
	def invokeHandlers(
		self, 
		extPointName: str, 
		epType: str, 
		*args, 
		**kwargs
	) -> Any:
		"""Invoke extension point handlers in ART process."""
		handlerService = self.artManager.getService("handlers")
		if not handlerService:
			log.debug("No ART handler service available")
			return self._getDefaultResult(epType)
			
		try:
			return handlerService.executeHandlers(
				extPointName, 
				epType, 
				*args, 
				**kwargs
			)
		except Exception:
			log.exception(f"Error invoking ART handlers for {extPointName}")
			return self._getDefaultResult(epType)
			
	def _getDefaultResult(self, epType: str) -> Any:
		"""Get default result for extension point type."""
		if epType == "action":
			return None
		elif epType in ("decider", "accumulating_decider"):
			return True
		elif epType == "filter":
			return None  # Caller should handle
		elif epType == "chain":
			return []
		return None
