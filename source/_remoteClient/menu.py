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
			# Translators: Menu item in Remote Access submenu to mute speech and sounds from the remote computer.
			_("Mute remote"),
			# Translators: Tooltip for the Mute Remote menu item in the Remote Access submenu.
			pgettext("remote", "Mute speech and sounds from the remote computer."),
			kind=wx.ITEM_CHECK,
		)
		self.muteItem.Enable(False)
		sysTrayIcon.Bind(wx.EVT_MENU, self.onMuteItem, self.muteItem)
		self.pushClipboardItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in the Remote Access submenu to send the contents of the clipboard to the remote computer.
			pgettext("remote", "&Send clipboard"),
			# Translators: Tooltip for the Send clipboard menu item in the Remote Access submenu.
			pgettext("remote", "Send the clipboard text to the remote computer."),
		)
		self.pushClipboardItem.Enable(False)
		sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onPushClipboardItem,
			self.pushClipboardItem,
		)
		self.copyLinkItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in the Remote Access submenu to copy a link to the current session.
			_("Copy &link"),
			# Translators: Tooltip for the Copy Link menu item in the Remote Access submenu.
			pgettext("remote", "Copy a link to the current Remote Access session to the clipboard."),
		)
		self.copyLinkItem.Enable(False)
		sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onCopyLinkItem,
			self.copyLinkItem,
		)
		self.sendCtrlAltDelItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in the Remote Access submenu to send Control+Alt+Delete to the remote computer.
			pgettext("remote", "S&end control+alt+delete"),
			# Translators: Tooltip for the Send Control+Alt+Delete menu item in the Remote Access submenu.
			pgettext("remote", "Send control+alt+delete to the controlled computer."),
		)
		sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onSendCtrlAltDel,
			self.sendCtrlAltDelItem,
		)
		self.sendCtrlAltDelItem.Enable(False)
		self.remoteItem = toolsMenu.AppendSubMenu(
			self,
			# Translators: Label of the Remote Access submenu in the NVDA tools menu.
			pgettext("remote", "R&emote Access"),
			pgettext(
				"remote",
				# Translators: Tooltip for the Remote Access submenu in the NVDA Tools menu.
				"Allow someone to control this computer from elsewhere, or control another computer running NVDA with this one.",
			),
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
		self.client.doDisconnect()

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
		self.muteItem.Enable(connected and mode is ConnectionMode.LEADER)
		if not connected:
			self.muteItem.Check(False)
		self.pushClipboardItem.Enable(connected)
		self.copyLinkItem.Enable(connected)
		self.sendCtrlAltDelItem.Enable(connected and mode is ConnectionMode.LEADER)

	def handleConnecting(self, mode: ConnectionMode) -> None:
		self._switchToDisconnectItem()

	def _switchToConnectItem(self):
		"""Switch to showing the "Connect..." item in the menu.

		Sets the label, help text and event bindings of the connection item
		to those appropriate for creating a new Remote session.
		"""
		# Translators: Item in the Remote Access submenu to connect to another computer.
		self.connectionItem.SetItemLabel(_("Connect..."))
		# Translators: Tooltip for the Connect menu item in the Remote Access submenu.
		self.connectionItem.SetHelp(pgettext("remote", "Remotely connect to another computer running NVDA."))
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
		# Translators: Menu item in the Remote Access submenu to disconnect from another computer running NVDA.
		self.connectionItem.SetItemLabel(_("Disconnect"))
		# Translators: Tooltip for the Disconnect menu item in the Remote Access submenu.
		self.connectionItem.SetHelp(pgettext("remote", "Disconnect from the current Remote Access session."))
		gui.mainFrame.sysTrayIcon.Unbind(wx.EVT_MENU, self.connectionItem)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.doDisconnect,
			self.connectionItem,
		)
		# The option to disconnect from a Remote Access session should always be available.
		self.connectionItem.Enable()
