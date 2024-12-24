from logging import getLogger
from typing import Any, Callable, Dict, List
from collections import defaultdict

import wx

logger = getLogger("callback_manager")


class CallbackManager:
	"""A simple way of associating multiple callbacks to events and calling them all when that event happens"""

	def __init__(self) -> None:
		self.callbacks: Dict[str, List[Callable[..., Any]]] = defaultdict(list)

	def registerCallback(self, event_type: str, callback: Callable[..., Any]) -> None:
		"""Registers a callback as a callable to an event type, which can be anything hashable"""
		self.callbacks[event_type].append(callback)

	def unregisterCallback(self, event_type: str, callback: Callable[..., Any]) -> None:
		"""Unregisters a callback from an event type"""
		self.callbacks[event_type].remove(callback)

	def callCallbacks(self, type: str, *args: Any, **kwargs: Any) -> None:
		"""Calls all callbacks for a given event type with the provided args and kwargs"""
		for callback in self.callbacks[type]:
			try:
				wx.CallAfter(callback, *args, **kwargs)
			except Exception:
				logger.exception("Error calling callback %r" % callback)
		for callback in self.callbacks["*"]:
			try:
				wx.CallAfter(callback, type, *args, **kwargs)
			except Exception:
				logger.exception("Error calling callback %r" % callback)
