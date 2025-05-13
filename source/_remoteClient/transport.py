# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Network transport layer for NVDA Remote.

This module provides the core networking functionality for NVDA Remote.

Classes:
	Transport: Base class defining the transport interface
	TCPTransport: Implementation of secure TCP socket transport
	RelayTransport: Extended TCP transport for relay server connections
	ConnectorThread: Helper class for connection management

The transport layer handles:
	* Secure socket connections with SSL/TLS
	* Message serialization and deserialization
	* Connection management and reconnection
	* Event notifications for connection state changes
	* Message routing based on RemoteMessageType enum

All network operations run in background threads, while message handlers
are called on the main wxPython thread for thread-safety.
"""

from abc import ABC, abstractmethod
import hashlib
import select
import socket
import ssl
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from logHandler import log
from queue import Queue
from typing import Any, Literal, Optional, Self

import wx
from extensionPoints import Action, HandlerRegistrar

from . import configuration
from .connectionInfo import ConnectionInfo
from .protocol import PROTOCOL_VERSION, RemoteMessageType, hostPortToAddress
from .serializer import Serializer


@dataclass
class RemoteExtensionPoint:
	"""Bridges local extension points to remote message sending.

	This class connects local NVDA extension points to the remote transport layer,
	allowing local events to trigger remote messages with optional argument transformation.

	:note: The filter function, if provided, should take (*args, **kwargs) and return
	       a new kwargs dict to be sent in the message.
	"""

	extensionPoint: HandlerRegistrar
	"""The NVDA extension point to bridge"""

	messageType: RemoteMessageType
	"""The remote message type to send"""

	filter: Optional[Callable[..., dict[str, Any]]] = None
	"""Optional function to transform arguments before sending"""

	transport: Optional["Transport"] = None
	"""The transport instance (set on registration)"""

	def remoteBridge(self, *args: Any, **kwargs: Any) -> Literal[True]:
		"""Bridge function that gets registered to the extension point.

		Handles calling the filter if present and sending the message.

		:param args: Positional arguments from the extension point
		:param kwargs: Keyword arguments from the extension point
		:return: Always returns True to allow other handlers to process the event
		"""
		if self.filter is not None:
			# Filter should transform args/kwargs into just the kwargs needed for the message
			kwargs = self.filter(*args, **kwargs)
		if self.transport is not None:
			self.transport.send(self.messageType, **kwargs)
		return True

	def register(self, transport: "Transport") -> None:
		"""Register this bridge with a transport and the extension point."""
		self.transport = transport
		self.extensionPoint.register(self.remoteBridge)

	def unregister(self) -> None:
		"""Unregister this bridge from the extension point."""
		self.extensionPoint.unregister(self.remoteBridge)


class Transport(ABC):
	"""Base class defining the network transport interface for NVDA Remote.

	This abstract base class defines the interface that all network transports must implement.
	It provides core functionality for secure message passing, connection management,
	and event handling between NVDA instances.

	The Transport class handles:

	* Message serialization and routing using a pluggable serializer
	* Connection state management and event notifications
	* Registration of message type handlers
	* Thread-safe connection events

	To implement a new transport:

	1. Subclass Transport
	2. Implement connection logic in run()
	3. Call onTransportConnected() when connected
	4. Use send() to transmit messages
	5. Call appropriate event notifications

	Example:
		>>> serializer = JSONSerializer()
		>>> transport = TCPTransport(serializer, ("localhost", 8090))
		>>> transport.registerInbound(RemoteMessageType.key, handle_key)
		>>> transport.run()
	"""

	def __init__(self, serializer: Serializer) -> None:
		"""Initialize the transport.

		:param serializer: The serializer instance to use for message encoding/decoding
		"""
		self.serializer: Serializer = serializer
		"""The message serializer instance"""

		self.connected: bool = False
		""" True if transport has an active connection """

		self.successfulConnects: int = 0
		""" Counter of successful connection attempts """

		self.connectedEvent: threading.Event = threading.Event()
		""" Event that is set when connected """

		self.inboundHandlers: dict[RemoteMessageType, Action] = {}
		""" Registered message handlers """

		self.outboundHandlers: dict[RemoteMessageType, RemoteExtensionPoint] = {}
		""" Registered message handlers for outgoing messages"""

		self.transportConnected: Action = Action()
		"""Notifies when the transport is connected"""

		self.transportDisconnected: Action = Action()
		"""Notifies when the transport is disconnected"""

		self.transportCertificateAuthenticationFailed: Action = Action()
		"""Notifies when the transport fails to authenticate the certificate"""

		self.transportConnectionFailed: Action = Action()
		""" Notifies when the transport fails to connect """

		self.transportClosing: Action = Action()
		""" Notifies when the transport is closing """

	@abstractmethod
	def run(self) -> None:
		"""Connection logic for this transport."""
		...

	def onTransportConnected(self) -> None:
		"""Handle successful transport connection.

		:note: Called internally when connection established:
		    - Increments successful connection counter
		    - Sets connected flag to True
		    - Sets connected event
		    - Notifies transportConnected listeners
		"""
		self.successfulConnects += 1
		self.connected = True
		self.connectedEvent.set()
		self.transportConnected.notify()

	def registerInbound(self, type: RemoteMessageType, handler: Callable[..., None]) -> None:
		"""Register a handler for incoming messages of a specific type.

		:param type: The message type to handle
		:param handler: Callback function to process messages of this type
		:note: Multiple handlers can be registered for the same type.
		    Handlers are called asynchronously on wx main thread via CallAfter.
		    Handler will receive message payload as kwargs.
		:example:
		    >>> def handleKeypress(keyCode, pressed):
		    ...     print(f"Key {keyCode} {'pressed' if pressed else 'released'}")
		    >>> transport.registerInbound(RemoteMessageType.KEY, handleKeypress)
		"""
		if type not in self.inboundHandlers:
			log.debug(f"Creating new handler for {type}")
			self.inboundHandlers[type] = Action()
		log.debug(f"Registering handler for {type}")
		self.inboundHandlers[type].register(handler)

	def unregisterInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Remove a previously registered message handler.

		:param type: The message type to unregister from
		:param handler: The handler function to remove
		:note: If handler was not registered, this is a no-op
		"""
		self.inboundHandlers[type].unregister(handler)
		log.debug(f"Unregistered handler for {type}")

	def registerOutbound(
		self,
		extensionPoint: HandlerRegistrar,
		messageType: RemoteMessageType,
		filter: Optional[Callable[..., dict[str, Any]]] = None,
	) -> None:
		"""Register an extension point to a message type.

		:param extensionPoint: The extension point to register
		:param messageType: The message type to register the extension point to
		:param filter: Optional function to transform message before sending
		:note: Filter function should take (*args, **kwargs) and return new kwargs dict
		"""
		remoteExtension = RemoteExtensionPoint(
			extensionPoint=extensionPoint,
			messageType=messageType,
			filter=filter,
		)
		remoteExtension.register(self)
		self.outboundHandlers[messageType] = remoteExtension

	def unregisterOutbound(self, messageType: RemoteMessageType) -> None:
		"""Unregister an extension point from a message type.

		Args:
			messageType (RemoteMessageType): The message type to unregister the extension point from
		"""
		self.outboundHandlers[messageType].unregister()
		del self.outboundHandlers[messageType]

	@abstractmethod
	def send(self, type: RemoteMessageType, **kwargs: Any) -> None:
		"""Send a message through this transport.

		:param type: Message type, typically a :class:`~_remoteClient.protocol.RemoteMessageType` enum value.
		:param kwargs: Message payload data to serialize.
		"""
		...


class TCPTransport(Transport):
	"""Secure TCP socket transport implementation.

	This class implements the Transport interface using TCP sockets with SSL/TLS
	encryption. It handles connection establishment, data transfer, and connection
	lifecycle management.
	"""

	def __init__(
		self,
		serializer: Serializer,
		address: tuple[str, int],
		timeout: int = 0,
		insecure: bool = False,
	) -> None:
		"""Initialize the TCP transport.

		:param serializer: Message serializer instance
		:param address: Remote address to connect to, as (host, port) tuple
		:param timeout: Connection timeout in seconds, defaults to 0
		:param insecure: Skip certificate verification, defaults to False
		"""
		super().__init__(serializer=serializer)
		self.closed: bool = False
		"""Whether transport is closed"""

		self.buffer = b""
		""" Buffer to hold partially received data """

		self.queue = Queue()
		""" Queue of outbound messages """

		self.address = address
		""" Remote address to connect to """

		self.serverSock = None
		""" The SSL socket connection """

		# Reading/writing from an SSL socket is not thread safe, so guard access to the socket with a lock.
		# See https://bugs.python.org/issue41597#msg375692
		self.serverSockLock = threading.Lock()
		""" Lock for thread-safe socket access """

		self.queueThread: threading.Thread | None = None
		""" Thread handling outbound messages """

		self.timeout: int = timeout
		""" Connection timeout in seconds """

		self.reconnectorThread: ConnectorThread = ConnectorThread(self)
		""" Thread managing reconnection """

		self.insecure: bool = insecure
		"""Whether to skip certificate verification"""

	def run(self) -> None:
		"""
		Establishes a connection to the server and manages the transport lifecycle.

		This method attempts to create and connect an outbound socket to the server
		using the provided address. If SSL certificate verification fails, it checks
		if the host fingerprint is trusted. If trusted, it retries the connection
		with insecure mode enabled. If not, it notifies about the certificate
		authentication failure and raises the exception. For other exceptions, it
		notifies about the connection failure and raises the exception.

		Once connected, it triggers the transport connected event, starts the queue
		thread, and enters the read loop. Upon disconnection, it clears the connected
		event, notifies about the transport disconnection, and performs cleanup.

		Raises:
			ssl.SSLCertVerificationError: If SSL certificate verification fails and
										  the fingerprint is not trusted.
			Exception: For any other exceptions during the connection process.
		"""
		self.closed = False
		try:
			self.serverSock = self.createOutboundSocket(
				*self.address,
				insecure=self.insecure,
			)
			self.serverSock.connect(self.address)
		except ssl.SSLCertVerificationError:
			fingerprint = None
			try:
				fingerprint = self.getHostFingerprint()
			except Exception:
				pass
			if self.isFingerprintTrusted(fingerprint):
				self.insecure = True
				return self.run()
			self.lastFailFingerprint = fingerprint
			self.transportCertificateAuthenticationFailed.notify()
			raise
		except Exception:
			self.transportConnectionFailed.notify()
			raise
		self.onTransportConnected()
		self.startQueueThread()
		self._readLoop()
		self.connected = False
		self.connectedEvent.clear()
		self.transportDisconnected.notify()
		self._disconnect()

	def isFingerprintTrusted(self, fingerprint: str) -> bool:
		"""Check if the fingerprint is trusted.

		:param fingerprint: The fingerprint to check
		:return: True if the fingerprint is trusted, False otherwise
		"""
		config = configuration.getRemoteConfig()
		return (
			hostPortToAddress(self.address) in config["trustedCertificates"]
			and config["trustedCertificates"][hostPortToAddress(self.address)] == fingerprint
		)

	def getHostFingerprint(self) -> str:
		tempConnection = self.createOutboundSocket(*self.address, insecure=True)
		tempConnection.connect(self.address)
		certBin = tempConnection.getpeercert(True)
		tempConnection.close()
		fingerprint = hashlib.sha256(certBin).hexdigest().lower()
		return fingerprint

	def startQueueThread(self) -> None:
		"""Start the outbound message queue thread."""
		if self.queueThread and self.queueThread.is_alive():
			return
		self.queueThread = threading.Thread(target=self.sendQueue, name="queue_thread")
		self.queueThread.daemon = True
		self.queueThread.start()

	def _readLoop(self) -> None:
		"""Main loop for reading data from the server socket."""
		while self.serverSock is not None:
			try:
				readers, writers, error = select.select(
					[self.serverSock],
					[],
					[self.serverSock],
				)
			except socket.error:
				self.buffer = b""
				break
			if self.serverSock in error:
				self.buffer = b""
				break
			if self.serverSock in readers:
				try:
					self.processIncomingSocketData()
				except socket.error:
					self.buffer = b""
					break

	def createOutboundSocket(
		self,
		host: str,
		port: int,
		insecure: bool = False,
	) -> ssl.SSLSocket:
		"""Create and configure an SSL socket for outbound connections.

		Creates a TCP socket with appropriate timeout and keep-alive settings,
		then wraps it with SSL/TLS encryption.

		:param host: Remote hostname to connect to
		:param port: Remote port number
		:param insecure: Skip certificate verification, defaults to False
		:return: Configured SSL socket ready for connection
		:note: The socket is created but not yet connected. Call connect() separately.
		:raises socket.error: If socket creation fails
		:raises ssl.SSLError: If SSL/TLS setup fails
		"""
		if host.lower().endswith(".onion"):
			serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			address = socket.getaddrinfo(host, port)[0]
			serverSock = socket.socket(*address[:3])
		if self.timeout:
			serverSock.settimeout(self.timeout)
		serverSock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		serverSock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60000, 2000))
		ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		if insecure:
			ctx.verify_mode = ssl.CERT_NONE
			log.warn(f"Skipping certificate verification for {host}:{port}")
		ctx.check_hostname = not insecure
		ctx.load_default_certs()

		serverSock = ctx.wrap_socket(sock=serverSock, server_hostname=host)
		return serverSock

	def getpeercert(
		self,
		binaryForm: bool = False,
	) -> dict[str, Any] | bytes | None:
		"""Get the certificate from the peer.

		Retrieves the certificate presented by the remote peer during SSL handshake.

		:param binaryForm: If True, return the raw certificate bytes, if False return a parsed dictionary, defaults to False
		:return: The peer's certificate, or None if not connected
		:raises ssl.SSLError: If certificate retrieval fails
		"""
		if self.serverSock is None:
			return None
		return self.serverSock.getpeercert(binaryForm)

	def processIncomingSocketData(self) -> None:
		"""Process incoming data from the server socket.

		Reads data from the socket in chunks, handling partial messages and SSL behavior.
		Complete messages are passed to parse() for processing.

		:note: Uses non-blocking reads with SSL and 16KB buffer size
		:raises socket.error: If socket read fails
		:raises ssl.SSLWantReadError: If no SSL data is available
		"""
		# This approach may be problematic:
		# See also server.py handle_data in class Client.
		buffSize = 16384
		with self.serverSockLock:
			# select operates on the raw socket. Even though it said there was data to
			# read, that might be SSL data which might not result in actual data for
			# us. Therefore, do a non-blocking read so SSL doesn't try to wait for
			# more data for us.
			# We don't make the socket non-blocking earlier because then we'd have to
			# handle retries during the SSL handshake.
			# See https://stackoverflow.com/questions/3187565/select-and-ssl-in-python
			# and https://docs.python.org/3/library/ssl.html#notes-on-non-blocking-sockets
			self.serverSock.setblocking(False)
			try:
				data = self.buffer + self.serverSock.recv(buffSize)
			except ssl.SSLWantReadError:
				# There's no data for us.
				return
			finally:
				self.serverSock.setblocking(True)
		self.buffer = b""
		if not data:
			self._disconnect()
			return
		if b"\n" not in data:
			self.buffer += data
			return
		while b"\n" in data:
			line, sep, data = data.partition(b"\n")
			self.parse(line)
		self.buffer += data

	def parse(self, line: bytes) -> None:
		"""Parse and handle a complete message line.

		Deserializes message and routes to appropriate handler based on type.

		:param line: Complete message line to parse
		:raises ValueError: If message type is invalid
		:note: Messages require 'type' field matching RemoteMessageType
		:note: Handlers execute asynchronously on wx main thread
		"""
		obj = self.serializer.deserialize(line)
		if configuration._isDebugForRemoteClient():
			log.debug(f"Received message: {obj!r}")
		if "type" not in obj:
			log.warn(f"Received message without type: {obj!r}")
			return
		try:
			messageType = RemoteMessageType(obj["type"])
		except ValueError:
			log.warn(f"Received message with invalid type: {obj!r}")
			return
		del obj["type"]
		extensionPoint = self.inboundHandlers.get(messageType)
		if not extensionPoint:
			log.warn(f"Received message with unhandled type: {messageType} {obj!r}")
			return
		wx.CallAfter(extensionPoint.notify, **obj)

	def sendQueue(self) -> None:
		"""Background thread that processes the outbound message queue.

		:note: Runs in separate thread with thread-safe socket access via serverSockLock
		:note: Exits on receiving None or socket error
		:raises socket.error: If sending data fails
		"""
		while True:
			item = self.queue.get()
			if configuration._isDebugForRemoteClient():
				log.debug(f"Sending outbound message: {item!r}")
			if item is None:
				return
			try:
				with self.serverSockLock:
					self.serverSock.sendall(item)
			except socket.error:
				return

	def send(self, type: RemoteMessageType, **kwargs: Any) -> None:
		"""Send a message through the transport.

		:param type: Message type, typically a RemoteMessageType enum value
		:param kwargs: Message payload data to serialize
		:note: Thread-safe and can be called from any thread
		:note: Messages are dropped if transport is not connected
		"""
		if self.connected:
			obj = self.serializer.serialize(type=type, **kwargs)
			if configuration._isDebugForRemoteClient():
				log.debug(f"Enqueuing outbound message: {obj!r}")
			self.queue.put(obj)
		else:
			log.debugWarning(f"Attempted to send message {type} while not connected")

	def _disconnect(self) -> None:
		"""Internal method to disconnect the transport.

		:note: Called internally on errors, unlike close() which is called explicitly
		:note: Cleans up queue thread and socket without stopping connector thread
		"""
		if self.queueThread is not None:
			self.queue.put(None)
			self.queueThread.join()
			self.queueThread = None
		clearQueue(self.queue)
		if self.serverSock:
			self.serverSock.close()
			self.serverSock = None

	def close(self):
		"""Close the transport and stop all threads.

		:note: Stops reconnector thread and cleans up all resources
		"""
		self.transportClosing.notify()
		self.reconnectorThread.running = False
		self._disconnect()
		self.closed = True
		self.reconnectorThread = ConnectorThread(self)


class RelayTransport(TCPTransport):
	"""Transport for connecting through a relay server.

	Extends TCPTransport with relay-specific protocol handling for channels
	and connection types. Manages protocol versioning and channel joining.
	"""

	def __init__(
		self,
		serializer: Serializer,
		address: tuple[str, int],
		timeout: int = 0,
		channel: str | None = None,
		connectionType: str | None = None,
		protocolVersion: int = PROTOCOL_VERSION,
		insecure: bool = False,
	) -> None:
		"""Initialize a new RelayTransport instance.

		:param serializer: Serializer for encoding/decoding messages
		:param address: Tuple of (host, port) to connect to
		:param timeout: Connection timeout in seconds, defaults to 0
		:param channel: Channel name to join, defaults to ``None``
		:param connectionType: Connection type identifier, defaults to ``None``
		:param protocolVersion: Protocol version to use, defaults to :const:`PROTOCOL_VERSION`
		:param insecure: Whether to skip certificate verification, defaults to ``False``
		"""
		super().__init__(
			address=address,
			serializer=serializer,
			timeout=timeout,
			insecure=insecure,
		)
		log.info(f"Connecting to {address} channel {channel}")
		self.channel: str | None = channel
		"""Relay channel name"""

		self.connectionType: str | None = connectionType
		""" Type of relay connection """

		self.protocolVersion: int = protocolVersion
		""" Protocol version in use """

		self.transportConnected.register(self.onConnected)

	@classmethod
	def create(cls, connectionInfo: ConnectionInfo, serializer: Serializer) -> Self:
		"""Create a RelayTransport from a ConnectionInfo object.

		:param connectionInfo: ConnectionInfo instance containing connection details
		:param serializer: Serializer instance for message encoding/decoding
		:return: Configured RelayTransport instance ready for connection
		"""
		return cls(
			serializer=serializer,
			address=(connectionInfo.hostname, connectionInfo.port),
			channel=connectionInfo.key,
			connectionType=connectionInfo.mode,
			insecure=connectionInfo.insecure,
		)

	def onConnected(self) -> None:
		"""Handle successful connection to relay server.

		Called automatically when transport connects. Sends protocol version and
		either joins channel or requests key generation.

		:raises ValueError: If protocol version is invalid
		"""
		self.send(RemoteMessageType.PROTOCOL_VERSION, version=self.protocolVersion)
		if self.channel is not None:
			self.send(
				RemoteMessageType.JOIN,
				channel=self.channel,
				connection_type=self.connectionType,
			)
		else:
			self.send(RemoteMessageType.GENERATE_KEY)


class ConnectorThread(threading.Thread):
	"""Background thread that manages connection attempts.

	Handles automatic reconnection with configurable delay between attempts.
	Runs until explicitly stopped.

	To stop, set :attr:`running` to ``False``.
	"""

	def __init__(self, connector: Transport, reconnectDelay: int = 5) -> None:
		"""Initialize the connector thread.

		:param connector: Transport instance to manage connections for
		:param reconnectDelay: Seconds between attempts, defaults to 5
		"""
		super().__init__()
		self.reconnectDelay: int = reconnectDelay
		"""Seconds to wait between connection attempts"""

		self.running: bool = True
		"""Whether thread should continue running"""

		self.connector: Transport = connector
		"""Transport to manage connections for"""

		self.name = self.name + "_connector_loop"
		self.daemon = True

	def run(self):
		while self.running:
			try:
				self.connector.run()
			except socket.error:
				time.sleep(self.reconnectDelay)
				continue
			else:
				time.sleep(self.reconnectDelay)
		log.info(f"Ending control connector thread {self.name}")


def clearQueue(queue: Queue[bytes | None]) -> None:
	"""Empty all items from a queue without blocking.

	Removes all items from the queue in a non-blocking way,
	useful for cleaning up before disconnection.

	:param queue: Queue instance to clear
	:note: This function catches and ignores any exceptions that occur
	       while trying to get items from an empty queue.
	"""
	try:
		while True:
			queue.get_nowait()
	except Exception:
		pass
