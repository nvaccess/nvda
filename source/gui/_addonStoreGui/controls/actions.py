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

from logHandler import log

from ..viewModels.action import AddonActionVM
from ..viewModels.store import AddonStoreVM


class _ActionsContextMenu:
	def __init__(self, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._actionMenuItemMap: Dict[AddonActionVM, wx.MenuItem] = {}
		self._contextMenu = wx.Menu()

	def popupContextMenuFromPosition(
			self,
			targetWindow: wx.Window,
			position: wx.Position = wx.DefaultPosition
	):
		self._populateContextMenu()
		targetWindow.PopupMenu(self._contextMenu, pos=position)

	def _menuItemClicked(self, evt: wx.ContextMenuEvent, actionVM: AddonActionVM):
		selectedAddon = actionVM.listItemVM
		log.debug(f"action selected: actionVM: {actionVM}, selectedAddon: {selectedAddon}")
		actionVM.actionHandler(selectedAddon)

	def _populateContextMenu(self):
		prevActionIndex = -1
		for action in self._storeVM.actionVMList:
			menuItem = self._actionMenuItemMap.get(action)
			menuItems: List[wx.MenuItem] = list(self._contextMenu.GetMenuItems())
			isMenuItemInContextMenu = menuItem is not None and menuItem in menuItems

			if isMenuItemInContextMenu:
				# Always unbind as we need to rebind menu items to the latest action VM
				self._contextMenu.Unbind(wx.EVT_MENU, source=menuItem)

			if action.isValid:
				if isMenuItemInContextMenu:
					prevActionIndex = menuItems.index(menuItem)
				else:
					# Insert menu item into context menu
					prevActionIndex += 1
					self._actionMenuItemMap[action] = self._contextMenu.Insert(
						prevActionIndex,
						id=-1,
						item=action.displayName
					)

				# Bind the menu item to the latest action VM
				self._contextMenu.Bind(
					event=wx.EVT_MENU,
					handler=functools.partial(self._menuItemClicked, actionVM=action),
					source=self._actionMenuItemMap[action],
				)

			elif isMenuItemInContextMenu:
				# The action is invalid but the menu item exists and is in the context menu.
				# Remove the menu item from the context menu.
				self._contextMenu.RemoveItem(menuItem)
				del self._actionMenuItemMap[action]
