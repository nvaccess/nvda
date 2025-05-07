# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import threading
from typing import Optional, Set, Tuple

import api
import braille
from config.configFlags import RemoteConnectionMode
import core
import globalVars
import gui
import inputCore
import ui
import wx
from config import isInstalledCopy
from keyboardHandler import KeyboardInputGesture
from logHandler import log
from gui.guiHelper import alwaysCallAfter
from utils.security import isRunningOnSecureDesktop
import scriptHandler

from . import configuration, cues, dialogs, serializer, server, urlHandler
from .connectionInfo import ConnectionInfo, ConnectionMode
from .localMachine import LocalMachine
from .menu import RemoteMenu
from .protocol import RemoteMessageType, addressToHostPort
from .secureDesktop import SecureDesktopHandler
from .session import LeaderSession, FollowerSession
from .protocol import hostPortToAddress
from .transport import RelayTransport

# Type aliases
KeyModifier = Tuple[int, bool]  # (vk_code, extended)
Address = Tuple[str, int]  # (hostname, port)


class RemoteClient:
	localScripts: Set[scriptHandler._ScriptFunctionT]
	localMachine: LocalMachine
	leaderSession: Optional[LeaderSession]
	followerSession: Optional[FollowerSession]
	keyModifiers: Set[KeyModifier]
	hostPendingModifiers: Set[KeyModifier]
	connecting: bool
	leaderTransport: Optional[RelayTransport]
	followerTransport: Optional[RelayTransport]
	localControlServer: Optional[server.LocalRelayServer]
	sendingKeys: bool

	def __init__(
		self,
	):
		log.info("Initializing NVDA Remote client")
		self.keyModifiers = set()
		self.hostPendingModifiers = set()
		self.localScripts = set()
		self.localMachine = LocalMachine()
		self.followerSession = None
		self.leaderSession = None
		self.menu: Optional[RemoteMenu] = None
		if not isRunningOnSecureDesktop():
			self.menu: Optional[RemoteMenu] = RemoteMenu(self)
		self.connecting = False
		urlHandler.registerURLHandler()
		self.leaderTransport = None
		self.followerTransport = None
		self.localControlServer = None
		self.sendingKeys = False
		self.sdHandler = SecureDesktopHandler()
		if isRunningOnSecureDesktop():
			connection = self.sdHandler.initializeSecureDesktop()
			if connection:
				self.connectAsFollower(connection)
				self.followerSession.transport.connectedEvent.wait(
					self.sdHandler.SD_CONNECT_BLOCK_TIMEOUT,
				)
		core.postNvdaStartup.register(self.performAutoconnect)
		inputCore.decide_handleRawKey.register(self.processKeyInput)

	def performAutoconnect(self):
		controlServerConfig = configuration.getRemoteConfig()["controlServer"]
		if not controlServerConfig["autoconnect"] or self.leaderSession or self.followerSession:
			log.debug("Autoconnect disabled or already connected")
			return
		key = controlServerConfig["key"]
		insecure = False
		selfHosted = controlServerConfig["selfHosted"]
		if selfHosted:
			port = controlServerConfig["port"]
			hostname = "localhost"
			insecure = True
			self.startControlServer(port, key)
		else:
			hostname, port = addressToHostPort(controlServerConfig["host"])
		mode = RemoteConnectionMode(controlServerConfig["connectionMode"]).toConnectionMode()
		conInfo = ConnectionInfo(mode=mode, hostname=hostname, port=port, key=key, insecure=insecure)
		self.connect(conInfo)

	def terminate(self):
		self.sdHandler.terminate()
		self.disconnect()
		self.localMachine.terminate()
		self.localMachine = None
		if self.menu is not None:
			self.menu.terminate()
			self.menu = None
		self.localScripts.clear()
		core.postNvdaStartup.unregister(self.performAutoconnect)
		inputCore.decide_handleRawKey.unregister(self.processKeyInput)
		if not isInstalledCopy():
			urlHandler.unregisterURLHandler()

	def toggleMute(self):
		"""Toggle muting of speech and sounds from the remote computer.

		:note: Updates menu item state and announces new mute status
		"""
		if not self.isConnected():
			# Translators: Message shown when attempting to mute the remote computer when no session is connected.
			ui.message(pgettext("remote", "Not connected"))
			return
		self.localMachine.isMuted = not self.localMachine.isMuted
		self.menu.muteItem.Check(self.localMachine.isMuted)
		# Translators: Displayed when muting speech and sounds from the remote computer
		MUTE_MESSAGE = _("Muted remote")
		# Translators: Displayed when unmuting speech and sounds from the remote computer
		UNMUTE_MESSAGE = _("Unmuted remote")
		status = MUTE_MESSAGE if self.localMachine.isMuted else UNMUTE_MESSAGE
		ui.message(status)

	def pushClipboard(self):
		"""Send local clipboard content to the remote computer.

		:note: Requires an active connection
		:raises TypeError: If clipboard content cannot be serialized
		"""
		connector = self.followerTransport or self.leaderTransport
		if not getattr(connector, "connected", False):
			# Translators: Message shown when trying to send the clipboard to the remote computer while not connected.
			ui.message(pgettext("remote", "Not connected"))
			return
		elif self.connectedClientsCount < 1:
			# Translators: Reported when performing a Remote Access action, but there are no other computers in the channel.
			ui.message(pgettext("remote", "No one else is connected"))
			return
		try:
			connector.send(RemoteMessageType.SET_CLIPBOARD_TEXT, text=api.getClipData())
			cues.clipboardPushed()
		except (TypeError, OSError):
			log.debug("Unable to push clipboard", exc_info=True)
			# Translators: Message shown when clipboard content cannot be sent to the remote computer.
			ui.message(pgettext("remote", "Unable to send clipboard"))

	def copyLink(self):
		"""Copy connection URL to clipboard.

		:note: Requires an active session
		"""
		session = self.leaderSession or self.followerSession
		if session is None:
			# Translators: Message shown when trying to copy the link to connect to the remote computer while not connected.
			ui.message(pgettext("remote", "Not connected"))
			return
		url = session.getConnectionInfo().getURLToConnect()
		api.copyToClip(str(url))

	def sendSAS(self):
		"""Send Secure Attention Sequence to remote computer.

		:note: Requires an active leader transport connection
		"""
		if self.leaderTransport is None:
			log.error("No leader transport to send SAS")
			return
		self.leaderTransport.send(RemoteMessageType.SEND_SAS)

	def connect(self, connectionInfo: ConnectionInfo):
		"""Establish connection based on connection info.

		:param connectionInfo: Connection details including mode, host, port etc.
		:note: Initiates either leader or follower connection based on mode
		"""
		log.info(
			f"Initiating connection as {connectionInfo.mode} to {connectionInfo.hostname}:{connectionInfo.port}",
		)
		if connectionInfo.mode == ConnectionMode.LEADER:
			self.connectAsLeader(connectionInfo)
		elif connectionInfo.mode == ConnectionMode.FOLLOWER:
			self.connectAsFollower(connectionInfo)

	def disconnect(self):
		"""Close all active connections and clean up resources.

		:note: Closes local control server and both leader/follower sessions if active
		"""
		if self.leaderSession is None and self.followerSession is None:
			log.debug("Disconnect called but no active sessions")
			return
		log.info("Disconnecting from remote session")
		if self.localControlServer is not None:
			self.localControlServer.close()
			self.localControlServer = None
		if self.leaderSession is not None:
			self.disconnectAsLeader()
		if self.followerSession is not None:
			self.disconnectAsFollower()
		cues.disconnected()

	def disconnectAsLeader(self):
		"""Close leader session and clean up related resources."""
		self.leaderSession.close()
		self.leaderSession = None
		self.leaderTransport = None

	def disconnectAsFollower(self):
		"""Close follower session and clean up related resources."""
		self.followerSession.close()
		self.followerSession = None
		self.followerTransport = None
		self.sdHandler.followerSession = None

	@alwaysCallAfter
	def onConnectAsLeaderFailed(self):
		if self.leaderTransport.successfulConnects == 0:
			log.error(f"Failed to connect to {self.leaderTransport.address}")
			self.disconnectAsLeader()
			# Translators: Title of the connection error dialog.
			gui.messageBox(
				parent=gui.mainFrame,
				# Translators: Title of the connection error dialog.
				caption=_("Error Connecting"),
				# Translators: Message shown when unable to connect to the remote computer.
				message=_("Unable to connect to the remote computer"),
				style=wx.OK | wx.ICON_WARNING,
			)

	def doConnect(self, evt: inputCore.InputGesture = None):
		"""Show connection dialog and handle connection initiation.

		:param evt: Optional wx event object
		:note: Displays dialog with previous connections list
		"""
		if evt is not None:
			evt.Skip()
		if globalVars.appArgs.secure:
			log.error(
				"Creating new Remote Access connections is not allowed in Secure Mode.",
				stack_info=True,
			)
			return
		previousConnections = configuration.getRemoteConfig()["connections"]["lastConnected"]
		hostnames = list(reversed(previousConnections))
		dlg = dialogs.DirectConnectDialog(
			parent=gui.mainFrame,
			id=wx.ID_ANY,
			# Translators: Title of the Remote Access connection dialog.
			title=pgettext("remote", "Connect to Another Computer"),
			hostnames=hostnames,
		)

		def handleDialogCompletion(dlgResult):
			if dlgResult != wx.ID_OK:
				return
			connectionInfo = dlg.getConnectionInfo()
			if dlg._clientOrServerControl.GetSelection() == 1:  # server
				self.startControlServer(connectionInfo.port, connectionInfo.key)
			self.connect(connectionInfo=connectionInfo)

		gui.runScriptModalDialog(dlg, callback=handleDialogCompletion)

	def connectAsLeader(self, connectionInfo: ConnectionInfo):
		transport = RelayTransport.create(
			connectionInfo=connectionInfo,
			serializer=serializer.JSONSerializer(),
		)
		self.leaderSession = LeaderSession(
			transport=transport,
			localMachine=self.localMachine,
		)
		transport.transportCertificateAuthenticationFailed.register(
			self.onLeaderCertificateFailed,
		)
		transport.transportConnected.register(self.onConnectedAsLeader)
		transport.transportConnectionFailed.register(self.onConnectAsLeaderFailed)
		transport.transportClosing.register(self.onDisconnectingAsLeader)
		transport.transportDisconnected.register(self.onDisconnectedAsLeader)
		transport.reconnectorThread.start()
		self.leaderTransport = transport
		if self.menu:
			self.menu.handleConnecting(connectionInfo.mode)

	@alwaysCallAfter
	def onConnectedAsLeader(self):
		log.info("Successfully connected as leader")
		configuration.writeConnectionToConfig(self.leaderSession.getConnectionInfo())
		if self.menu:
			self.menu.handleConnected(ConnectionMode.LEADER, True)
		ui.message(
			# Translators: Presented when connected to the remote computer.
			_("Connected"),
		)
		cues.connected()

	@alwaysCallAfter
	def onDisconnectingAsLeader(self):
		log.info("Leader session disconnecting")
		if self.menu:
			self.menu.handleConnected(ConnectionMode.LEADER, False)
		if self.localMachine:
			self.localMachine.isMuted = False
		self.sendingKeys = False
		self.keyModifiers = set()

	@alwaysCallAfter
	def onDisconnectedAsLeader(self):
		log.info("Leader session disconnected")
		# Translators: Presented when connection to a remote computer was interupted.
		ui.message(_("Disconnected"))

	def connectAsFollower(self, connectionInfo: ConnectionInfo):
		transport = RelayTransport.create(
			connectionInfo=connectionInfo,
			serializer=serializer.JSONSerializer(),
		)
		self.followerSession = FollowerSession(
			transport=transport,
			localMachine=self.localMachine,
		)
		self.sdHandler.followerSession = self.followerSession
		self.followerTransport = transport
		transport.transportCertificateAuthenticationFailed.register(
			self.onFollowerCertificateFailed,
		)
		transport.transportConnected.register(self.onConnectedAsFollower)
		transport.transportDisconnected.register(self.onDisconnectedAsFollower)
		transport.reconnectorThread.start()
		if self.menu:
			self.menu.handleConnecting(connectionInfo.mode)

	@alwaysCallAfter
	def onConnectedAsFollower(self):
		log.info("Control connector connected")
		cues.controlServerConnected()
		if self.menu:
			self.menu.handleConnected(ConnectionMode.FOLLOWER, True)
		configuration.writeConnectionToConfig(self.followerSession.getConnectionInfo())

	@alwaysCallAfter
	def onDisconnectedAsFollower(self):
		log.info("Control connector disconnected")
		if self.menu:
			self.menu.handleConnected(ConnectionMode.FOLLOWER, False)

	### certificate handling

	def handleCertificateFailure(self, transport: RelayTransport):
		log.warning(f"Certificate validation failed for {transport.address}")
		self.lastFailAddress = transport.address
		self.lastFailKey = transport.channel
		self.disconnect()
		try:
			certHash = transport.lastFailFingerprint

			wnd = dialogs.CertificateUnauthorizedDialog(None, fingerprint=certHash)
			a = wnd.ShowModal()
			if a == wx.ID_YES:
				config = configuration.getRemoteConfig()
				config["trustedCertificates"][hostPortToAddress(self.lastFailAddress)] = certHash
			if a == wx.ID_YES or a == wx.ID_NO:
				return True
		except Exception as ex:
			log.error(ex)
		return False

	@alwaysCallAfter
	def onLeaderCertificateFailed(self):
		if self.handleCertificateFailure(self.leaderSession.transport):
			connectionInfo = ConnectionInfo(
				mode=ConnectionMode.LEADER,
				hostname=self.lastFailAddress[0],
				port=self.lastFailAddress[1],
				key=self.lastFailKey,
				insecure=True,
			)
			self.connectAsLeader(connectionInfo=connectionInfo)

	@alwaysCallAfter
	def onFollowerCertificateFailed(self):
		if self.handleCertificateFailure(self.followerSession.transport):
			connectionInfo = ConnectionInfo(
				mode=ConnectionMode.FOLLOWER,
				hostname=self.lastFailAddress[0],
				port=self.lastFailAddress[1],
				key=self.lastFailKey,
				insecure=True,
			)
			self.connectAsFollower(connectionInfo=connectionInfo)

	def startControlServer(self, serverPort, channel):
		"""Start local relay server for handling connections.

		:param serverPort: Port number to listen on
		:param channel: Channel key for authentication
		:note: Creates daemon thread to run server
		"""
		self.localControlServer = server.LocalRelayServer(serverPort, channel)
		serverThread = threading.Thread(target=self.localControlServer.run)
		serverThread.daemon = True
		serverThread.start()

	def processKeyInput(
		self,
		vkCode: int | None = None,
		scanCode: int | None = None,
		extended: bool | None = None,
		pressed: bool | None = None,
	) -> bool:
		"""Process keyboard input and forward to remote if sending keys.

		:param vkCode: Virtual key code
		:param scanCode: Scan code
		:param extended: Whether this is an extended key
		:param pressed: True if key pressed, False if released
		:return: ``True`` to allow local processing, ``False`` to block
		"""
		if not self.sendingKeys:
			return True
		keyCode = (vkCode, extended)
		gesture = KeyboardInputGesture(
			self.keyModifiers,
			keyCode[0],
			scanCode,
			keyCode[1],
		)
		if not pressed and keyCode in self.hostPendingModifiers:
			self.hostPendingModifiers.discard(keyCode)
			return True
		gesture = KeyboardInputGesture(
			self.keyModifiers,
			keyCode[0],
			scanCode,
			keyCode[1],
		)
		if gesture.isModifier:
			if pressed:
				self.keyModifiers.add(keyCode)
			else:
				self.keyModifiers.discard(keyCode)
		elif pressed:
			script = gesture.script
			if script in self.localScripts:
				wx.CallAfter(script, gesture)
				return False
		self.leaderTransport.send(
			RemoteMessageType.KEY,
			vk_code=vkCode,
			extended=extended,
			pressed=pressed,
			scan_code=scanCode,
		)
		return False  # Don't pass it on

	def toggleRemoteKeyControl(self, gesture: KeyboardInputGesture):
		"""Toggle sending keyboard input to remote machine.

		:param gesture: The keyboard gesture that triggered this
		:note: Also toggles braille input and mute state
		"""
		if not self.isConnected():
			# Translators: A message indicating that the remote client is not connected.
			ui.message(pgettext("remote", "Not connected"))
			return
		elif not self.leaderTransport:
			# Translators: Presented when attempting to switch to controling a remote computer when connected as the controlled computer.
			ui.message(pgettext("remote", "Not the controlling computer"))
			return
		elif self.leaderSession.connectedFollowersCount < 1 and not self.sendingKeys:
			# Translators: Presented when attempting to switch to controling a remote computer when there are no controllable computers in the channel.
			ui.message(pgettext("remote", "No controlled computers are connected"))
			return
		if self.sendingKeys:
			self._switchToLocalControl()
		else:
			self._switchToRemoteControl(gesture)

	def _switchToLocalControl(self) -> None:
		"""Switch to controlling the local computer."""
		self.sendingKeys = False
		log.info("Remote key control disabled")
		self.setReceivingBraille(False)
		self.releaseKeys()
		# Translators: Presented when keyboard control is back to the controlling computer.
		ui.message(pgettext("remote", "Controlling local computer"))

	def _switchToRemoteControl(self, gesture: KeyboardInputGesture) -> None:
		"""Switch to controlling the remote computer."""
		self.sendingKeys = True
		log.info("Remote key control enabled")
		self.setReceivingBraille(self.sendingKeys)
		self.hostPendingModifiers = gesture.modifiers
		# Translators: Presented when sending keyboard keys from the controlling computer to the controlled computer.
		ui.message(pgettext("remote", "Controlling remote computer"))
		if self.localMachine.isMuted:
			self.toggleMute()

	def releaseKeys(self):
		"""Release all pressed keys on the remote machine.

		:note: Sends key-up events for all held modifiers
		"""
		# release all pressed keys in the guest.
		for k in self.keyModifiers:
			self.leaderTransport.send(
				RemoteMessageType.KEY,
				vk_code=k[0],
				extended=k[1],
				pressed=False,
			)
		self.keyModifiers = set()

	def setReceivingBraille(self, state):
		"""Enable or disable receiving braille from remote.

		:param state: True to enable remote braille, False to disable
		:note: Only enables if leader session and braille handler are ready
		"""
		if state and self.leaderSession.callbacksAdded and braille.handler.enabled:
			self.leaderSession.registerBrailleInput()
			self.localMachine.receivingBraille = True
		elif not state:
			self.leaderSession.unregisterBrailleInput()
			self.localMachine.receivingBraille = False

	@alwaysCallAfter
	def verifyAndConnect(self, conInfo: ConnectionInfo):
		"""Verify connection details and establish connection if approved by user.

		:param conInfo: Connection information to verify and use
		:note: Shows confirmation dialog before connecting
		:raises: Displays error if already connected
		"""
		if self.isConnected() or self.connecting:
			gui.messageBox(
				pgettext(
					"remote",
					# Translators: Message shown when trying to connect while already connected.
					"A Remote Access session is already in progress. Disconnect before starting a new session.",
				),
				# Translators: Title of the connection error dialog.
				pgettext("remote", "Already Connected"),
				wx.OK | wx.ICON_WARNING,
			)
			return

		self.connecting = True
		try:
			serverAddr = conInfo.getAddress()
			key = conInfo.key

			# Prepare connection request message based on mode
			if conInfo.mode == ConnectionMode.LEADER:
				question = pgettext(
					"remote",
					# Translators: Ask the user if they want to control the remote computer.
					"Do you wish to control the computer on server {server} with key {key}?",
				)
			else:
				question = pgettext(
					"remote",
					# Translators: Ask the user if they want to allow the remote computer to control this computer.
					"Do you wish to allow this computer to be controlled on server {server} with key {key}?",
				)

			question = question.format(server=serverAddr, key=key)

			# Translators: Title of the connection request dialog.
			dialogTitle = pgettext("remote", "Remote Access Connection Request")

			# Show confirmation dialog
			if (
				gui.messageBox(
					question,
					dialogTitle,
					wx.YES | wx.NO | wx.NO_DEFAULT | wx.ICON_WARNING,
				)
				== wx.YES
			):
				self.connect(conInfo)
		finally:
			self.connecting = False

	def isConnected(self) -> bool:
		"""Check if there is an active connection.

		:return: True if either follower or leader transport is connected
		"""
		connector = self.followerTransport or self.leaderTransport
		if connector is not None:
			return connector.connected
		return False

	def registerLocalScript(self, script: scriptHandler._ScriptFunctionT):
		"""Add a script to be handled locally instead of sent to remote.

		:param script: Script function to register
		"""
		self.localScripts.add(script)

	def unregisterLocalScript(self, script: scriptHandler._ScriptFunctionT):
		"""Remove a script from local handling.

		:param script: Script function to unregister
		"""
		self.localScripts.discard(script)

	@property
	def connectedClientsCount(self) -> int:
		if not self.isConnected():
			return 0
		elif self.leaderSession is not None:
			return self.leaderSession.connectedClientsCount
		elif self.followerSession is not None:
			return self.followerSession.connectedClientsCount
		log.error(
			"is connected returned true, but neither leaderSession or followerSession is not None.",
			stack_info=True,
		)
		return 0
