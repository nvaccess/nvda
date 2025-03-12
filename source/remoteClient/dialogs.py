# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import json
import random
import threading
from typing import List, Optional, TypedDict
from urllib import request

import gui
import wx
from wx.lib.expando import ExpandoTextCtrl
from logHandler import log
from gui.guiHelper import alwaysCallAfter, BoxSizerHelper
from gui import guiHelper
from gui.nvdaControls import SelectOnFocusSpinCtrl

from . import configuration, serializer, server, protocol, transport
from .connectionInfo import ConnectionInfo, ConnectionMode
from .protocol import SERVER_PORT, RemoteMessageType


class ClientPanel(wx.Panel):
	host: wx.ComboBox
	key: wx.TextCtrl
	generateKey: wx.Button
	keyConnector: Optional["transport.RelayTransport"]

	def __init__(self, parent: Optional[wx.Window] = None, id: int = wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = BoxSizerHelper(self, sizer=sizer)
		self.host = sizerHelper.addLabeledControl(
			# Translators: The label of an edit field in connect dialog to enter name or address of the remote computer.
			_("&Host:"),
			wx.ComboBox,
		)
		# Translators: The label of an edit field in connect dialog to enter name or address of the remote computer.
		# sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		# self.host = wx.ComboBox(self, wx.ID_ANY)
		# sizer.Add(self.host)
		self.key = sizerHelper.addLabeledControl(
			# Translators: Label of the edit field to enter key (password) to secure the remote connection.
			_("&Key:"),
			wx.TextCtrl,
		)
		# Translators: Label of the edit field to enter key (password) to secure the remote connection.
		# sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		# self.key = wx.TextCtrl(self, wx.ID_ANY)
		# sizer.Add(self.key)
		# Translators: The button used to generate a random key/password.
		self.generateKey = wx.Button(parent=self, label=_("&Generate Key"))
		self.generateKey.Bind(wx.EVT_BUTTON, self.onGenerateKey)
		keyControlsSizerHelper = BoxSizerHelper(self, sizer=self.key.GetContainingSizer())
		keyControlsSizerHelper.addItem(self.generateKey)
		# sizer.Add(self.generateKey)
		self.SetSizerAndFit(sizer)

	def onGenerateKey(self, evt: wx.CommandEvent) -> None:
		if not self.host.GetValue():
			gui.messageBox(
				# Translators: A message box displayed when the host field is empty and the user tries to generate a key.
				_("Host must be set."),
				# Translators: A title of a message box displayed when the host field is empty and the user tries to generate a key.
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)
			self.host.SetFocus()
		else:
			evt.Skip()
			self.generateKeyCommand()

	def generateKeyCommand(self, insecure: bool = False) -> None:
		address = protocol.addressToHostPort(self.host.GetValue())
		self.keyConnector = transport.RelayTransport(
			address=address,
			serializer=serializer.JSONSerializer(),
			insecure=insecure,
		)
		self.keyConnector.registerInbound(RemoteMessageType.GENERATE_KEY, self.handleKeyGenerated)
		self.keyConnector.transportCertificateAuthenticationFailed.register(self.handleCertificateFailed)
		t = threading.Thread(target=self.keyConnector.run)
		t.start()

	@alwaysCallAfter
	def handleKeyGenerated(self, key: Optional[str] = None) -> None:
		self.key.SetValue(key)
		self.key.SetFocus()
		self.keyConnector.close()
		self.keyConnector = None

	@alwaysCallAfter
	def handleCertificateFailed(self) -> None:
		"""
		Handles the event when a certificate validation fails.

		This method attempts to retrieve the last failed certificate fingerprint
		and displays a dialog to the user to decide whether to trust the certificate.
		If the user chooses to trust the certificate, it is added to the trusted certificates
		configuration. If an exception occurs during this process, it is logged.

		Steps:
		1. Retrieve the last failed certificate fingerprint.
		2. Display a dialog to the user with the certificate fingerprint.
		3. If the user chooses to trust the certificate, add it to the trusted certificates configuration.
		4. Handle any exceptions by logging the error.
		5. Close the key connector and reset it.
		6. Generate a new key from the server.
		"""
		try:
			certHash = self.keyConnector.lastFailFingerprint

			wnd = CertificateUnauthorizedDialog(None, fingerprint=certHash)
			a = wnd.ShowModal()
			if a == wx.ID_YES:
				config = configuration.getRemoteConfig()
				config["trusted_certs"][self.host.GetValue()] = certHash
			if a != wx.ID_YES and a != wx.ID_NO:
				return
		except Exception:
			log.exception("Error handling certificate failure")
			return
		finally:
			self.keyConnector.close()
			self.keyConnector = None
		self.generateKeyCommand(True)


class PortCheckResponse(TypedDict):
	host: str
	port: int
	open: bool


class ServerPanel(wx.Panel):
	getIP: wx.Button
	externalIP: wx.TextCtrl
	port: wx.TextCtrl
	key: wx.TextCtrl
	generateKey: wx.Button

	def __init__(self, parent: Optional[wx.Window] = None, id: int = wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = BoxSizerHelper(self, sizer=sizer)
		self.externalIP = sizerHelper.addLabeledControl(
			# Translators: Label of the field displaying the external IP address if using direct (client to server) connection.
			_("`ternal IP:"),
			ExpandoTextCtrl,
			style=wx.TE_READONLY,
		)
		# Translators: Used in server mode to obtain the external IP address for the server (controlled computer) for direct connection.
		self.getIP = wx.Button(parent=self, label=_("Get External &IP"))
		self.getIP.Bind(wx.EVT_BUTTON, self.onGetIP)
		externalIPControlsSizerHelper = BoxSizerHelper(self, sizer=self.externalIP.GetContainingSizer())
		externalIPControlsSizerHelper.addItem(self.getIP)
		# Translators: Used in server mode to obtain the external IP address for the server (controlled computer) for direct connection.
		# self.getIP = wx.Button(parent=self, label=_("Get External &IP"))
		# self.getIP.Bind(wx.EVT_BUTTON, self.onGetIP)
		# sizer.Add(self.getIP)
		# Translators: Label of the field displaying the external IP address if using direct (client to server) connection.
		# sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&External IP:")))
		# self.externalIP = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY | wx.TE_MULTILINE)
		# sizer.Add(self.externalIP)
		# Translators: The label of an edit field in connect dialog to enter the port the server will listen on.
		self.port = sizerHelper.addLabeledControl(
			_("&Port:"),
			SelectOnFocusSpinCtrl,
			min=1,
			max=65535,
			initial=SERVER_PORT,
		)
		# Translators: The label of an edit field in connect dialog to enter the port the server will listen on.
		# sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Port:")))
		# self.port = wx.TextCtrl(self, wx.ID_ANY, value=str(SERVER_PORT))
		# sizer.Add(self.port)
		# Translators: Label of the edit field to enter key (password) to secure the remote connection.
		self.key = sizerHelper.addLabeledControl(_("&Key"), wx.TextCtrl)
		# sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		# self.key = wx.TextCtrl(self, wx.ID_ANY)
		# sizer.Add(self.key)
		self.generateKey = wx.Button(parent=self, label=_("&Generate Key"))
		self.generateKey.Bind(wx.EVT_BUTTON, self.onGenerateKey)
		keyControlsSizerHelper = BoxSizerHelper(self, sizer=self.key.GetContainingSizer())
		keyControlsSizerHelper.addItem(self.generateKey)
		# sizer.Add(self.generateKey)
		self.SetSizerAndFit(sizer)

	def onGenerateKey(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		res = str(random.randrange(1, 9))
		for n in range(6):
			res += str(random.randrange(0, 9))
		self.key.SetValue(res)
		self.key.SetFocus()

	def onGetIP(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.getIP.Enable(False)
		t = threading.Thread(target=self.doPortcheck, args=[int(self.port.GetValue())])
		t.daemon = True
		t.start()

	def doPortcheck(self, port: int) -> None:
		tempServer = server.LocalRelayServer(port=port, password=None)
		try:
			req = request.urlopen("https://portcheck.nvdaremote.com/port/%s" % port)
			data = req.read()
			result = json.loads(data)
			wx.CallAfter(self.onGetIPSucceeded, result)
		except Exception as e:
			wx.CallAfter(self.onGetIPFail, e)
			raise
		finally:
			tempServer.close()
			wx.CallAfter(self.getIP.Enable, True)

	def onGetIPSucceeded(self, data: PortCheckResponse) -> None:
		ip = data["host"]
		port = data["port"]
		isOpen = data["open"]

		if isOpen:
			# Translators: Message shown when successfully getting external IP and the specified port is open
			successMsg = _("Successfully retrieved IP address. Port {port} is open.")
			# Translators: Title of success dialog
			successTitle = _("Success")
			wx.MessageBox(
				message=successMsg.format(port=port),
				caption=successTitle,
				style=wx.OK,
			)
		else:
			# Translators: Message shown when IP was retrieved but the specified port is not forwarded
			# {port} will be replaced with the actual port number
			warningMsg = _("Retrieved external IP, but port {port} is most likely not currently forwarded.")
			# Translators: Title of warning dialog
			warningTitle = _("Warning")
			wx.MessageBox(
				message=warningMsg.format(port=port),
				caption=warningTitle,
				style=wx.ICON_WARNING | wx.OK,
			)

		self.externalIP.SetValue(ip)
		self.externalIP.SelectAll()
		self.externalIP.SetFocus()

	def onGetIPFail(self, exc: Exception) -> None:
		# Translators: Error message when unable to get IP address from portcheck server
		errorMsg = _("Unable to contact portcheck server, please manually retrieve your IP address")
		# Translators: Title of error dialog
		errorTitle = _("Error")
		wx.MessageBox(
			message=errorMsg,
			caption=errorTitle,
			style=wx.ICON_ERROR | wx.OK,
		)


class DirectConnectDialog(wx.Dialog):
	_selectedPanel: ClientPanel | ServerPanel

	def __init__(self, parent: wx.Window, id: int, title: str, hostnames: Optional[List[str]] = None):
		super().__init__(parent, id, title=title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizerHelper = BoxSizerHelper(self, wx.VERTICAL)
		self._connectionModeControl = contentsSizerHelper.addLabeledControl(
			"&Mode",
			wx.Choice,
			choices=("Allow this computer to be controlled", "Control another computer"),
		)
		self._clientOrServerControl = contentsSizerHelper.addLabeledControl(
			_("&Server:"),
			wx.Choice,
			choices=(
				# Translators: A choice to connect to another machine.
				"Remote control server",
				# Translators: A choice to allow another machine to connect to this machine.
				"Host control server",
			),
		)
		self._clientOrServerControl.Bind(wx.EVT_CHOICE, self._onClientOrServer)
		simpleBook = self._simpleBook = wx.Simplebook(self)
		self._clientPanel = ClientPanel(simpleBook)
		if hostnames:
			self._clientPanel.host.AppendItems(hostnames)
			self._clientPanel.host.SetSelection(0)
		self._serverPanel = ServerPanel(simpleBook)
		simpleBook.AddPage(self._clientPanel, "Client")
		simpleBook.AddPage(self._serverPanel, "Server")
		self._clientOrServerControl.SetSelection(0)
		self._selectedPanel = self._clientPanel
		contentsSizerHelper.addItem(simpleBook)
		contentsSizerHelper.addDialogDismissButtons(wx.OK | wx.CANCEL, True)
		self.Bind(wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
		mainSizer.Add(contentsSizerHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.SetSizer(mainSizer)
		self.Fit()
		self.CenterOnScreen()

	def _onClientOrServer(self, evt: wx.CommandEvent) -> None:
		selectedIndex = self._clientOrServerControl.GetSelection()
		self._simpleBook.ChangeSelection(selectedIndex)
		# Hack: setting or changing the selection of a wx.SimpleBookseems to cause focus to jump to the first focusable control in the newly selected page, so force focus back to the control that caused the change.
		self._clientOrServerControl.SetFocus()
		self._selectedPanel = self._simpleBook.GetPage(selectedIndex)
		gui.messageBox("Changed")
		evt.Skip()

	def _onOk(self, evt: wx.CommandEvent) -> None:
		# gui.messageBox(f"{self.panel} is {self.clientPanel} = {self.panel is self.serverPanel}")
		message: str | None = None
		focusTarget: wx.Window | None = None
		if self._selectedPanel is self._clientPanel and (
			not self._selectedPanel.host.GetValue() or not self._selectedPanel.key.GetValue()
		):
			# Translators: A message box displayed when the host or key field is empty and the user tries to connect.
			message = _("Both host and key must be set.")
			focusTarget = self._selectedPanel.host
		elif self._selectedPanel is self._serverPanel and (
			not self._selectedPanel.port.GetValue() or not self._selectedPanel.key.GetValue()
		):
			# Translators: A message box displayed when the port or key field is empty and the user tries to connect.
			message = _("Both port and key must be set.")
			focusTarget = self._selectedPanel.port
		if message is not None:
			gui.messageBox(
				message,
				# Translators: Title of a dialog
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)
			if focusTarget is not None:
				focusTarget.SetFocus()
		else:
			evt.Skip()

	def _getKey(self) -> str:
		return self._selectedPanel.key.GetValue()

	def getConnectionInfo(self) -> ConnectionInfo:
		mode: ConnectionMode = (
			ConnectionMode.LEADER
			if self._connectionModeControl.GetSelection() == 0
			else ConnectionMode.FOLLOWER
		)
		serverAddr: str
		port: int
		insecure: bool
		if self._selectedPanel is self._clientPanel:
			serverAddr, port = protocol.addressToHostPort(self._selectedPanel.host.GetValue())
			insecure = False
		elif self._selectedPanel is self._serverPanel:
			serverAddr = "127.0.0.1"
			port = int(self._selectedPanel.port.GetValue())
			insecure = True
		return ConnectionInfo(
			hostname=serverAddr,
			mode=mode,
			key=self._getKey(),
			port=port,
			insecure=insecure,
		)


class CertificateUnauthorizedDialog(wx.MessageDialog):
	def __init__(self, parent: Optional[wx.Window], fingerprint: Optional[str] = None):
		# Translators: A title bar of a window presented when an attempt has been made to connect with a server with unauthorized certificate.
		title = _("NVDA Remote Connection Security Warning")
		message = _(
			# Translators: {fingerprint} is a SHA256 fingerprint of the server certificate.
			"The certificate of this server could not be verified. Using the wrong fingerprint may allow a third party to access the remote session..\n"
			"\n"
			"Before continuing, please make sure that the following server certificate fingerprint is correct.\n"
			"Server SHA256 fingerprint: {fingerprint}\n"
			"\n"
			"Continue connecting anyway?",
		).format(fingerprint=fingerprint)
		super().__init__(
			parent,
			caption=title,
			message=message,
			style=wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT | wx.CENTRE,
		)
		self.SetYesNoLabels(
			# Translators: A button to connect and remember the server with unauthorized certificate.
			_("Connect and do not ask again for this server"),
			# Translators: A button to connect and ask again for the server with unauthorized certificate.
			_("Connect"),
		)
