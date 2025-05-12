# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import json
import random
import threading
from typing import TypedDict
from urllib import request

import gui
import wx
from wx.lib.expando import ExpandoTextCtrl
from gui.contextHelp import ContextHelpMixin
from logHandler import log
from gui.guiHelper import alwaysCallAfter, BoxSizerHelper
from gui import guiHelper
from gui.nvdaControls import SelectOnFocusSpinCtrl
from config.configFlags import RemoteConnectionMode, RemoteServerType

from . import configuration, serializer, server, protocol, transport
from .connectionInfo import ConnectionInfo, ConnectionMode
from .protocol import SERVER_PORT, RemoteMessageType


class ClientPanel(ContextHelpMixin, wx.Panel):
	helpId = "RemoteAccessConnectExisting"
	host: wx.ComboBox
	key: wx.TextCtrl
	_generateKeyButton: wx.Button
	_keyConnector: "transport.RelayTransport | None"
	_keyGenerationProgressDialog: gui.IndeterminateProgressDialog | None = None

	def __init__(self, parent: wx.Window | None = None, id: int = wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = BoxSizerHelper(self, sizer=sizer)
		self.host = sizerHelper.addLabeledControl(
			# Translators: The label of an edit field in connect dialog to enter name or address of the remote computer.
			_("&Host:"),
			wx.ComboBox,
		)
		self.key = sizerHelper.addLabeledControl(
			# Translators: Label of the edit field to enter key (password) to secure the Remote Access connection.
			_("&Key:"),
			wx.TextCtrl,
		)
		# Translators: The button used to generate a random key/password.
		self._generateKeyButton = wx.Button(parent=self, label=_("&Generate Key"))
		self._generateKeyButton.Bind(wx.EVT_BUTTON, self._onGenerateKey)
		keyControlsSizerHelper = BoxSizerHelper(self, sizer=self.key.GetContainingSizer())
		keyControlsSizerHelper.addItem(self._generateKeyButton)
		self.SetSizerAndFit(sizer)

	def _onGenerateKey(self, evt: wx.CommandEvent) -> None:
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
			self._generateKeyCommand()

	def _generateKeyCommand(self, insecure: bool = False) -> None:
		self._keyGenerationProgressDialog = gui.IndeterminateProgressDialog(
			self,
			# Translators: Title of a dialog shown to users when asking a Remote Access server to generate a key
			pgettext("remote", "Generating key"),
			# Translators: Message on a dialog shown to users when asking a Remote Access server to generate a key
			pgettext("remote", "Generating key..."),
		)
		address = protocol.addressToHostPort(self.host.GetValue())
		self._keyConnector = transport.RelayTransport(
			address=address,
			serializer=serializer.JSONSerializer(),
			insecure=insecure,
		)
		self._keyConnector.registerInbound(RemoteMessageType.GENERATE_KEY, self._handleKeyGenerated)
		self._keyConnector.transportCertificateAuthenticationFailed.register(self._handleCertificateFailed)
		self._keyConnector.transportConnectionFailed.register(self._handleConnectionFailed)
		t = threading.Thread(target=self._keyConnector.run)
		t.start()

	@alwaysCallAfter
	def _handleKeyGenerated(self, key: str | None = None) -> None:
		self.key.SetValue(key)
		self._keyConnector.close()
		self._keyConnector = None

		# Because we don't know when the containing dialog will next be focusable,
		# and a window must be focusable in order for calling `SetFocus` to work,
		# we need to focus the "Key" field when the containing dialog is next active,
		# as this will happen when it is next focusable.
		def setFocusOnNextActivate(evt: wx.ActivateEvent):
			evt.Skip()
			# Only move focus when this window next becomes the foreground window.
			if evt.Active:
				self.key.SetFocus()
				self.GetTopLevelParent().Unbind(wx.EVT_ACTIVATE, handler=setFocusOnNextActivate)

		self.GetTopLevelParent().Bind(wx.EVT_ACTIVATE, setFocusOnNextActivate)
		self._keyGenerationProgressDialog.done()
		self._keyGenerationProgressDialog = None

	@alwaysCallAfter
	def _handleConnectionFailed(self) -> None:
		self._keyGenerationProgressDialog.done()
		self._keyGenerationProgressDialog = None
		gui.messageBox(
			pgettext(
				"remote",
				# Translators: Message shown to users when requesting that a Remote Access server generate a key fails.
				# {host} will be replaced with the address of the Remote Access server.
				"Unable to connect to {host}. Check that you have internet access, and that there are no mistakes in the host field.",
			).format(host=self.host.GetValue()),
			# Translators: Title of a dialog.
			pgettext("remote", "Host connection failed"),
			wx.OK | wx.ICON_ERROR,
		)

	@alwaysCallAfter
	def _handleCertificateFailed(self) -> None:
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
		self._keyGenerationProgressDialog.Done()
		self._keyGenerationProgressDialog = None
		try:
			certHash = self._keyConnector.lastFailFingerprint

			wnd = CertificateUnauthorizedDialog(None, fingerprint=certHash)
			a = wnd.ShowModal()
			if a == wx.ID_YES:
				config = configuration.getRemoteConfig()
				config["trustedCertificates"][self.host.GetValue()] = certHash
			if a != wx.ID_YES and a != wx.ID_NO:
				return
		except Exception:
			log.exception("Error handling certificate failure")
			return
		finally:
			self._keyConnector.close()
			self._keyConnector = None
		self._generateKeyCommand(True)


class PortCheckResponse(TypedDict):
	host: str
	port: int
	open: bool


class ServerPanel(ContextHelpMixin, wx.Panel):
	helpId = "RemoteAccessConnectLocal"
	_getIPButton: wx.Button
	_externalIPControl: wx.TextCtrl
	port: wx.TextCtrl
	key: wx.TextCtrl
	_generateKeyButton: wx.Button
	_progressDialog: gui.IndeterminateProgressDialog | None = None

	def __init__(self, parent: wx.Window | None = None, id: int = wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = BoxSizerHelper(self, sizer=sizer)
		self._externalIPControl = sizerHelper.addLabeledControl(
			# Translators: Label of the field displaying the external IP address if using direct (client to server) connection.
			_("&External IP:"),
			ExpandoTextCtrl,
			style=wx.TE_READONLY,
		)
		# Translators: Used in server mode to obtain the external IP address for the server (controlled computer) for direct connection.
		self._getIPButton = wx.Button(parent=self, label=_("Get External &IP"))
		self._getIPButton.Bind(wx.EVT_BUTTON, self.onGetIP)
		externalIPControlsSizerHelper = BoxSizerHelper(
			self,
			sizer=self._externalIPControl.GetContainingSizer(),
		)
		externalIPControlsSizerHelper.addItem(self._getIPButton)

		# Translators: The label of an edit field in connect dialog to enter the port the server will listen on.
		self.port = sizerHelper.addLabeledControl(
			_("&Port:"),
			SelectOnFocusSpinCtrl,
			min=1,
			max=65535,
			initial=SERVER_PORT,
		)
		# Translators: Label of the edit field to enter key (password) to secure the Remote Access connection.
		self.key = sizerHelper.addLabeledControl(pgettext("remote", "&Key"), wx.TextCtrl)
		# Translators: The button used to generate a random key/password.
		self._generateKeyButton = wx.Button(parent=self, label=_("&Generate Key"))
		self._generateKeyButton.Bind(wx.EVT_BUTTON, self.onGenerateKey)
		keyControlsSizerHelper = BoxSizerHelper(self, sizer=self.key.GetContainingSizer())
		keyControlsSizerHelper.addItem(self._generateKeyButton)
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
		self._progressDialog = gui.IndeterminateProgressDialog(
			self,
			# Translators: Title of a dialog shown to users while attempting to detect their external IP address
			pgettext("remote", "Getting external IP"),
			# Translators: Message on a dialog shown to users while attempting to detect their external IP address
			pgettext("remote", "Getting external IP..."),
		)
		t = threading.Thread(target=self.doPortcheck, args=[int(self.port.GetValue())])
		t.daemon = True
		t.start()

	def doPortcheck(self, port: int) -> None:
		tempServer = server.LocalRelayServer(port=port, password=None)
		try:
			req = request.urlopen("https://portcheck.nvdaremote.com/port/%s" % port)
			data = req.read()
			result = json.loads(data)

			# Because we don't know when the containing dialog will next be focusable,
			# and a window must be focusable in order for calling `SetFocus` to work,
			# we need to focus the "Key" field when the containing dialog is next active,
			# as this will happen when it is next focusable.
			def setFocusOnNextActivate(evt: wx.ActivateEvent):
				evt.Skip()
				# Only move focus when this window next becomes the foreground window.
				if evt.Active:
					self._externalIPControl.SetFocus()
					self.GetTopLevelParent().Unbind(wx.EVT_ACTIVATE, handler=setFocusOnNextActivate)

			self.GetTopLevelParent().Bind(wx.EVT_ACTIVATE, setFocusOnNextActivate)
			wx.CallAfter(self.onGetIPSucceeded, result)
		except Exception as e:
			wx.CallAfter(self.onGetIPFail, e)
			raise
		finally:
			tempServer.close()
			wx.CallAfter(self._progressDialog.done)

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

		self._externalIPControl.SetValue(ip)
		self._externalIPControl.SelectAll()
		self._externalIPControl.SetFocus()

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


class DirectConnectDialog(ContextHelpMixin, wx.Dialog):
	helpId = "RemoteAccessConnect"
	_selectedPanel: ClientPanel | ServerPanel

	def __init__(self, parent: wx.Window, id: int, title: str, hostnames: list[str] | None = None):
		super().__init__(parent, id, title=title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizerHelper = BoxSizerHelper(self, wx.VERTICAL)
		self._connectionModeControl = contentsSizerHelper.addLabeledControl(
			# Translators: Label of the control allowing users to set whether they are the controlling or controlled computer in the Remote Access connection dialog.
			pgettext("remote", "&Mode:"),
			wx.Choice,
			choices=tuple(mode.displayString for mode in RemoteConnectionMode),
		)
		self._connectionModeControl.SetSelection(0)
		self._clientOrServerControl = contentsSizerHelper.addLabeledControl(
			# Translators: Label of the control allowing users to select whether to use a pre-existing Remote Access server, or to run their own.
			pgettext("remote", "&Server:"),
			wx.Choice,
			choices=tuple(serverType.displayString for serverType in RemoteServerType.__members__.values()),
		)
		self._clientOrServerControl.Bind(wx.EVT_CHOICE, self._onClientOrServer)
		simpleBook = self._simpleBook = wx.Simplebook(self)
		self._clientPanel = ClientPanel(simpleBook)
		if hostnames:
			self._clientPanel.host.AppendItems(hostnames)
			self._clientPanel.host.SetSelection(0)
		self._serverPanel = ServerPanel(simpleBook)
		# Since wx.SimpleBook doesn't create a page switcher for us, the following page labels are not used in the GUI.
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
		self._connectionModeControl.SetFocus()
		self.Bind(wx.EVT_SHOW, self._onShow)

	def _onClientOrServer(self, evt: wx.CommandEvent) -> None:
		"""Respond to changing between using a control server or hosting it locally"""
		selectedIndex = self._clientOrServerControl.GetSelection()
		self._simpleBook.ChangeSelection(selectedIndex)
		# Hack: setting or changing the selection of a wx.SimpleBook seems to cause focus to jump to the first focusable control in the newly selected page, so force focus back to the control that caused the change.
		self._clientOrServerControl.SetFocus()
		self._selectedPanel = self._simpleBook.GetPage(selectedIndex)
		evt.Skip()

	def _onOk(self, evt: wx.CommandEvent) -> None:
		"""Respond to the OK button being pressed."""
		message: str | None = None
		focusTarget: wx.Window | None = None
		if self._selectedPanel is self._clientPanel and (
			not self._selectedPanel.host.GetValue() or not self._selectedPanel.key.GetValue()
		):
			# Translators: Message displayed when the host or key field is empty and the user tries to connect.
			message = _("Both host and key must be set.")
			focusTarget = (
				self._selectedPanel.host if not self._selectedPanel.host.Value else self._selectedPanel.key
			)
		elif self._selectedPanel is self._serverPanel and (
			not self._selectedPanel.port.GetValue() or not self._selectedPanel.key.GetValue()
		):
			# Translators: Message displayed when the port or key field is empty and the user tries to connect.
			message = _("Both port and key must be set.")
			focusTarget = (
				self._selectedPanel.port if not self._selectedPanel.port.Value else self._selectedPanel.key
			)
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
		"""Get the connection key."""
		return self._selectedPanel.key.GetValue()

	def getConnectionInfo(self) -> ConnectionInfo:
		"""Get a :class:`ConnectionInfo` object based on the responses to the dialog."""
		mode: ConnectionMode = RemoteConnectionMode(
			self._connectionModeControl.GetSelection(),
		).toConnectionMode()
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

	def _onShow(self, evt: wx.ShowEvent):
		"""Make sure this dialog is focused when opened."""
		self.Raise()
		self.SetFocus()
		evt.Skip()


class CertificateUnauthorizedDialog(wx.MessageDialog):
	def __init__(self, parent: wx.Window | None, fingerprint: str | None = None):
		# Translators: Title of the dialog presented when attempting to connect to a server with an untrusted certificate.
		title = pgettext("remote", "Security Warning")
		message = pgettext(
			"remote",
			# Translators: Message presented when attempting to connect to a server with an untrusted certificate.
			# {fingerprint} will be replaced with the SHA256 fingerprint of the server certificate.
			"The certificate of this server could not be verified. Using the wrong fingerprint may allow a third party to access the Remote Access session.\n"
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
