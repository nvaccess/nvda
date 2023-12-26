# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from os import (
	PathLike,
	startfile,
)
import os
from typing import (
	Iterable,
	List,
	Optional,
	cast,
)
import threading

import addonHandler
from addonStore.dataManager import addonDataManager
from addonStore.install import installAddon
from addonStore.models.addon import (
	_createAddonGUICollection,
	_AddonGUIModel,
	_AddonManifestModel,
	_AddonStoreModel,
)
from addonStore.models.channel import (
	Channel,
	_channelFilters,
)
from addonStore.models.status import (
	EnabledStatus,
	getStatus,
	_statusFilters,
	_StatusFilterKey,
	AvailableAddonStatus,
)
from addonStore.network import AddonFileDownloader
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
		assert addonDataManager
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
			listVM=self.listVM
		)
		self.actionVMList = self._makeActionsList()
		self.listVM.selectionChanged.register(self._onSelectedItemChanged)

	def _onSelectedItemChanged(self):
		selectedVM = self.listVM.getSelection()
		log.debug(f"Setting selection: {selectedVM}")
		self.detailsVM.listItem = selectedVM
		for action in self.actionVMList:
			action.actionTarget = selectedVM

	def _makeActionsList(self):
		selectedListItem: Optional[AddonListItemVM] = self.listVM.getSelection()
		return [
			AddonActionVM(
				# Translators: Label for an action that installs the selected addon
				displayName=pgettext("addonStore", "&Install"),
				actionHandler=self.getAddon,
				validCheck=lambda aVM: aVM.canUseInstallAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that installs the selected addon
				displayName=pgettext("addonStore", "&Install (override incompatibility)"),
				actionHandler=self.installOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: aVM.canUseInstallOverrideIncompatibilityAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that updates the selected addon
				displayName=pgettext("addonStore", "&Update"),
				actionHandler=self.getAddon,
				validCheck=lambda aVM: aVM.canUseUpdateAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that installs the selected addon
				displayName=pgettext("addonStore", "&Update (override incompatibility)"),
				actionHandler=self.installOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: aVM.canUseUpdateOverrideIncompatibilityAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that replaces the selected addon with
				# an add-on store version.
				displayName=pgettext("addonStore", "Re&place"),
				actionHandler=self.replaceAddon,
				validCheck=lambda aVM: aVM.canUseReplaceAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that disables the selected addon
				displayName=pgettext("addonStore", "&Disable"),
				actionHandler=self.disableAddon,
				validCheck=lambda aVM: aVM.canUseDisableAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that enables the selected addon
				displayName=pgettext("addonStore", "&Enable"),
				actionHandler=self.enableAddon,
				validCheck=lambda aVM: aVM.canUseEnableAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that enables the selected addon
				displayName=pgettext("addonStore", "&Enable (override incompatibility)"),
				actionHandler=self.enableOverrideIncompatibilityForAddon,
				validCheck=lambda aVM: aVM.canUseEnableOverrideIncompatibilityAction(),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that removes the selected addon
				displayName=pgettext("addonStore", "&Remove"),
				actionHandler=self.removeAddon,
				validCheck=lambda aVM: (
					aVM.canUseRemoveAction()
					and self._filteredStatusKey in (
						# Removing add-ons in the updatable view fails,
						# as the updated version cannot be removed.
						_StatusFilterKey.INSTALLED,
						_StatusFilterKey.INCOMPATIBLE,
					)
				),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens help for the selected addon
				displayName=pgettext("addonStore", "&Help"),
				actionHandler=self.helpAddon,
				validCheck=lambda aVM: (
					aVM.model.isInstalled
					and self._filteredStatusKey in (
						# Showing help in the updatable add-ons view is misleading
						# as we can only fetch the add-on help from the installed version.
						_StatusFilterKey.INSTALLED,
						_StatusFilterKey.INCOMPATIBLE,
					)
					and aVM.model._addonHandlerModel is not None
					and aVM.model._addonHandlerModel.getDocFilePath() is not None
				),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the homepage for the selected addon
				displayName=pgettext("addonStore", "Ho&mepage"),
				actionHandler=lambda aVM: startfile(aVM.model.homepage),
				validCheck=lambda aVM: aVM.model.homepage is not None,
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the license for the selected addon
				displayName=pgettext("addonStore", "&License"),
				actionHandler=lambda aVM: startfile(
					cast(
						str,
						cast(_AddonStoreModel, aVM.model).licenseURL
					)
				),
				validCheck=lambda aVM: (
					isinstance(aVM.model, _AddonStoreModel)
					and aVM.model.licenseURL is not None
				),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the source code for the selected addon
				displayName=pgettext("addonStore", "Source &Code"),
				actionHandler=lambda aVM: startfile(cast(_AddonStoreModel, aVM.model).sourceURL),
				validCheck=lambda aVM: isinstance(aVM.model, _AddonStoreModel),
				actionTarget=selectedListItem
			),
			AddonActionVM(
				# Translators: Label for an action that opens the webpage to see and send feedback for the selected add-on
				displayName=pgettext("addonStore", "Community re&views"),
				actionHandler=lambda aVM: startfile(
					cast(
						str,
						cast(_AddonStoreModel, aVM.model).reviewURL
					)
				),
				validCheck=lambda aVM: (
					isinstance(aVM.model, _AddonStoreModel)
					and aVM.model.reviewURL is not None
				),
				actionTarget=selectedListItem
			),
		]

	def helpAddon(self, listItemVM: AddonListItemVM) -> None:
		assert listItemVM.model._addonHandlerModel is not None
		path = listItemVM.model._addonHandlerModel.getDocFilePath()
		assert path is not None
		startfile(path)

	def removeAddon(
			self,
			listItemVM: AddonListItemVM[_AddonGUIModel],
			askConfirmation: bool = True,
			useRememberChoiceCheckbox: bool = False,
	) -> tuple[bool, bool]:
		from gui import mainFrame
		assert addonDataManager
		assert listItemVM.model
		if askConfirmation:
			shouldRemove, shouldRememberChoice = _shouldProceedToRemoveAddonDialog(
				mainFrame,
				listItemVM.model,
				useRememberChoiceCheckbox=useRememberChoiceCheckbox,
			)
		else:
			shouldRemove = True
			shouldRememberChoice = True
		if shouldRemove:
			addonDataManager._deleteCacheInstalledAddon(listItemVM.model.name)
			assert listItemVM.model._addonHandlerModel is not None
			listItemVM.model._addonHandlerModel.requestRemove()
			self.refresh()
			listItemVM.status = getStatus(listItemVM.model, self._filteredStatusKey)
		return shouldRemove, shouldRememberChoice

	def removeAddons(self, listItemVMs: Iterable[AddonListItemVM[_AddonStoreModel]]) -> None:
		shouldRemove = True
		shouldRememberChoice = False
		for aVM in listItemVMs:
			if not aVM.canUseRemoveAction():
				log.debug(f"Skipping {aVM.Id} ({aVM.status}) as it is not relevant for remove action")
			else:
				if shouldRememberChoice:
					if shouldRemove:
						self.removeAddon(aVM, askConfirmation=False)
					else:
						log.debug(
							f"Skipping {aVM.Id} as removal has been previously declined for all remaining"
							" add-ons."
						)
				else:
					shouldRemove, shouldRememberChoice = self.removeAddon(
						aVM,
						askConfirmation=True,
						useRememberChoiceCheckbox=True,
					)

	def installOverrideIncompatibilityForAddon(
			self,
			listItemVM: AddonListItemVM,
			askConfirmation: bool = True,
			useRememberChoiceCheckbox: bool = False,
	) -> tuple[bool, bool]:
		from gui import mainFrame
		if askConfirmation:
			shouldInstall, shouldRememberChoice = _shouldInstallWhenAddonTooOldDialog(
				mainFrame,
				listItemVM.model,
				useRememberChoiceCheckbox=useRememberChoiceCheckbox,
			)
		else:
			shouldInstall = True
			shouldRememberChoice = True
		if shouldInstall:
			listItemVM.model.enableCompatibilityOverride()
			self.getAddon(listItemVM)
			self.refresh()
		return shouldInstall, shouldRememberChoice

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

	def _handleEnableDisable(self, listItemVM: AddonListItemVM[_AddonManifestModel], shouldEnable: bool) -> None:
		try:
			listItemVM.model._addonHandlerModel.enable(shouldEnable)
		except addonHandler.AddonError:
			if shouldEnable:
				errorMessage = self._enableErrorMessage
			else:
				errorMessage = self._disableErrorMessage
			log.debug(errorMessage, exc_info=True)
			displayableError = DisplayableError(
				displayMessage=errorMessage.format(addon=listItemVM.model.displayName)
			)
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.onDisplayableError.notify, displayableError=displayableError)

		listItemVM.status = getStatus(listItemVM.model, self._filteredStatusKey)
		self.refresh()

	def enableOverrideIncompatibilityForAddon(
			self,
			listItemVM: AddonListItemVM[_AddonManifestModel],
			askConfirmation: bool = True,
			useRememberChoiceCheckbox: bool = False,
	) -> tuple[bool, bool]:
		from ... import mainFrame
		if askConfirmation:
			shouldEnable, shouldRememberChoice = _shouldEnableWhenAddonTooOldDialog(
				mainFrame,
				listItemVM.model,
				
				useRememberChoiceCheckbox=useRememberChoiceCheckbox,
			)
		else:
			shouldEnable = True
			shouldRememberChoice = True
		if shouldEnable:
			listItemVM.model.enableCompatibilityOverride()
			self._handleEnableDisable(listItemVM, True)
		return shouldEnable, shouldRememberChoice

	def enableAddon(self, listItemVM: AddonListItemVM) -> None:
		self._handleEnableDisable(listItemVM, True)

	def enableAddons(self, listItemVMs: Iterable[AddonListItemVM[_AddonStoreModel]]) -> None:
		shouldEnableIncompatible = True
		shouldRememberChoice = False
		for aVM in listItemVMs:
			if aVM.canUseEnableOverrideIncompatibilityAction():
				if shouldRememberChoice:
					if shouldEnableIncompatible:
						self.enableOverrideIncompatibilityForAddon(aVM, askConfirmation=False)
					else:
						log.debug(
							f"Skipping {aVM.Id} as override incompatibility has been previously declined for all remaining"
							" add-ons."
						)
				else:
					shouldEnableIncompatible, shouldRememberChoice = self.enableOverrideIncompatibilityForAddon(
						aVM,
						askConfirmation=True,
						useRememberChoiceCheckbox=True,
					)
			elif aVM.canUseEnableAction():
				self.enableAddon(aVM)
			else:
				log.debug(f"Skipping {aVM.Id} ({aVM.status}) as it is not relevant for enable action")

	def disableAddon(self, listItemVM: AddonListItemVM) -> None:
		self._handleEnableDisable(listItemVM, False)

	def disableAddons(self, listItemVMs: Iterable[AddonListItemVM[_AddonStoreModel]]) -> None:
		for aVM in listItemVMs:
			if not aVM.canUseDisableAction():
				log.debug(f"Skipping {aVM.Id} ({aVM.status}) as it is not relevant for disable action")
			else:
				self.disableAddon(aVM)

	def replaceAddon(
			self,
			listItemVM: AddonListItemVM,
			askConfirmation: bool = True,
			useRememberChoiceCheckbox: bool = False,
	) -> tuple[bool, bool]:
		from ... import mainFrame
		assert listItemVM.model
		if askConfirmation:
			shouldReplace, shouldRememberChoice = _shouldProceedWhenInstalledAddonVersionUnknown(
				mainFrame,
				listItemVM.model,
				useRememberChoiceCheckbox=useRememberChoiceCheckbox,
			)
		else:
			shouldReplace = True
			shouldRememberChoice = True
		if shouldReplace:
			self.getAddon(listItemVM)
		return shouldReplace, shouldRememberChoice

	def replaceAddons(self, listItemVMs: Iterable[AddonListItemVM[_AddonStoreModel]]) -> None:
		shouldReplace = True
		shouldRememberChoice = False
		for aVM in listItemVMs:
			if not aVM.canUseReplaceAction():
				log.debug(f"Skipping {aVM.Id} ({aVM.status}) as it is not relevant for replace action")
			else:
				if shouldRememberChoice:
					if shouldReplace:
						self.replaceAddon(aVM, askConfirmation=False)
					else:
						log.debug(
							f"Skipping {aVM.Id} as replacement has been previously declined for all remaining add-ons."
						)
				else:
					shouldReplace, shouldRememberChoice = self.replaceAddon(
						aVM,
						askConfirmation=True,
						useRememberChoiceCheckbox=True,
					)

	def getAddon(self, listItemVM: AddonListItemVM[_AddonStoreModel]) -> None:
		assert addonDataManager
		addonDataManager._downloadsPendingCompletion.add(listItemVM)
		listItemVM.status = AvailableAddonStatus.DOWNLOADING
		log.debug(f"{listItemVM.Id} status: {listItemVM.status}")
		self._downloader.download(listItemVM, self._downloadComplete, self.onDisplayableError)

	def getAddons(self, listItemVMs: Iterable[AddonListItemVM[_AddonStoreModel]]) -> None:
		shouldReplace = True
		shouldInstallIncompatible = True
		shouldRememberReplaceChoice = False
		shouldRememberInstallChoice = False
		for aVM in listItemVMs:
			if aVM.canUseInstallAction() or aVM.canUseUpdateAction():
				self.getAddon(aVM)
			elif aVM.canUseReplaceAction():
				if shouldRememberReplaceChoice:
					if shouldReplace:
						self.replaceAddon(aVM, askConfirmation=False)
					else:
						log.debug(
							f"Skipping {aVM.Id} as replacement has been previously declined for all remaining add-ons."
						)
				else:
					shouldReplace, shouldRememberReplaceChoice = self.replaceAddon(
						aVM,
						askConfirmation=True,
						useRememberChoiceCheckbox=True,
					)
			elif not aVM.model.isCompatible and aVM.model.canOverrideCompatibility:
				if shouldRememberInstallChoice:
					if shouldInstallIncompatible:
						self.installOverrideIncompatibilityForAddon(aVM, askConfirmation=False)
					else:
						log.debug(
							f"Skipping {aVM.Id} as override incompatibility has been previously declined for all remaining"
							" add-ons."
						)
				else:
					shouldInstallIncompatible, shouldRememberInstallChoice = self.installOverrideIncompatibilityForAddon(
						aVM,
						askConfirmation=True,
						useRememberChoiceCheckbox=True
					)
			else:
				log.debug(f"Skipping {aVM.Id} ({aVM.status}) as it is not available or updatable")

	def _downloadComplete(
			self,
			listItemVM: AddonListItemVM[_AddonStoreModel],
			fileDownloaded: Optional[PathLike]
	):
		try:
			addonDataManager._downloadsPendingCompletion.remove(listItemVM)
		except KeyError:
			log.debug("Download already completed")

		if fileDownloaded is None:
			# Download may have been cancelled or otherwise failed
			listItemVM.status = AvailableAddonStatus.DOWNLOAD_FAILED
			log.debugWarning(f"Error during download of {listItemVM.Id}", exc_info=True)
			return

		listItemVM.status = AvailableAddonStatus.DOWNLOAD_SUCCESS
		log.debug(f"Queuing add-on for install on dialog exit: {listItemVM.Id}")
		# Add-ons can have "installTasks", which often call the GUI assuming they are on the main thread.
		assert addonDataManager
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
		try:
			os.remove(fileDownloaded)
		except FileNotFoundError:
			pass
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
		self.listVM._isLoading = True
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
						and incompatibleAddons[channel][addonId].canOverrideCompatibility
					):
						availableAddons[channel][addonId] = incompatibleAddons[channel][addonId]
		log.debug("completed getting addons in the background")
		self._availableAddons = availableAddons
		self.listVM.resetListItems(self._createListItemVMs())
		self.detailsVM.listItem = self.listVM.getSelection()
		self.listVM._isLoading = False
		# ensure calling on the main thread.
		core.callLater(delay=0, callable=self.detailsVM.updated.notify, addonDetailsVM=self.detailsVM)
		log.debug("completed refresh")

	def cancelDownloads(self):
		while addonDataManager._downloadsPendingCompletion:
			listItem = addonDataManager._downloadsPendingCompletion.pop()
			listItem.status = AvailableAddonStatus.AVAILABLE
		self._downloader.cancelAll()

	def _filterByEnabledKey(self, model: _AddonGUIModel) -> bool:
		if EnabledStatus.ALL == self._filterEnabledDisabled:
			return True

		elif EnabledStatus.ENABLED == self._filterEnabledDisabled:
			return model.isPendingEnable or (
				not model.isDisabled
				and not model.isPendingDisable
				and not model.isBlocked
			)

		elif EnabledStatus.DISABLED == self._filterEnabledDisabled:
			return (
				model.isDisabled
				or model.isPendingDisable
				or model.isBlocked
			)

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
			(model, getStatus(model, self._filteredStatusKey))
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
