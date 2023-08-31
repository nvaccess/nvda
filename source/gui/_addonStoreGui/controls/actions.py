# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import functools
from typing import (
	Dict,
	Generic,
	Iterable,
	List,
	TypeVar,
)
from typing_extensions import Protocol

import wx

from _addonStore.models.status import _StatusFilterKey
from logHandler import log

from ..viewModels.action import AddonActionVM, BulkAddonActionVM
from ..viewModels.addonList import AddonListItemVM
from ..viewModels.store import AddonStoreVM


AddonActionT = TypeVar("AddonActionT", AddonActionVM, BulkAddonActionVM)


class _ActionsContextMenuP(Generic[AddonActionT], Protocol):
	_actions: List[AddonActionT]
	_actionMenuItemMap: Dict[AddonActionT, wx.MenuItem]
	_contextMenu: wx.Menu

	def _menuItemClicked(self, evt: wx.ContextMenuEvent, actionVM: AddonActionT):
		...

	def popupContextMenuFromPosition(
			self,
			targetWindow: wx.Window,
			position: wx.Position = wx.DefaultPosition
	):
		self._populateContextMenu()
		targetWindow.PopupMenu(self._contextMenu, pos=position)

	def _populateContextMenu(self):
		prevActionIndex = -1
		for action in self._actions:
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

		menuItems: List[wx.MenuItem] = list(self._contextMenu.GetMenuItems())
		for menuItem in menuItems:
			if menuItem not in self._actionMenuItemMap.values():
				# The menu item is not in the action menu item map.
				# It should be removed from the context menu.
				self._contextMenu.RemoveItem(menuItem)


class _MonoActionsContextMenu(_ActionsContextMenuP[AddonActionVM]):
	"""Context menu for actions for a single add-on"""
	def __init__(self, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._actionMenuItemMap = {}
		self._contextMenu = wx.Menu()

	def _menuItemClicked(self, evt: wx.ContextMenuEvent, actionVM: AddonActionVM):
		selectedAddon = actionVM.listItemVM
		log.debug(f"action selected: actionVM: {actionVM.displayName}, selectedAddon: {selectedAddon}")
		actionVM.actionHandler(selectedAddon)

	@property
	def _actions(self) -> List[AddonActionVM]:
		return self._storeVM.actionVMList


class _BulkActionsContextMenu(_ActionsContextMenuP[BulkAddonActionVM]):
	"""Context menu for actions for a group of add-ons"""
	def __init__(self, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._actionMenuItemMap = {}
		self._contextMenu = wx.Menu()
		self._selectedAddons: Iterable[AddonListItemVM] = tuple()

	def _updateSelectedAddons(self, selectedAddons: Iterable[AddonListItemVM]):
		# Reset the action menu as self._actions depends on the selected add-ons
		self._actionMenuItemMap = {}
		self._selectedAddons = selectedAddons

	def _menuItemClicked(self, evt: wx.ContextMenuEvent, actionVM: BulkAddonActionVM):
		log.debug(f"Performing bulk action for actionVM: {actionVM.displayName}")
		actionVM.actionHandler(self._selectedAddons)

	@property
	def _actions(self) -> List[BulkAddonActionVM]:
		return [
			BulkAddonActionVM(
				# Translators: Label for an action that installs the selected add-ons
				displayName=pgettext("addonStore", "&Install selected add-ons"),
				actionHandler=self._storeVM.getAddons,
				validCheck=lambda aVMs: self._storeVM._filteredStatusKey == _StatusFilterKey.AVAILABLE,
				listItemVMs=self._selectedAddons
			),
		]
