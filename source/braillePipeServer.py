# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Pneuma Solutions
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Named-pipe IPC server that exposes the Braille Mirror and Direct Braille Window APIs to external processes.

Two pipe names are used:

* ``\\\\.\\pipe\\screen_reader_braille``        – normal desktop instance
* ``\\\\.\\pipe\\screen_reader_braille_secure`` – secure desktop instance

Wire protocol:
Every message is length-prefixed: 4 bytes little-endian uint32 body length, followed by a UTF-8 JSON object.

One connection handles one role (mirror or direct braille).
"""

import ctypes
import ctypes.wintypes
import json
import queue
import struct
import threading

import wx

import braille
from logHandler import log
from utils.security import isRunningOnSecureDesktop
from winBindings import advapi32 as _advapi32
from winBindings import kernel32 as _kernel32
from winBindings.advapi32 import SECURITY_ATTRIBUTES

INVALID_HANDLE_VALUE = ctypes.wintypes.HANDLE(-1).value
ERROR_PIPE_CONNECTED = 535
ERROR_BROKEN_PIPE = 109
ERROR_IO_PENDING = 997
PIPE_ACCESS_DUPLEX = 0x00000003
PIPE_TYPE_BYTE = 0x00000000
PIPE_READMODE_BYTE = 0x00000000
PIPE_WAIT = 0x00000000
PIPE_UNLIMITED_INSTANCES = 255
NMPWAIT_USE_DEFAULT_WAIT = 0
FILE_FLAG_OVERLAPPED = 0x40000000

SDDL_REVISION_1 = 1

# SDDL for the normal-desktop pipe.
# The normal-desktop NVDA instance runs as the logged-in user.  Its default token DACL grants that user and local Administrators access, but does NOT reliably include NT AUTHORITY\SYSTEM, which is the identity used by RIM's elevated service component.
_NORMAL_PIPE_SDDL = "D:(A;;GA;;;OW)(A;;GRGW;;;SY)"


def _buildSystemAccessSA() -> tuple[SECURITY_ATTRIBUTES, ctypes.c_void_p]:
	"""Build a SECURITY_ATTRIBUTES granting SYSTEM read/write on the normal-desktop pipe.

	Returns ``(sa, sd)`` where *sd* is the LocalAlloc'd security descriptor that must be freed with ``_kernel32.LocalFree(sd)`` when the pipe server stops.
	"""
	sd = ctypes.c_void_p()
	ok = _advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW(
		_NORMAL_PIPE_SDDL,
		SDDL_REVISION_1,
		ctypes.byref(sd),
		None,
	)
	if not ok:
		raise ctypes.WinError()
	sa = SECURITY_ATTRIBUTES(nLength=ctypes.sizeof(SECURITY_ATTRIBUTES), lpSecurityDescriptor=sd)
	return sa, sd


def _createPipeInstance(
	name: str,
	sa: SECURITY_ATTRIBUTES | None = None,
) -> ctypes.wintypes.HANDLE:
	"""Create a single named-pipe instance and return its handle."""
	handle = _kernel32.CreateNamedPipe(
		name,
		PIPE_ACCESS_DUPLEX,
		PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,
		PIPE_UNLIMITED_INSTANCES,
		65536,
		65536,
		NMPWAIT_USE_DEFAULT_WAIT,
		ctypes.byref(sa) if sa is not None else None,
	)
	if handle == INVALID_HANDLE_VALUE:
		raise ctypes.WinError()
	return handle


def _connectClient(handle: ctypes.wintypes.HANDLE) -> bool:
	"""Block until a client connects.  Return False if the pipe is broken."""
	result = _kernel32.ConnectNamedPipe(handle, None)
	if result:
		return True
	err = ctypes.GetLastError()
	if err == ERROR_PIPE_CONNECTED:
		return True
	return False


def _readExact(handle: ctypes.wintypes.HANDLE, n: int) -> bytes | None:
	"""Read exactly *n* bytes from *handle*.  Return None on pipe break."""
	buf = (ctypes.c_char * n)()
	total = 0
	while total < n:
		read = ctypes.wintypes.DWORD(0)
		ok = _kernel32.ReadFile(handle, ctypes.byref(buf, total), n - total, ctypes.byref(read), None)
		if not ok or read.value == 0:
			return None
		total += read.value
	return bytes(buf)


def _writeAll(handle: ctypes.wintypes.HANDLE, data: bytes) -> bool:
	"""Write all of *data* to *handle*.  Return False on pipe break."""
	offset = 0
	while offset < len(data):
		written = ctypes.wintypes.DWORD(0)
		ok = _kernel32.WriteFile(
			handle,
			ctypes.c_char_p(data[offset:]),
			len(data) - offset,
			ctypes.byref(written),
			None,
		)
		if not ok or written.value == 0:
			return False
		offset += written.value
	return True


def _frameMessage(obj: dict) -> bytes:
	body = json.dumps(obj).encode("utf-8")
	return struct.pack("<I", len(body)) + body


def _sendMessage(handle: ctypes.wintypes.HANDLE, obj: dict) -> bool:
	return _writeAll(handle, _frameMessage(obj))


def _recvMessage(handle: ctypes.wintypes.HANDLE) -> dict | None:
	header = _readExact(handle, 4)
	if header is None:
		return None
	(length,) = struct.unpack("<I", header)
	body = _readExact(handle, length)
	if body is None:
		return None
	try:
		return json.loads(body.decode("utf-8"))
	except json.JSONDecodeError:
		log.warning("braillePipeServer: malformed JSON from client")
		return None


class _PipeBrailleGesture(braille.BrailleDisplayGesture):
	"""A synthetic BrailleDisplayGesture constructed from wire data."""

	def __init__(self, source: str, model: str, id_: str, routingIndex, dots: int, space: bool) -> None:
		super().__init__()
		self._source = source
		self._model = model or None
		self._id = id_
		self.routingIndex = routingIndex
		self.dots = dots
		self.space = space

	def _get_source(self) -> str:
		return self._source

	def _get_model(self) -> str:
		return self._model

	def _get_id(self) -> str:
		return self._id


class _AsyncWriter:
	"""Background writer thread that drains a queue to a pipe handle.

	All sends from NVDA's main-thread callbacks (display updates, gesture
	notifications) go through here so pipe I/O never blocks the core loop.
	Sending ``None`` to the queue is the stop sentinel.
	"""

	def __init__(self, handle: ctypes.wintypes.HANDLE) -> None:
		self._handle = handle
		self._queue: queue.SimpleQueue = queue.SimpleQueue()
		self._thread = threading.Thread(target=self._loop, daemon=True, name="braillePipeWriter")
		self._thread.start()

	def send(self, obj: dict) -> None:
		"""Enqueue *obj* for asynchronous delivery to the pipe client."""
		self._queue.put(_frameMessage(obj))

	def stop(self) -> None:
		"""Signal the writer thread to stop after draining remaining items."""
		self._queue.put(None)

	def _loop(self) -> None:
		while True:
			frame = self._queue.get()
			if frame is None:
				break
			if not _writeAll(self._handle, frame):
				break


class _MirrorSession(braille.BrailleMirror):
	"""BrailleMirror that forwards display updates over the pipe."""

	def __init__(self, handle: ctypes.wintypes.HANDLE, numCells: int) -> None:
		self._numCells = numCells
		self._writer = _AsyncWriter(handle)
		braille.registerMirror(self)
		braille.displaySizeChanged.register(self._handleDisplaySizeChanged)
		if braille.handler:
			self._writer.send({"type": "display_size", "numCols": braille.handler.displayDimensions.numCols})

	def numCells(self) -> int:
		return self._numCells

	def display(self, cells: list) -> None:
		self._writer.send({"type": "display", "cells": cells})

	def _handleDisplaySizeChanged(self, displaySize: int, numRows: int, numCols: int) -> None:
		self._writer.send({"type": "display_size", "numCols": numCols})

	def handleMessage(self, msg: dict) -> None:
		mtype = msg.get("type")
		if mtype == "inject_gesture":
			gesture = _PipeBrailleGesture(
				source=msg.get("source", ""),
				model=msg.get("model", ""),
				id_=msg.get("id", ""),
				routingIndex=msg.get("routingIndex"),
				dots=msg.get("dots", 0),
				space=msg.get("space", False),
			)
			wx.CallAfter(braille.injectGesture, gesture)
		else:
			log.debug(f"braillePipeServer: unexpected mirror message type {mtype!r}")

	def close(self) -> None:
		braille.displaySizeChanged.unregister(self._handleDisplaySizeChanged)
		braille.unregisterMirror(self)
		self._writer.stop()


class _DirectSession(braille.DirectBrailleWindow):
	"""DirectBrailleWindow that forwards gestures over the pipe."""

	def __init__(self, handle: ctypes.wintypes.HANDLE, hwnd: int, numCells: int) -> None:
		super().__init__(hwnd=hwnd, numCells=numCells)
		self._writer = _AsyncWriter(handle)
		self.activate()

	def onGesture(self, gesture: braille.BrailleDisplayGesture) -> None:
		self._writer.send(
			{
				"type": "gesture",
				"source": getattr(gesture, "source", ""),
				"model": getattr(gesture, "model", "") or "",
				"id": getattr(gesture, "id", ""),
				"routingIndex": getattr(gesture, "routingIndex", None),
				"dots": getattr(gesture, "dots", 0),
				"space": getattr(gesture, "space", False),
			},
		)

	def handleMessage(self, msg: dict) -> None:
		mtype = msg.get("type")
		if mtype == "display":
			cells = msg.get("cells", [])
			self.display(cells)
		else:
			log.debug(f"braillePipeServer: unexpected direct message type {mtype!r}")

	def close(self) -> None:
		self.deactivate()
		self._writer.stop()


def _handleConnection(handle: ctypes.wintypes.HANDLE, pending_q: "queue.Queue") -> None:
	"""Thread that drives one client connection from registration to close."""
	session = None
	try:
		# First message must be a registration.
		msg = _recvMessage(handle)
		if msg is None:
			return
		mtype = msg.get("type")
		if mtype == "register_mirror":
			numCells = int(msg.get("numCells", 0))
			# If braille is not yet initialised, queue registration.
			if braille.handler is None:
				pending_q.put(("mirror", handle, numCells))
				return
			session = _MirrorSession(handle, numCells)
		elif mtype == "register_direct_braille":
			hwnd = int(msg.get("hwnd", 0))
			numCells = int(msg.get("numCells", 0))
			if braille.handler is None:
				pending_q.put(("direct", handle, hwnd, numCells))
				return
			session = _DirectSession(handle, hwnd, numCells)
		else:
			log.warning(f"braillePipeServer: unexpected first message type {mtype!r}")
			return
		while True:
			msg = _recvMessage(handle)
			if msg is None:
				break
			session.handleMessage(msg)
	except Exception:
		log.exception("braillePipeServer: error in connection handler")
	finally:
		if session is not None:
			session.close()
		_kernel32.CloseHandle(handle)


class _PipeServer:
	"""Listens on a named pipe and spawns per-connection threads."""

	def __init__(self, pipeName: str, useSystemDacl: bool = False) -> None:
		self._pipeName = pipeName
		self._useSystemDacl = useSystemDacl
		self._stop = threading.Event()
		self._thread: threading.Thread | None = None
		self._sa: SECURITY_ATTRIBUTES | None = None
		self._sd: ctypes.c_void_p | None = None
		# Queue for registrations that arrive before braille.handler is ready.
		self._pending: queue.Queue = queue.Queue()

	def start(self) -> None:
		if self._useSystemDacl:
			try:
				self._sa, self._sd = _buildSystemAccessSA()
			except OSError:
				log.exception(
					"braillePipeServer: failed to build SYSTEM-access security descriptor;"
					" falling back to default DACL (SYSTEM clients may be unable to connect)",
				)
		self._thread = threading.Thread(target=self._loop, name="braillePipeServer", daemon=True)
		self._thread.start()

	def stop(self) -> None:
		self._stop.set()
		# Unblock the accept loop by opening a dummy connection.
		try:
			dummy = _kernel32.CreateFile(
				self._pipeName,
				0,  # GENERIC_READ | GENERIC_WRITE not needed, just unblock
				0,
				None,
				3,  # OPEN_EXISTING
				0,
				None,
			)
			if dummy != INVALID_HANDLE_VALUE:
				_kernel32.CloseHandle(dummy)
		except Exception:
			pass
		if self._thread:
			self._thread.join(timeout=2.0)
		if self._sd is not None:
			_kernel32.LocalFree(self._sd)
			self._sd = None
			self._sa = None

	def processPending(self) -> None:
		"""Process any registrations that arrived before braille was ready."""
		while not self._pending.empty():
			try:
				item = self._pending.get_nowait()
			except queue.Empty:
				break
			role = item[0]
			if role == "mirror":
				_, handle, numCells = item
				try:
					session = _MirrorSession(handle, numCells)
					threading.Thread(
						target=_driveSession,
						args=(handle, session),
						daemon=True,
					).start()
				except Exception:
					log.exception("braillePipeServer: error creating pending mirror session")
					_kernel32.CloseHandle(handle)
			elif role == "direct":
				_, handle, hwnd, numCells = item
				try:
					session = _DirectSession(handle, hwnd, numCells)
					threading.Thread(
						target=_driveSession,
						args=(handle, session),
						daemon=True,
					).start()
				except Exception:
					log.exception("braillePipeServer: error creating pending direct session")
					_kernel32.CloseHandle(handle)

	def _loop(self) -> None:
		while not self._stop.is_set():
			try:
				handle = _createPipeInstance(self._pipeName, self._sa)
			except OSError:
				log.exception("braillePipeServer: failed to create pipe instance")
				break
			connected = _connectClient(handle)
			if self._stop.is_set():
				_kernel32.CloseHandle(handle)
				break
			if not connected:
				_kernel32.CloseHandle(handle)
				continue
			threading.Thread(
				target=_handleConnection,
				args=(handle, self._pending),
				daemon=True,
			).start()


def _driveSession(handle: ctypes.wintypes.HANDLE, session) -> None:
	"""Message loop for a session created from a pending registration."""
	try:
		while True:
			msg = _recvMessage(handle)
			if msg is None:
				break
			session.handleMessage(msg)
	except Exception:
		log.exception("braillePipeServer: error in deferred session")
	finally:
		session.close()
		_kernel32.CloseHandle(handle)


_server: _PipeServer | None = None


def initialize() -> None:
	"""Start the named pipe server."""
	global _server
	if _server is not None:
		return
	isSecure = isRunningOnSecureDesktop()
	pipeName = r"\\.\pipe\screen_reader_braille_secure" if isSecure else r"\\.\pipe\screen_reader_braille"
	# The secure-desktop instance runs as SYSTEM, so its default DACL already permits SYSTEM connections.  Only the normal-desktop instance needs the explicit SYSTEM ACE.
	_server = _PipeServer(pipeName, useSystemDacl=not isSecure)
	_server.start()
	log.info(f"braillePipeServer: listening on {pipeName}")
	# Resolve any registrations that beat us to it (shouldn't normally happen since we start early, but be defensive).
	_server.processPending()


def terminate() -> None:
	"""Stop the named pipe server."""
	global _server
	if _server is None:
		return
	_server.stop()
	_server = None
	log.info("braillePipeServer: stopped")
