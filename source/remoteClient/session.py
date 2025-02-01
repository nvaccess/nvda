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
RemoteSession
	Base session managing shared functionality:
	- Message handler registration
	- Connection validation
	- Version compatibility
	- MOTD handling

MasterSession
	Controls remote instance:
	- Input capture/forwarding
	- Remote output reception
	- Connection management
	- Master-specific patches

SlaveSession
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
from typing import Any, Dict, List, Optional, Union

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

	This abstract base class defines the core functionality shared between master and slave
	sessions. It handles basic session management tasks like:

	- Handling version mismatch notifications
	- Message of the day handling
	- Connection info management
	- Transport registration

	"""

	transport: RelayTransport  # The transport layer handling network communication
	localMachine: LocalMachine  # Interface to control the local NVDA instance
	# Session mode - either 'master' or 'slave'
	mode: Optional[connectionInfo.ConnectionMode] = None
	callbacksAdded: bool  # Whether callbacks are currently registered

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

		This method is called when the transport layer detects that the client's
		protocol version is not compatible. It:
		1. Displays a localized error message to the user
		2. Closes the transport connection
		3. Prevents further communication attempts
		"""
		log.error("Protocol version mismatch detected with relay server")
		ui.message(
			# Translators: Message for version mismatch
			_("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please use a different server."""),
		)
		self.transport.close()

	def handleMOTD(self, motd: str, force_display=False):
		"""Handle Message of the Day from relay server.

		log.info("Received MOTD from server (force_display=%s)", force_display)

		Displays server MOTD to user if:
		1. It hasn't been shown before (tracked by message hash), or
		2. force_display is True (for important announcements)

		The MOTD system allows server operators to communicate important
		information to users like:
		- Service announcements
		- Maintenance windows
		- Version update notifications
		- Security advisories
		Note:
				Message hashes are stored per-server in the config file to track
				which messages have already been shown to the user.
		"""
		if force_display or self.shouldDisplayMotd(motd):
			gui.messageBox(
				parent=gui.mainFrame,
				# Translators: Caption for message of the day dialog
				caption=_("Message of the Day"),
				message=motd,
			)

	def shouldDisplayMotd(self, motd: str) -> bool:
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

	def handleClientConnected(self, client: Optional[Dict[str, Any]] = None) -> None:
		"""Handle new client connection."""
		log.info("Client connected: %r", client)
		cues.clientConnected()

	def handleClientDisconnected(self, client=None):
		"""Handle client disconnection.
		Plays disconnection sound when remote client disconnects.
		"""
		cues.clientDisconnected()

	def getConnectionInfo(self) -> connectionInfo.ConnectionInfo:
		"""Get information about the current connection.

		Returns a ConnectionInfo object containing:
		- Hostname and port of the relay server
		- Channel key for the connection
		- Session mode (master/slave)
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


class SlaveSession(RemoteSession):
	"""Session that runs on the controlled (slave) NVDA instance.

	This class implements the slave side of an NVDA Remote connection. It handles:

	- Receiving and executing commands from master(s)
	- Forwarding speech/braille/tones/NVWave output to master(s)
	- Managing connected master clients and their braille display sizes
	- Coordinating braille display functionality

	The slave session allows multiple master connections simultaneously and manages
	state for each connected master separately.
	"""

	# Connection mode - always 'slave'
	mode: connectionInfo.ConnectionMode = connectionInfo.ConnectionMode.SLAVE
	# Information about connected master clients
	masters: Dict[int, Dict[str, Any]]
	masterDisplaySizes: List[int]  # Braille display sizes of connected masters

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
		self.masters = defaultdict(dict)
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

	def handleClientConnected(self, client: Dict[str, Any]) -> None:
		super().handleClientConnected(client)
		if client["connection_type"] == "master":
			self.masters[client["id"]]["active"] = True
		if self.masters:
			self.registerCallbacks()

	def handleChannelJoined(
		self,
		channel: Optional[str] = None,
		clients: Optional[List[Dict[str, Any]]] = None,
		origin: Optional[int] = None,
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
		cues.clientConnected()

	def handleClientDisconnected(self, client: Optional[Dict[str, Any]] = None) -> None:
		super().handleClientDisconnected(client)
		if client["connection_type"] == "master":
			log.info("Master client disconnected: %r", client)
			del self.masters[client["id"]]
		if not self.masters:
			self.unregisterCallbacks()

	def setDisplaySize(self, sizes=None):
		self.masterDisplaySizes = (
			sizes if sizes else [info.get("braille_numCells", 0) for info in self.masters.values()]
		)
		log.debug("Setting slave display size to: %r", self.masterDisplaySizes)
		self.localMachine.setBrailleDisplay_size(self.masterDisplaySizes)

	def handleBrailleInfo(
		self,
		name: Optional[str] = None,
		numCells: int = 0,
		origin: Optional[int] = None,
	) -> None:
		if not self.masters.get(origin):
			return
		self.masters[origin]["braille_name"] = name
		self.masters[origin]["braille_numCells"] = numCells
		self.setDisplaySize()

	def _filterUnsupportedSpeechCommands(self, speechSequence: List[Any]) -> List[Any]:
		"""Remove unsupported speech commands from a sequence.

		Filters out commands that cannot be properly serialized or executed remotely,
		like callback commands and cancellable commands.

		Returns:
				Filtered sequence containing only supported speech commands
		"""
		return list([item for item in speechSequence if not isinstance(item, EXCLUDED_SPEECH_COMMANDS)])

	def sendSpeech(self, speechSequence: List[Any], priority: Optional[str]) -> None:
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

	def display(self, cells: List[int]) -> None:
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


class MasterSession(RemoteSession):
	"""Session that runs on the controlling (master) NVDA instance.

	This class implements the master side of an NVDA Remote connection. It handles:

	- Sending control commands to slaves
	- Receiving and playing speech/braille from slaves
	- Playing basic notification sounds from slaves
	- Managing connected slave clients
	- Synchronizing braille display information
	- Patching NVDA for remote input handling

	The master session takes input from the local NVDA instance and forwards
	appropriate commands to control the remote slave instance.
	"""

	mode: connectionInfo.ConnectionMode = connectionInfo.ConnectionMode.MASTER
	slaves: Dict[int, Dict[str, Any]]  # Information about connected slave

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
			self.handleChannel_joined,
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

	def handleChannel_joined(
		self,
		channel: Optional[str] = None,
		clients: Optional[List[Dict[str, Any]]] = None,
		origin: Optional[int] = None,
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
		display: Optional[Any] = None,
		displaySize: Optional[int] = None,
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

	def handle_decide_executeGesture(
		self,
		gesture: Union[braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture, Any],
	) -> bool:
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
		inputCore.decide_executeGesture.register(self.handle_decide_executeGesture)

	def unregisterBrailleInput(self) -> None:
		inputCore.decide_executeGesture.unregister(self.handle_decide_executeGesture)
