"""Secure desktop support for NVDA Remote.

This module handles the transition between regular and secure desktop sessions in Windows,
maintaining remote connections across these transitions. It manages the creation of local
relay servers, connection bridging, and IPC (Inter-Process Communication) between the
regular and secure desktop instances of NVDA.

The secure desktop is a special Windows session used for UAC prompts and login screens
that runs in an isolated environment for security. This module ensures NVDA Remote
connections persist when entering and leaving this secure environment.
"""

import json
import socket
import threading
import uuid
from pathlib import Path
from typing import Any, Optional

import shlobj
from logHandler import log
from winAPI.secureDesktop import post_secureDesktopStateChange

from . import bridge, server
from .connection_info import ConnectionInfo, ConnectionMode
from .protocol import RemoteMessageType
from .serializer import JSONSerializer
from .session import SlaveSession
from .transport import RelayTransport


def getProgramDataTempPath() -> Path:
	"""Get the system's program data temp directory path."""
	if hasattr(shlobj, "SHGetKnownFolderPath"):
		return Path(shlobj.SHGetKnownFolderPath(shlobj.FolderId.PROGRAM_DATA)) / "temp"
	return Path(shlobj.SHGetFolderPath(0, shlobj.CSIDL_COMMON_APPDATA)) / "temp"


class SecureDesktopHandler:
	"""Maintains remote connections during secure desktop transitions.

	Handles relay servers, IPC, and connection bridging between
	regular and secure desktop sessions.
	"""

	SD_CONNECT_BLOCK_TIMEOUT: int = 1

	def __init__(self, temp_path: Path = getProgramDataTempPath()) -> None:
		"""
		Initialize secure desktop handler.

		Args:
			temp_path: Path to temporary directory for IPC file. Defaults to program data temp path.
		"""
		self.tempPath = temp_path
		self.IPCFile = temp_path / "remote.ipc"
		log.debug(f"Initialized SecureDesktopHandler with IPC file: {self.IPCFile}")

		self._slaveSession: Optional[SlaveSession] = None
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
			log.debug(f"Removing IPC file: {self.IPCFile}")
			self.IPCFile.unlink()
		except FileNotFoundError:
			log.debug("IPC file already removed")
		log.info("Secure desktop cleanup completed")

	@property
	def slaveSession(self) -> Optional[SlaveSession]:
		return self._slaveSession

	@slaveSession.setter
	def slaveSession(self, session: Optional[SlaveSession]) -> None:
		"""
		Update slave session reference and handle necessary cleanup/setup.

		Args:
			session: New SlaveSession instance or None to clear
		"""
		if self._slaveSession == session:
			log.debug("Slave session unchanged, skipping update")
			return

		log.info("Updating slave session reference")
		if self.sdServer is not None:
			self.leaveSecureDesktop()

		if self._slaveSession is not None and self._slaveSession.transport is not None:
			transport = self._slaveSession.transport
			transport.unregisterInbound(RemoteMessageType.set_braille_info, self._onMasterDisplayChange)
		self._slaveSession = session
		self.slaveSession.transport.registerInbound(
			RemoteMessageType.set_braille_info,
			self._onMasterDisplayChange,
		)

	def _onSecureDesktopChange(self, isSecureDesktop: Optional[bool] = None) -> None:
		"""
		Internal callback for secure desktop state changes.

		Args:
			isSecureDesktop: True if transitioning to secure desktop, False otherwise
		"""
		log.info(f"Secure desktop state changed: {'entering' if isSecureDesktop else 'leaving'}")
		if isSecureDesktop:
			self.enterSecureDesktop()
		else:
			self.leaveSecureDesktop()

	def enterSecureDesktop(self) -> None:
		"""Set up necessary components when entering secure desktop."""
		log.debug("Attempting to enter secure desktop")
		if self.slaveSession is None or self.slaveSession.transport is None:
			log.warning("No slave session connected, not entering secure desktop.")
			return
		if not self.tempPath.exists():
			log.debug(f"Creating temp directory: {self.tempPath}")
			self.tempPath.mkdir(parents=True, exist_ok=True)

		channel = str(uuid.uuid4())
		log.debug("Starting local relay server")
		self.sdServer = server.LocalRelayServer(port=0, password=channel, bind_host="127.0.0.1")
		port = self.sdServer.serverSocket.getsockname()[1]
		log.info(f"Local relay server started on port {port}")

		serverThread = threading.Thread(target=self.sdServer.run)
		serverThread.daemon = True
		serverThread.start()

		self.sdRelay = RelayTransport(
			address=("127.0.0.1", port),
			serializer=JSONSerializer(),
			channel=channel,
			insecure=True,
			connectionType=ConnectionMode.MASTER.value,
		)
		self.sdRelay.registerInbound(RemoteMessageType.client_joined, self._onMasterDisplayChange)
		self.slaveSession.transport.registerInbound(
			RemoteMessageType.set_braille_info,
			self._onMasterDisplayChange,
		)

		self.sdBridge = bridge.BridgeTransport(self.slaveSession.transport, self.sdRelay)

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

		if self.slaveSession is not None and self.slaveSession.transport is not None:
			self.slaveSession.transport.unregisterInbound(
				RemoteMessageType.set_braille_info,
				self._onMasterDisplayChange,
			)
			self.slaveSession.setDisplaySize()

		try:
			self.IPCFile.unlink()
		except FileNotFoundError:
			pass

	def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
		"""
		Initialize connection when starting in secure desktop.

		Returns:
			ConnectionInfo instance if successful, None otherwise
		"""
		log.info("Initializing secure desktop connection")
		try:
			log.debug(f"Reading connection data from IPC file: {self.IPCFile}")
			data = json.loads(self.IPCFile.read_text())
			self.IPCFile.unlink()
			port, channel = data

			testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			testSocket.close()

			log.info(f"Successfully established secure desktop connection on port {port}")
			return ConnectionInfo(
				hostname="127.0.0.1",
				mode=ConnectionMode.SLAVE,
				key=channel,
				port=port,
				insecure=True,
			)

		except Exception:
			log.exception("Failed to initialize secure desktop connection.")
			return None

	def _onMasterDisplayChange(self, **kwargs: Any) -> None:
		"""Handle display size changes."""
		log.debug("Master display change detected")
		if self.sdRelay is not None and self.slaveSession is not None:
			log.debug("Propagating display size change to secure desktop relay")
			self.sdRelay.send(
				type=RemoteMessageType.set_display_size,
				sizes=self.slaveSession.masterDisplaySizes,
			)
