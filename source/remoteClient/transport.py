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
from enum import Enum
from logging import getLogger
from queue import Queue
from typing import Any, Callable, Dict, Optional, Tuple, Union

from dataclasses import dataclass
import wx
from extensionPoints import Action, HandlerRegistrar

from . import configuration
from .connection_info import ConnectionInfo
from .protocol import PROTOCOL_VERSION, RemoteMessageType
from .serializer import Serializer
from .socket_utils import hostPortToAddress

log = getLogger("transport")


@dataclass
class RemoteExtensionPoint:
	"""Bridges local extension points to remote message sending.

	This class connects local NVDA extension points to the remote transport layer,
	allowing local events to trigger remote messages with optional argument transformation.

	Args:
		extensionPoint: The NVDA extension point to bridge
		messageType: The remote message type to send
		filter: Optional function to transform arguments before sending
		transport: The transport instance (set on registration)

	The filter function, if provided, should take (*args, **kwargs) and return
	a new kwargs dict to be sent in the message.
	"""

	extensionPoint: HandlerRegistrar
	messageType: RemoteMessageType
	filter: Optional[Callable[..., Dict[str, Any]]] = None
	transport: Optional["Transport"] = None

	def remoteBridge(self, *args: Any, **kwargs: Any) -> bool:
		"""Bridge function that gets registered to the extension point.

		Handles calling the filter if present and sending the message.
		Always returns True to allow other handlers to process the event.
		"""
		if self.filter:
			# Filter should transform args/kwargs into just the kwargs needed for the message
			kwargs = self.filter(*args, **kwargs)
		if self.transport:
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

	Args:
		serializer: The serializer instance to use for message encoding/decoding

	Attributes:
		connected (bool): True if transport has an active connection
		successful_connects (int): Counter of successful connection attempts
		connected_event (threading.Event): Event that is set when connected
		serializer (Serializer): The message serializer instance
		inboundHandlers (Dict[RemoteMessageType, Callable]): Registered message handlers

	Events:
		transportConnected: Fired after connection is established and ready
		transportDisconnected: Fired when existing connection is lost
		transportCertificateAuthenticationFailed: Fired when SSL certificate validation fails
		transportConnectionFailed: Fired when a connection attempt fails
		transportClosing: Fired before transport is shut down
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
		self.inboundHandlers: Dict[RemoteMessageType, Action] = {}
		self.outboundHandlers: Dict[RemoteMessageType, RemoteExtensionPoint] = {}
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

		Called internally when a connection is established. Updates connection state,
		increments successful connection counter, and notifies listeners.

		This method:
		1. Increments successful connection counter
		2. Sets connected flag to True
		3. Sets the connected event
		4. Notifies transportConnected listeners
		"""
		self.successfulConnects += 1
		self.connected = True
		self.connectedEvent.set()
		self.transportConnected.notify()

	def registerInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Register a handler for incoming messages of a specific type.

		Adds a callback function to handle messages of the specified RemoteMessageType.
		Multiple handlers can be registered for the same message type.

		Args:
				type (RemoteMessageType): The message type to handle
				handler (Callable): Callback function to process messages of this type.
						Will be called with the message payload as kwargs.

		Example:
				>>> def handle_keypress(key_code, pressed):
				...     print(f"Key {key_code} {'pressed' if pressed else 'released'}")
				>>> transport.registerInbound(RemoteMessageType.key_press, handle_keypress)

		Note:
				Handlers are called asynchronously on the wx main thread via wx.CallAfter
		"""
		if type not in self.inboundHandlers:
			log.debug("Creating new handler for %s", type)
			self.inboundHandlers[type] = Action()
		log.debug("Registering handler for %s", type)
		self.inboundHandlers[type].register(handler)

	def unregisterInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Remove a previously registered message handler.

		Removes a specific handler function from the list of handlers for a message type.
		If the handler was not previously registered, this is a no-op.

		Args:
				type (RemoteMessageType): The message type to unregister from
				handler (Callable): The handler function to remove
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

		Args:
			extensionPoint (HandlerRegistrar): The extension point to register
			messageType (RemoteMessageType): The message type to register the extension point to
			filter (Optional[Callable], optional): A filter function to apply to the message before sending. Defaults to None.
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

	Args:
		serializer (Serializer): Message serializer instance
		address (Tuple[str, int]): Remote address to connect to
		timeout (int, optional): Connection timeout in seconds. Defaults to 0.
		insecure (bool, optional): Skip certificate verification. Defaults to False.

	Attributes:
		buffer (bytes): Buffer for incomplete received data
		closed (bool): Whether transport is closed
		queue (Queue[Optional[bytes]]): Queue of outbound messages
		insecure (bool): Whether to skip certificate verification
		address (Tuple[str, int]): Remote address to connect to
		timeout (int): Connection timeout in seconds
		serverSock (Optional[ssl.SSLSocket]): The SSL socket connection
		serverSockLock (threading.Lock): Lock for thread-safe socket access
		queueThread (Optional[threading.Thread]): Thread handling outbound messages
		reconnectorThread (ConnectorThread): Thread managing reconnection
	"""

	buffer: bytes
	closed: bool
	queue: Queue[Optional[bytes]]
	insecure: bool
	serverSockLock: threading.Lock
	address: Tuple[str, int]
	serverSock: Optional[ssl.SSLSocket]
	queueThread: Optional[threading.Thread]
	timeout: int
	reconnectorThread: "ConnectorThread"
	lastFailFingerprint: Optional[str]

	def __init__(
		self,
		serializer: Serializer,
		address: Tuple[str, int],
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
	) -> ssl.SSLSocket:
		"""Create and configure an SSL socket for outbound connections.

		Creates a TCP socket with appropriate timeout and keep-alive settings,
		then wraps it with SSL/TLS encryption.

		Args:
				host (str): Remote hostname to connect to
				port (int): Remote port number
				insecure (bool, optional): Skip certificate verification. Defaults to False.

		Returns:
				ssl.SSLSocket: Configured SSL socket ready for connection

		Note:
				The socket is created but not yet connected. Call connect() separately.
		"""
		address = socket.getaddrinfo(host, port)[0]
		serverSock = socket.socket(*address[:3])
		if self.timeout:
			serverSock.settimeout(self.timeout)
		serverSock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		serverSock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60000, 2000))
		ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		if insecure:
			ctx.verify_mode = ssl.CERT_NONE
		ctx.check_hostname = not insecure
		ctx.load_default_certs()

		if insecure:
			log.warn("Skipping certificate verification for %s:%d", host, port)
		serverSock = ctx.wrap_socket(sock=serverSock, server_hostname=host)
		return serverSock

	def getpeercert(
		self,
		binary_form: bool = False,
	) -> Optional[Union[Dict[str, Any], bytes]]:
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

	channel: Optional[str]
	connectionType: Optional[str]
	protocol_version: int

	def __init__(
		self,
		serializer: Serializer,
		address: Tuple[str, int],
		timeout: int = 0,
		channel: Optional[str] = None,
		connectionType: Optional[str] = None,
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

		Args:
			connection_info: ConnectionInfo instance containing connection details
			serializer: Serializer instance for message encoding/decoding

		Returns:
			Configured RelayTransport instance ready for connection
		"""
		return cls(
			serializer=serializer,
			address=(connection_info.hostname, connection_info.port),
			channel=connection_info.key,
			connectionType=connection_info.mode.value,
			insecure=connection_info.insecure,
		)

	def onConnected(self) -> None:
		self.send(RemoteMessageType.protocol_version, version=self.protocol_version)
		if self.channel is not None:
			self.send(
				RemoteMessageType.join,
				channel=self.channel,
				connection_type=self.connectionType,
			)
		else:
			self.send(RemoteMessageType.generate_key)


class ConnectorThread(threading.Thread):
	"""Background thread that manages connection attempts.

	Handles automatic reconnection with configurable delay between attempts.
	Runs until explicitly stopped.

	Args:
		connector (Transport): Transport instance to manage connections for
		reconnectDelay (int, optional): Seconds between attempts. Defaults to 5.

	Attributes:
		running (bool): Whether thread should continue running
		connector (Transport): Transport to manage connections for
		reconnectDelay (int): Seconds to wait between connection attempts
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


def clearQueue(queue: Queue[Optional[bytes]]) -> None:
	"""Empty all items from a queue without blocking.

	Removes all items from the queue in a non-blocking way,
	useful for cleaning up before disconnection.

	Args:
		queue (Queue[Optional[bytes]]): Queue instance to clear

	Note:
		This function catches and ignores any exceptions that occur
		while trying to get items from an empty queue.
	"""
	try:
		while True:
			queue.get_nowait()
	except Exception:
		pass
