# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2026 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Secure desktop support for NVDA Remote.

Handles the transition between regular and secure desktop sessions in Windows,
maintaining remote connections across these transitions. Manages the creation of local
relay servers, connection bridging, and IPC (Inter-Process Communication) between the
regular and secure desktop instances of NVDA.

The secure desktop is a special Windows session used for UAC prompts and login screens
that runs in an isolated environment for security. This module ensures NVDA Remote
connections persist when entering and leaving this secure environment.

Note:
    All IPC operations use a temporary file in the system's ProgramData directory
    to exchange connection information between sessions.
"""

import json
import socket
import threading
import uuid
from pathlib import Path
from typing import Any, Optional
from ctypes import (
	FormatError,
	GetLastError,
	sizeof,
	create_unicode_buffer,
	wstring_at,
)
from ctypes.wintypes import WCHAR
from serial.win32 import INVALID_HANDLE_VALUE

import shlobj
from logHandler import log
from winAPI.secureDesktop import post_secureDesktopStateChange
from NVDAHelper import localLib
from winBindings.kernel32 import (
	FILE_MAP,
	PAGE,
	WAIT,
	CreateEvent,
	CreateFileMapping,
	GetModuleFileName,
	MapViewOfFile,
	OpenFileMapping,
	ResetEvent,
	SetEvent,
	UnmapViewOfFile,
	WaitForSingleObject,
)
from winKernel import closeHandle
from winKernel import ERROR_ALREADY_EXISTS

from . import bridge, server
from .connectionInfo import ConnectionInfo, ConnectionMode
from .protocol import RemoteMessageType
from .serializer import JSONSerializer
from .session import FollowerSession
from .transport import RelayTransport


def getProgramDataTempPath() -> Path:
	"""Get the system's program data temp directory path.

	:return: Path to the ProgramData temp directory
	"""
	return Path(shlobj.SHGetKnownFolderPath(shlobj.FolderId.PROGRAM_DATA)) / "temp"


class SecureDesktopHandler:
	"""Maintains remote connections during secure desktop transitions.

	Handles relay servers, IPC, and connection bridging between
	regular and secure desktop sessions.

	:cvar SD_CONNECT_BLOCK_TIMEOUT: Timeout in seconds for secure desktop connection attempts
	"""

	SD_CONNECT_BLOCK_TIMEOUT: int = 1

	_IPC_FILENAME = r"Local\NVDARemoteAccessSDHIPCFile"
	"""IPC filename"""
	_IPC_EVENTNAME = r"Local\NVDARemoteAccessSDHIPCEvent"
	"""IPC write event name"""
	_IPC_MAXLEN = 64
	"""
	Maximum length of IPC data, in characters.

	36 chars for a UUID4, 5 chars for a port number, and plenty of slack for JSON syntax.

	.. note::
		Must be multiplied by the size of a character when allocating memory.
	"""

	def __init__(self):
		"""Initialize secure desktop handler.

		:raises RuntimeError: if the IPC event cannot be created or opened.
		"""
		self._mapFile: int | None = None
		self._bufferAddress: int | None = None
		self._ipcEventHandle = CreateEvent(None, False, False, self._IPC_EVENTNAME)
		if self._ipcEventHandle is None:
			raise RuntimeError(f"Unable to get handle to IPC event. {GetLastError()}: {FormatError()}")
		log.debug("Initialized SecureDesktopHandler")

		self._followerSession: Optional[FollowerSession] = None
		self.sdServer: Optional[server.LocalRelayServer] = None
		self.sdRelay: Optional[RelayTransport] = None
		self.sdBridge: Optional[bridge.BridgeTransport] = None

		post_secureDesktopStateChange.register(self._onSecureDesktopChange)

	def terminate(self) -> None:
		"""Clean up handler resources."""
		log.debug("Terminating SecureDesktopHandler")
		post_secureDesktopStateChange.unregister(self._onSecureDesktopChange)
		self.leaveSecureDesktop()
		# The IPC event will be disposed of by the OS when all of its handles are closed.
		if not closeHandle(self._ipcEventHandle):
			log.debugWarning(f"Error closing handle to IPC event. {GetLastError()}: {FormatError()}")
		# We shouldn't be in a situation where we have shared IPC data,
		# but it's still good to check and clean it up if we do.
		if self._bufferAddress is not None:
			if not UnmapViewOfFile(self._bufferAddress):
				log.debugWarning(f"Error unmapping IPC shared memory. {GetLastError()}: {FormatError()}")
		if self._mapFile is not None:
			if not closeHandle(self._mapFile):
				log.debugWarning(
					f"Error closing handle to IPC file mapping. {GetLastError()}: {FormatError()}",
				)
		log.info("Secure desktop cleanup completed")

	@property
	def followerSession(self) -> Optional[FollowerSession]:
		return self._followerSession

	@followerSession.setter
	def followerSession(self, session: Optional[FollowerSession]) -> None:
		"""Update follower session reference and handle necessary cleanup/setup."""
		if self._followerSession == session:
			log.debug("Follower session unchanged, skipping update")
			return

		log.info("Updating follower session reference")
		if self.sdServer is not None:
			self.leaveSecureDesktop()

		if self._followerSession is not None and self._followerSession.transport is not None:
			transport = self._followerSession.transport
			transport.unregisterInbound(RemoteMessageType.SET_BRAILLE_INFO, self._onLeaderDisplayChange)
		self._followerSession = session
		if session is not None:
			session.transport.registerInbound(
				RemoteMessageType.SET_BRAILLE_INFO,
				self._onLeaderDisplayChange,
			)

	def _onSecureDesktopChange(self, isSecureDesktop: Optional[bool] = None) -> None:
		"""Internal callback for secure desktop state changes.

		:param isSecureDesktop: True if transitioning to secure desktop, False otherwise
		"""
		log.info(f"Secure desktop state changed: {'entering' if isSecureDesktop else 'leaving'}")
		if isSecureDesktop:
			self.enterSecureDesktop()
		else:
			self.leaveSecureDesktop()

	def enterSecureDesktop(self) -> None:
		"""Set up necessary components when entering secure desktop."""
		log.debug("Attempting to enter secure desktop")
		if self.followerSession is None or self.followerSession.transport is None:
			log.warning("No follower session connected, not entering secure desktop.")
			return
		log.debug("Creating shared memory for IPC.")
		mapFile = CreateFileMapping(
			INVALID_HANDLE_VALUE,  # Shared memory
			None,
			PAGE.READWRITE,
			0,  # High-order size
			self._IPC_MAXLEN * sizeof(WCHAR),  # Low-order size
			self._IPC_FILENAME,
		)
		if mapFile is None:
			log.error(f"Error creating file mapping: {GetLastError()}: {FormatError()}")
			return
		if GetLastError() == ERROR_ALREADY_EXISTS:
			log.debugWarning("Mapped file already exists")
		bufferAddress = MapViewOfFile(
			mapFile,
			FILE_MAP.ALL_ACCESS,
			0,
			0,
			self._IPC_MAXLEN * sizeof(WCHAR),
		)
		if bufferAddress is None:
			log.error(f"Couldn't map view of file. {GetLastError()}: {FormatError()}")
			if not closeHandle(mapFile):
				log.debugWarning(
					f"Error closing handle to IPC file mapping. {GetLastError()}: {FormatError()}",
				)
			return
		buffer = (WCHAR * self._IPC_MAXLEN).from_address(bufferAddress)
		channel = str(uuid.uuid4())
		log.debug("Starting local relay server")
		self.sdServer = server.LocalRelayServer(port=0, password=channel, bindHost="127.0.0.1")
		port = self.sdServer.serverSocket.getsockname()[1]
		log.info("Local relay server started on port %d", port)
		try:
			log.debug("Writing connection data to shared memory")
			buffer.value = json.dumps([port, channel])
			# Setting value checks if the array is long enough to contain the literal value,
			# and will write a terminating null if there is space to do so.
			# However, if the given string is exactly the length of the buffer,
			# no null terminator will be written.
			# If this happens, we cannot proceed,
			# as the contents of the array are not a valid c string.
			if buffer[-1] != "\x00":
				raise ValueError("Insufficient length for null terminator.")
		except ValueError:
			log.exception("Failed to write IPC data.", exc_info=True)
			if not UnmapViewOfFile(bufferAddress):
				log.debugWarning(f"Error unmapping IPC shared memory. {GetLastError()}: {FormatError()}")
			if not closeHandle(mapFile):
				log.debugWarning(
					f"Error closing handle to IPC file mapping. {GetLastError()}: {FormatError()}",
				)
			self.sdServer.close()
			self.sdServer = None
			return None

		serverThread = threading.Thread(target=self.sdServer.run)
		serverThread.daemon = True
		serverThread.start()

		self.sdRelay = RelayTransport(
			address=("127.0.0.1", port),
			serializer=JSONSerializer(),
			channel=channel,
			insecure=True,
			connectionType=ConnectionMode.LEADER,
		)
		self.sdRelay.registerInbound(RemoteMessageType.CLIENT_JOINED, self._onLeaderDisplayChange)
		self.followerSession.transport.registerInbound(
			RemoteMessageType.SET_BRAILLE_INFO,
			self._onLeaderDisplayChange,
		)

		self.sdBridge = bridge.BridgeTransport(self.followerSession.transport, self.sdRelay)

		relayThread = threading.Thread(target=self.sdRelay.run)
		relayThread.daemon = True
		relayThread.start()

		self._mapFile, self._bufferAddress = mapFile, bufferAddress
		# Signal that it's now safe to read the IPC shared memory and connect
		if not SetEvent(self._ipcEventHandle):
			log.error(f"Failed to set IPC event. {GetLastError()}: {FormatError()}")
		log.info("Secure desktop setup completed successfully")

	def leaveSecureDesktop(self) -> None:
		"""Clean up when leaving secure desktop."""
		log.debug("Attempting to leave secure desktop")
		if self.sdServer is None:
			log.debug("No secure desktop server running, nothing to clean up")
			return

		if self.sdBridge is not None:
			self.sdBridge.disconnect()
			self.sdBridge = None

		if self.sdServer is not None:
			self.sdServer.close()
			self.sdServer = None

		if self.sdRelay is not None:
			self.sdRelay.close()
			self.sdRelay = None

		if self.followerSession is not None and self.followerSession.transport is not None:
			self.followerSession.transport.unregisterInbound(
				RemoteMessageType.SET_BRAILLE_INFO,
				self._onLeaderDisplayChange,
			)
			self.followerSession.setDisplaySize()

		# The IPC event won't have been reset if a secure desktop copy didn't wait for it.
		# Even if it's not in the set state, resetting it is harmless.
		if not ResetEvent(self._ipcEventHandle):
			log.debugWarning(f"Failed to reset IPC event. {GetLastError()}: {FormatError()}")
		if self._bufferAddress is not None:
			if not UnmapViewOfFile(self._bufferAddress):
				log.debugWarning(f"Failed to unmap IPC file. {GetLastError()}: {FormatError()}")
			self._bufferAddress = None
		if self._mapFile is not None:
			if not closeHandle(self._mapFile):
				log.debugWarning(
					"Failed to close handle to memory mapped IPC file. {GetLastError()}: {FormatError()}",
				)
			self._mapFile = None

	def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
		"""Initialize connection when starting in secure desktop.

		:return: Connection information if successful, None on failure
		"""
		log.info("Initializing secure desktop connection")
		# Even though we only need read access,
		# Memory mapped files must all be mapped with the same permissions.
		mapFile = OpenFileMapping(FILE_MAP.ALL_ACCESS, False, self._IPC_FILENAME)
		if mapFile is None:
			log.debug(f"Failed to open IPC file mapping. {GetLastError()}: {FormatError()}")
			return None
		bufferAddress = MapViewOfFile(mapFile, FILE_MAP.ALL_ACCESS, 0, 0, self._IPC_MAXLEN * sizeof(WCHAR))
		if bufferAddress is None:
			log.error(f"Failed to map IPC file mapping. {GetLastError()}: {FormatError()}")
			if not closeHandle(mapFile):
				log.debugWarning(f"Failed to close file mapping. {GetLastError()}: {FormatError()}")
			return None
		waitResult = WaitForSingleObject(self._ipcEventHandle, 2000)
		if waitResult == WAIT.TIMEOUT:
			log.error("Timed out while waiting for IPC data.")
			return None
		elif waitResult == WAIT.FAILED:
			log.error(f"Failed to wait for event. {GetLastError()}: {FormatError()}")
			return None
		elif waitResult != WAIT.OBJECT_0:
			log.error(f"Unknown return from WaitForSingleObject: {waitResult}")
			return None
		try:
			log.debug("Reading connection data from IPC file mapping.")
			data = json.loads(wstring_at(bufferAddress))
			port, channel = data

			# Try opening a socket to make sure we have the appropriate permissions
			testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			testSocket.close()

			# Check that a socket is open on the right IP and port and with the same owning process image
			processImageName = create_unicode_buffer(1024)
			GetModuleFileName(0, processImageName, 1024)
			if not localLib.localListeningSocketExists(port, processImageName):
				raise RuntimeError("Matching socket not open.")

			log.info(f"Successfully established secure desktop connection on port {port}")
			return ConnectionInfo(
				hostname="127.0.0.1",
				mode=ConnectionMode.FOLLOWER,
				key=channel,
				port=port,
				insecure=True,
			)

		except Exception:
			log.warning("Failed to initialize secure desktop connection.", exc_info=True)
			return None
		finally:
			if not UnmapViewOfFile(bufferAddress):
				log.debugWarning(f"Failed to unmap view of IPC file. {GetLastError()}: {FormatError()}")
			if not closeHandle(mapFile):
				log.debugWarning(
					f"Failed to close handle to IPC file mapping. {GetLastError()}: {FormatError()}",
				)

	def _onLeaderDisplayChange(self, **kwargs: Any) -> None:
		"""Handle display size changes."""
		log.debug("Leader display change detected")
		if self.sdRelay is not None and self.followerSession is not None:
			log.debug("Propagating display size change to secure desktop relay")
			self.sdRelay.send(
				type=RemoteMessageType.SET_DISPLAY_SIZE,
				sizes=self.followerSession.leaderDisplaySizes,
			)
		else:
			log.warning("No secure desktop relay or follower session available, skipping display change")
