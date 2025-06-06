# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
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
from ctypes import create_unicode_buffer

import shlobj
from logHandler import log
from winAPI.secureDesktop import post_secureDesktopStateChange
from NVDAHelper import localLib
from winBindings import kernel32

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

	def __init__(self, tempPath: Path = getProgramDataTempPath()) -> None:
		"""Initialize secure desktop handler.

		:param tempPath: Directory for IPC file storage
		"""
		self.tempPath = tempPath
		self.IPCPath: Path = self.tempPath / "NVDA"
		self.IPCPath.mkdir(parents=True, exist_ok=True)
		self.IPCFile = self.IPCPath / "remote.ipc"
		log.debug("Initialized SecureDesktopHandler with IPC file: %s", self.IPCFile)

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
		try:
			log.debug("Removing IPC file: %s", self.IPCFile)
			self.IPCFile.unlink()
		except FileNotFoundError:
			log.debug("IPC file already removed")
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
		if not self.tempPath.exists():
			log.debug(f"Creating temp directory: {self.tempPath}")
			self.tempPath.mkdir(parents=True, exist_ok=True)

		channel = str(uuid.uuid4())
		log.debug("Starting local relay server")
		self.sdServer = server.LocalRelayServer(port=0, password=channel, bindHost="127.0.0.1")
		port = self.sdServer.serverSocket.getsockname()[1]
		log.info("Local relay server started on port %d", port)

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

		data = [port, channel]
		log.debug(f"Writing connection data to IPC file: {self.IPCFile}")
		self.IPCFile.write_text(json.dumps(data))
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

		try:
			self.IPCFile.unlink()
		except FileNotFoundError:
			pass

	def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
		"""Initialize connection when starting in secure desktop.

		:return: Connection information if successful, None on failure
		"""
		log.info("Initializing secure desktop connection")
		try:
			log.debug(f"Reading connection data from IPC file: {self.IPCFile}")
			data = json.loads(self.IPCFile.read_text())
			self.IPCFile.unlink()
			port, channel = data

			# Try opening a socket to make sure we have the appropriate permissions
			testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			testSocket.close()

			# Check that a socket is open on the right IP and port and with the same owning process image
			processImageName = create_unicode_buffer(1024)
			kernel32.GetModuleFileName(0, processImageName, 1024)
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
