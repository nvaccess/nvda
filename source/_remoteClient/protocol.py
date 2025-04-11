# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import urllib.parse
from enum import StrEnum

PROTOCOL_VERSION: int = 2


class RemoteMessageType(StrEnum):
	# Connection and Protocol Messages
	PROTOCOL_VERSION = "protocol_version"
	JOIN = "join"
	CHANNEL_JOINED = "channel_joined"
	CLIENT_JOINED = "client_joined"
	CLIENT_LEFT = "client_left"
	GENERATE_KEY = "generate_key"

	# Control Messages
	KEY = "key"
	SPEAK = "speak"
	CANCEL = "cancel"
	PAUSE_SPEECH = "pause_speech"
	TONE = "tone"
	WAVE = "wave"
	SEND_SAS = "send_SAS"  # Send Secure Attention Sequence
	INDEX = "index"

	# Display and Braille Messages
	DISPLAY = "display"
	BRAILLE_INPUT = "braille_input"
	SET_BRAILLE_INFO = "set_braille_info"
	SET_DISPLAY_SIZE = "set_display_size"

	# Clipboard Operations
	SET_CLIPBOARD_TEXT = "set_clipboard_text"

	# System Messages
	MOTD = "motd"
	VERSION_MISMATCH = "version_mismatch"
	PING = "ping"
	ERROR = "error"
	NVDA_NOT_CONNECTED = (
		"nvda_not_connected"  # This was added in version 2 but never implemented on the server
	)


SERVER_PORT = 6837
URL_PREFIX = "nvdaremote://"


def addressToHostPort(addr) -> tuple:
	"""Converts an address such as google.com:80 into a tuple of (address, port).
	If no port is given, use SERVER_PORT.
	"""
	addr = urllib.parse.urlparse("//" + addr)
	port = addr.port or SERVER_PORT
	return (addr.hostname, port)


def hostPortToAddress(hostPort: tuple) -> str:
	"""Converts a tuple of (address, port) into a string such as google.com:80.
	If the port is SERVER_PORT, it is omitted
	"""
	host, port = hostPort
	if ":" in host:
		host = f"[{host}]"
	if port != SERVER_PORT:
		return f"{host}:{port}"
	return host
