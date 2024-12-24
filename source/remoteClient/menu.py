from typing import TYPE_CHECKING

import wx

if TYPE_CHECKING:
	from .client import RemoteClient

import gui

from .connection_info import ConnectionMode


class RemoteMenu(wx.Menu):
	"""Menu for the NVDA Remote addon that appears in the NVDA Tools menu"""

	connectItem: wx.MenuItem
	disconnectItem: wx.MenuItem
	muteItem: wx.MenuItem
	pushClipboardItem: wx.MenuItem
	copyLinkItem: wx.MenuItem
	sendCtrlAltDelItem: wx.MenuItem
	remoteItem: wx.MenuItem

	def __init__(self, client: "RemoteClient") -> None:
		super().__init__()
		self.client = client
		toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.connectItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Item in NVDA Remote submenu to connect to a remote computer.
			_("Connect..."),
			# Translators: Tooltip for the Connect menu item in the NVDA Remote submenu.
			_("Remotely connect to another computer running NVDA Remote Access"),
		)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.client.doConnect,
			self.connectItem,
		)
		# Translators: Item in NVDA Remote submenu to disconnect from a remote computer.
		self.disconnectItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NVDA Remote submenu to disconnect from another computer running NVDA Remote Access.
			_("Disconnect"),
			# Translators: Tooltip for the Disconnect menu item in the NVDA Remote submenu.
			_("Disconnect from another computer running NVDA Remote Access"),
		)
		self.disconnectItem.Enable(False)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU,
			self.onDisconnectItem,
			self.disconnectItem,
		)
		self.muteItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NvDA Remote submenu to mute speech and sounds from the remote computer.
			_("Mute remote"),
			# Translators: Tooltip for the Mute Remote menu item in the NVDA Remote submenu.
			_("Mute speech and sounds from the remote computer"),
			kind=wx.ITEM_CHECK,
		)
		self.muteItem.Enable(False)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMuteItem, self.muteItem)
		self.pushClipboardItem: wx.MenuItem = self.Append(
			wx.ID_ANY,
			# Translators: Menu item in NVDA Remote submenu to push clipboard content to the remote computer.
			_("&Push clipboard"),
			# Translators: Tooltip for the Push Clipboard menu item in the NVDA Remote submenu.
			_("Push the clipboard to the other machine"),
		)
		self.pushClipboardItem.Enable(False)
		gui.mainFrame.sysTrayIcon.Bind(
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
		gui.mainFrame.sysTrayIcon.Bind(
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
		gui.mainFrame.sysTrayIcon.Bind(
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
		self.Remove(self.connectItem.Id)
		self.connectItem.Destroy()
		self.connectItem = None
		self.Remove(self.disconnectItem.Id)
		self.disconnectItem.Destroy()
		self.disconnectItem = None
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
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		tools_menu.Remove(self.remoteItem.Id)
		self.remoteItem.Destroy()
		self.remoteItem = None
		try:
			self.Destroy()
		except (RuntimeError, AttributeError):
			pass

	def onDisconnectItem(self, evt: wx.CommandEvent) -> None:
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
		self.connectItem.Enable(not connected)
		self.disconnectItem.Enable(connected)
		self.muteItem.Enable(connected)
		if not connected:
			self.muteItem.Check(False)
		self.pushClipboardItem.Enable(connected)
		self.copyLinkItem.Enable(connected)
		self.sendCtrlAltDelItem.Enable(connected)

	def handleConnecting(self, mode: ConnectionMode) -> None:
		self.disconnectItem.Enable(True)
		self.connectItem.Enable(False)
