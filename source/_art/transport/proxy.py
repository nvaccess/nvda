# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""The ``Proxy`` base class, which mediates between local NVDA code and the ART."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from rpyc.core.stream import Stream

from .._log import log

if TYPE_CHECKING:
	from .connection import Connection
	from .service import Service


_DEFAULT_DEPENDENT_SERVICE_NAME: Final[str] = "dependent service"


class Proxy[Service_t: Service]:
	"""Base class for the local-side wrapper around a remote :class:`.service.Service`.

	A ``Proxy`` re-presents the remote service through NVDA's normal local interface,
	so consuming code is unaware the implementation lives in another process.
	It may be used as a mixin (e.g. alongside ``SynthDriver``);
	``__init__`` and ``__del__`` cooperate with the rest of the MRO.

	The proxy owns any connections on which it depends and closes them when it is destroyed.
	"""

	def __init__(self, remoteService: Service_t, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self._remoteService = remoteService
		self._heldConnections: list[Connection] = []

	def _holdConnection(self, conn: Connection) -> None:
		"""Keep ``conn`` alive for at least as long as this proxy.

		:param con: Connection to keep alive.
		"""
		self._heldConnections.append(conn)

	def _connectDependentService(
		self,
		stream: Stream,
		localService: Service | None = None,
		name: str = _DEFAULT_DEPENDENT_SERVICE_NAME,
	) -> Service:
		"""Connect to a side-channel service and tie it to this proxy's lifetime.

		:param stream: Stream over which the service will communicate.
		:param localService: The service to attach.
		:param name: Name of this dependency, defaults to :const:`_DEFAULT_DEPENDENT_SERVICE_NAME`.
		"""
		from .connection import Connection

		conn = Connection(stream, localService, name)
		conn.bgEventLoop(daemon=True)
		self._holdConnection(conn)
		return conn.remoteService

	def __del__(self):
		for conn in self._heldConnections:
			if not conn.closed:
				try:
					conn.close()
				except Exception:  # noqa: BLE001
					log.debugWarning(f"Error closing held connection {conn.name!r}", exc_info=True)
		self._heldConnections.clear()
		# As a mixin we may sit above another class with its own __del__; chain to it.
		deleter = getattr(super(), "__del__", None)
		if deleter is not None:
			deleter()
