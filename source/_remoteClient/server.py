# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Server implementation for NVDA Remote relay functionality.

This module implements a relay server that enables NVDA Remote connections between
multiple clients. It provides:

- A secure SSL/TLS encrypted relay server
- Client authentication via channel password matching
- Message routing between connected clients
- Protocol version recording (clients declare their version)
- Connection monitoring with periodic one-way pings
- Separate IPv4 and IPv6 socket handling
- Dynamic certificate generation and management

The server creates separate IPv4 and IPv6 sockets but routes messages between all
connected clients regardless of IP version. Messages use JSON format and must be
newline-delimited. Invalid messages will cause client disconnection.

When clients disconnect or lose connection, the server automatically removes them and
notifies other connected clients of the departure.
"""

import os
import socket
import ssl
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from select import select
from itertools import count
from typing import Any, Final

import cffi  # noqa # required for cryptography
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from logHandler import log

from . import configuration
from .protocol import RemoteMessageType
from .secureDesktop import getProgramDataTempPath
from .serializer import JSONSerializer


class RemoteCertificateManager:
	"""Manages SSL certificates for the NVDA Remote relay server.

	:ivar certDir: Directory where certificates and keys are stored
	:ivar certPath: Path to the certificate file
	:ivar keyPath: Path to the private key file
	:ivar fingerprintPath: Path to the fingerprint file
	"""

	CERT_FILE = "NvdaRemoteRelay.pem"
	KEY_FILE = "NvdaRemoteRelay.key"
	FINGERPRINT_FILE = "NvdaRemoteRelay.fingerprint"
	CERT_DURATION_DAYS = 365
	CERT_RENEWAL_THRESHOLD_DAYS = 30

	def __init__(self, certDir: Path | None = None):
		"""Initialize the certificate manager.

		:param certDir: Directory to store certificate files, defaults to program data temp path
		"""
		self.certDir: Path = certDir or getProgramDataTempPath()
		self.certPath: Path = self.certDir / self.CERT_FILE
		self.keyPath: Path = self.certDir / self.KEY_FILE
		self.fingerprintPath: Path = self.certDir / self.FINGERPRINT_FILE

	def ensureValidCertExists(self) -> None:
		"""Ensures a valid certificate and key exist, regenerating if needed."""
		log.info("Checking certificate validity")
		os.makedirs(self.certDir, exist_ok=True)

		if self._filesExist():
			try:
				self._validateCertificate()
				return
			except Exception as e:
				log.warning(f"Certificate validation failed: {e}", exc_info=True)

		self._generateSelfSignedCert()

	def _filesExist(self) -> bool:
		"""Check if both certificate and key files exist."""
		return self.certPath.is_file() and self.keyPath.is_file()

	def _validateCertificate(self) -> None:
		"""Validates the existing certificate and key.

		:raises ValueError: If the current date/time is outside the certificate's validity period, or if the certificate is approaching expiration.
		:raises OSError: If the certificate or private key files cannot be opened.
		:raises ValueError: If the private key data cannot be decoded.
		:raises TypeError: If the private key is encrypted.
		"""
		# Load and validate certificate
		with open(self.certPath, "rb") as f:
			certData = f.read()
			cert = x509.load_pem_x509_certificate(certData)

		# Check validity period
		now = datetime.now(timezone.utc)
		if not (cert.not_valid_before_utc < now <= cert.not_valid_after_utc):
			raise ValueError("Certificate is not within its validity period")

		# Check renewal threshold
		timeRemaining = cert.not_valid_after_utc - now
		if timeRemaining.days <= self.CERT_RENEWAL_THRESHOLD_DAYS:
			raise ValueError("Certificate is approaching expiration")

		# Verify private key can be loaded
		with open(self.keyPath, "rb") as f:
			serialization.load_pem_private_key(f.read(), password=None)

	def _generateSelfSignedCert(self) -> None:
		"""Generates a self-signed certificate and private key."""
		privateKey = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
		)

		subject = issuer = x509.Name(
			[
				x509.NameAttribute(NameOID.COMMON_NAME, "NVDA Remote Access Service"),
				x509.NameAttribute(NameOID.ORGANIZATION_NAME, "NV Access"),
			],
		)

		now = datetime.now(timezone.utc)
		cert = (
			x509.CertificateBuilder()
			.subject_name(
				subject,
			)
			.issuer_name(
				issuer,
			)
			.public_key(
				privateKey.public_key(),
			)
			.serial_number(
				x509.random_serial_number(),
			)
			.not_valid_before(
				now,
			)
			.not_valid_after(
				now + timedelta(days=self.CERT_DURATION_DAYS),
			)
			.add_extension(
				x509.BasicConstraints(ca=True, path_length=None),
				critical=True,
			)
			.add_extension(
				x509.SubjectAlternativeName(
					[
						x509.DNSName("localhost"),
					],
				),
				critical=False,
			)
			.sign(privateKey, hashes.SHA256())
		)

		# Calculate fingerprint
		fingerprint = cert.fingerprint(hashes.SHA256()).hex()
		# Write private key
		with open(self.keyPath, "wb") as f:
			f.write(
				privateKey.private_bytes(
					encoding=serialization.Encoding.PEM,
					format=serialization.PrivateFormat.PKCS8,
					encryption_algorithm=serialization.NoEncryption(),
				),
			)

		# Write certificate
		with open(self.certPath, "wb") as f:
			f.write(cert.public_bytes(serialization.Encoding.PEM))

		# Save fingerprint
		with open(self.fingerprintPath, "w") as f:
			f.write(fingerprint)

		# Add to trusted certificates in config
		config = configuration.getRemoteConfig()
		if "trustedCertificates" not in config:
			config["trustedCertificates"] = {}
		config["trustedCertificates"]["localhost"] = fingerprint
		config["trustedCertificates"]["127.0.0.1"] = fingerprint

		log.info(f"Generated new self-signed certificate for NVDA Remote. Fingerprint: {fingerprint}")

	def getCurrentFingerprint(self) -> str | None:
		"""Get the fingerprint of the current certificate."""
		try:
			if self.fingerprintPath.is_file():
				with open(self.fingerprintPath, "r") as f:
					return f.read().strip()
		except Exception as e:
			log.warning(f"Error reading fingerprint: {e}", exc_info=True)
		return None

	def createSSLContext(self) -> ssl.SSLContext:
		"""Creates an SSL context using the certificate and key."""
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		# Load our certificate and private key
		context.load_cert_chain(
			certfile=str(self.certPath),
			keyfile=str(self.keyPath),
		)
		# Trust our own CA for server verification
		context.load_verify_locations(cafile=str(self.certPath))
		# Require client cert verification
		context.verify_mode = ssl.CERT_NONE  # Don't require client certificates
		context.check_hostname = False  # Don't verify hostname since we're using self-signed certs
		return context


class LocalRelayServer:
	"""Secure relay server for NVDA Remote connections.

	Accepts encrypted connections from NVDA Remote clients and routes messages between them.
	Creates IPv4 and IPv6 listening sockets using SSL/TLS encryption.
	Uses select() for non-blocking I/O and monitors connection health with periodic pings.

	Clients must authenticate by providing the correct channel password in their join message
	before they can exchange messages. Both IPv4 and IPv6 clients share the same channel
	and can interact with each other transparently.

	:ivar port: Port number to listen on
	:ivar password: Channel password for client authentication
	:ivar clients: Dictionary mapping sockets to Client objects
	:ivar clientSockets: List of client sockets
	:ivar PING_TIME_SECONDS: Seconds between ping messages
	"""

	PING_TIME_SECONDS: int = 300
	SELECT_TIMEOUT_SECONDS: Final[int] = 60

	def __init__(
		self,
		port: int,
		password: str,
		bindHost: str = "",
		bindHost6: str = "[::]:",
		certDir: Path | None = None,
	):
		"""Initialize the relay server.

		:param port: Port number to listen on
		:param password: Channel password for client authentication
		:param bindHost: IPv4 address to bind to, defaults to all interfaces
		:param bindHost6: IPv6 address to bind to, defaults to all interfaces
		:param certDir: Directory to store certificate files, defaults to None
		"""
		self.port = port
		self.password = password
		self.certManager = RemoteCertificateManager(certDir)
		self.certManager.ensureValidCertExists()

		# Initialize other server components
		self.serializer = JSONSerializer()
		self.clients: dict[socket.socket, Client] = {}
		self.clientSockets: list[socket.socket] = []
		self._running = False
		self.lastPingTime = 0

		# Create server sockets
		self.serverSocket = self.createServerSocket(
			socket.AF_INET,
			socket.SOCK_STREAM,
			bindAddress=(bindHost, self.port),
		)
		self.serverSocket6 = self.createServerSocket(
			socket.AF_INET6,
			socket.SOCK_STREAM,
			bindAddress=(bindHost6, self.port),
		)

	def createServerSocket(self, family: int, type: int, bindAddress: tuple[str, int]) -> ssl.SSLSocket:
		"""Creates an SSL wrapped socket using the certificate.

		:param family: Socket address family (AF_INET or AF_INET6)
		:param type: Socket type (typically SOCK_STREAM)
		:param bindAddress: Tuple of (host, port) to bind to
		:return: SSL wrapped server socket
		:raises socket.error: If socket creation or binding fails
		"""
		serverSocket = socket.socket(family, type)
		sslContext = self.certManager.createSSLContext()
		serverSocket = sslContext.wrap_socket(serverSocket, server_side=True)
		serverSocket.bind(bindAddress)
		serverSocket.listen(5)  # Set the maximum number of queued connections
		return serverSocket

	def run(self) -> None:
		"""Main server loop that handles client connections and message routing.

		Continuously accepts new connections and processes messages from connected clients.
		Sends periodic ping messages to maintain connection health.

		:raises socket.error: If there are socket communication errors
		"""
		log.info(f"Starting NVDA Remote relay server on port {self.port}")
		self._running = True
		self.lastPingTime = time.time()
		while self._running:
			read, write, error = select(
				self.clientSockets + [self.serverSocket, self.serverSocket6],
				[],
				self.clientSockets,
				self.SELECT_TIMEOUT_SECONDS,
			)
			if not self._running:
				break
			for sock in read:
				if sock is self.serverSocket or sock is self.serverSocket6:
					self.acceptNewConnection(sock)
					continue
				self.clients[sock].handleData()
			if time.time() - self.lastPingTime >= self.PING_TIME_SECONDS:
				for client in self.clients.values():
					if client.authenticated:
						client.send(type=RemoteMessageType.PING)
				self.lastPingTime = time.time()

	def acceptNewConnection(self, sock: ssl.SSLSocket) -> None:
		"""Accept and set up a new client connection."""
		try:
			clientSock, addr = sock.accept()
			log.info(f"New client connection from {addr}")
		except (ssl.SSLError, socket.error, OSError):
			log.error("Error accepting connection", exc_info=True)
			return
		# Disable Nagle's algorithm so that packets are always sent immediately.
		clientSock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		client = Client(server=self, socket=clientSock)
		self.addClient(client)

	def addClient(self, client: "Client") -> None:
		"""Add a new client to the server."""
		self.clients[client.socket] = client
		self.clientSockets.append(client.socket)

	def removeClient(self, client: "Client") -> None:
		"""Remove a client from the server."""
		del self.clients[client.socket]
		self.clientSockets.remove(client.socket)

	def clientDisconnected(self, client: "Client") -> None:
		"""Handle client disconnection and notify other clients."""
		log.info(f"Client {client.id} disconnected")
		self.removeClient(client)
		if client.authenticated:
			client.sendToOthers(
				type=RemoteMessageType.CLIENT_LEFT,
				user_id=client.id,
				client=client.asDict(),
			)

	def close(self) -> None:
		"""Shut down the server and close all connections."""
		log.info("Shutting down NVDA Remote relay server")
		self._running = False
		self.serverSocket.close()
		self.serverSocket6.close()
		log.info("Server shutdown complete")


class Client:
	"""Handles a single connected NVDA Remote client.

	Processes incoming messages, handles authentication via channel password,
	records client protocol version, and routes messages to other connected clients.
	Maintains a buffer of received data and processes complete messages delimited
	by newlines.

	:ivar id: Unique client identifier
	:ivar socket: SSL socket for this client connection
	:ivar buffer: Buffer for incomplete received data
	:ivar authenticated: Whether client has authenticated successfully
	:ivar connectionType: Type of client connection
	:ivar protocolVersion: Client protocol version number
	"""

	_idCounter = count(1)

	def __init__(self, server: LocalRelayServer, socket: ssl.SSLSocket) -> None:
		"""Initialize a client connection.

		:param server: The relay server instance this client belongs to
		:param socket: The SSL socket for this client connection
		"""
		self.server: LocalRelayServer = server
		self.socket: ssl.SSLSocket = socket
		self.buffer: bytes = b""
		self.serializer: JSONSerializer = server.serializer
		self.authenticated: bool = False
		self.id: int = next(self._idCounter)
		self.connectionType: str | None = None
		self.protocolVersion: int = 1

	def handleData(self) -> None:
		"""Process incoming data from the client socket."""
		sockData = b""
		try:
			sockData = self.socket.recv(16384)
		except Exception:
			self.close()
			return
		if not sockData:  # Disconnect
			self.close()
			return
		data = self.buffer + sockData
		if b"\n" not in data:
			self.buffer = data
			return
		self.buffer = b""
		while b"\n" in data:
			line, sep, data = data.partition(b"\n")
			try:
				self.parse(line)
			except ValueError:
				log.error(f"Error parsing message from client {self.id}", exc_info=True)
				self.close()
				return
		self.buffer += data

	def parse(self, line: bytes) -> None:
		"""Parse and handle an incoming message line."""
		parsed = self.serializer.deserialize(line)
		if "type" not in parsed:
			return
		if self.authenticated:
			self.sendToOthers(**parsed)
			return
		fn = "do_" + parsed["type"]
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def asDict(self) -> dict[str, Any]:
		"""Get client information as a dictionary."""
		return dict(id=self.id, connection_type=self.connectionType)

	def do_join(self, obj: dict[str, Any]) -> None:
		"""Handle client join request and authentication."""
		password = obj.get("channel", None)
		if password != self.server.password:
			log.warning("Client %s sent incorrect password", self.id)
			self.send(
				type=RemoteMessageType.ERROR,
				message="incorrect_password",
			)
			self.close()
			return
		self.connectionType = obj.get("connection_type")
		self.authenticated = True
		log.info(f"Client {self.id} authenticated successfully (connection type: {self.connectionType})")
		clients = []
		clientIds = []
		for client in list(self.server.clients.values()):
			if client is self or not client.authenticated:
				continue
			clients.append(client.asDict())
			clientIds.append(client.id)
		self.send(
			type=RemoteMessageType.CHANNEL_JOINED,
			channel=self.server.password,
			user_ids=clientIds,
			clients=clients,
		)
		self.sendToOthers(
			type=RemoteMessageType.CLIENT_JOINED,
			user_id=self.id,
			client=self.asDict(),
		)

	def do_protocol_version(self, obj: dict[str, Any]) -> None:
		"""Record client's protocol version."""
		version = obj.get("version")
		if not version:
			return
		self.protocolVersion = version

	def close(self) -> None:
		"""Close the client connection."""
		self.socket.close()
		self.server.clientDisconnected(self)

	def send(
		self,
		type: str | RemoteMessageType,
		origin: int | None = None,
		clients: list[dict[str, Any]] | None = None,
		client: dict[str, Any] | None = None,
		**kwargs: Any,
	) -> None:
		"""Send a message to this client.

		:param type: Message type
		:param origin: Originating client ID
		:param clients: List of connected clients
		:param client: Client information

		:note: Additional keyword arguments are included in the message data.
		"""
		msg = kwargs
		if self.protocolVersion > 1:
			if origin:
				msg["origin"] = origin
			if clients:
				msg["clients"] = clients
			if client:
				msg["client"] = client
		try:
			data = self.serializer.serialize(type=type, **msg)
			self.socket.sendall(data)
		except Exception:
			log.error(f"Error sending message to client {self.id}", exc_info=True)
			self.close()

	def sendToOthers(self, origin: int | None = None, **payload: Any) -> None:
		"""Send a message to all other authenticated clients.

		:param origin: Originating client ID
		:param payload: Message data
		"""

		if origin is None:
			origin = self.id
		for c in self.server.clients.values():
			if c is not self and c.authenticated:
				c.send(origin=origin, **payload)
