# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import functools
from typing import (
	Dict,
	List,
)

import wx
import wx.lib.newevent

from gui import (
	guiHelper,
	nvdaControls,
)
from gui.dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from logHandler import log

from ..viewModels.addonList import (
	AddonListVM,
	AddonListItemVM,
	AddonActionVM,
)


class AddonVirtualList(
		nvdaControls.AutoWidthColumnListCtrl,
		DpiScalingHelperMixinWithoutInit,
):

	def __init__(self, parent, addonsListVM: AddonListVM, actionVMList: List[AddonActionVM]):
		super().__init__(
			parent,
			style=(
				wx.LC_REPORT  # Single or multicolumn report view, with optional header.
				| wx.LC_VIRTUAL  # The application provides items text on demand. May only be used with LC_REPORT.
				| wx.LC_SINGLE_SEL  # Single selection (default is multiple).
				| wx.LC_HRULES  # Draws light horizontal rules between rows in report mode.
				| wx.LC_VRULES  # Draws light vertical rules between columns in report mode.
			),
			autoSizeColumn=1,
		)

		self.SetMinSize(self.scaleSize((500, 500)))

		# Translators: The name of the column that contains names of addons. In the add-on store dialog.
		self.InsertColumn(0, pgettext("addonStore", "Name"))
		# Translators: The name of the column that contains the addons version string. In the add-on store dialog.
		self.InsertColumn(1, pgettext("addonStore", "Version"))
		# Translators: The name of the column that contains the channel of the addon (e.g stable, beta, dev).
		self.InsertColumn(2, pgettext("addonStore", "Channel"))
		# Translators: The name of the column that contains the addons publisher. In the add-on store dialog.
		self.InsertColumn(3, pgettext("addonStore", "Publisher"))
		self.InsertColumn(
			4,
			# Translators: The name of the column that contains the status of the addon (E.G. available, downloading
			# installing). In the add-on store dialog.
			pgettext("addonStore", "Status"),
			# Enough space for the longer contents, eg: "Installed, restart required"
			width=self.scaleSize(150)
		)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

		self._addonsListVM = addonsListVM
		self._actionVMList = actionVMList
		self._contextMenu = wx.Menu()
		self._actionMenuItemMap: Dict[AddonActionVM, wx.MenuItem] = {}
		self.Bind(event=wx.EVT_CONTEXT_MENU, handler=self._popupContextMenu)
		for action in self._actionVMList:
			menuItem: wx.MenuItem = self._contextMenu.Append(id=-1, item=action.displayName)
			self._actionMenuItemMap[action] = menuItem
			action.updated.register(self._updateContextMenuItem)
			self.Bind(
				event=wx.EVT_MENU,
				handler=functools.partial(self._menuItemClicked, actionVM=action),
				source=menuItem,
			)
			self._updateContextMenuItem(action)

		self.SetItemCount(addonsListVM.getCount())
		selIndex = self._addonsListVM.getSelectedIndex()
		if selIndex is not None:
			self.Select(selIndex)
			self.Focus(selIndex)
		self._addonsListVM.itemUpdated.register(self._itemDataUpdated)
		self._addonsListVM.updated.register(self._doRefresh)

	def _popupContextMenu(self, evt: wx.ContextMenuEvent):
		position = evt.GetPosition()
		firstSelectedIndex: int = self.GetFirstSelected()
		if firstSelectedIndex == -1:
			# context menu only valid on an item.
			return
		if position == wx.DefaultPosition:
			# keyboard triggered context menu (due to "applications" key)
			# don't have position set. It must be fetched from the selected item.
			itemRect: wx.Rect = self.GetItemRect(firstSelectedIndex)
			position: wx.Position = itemRect.GetBottomLeft()
			self.PopupMenu(self._contextMenu, position)
		else:
			# Mouse (right click) triggered context menu.
			# In this case the menu is positioned better with GetPopupMenuSelectionFromUser.
			self.GetPopupMenuSelectionFromUser(self._contextMenu)

	def _menuItemClicked(self, evt: wx.CommandEvent, actionVM: AddonActionVM):
		selectedAddon: AddonListItemVM = self._addonsListVM.getSelection()
		log.debug(f"evt {evt}, actionVM: {actionVM}, selectedAddon: {selectedAddon}")
		actionVM.actionHandler(selectedAddon)

	def _itemDataUpdated(self, index: int):
		log.debug(f"index: {index}")
		self.RefreshItem(index)

	def OnItemSelected(self, evt: wx.ListEvent):
		newIndex = evt.GetIndex()
		log.debug(f"item selected: {newIndex}")
		self._addonsListVM.setSelection(index=newIndex)

	def _updateContextMenuItem(self, addonActionVM: AddonActionVM):
		menuItem = self._actionMenuItemMap[addonActionVM]
		menuItem.Enable(enable=addonActionVM.isValid)

	def OnItemActivated(self, evt: wx.ListEvent):
		activatedIndex = evt.GetIndex()
		log.debug(f"item activated: {activatedIndex}")

	def OnItemDeselected(self, evt: wx.ListEvent):
		log.debug(f"item deselected")
		self._addonsListVM.setSelection(None)

	def OnGetItemText(self, itemIndex: int, colIndex: int) -> str:
		dataItem = self._addonsListVM.getAddonAttrText(
			itemIndex,
			AddonListVM.presentedAttributes[colIndex]
		)
		if dataItem is None:
			# Failed to get dataItem, index may have been lost in refresh.
			return ''
		return str(dataItem)

	def OnColClick(self, evt: wx.ListEvent):
		colIndex = evt.GetColumn()
		log.debug(f"col clicked: {colIndex}")
		self._addonsListVM.setSortField(AddonListVM.presentedAttributes[colIndex])

	def _doRefresh(self):
		with guiHelper.autoThaw(self):
			newCount = self._addonsListVM.getCount()
			self.SetItemCount(newCount)
			self._refreshSelection()

	def _refreshSelection(self):
		selected = self.GetFirstSelected()
		newSelectedIndex = self._addonsListVM.getSelectedIndex()
		log.debug(f"_refreshSelection {newSelectedIndex}")
		if newSelectedIndex is not None:
			self.Select(newSelectedIndex)
			self.Focus(newSelectedIndex)
			# wx.ListCtrl doesn't send a selection event if the index hasn't changed,
			# however, the item at that index may have changed as a result of filtering.
			# To ensure parent dialogs are notified, explicitly send an event.
			if selected == newSelectedIndex:
				evt = wx.ListEvent(wx.wxEVT_LIST_ITEM_SELECTED, self.GetId())
				evt.SetIndex(newSelectedIndex)
				evt.SetClientObject(self._addonsListVM.getSelection())
				self.GetEventHandler().ProcessEvent(evt)
		elif newSelectedIndex is None:
			# wx.ListCtrl doesn't send a deselection event when the list is emptied.
			# To ensure parent dialogs are notified, explicitly send an event.
			self.Select(selected, on=0)
			evt = wx.ListEvent(wx.wxEVT_LIST_ITEM_DESELECTED, self.GetId())
			evt.SetIndex(-1)
			evt.SetClientObject(None)
			self.GetEventHandler().ProcessEvent(evt)
