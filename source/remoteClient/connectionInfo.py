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
	"""Raised if it's impossible to parse out the URL"""


class ConnectionMode(StrEnum):
	MASTER = "master"
	SLAVE = "slave"


class ConnectionState(StrEnum):
	CONNECTED = "connected"
	DISCONNECTED = "disconnected"
	CONNECTING = "connecting"
	DISCONNECTING = "disconnecting"


@dataclass
class ConnectionInfo:
	hostname: str
	mode: ConnectionMode
	key: str
	port: int = SERVER_PORT
	insecure: bool = False

	def __post_init__(self):
		self.port = self.port or SERVER_PORT
		self.mode = ConnectionMode(self.mode)

	@classmethod
	def fromURL(cls, url):
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

	def getAddress(self):
		# Handle IPv6 addresses by adding brackets if needed
		hostname = f"[{self.hostname}]" if ":" in self.hostname else self.hostname
		return f"{hostname}:{self.port}"

	def _build_url(self, mode: ConnectionMode):
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

	def getURLToConnect(self):
		# Flip master/slave for connection URL
		connect_mode = ConnectionMode.SLAVE if self.mode == ConnectionMode.MASTER else ConnectionMode.MASTER
		return self._build_url(connect_mode)

	def getURL(self):
		return self._build_url(self.mode)
