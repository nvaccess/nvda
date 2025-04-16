# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import TYPE_CHECKING

import wx

if TYPE_CHECKING:
	from .client import RemoteClient

import globalVars
import gui

from .connectionInfo import ConnectionMode


class RemoteMenu(wx.Menu):
	"""Menu for the NVDA Remote functionality that appears in the NVDA Tools menu"""

	def __init__(self, client: "RemoteClient") -> None:
		super().__init__()
		self.client = client
		sysTrayIcon = gui.mainFrame.sysTrayIcon
		toolsMenu = sysTrayIcon.toolsMenu
		self.connectionItem: wx.MenuItem = self.Append(wx.ID_ANY, " ")
		self._switchToConnectItem()
		self.muteItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NvDA Remote submenu to mute speech and sounds from the remote computer.
			_("Mute remote"),
			# Translators: Tooltip for the Mute Remote menu item in the NVDA Remote submenu.
			_("Mute speech and sounds from the remote computer"),
			kind=wx.ITEM_CHECK,
		)
		self.muteItem.Enable(False)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onMuteItem, self.muteItem)
		self.pushClipboardItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NVDA Remote submenu to push clipboard content to the remote computer.
			_("&Push clipboard"),
			# Translators: Tooltip for the Push Clipboard menu item in the NVDA Remote submenu.
			_("Push the clipboard to the other machine"),
		)
		self.pushClipboardItem.Enable(False)
		sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onPushClipboardItem,
			self.pushClipboardItem,
		)
		self.copyLinkItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NVDA Remote submenu to copy a link to the current session.
			_("Copy &link"),
			# Translators: Tooltip for the Copy Link menu item in the NVDA Remote submenu.
			_("Copy a link to the remote session"),
		)
		self.copyLinkItem.Enable(False)
		sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onCopyLinkItem,
			self.copyLinkItem,
		)
		self.sendCtrlAltDelItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NVDA Remote submenu to send Control+Alt+Delete to the remote computer.
			_("Send Ctrl+Alt+Del"),
			# Translators: Tooltip for the Send Ctrl+Alt+Del menu item in the NVDA Remote submenu.
			_("Send Ctrl+Alt+Del"),
		)
		sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onSendCtrlAltDel,
			self.sendCtrlAltDelItem,
		)
		self.sendCtrlAltDelItem.Enable(False)
		self.remoteItem = toolsMenu.AppendSubMenu(
			self,
			# Translators: Label of menu in NVDA tools menu.
			_("R&emote"),
			# Translators: Tooltip for the Remote menu in the NVDA Tools menu.
			_("NVDA Remote Access"),
		)

	def terminate(self) -> None:
		self.Remove(self.connectionItem.Id)
		self.connectionItem.Destroy()
		self.connectionItem = None
		self.Remove(self.muteItem.Id)
		self.muteItem.Destroy()
		self.muteItem = None
		self.Remove(self.pushClipboardItem.Id)
		self.pushClipboardItem.Destroy()
		self.pushClipboardItem = None
		self.Remove(self.copyLinkItem.Id)
		self.copyLinkItem.Destroy()
		self.copyLinkItem = None
		self.Remove(self.sendCtrlAltDelItem.Id)
		self.sendCtrlAltDelItem.Destroy()
		self.sendCtrlAltDelItem = None
		toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		toolsMenu.Remove(self.remoteItem.Id)
		self.remoteItem.Destroy()
		self.remoteItem = None
		try:
			self.Destroy()
		except (RuntimeError, AttributeError):
			pass

	def doDisconnect(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.client.disconnect()

	def onMuteItem(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.client.toggleMute()

	def onPushClipboardItem(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.client.pushClipboard()

	def onCopyLinkItem(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.client.copyLink()

	def onSendCtrlAltDel(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.client.sendSAS()

	def handleConnected(self, mode: ConnectionMode, connected: bool) -> None:
		if connected:
			self._switchToDisconnectItem()
		else:
			self._switchToConnectItem()
		self.muteItem.Enable(connected)
		if not connected:
			self.muteItem.Check(False)
		self.pushClipboardItem.Enable(connected)
		self.copyLinkItem.Enable(connected)
		self.sendCtrlAltDelItem.Enable(connected)

	def handleConnecting(self, mode: ConnectionMode) -> None:
		self._switchToDisconnectItem()

	def _switchToConnectItem(self):
		"""Switch to showing the "Connect..." item in the menu.

		Sets the label, help text and event bindings of the connection item
		to those appropriate for creating a new Remote session.
		"""
		# Translators: Item in NVDA Remote submenu to connect to a remote computer.
		self.connectionItem.SetItemLabel(_("Connect..."))
		# Translators: Tooltip for the Connect menu item in the NVDA Remote submenu.
		self.connectionItem.SetHelp(_("Remotely connect to another computer running NVDA Remote Access"))
		gui.mainFrame.sysTrayIcon.Unbind(wx.EVT_MENU, self.connectionItem)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.client.doConnect,
			self.connectionItem,
		)
		# The option to start a new Remote Access session should be unavailable in secure mode.
		if globalVars.appArgs.secure:
			self.connectionItem.Enable(False)

	def _switchToDisconnectItem(self):
		"""Switch to showing the "Disconnect" item in the menu.

		Sets the label, help text and event bindings of the connection item
		to those appropriate for disconnecting an existing Remote session.
		"""
		# Translators: Menu item in NVDA Remote submenu to disconnect from another computer running NVDA Remote Access.
		self.connectionItem.SetItemLabel(_("Disconnect"))
		# Translators: Tooltip for the Disconnect menu item in the NVDA Remote submenu.
		self.connectionItem.SetHelp(_("Disconnect from another computer running NVDA Remote Access"))
		gui.mainFrame.sysTrayIcon.Unbind(wx.EVT_MENU, self.connectionItem)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.doDisconnect,
			self.connectionItem,
		)
		# The option to disconnect from a Remote Access session should always be available.
		self.connectionItem.Enable()
