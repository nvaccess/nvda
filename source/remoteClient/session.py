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
Master (Controlling)
	- Captures and forwards input
	- Receives remote output (speech/braille)
	- Manages connection state
	- Patches input handling

Slave (Controlled)
	- Executes received commands
	- Forwards output to master(s)
	- Tracks connected masters
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
	- Master-specific patches

:class:`FollowerSession`
	Controlled by remote instance:
	- Command execution
	- Output forwarding
	- Multi-master support
	- Slave-specific patches

Thread Safety:
------------
All message handlers execute on wx main thread via CallAfter
to ensure thread-safe NVDA operations.

See Also:
	transport.py: Network communication
	local_machine.py: NVDA interface
"""

import hashlib
from collections import defaultdict
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
from .localMachine import LocalMachine
from .protocol import RemoteMessageType
from .transport import RelayTransport

EXCLUDED_SPEECH_COMMANDS = (
	speech.commands.BaseCallbackCommand,
	# _CancellableSpeechCommands are not designed to be reported and are used internally by NVDA. (#230)
	speech.commands._CancellableSpeechCommand,
)


class RemoteSession:
	"""Base class for a session that runs on either the master or slave machine.

	:param localMachine: Interface to control local NVDA instance
	:param transport: Network transport layer instance
	:note: Handles core session tasks:
	    - Version compatibility checks
	    - Message of the day handling
	    - Connection management
	    - Transport registration
	"""

	transport: RelayTransport  # The transport layer handling network communication
	localMachine: LocalMachine  # Interface to control the local NVDA instance
	# Session mode - either 'master' or 'slave'
	mode: connectionInfo.ConnectionMode | None = None
	callbacksAdded: bool = False  # Whether callbacks are currently registered

	def __init__(
		self,
		localMachine: LocalMachine,
		transport: RelayTransport,
	) -> None:
		log.info("Initializing Remote Session")
		self.localMachine = localMachine
		self.callbacksAdded = False
		self.transport = transport
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

	def handleVersionMismatch(self) -> None:
		"""Handle protocol version mismatch between client and server.

		:note: Called when transport detects incompatible protocol versions.
		    - Displays localized error message
		    - Closes transport connection
		    - Prevents further communication
		"""
		log.error("Protocol version mismatch detected with relay server")
		ui.message(
			# Translators: Message for version mismatch
			_("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please use a different server."""),
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
				# Translators: Caption for message of the day dialog
				caption=_("Message of the Day"),
				message=motd,
			)

	def shouldDisplayMotd(self, motd: str) -> bool:
		"""Check if MOTD should be displayed.

		:param motd: Message to check
		:return: True if message should be shown
		:note: Compares message hash against previously shown messages
		    stored in config file per server
		"""
		conf = configuration.get_config()
		connection = self.getConnectionInfo()
		address = "{host}:{port}".format(
			host=connection.hostname,
			port=connection.port,
		)
		motdBytes = motd.encode("utf-8", errors="surrogatepass")
		hashed = hashlib.sha1(motdBytes).hexdigest()
		current = conf["seen_motds"].get(address, "")
		if current == hashed:
			return False
		conf["seen_motds"][address] = hashed
		return True

	def handleClientConnected(self, client: dict[str, Any] | None) -> None:
		"""Handle new client connection.

		:param client: Dictionary containing client connection details
		:note: Logs connection info and plays connection sound
		"""
		log.info("Client connected: %r", client)
		cues.clientConnected()

	def handleClientDisconnected(self, client: dict[str, Any] | None = None) -> None:
		"""Handle client disconnection.

		:param client: Optional client info dictionary
		:note: Plays disconnection sound when remote client disconnects
		"""
		cues.clientDisconnected()

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


class FollowerSession(RemoteSession):
	"""Session that runs on the controlled (slave) NVDA instance.

	:ivar leaders: Information about connected master clients
	:ivar masterDisplaySizes: Braille display sizes of connected masters
	:note: Handles:
	    - Command execution from masters
	    - Output forwarding to masters
	    - Multi-master connections
	    - Braille display coordination
	"""

	# Connection mode - always 'slave'
	mode: Final[connectionInfo.ConnectionMode] = connectionInfo.ConnectionMode.FOLLOWER
	# Information about connected master clients
	leaders: dict[int, dict[str, Any]]
	masterDisplaySizes: list[int]  # Braille display sizes of connected masters

	def __init__(
		self,
		localMachine: LocalMachine,
		transport: RelayTransport,
	) -> None:
		super().__init__(localMachine, transport)
		self.transport.registerInbound(
			RemoteMessageType.KEY,
			self.localMachine.sendKey,
		)
		self.leaders = defaultdict(dict)
		self.masterDisplaySizes = []
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
		braille.filter_displaySize.register(
			self.localMachine.handleFilterDisplaySize,
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
		self.transport.registerOutbound(
			tones.decide_beep,
			RemoteMessageType.TONE,
		)
		self.transport.registerOutbound(
			speechCanceled,
			RemoteMessageType.CANCEL,
		)
		self.transport.registerOutbound(decide_playWaveFile, RemoteMessageType.WAVE)
		self.transport.registerOutbound(post_speechPaused, RemoteMessageType.PAUSE_SPEECH)
		braille.pre_writeCells.register(self.display)
		pre_speechQueued.register(self.sendSpeech)
		self.callbacksAdded = True

	def unregisterCallbacks(self) -> None:
		if not self.callbacksAdded:
			return
		self.transport.unregisterOutbound(RemoteMessageType.TONE)
		self.transport.unregisterOutbound(RemoteMessageType.CANCEL)
		self.transport.unregisterOutbound(RemoteMessageType.WAVE)
		self.transport.unregisterOutbound(RemoteMessageType.PAUSE_SPEECH)
		braille.pre_writeCells.unregister(self.display)
		pre_speechQueued.unregister(self.sendSpeech)
		self.callbacksAdded = False

	def handleClientConnected(self, client: dict[str, Any]) -> None:
		super().handleClientConnected(client)
		if client["connection_type"] == "master":
			self.leaders[client["id"]]["active"] = True
		if self.leaders:
			self.registerCallbacks()

	def handleChannelJoined(
		self,
		channel: str,
		clients: list[dict[str, Any]],
		origin: int | None = None,
	) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

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
		log.info("Transport disconnected from slave session")
		cues.clientDisconnected()

	def handleClientDisconnected(self, client: dict[str, Any]) -> None:
		super().handleClientDisconnected(client)
		if client["connection_type"] == "master":
			log.info("Master client disconnected: %r", client)
			del self.leaders[client["id"]]
		if not self.leaders:
			self.unregisterCallbacks()

	def setDisplaySize(self, sizes: list[int] | None = None) -> None:
		self.masterDisplaySizes = (
			sizes if sizes else [info.get("braille_numCells", 0) for info in self.leaders.values()]
		)
		log.debug("Setting slave display size to: %r", self.masterDisplaySizes)
		self.localMachine.setBrailleDisplay_size(self.masterDisplaySizes)

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
		"""Forward speech output to connected master instances.

		Filters the speech sequence for supported commands and sends it
		to master instances for speaking.
		"""
		self.transport.send(
			RemoteMessageType.SPEAK,
			sequence=self._filterUnsupportedSpeechCommands(
				speechSequence,
			),
			priority=priority,
		)

	def pauseSpeech(self, switch: bool) -> None:
		"""Toggle speech pause state on master instances."""
		self.transport.send(type=RemoteMessageType.PAUSE_SPEECH, switch=switch)

	def display(self, cells: list[int]) -> None:
		"""Forward braille display content to master instances.

		Only sends braille data if there are connected masters with braille displays.
		"""
		# Only send braille data when there are controlling machines with a braille display
		if self.hasBrailleMasters():
			self.transport.send(type=RemoteMessageType.DISPLAY, cells=cells)

	def hasBrailleMasters(self) -> bool:
		"""Check if any connected masters have braille displays.

		Returns:
				True if at least one master has a braille display with cells > 0
		"""
		return bool([i for i in self.masterDisplaySizes if i > 0])


class LeaderSession(RemoteSession):
	"""Session that runs on the controlling (master) NVDA instance.

	:ivar slaves: Information about connected slave clients
	:note: Handles:
	    - Control command sending
	    - Remote output reception
	    - Sound notification playback
	    - Client connection management
	    - Braille display sync
	    - Input handling patches
	"""

	mode: Final[connectionInfo.ConnectionMode] = connectionInfo.ConnectionMode.LEADER
	slaves: dict[int, dict[str, Any]]  # Information about connected slave

	def __init__(
		self,
		localMachine: LocalMachine,
		transport: RelayTransport,
	) -> None:
		super().__init__(localMachine, transport)
		self.slaves = defaultdict(dict)
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
			_("Remote NVDA not connected."),
		)

	def handleChannelJoined(
		self,
		channel: str,
		clients: list[dict[str, Any]] | None = None,
		origin: int | None = None,
	) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

	def handleClientConnected(self, client=None):
		hasSlaves = bool(self.slaves)
		super().handleClientConnected(client)
		self.sendBrailleInfo()
		if not hasSlaves:
			self.registerCallbacks()

	def handleClientDisconnected(self, client=None):
		"""Handle client disconnection.
		Also calls parent class disconnection handler.
		"""
		super().handleClientDisconnected(client)
		if self.callbacksAdded and not self.slaves:
			self.unregisterCallbacks()

	def sendBrailleInfo(
		self,
		display: braille.BrailleDisplayDriver | None = None,
		displaySize: int | None = None,
	) -> None:
		if display is None:
			display = braille.handler.display
		if displaySize is None:
			displaySize = braille.handler.displaySize
		log.debug(
			"Sending braille info to slave - display: %s, size: %d",
			display.name if display else "None",
			displaySize if displaySize else 0,
		)
		self.transport.send(
			type=RemoteMessageType.SET_BRAILLE_INFO,
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
		if isinstance(gesture, (braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture)):
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
			self.transport.send(type=RemoteMessageType.BRAILLE_INPUT, **dict)
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
