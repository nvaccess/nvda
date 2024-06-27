# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	List,
	Optional,
)

import wx

from gui import (
	guiHelper,
	nvdaControls,
)
from gui.dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from logHandler import log

from .actions import (
	_ActionsContextMenuP,
	_BatchActionsContextMenu,
	_MonoActionsContextMenu,
)
from ..viewModels.addonList import AddonListItemVM, AddonListVM


class AddonVirtualList(
		nvdaControls.AutoWidthColumnListCtrl,
		DpiScalingHelperMixinWithoutInit,
):
	def __init__(
			self,
			parent: wx.Window,
			addonsListVM: AddonListVM,
			actionsContextMenu: _MonoActionsContextMenu,
	):
		super().__init__(
			parent,
			style=(
				wx.LC_REPORT  # Single or multicolumn report view, with optional header.
				| wx.LC_VIRTUAL  # The application provides items text on demand. May only be used with LC_REPORT.
				| wx.LC_HRULES  # Draws light horizontal rules between rows in report mode.
				| wx.LC_VRULES  # Draws light vertical rules between columns in report mode.
			),
			autoSizeColumn=1,
		)
		self._addonsListVM = addonsListVM
		self._actionsContextMenu = actionsContextMenu
		self._batchActionsContextMenu = _BatchActionsContextMenu(self._addonsListVM._storeVM)

		self.SetMinSize(self.scaleSize((500, 500)))

		self._refreshColumns()
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

		self.Bind(event=wx.EVT_CONTEXT_MENU, handler=self._popupContextMenuFromList)

		self.SetItemCount(addonsListVM.getCount())
		selIndex = self._addonsListVM.getSelectedIndex()
		if selIndex is not None:
			self.Select(selIndex)
			self.Focus(selIndex)
		self._addonsListVM.itemUpdated.register(self._itemDataUpdated)
		self._addonsListVM.updated.register(self._doRefresh)

	def _refreshColumns(self):
		self.ClearAll()
		for col in self._addonsListVM.presentedFields:
			self.AppendColumn(col.displayString, width=self.scaleSize(col.width))
		self.Layout()

	def _getListSelectionPosition(self) -> Optional[wx.Position]:
		firstSelectedIndex: int = self.GetFirstSelected()
		if firstSelectedIndex < 0:
			return None
		itemRect: wx.Rect = self.GetItemRect(firstSelectedIndex)
		return itemRect.GetBottomLeft()

	def _updateBatchContextMenuSelection(self):
		numSelected = self.GetSelectedItemCount()
		prevSelectedIndex = self.GetFirstSelected()
		selectedAddons: List[AddonListItemVM] = []
		for _ in range(numSelected):
			addon = self._addonsListVM.getAddonAtIndex(prevSelectedIndex)
			selectedAddons.append(addon)
			prevSelectedIndex = self.GetNextSelected(prevSelectedIndex)

		self._batchActionsContextMenu._updateSelectedAddons(selectedAddons)

	@property
	def _contextMenu(self) -> _ActionsContextMenuP:
		numSelected = self.GetSelectedItemCount()
		if numSelected > 1:
			self._updateBatchContextMenuSelection()
			return self._batchActionsContextMenu
		return self._actionsContextMenu

	def _popupContextMenuFromList(self, evt: wx.ContextMenuEvent):
		listSelectionPosition = self._getListSelectionPosition()
		if listSelectionPosition is None:
			return
		eventPosition: wx.Position = evt.GetPosition()
		if eventPosition == wx.DefaultPosition:
			# keyboard triggered context menu (due to "applications" key)
			# don't have position set. It must be fetched from the selected item.
			self._contextMenu.popupContextMenuFromPosition(self, listSelectionPosition)
		else:
			# Mouse (right click) triggered context menu.
			# In this case the menu is positioned better with GetPopupMenuSelectionFromUser.
			self._contextMenu.popupContextMenuFromPosition(self)

	def _itemDataUpdated(self, index: int):
		log.debug(f"index: {index}")
		self.RefreshItem(index)
		# Emit a namechange event for the list item in order for NVDA to report the updated state.
		wx.Accessible.NotifyEvent(wx.ACC_EVENT_OBJECT_NAMECHANGE, self, wx.OBJID_CLIENT, index + 1)

	def OnItemSelected(self, evt: wx.ListEvent):
		newIndex = evt.GetIndex()
		log.debug(f"item selected: {newIndex}")
		self._addonsListVM.setSelection(index=newIndex)

	def OnItemActivated(self, evt: wx.ListEvent):
		if evt.GetKeyCode() == wx.WXK_SPACE:
			# Space key is used to toggle add-on selection.
			# Don't trigger the context menu.
			return
		position = self._getListSelectionPosition()
		self._contextMenu.popupContextMenuFromPosition(self, position)
		log.debug(f"item activated: {evt.GetIndex()}")

	def OnItemDeselected(self, evt: wx.ListEvent):
		log.debug("item deselected")
		self._addonsListVM.setSelection(None)

	def OnGetItemText(self, itemIndex: int, colIndex: int) -> str:
		dataItem = self._addonsListVM.getAddonFieldText(
			itemIndex,
			self._addonsListVM.presentedFields[colIndex]
		)
		if dataItem is None:
			# Failed to get dataItem, index may have been lost in refresh.
			return ''
		return str(dataItem)

	def OnColClick(self, evt: wx.ListEvent):
		colIndex = evt.GetColumn()
		log.debug(f"col clicked: {colIndex}")
		self._addonsListVM.setSortField(self._addonsListVM.presentedFields[colIndex])

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
