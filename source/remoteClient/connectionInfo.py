# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from . import protocol
from .protocol import SERVER_PORT, URL_PREFIX


class URLParsingError(Exception):
	"""Exception raised when URL parsing fails.

	Raised when the URL cannot be parsed due to missing or invalid components
	such as hostname, key, or mode.

	:raises URLParsingError: When URL components are missing or invalid
	"""


class ConnectionMode(StrEnum):
	"""Defines the connection mode for remote connections.

	:cvar LEADER: Controller mode for controlling the remote system
	:cvar FOLLOWER: Controlled mode for being controlled by remote system
	"""

	LEADER = "master"
	FOLLOWER = "slave"


class ConnectionState(StrEnum):
	"""Defines possible states of a remote connection.

	:cvar CONNECTED: Connection is established and active
	:cvar DISCONNECTED: No active connection exists
	:cvar CONNECTING: Connection attempt is currently in progress
	:cvar DISCONNECTING: Connection termination is in progress
	"""

	CONNECTED = "connected"
	DISCONNECTED = "disconnected"
	CONNECTING = "connecting"
	DISCONNECTING = "disconnecting"


@dataclass
class ConnectionInfo:
	"""Stores and manages remote connection information.

	Handles connection details including hostname, mode, authentication key,
	port number and security settings. Provides methods for URL generation and parsing.

	:param hostname: Remote host address to connect to
	:param mode: Connection mode (leader/follower)
	:param key: Authentication key for securing the connection
	:param port: Port number to use for connection, defaults to SERVER_PORT
	:param insecure: Allow insecure connections without SSL/TLS, defaults to False
	:raises URLParsingError: When URL components are missing or invalid
	:return: A ConnectionInfo instance with the specified connection details
	:rtype: ConnectionInfo
	"""

	hostname: str
	mode: ConnectionMode
	key: str
	port: int = SERVER_PORT
	insecure: bool = False

	def __post_init__(self) -> None:
		self.port = self.port or SERVER_PORT
		self.mode = ConnectionMode(self.mode)

	@classmethod
	def fromURL(cls, url: str) -> "ConnectionInfo":
		"""Creates a ConnectionInfo instance from a URL string.

		:param url: The URL to parse in nvdaremote:// format
		:raises URLParsingError: If URL cannot be parsed or contains invalid data
		:return: A new ConnectionInfo instance configured from the URL
		:rtype: ConnectionInfo
		"""
		parsedUrl = urlparse(url)
		parsedQuery = parse_qs(parsedUrl.query)
		hostname = parsedUrl.hostname
		port = parsedUrl.port
		key = parsedQuery.get("key", [""])[0]
		mode = parsedQuery.get("mode", [""])[0].lower()
		insecure = parsedQuery.get("insecure", ["false"])[0].lower() == "true"
		if not hostname:
			raise URLParsingError("No hostname provided")
		if not key:
			raise URLParsingError("No key provided")
		if not mode:
			raise URLParsingError("No mode provided")
		try:
			ConnectionMode(mode)
		except ValueError:
			raise URLParsingError("Invalid mode provided: %r" % mode)
		return cls(hostname=hostname, mode=mode, key=key, port=port, insecure=insecure)

	def getAddress(self) -> str:
		"""Gets the formatted address string.

		:return: Address string in format hostname:port, with IPv6 brackets if needed
		:rtype: str
		"""
		# Handle IPv6 addresses by adding brackets if needed
		hostname = f"[{self.hostname}]" if ":" in self.hostname else self.hostname
		return f"{hostname}:{self.port}"

	def _build_url(self, mode: ConnectionMode) -> str:
		"""Builds a URL string for the given mode.

		:param mode: The connection mode to use in the URL
		:return: Complete URL string
		"""
		# Build URL components
		netloc = protocol.hostPortToAddress((self.hostname, self.port))
		params = {
			"key": self.key,
			"mode": mode,
		}
		if self.insecure:
			params["insecure"] = "true"
		query = urlencode(params)

		# Use urlunparse for proper URL construction
		return urlunparse(
			(
				URL_PREFIX.split("://")[0],  # scheme from URL_PREFIX
				netloc,  # network location
				"",  # path
				"",  # params
				query,  # query string
				"",  # fragment
			),
		)

	def getURLToConnect(self) -> str:
		"""Gets a URL for connecting with reversed mode.

		:return: URL string with opposite connection mode
		"""
		# Flip leader/follower for connection URL
		connect_mode = (
			ConnectionMode.FOLLOWER if self.mode == ConnectionMode.LEADER else ConnectionMode.LEADER
		)
		return self._build_url(connect_mode)

	def getURL(self) -> str:
		"""Gets the URL representation of the current connection info.

		:return: URL string with current connection mode
		"""
		return self._build_url(self.mode)
