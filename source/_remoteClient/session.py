# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""NVDA Remote session management and message routing.

Implements the session layer for NVDA Remote, handling message routing,
connection roles, and NVDA feature coordination between instances.

Core Operation:
-------------
1. Transport layer delivers typed messages (RemoteMessageType)
2. Session routes messages to registered handlers
3. Handlers execute on wx main thread via CallAfter
4. Results flow back through transport layer

Connection Roles:
--------------
Leader (Controlling)
	- Captures and forwards input
	- Receives remote output (speech/braille)
	- Manages connection state
	- Patches input handling

Follower (Controlled)
	- Executes received commands
	- Forwards output to leader(s)
	- Tracks connected leaders
	- Patches output handling

Key Components:
------------
:class:`RemoteSession`
	Base session managing shared functionality:
	- Message handler registration
	- Connection validation
	- Version compatibility
	- MOTD handling

:class:`LeaderSession`
	Controls remote instance:
	- Input capture/forwarding
	- Remote output reception
	- Connection management
	- Leader-specific patches

:class:`FollowerSession`
	Controlled by remote instance:
	- Command execution
	- Output forwarding
	- Multi-leader support
	- Follower-specific patches

Thread Safety:
------------
All message handlers execute on wx main thread via CallAfter
to ensure thread-safe NVDA operations.

See Also:
	transport.py: Network communication
	local_machine.py: NVDA interface
"""

from collections.abc import Collection
import hashlib
import json
from collections import defaultdict
from extensionPoints import Action
from typing import Any, Final

import braille
import brailleInput
import gui
import inputCore
import scriptHandler
import speech
import speech.commands
import tones
import ui
from logHandler import log
from nvwave import decide_playWaveFile
from speech.extensions import post_speechPaused, pre_speechQueued, speechCanceled

from . import configuration, connectionInfo, cues
from .e2e import E2ESession
from .localMachine import LocalMachine
from .protocol import RemoteMessageType
from .serializer import SpeechCommandJSONEncoder, asSequence
from .transport import RelayTransport

EXCLUDED_SPEECH_COMMANDS = (
	speech.commands.BaseCallbackCommand,
	# _CancellableSpeechCommands are not designed to be reported and are used internally by NVDA. (#230)
	speech.commands._CancellableSpeechCommand,
)

#: Control-plane message types that must NOT be encrypted — the server needs to parse these.
#: All other message types (including any added by extensions) are encrypted when E2E is active.
_E2E_CONTROL_PLANE_TYPES: frozenset[RemoteMessageType] = frozenset(
	{
		RemoteMessageType.PROTOCOL_VERSION,
		RemoteMessageType.JOIN,
		RemoteMessageType.CHANNEL_JOINED,
		RemoteMessageType.CLIENT_JOINED,
		RemoteMessageType.CLIENT_LEFT,
		RemoteMessageType.GENERATE_KEY,
		RemoteMessageType.MOTD,
		RemoteMessageType.VERSION_MISMATCH,
		RemoteMessageType.PING,
		RemoteMessageType.ERROR,
		RemoteMessageType.NVDA_NOT_CONNECTED,
		RemoteMessageType.E2E_PUBKEY,
		RemoteMessageType.E2E_DATA,
	},
)


class RemoteSession:
	"""Base class for a session that runs on either the leader or follower machine.

	:note: Handles core session tasks:
	    - Version compatibility checks
	    - Message of the day handling
	    - Connection management
	    - Transport registration
	"""

	transport: RelayTransport
	"""The transport layer handling network communication"""

	localMachine: LocalMachine
	"""Interface to control the local NVDA instance"""

	mode: connectionInfo.ConnectionMode | None = None
	"""Session mode - either 'leader' or 'follower'"""

	callbacksAdded: bool = False
	"""Whether callbacks are currently registered"""

	leaders: Collection[str]
	"""Information about connected leaders."""

	followers: Collection[str]
	"""Information about connected followers."""

	def __init__(
		self,
		localMachine: LocalMachine,
		transport: RelayTransport,
		isDirectConnection: bool = False,
	) -> None:
		"""Initialise the remote session.

		:param localMachine: Interface to control local NVDA instance
		:param transport: Network transport layer instance
		:param isDirectConnection: True when connected directly to another NVDA
			instance running a local relay server, rather than through an
			external relay. E2E warnings are suppressed for direct connections
			as they are already secured by TLS.
		"""
		log.info("Initializing Remote Session")
		self.localMachine = localMachine
		self.callbacksAdded = False
		self.transport = transport
		self._isDirectConnection: bool = isDirectConnection
		self.e2eUnavailable: Action = Action()
		"""Fired when E2E encryption cannot be established because the server
		does not support it. Handlers receive keyword argument
		``address`` (tuple[str, int]) identifying the server.
		This can be suppressed per-server.
		"""
		self.e2ePeerUnsupported: Action = Action()
		"""Fired when E2E encryption is torn down because a connected peer
		does not support it, most likely due to running an older NVDA version.
		This cannot be suppressed as the peer set may change with each connection.
		"""
		# E2E encryption state
		self.e2e: E2ESession | None = None
		self._e2eAvailable: bool = False
		self._myUserId: int | None = None
		self._peerE2ESupport: dict[int, bool] = {}
		self.transport.registerInbound(
			RemoteMessageType.VERSION_MISMATCH,
			self.handleVersionMismatch,
		)
		self.transport.registerInbound(RemoteMessageType.MOTD, self.handleMOTD)
		self.transport.registerInbound(
			RemoteMessageType.SET_CLIPBOARD_TEXT,
			self.localMachine.setClipboardText,
		)
		self.transport.registerInbound(
			RemoteMessageType.CLIENT_JOINED,
			self.handleClientConnected,
		)
		self.transport.registerInbound(
			RemoteMessageType.CLIENT_LEFT,
			self.handleClientDisconnected,
		)
		# E2E message handlers
		self.transport.registerInbound(
			RemoteMessageType.E2E_PUBKEY,
			self._handleE2EPubkey,
		)
		self.transport.registerInbound(
			RemoteMessageType.E2E_DATA,
			self._handleE2EData,
		)

	def handleVersionMismatch(self) -> None:
		"""Handle protocol version mismatch between client and server.

		:note: Called when transport detects incompatible protocol versions.
		    - Displays localized error message
		    - Closes transport connection
		    - Prevents further communication
		"""
		log.error("Protocol version mismatch detected with relay server")
		ui.message(
			pgettext(
				"remote",
				# Translators: Message presented when attempting to connect to an incompatible Remote Access server.
				"The Remote Access server you have connected to is not compatible with this version of NVDA. Please use a different server.",
			),
		)
		self.transport.close()

	def handleMOTD(self, motd: str, force_display: bool = False) -> None:
		"""Handle Message of the Day from relay server.

		:param motd: Message text to display
		:param force_display: If True, always show message even if seen before
		:note: Shows message if:
		    - Not shown before (tracked by hash)
		    - force_display is True
		    Used for service announcements, maintenance notices, etc.
		    Message hashes stored per-server in config.
		"""
		if force_display or self.shouldDisplayMotd(motd):
			gui.messageBox(
				parent=gui.mainFrame,
				# Translators: Title of a dialog showing a message sent by a Remote Access server.
				caption=pgettext("remote", "Message from Remote Access Server"),
				message=motd,
			)

	def shouldDisplayMotd(self, motd: str) -> bool:
		"""Check if MOTD should be displayed.

			:param motd: Message to check
			:return: True if message should be shown
			:note: Compares message hash against previously shown messages
			    stored in config file per server

			.. warning::
		Calling this method will cause the MoTD to be registered as shown if it has not been already.
		"""
		conf = configuration.getRemoteConfig()
		connection = self.getConnectionInfo()
		address = "{host}:{port}".format(
			host=connection.hostname,
			port=connection.port,
		)
		motdBytes = motd.encode("utf-8", errors="surrogatepass")
		hashed = hashlib.sha1(motdBytes).hexdigest()
		current = conf["seenMOTDs"].get(address, "")
		if current == hashed:
			return False
		conf["seenMOTDs"][address] = hashed
		return True

	def handleClientConnected(self, client: dict[str, Any] | None) -> None:
		"""Handle new client connection.

		:param client: Dictionary containing client connection details
		:note: Logs connection info and plays connection sound.
			Also tracks E2E support and manages E2E session state.
		"""
		log.info(f"Client connected: {client!r}")
		cues.clientConnected()
		if client is not None:
			self._peerE2ESupport[client["id"]] = client.get("e2e_supported", False)
			if not client.get("e2e_supported", False) and self.e2e is not None:
				# Non-E2E peer joined - tear down E2E
				log.info("E2E: Session torn down, peer %d does not support encryption", client["id"])
				self.e2e = None
				self._warnE2EPeerUnsupported(client["id"])
			elif client.get("e2e_supported", False) and self.e2e is not None:
				# E2E peer joined - send them our pubkey
				self.transport.send(RemoteMessageType.E2E_PUBKEY, **self.e2e.get_pubkey_message())

	def handleClientDisconnected(self, client: dict[str, Any] | None = None) -> None:
		"""Handle client disconnection.

		:param client: Optional client info dictionary
		:note: Plays disconnection sound when remote client disconnects.
			Cleans up E2E peer state.
		"""
		cues.clientDisconnected()
		if client is not None:
			self._peerE2ESupport.pop(client.get("id"), None)
			if self.e2e is not None:
				self.e2e.remove_peer(client.get("id", 0))

	def _warnE2EUnavailable(self) -> None:
		"""Warn the user that E2E encryption is not available on a relay connection.

		Skips the warning for direct connections where E2E is not expected.
		Notifies :attr:`e2eUnavailable` so the client layer can prompt the user.
		"""
		if self._isDirectConnection:
			return
		log.warning("E2E encryption unavailable: server does not support E2E")
		self.e2eUnavailable.notify(address=self.transport.address)

	def _warnE2EPeerUnsupported(self, peerId: int | None = None) -> None:
		"""Warn that E2E was torn down because a peer does not support it.

		Skips the warning for direct connections where E2E is not expected.
		Notifies :attr:`e2ePeerUnsupported` so the client layer can prompt the user.
		Unlike :meth:`_warnE2EUnavailable`, this cannot be suppressed per-server
		as the peer set may change with each connection.
		"""
		if self._isDirectConnection:
			return
		if peerId is not None:
			log.warning("E2E disabled: peer %d does not support encryption", peerId)
		else:
			log.warning("E2E disabled: not all peers support encryption")
		self.e2ePeerUnsupported.notify()

	def _tryInitE2E(self) -> None:
		"""Init E2E if conditions are met: server allows it and all peers support it."""
		if not self._e2eAvailable:
			self.e2e = None
			self._warnE2EUnavailable()
			return
		all_peers_e2e = all(self._peerE2ESupport.values()) if self._peerE2ESupport else True
		if all_peers_e2e:
			self.e2e = E2ESession()
			self.transport.send(RemoteMessageType.E2E_PUBKEY, **self.e2e.get_pubkey_message())
			log.info("E2E: Session initialized, public key broadcast")
		else:
			self.e2e = None
			self._warnE2EPeerUnsupported()

	def _handleE2EPubkey(self, pubkey: str, nonce_prefix: str, origin: int, **kwargs: Any) -> None:
		"""Process a peer's public key and derive shared secret."""
		if self.e2e is not None:
			self.e2e.add_peer(origin, pubkey, nonce_prefix)

	def _handleE2EData(self, ciphertext: str, nonce: str, origin: int, to: int, **kwargs: Any) -> None:
		"""Decrypt an E2E message and dispatch the inner message."""
		if self.e2e is None:
			return
		if self._myUserId is not None and to != self._myUserId:
			return  # Not addressed to us
		result = self.e2e.decrypt(origin, ciphertext, nonce)
		if result is None:
			return
		msg_type, msg_kwargs = result
		# Reconstruct speech commands if this is a SPEAK message
		if msg_type == RemoteMessageType.SPEAK.value:
			msg_kwargs = asSequence({"type": msg_type, **msg_kwargs})
			msg_kwargs.pop("type", None)
		try:
			messageType = RemoteMessageType(msg_type)
		except ValueError:
			log.warning(f"E2E: Unknown decrypted message type: {msg_type}")
			return
		extensionPoint = self.transport.inboundHandlers.get(messageType)
		if extensionPoint:
			extensionPoint.notify(**msg_kwargs)

	def send(self, type: RemoteMessageType, **kwargs: Any) -> None:
		"""Send a message, transparently encrypting data-plane messages when E2E is active.

		Control-plane messages (JOIN, PROTOCOL_VERSION, E2E_PUBKEY, etc.) are always
		sent in plaintext. Data-plane messages (KEY, SPEAK, TONE, etc.) are encrypted
		per-peer when an E2E session is established.

		SPEAK messages receive special handling: speech command objects are serialized
		with :class:`SpeechCommandJSONEncoder` before encryption, since the default
		``json.dumps`` cannot handle them.
		"""
		if (
			self.e2e is not None
			and self.e2e.peer_ids
			and self._myUserId is not None
			and type not in _E2E_CONTROL_PLANE_TYPES
		):
			if type is RemoteMessageType.SPEAK:
				# Speech commands need the custom encoder
				serialized = json.dumps(kwargs, cls=SpeechCommandJSONEncoder).encode("utf-8")
				encrypted_msgs = self.e2e.encrypt_preserialized(
					type.value,
					from_id=self._myUserId,
					serialized_kwargs=serialized,
				)
			else:
				encrypted_msgs = self.e2e.encrypt(type.value, from_id=self._myUserId, **kwargs)
			for msg in encrypted_msgs:
				self.transport.send(RemoteMessageType.E2E_DATA, **msg)
		else:
			self.transport.send(type, **kwargs)

	def getConnectionInfo(self) -> connectionInfo.ConnectionInfo:
		"""Get information about the current connection.

		:return: ConnectionInfo object with server details and session mode
		:note: Contains hostname, port, channel key and session mode
		"""
		hostname, port = self.transport.address
		key = self.transport.channel
		return connectionInfo.ConnectionInfo(
			hostname=hostname,
			port=port,
			key=key,
			mode=self.mode,
		)

	def close(self) -> None:
		"""Close the transport connection.

		Terminates the network connection and cleans up resources.
		"""
		self.transport.close()

	def __del__(self) -> None:
		"""Ensure transport is closed when object is deleted."""
		self.close()

	@property
	def connectedLeadersCount(self) -> int:
		return len(self.leaders)

	@property
	def connectedFollowersCount(self) -> int:
		return len(self.followers)

	@property
	def connectedClientsCount(self) -> int:
		return self.connectedLeadersCount + self.connectedFollowersCount


class FollowerSession(RemoteSession):
	"""Session that runs on the controlled (follower) NVDA instance.

	:ivar leaders: Information about connected leader clients
	:ivar leaderDisplaySizes: Braille display sizes of connected leaders
	:note: Handles:
	    - Command execution from leaders
	    - Output forwarding to leaders
	    - Multi-leader connections
	    - Braille display coordination
	"""

	# Connection mode - always follower
	mode: Final[connectionInfo.ConnectionMode] = connectionInfo.ConnectionMode.FOLLOWER
	# Information about connected leader clients
	leaders: dict[int, dict[str, Any]]
	leaderDisplaySizes: list[int]  # Braille display sizes of connected leaders
	followers: set[str]

	def __init__(
		self,
		localMachine: LocalMachine,
		transport: RelayTransport,
		isDirectConnection: bool = False,
	) -> None:
		super().__init__(localMachine, transport, isDirectConnection=isDirectConnection)
		self.transport.registerInbound(
			RemoteMessageType.KEY,
			self.localMachine.sendKey,
		)
		self.leaders = defaultdict(dict)
		self.leaderDisplaySizes = []
		self.followers = set()
		self.transport.transportClosing.register(self.handleTransportClosing)
		self.transport.registerInbound(
			RemoteMessageType.CHANNEL_JOINED,
			self.handleChannelJoined,
		)
		self.transport.registerInbound(
			RemoteMessageType.SET_BRAILLE_INFO,
			self.handleBrailleInfo,
		)
		self.transport.registerInbound(
			RemoteMessageType.SET_DISPLAY_SIZE,
			self.setDisplaySize,
		)
		braille.filter_displayDimensions.register(
			self.localMachine._handleFilterDisplayDimensions,
		)
		self.transport.registerInbound(
			RemoteMessageType.BRAILLE_INPUT,
			self.localMachine.brailleInput,
		)
		self.transport.registerInbound(
			RemoteMessageType.SEND_SAS,
			self.localMachine.sendSAS,
		)

	def registerCallbacks(self) -> None:
		if self.callbacksAdded:
			return
		tones.decide_beep.register(self._handleToneOutbound)
		speechCanceled.register(self._handleCancelOutbound)
		decide_playWaveFile.register(self._handleWaveOutbound)
		post_speechPaused.register(self._handlePauseSpeechOutbound)
		braille.pre_writeCells.register(self.display)
		pre_speechQueued.register(self.sendSpeech)
		self.callbacksAdded = True

	def unregisterCallbacks(self) -> None:
		if not self.callbacksAdded:
			return
		tones.decide_beep.unregister(self._handleToneOutbound)
		speechCanceled.unregister(self._handleCancelOutbound)
		decide_playWaveFile.unregister(self._handleWaveOutbound)
		post_speechPaused.unregister(self._handlePauseSpeechOutbound)
		braille.pre_writeCells.unregister(self.display)
		pre_speechQueued.unregister(self.sendSpeech)
		self.callbacksAdded = False

	def _handleToneOutbound(self, *args: Any, **kwargs: Any) -> bool:
		self.send(RemoteMessageType.TONE, **kwargs)
		return True

	def _handleCancelOutbound(self, *args: Any, **kwargs: Any) -> bool:
		self.send(RemoteMessageType.CANCEL, **kwargs)
		return True

	def _handleWaveOutbound(self, *args: Any, **kwargs: Any) -> bool:
		self.send(RemoteMessageType.WAVE, **kwargs)
		return True

	def _handlePauseSpeechOutbound(self, *args: Any, **kwargs: Any) -> bool:
		self.send(RemoteMessageType.PAUSE_SPEECH, **kwargs)
		return True

	def handleClientConnected(self, client: dict[str, Any]) -> None:
		super().handleClientConnected(client)
		if client["connection_type"] == connectionInfo.ConnectionMode.LEADER.value:
			self.leaders[client["id"]]["active"] = True
		elif client["connection_type"] == connectionInfo.ConnectionMode.FOLLOWER.value:
			self.followers.add(client["id"])
		if self.leaders:
			self.registerCallbacks()

	def handleChannelJoined(
		self,
		channel: str,
		clients: list[dict[str, Any]] | None = None,
		origin: int | None = None,
		user_id: int | None = None,
		e2e_available: bool = False,
		**kwargs: Any,
	) -> None:
		if clients is None:
			clients = []
		self._myUserId = user_id
		self._e2eAvailable = e2e_available
		for client in clients:
			self._peerE2ESupport[client["id"]] = client.get("e2e_supported", False)
			self.handleClientConnected(client)
		self._tryInitE2E()

	def handleTransportClosing(self) -> None:
		"""Handle cleanup when transport connection is closing.

		Removes any registered callbacks
		to ensure clean shutdown of remote features.
		"""
		self.unregisterCallbacks()

	def handleTransportDisconnected(self) -> None:
		"""Handle disconnection from the transport layer.

		Called when the transport connection is lost. This method:
		1. Plays a connection sound cue
		2. Removes any NVDA patches
		"""
		log.info("Transport disconnected from follower session")
		cues.clientDisconnected()

	def handleClientDisconnected(self, client: dict[str, Any]) -> None:
		super().handleClientDisconnected(client)
		if client["connection_type"] == connectionInfo.ConnectionMode.LEADER.value:
			log.info(f"Leader client disconnected: {client!r}")
			del self.leaders[client["id"]]
		elif client["connection_type"] == connectionInfo.ConnectionMode.FOLLOWER.value:
			self.followers.discard(client["id"])
		if not self.leaders:
			self.unregisterCallbacks()

	def setDisplaySize(self, sizes: list[int] | None = None) -> None:
		self.leaderDisplaySizes = (
			sizes if sizes else [info.get("braille_numCells", 0) for info in self.leaders.values()]
		)
		log.debug(f"Setting follower display size to: {self.leaderDisplaySizes!r}")
		self.localMachine.setBrailleDisplaySize(self.leaderDisplaySizes)

	def handleBrailleInfo(
		self,
		name: str | None = None,
		numCells: int = 0,
		origin: int | None = None,
	) -> None:
		if not self.leaders.get(origin):
			return
		self.leaders[origin]["braille_name"] = name
		self.leaders[origin]["braille_numCells"] = numCells
		self.setDisplaySize()

	def _filterUnsupportedSpeechCommands(self, speechSequence: list[Any]) -> list[Any]:
		"""Remove unsupported speech commands from a sequence.

		Filters out commands that cannot be properly serialized or executed remotely,
		like callback commands and cancellable commands.

		Returns:
				Filtered sequence containing only supported speech commands
		"""
		return list([item for item in speechSequence if not isinstance(item, EXCLUDED_SPEECH_COMMANDS)])

	def sendSpeech(self, speechSequence: list[Any], priority: str | None) -> None:
		"""Forward speech output to connected leader instances.

		Filters the speech sequence for supported commands and sends it
		to leader instances for speaking. E2E encryption with proper
		speech command serialization is handled transparently by send().
		"""
		self.send(
			RemoteMessageType.SPEAK,
			sequence=self._filterUnsupportedSpeechCommands(
				speechSequence,
			),
			priority=priority,
		)

	def pauseSpeech(self, switch: bool) -> None:
		"""Toggle speech pause state on leader instances."""
		self.send(RemoteMessageType.PAUSE_SPEECH, switch=switch)

	def display(self, cells: list[int]) -> None:
		"""Forward braille display content to leader instances.

		Only sends braille data if there are connected leaders with braille displays.
		"""
		# Only send braille data when there are controlling machines with a braille display
		if self.hasBrailleLeaders():
			self.send(RemoteMessageType.DISPLAY, cells=cells)

	def hasBrailleLeaders(self) -> bool:
		"""Check if any connected leaders have braille displays.

		Returns:
				True if at least one leader has a braille display with cells > 0
		"""
		return bool([i for i in self.leaderDisplaySizes if i > 0])


class LeaderSession(RemoteSession):
	"""Session that runs on the controlling (leader) NVDA instance.

	:ivar followers: Information about connected follower clients
	:note: Handles:
	    - Control command sending
	    - Remote output reception
	    - Sound notification playback
	    - Client connection management
	    - Braille display sync
	    - Input handling patches
	"""

	mode: Final[connectionInfo.ConnectionMode] = connectionInfo.ConnectionMode.LEADER
	followers: dict[int, dict[str, Any]]  # Information about connected follower
	leaders: set[str]

	def __init__(
		self,
		localMachine: LocalMachine,
		transport: RelayTransport,
		isDirectConnection: bool = False,
	) -> None:
		super().__init__(localMachine, transport, isDirectConnection=isDirectConnection)
		self.followers = defaultdict(dict)
		self.leaders = set()
		self.transport.registerInbound(
			RemoteMessageType.SPEAK,
			self.localMachine.speak,
		)
		self.transport.registerInbound(
			RemoteMessageType.CANCEL,
			self.localMachine.cancelSpeech,
		)
		self.transport.registerInbound(
			RemoteMessageType.PAUSE_SPEECH,
			self.localMachine.pauseSpeech,
		)
		self.transport.registerInbound(
			RemoteMessageType.TONE,
			self.localMachine.beep,
		)
		self.transport.registerInbound(
			RemoteMessageType.WAVE,
			self.localMachine.playWave,
		)
		self.transport.registerInbound(
			RemoteMessageType.DISPLAY,
			self.localMachine.display,
		)
		self.transport.registerInbound(
			RemoteMessageType.NVDA_NOT_CONNECTED,
			self.handleNVDANotConnected,
		)
		self.transport.registerInbound(
			RemoteMessageType.CHANNEL_JOINED,
			self.handleChannelJoined,
		)
		self.transport.registerInbound(
			RemoteMessageType.SET_BRAILLE_INFO,
			self.sendBrailleInfo,
		)

	def registerCallbacks(self) -> None:
		if self.callbacksAdded:
			return
		braille.displayChanged.register(self.sendBrailleInfo)
		braille.displaySizeChanged.register(self.sendBrailleInfo)
		self.callbacksAdded = True

	def unregisterCallbacks(self) -> None:
		if not self.callbacksAdded:
			return
		braille.displayChanged.unregister(self.sendBrailleInfo)
		braille.displaySizeChanged.unregister(self.sendBrailleInfo)
		self.callbacksAdded = False

	def handleNVDANotConnected(self) -> None:
		log.warning("Attempted to connect to remote NVDA that is not available")
		speech.cancelSpeech()
		ui.message(
			# Translators: Message for when the remote NVDA is not connected
			pgettext("remote", "Remote NVDA not connected"),
		)

	def handleChannelJoined(
		self,
		channel: str,
		clients: list[dict[str, Any]] | None = None,
		origin: int | None = None,
		user_id: int | None = None,
		e2e_available: bool = False,
		**kwargs: Any,
	) -> None:
		if clients is None:
			clients = []
		self._myUserId = user_id
		self._e2eAvailable = e2e_available
		for client in clients:
			self._peerE2ESupport[client["id"]] = client.get("e2e_supported", False)
			self.handleClientConnected(client)
		self._tryInitE2E()

	def handleClientConnected(self, client: dict[str, Any] | None = None):
		hasFollowers = bool(self.followers)
		super().handleClientConnected(client)
		if client["connection_type"] == connectionInfo.ConnectionMode.FOLLOWER.value:
			self.followers[client["id"]]["active"] = True
		elif client["connection_type"] == connectionInfo.ConnectionMode.LEADER.value:
			self.leaders.add(client["id"])
		self.sendBrailleInfo()
		if not hasFollowers:
			self.registerCallbacks()

	def handleClientDisconnected(self, client: dict[str, Any] | None = None):
		"""Handle client disconnection.
		Also calls parent class disconnection handler.
		"""
		super().handleClientDisconnected(client)
		if client["connection_type"] == connectionInfo.ConnectionMode.FOLLOWER.value:
			del self.followers[client["id"]]
		elif client["connection_type"] == connectionInfo.ConnectionMode.LEADER.value:
			self.leaders.discard(client["id"])
		if self.callbacksAdded and not self.followers:
			self.unregisterCallbacks()

	def sendBrailleInfo(
		self,
		display: braille.BrailleDisplayDriver | None = None,
		displayDimensions: braille.DisplayDimensions | None = None,
	) -> None:
		if display is None:
			display = braille.handler.display
		if displayDimensions is None:
			displayDimensions = braille.handler.displayDimensions
		displaySize = displayDimensions.numCols
		log.debug(f"Sending braille info to follower - display: {display.name}, width: {displaySize}")
		self.send(
			RemoteMessageType.SET_BRAILLE_INFO,
			name=display.name,
			numCells=displaySize,
		)

	def handleDecideExecuteGesture(
		self,
		gesture: braille.BrailleDisplayGesture | brailleInput.BrailleInputGesture,
	) -> bool:
		"""Handle and forward braille gestures to remote client.

		:param gesture: Braille display or input gesture to process
		:return: False if gesture was processed and sent, True otherwise
		:note: Extracts gesture details and script info before sending
		"""
		# Import late to avoid circular import
		from globalCommands import commands

		if isinstance(gesture, (braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture)):
			if self.localMachine._showingLocalUiMessage and gesture.script in (
				commands.script_braille_routeTo,
				commands.script_braille_scrollBack,
				commands.script_braille_scrollForward,
			):
				return True
			dict = {
				key: gesture.__dict__[key]
				for key in gesture.__dict__
				if isinstance(gesture.__dict__[key], (int, str, bool))
			}
			if gesture.script:
				name = scriptHandler.getScriptName(gesture.script)
				if name.startswith("kb"):
					location = ["globalCommands", "GlobalCommands"]
				else:
					location = scriptHandler.getScriptLocation(gesture.script).rsplit(".", 1)
				dict["scriptPath"] = location + [name]
			else:
				scriptData = None
				maps = [inputCore.manager.userGestureMap, inputCore.manager.localeGestureMap]
				if braille.handler.display.gestureMap:
					maps.append(braille.handler.display.gestureMap)
				for map in maps:
					for identifier in gesture.identifiers:
						try:
							scriptData = next(map.getScriptsForGesture(identifier))
							break
						except StopIteration:
							continue
				if scriptData:
					dict["scriptPath"] = [scriptData[0].__module__, scriptData[0].__name__, scriptData[1]]
			if hasattr(gesture, "source") and "source" not in dict:
				dict["source"] = gesture.source
			if hasattr(gesture, "model") and "model" not in dict:
				dict["model"] = gesture.model
			if hasattr(gesture, "id") and "id" not in dict:
				dict["id"] = gesture.id
			elif hasattr(gesture, "identifiers") and "identifiers" not in dict:
				dict["identifiers"] = gesture.identifiers
			if hasattr(gesture, "dots") and "dots" not in dict:
				dict["dots"] = gesture.dots
			if hasattr(gesture, "space") and "space" not in dict:
				dict["space"] = gesture.space
			if hasattr(gesture, "routingIndex") and "routingIndex" not in dict:
				dict["routingIndex"] = gesture.routingIndex
			self.localMachine._dismissLocalBrailleMessage()
			self.send(RemoteMessageType.BRAILLE_INPUT, **dict)
			return False
		else:
			return True

	def registerBrailleInput(self) -> None:
		"""Register handler for braille input gestures.

		:note: Connects to inputCore's gesture execution decision point
		"""
		inputCore.decide_executeGesture.register(self.handleDecideExecuteGesture)

	def unregisterBrailleInput(self) -> None:
		"""Unregister handler for braille input gestures.

		:note: Disconnects from inputCore's gesture execution decision point
		"""
		inputCore.decide_executeGesture.unregister(self.handleDecideExecuteGesture)
