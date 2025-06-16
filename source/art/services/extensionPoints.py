# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Any, Dict, List, Optional, TYPE_CHECKING

import Pyro5.api

from logHandler import log

if TYPE_CHECKING:
	from art.manager import ARTManager


class ExtensionPointProxy:
	"""Proxy for invoking extension point handlers in ART."""
	
	def __init__(self, artManager: "ARTManager") -> None:
		self.artManager = artManager
		
	def invokeHandlers(
		self, 
		extPointName: str, 
		epType: str, 
		*args: Any, 
		**kwargs: Any
	) -> Any:
		"""Invoke extension point handlers in all ART processes."""
		results = []
		default_result = self._getDefaultResult(epType, *args)
		
		# Invoke handlers in all addon processes
		for addon_name, process in self.artManager.addonProcesses.items():
			handlerService = process.getService("handlers")
			if not handlerService:
				log.debug(f"No ART handler service available for addon {addon_name}")
				continue
				
			try:
				result = handlerService.executeHandlers(
					extPointName, 
					epType, 
					*args, 
					**kwargs
				)
				results.append(result)
			except Exception:
				log.exception(f"Error invoking ART handlers for {extPointName} in addon {addon_name}")
				
		# Combine results based on extension point type
		if not results:
			return default_result
			
		return self._combineResults(epType, results, default_result)
			
	def _getDefaultResult(self, epType: str, *args: Any) -> Any:
		"""Get default result for extension point type."""
		if epType == "action":
			return None
		elif epType in ("decider", "accumulating_decider"):
			return True
		elif epType == "filter":
			return args[0] if args else None
		elif epType == "chain":
			return []
		return None
		
	def _combineResults(self, epType: str, results: List[Any], default: Any) -> Any:
		"""Combine results from multiple addon processes based on extension point type."""
		if epType == "action":
			# Actions don't return values
			return None
		elif epType == "decider":
			# All must agree (AND logic)
			return all(results) if results else default
		elif epType == "accumulating_decider":
			# Any can veto (AND logic, but all handlers run)
			return all(results) if results else default
		elif epType == "filter":
			# Chain filters together
			if not results:
				return default
			value = results[0]
			for result in results[1:]:
				if result is not None:
					value = result
			return value
		elif epType == "chain":
			# Concatenate all results
			flattened = []
			for result in results:
				if isinstance(result, list):
					flattened.extend(result)
			return flattened
		return results
