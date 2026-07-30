# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""The base class for services exposed across the ART transport."""

from __future__ import annotations

import functools
import weakref
from collections.abc import Callable
from typing import TYPE_CHECKING

import rpyc
from rpyc.core.stream import Stream

from logHandler import log

if TYPE_CHECKING:
	from .connection import Connection


@rpyc.service
class Service(rpyc.Service):
	"""Base class for objects exposed across the ART transport boundary.

	A ``Service`` wraps a real object and exposes a curated set of methods, each decorated with :meth:`exposed`, to the remote peer.
	Concrete subclasses must also be decorated with ``@rpyc.service``.

	A service owns the lifecycle of anything it hands out.
	Dependent connections it opens and dependant services it returns over the boundary are all torn down when it is terminated.
	"""

	_terminated: bool = False

	def __init__(self) -> None:
		super().__init__()
		self._dependentConnections: list[Connection] = []
		self._dependantServices: list[weakref.ref[Service]] = []

	@classmethod
	def exposed[R](cls, func: Callable[..., R]) -> Callable[..., R]:
		"""Expose a method across the boundary.

		Wraps :func:`rpyc.exposed`, additionally refusing calls on a terminated service
		and registering any returned ``Service`` as a dependant so it shares this service's lifetime.
		"""
		exposedFunc = rpyc.exposed(func)

		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			self = args[0] if args else None
			assert isinstance(self, Service), f"{func.__qualname__} is not a Service method"
			if self._terminated:
				raise RuntimeError(f"Cannot call {func.__qualname__} on terminated service {self!r}")
			result = exposedFunc(*args, **kwargs)
			if isinstance(result, Service):
				self._dependantServices.append(weakref.ref(result))
			return result

		return wrapper

	def _addDependentConnection(
		self,
		stream: Stream,
		localService: Service | None = None,
		name: str | None = None,
	) -> Connection:
		"""Open a connection bound to this service's lifetime.

		The connection is closed automatically when this service is terminated.
		Used for side channels such as audio streaming.

		:param stream: Stream over which channel communications will take place.
		:param localService: Service to attach, defaults to ``None``.
		:param name: The name of this dependency, defaults to ``None``.
			If ``None`` is given, a default name will be computed.
		"""
		from .connection import Connection

		if name is None:
			name = f"dependent connection of {type(self).__name__}"
		conn = Connection(stream, localService, name=name)
		self._dependentConnections.append(conn)
		conn.bgEventLoop(daemon=True)
		return conn

	@property
	def terminated(self) -> bool:
		"""Whether this service has been terminated."""
		return self._terminated

	def terminate(self) -> None:
		"""Tear down this service and everything bound to its lifetime."""
		if self._terminated:
			return
		# Set first so in-flight exposed calls are refused while we tear down.
		self._terminated = True
		for conn in self._dependentConnections:
			if not conn.closed:
				try:
					conn.close()
				except Exception:
					log.debugWarning(f"Error closing dependent connection {conn.name!r}", exc_info=True)
		self._dependentConnections.clear()
		for serviceRef in self._dependantServices:
			service = serviceRef()
			if service is not None and not service.terminated:
				try:
					service.terminate()
				except Exception:
					log.debugWarning("Error terminating dependant service", exc_info=True)
		self._dependantServices.clear()

	def __del__(self):
		if not self._terminated:
			self.terminate()
