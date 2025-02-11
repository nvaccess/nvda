# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import threading
from typing import Callable, Optional, Set, Tuple

import api
import braille
import core
import gui
import inputCore
import ui
import wx
from config import isInstalledCopy
from keyboardHandler import KeyboardInputGesture
from logHandler import log
from gui.guiHelper import alwaysCallAfter
from utils.security import isRunningOnSecureDesktop

from . import configuration, cues, dialogs, serializer, server, urlHandler
from .connectionInfo import ConnectionInfo, ConnectionMode
from .localMachine import LocalMachine
from .menu import RemoteMenu
from .protocol import RemoteMessageType, addressToHostPort
from .secureDesktop import SecureDesktopHandler
from .session import MasterSession, FollowerSession
from .protocol import hostPortToAddress
from .transport import RelayTransport

# Type aliases
KeyModifier = Tuple[int, bool]  # (vk_code, extended)
Address = Tuple[str, int]  # (hostname, port)


class RemoteClient:
	localScripts: Set[Callable]
	localMachine: LocalMachine
	masterSession: Optional[MasterSession]
	followerSession: Optional[FollowerSession]
	keyModifiers: Set[KeyModifier]
	hostPendingModifiers: Set[KeyModifier]
	connecting: bool
	masterTransport: Optional[RelayTransport]
	slaveTransport: Optional[RelayTransport]
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
		self.masterSession = None
		self.menu: Optional[RemoteMenu] = None
		if not isRunningOnSecureDesktop():
			self.menu: Optional[RemoteMenu] = RemoteMenu(self)
		self.connecting = False
		urlHandler.registerURLHandler()
		self.masterTransport = None
		self.slaveTransport = None
		self.localControlServer = None
		self.sendingKeys = False
		self.sdHandler = SecureDesktopHandler()
		if isRunningOnSecureDesktop():
			connection = self.sdHandler.initializeSecureDesktop()
			if connection:
				self.connectAsSlave(connection)
				self.followerSession.transport.connectedEvent.wait(
					self.sdHandler.SD_CONNECT_BLOCK_TIMEOUT,
				)
		core.postNvdaStartup.register(self.performAutoconnect)
		inputCore.decide_handleRawKey.register(self.processKeyInput)

	def performAutoconnect(self):
		controlServerConfig = configuration.get_config()["controlserver"]
		if not controlServerConfig["autoconnect"] or self.masterSession or self.followerSession:
			log.debug("Autoconnect disabled or already connected")
			return
		key = controlServerConfig["key"]
		insecure = False
		if controlServerConfig["self_hosted"]:
			port = controlServerConfig["port"]
			hostname = "localhost"
			insecure = True
			self.startControlServer(port, key)
		else:
			address = addressToHostPort(controlServerConfig["host"])
			hostname, port = address
		mode = ConnectionMode.SLAVE if controlServerConfig["connection_type"] == 0 else ConnectionMode.MASTER
		conInfo = ConnectionInfo(mode=mode, hostname=hostname, port=port, key=key, insecure=insecure)
		self.connect(conInfo)

	def terminate(self):
		self.sdHandler.terminate()
		self.disconnect()
		self.localMachine.terminate()
		self.localMachine = None
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
		self.localMachine.isMuted = not self.localMachine.isMuted
		self.menu.muteItem.Check(self.localMachine.isMuted)
		# Translators: Displayed when muting speech and sounds from the remote computer
		mute_msg = _("Mute speech and sounds from the remote computer")
		# Translators: Displayed when unmuting speech and sounds from the remote computer
		unmute_msg = _("Unmute speech and sounds from the remote computer")
		status = mute_msg if self.localMachine.isMuted else unmute_msg
		ui.message(status)

	def pushClipboard(self):
		"""Send local clipboard content to the remote computer.

		:note: Requires an active connection
		:raises TypeError: If clipboard content cannot be serialized
		"""
		connector = self.slaveTransport or self.masterTransport
		if not getattr(connector, "connected", False):
			# Translators: Message shown when trying to push the clipboard to the remote computer while not connected.
			ui.message(_("Not connected."))
			return
		try:
			connector.send(RemoteMessageType.SET_CLIPBOARD_TEXT, text=api.getClipData())
			cues.clipboardPushed()
		except TypeError:
			log.exception("Unable to push clipboard")
			# Translators: Message shown when clipboard content cannot be sent to the remote computer.
			ui.message(_("Unable to push clipboard"))

	def copyLink(self):
		"""Copy connection URL to clipboard.

		:note: Requires an active session
		"""
		session = self.masterSession or self.followerSession
		if session is None:
			# Translators: Message shown when trying to copy the link to connect to the remote computer while not connected.
			ui.message(_("Not connected."))
			return
		url = session.getConnectionInfo().getURLToConnect()
		api.copyToClip(str(url))

	def sendSAS(self):
		"""Send Secure Attention Sequence to remote computer.

		:note: Requires an active master transport connection
		"""
		if self.masterTransport is None:
			log.error("No master transport to send SAS")
			return
		self.masterTransport.send(RemoteMessageType.SEND_SAS)

	def connect(self, connectionInfo: ConnectionInfo):
		"""Establish connection based on connection info.

		:param connectionInfo: Connection details including mode, host, port etc.
		:note: Initiates either master or slave connection based on mode
		"""
		log.info(
			f"Initiating connection as {connectionInfo.mode} to {connectionInfo.hostname}:{connectionInfo.port}",
		)
		if connectionInfo.mode == ConnectionMode.MASTER:
			self.connectAsMaster(connectionInfo)
		elif connectionInfo.mode == ConnectionMode.SLAVE:
			self.connectAsSlave(connectionInfo)

	def disconnect(self):
		"""Close all active connections and clean up resources.

		:note: Closes local control server and both master/slave sessions if active
		"""
		if self.masterSession is None and self.followerSession is None:
			log.debug("Disconnect called but no active sessions")
			return
		log.info("Disconnecting from remote session")
		if self.localControlServer is not None:
			self.localControlServer.close()
			self.localControlServer = None
		if self.masterSession is not None:
			self.disconnectAsMaster()
		if self.followerSession is not None:
			self.disconnectAsSlave()
		cues.disconnected()

	def disconnectAsMaster(self):
		"""Close master session and clean up related resources."""
		self.masterSession.close()
		self.masterSession = None
		self.masterTransport = None

	def disconnectAsSlave(self):
		"""Close slave session and clean up related resources."""
		self.followerSession.close()
		self.followerSession = None
		self.slaveTransport = None
		self.sdHandler.followerSession = None

	@alwaysCallAfter
	def onConnectAsMasterFailed(self):
		if self.masterTransport.successfulConnects == 0:
			log.error(f"Failed to connect to {self.masterTransport.address}")
			self.disconnectAsMaster()
			# Translators: Title of the connection error dialog.
			gui.messageBox(
				parent=gui.mainFrame,
				# Translators: Title of the connection error dialog.
				caption=_("Error Connecting"),
				# Translators: Message shown when cannot connect to the remote computer.
				message=_("Unable to connect to the remote computer"),
				style=wx.OK | wx.ICON_WARNING,
			)

	def doConnect(self, evt=None):
		"""Show connection dialog and handle connection initiation.

		:param evt: Optional wx event object
		:note: Displays dialog with previous connections list
		"""
		if evt is not None:
			evt.Skip()
		previousConnections = configuration.get_config()["connections"]["last_connected"]
		hostnames = list(reversed(previousConnections))
		# Translators: Title of the connect dialog.
		dlg = dialogs.DirectConnectDialog(
			parent=gui.mainFrame,
			id=wx.ID_ANY,
			# Translators: Title of the connect dialog.
			title=_("Connect"),
			hostnames=hostnames,
		)

		def handleDialogCompletion(dlgResult):
			if dlgResult != wx.ID_OK:
				return
			connectionInfo = dlg.getConnectionInfo()
			if dlg.clientOrServer.GetSelection() == 1:  # server
				self.startControlServer(connectionInfo.port, connectionInfo.key)
			self.connect(connectionInfo=connectionInfo)

		gui.runScriptModalDialog(dlg, callback=handleDialogCompletion)

	def connectAsMaster(self, connectionInfo: ConnectionInfo):
		transport = RelayTransport.create(
			connection_info=connectionInfo,
			serializer=serializer.JSONSerializer(),
		)
		self.masterSession = MasterSession(
			transport=transport,
			localMachine=self.localMachine,
		)
		transport.transportCertificateAuthenticationFailed.register(
			self.onMasterCertificateFailed,
		)
		transport.transportConnected.register(self.onConnectedAsMaster)
		transport.transportConnectionFailed.register(self.onConnectAsMasterFailed)
		transport.transportClosing.register(self.onDisconnectingAsMaster)
		transport.transportDisconnected.register(self.onDisconnectedAsMaster)
		transport.reconnectorThread.start()
		self.masterTransport = transport
		if self.menu:
			self.menu.handleConnecting(connectionInfo.mode)

	@alwaysCallAfter
	def onConnectedAsMaster(self):
		log.info("Successfully connected as master")
		configuration.write_connection_to_config(self.masterSession.getConnectionInfo())
		if self.menu:
			self.menu.handleConnected(ConnectionMode.MASTER, True)
		ui.message(
			# Translators: Presented when connected to the remote computer.
			_("Connected!"),
		)
		cues.connected()

	@alwaysCallAfter
	def onDisconnectingAsMaster(self):
		log.info("Master session disconnecting")
		if self.menu:
			self.menu.handleConnected(ConnectionMode.MASTER, False)
		if self.localMachine:
			self.localMachine.isMuted = False
		self.sendingKeys = False
		self.keyModifiers = set()

	@alwaysCallAfter
	def onDisconnectedAsMaster(self):
		log.info("Master session disconnected")
		# Translators: Presented when connection to a remote computer was interupted.
		ui.message(_("Connection interrupted"))

	def connectAsSlave(self, connectionInfo: ConnectionInfo):
		transport = RelayTransport.create(
			connection_info=connectionInfo,
			serializer=serializer.JSONSerializer(),
		)
		self.followerSession = FollowerSession(
			transport=transport,
			localMachine=self.localMachine,
		)
		self.sdHandler.followerSession = self.followerSession
		self.slaveTransport = transport
		transport.transportCertificateAuthenticationFailed.register(
			self.onSlaveCertificateFailed,
		)
		transport.transportConnected.register(self.onConnectedAsSlave)
		transport.transportDisconnected.register(self.onDisconnectedAsSlave)
		transport.reconnectorThread.start()
		if self.menu:
			self.menu.handleConnecting(connectionInfo.mode)

	@alwaysCallAfter
	def onConnectedAsSlave(self):
		log.info("Control connector connected")
		cues.controlServerConnected()
		if self.menu:
			self.menu.handleConnected(ConnectionMode.SLAVE, True)
		configuration.write_connection_to_config(self.followerSession.getConnectionInfo())

	@alwaysCallAfter
	def onDisconnectedAsSlave(self):
		log.info("Control connector disconnected")
		# cues.control_server_disconnected()
		if self.menu:
			self.menu.handleConnected(ConnectionMode.SLAVE, False)

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
				config = configuration.get_config()
				config["trusted_certs"][hostPortToAddress(self.lastFailAddress)] = certHash
			if a == wx.ID_YES or a == wx.ID_NO:
				return True
		except Exception as ex:
			log.error(ex)
		return False

	@alwaysCallAfter
	def onMasterCertificateFailed(self):
		if self.handleCertificateFailure(self.masterSession.transport):
			connectionInfo = ConnectionInfo(
				mode=ConnectionMode.MASTER,
				hostname=self.lastFailAddress[0],
				port=self.lastFailAddress[1],
				key=self.lastFailKey,
				insecure=True,
			)
			self.connectAsMaster(connectionInfo=connectionInfo)

	@alwaysCallAfter
	def onSlaveCertificateFailed(self):
		if self.handleCertificateFailure(self.followerSession.transport):
			connectionInfo = ConnectionInfo(
				mode=ConnectionMode.SLAVE,
				hostname=self.lastFailAddress[0],
				port=self.lastFailAddress[1],
				key=self.lastFailKey,
				insecure=True,
			)
			self.connectAsSlave(connectionInfo=connectionInfo)

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

	def processKeyInput(self, vkCode=None, scanCode=None, extended=None, pressed=None):
		"""Process keyboard input and forward to remote if sending keys.

		:param vkCode: Virtual key code
		:param scanCode: Scan code
		:param extended: Whether this is an extended key
		:param pressed: True if key pressed, False if released
		:return: True to allow local processing, False to block
		:rtype: bool
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
		self.masterTransport.send(
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
		if not self.masterTransport:
			gesture.send()
			return
		self.sendingKeys = not self.sendingKeys
		log.info(f"Remote key control {'enabled' if self.sendingKeys else 'disabled'}")
		self.setReceivingBraille(self.sendingKeys)
		if self.sendingKeys:
			self.hostPendingModifiers = gesture.modifiers
			# Translators: Presented when sending keyboard keys from the controlling computer to the controlled computer.
			ui.message(_("Controlling remote machine."))
			if self.localMachine.isMuted:
				self.toggleMute()
		else:
			self.releaseKeys()
			# Translators: Presented when keyboard control is back to the controlling computer.
			ui.message(_("Controlling local machine."))

	def releaseKeys(self):
		"""Release all pressed keys on the remote machine.

		:note: Sends key-up events for all held modifiers
		"""
		# release all pressed keys in the guest.
		for k in self.keyModifiers:
			self.masterTransport.send(
				RemoteMessageType.KEY,
				vk_code=k[0],
				extended=k[1],
				pressed=False,
			)
		self.keyModifiers = set()

	def setReceivingBraille(self, state):
		"""Enable or disable receiving braille from remote.

		:param state: True to enable remote braille, False to disable
		:note: Only enables if master session and braille handler are ready
		"""
		if state and self.masterSession.callbacksAdded and braille.handler.enabled:
			self.masterSession.registerBrailleInput()
			self.localMachine.receivingBraille = True
		elif not state:
			self.masterSession.unregisterBrailleInput()
			self.localMachine.receivingBraille = False

	@alwaysCallAfter
	def verifyAndConnect(self, conInfo: ConnectionInfo):
		"""Verify connection details and establish connection if approved by user.

		:param conInfo: Connection information to verify and use
		:note: Shows confirmation dialog before connecting
		:raises: Displays error if already connected
		"""
		if self.isConnected() or self.connecting:
			# Translators: Message shown when trying to connect while already connected.
			error_msg = _("NVDA Remote is already connected. Disconnect before opening a new connection.")
			# Translators: Title of the connection error dialog.
			error_title = _("NVDA Remote Already Connected")
			gui.messageBox(error_msg, error_title, wx.OK | wx.ICON_WARNING)
			return

		self.connecting = True
		try:
			serverAddr = conInfo.getAddress()
			key = conInfo.key

			# Prepare connection request message based on mode
			if conInfo.mode == ConnectionMode.MASTER:
				# Translators: Ask the user if they want to control the remote computer.
				question = _("Do you wish to control the machine on server {server} with key {key}?")
			else:
				question = _(
					# Translators: Ask the user if they want to allow the remote computer to control this computer.
					"Do you wish to allow this machine to be controlled on server {server} with key {key}?",
				)

			question = question.format(server=serverAddr, key=key)

			# Translators: Title of the connection request dialog.
			dialogTitle = _("NVDA Remote Connection Request")

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

	def isConnected(self):
		"""Check if there is an active connection.

		:return: True if either slave or master transport is connected
		:rtype: bool
		"""
		connector = self.slaveTransport or self.masterTransport
		if connector is not None:
			return connector.connected
		return False

	def registerLocalScript(self, script):
		"""Add a script to be handled locally instead of sent to remote.

		:param script: Script function to register
		"""
		self.localScripts.add(script)

	def unregisterLocalScript(self, script):
		"""Remove a script from local handling.

		:param script: Script function to unregister
		"""
		self.localScripts.discard(script)
