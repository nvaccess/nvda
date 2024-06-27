# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from abc import ABC, abstractmethod
import functools
from typing import (
	Dict,
	Generic,
	Iterable,
	List,
	TypeVar,
)

import wx

from addonStore.models.status import _StatusFilterKey
from logHandler import log
import ui

from ..viewModels.action import AddonActionVM, BatchAddonActionVM
from ..viewModels.addonList import AddonListItemVM
from ..viewModels.store import AddonStoreVM


AddonActionT = TypeVar("AddonActionT", AddonActionVM, BatchAddonActionVM)


class _ActionsContextMenuP(Generic[AddonActionT], ABC):
	_actions: List[AddonActionT]
	_actionMenuItemMap: Dict[AddonActionT, wx.MenuItem]
	_contextMenu: wx.Menu

	@abstractmethod
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
				self._contextMenu.Remove(menuItem)
				del self._actionMenuItemMap[action]

		menuItems: List[wx.MenuItem] = list(self._contextMenu.GetMenuItems())
		for menuItem in menuItems:
			if menuItem not in self._actionMenuItemMap.values():
				# The menu item is not in the action menu item map.
				# It should be removed from the context menu.
				self._contextMenu.Remove(menuItem)


class _MonoActionsContextMenu(_ActionsContextMenuP[AddonActionVM]):
	"""Context menu for actions for a single add-on"""
	def __init__(self, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._actionMenuItemMap = {}
		self._contextMenu = wx.Menu()

	def _menuItemClicked(self, evt: wx.ContextMenuEvent, actionVM: AddonActionVM):
		selectedAddon = actionVM.actionTarget
		log.debug(f"action selected: actionVM: {actionVM.displayName}, selectedAddon: {selectedAddon}")
		actionVM.actionHandler(selectedAddon)

	@property
	def _actions(self) -> List[AddonActionVM]:
		return self._storeVM.actionVMList


class _BatchActionsContextMenu(_ActionsContextMenuP[BatchAddonActionVM]):
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

	def popupContextMenuFromPosition(
			self,
			targetWindow: wx.Window,
			position: wx.Position = wx.DefaultPosition
	):
		super().popupContextMenuFromPosition(targetWindow, position)
		if self._contextMenu.GetMenuItemCount() == 0:
			# Translators: a message displayed when activating the context menu on multiple selected add-ons,
			# but no actions are available for the add-ons.
			ui.message(pgettext("addonStore", "No actions available for the selected add-ons"))

	def _menuItemClicked(self, evt: wx.ContextMenuEvent, actionVM: BatchAddonActionVM):
		log.debug(f"Performing batch action for actionVM: {actionVM.displayName}")
		actionVM.actionHandler(self._selectedAddons)

	@property
	def _actions(self) -> List[BatchAddonActionVM]:
		return [
			BatchAddonActionVM(
				# Translators: Label for an action that installs the selected add-ons
				displayName=pgettext("addonStore", "&Install selected add-ons"),
				actionHandler=self._storeVM.getAddons,
				validCheck=lambda aVMs: (
					self._storeVM._filteredStatusKey == _StatusFilterKey.AVAILABLE
					and AddonListValidator(aVMs).canUseInstallAction()
				),
				actionTarget=self._selectedAddons
			),
			BatchAddonActionVM(
				# Translators: Label for an action that updates the selected add-ons
				displayName=pgettext("addonStore", "&Update selected add-ons"),
				actionHandler=self._storeVM.getAddons,
				validCheck=lambda aVMs: AddonListValidator(aVMs).canUseUpdateAction(),
				actionTarget=self._selectedAddons
			),
			BatchAddonActionVM(
				# Translators: Label for an action that removes the selected add-ons
				displayName=pgettext("addonStore", "&Remove selected add-ons"),
				actionHandler=self._storeVM.removeAddons,
				validCheck=lambda aVMs: (
					self._storeVM._filteredStatusKey in [
						# Removing add-ons in the updatable view fails,
						# as the updated version cannot be removed.
						_StatusFilterKey.INSTALLED,
						_StatusFilterKey.INCOMPATIBLE,
					]
					and AddonListValidator(aVMs).canUseRemoveAction()
				),
				actionTarget=self._selectedAddons
			),
			BatchAddonActionVM(
				# Translators: Label for an action that enables the selected add-ons
				displayName=pgettext("addonStore", "&Enable selected add-ons"),
				actionHandler=self._storeVM.enableAddons,
				validCheck=lambda aVMs: AddonListValidator(aVMs).canUseEnableAction(),
				actionTarget=self._selectedAddons
			),
			BatchAddonActionVM(
				# Translators: Label for an action that disables the selected add-ons
				displayName=pgettext("addonStore", "&Disable selected add-ons"),
				actionHandler=self._storeVM.disableAddons,
				validCheck=lambda aVMs: AddonListValidator(aVMs).canUseDisableAction(),
				actionTarget=self._selectedAddons
			),
		]


class AddonListValidator:
	def __init__(self, addonsList: List[AddonListItemVM]):
		self.addonsList = addonsList

	def canUseInstallAction(self) -> bool:
		for aVM in self.addonsList:
			if aVM.canUseInstallAction() or aVM.canUseInstallOverrideIncompatibilityAction():
				return True
		return False
	
	def canUseUpdateAction(self) -> bool:
		hasUpdatable = False
		hasInstallable = False
		for aVM in self.addonsList:
			if (
				aVM.canUseUpdateAction()
				or aVM.canUseReplaceAction()
				or aVM.canUseUpdateOverrideIncompatibilityAction()
			):
				hasUpdatable = True
			if aVM.canUseInstallAction() or aVM.canUseInstallOverrideIncompatibilityAction():
				hasInstallable = True
		return hasUpdatable and not hasInstallable

	def canUseRemoveAction(self) -> bool:
		for aVM in self.addonsList:
			if aVM.canUseRemoveAction():
				return True
		return False

	def canUseEnableAction(self) -> bool:
		for aVM in self.addonsList:
			if aVM.canUseEnableOverrideIncompatibilityAction() or aVM.canUseEnableAction():
				return True
		return False

	def canUseDisableAction(self) -> bool:
		for aVM in self.addonsList:
			if aVM.canUseDisableAction():
				return True
		return False
