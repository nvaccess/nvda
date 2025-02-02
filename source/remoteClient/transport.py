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

import hashlib
import select
import socket
import ssl
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from logging import getLogger
from queue import Queue
from typing import Any, Optional

import wx
from extensionPoints import Action, HandlerRegistrar

from . import configuration
from .connectionInfo import ConnectionInfo
from .protocol import PROTOCOL_VERSION, RemoteMessageType, hostPortToAddress
from .serializer import Serializer

log = getLogger("transport")


@dataclass
class RemoteExtensionPoint:
	"""Bridges local extension points to remote message sending.

	This class connects local NVDA extension points to the remote transport layer,
	allowing local events to trigger remote messages with optional argument transformation.

	:param extensionPoint: The NVDA extension point to bridge
	:type extensionPoint: HandlerRegistrar
	:param messageType: The remote message type to send
	:type messageType: RemoteMessageType
	:param filter: Optional function to transform arguments before sending
	:type filter: Optional[Callable[..., dict[str, Any]]]
	:param transport: The transport instance (set on registration)
	:type transport: Optional[Transport]

	:note: The filter function, if provided, should take (*args, **kwargs) and return
	       a new kwargs dict to be sent in the message.
	"""

	extensionPoint: HandlerRegistrar
	messageType: RemoteMessageType
	filter: Optional[Callable[..., dict[str, Any]]] = None
	transport: Optional["Transport"] = None

	def remoteBridge(self, *args: Any, **kwargs: Any) -> bool:
		"""Bridge function that gets registered to the extension point.

		Handles calling the filter if present and sending the message.

		:param args: Positional arguments from the extension point
		:type args: Any
		:param kwargs: Keyword arguments from the extension point
		:type kwargs: Any
		:return: Always returns True to allow other handlers to process the event
		:rtype: bool
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


class Transport:
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

	:param serializer: The serializer instance to use for message encoding/decoding
	:type serializer: Serializer

	:ivar connected: True if transport has an active connection
	:vartype connected: bool
	:ivar successfulConnects: Counter of successful connection attempts
	:vartype successfulConnects: int
	:ivar connectedEvent: Event that is set when connected
	:vartype connectedEvent: threading.Event
	:ivar serializer: The message serializer instance
	:vartype serializer: Serializer
	:ivar inboundHandlers: Registered message handlers
	:vartype inboundHandlers: Dict[RemoteMessageType, Callable]

	:cvar transportConnected: Fired after connection is established and ready
	:vartype transportConnected: Action
	:cvar transportDisconnected: Fired when existing connection is lost
	:vartype transportDisconnected: Action
	:cvar transportCertificateAuthenticationFailed: Fired when SSL certificate validation fails
	:vartype transportCertificateAuthenticationFailed: Action
	:cvar transportConnectionFailed: Fired when a connection attempt fails
	:vartype transportConnectionFailed: Action
	:cvar transportClosing: Fired before transport is shut down
	:vartype transportClosing: Action
	"""

	connected: bool
	successfulConnects: int
	connectedEvent: threading.Event
	serializer: Serializer

	def __init__(self, serializer: Serializer) -> None:
		self.serializer = serializer
		self.connected = False
		self.successfulConnects = 0
		self.connectedEvent = threading.Event()
		self.inboundHandlers: dict[RemoteMessageType, Action] = {}
		self.outboundHandlers: dict[RemoteMessageType, RemoteExtensionPoint] = {}
		self.transportConnected = Action()
		"""
		Notifies when the transport is connected
		"""
		self.transportDisconnected = Action()
		"""
		Notifies when the transport is disconnected
		"""
		self.transportCertificateAuthenticationFailed = Action()
		"""
		Notifies when the transport fails to authenticate the certificate
		"""
		self.transportConnectionFailed = Action()
		"""
		Notifies when the transport fails to connect
		"""
		self.transportClosing = Action()
		"""
		Notifies when the transport is closing
		"""

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

	def registerInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Register a handler for incoming messages of a specific type.

		:param type: The message type to handle
		:param handler: Callback function to process messages of this type
		:note: Multiple handlers can be registered for the same type.
		    Handlers are called asynchronously on wx main thread via CallAfter.
		    Handler will receive message payload as kwargs.
		:example:
		    >>> def handle_keypress(key_code, pressed):
		    ...     print(f"Key {key_code} {'pressed' if pressed else 'released'}")
		    >>> transport.registerInbound(RemoteMessageType.key_press, handle_keypress)
		"""
		if type not in self.inboundHandlers:
			log.debug("Creating new handler for %s", type)
			self.inboundHandlers[type] = Action()
		log.debug("Registering handler for %s", type)
		self.inboundHandlers[type].register(handler)

	def unregisterInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Remove a previously registered message handler.

		:param type: The message type to unregister from
		:param handler: The handler function to remove
		:note: If handler was not registered, this is a no-op
		"""
		self.inboundHandlers[type].unregister(handler)
		log.debug("Unregistered handler for %s", type)

	def registerOutbound(
		self,
		extensionPoint: HandlerRegistrar,
		messageType: RemoteMessageType,
		filter: Optional[Callable] = None,
	):
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

	def unregisterOutbound(self, messageType: RemoteMessageType):
		"""Unregister an extension point from a message type.

		Args:
			messageType (RemoteMessageType): The message type to unregister the extension point from
		"""
		self.outboundHandlers[messageType].unregister()
		del self.outboundHandlers[messageType]


class TCPTransport(Transport):
	"""Secure TCP socket transport implementation.

	This class implements the Transport interface using TCP sockets with SSL/TLS
	encryption. It handles connection establishment, data transfer, and connection
	lifecycle management.

	:param serializer: Message serializer instance
	:type serializer: Serializer
	:param address: Remote address to connect to as (host, port) tuple
	:type address: tuple[str, int]
	:param timeout: Connection timeout in seconds, defaults to 0
	:type timeout: int, optional
	:param insecure: Skip certificate verification, defaults to False
	:type insecure: bool, optional

	:ivar buffer: Buffer for incomplete received data
	:vartype buffer: bytes
	:ivar closed: Whether transport is closed
	:vartype closed: bool
	:ivar queue: Queue of outbound messages
	:vartype queue: Queue[Optional[bytes]]
	:ivar insecure: Whether to skip certificate verification
	:vartype insecure: bool
	:ivar address: Remote address to connect to
	:vartype address: tuple[str, int]
	:ivar timeout: Connection timeout in seconds
	:vartype timeout: int
	:ivar serverSock: The SSL socket connection
	:vartype serverSock: Optional[ssl.SSLSocket]
	:ivar serverSockLock: Lock for thread-safe socket access
	:vartype serverSockLock: threading.Lock
	:ivar queueThread: Thread handling outbound messages
	:vartype queueThread: Optional[threading.Thread]
	:ivar reconnectorThread: Thread managing reconnection
	:vartype reconnectorThread: ConnectorThread
	"""

	buffer: bytes
	closed: bool
	queue: Queue[Optional[bytes]]
	insecure: bool
	serverSockLock: threading.Lock
	address: tuple[str, int]
	serverSock: Optional[ssl.SSLSocket]
	queueThread: Optional[threading.Thread]
	timeout: int
	reconnectorThread: "ConnectorThread"
	lastFailFingerprint: Optional[str]

	def __init__(
		self,
		serializer: Serializer,
		address: tuple[str, int],
		timeout: int = 0,
		insecure: bool = False,
	) -> None:
		super().__init__(serializer=serializer)
		self.closed = False
		# Buffer to hold partially received data
		self.buffer = b""
		self.queue = Queue()
		self.address = address
		self.serverSock = None
		# Reading/writing from an SSL socket is not thread safe.
		# See https://bugs.python.org/issue41597#msg375692
		# Guard access to the socket with a lock.
		self.serverSockLock = threading.Lock()
		self.queueThread = None
		self.timeout = timeout
		self.reconnectorThread = ConnectorThread(self)
		self.insecure = insecure

	def run(self) -> None:
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
				tmp_con = self.createOutboundSocket(*self.address, insecure=True)
				tmp_con.connect(self.address)
				certBin = tmp_con.getpeercert(True)
				tmp_con.close()
				fingerprint = hashlib.sha256(certBin).hexdigest().lower()
			except Exception:
				pass
			config = configuration.get_config()
			if (
				hostPortToAddress(self.address) in config["trusted_certs"]
				and config["trusted_certs"][hostPortToAddress(self.address)] == fingerprint
			):
				self.insecure = True
				return self.run()
			self.lastFailFingerprint = fingerprint
			self.transportCertificateAuthenticationFailed.notify()
			raise
		except Exception:
			self.transportConnectionFailed.notify()
			raise
		self.onTransportConnected()
		self.queueThread = threading.Thread(target=self.sendQueue)
		self.queueThread.daemon = True
		self.queueThread.start()
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
		self.connected = False
		self.connectedEvent.clear()
		self.transportDisconnected.notify()
		self._disconnect()

	def createOutboundSocket(
		self,
		host: str,
		port: int,
		insecure: bool = False,
	) -> ssl.SSLSocket | None:
		"""Create and configure an SSL socket for outbound connections.

		Creates a TCP socket with appropriate timeout and keep-alive settings,
		then wraps it with SSL/TLS encryption.

		:param host: Remote hostname to connect to
		:type host: str
		:param port: Remote port number
		:type port: int
		:param insecure: Skip certificate verification, defaults to False
		:type insecure: bool, optional
		:return: Configured SSL socket ready for connection
		:rtype: ssl.SSLSocket | None
		:note: The socket is created but not yet connected. Call connect() separately.
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
			log.warn("Skipping certificate verification for %s:%d", host, port)
		ctx.check_hostname = not insecure
		ctx.load_default_certs()

		serverSock = ctx.wrap_socket(sock=serverSock, server_hostname=host)
		return serverSock

	def getpeercert(
		self,
		binary_form: bool = False,
	) -> dict[str, Any] | bytes | None:
		"""Get the certificate from the peer.

		Retrieves the certificate presented by the remote peer during SSL handshake.

		Args:
				binary_form (bool, optional): If True, return the raw certificate bytes.
						If False, return a parsed dictionary. Defaults to False.

		Returns:
				Optional[Union[Dict[str, Any], bytes]]: The peer's certificate, or None if not connected.
						Format depends on binary_form parameter.
		"""
		if self.serverSock is None:
			return None
		return self.serverSock.getpeercert(binary_form)

	def processIncomingSocketData(self) -> None:
		"""Process incoming data from the server socket.

		Reads available data from the socket, buffers partial messages,
		and processes complete messages by passing them to parse().

		Messages are expected to be newline-delimited.
		Partial messages are stored in self.buffer until complete.

		Note:
				This method handles SSL-specific socket behavior and non-blocking reads.
				It is called when select() indicates data is available.
				Uses a fixed 16384 byte buffer which may need tuning for performance.
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

		Deserializes a message and routes it to the appropriate handler based on type.

		Args:
				line (bytes): Complete message line to parse

		Note:
				Messages must include a 'type' field matching a RemoteMessageType enum value.
				Handler callbacks are executed asynchronously on the wx main thread.
				Invalid or unhandled message types are logged as errors.
		"""
		obj = self.serializer.deserialize(line)
		if "type" not in obj:
			log.warn("Received message without type: %r" % obj)
			return
		try:
			messageType = RemoteMessageType(obj["type"])
		except ValueError:
			log.warn("Received message with invalid type: %r" % obj)
			return
		del obj["type"]
		extensionPoint = self.inboundHandlers.get(messageType)
		if not extensionPoint:
			log.warn("Received message with unhandled type: %r %r", messageType, obj)
			return
		wx.CallAfter(extensionPoint.notify, **obj)

	def sendQueue(self) -> None:
		"""Background thread that processes the outbound message queue.

		Continuously pulls messages from the queue and sends them over the socket.
		Thread exits when None is received from the queue or a socket error occurs.

		Note:
				This method runs in a separate thread and handles thread-safe socket access
				using the serverSockLock.
		"""
		while True:
			item = self.queue.get()
			if item is None:
				return
			try:
				with self.serverSockLock:
					self.serverSock.sendall(item)
			except socket.error:
				return

	def send(self, type: str | Enum, **kwargs: Any) -> None:
		"""Send a message through the transport.

		Serializes and queues a message for transmission. Messages are sent
		asynchronously by the queue thread.

		Args:
				type (str|Enum): Message type, typically a RemoteMessageType enum value
				**kwargs: Message payload data to serialize

		Note:
				This method is thread-safe and can be called from any thread.
				If the transport is not connected, the message will be silently dropped.
		"""
		if self.connected:
			obj = self.serializer.serialize(type=type, **kwargs)
			self.queue.put(obj)
		else:
			log.error("Attempted to send message %r while not connected", type)

	def _disconnect(self) -> None:
		"""Internal method to disconnect the transport.

		Cleans up the send queue thread, empties queued messages,
		and closes the socket connection.

		Note:
				This is called internally on errors, unlike close() which is called
				explicitly to shut down the transport.
		"""
		"""Disconnect the transport due to an error, without closing the connector thread."""
		if self.queueThread is not None:
			self.queue.put(None)
			self.queueThread.join()
			self.queueThread = None
		clearQueue(self.queue)
		if self.serverSock:
			self.serverSock.close()
			self.serverSock = None

	def close(self):
		"""Close the transport."""
		self.transportClosing.notify()
		self.reconnectorThread.running = False
		self._disconnect()
		self.closed = True
		self.reconnectorThread = ConnectorThread(self)


class RelayTransport(TCPTransport):
	"""Transport for connecting through a relay server.

	Extends TCPTransport with relay-specific protocol handling for channels
	and connection types. Manages protocol versioning and channel joining.

	Args:
		serializer (Serializer): Message serializer instance
		address (Tuple[str, int]): Relay server address
		timeout (int, optional): Connection timeout. Defaults to 0.
		channel (Optional[str], optional): Channel to join. Defaults to None.
		connectionType (Optional[str], optional): Connection type. Defaults to None.
		protocol_version (int, optional): Protocol version. Defaults to PROTOCOL_VERSION.
		insecure (bool, optional): Skip certificate verification. Defaults to False.

	Attributes:
		channel (Optional[str]): Relay channel name
		connectionType (Optional[str]): Type of relay connection
		protocol_version (int): Protocol version to use
	"""

	channel: str | None
	connectionType: str | None
	protocol_version: int

	def __init__(
		self,
		serializer: Serializer,
		address: tuple[str, int],
		timeout: int = 0,
		channel: str | None = None,
		connectionType: str | None = None,
		protocol_version: int = PROTOCOL_VERSION,
		insecure: bool = False,
	) -> None:
		"""Initialize a new RelayTransport instance.

		Args:
			serializer: Serializer for encoding/decoding messages
			address: Tuple of (host, port) to connect to
			timeout: Connection timeout in seconds
			channel: Optional channel name to join
			connectionType: Optional connection type identifier
			protocol_version: Protocol version to use
			insecure: Whether to skip certificate verification
		"""
		super().__init__(
			address=address,
			serializer=serializer,
			timeout=timeout,
			insecure=insecure,
		)
		log.info("Connecting to %s channel %s" % (address, channel))
		self.channel = channel
		self.connectionType = connectionType
		self.protocol_version = protocol_version
		self.transportConnected.register(self.onConnected)

	@classmethod
	def create(cls, connection_info: ConnectionInfo, serializer: Serializer) -> "RelayTransport":
		"""Create a RelayTransport from a ConnectionInfo object.

		:param connection_info: ConnectionInfo instance containing connection details
		:type connection_info: ConnectionInfo
		:param serializer: Serializer instance for message encoding/decoding
		:type serializer: Serializer
		:return: Configured RelayTransport instance ready for connection
		:rtype: RelayTransport
		"""
		return cls(
			serializer=serializer,
			address=(connection_info.hostname, connection_info.port),
			channel=connection_info.key,
			connectionType=connection_info.mode,
			insecure=connection_info.insecure,
		)

	def onConnected(self) -> None:
		"""Handle successful connection to relay server.

		:note: Called automatically when transport connects:
		       - Sends protocol version
		       - Joins channel if specified
		       - Otherwise requests key generation
		"""
		self.send(RemoteMessageType.PROTOCOL_VERSION, version=self.protocol_version)
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

	:param connector: Transport instance to manage connections for
	:type connector: Transport
	:param reconnectDelay: Seconds between attempts, defaults to 5
	:type reconnectDelay: int, optional

	:ivar running: Whether thread should continue running
	:vartype running: bool
	:ivar connector: Transport to manage connections for
	:vartype connector: Transport
	:ivar reconnectDelay: Seconds to wait between connection attempts
	:vartype reconnectDelay: int
	"""

	running: bool
	connector: Transport
	reconnectDelay: int

	def __init__(self, connector: Transport, reconnectDelay: int = 5) -> None:
		super().__init__()
		self.reconnectDelay = reconnectDelay
		self.running = True
		self.connector = connector
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
		log.info("Ending control connector thread %s" % self.name)


def clearQueue(queue: Queue[bytes | None]) -> None:
	"""Empty all items from a queue without blocking.

	Removes all items from the queue in a non-blocking way,
	useful for cleaning up before disconnection.

	:param queue: Queue instance to clear
	:type queue: Queue[Optional[bytes]]
	:note: This function catches and ignores any exceptions that occur
	       while trying to get items from an empty queue.
	"""
	try:
		while True:
			queue.get_nowait()
	except Exception:
		pass
