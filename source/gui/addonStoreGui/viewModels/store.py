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
from typing import (
	Set,
	List,
	Optional,
	Tuple,
)
import threading

import addonHandler
from addonStore.dataManager import addonDataManager
from addonStore.install import installAddon
from addonStore.models.addon import (
	AddonStoreModel,
	_createAddonGUICollection,
)
from addonStore.models.channel import (
	Channel,
	_channelFilters,
)
from addonStore.models.status import (
	getStatus,
	_statusFilters,
	_StatusFilterKey,
	AvailableAddonStatus,
)
import config
import core
import extensionPoints
from gui.message import DisplayableError
from logHandler import log

from ..controls.messageDialogs import (
	_shouldProceedToRemoveAddonDialog,
	_shouldProceedWhenAddonTooOldDialog,
	_shouldProceedWhenInstalledAddonVersionUnknown,
)

from .addonList import (
	AddonActionVM,
	AddonDetailsVM,
	AddonListItemVM,
	AddonListVM,
)


class AddonStoreVM:
	def __init__(self):
		self._availableAddons = _createAddonGUICollection()
		self._installedAddons = _createAddonGUICollection()
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
		self._filteredChannels: Set[Channel] = next(iter(_channelFilters.values()))
		"""
		Filters the add-on list view model by add-on channel.
		Add-ons with a channel in _filteredChannels should be displayed in the list.
		Uses first filter in _channelFilters as default.
		"""

		self._downloader = addonDataManager.getFileDownloader()
		self._pendingInstalls: List[Tuple[AddonListItemVM, PathLike]] = []

		self.listVM: AddonListVM = AddonListVM(
			addons=self._createListItemVMs()
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
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "&Install"),
				actionHandler=self.getAddon,
				validCheck=lambda aVM: aVM.status == AvailableAddonStatus.AVAILABLE,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "&Install (override incompatibility)"),
				actionHandler=self.installOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: (
					aVM.status == AvailableAddonStatus.INCOMPATIBLE
					and aVM.model.canOverrideCompatibility
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "&Update"),
				actionHandler=self.getAddon,
				validCheck=lambda aVM: aVM.status == AvailableAddonStatus.UPDATE,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "Re&place"),
				actionHandler=self.replaceAddon,
				validCheck=lambda aVM: aVM.status == AvailableAddonStatus.REPLACE_SIDE_LOAD,
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "&Disable"),
				actionHandler=self.disableAddon,
				validCheck=lambda aVM: aVM.status not in (
					AvailableAddonStatus.DISABLED,
					AvailableAddonStatus.PENDING_DISABLE,
					AvailableAddonStatus.AVAILABLE,
					AvailableAddonStatus.INCOMPATIBLE,
					AvailableAddonStatus.INCOMPATIBLE_DISABLED,
					AvailableAddonStatus.DOWNLOAD_FAILED,
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "&Enable"),
				actionHandler=self.enableAddon,
				validCheck=lambda aVM: (
					aVM.status == AvailableAddonStatus.DISABLED
					or aVM.status == AvailableAddonStatus.PENDING_DISABLE
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "&Enable (override incompatibility)"),
				actionHandler=self.enableOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: (
					aVM.status == AvailableAddonStatus.INCOMPATIBLE_DISABLED
					and aVM.model.canOverrideCompatibility
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that removes the selected addon
				displayName=pgettext("addonStore", "&Remove"),
				actionHandler=self.removeAddon,
				validCheck=lambda aVM: aVM.status not in (
					AvailableAddonStatus.AVAILABLE,
					AvailableAddonStatus.INCOMPATIBLE,
					AvailableAddonStatus.PENDING_REMOVE,
					AvailableAddonStatus.DOWNLOAD_FAILED,
				),
				listItemVM=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for a button that installs the selected addon
				displayName=pgettext("addonStore", "Add-on &help"),
				actionHandler=self.helpAddon,
				validCheck=lambda aVM: aVM.status not in (
					AvailableAddonStatus.AVAILABLE,
					AvailableAddonStatus.INCOMPATIBLE,
					AvailableAddonStatus.DOWNLOAD_FAILED,
				),
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

	def installOverrideIncompatibilityForAddon(self, listItemVM: AddonListItemVM) -> None:
		from gui import mainFrame
		if _shouldProceedWhenAddonTooOldDialog(mainFrame, listItemVM.model):
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
			return
		listItemVM.status = getStatus(listItemVM.model)
		self.refresh()

	def enableOverrideIncompatibilityForAddon(self, listItemVM: AddonListItemVM) -> None:
		from ... import mainFrame
		if _shouldProceedWhenAddonTooOldDialog(mainFrame, listItemVM.model):
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
		self._pendingInstalls.append((listItemVM, fileDownloaded))

	def installPending(self):
		if not core.isMainThread():
			# Add-ons can have "installTasks", which often call the GUI assuming they are on the main thread.
			log.error("installation must happen on main thread.")
		for listItemVM, fileDownloaded in self._pendingInstalls:
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
		log.debug(f"{listItemVM.Id} status: {listItemVM.status}")

	def refresh(self):
		threading.Thread(target=self._getAddonsInBG, name="getAddonData").start()

	def _getAddonsInBG(self):
		log.debug("getting addons in the background")
		assert addonDataManager
		self._installedAddons = addonDataManager._installedAddonsCache.installedAddonGUICollection
		availableAddons = addonDataManager.getLatestCompatibleAddons(self.onDisplayableError)
		if bool(config.conf["addonStore"]["incompatibleAddons"]):
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
		log.debug("completed refresh")

	def cancelDownloads(self):
		for a in self._downloader.progress.keys():
			self.listVM._addons[a.listItemVMId].status = AvailableAddonStatus.AVAILABLE
		self._downloader.cancelAll()

	def _createListItemVMs(self) -> List[AddonListItemVM]:
		if self._filteredStatusKey in {
			_StatusFilterKey.AVAILABLE,
			_StatusFilterKey.UPDATE,
		}:
			addons = self._availableAddons
		elif self._filteredStatusKey in {
			_StatusFilterKey.INSTALLED,
			_StatusFilterKey.DISABLED,
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
			and model.channel in self._filteredChannels
			# Legacy add-ons contain invalid metadata
			# and should not be accessible through the add-on store.
			and not model.legacy
		]
