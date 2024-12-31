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

import logging
import os
import socket
import ssl
import time
import cffi  # noqa # required for cryptography
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from select import select
from typing import Any, Dict, List, Optional, Tuple

from .protocol import RemoteMessageType
from .serializer import JSONSerializer
from .secureDesktop import getProgramDataTempPath

logger = logging.getLogger(__name__)


class RemoteCertificateManager:
	"""Manages SSL certificates for the NVDA Remote relay server."""

	CERT_FILE = "NvdaRemoteRelay.pem"
	KEY_FILE = "NvdaRemoteRelay.key"
	CERT_DURATION_DAYS = 365
	CERT_RENEWAL_THRESHOLD_DAYS = 30

	def __init__(self, cert_dir: Optional[Path] = None):
		self.cert_dir = cert_dir or getProgramDataTempPath()
		self.cert_path = self.cert_dir / self.CERT_FILE
		self.key_path = self.cert_dir / self.KEY_FILE

	def ensureValidCertExists(self) -> None:
		"""Ensures a valid certificate and key exist, regenerating if needed."""
		os.makedirs(self.cert_dir, exist_ok=True)

		should_generate = False
		if not self._filesExist():
			should_generate = True
		else:
			try:
				self._validateCertificate()
			except Exception as e:
				logging.warning(f"Certificate validation failed: {e}")
				should_generate = True

		if should_generate:
			self._generateSelfSignedCert()

	def _filesExist(self) -> bool:
		"""Check if both certificate and key files exist."""
		return self.cert_path.exists() and self.key_path.exists()

	def _validateCertificate(self) -> None:
		"""Validates the existing certificate and key."""
		# Load and validate certificate
		with open(self.cert_path, "rb") as f:
			cert_data = f.read()
			cert = x509.load_pem_x509_certificate(cert_data)

		# Check validity period
		now = datetime.utcnow()
		if now >= cert.not_valid_after or now < cert.not_valid_before:
			raise ValueError("Certificate is not within its validity period")

		# Check renewal threshold
		time_remaining = cert.not_valid_after - now
		if time_remaining.days <= self.CERT_RENEWAL_THRESHOLD_DAYS:
			raise ValueError("Certificate is approaching expiration")

		# Verify private key can be loaded
		with open(self.key_path, "rb") as f:
			serialization.load_pem_private_key(f.read(), password=None)

	def _generateSelfSignedCert(self) -> None:
		"""Generates a self-signed certificate and private key."""
		private_key = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
		)

		subject = issuer = x509.Name(
			[
				x509.NameAttribute(NameOID.COMMON_NAME, "NVDARemote Relay"),
				x509.NameAttribute(NameOID.ORGANIZATION_NAME, "NVDARemote"),
			],
		)

		cert = (
			x509.CertificateBuilder()
			.subject_name(
				subject,
			)
			.issuer_name(
				issuer,
			)
			.public_key(
				private_key.public_key(),
			)
			.serial_number(
				x509.random_serial_number(),
			)
			.not_valid_before(
				datetime.utcnow(),
			)
			.not_valid_after(
				datetime.utcnow() + timedelta(days=self.CERT_DURATION_DAYS),
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
			.sign(private_key, hashes.SHA256())
		)

		# Write private key
		with open(self.key_path, "wb") as f:
			f.write(
				private_key.private_bytes(
					encoding=serialization.Encoding.PEM,
					format=serialization.PrivateFormat.PKCS8,
					encryption_algorithm=serialization.NoEncryption(),
				),
			)

		# Write certificate
		with open(self.cert_path, "wb") as f:
			f.write(cert.public_bytes(serialization.Encoding.PEM))

		logging.info("Generated new self-signed certificate for NVDA Remote")

	def createSSLContext(self) -> ssl.SSLContext:
		"""Creates an SSL context using the certificate and key."""
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		context.load_cert_chain(
			certfile=str(self.cert_path),
			keyfile=str(self.key_path),
		)
		return context


class LocalRelayServer:
	"""Secure relay server for NVDA Remote connections.

	Accepts encrypted connections from NVDA Remote clients and routes messages between them.
	Creates IPv4 and IPv6 listening sockets using SSL/TLS encryption.
	Uses select() for non-blocking I/O and monitors connection health with periodic pings
	(sent every PING_TIME seconds, no response expected).

	Clients must authenticate by providing the correct channel password in their join message
	before they can exchange messages. Both IPv4 and IPv6 clients share the same channel
	and can interact with each other transparently.
	"""

	PING_TIME: int = 300

	def __init__(
		self,
		port: int,
		password: str,
		bind_host: str = "",
		bind_host6: str = "[::]:",
		cert_dir: Optional[Path] = None,
	):
		self.port = port
		self.password = password
		self.cert_manager = RemoteCertificateManager(cert_dir)
		self.cert_manager.ensureValidCertExists()

		# Initialize other server components
		self.serializer = JSONSerializer()
		self.clients: Dict[socket.socket, Client] = {}
		self.clientSockets: List[socket.socket] = []
		self._running = False
		self.lastPingTime = 0

		# Create server sockets
		self.serverSocket = self.createServerSocket(
			socket.AF_INET,
			socket.SOCK_STREAM,
			bind_addr=(bind_host, self.port),
		)
		self.serverSocket6 = self.createServerSocket(
			socket.AF_INET6,
			socket.SOCK_STREAM,
			bind_addr=(bind_host6, self.port),
		)

	def createServerSocket(self, family: int, type: int, bind_addr: Tuple[str, int]) -> ssl.SSLSocket:
		"""Creates an SSL wrapped socket using the certificate."""
		serverSocket = socket.socket(family, type)
		ssl_context = self.cert_manager.createSSLContext()
		serverSocket = ssl_context.wrap_socket(serverSocket)
		serverSocket.bind(bind_addr)
		serverSocket.listen(5)
		return serverSocket

	def run(self) -> None:
		"""Main server loop that handles client connections and message routing."""
		self._running = True
		self.lastPingTime = time.time()
		while self._running:
			r, w, e = select(
				self.clientSockets + [self.serverSocket, self.serverSocket6],
				[],
				self.clientSockets,
				60,
			)
			if not self._running:
				break
			for sock in r:
				if sock is self.serverSocket or sock is self.serverSocket6:
					self.acceptNewConnection(sock)
					continue
				self.clients[sock].handleData()
			if time.time() - self.lastPingTime >= self.PING_TIME:
				for client in self.clients.values():
					if client.authenticated:
						client.send(type=RemoteMessageType.ping)
				self.lastPingTime = time.time()

	def acceptNewConnection(self, sock: ssl.SSLSocket) -> None:
		"""Accept and set up a new client connection."""
		try:
			clientSock, addr = sock.accept()
		except (ssl.SSLError, socket.error, OSError):
			logger.exception("Error accepting connection")
			return
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
		self.removeClient(client)
		if client.authenticated:
			client.send_to_others(
				type="client_left",
				user_id=client.id,
				client=client.asDict(),
			)

	def close(self) -> None:
		"""Shut down the server and close all connections."""
		self._running = False
		self.serverSocket.close()
		self.serverSocket6.close()


class Client:
	"""Handles a single connected NVDA Remote client.

	Processes incoming messages, handles authentication via channel password,
	records client protocol version, and routes messages to other connected clients.
	Maintains a buffer of received data and processes complete messages delimited
	by newlines.
	"""

	id: int = 0

	def __init__(self, server: LocalRelayServer, socket: ssl.SSLSocket):
		self.server = server
		self.socket = socket
		self.buffer = b""
		self.serializer = server.serializer
		self.authenticated = False
		self.id = Client.id + 1
		self.connectionType = None
		self.protocolVersion = 1
		Client.id += 1

	def handleData(self) -> None:
		"""Process incoming data from the client socket."""
		sock_data = b""
		try:
			sock_data = self.socket.recv(16384)
		except Exception:
			self.close()
			return
		if not sock_data:  # Disconnect
			self.close()
			return
		data = self.buffer + sock_data
		if b"\n" not in data:
			self.buffer = data
			return
		self.buffer = b""
		while b"\n" in data:
			line, sep, data = data.partition(b"\n")
			try:
				self.parse(line)
			except ValueError:
				logger.exception("Error parsing line")
				self.close()
				return
		self.buffer += data

	def parse(self, line: bytes) -> None:
		"""Parse and handle an incoming message line."""
		parsed = self.serializer.deserialize(line)
		if "type" not in parsed:
			return
		if self.authenticated:
			self.send_to_others(**parsed)
			return
		fn = "do_" + parsed["type"]
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def asDict(self) -> Dict[str, Any]:
		"""Get client information as a dictionary."""
		return dict(id=self.id, connection_type=self.connectionType)

	def do_join(self, obj: Dict[str, Any]) -> None:
		"""Handle client join request and authentication."""
		password = obj.get("channel", None)
		if password != self.server.password:
			self.send(
				type=RemoteMessageType.error,
				message="incorrect_password",
			)
			self.close()
			return
		self.connectionType = obj.get("connection_type")
		self.authenticated = True
		clients = []
		client_ids = []
		for c in list(self.server.clients.values()):
			if c is self or not c.authenticated:
				continue
			clients.append(c.asDict())
			client_ids.append(c.id)
		self.send(
			type=RemoteMessageType.channel_joined,
			channel=self.server.password,
			user_ids=client_ids,
			clients=clients,
		)
		self.send_to_others(
			type="client_joined",
			user_id=self.id,
			client=self.asDict(),
		)

	def do_protocol_version(self, obj: Dict[str, Any]) -> None:
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
		type: str | Enum,
		origin: Optional[int] = None,
		clients: Optional[List[Dict[str, Any]]] = None,
		client: Optional[Dict[str, Any]] = None,
		**kwargs: Any,
	) -> None:
		"""Send a message to this client."""
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
			self.close()

	def send_to_others(self, origin: Optional[int] = None, **obj: Any) -> None:
		"""Send a message to all other authenticated clients."""
		if origin is None:
			origin = self.id
		for c in self.server.clients.values():
			if c is not self and c.authenticated:
				c.send(origin=origin, **obj)
