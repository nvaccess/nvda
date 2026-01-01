# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import functools
import traceback
import weakref
from typing import (
	ParamSpec,
	Callable,
	cast,
	Self,
)
from collections.abc import Callable
import functools
import threading
import time
import queue
import rpyc
from rpyc.core.stream import PipeStream
from logHandler import log
import secureProcess


"""Base classes for NVDA Bridge components."""

@rpyc.service
class Service(rpyc.Service):
	_terminated: bool = False
	_dependentConnections: list[Connection]
	_dependantServices: list[weakref.ref[Service]]
	_childProcess: secureProcess.SecurePopen | None

	def __init__(self, childProcess: secureProcess.SecurePopen | None = None):
		log.debug(f"Creating Service instance of type {self.__class__.__name__}")
		super().__init__()
		self._childProcess = childProcess
		self._dependentConnections = []
		self._dependantServices = []

	def _createDependentConnection(self, localService: Service, name: str | None=None) -> tuple[int, int]:
		if not name:
			name = f"Dependent service '{localService.__class__.__name__}' of '{self.__class__.__name__}'"
		log.debug(f"Creating dependent connection: {name} on Service {self}, using service {localService} as root")
		if not self._childProcess:
			raise RuntimeError("This service is not associated with a child process.")
		log.debug("Creating pipes for new RPYC stream")
		w_file, r_handle = self._childProcess._createPipe(push=True, duplicateIntoProcess=True)
		r_file, w_handle = self._childProcess._createPipe(push=False, duplicateIntoProcess=True)
		log.debug("Creating PipeStream over new pipes")
		stream = PipeStream(r_file, w_file)
		log.debug("Connecting new RPYC service over PipeStream")
		conn = Connection(stream, localService, name=name)
		self._dependentConnections.append(conn)
		conn.bgEventLoop(daemon=True)
		log.debug(f"Returning new pipe handles: r={r_handle.value}, w={w_handle.value}")
		return r_handle.value, w_handle.value

	@classmethod
	def exposed(cls, func: Callable):
		func = rpyc.exposed(func)
		@functools.wraps(func)
		def f(*args, **kwargs):
			service = args[0] if len(args) > 0 else None
			assert isinstance(service, Service), f"{func.__qualname__} is not a  Service method"
			if service.terminated:
				log.debug(f"Cannot call {func.__qualname__} on terminated service {service}")
				raise RuntimeError(f"Cannot call method {func.__qualname__} on terminated service {service}")
			log.debug(f"Calling {func.__qualname__}")
			try:
				res = func(*args, **kwargs)
			except Exception:
				log.debugWarning(f"Exception in {func.__qualname__}", exc_info=True)
				raise
			log.debug(f"{func.__qualname__} returned {res!r}")
			if isinstance(res, Service):
				log.debug(f"Registering dependant service {res} on parent service {service}")
				service._dependantServices.append(weakref.ref(res))
			return res
		return f

	@property
	def terminated(self) -> bool:
		return self._terminated

	def terminate(self):
		"""Terminate this service and any dependent connections and services."""
		if self._terminated:
			return
		for conn in self._dependentConnections:
			if not conn.closed:
				log.debug(f"Closing dependent connection '{conn.name}' on parent service {self}")
				try:
					conn.close()
				except Exception:
					log.debugWarning("Exception while closing dependent connection", exc_info=True)
		self._dependentConnections.clear()
		for service_ref in self._dependantServices:
			service = service_ref()
			if service and not service.terminated:
				log.debug(f"Terminating dependant service {service} on parent service {self}")
				try:
					service.terminate()
				except Exception:
					log.debugWarning("Exception while terminating dependant service", exc_info=True)
		self._dependantServices.clear()
		self._terminated = True

	def __del__(self):
		log.debug(f"Destroying Service {self}")
		if not self._terminated:
			self.terminate()


class Proxy[Service_t: Service]:
	"""Proxy for wrapping remote rpyc services.
	All NVDA Bridge proxies should inherit from this class.

	This class stores a reference to a remote rpyc service and provides a
	helper method to create a subclass with the remote service bound.

	:ivar _remoteService: The remote rpyc service instance associated with this proxy.
	"""

	_heldConnections: list[Connection]
	_remoteService: Service_t

	def __init__(self, remoteService: Service_t, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._heldConnections = []
		self._remoteService = remoteService

	def holdConnection(self, conn: Connection):
		log.debug(f"Holding Connection '{conn._name}' on Proxy {self}")
		self._heldConnections.append(conn)

	def _connectToDependentServiceOverPipes(self, r_handle: int, w_handle: int, localService: Service | None = None, name: str = "unknown") -> Service:
		log.debug(f"	Connecting to dependent service over pipes: {name} on Proxy {self}")
		stream = PipeStream(r_handle, w_handle)
		newConn = Connection(stream, localService, name=name)
		newConn.bgEventLoop(daemon=True)
		self.holdConnection(newConn)
		return newConn.remoteService

	def __del__(self):
		log.debug(f"Destroying Proxy {self}")
		for conn in self._heldConnections:
			if not conn.closed:
				log.debug(f"Closing held Connection '{conn._name}' on Proxy {self}")
				try:
					conn.close()
				except Exception:
					log.debugWarning("Exception while closing held connection", exc_info=True)


class Connection[LocalService_t: Service | None, RemoteService_t: Service]:

	_closed: bool = False
	_name: str
	_conn: rpyc.Connection | None
	_localService: LocalService_t | None

	def __init__(self, stream, localService: LocalService_t=None, name:str="unknown"):
		self._name = name
		log.debug(f"Creating connection '{name}'")
		self._conn = rpyc.connect_stream(stream, service=localService or rpyc.VoidService, config={'allow_public_attrs': False, 'allow_safe_attrs': False, 'close_catchall': True})
		self._localService = localService

	@property
	def name(self) -> str:
		return self._name

	@property
	def closed(self) -> bool:
		return self._conn is None or self._conn._closed

	def _serve_request(self, timeout: float=0.5) -> bool:
		conn = self._conn
		if not conn or conn._closed:
			return False
		assert isinstance(conn, rpyc.Connection)
		return conn.serve(timeout=timeout)
		return False

	@classmethod
	def _bgEventLoop(cls, connRef: weakref.ref[Connection], name: str):
		log.debug(f"Starting background event loop for Connection '{name}'")
		conn = connRef()
		if conn is None or conn._closed:
			log.debug(f"Connection '{name}' has been garbage collected, exiting event loop")
			return
		rawConn = conn._conn
		if rawConn is None or rawConn._closed:
			log.debug(f"Rpyc Connection '{name}' is closed, exiting event loop")
			return
		try:
			rawConn.serve_all()
		except Exception:
			if not rawConn._closed:
				log.debugWarning(f"Error in event loop for Connection '{name}'", exc_info=True)
		log.debug(f"Exiting event loop for Connection '{name}'")

	def bgEventLoop(self, daemon: bool = False) -> threading.Thread:
		t = threading.Thread(target=self._bgEventLoop, args=(weakref.ref(self), self._name), name=f"Connection Event Loop: {self._name}", daemon=daemon)
		t.start()
		return t

	def eventLoop(self):
		log.debug(f"Starting event loop for Connection '{self._name}'")
		rawConn = self._conn
		if rawConn is None or rawConn._closed:
			log.debug(f"Connection '{self._name}' is closed, exiting event loop")
			return
		try:
			rawConn.serve_all()
		except Exception:
			if not rawConn._closed:
				log.debugWarning(f"Error in event loop for Connection '{self._name}'", exc_info=True)
		log.debug(f"Exiting event loop for Connection '{self._name}'")

	@property
	def remoteService(self) -> RemoteService_t:
		return cast(RemoteService_t, self._conn.root)

	@classmethod
	def _closeRawConnection(cls, conn: rpyc.Connection, name: str):
		log.debug(f"Closing RPYC connection for '{name}'")
		try:
			conn.close()
		except Exception as e:
			if not conn._closed:
				log.debugWarning(f"Exception while closing RPYC connection for '{name}', {e}")
			del e
		log.debug(f"RPYC connection for '{name}' closed")

	def close(self):
		if self._closed:
			return
		if isinstance(self._localService, Service) and not self._localService.terminated:
			log.debug(f"Terminating service {self._localService} on Connection '{self._name}'")
			try:
				self._localService.terminate()
			except Exception:
				log.debugWarning("Exception while terminating local service", exc_info=True)
			self._localService = None
		conn = self._conn
		self._conn = None
		if conn and not conn._closed:
			# Unfortunately if there is an exception when closing the connection,
			# Our Connection object can get stuck in a traceback frame.
			t = threading.Thread(target=self._closeRawConnection, args=(conn, self._name), name=f"Connection Close: {self._name}", daemon=True)
			t.start()
		self._closed = True

	def __del__(self):
		log.debug(f"Destroying Connection '{self._name}'")
		self.close()
