# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
rpyc connection wrapper used by the Add-on Runtime transport.
"""

from __future__ import annotations

import threading
import weakref

import rpyc
from rpyc.core.stream import Stream

from logHandler import log

from .config import PROTOCOL_CONFIG
from .service import Service


class Connection[LocalService_t: Service | None, RemoteService_t: Service]:
	"""A single bidirectional rpyc connection over a :class:`Stream`.

	The local service (if any) is exposed to the peer; the peer's root service is reached
	via :attr:`remoteService`. Requests from the peer are handled by a serving loop, run
	either in a background thread (:meth:`bgEventLoop`) or in the calling thread
	(:meth:`eventLoop`).
	"""

	def __init__(
		self,
		stream: Stream,
		localService: LocalService_t = None,
		name: str = "unknown",
	) -> None:
		"""Initializer.

		:param stream: rpyc stream over which NVDA and the add-on will communicate.
		:param localService: The service to expose to the add-on, defaults to ``None``.
		:param name: Name of this connection, defaults to "unknown".
		"""
		self._name = name
		log.debug(f"Creating _art connection {name!r}")
		self._localService = localService
		self._conn: rpyc.Connection | None = rpyc.connect_stream(
			stream,
			service=localService or rpyc.VoidService,
			config=PROTOCOL_CONFIG,
		)

	@property
	def name(self) -> str:
		"""The name of the connection."""
		return self._name

	@property
	def closed(self) -> bool:
		"""Whether this connection is closed."""
		return self._conn is None or self._conn.closed

	@property
	def remoteService(self) -> RemoteService_t:
		"""The service exposed by the add-on.

		:raises RuntimeError: If the connection is closed.
		"""
		if self._conn is None:
			raise RuntimeError(f"Connection {self._name!r} is closed")
		return self._conn.root

	def eventLoop(self) -> None:
		"""Serve peer requests in the calling thread until the connection closes."""
		conn = self._conn
		if conn is None or conn.closed:
			return
		try:
			conn.serve_all()
		except Exception:
			if self._conn is not None and not self._conn.closed:
				log.debugWarning(f"Error in event loop for connection {self._name!r}", exc_info=True)

	def bgEventLoop(self, daemon: bool = False) -> threading.Thread:
		"""Serve peer requests in a background thread."""
		thread = threading.Thread(
			target=self._bgEventLoop,
			args=(weakref.ref(self), self._name),
			name=f"ART connection event loop: {self._name}",
			daemon=daemon,
		)
		thread.start()
		return thread

	@staticmethod
	def _bgEventLoop(connRef: weakref.ref[Connection], name: str) -> None:
		# Hold only a weak reference while waiting for work,
		# so the serving thread never keeps the Connection (and hence the child process) alive on its own.
		conn = connRef()
		rawConn = conn._conn if conn is not None else None
		del conn
		if rawConn is None or rawConn.closed:
			return
		try:
			rawConn.serve_all()
		except Exception:
			if not rawConn.closed:
				log.debugWarning(f"Error in event loop for connection {name!r}", exc_info=True)

	def close(self) -> None:
		"""Close the connection."""
		if self._conn is None:
			return
		if isinstance(self._localService, Service) and not self._localService.terminated:
			try:
				self._localService.terminate()
			except Exception:
				log.debugWarning("Error terminating local service", exc_info=True)
		self._localService = None
		conn = self._conn
		self._conn = None
		if not conn.closed:
			# Closing can raise;
			# do it off-thread so a failure cannot pin this Connection in a traceback frame and leak it (and its child process).
			threading.Thread(
				target=self._closeRawConnection,
				args=(conn, self._name),
				name=f"ART connection close: {self._name}",
				daemon=True,
			).start()

	@staticmethod
	def _closeRawConnection(conn: rpyc.Connection, name: str) -> None:
		try:
			conn.close()
		except Exception:
			if not conn.closed:
				log.debugWarning(f"Error closing connection {name!r}", exc_info=True)

	def __del__(self):
		self.close()
