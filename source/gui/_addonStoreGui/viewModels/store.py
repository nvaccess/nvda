# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Needed for type hinting CaseInsensitiveDict
# Can be removed in a future version of python (3.8+)
from __future__ import annotations

from os import (
	PathLike,
	startfile,
)
import os
from typing import (
	List,
	Optional,
	cast,
)
import threading

import addonHandler
from _addonStore.dataManager import addonDataManager
from _addonStore.install import installAddon
from _addonStore.models.addon import (
	AddonStoreModel,
	_createAddonGUICollection,
	_AddonGUIModel,
)
from _addonStore.models.channel import (
	Channel,
	_channelFilters,
)
from _addonStore.models.status import (
	EnabledStatus,
	getStatus,
	_statusFilters,
	_StatusFilterKey,
	AvailableAddonStatus,
)
from _addonStore.network import AddonFileDownloader
import core
import extensionPoints
from gui.message import DisplayableError
from logHandler import log

from ..controls.messageDialogs import (
	_shouldEnableWhenAddonTooOldDialog,
	_shouldProceedToRemoveAddonDialog,
	_shouldInstallWhenAddonTooOldDialog,
	_shouldProceedWhenInstalledAddonVersionUnknown,
)

from .action import AddonActionVM
from .addonList import (
	AddonDetailsVM,
	AddonListItemVM,
	AddonListVM,
)


class AddonStoreVM:
	def __init__(self):
		self._installedAddons = addonDataManager._installedAddonsCache.installedAddonGUICollection
		self._availableAddons = _createAddonGUICollection()
		self.hasError = extensionPoints.Action()
		self.onDisplayableError = DisplayableError.OnDisplayableErrorT()
		"""
		An extension point used to notify the add-on store VM when an error
		occurs that can be displayed to the user.

		This allows the add-on store GUI to handle displaying an error.

		@param displayableError: Error that can be displayed to the user.
		@type displayableError: gui.message.DisplayableError
		"""
		self._filteredStatusKey: _StatusFilterKey = _StatusFilterKey.INSTALLED
		"""
		Filters the add-on list view model by add-on status.
		Add-ons with a status in _statusFilters[self._filteredStatusKey] should be displayed in the list.
		"""
		self._filterChannelKey: Channel = Channel.ALL
		"""
		Filters the add-on list view model by add-on channel.
		Add-ons with a channel in _channelFilters[self._filterChannelKey] should be displayed in the list.
		"""
		self._filterEnabledDisabled: EnabledStatus = EnabledStatus.ALL
		"""
		Filters the add-on list view model by enabled or disabled.
		"""
		self._filterIncludeIncompatible: bool = False

		self._downloader = AddonFileDownloader()

		self.listVM: AddonListVM = AddonListVM(
			addons=self._createListItemVMs(),
			storeVM=self,
		)
		self.detailsVM: AddonDetailsVM = AddonDetailsVM(
			listItem=self.listVM.getSelection()
		)
		self.actionVMList = self._makeActionsList()
		self.listVM.selectionChanged.register(self._onSelectedItemChanged)

	def _onSelectedItemChanged(self):
		selectedVM = self.listVM.getSelection()
		log.debug(f"Setting selection: {selectedVM}")
		self.detailsVM.listItem = selectedVM
		for action in self.actionVMList:
			action.listItemVM = selectedVM

	def _makeActionsList(self):
		selectedListItem: Optional[AddonListItemVM] = self.listVM.getSelection()
		return [
			AddonActionVM(
				# Translators: Label for an action that installs the selected addon
				displayName=pgettext("addonStore", "&Install"),
				actionHandler=self.getAddon,
				validCheck=lambda aVM: aVM.status == AvailableAddonStatus.AVAILABLE,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that installs the selected addon
				displayName=pgettext("addonStore", "&Install (override incompatibility)"),
				actionHandler=self.installOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: (
					aVM.status == AvailableAddonStatus.INCOMPATIBLE
					and aVM.model.canOverrideCompatibility
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that updates the selected addon
				displayName=pgettext("addonStore", "&Update"),
				actionHandler=self.getAddon,
				validCheck=lambda aVM: aVM.status == AvailableAddonStatus.UPDATE,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that replaces the selected addon with
				# an add-on store version.
				displayName=pgettext("addonStore", "Re&place"),
				actionHandler=self.replaceAddon,
				validCheck=lambda aVM: aVM.status == AvailableAddonStatus.REPLACE_SIDE_LOAD,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that disables the selected addon
				displayName=pgettext("addonStore", "&Disable"),
				actionHandler=self.disableAddon,
				validCheck=lambda aVM: aVM.model.isInstalled and aVM.status not in (
					AvailableAddonStatus.DISABLED,
					AvailableAddonStatus.PENDING_DISABLE,
					AvailableAddonStatus.INCOMPATIBLE_DISABLED,
					AvailableAddonStatus.PENDING_INCOMPATIBLE_DISABLED,
					AvailableAddonStatus.PENDING_REMOVE,
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that enables the selected addon
				displayName=pgettext("addonStore", "&Enable"),
				actionHandler=self.enableAddon,
				validCheck=lambda aVM: (
					aVM.status == AvailableAddonStatus.DISABLED
					or aVM.status == AvailableAddonStatus.PENDING_DISABLE
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that enables the selected addon
				displayName=pgettext("addonStore", "&Enable (override incompatibility)"),
				actionHandler=self.enableOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: (
					aVM.status in (
						AvailableAddonStatus.INCOMPATIBLE_DISABLED,
						AvailableAddonStatus.PENDING_INCOMPATIBLE_DISABLED,
					)
					and aVM.model.canOverrideCompatibility
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that removes the selected addon
				displayName=pgettext("addonStore", "&Remove"),
				actionHandler=self.removeAddon,
				validCheck=lambda aVM: (
					aVM.model.isInstalled
					and aVM.status != AvailableAddonStatus.PENDING_REMOVE
					and self._filteredStatusKey in (
						# Removing add-ons in the updatable view fails,
						# as the updated version cannot be removed.
						_StatusFilterKey.INSTALLED,
						_StatusFilterKey.INCOMPATIBLE,
					)
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens help for the selected addon
				displayName=pgettext("addonStore", "&Help"),
				actionHandler=self.helpAddon,
				validCheck=lambda aVM: aVM.model.isInstalled and self._filteredStatusKey in (
					# Showing help in the updatable add-ons view is misleading
					# as we can only fetch the add-on help from the installed version.
					_StatusFilterKey.INSTALLED,
					_StatusFilterKey.INCOMPATIBLE,
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the homepage for the selected addon
				displayName=pgettext("addonStore", "Ho&mepage"),
				actionHandler=lambda aVM: startfile(aVM.model.homepage),
				validCheck=lambda aVM: aVM.model.homepage is not None,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the license for the selected addon
				displayName=pgettext("addonStore", "&License"),
				actionHandler=lambda aVM: startfile(cast(AddonStoreModel, aVM.model).licenseURL),
				validCheck=lambda aVM: (
					isinstance(aVM.model, AddonStoreModel)
					and aVM.model.licenseURL is not None
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the source code for the selected addon
				displayName=pgettext("addonStore", "Source &Code"),
				actionHandler=lambda aVM: startfile(cast(AddonStoreModel, aVM.model).sourceURL),
				validCheck=lambda aVM: isinstance(aVM.model, AddonStoreModel),
				listItemVM=selectedListItem
			),
		]

	def helpAddon(self, listItemVM: AddonListItemVM) -> None:
		path = listItemVM.model._addonHandlerModel.getDocFilePath()
		startfile(path)

	def removeAddon(self, listItemVM: AddonListItemVM) -> None:
		if _shouldProceedToRemoveAddonDialog(listItemVM.model):
			listItemVM.model._addonHandlerModel.requestRemove()
			self.refresh()
			listItemVM.status = getStatus(listItemVM.model)

	def installOverrideIncompatibilityForAddon(self, listItemVM: AddonListItemVM) -> None:
		from gui import mainFrame
		if _shouldInstallWhenAddonTooOldDialog(mainFrame, listItemVM.model):
			listItemVM.model.enableCompatibilityOverride()
			self.getAddon(listItemVM)
			self.refresh()

	_enableErrorMessage: str = pgettext(
		"addonStore",
		# Translators: The message displayed when the add-on cannot be enabled.
		# {addon} is replaced with the add-on name.
		"Could not enable the add-on: {addon}."
	)

	_disableErrorMessage: str = pgettext(
		"addonStore",
		# Translators: The message displayed when the add-on cannot be disabled.
		# {addon} is replaced with the add-on name.
		"Could not disable the add-on: {addon}."
	)

	def _handleEnableDisable(self, listItemVM: AddonListItemVM, shouldEnable: bool) -> None:
		try:
			listItemVM.model._addonHandlerModel.enable(shouldEnable)
		except addonHandler.AddonError:
			log.debug(exc_info=True)
			if shouldEnable:
				errorMessage = self._enableErrorMessage
			else:
				errorMessage = self._disableErrorMessage
			displayableError = DisplayableError(
				displayMessage=errorMessage.format(addon=listItemVM.model.displayName)
			)
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.onDisplayableError.notify, displayableError=displayableError)

		listItemVM.status = getStatus(listItemVM.model)
		self.refresh()

	def enableOverrideIncompatibilityForAddon(self, listItemVM: AddonListItemVM) -> None:
		from ... import mainFrame
		if _shouldEnableWhenAddonTooOldDialog(mainFrame, listItemVM.model):
			listItemVM.model.enableCompatibilityOverride()
			self._handleEnableDisable(listItemVM, True)

	def enableAddon(self, listItemVM: AddonListItemVM) -> None:
		self._handleEnableDisable(listItemVM, True)

	def disableAddon(self, listItemVM: AddonListItemVM) -> None:
		self._handleEnableDisable(listItemVM, False)

	def replaceAddon(self, listItemVM: AddonListItemVM) -> None:
		from ... import mainFrame
		if _shouldProceedWhenInstalledAddonVersionUnknown(mainFrame, listItemVM.model):
			self.getAddon(listItemVM)

	def getAddon(self, listItemVM: AddonListItemVM) -> None:
		listItemVM.status = AvailableAddonStatus.DOWNLOADING
		log.debug(f"{listItemVM.Id} status: {listItemVM.status}")
		self._downloader.download(listItemVM.model, self._downloadComplete, self.onDisplayableError)

	def _downloadComplete(self, addonDetails: AddonStoreModel, fileDownloaded: Optional[PathLike]):
		listItemVM: Optional[AddonListItemVM] = self.listVM._addons[addonDetails.listItemVMId]
		if listItemVM is None:
			log.error(f"No list item VM for addon with id: {addonDetails.addonId}")
			return

		if fileDownloaded is None:
			# Download may have been cancelled or otherwise failed
			listItemVM.status = AvailableAddonStatus.DOWNLOAD_FAILED
			log.debugWarning(f"Error during download of {listItemVM.Id}", exc_info=True)
			return

		listItemVM.status = AvailableAddonStatus.DOWNLOAD_SUCCESS
		log.debug(f"Queuing add-on for install on dialog exit: {listItemVM.Id}")
		# Add-ons can have "installTasks", which often call the GUI assuming they are on the main thread.
		addonDataManager._downloadsPendingInstall.add((listItemVM, fileDownloaded))

	def installPending(self):
		if not core.isMainThread():
			# Add-ons can have "installTasks", which often call the GUI assuming they are on the main thread.
			log.error("installation must happen on main thread.")
		while addonDataManager._downloadsPendingInstall:
			listItemVM, fileDownloaded = addonDataManager._downloadsPendingInstall.pop()
			self._doInstall(listItemVM, fileDownloaded)

	def _doInstall(self, listItemVM: AddonListItemVM, fileDownloaded: PathLike):
		if not core.isMainThread():
			# Add-ons can have "installTasks", which often call the GUI assuming they are on the main thread.
			log.error("installation must happen on main thread.")
			return
		listItemVM.status = AvailableAddonStatus.INSTALLING
		log.debug(f"{listItemVM.Id} status: {listItemVM.status}")
		try:
			installAddon(fileDownloaded)
		except DisplayableError as displayableError:
			listItemVM.status = AvailableAddonStatus.INSTALL_FAILED
			log.debug(f"{listItemVM.Id} status: {listItemVM.status}")
			core.callLater(delay=0, callable=self.onDisplayableError.notify, displayableError=displayableError)
			return
		listItemVM.status = AvailableAddonStatus.INSTALLED
		addonDataManager._cacheInstalledAddon(listItemVM.model)
		# Clean up download file
		os.remove(fileDownloaded)
		log.debug(f"{listItemVM.Id} status: {listItemVM.status}")

	def refresh(self):
		if self._filteredStatusKey in {
			_StatusFilterKey.AVAILABLE,
			_StatusFilterKey.UPDATE,
		}:
			threading.Thread(target=self._getAvailableAddonsInBG, name="getAddonData").start()

		elif self._filteredStatusKey in {
			_StatusFilterKey.INSTALLED,
			_StatusFilterKey.INCOMPATIBLE,
		}:
			self._installedAddons = addonDataManager._installedAddonsCache.installedAddonGUICollection
			self.listVM.resetListItems(self._createListItemVMs())
			self.detailsVM.listItem = self.listVM.getSelection()
		else:
			raise NotImplementedError(f"Unhandled status filter key {self._filteredStatusKey}")

	def _getAvailableAddonsInBG(self):
		self.detailsVM._isLoading = True
		self.listVM.resetListItems([])
		log.debug("getting available addons in the background")
		assert addonDataManager
		availableAddons = addonDataManager.getLatestCompatibleAddons(self.onDisplayableError)
		if self._filterIncludeIncompatible:
			incompatibleAddons = addonDataManager.getLatestAddons(self.onDisplayableError)
			for channel in incompatibleAddons:
				for addonId in incompatibleAddons[channel]:
					# only include incompatible add-ons if:
					# - no compatible or installed versions are available
					# - the user can override the compatibility of the add-on
					# (it's too old and not too new)
					if (
						addonId not in availableAddons[channel]
						and addonId not in self._installedAddons[channel]
						and incompatibleAddons[channel][addonId].canOverrideCompatibility
					):
						availableAddons[channel][addonId] = incompatibleAddons[channel][addonId]
		log.debug("completed getting addons in the background")
		self._availableAddons = availableAddons
		self.listVM.resetListItems(self._createListItemVMs())
		self.detailsVM.listItem = self.listVM.getSelection()
		self.detailsVM._isLoading = False
		log.debug("completed refresh")

	def cancelDownloads(self):
		for a in self._downloader.progress.keys():
			self.listVM._addons[a.listItemVMId].status = AvailableAddonStatus.AVAILABLE
		self._downloader.cancelAll()

	def _filterByEnabledKey(self, model: _AddonGUIModel) -> bool:
		if EnabledStatus.ALL == self._filterEnabledDisabled:
			return True

		elif EnabledStatus.ENABLED == self._filterEnabledDisabled:
			return model.isPendingEnable or (
				not model.isDisabled
				and not model.isPendingDisable
			)

		elif EnabledStatus.DISABLED == self._filterEnabledDisabled:
			return model.isDisabled or model.isPendingDisable

		raise NotImplementedError(f"Invalid EnabledStatus: {self._filterEnabledDisabled}")

	def _createListItemVMs(self) -> List[AddonListItemVM]:
		if self._filteredStatusKey in {
			_StatusFilterKey.AVAILABLE,
			_StatusFilterKey.UPDATE,
		}:
			addons = self._availableAddons

		elif self._filteredStatusKey in {
			_StatusFilterKey.INSTALLED,
			_StatusFilterKey.INCOMPATIBLE,
		}:
			addons = self._installedAddons
		else:
			raise NotImplementedError(f"Unhandled status filter key {self._filteredStatusKey}")

		addonsWithStatus = (
			(model, getStatus(model))
			for channel in addons
			for model in addons[channel].values()
		)

		return [
			AddonListItemVM(model=model, status=status)
			for model, status in addonsWithStatus
			if status in _statusFilters[self._filteredStatusKey]
			and model.channel in _channelFilters[self._filterChannelKey]
			# Legacy add-ons contain invalid metadata
			# and should not be accessible through the add-on store.
			and not model.legacy
			and self._filterByEnabledKey(model)
		]
