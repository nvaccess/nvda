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
	Callable,
	Set,
	cast,
	List,
	Optional,
	Dict,
	Tuple,
	TYPE_CHECKING,
)
import threading

from requests.structures import CaseInsensitiveDict

import addonHandler
from addonHandler import addonVersionCheck
from addonStore.dataManager import (
	addonDataManager,
)
from addonStore.models import (
	_channelFilters,
	AddonDetailsModel,
	AddonStoreModel,
	Channel,
	createAddonStoreCollection,
)
from addonStore.status import (
	_getStatus,
	_statusFilters,
	AvailableAddonStatus,
)
import config
import core
import extensionPoints
from gui.message import DisplayableError
from logHandler import log

from .dialogs import (
	_shouldProceedToRemoveAddonDialog,
	_shouldProceedWhenAddonTooOldDialog,
	_shouldProceedWhenInstalledAddonVersionUnknown,
)


if TYPE_CHECKING:
	# Remove when https://github.com/python/typing/issues/760 is resolved
	from _typeshed import SupportsLessThan
	from addonStore.models import AddonDetailsCollectionT


class AddonListItemVM:
	def __init__(
			self,
			model: AddonDetailsModel,
			status: AvailableAddonStatus = AvailableAddonStatus.AVAILABLE
	):
		self._model: AddonDetailsModel = model  # read-only
		self._status: AvailableAddonStatus = status  # modifications triggers L{updated.notify}
		self.updated = extensionPoints.Action()  # Notify of changes to VM, argument: addonListItemVM

	@property
	def model(self):
		return self._model

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, newStatus: AvailableAddonStatus):
		if newStatus != self.status:
			log.debug(f"addon status change: {self.Id}: status: {newStatus}")
			self._status = newStatus
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.updated.notify, addonListItemVM=self)

	@property
	def Id(self) -> str:
		return self._model.listItemVMId

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}: {self.Id}, {self.status}"


class AddonDetailsVM:
	def __init__(self, listItem: Optional[AddonListItemVM] = None):
		self._listItem: Optional[AddonListItemVM] = listItem
		self.updated = extensionPoints.Action()  # triggered by setting L{self._listItem}

	@property
	def listItem(self) -> Optional[AddonListItemVM]:
		return self._listItem

	@listItem.setter
	def listItem(self, newListItem: Optional[AddonListItemVM]):
		if (
			self._listItem == newListItem  # both may be same ref or None
			or (
				None not in (newListItem, self._listItem)
				and self._listItem.Id == newListItem.Id  # confirm with addonId
			)
		):
			# already set, exit early
			return
		self._listItem = newListItem
		# ensure calling on the main thread.
		core.callLater(delay=0, callable=self.updated.notify, addonDetailsVM=self)


if TYPE_CHECKING:
	AddonListItemVMCollectionT = Dict[Channel, CaseInsensitiveDict["AddonListItemVM"]]


def createAddonListItemVMCollection() -> "AddonListItemVMCollectionT":
	return {
		channel: CaseInsensitiveDict()
		for channel in Channel
		if channel != Channel.ALL
	}


class AddonListVM:
	presentedAttributes = (
		"displayName",
		"addonVersionName",
		"channel",
		"publisher",
		"status",  # NVDA state for this addon, see L{AvailableAddonStatus}
	)

	def __init__(
			self,
			addons: List[AddonListItemVM],
	):
		self._addons: CaseInsensitiveDict[AddonListItemVM] = CaseInsensitiveDict()
		self.itemUpdated = extensionPoints.Action()
		self.updated = extensionPoints.Action()
		self.selectionChanged = extensionPoints.Action()
		self.selectedAddonId: Optional[str] = None
		self.lastSelectedAddonId = self.selectedAddonId
		self._sortByModelFieldName: str = "displayName"
		self._filterString: Optional[str] = None

		self._setSelectionPending = False
		self._addonsFilteredOrdered: List[str] = self._getFilteredSortedIds()
		self._validate(
			sortField=self._sortByModelFieldName,
			selectionIndex=self.getSelectedIndex(),
			selectionId=self.selectedAddonId
		)
		self.selectedAddonId = self._tryPersistSelection(self._addonsFilteredOrdered)
		self.resetListItems(addons)

	def _itemDataUpdated(self, addonListItemVM: AddonListItemVM):
		addonId: str = addonListItemVM.Id
		log.debug(f"Item updated: {addonListItemVM!r}")
		assert addonListItemVM == self._addons[addonId], "Must be the same instance."
		if addonId in self._addonsFilteredOrdered:
			log.debug("Notifying of update")
			index = self._addonsFilteredOrdered.index(addonId)
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.itemUpdated.notify, index=index)

	def resetListItems(self, listVMs: List[AddonListItemVM]):
		log.debug("resetting list items")

		# Ensure that old listItemVMs can no longer notify of updates.
		for _addonListItemVM in self._addons.values():
			_addonListItemVM.updated.unregister(self._itemDataUpdated)

		# set new ID:listItemVM mapping.
		self._addons = CaseInsensitiveDict({
			vm.Id: vm
			for vm in listVMs
		})
		self._updateAddonListing()

		# allow new listItemVMs to notify of updates.
		for _addonListItemVM in listVMs:
			_addonListItemVM.updated.register(self._itemDataUpdated)

		# Notify observers of change in the list.
		# ensure calling on the main thread.
		core.callLater(delay=0, callable=self.updated.notify)

	def getAddonAttrText(self, index: int, attrName: str) -> Optional[str]:
		""" Get the text for an item's attribute.
		@param index: The index of the item in _addonsFilteredOrdered
		@param attrName: The exposed attribute for the addon. See L{AddonList.presentedAttributes}
		@return: The text for the addon attribute
		"""
		try:
			addonId = self._addonsFilteredOrdered[index]
		except IndexError:
			# Failed to get addonId, index may have been lost in refresh.
			return None
		try:
			listItemVM = self._addons[addonId]
		except KeyError:
			# Failed to get addon, may have been lost in refresh.
			return None
		return self._getAddonAttrText(listItemVM, attrName)

	def _getAddonAttrText(self, listItemVM: AddonListItemVM, attrName: str) -> str:
		assert attrName in AddonListVM.presentedAttributes
		if attrName == "status":  # special handling, not on the model.
			return listItemVM.status.displayString
		if attrName == "channel":
			return listItemVM.model.channel.displayString
		return getattr(listItemVM.model, attrName)

	def getCount(self) -> int:
		return len(self._addonsFilteredOrdered)

	def getSelectedIndex(self) -> Optional[int]:
		if self._addonsFilteredOrdered and self.selectedAddonId in self._addonsFilteredOrdered:
			return self._addonsFilteredOrdered.index(self.selectedAddonId)
		return None

	def setSelection(self, index: Optional[int]) -> Optional[AddonListItemVM]:
		self._validate(selectionIndex=index)
		self.selectedAddonId = None
		if index is not None:
			try:
				self.selectedAddonId = self._addonsFilteredOrdered[index]
			except IndexError:
				# Failed to get addonId, index may have been lost in refresh.
				pass
		selectedItemVM: Optional[AddonListItemVM] = self.getSelection()
		log.debug(f"selected Item: {selectedItemVM}")
		# ensure calling on the main thread.
		core.callLater(delay=0, callable=self.selectionChanged.notify)
		return selectedItemVM

	def getSelection(self) -> Optional[AddonListItemVM]:
		if self.selectedAddonId is None:
			return None
		return self._addons.get(self.selectedAddonId)

	def _validate(
			self,
			sortField: Optional[str] = None,
			selectionIndex: Optional[int] = None,
			selectionId: Optional[str] = None,
	):
		if sortField is not None:
			assert (sortField in AddonListVM.presentedAttributes)
		if selectionIndex is not None:
			assert (0 <= selectionIndex < len(self._addonsFilteredOrdered))
		if selectionId is not None:
			assert (selectionId in self._addons.keys())

	def setSortField(self, modelFieldName: str):
		oldOrder = self._addonsFilteredOrdered
		self._validate(sortField=modelFieldName)
		self._sortByModelFieldName = modelFieldName
		self._updateAddonListing()
		if oldOrder != self._addonsFilteredOrdered:
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.updated.notify)

	def _getFilteredSortedIds(self) -> List[str]:
		def _getSortFieldData(listItemVM: AddonListItemVM) -> "SupportsLessThan":
			return self._getAddonAttrText(listItemVM, self._sortByModelFieldName)

		def _containsTerm(detailsVM: AddonListItemVM, term: str) -> bool:
			term = term.casefold()
			model = detailsVM.model
			return (
				term in model.displayName.casefold()
				or term in model.description.casefold()
				or term in model.publisher.casefold()
			)

		filtered = (
			vm for vm in self._addons.values()
			if self._filterString is None or _containsTerm(vm, self._filterString)
		)
		filteredSorted = list([
			vm.Id for vm in sorted(filtered, key=_getSortFieldData)
		])
		return filteredSorted

	def _tryPersistSelection(
			self,
			newOrder: List[str],
	) -> Optional[str]:
		"""Get the ID of the selection in new order, _addonsFilteredOrdered should not have changed yet.
		"""
		selectedIndex = self.getSelectedIndex()
		selectedId = self.selectedAddonId
		if selectedId in newOrder:
			# nothing else to do, selection doesn't have to change.
			log.debug(f"Selected Id in new order {selectedId}")
			return selectedId
		elif not newOrder:
			log.debug(f"No entries in new order")
			# no entries after filter, select None
			return None
		elif selectedIndex is not None:
			# select the addon at the closest index
			oldMaxIndex: int = len(self._addonsFilteredOrdered) - 1
			oldIndexNorm: float = selectedIndex / max(oldMaxIndex, 1)  # min-max scaling / normalization
			newMaxIndex: int = len(newOrder) - 1
			approxNewIndex = int(oldIndexNorm * newMaxIndex)
			newSelectedIndex = max(0, min(approxNewIndex, newMaxIndex))
			log.debug(
				"Approximate from position "
				f"oldSelectedIndex: {selectedIndex}, "
				f"oldMaxIndex: {oldMaxIndex}, "
				f"newSelectedIndex: {newSelectedIndex}, "
				f"newMaxIndex: {newMaxIndex}"
			)
			return newOrder[newSelectedIndex]
		elif self.lastSelectedAddonId in newOrder:
			log.debug(f"lastSelected in new order: {self.lastSelectedAddonId}")
			return self.lastSelectedAddonId
		elif newOrder:
			# if there is any addon select it.
			return newOrder[0]
		else:
			log.debug(f"No selection")
			# no selection.
			return None

	def _updateAddonListing(self):
		newOrder = self._getFilteredSortedIds()
		self.selectedAddonId = self._tryPersistSelection(newOrder)
		if self.selectedAddonId:
			self.lastSelectedAddonId = self.selectedAddonId
		self._addonsFilteredOrdered = newOrder

	def applyFilter(self, filterText: str) -> None:
		oldOrder = self._addonsFilteredOrdered
		if not filterText:
			filterText = None
		self._filterString = filterText
		self._updateAddonListing()
		if oldOrder != self._addonsFilteredOrdered:
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.updated.notify)


class AddonActionVM:
	""" Actions/behaviour that can be embedded within other views/viewModels that can apply to a single
	L{AddonListItemVM}.
	Use the L{AddonActionVM.updated} extensionPoint.Action to be notified about changes.
	E.G.:
	- Updates within the AddonListItemVM (perhaps changing the action validity)
	- Entirely changing the AddonListItemVM action will be applied to, the validity can be checked for the new
	item.
	"""
	def __init__(
			self,
			displayName: str,
			actionHandler: Callable[[AddonListItemVM, ], None],
			validCheck: Callable[[AddonListItemVM, ], bool],
			listItemVM: Optional[AddonListItemVM],
	):
		"""
		@param displayName: Translated string, to be displayed to the user. Should describe the action / behaviour.
		@param actionHandler: Call when the action is triggered.
		@param validCheck: Is the action valid for the current listItemVM
		@param listItemVM: The listItemVM this action will be applied to. L{updated} notifies of modification.
		"""
		self.displayName: str = displayName
		self.actionHandler: Callable[[AddonListItemVM, ], None] = actionHandler
		self._validCheck: Callable[[AddonListItemVM, ], bool] = validCheck
		self._listItemVM: Optional[AddonListItemVM] = listItemVM
		if listItemVM:
			listItemVM.updated.register(self._listItemChanged)
		self.updated = extensionPoints.Action()
		"""Notify of changes to the action"""

	def _listItemChanged(self, addonListItemVM: AddonListItemVM):
		"""Something inside the AddonListItemVM has changed"""
		assert self._listItemVM == addonListItemVM
		self._notify()

	def _notify(self):
		# ensure calling on the main thread.
		core.callLater(delay=0, callable=self.updated.notify, addonActionVM=self)

	@property
	def isValid(self) -> bool:
		return (
			self._listItemVM is not None
			and self._validCheck(self._listItemVM)
		)

	@property
	def listItemVM(self) -> Optional[AddonListItemVM]:
		return self._listItemVM

	@listItemVM.setter
	def listItemVM(self, listItemVM: Optional[AddonListItemVM]):
		if self._listItemVM == listItemVM:
			return
		if self._listItemVM:
			self._listItemVM.updated.unregister(self._listItemChanged)
		if listItemVM:
			listItemVM.updated.register(self._listItemChanged)
		self._listItemVM = listItemVM
		self._notify()


class AddonStoreVM:
	def __init__(self):
		self._addons = createAddonStoreCollection()
		self.hasError = extensionPoints.Action()
		self.onDisplayableError = DisplayableError.OnDisplayableErrorT()
		"""
		An extension point used to notify the add-on store VM when an error
		occurs that can be displayed to the user.

		This allows the add-on store GUI to handle displaying an error.

		@param displayableError: Error that can be displayed to the user.
		@type displayableError: gui.message.DisplayableError
		"""
		self._filteredStatuses: Set[AvailableAddonStatus] = next(iter(_statusFilters.values()))
		"""
		Filters the add-on list view model by add-on status.
		Add-ons with a status in _filteredStatuses should be displayed in the list.
		Uses first filter in _statusFilters as default.
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
		from .. import mainFrame
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
		listItemVM.status = _getStatus(listItemVM.model)
		self.refresh()

	def enableOverrideIncompatibilityForAddon(self, listItemVM: AddonListItemVM) -> None:
		from .. import mainFrame
		if _shouldProceedWhenAddonTooOldDialog(mainFrame, listItemVM.model):
			listItemVM.model.enableCompatibilityOverride()
			self._handleEnableDisable(listItemVM, True)

	def enableAddon(self, listItemVM: AddonListItemVM) -> None:
		self._handleEnableDisable(listItemVM, True)

	def disableAddon(self, listItemVM: AddonListItemVM) -> None:
		self._handleEnableDisable(listItemVM, False)

	def replaceAddon(self, listItemVM: AddonListItemVM) -> None:
		from .. import mainFrame
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
			listItemVM.status = AvailableAddonStatus.DOWNLOAD_FAILED
			log.debugWarning(f"Error during download of {listItemVM.Id}", exc_info=True)
			displayableError = DisplayableError(
				# Translators: A message shown when downloading an add-on fails
				displayMessage=pgettext("addonStore", "Unable to download add-on.")
			)
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.onDisplayableError.notify, displayableError=displayableError)
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
			self.onDisplayableError.notify(displayableError=displayableError)
			return
		listItemVM.status = AvailableAddonStatus.INSTALLED
		addonDataManager._cacheInstalledAddon(listItemVM.model)
		log.debug(f"{listItemVM.Id} status: {listItemVM.status}")

	def refresh(self):
		threading.Thread(target=self._getAddonsInBG, name="getAddonData").start()

	def _getAddonsInBG(self):
		log.debug("getting addons in the background")
		assert addonDataManager
		assert addonHandler.state._addonHandlerCache
		addons: AddonDetailsCollectionT = addonDataManager.getLatestCompatibleAddons(self.onDisplayableError)
		addonHandlerAddons = addonHandler.state._addonHandlerCache.installedAddonsAsDetails
		for channel in addonHandlerAddons:
			for addonId in addonHandlerAddons[channel]:
				# only use installed add-on data if no add-on store details available
				if addonId not in addons[channel]:
					addons[channel][addonId] = addonHandlerAddons[channel][addonId]
		if bool(config.conf["addonStore"]["incompatibleAddons"]):
			incompatibleAddons = addonDataManager.getLatestAddons(self.onDisplayableError)
			for channel in incompatibleAddons:
				for addonId in incompatibleAddons[channel]:
					# only include incompatible add-ons if:
					# - no compatible or installed versions are available
					# - the user can override the compatibility of the add-on
					# (it's too old and not too new)
					if (
						addonId not in addons[channel]
						and incompatibleAddons[channel][addonId].canOverrideCompatibility
					):
						addons[channel][addonId] = incompatibleAddons[channel][addonId]
		log.debug("completed getting addons in the background")
		self._addons = addons
		self.listVM.resetListItems(self._createListItemVMs())
		self.detailsVM.listItem = self.listVM.getSelection()
		log.debug("completed refresh")

	def cancelDownloads(self):
		for a in self._downloader.progress.keys():
			self.listVM._addons[a.listItemVMId].status = AvailableAddonStatus.AVAILABLE
		self._downloader.cancelAll()

	def _createListItemVMs(self) -> List[AddonListItemVM]:
		addonsWithStatus = (
			(model, _getStatus(model))
			for channel in self._addons
			for model in self._addons[channel].values()
		)

		return [
			AddonListItemVM(model=model, status=status)
			for model, status in addonsWithStatus
			if status in self._filteredStatuses
			and model.channel in self._filteredChannels
		]


def getAddonBundleToInstallIfValid(addonPath: str) -> addonHandler.AddonBundle:
	"""
	@param addonPath: path to the 'nvda-addon' file.
	@return: the addonBundle, if valid
	@raise DisplayableError if the addon bundle is invalid / incompatible.
	"""
	try:
		bundle = addonHandler.AddonBundle(addonPath)
	except addonHandler.AddonError:
		log.error("Error opening addon bundle from %s" % addonPath, exc_info=True)
		raise DisplayableError(
			displayMessage=pgettext(
				"addonStore",
				# Translators: The message displayed when an error occurs when opening an add-on package for adding.
				# The %s will be replaced with the path to the add-on that could not be opened.
				"Failed to open add-on package file at %s - missing file or invalid file format"
			) % addonPath
		)

	if not (
		addonVersionCheck.isAddonCompatible(bundle)
		or bundle.overrideIncompatibility
	):
		# This should not happen, only compatible or overridable add-ons are
		# intended to be presented in the add-on store.
		raise DisplayableError(
			displayMessage=pgettext(
				"addonStore",
				# Translators: The message displayed when an add-on is not supported by this version of NVDA.
				# The %s will be replaced with the path to the add-on that is not supported.
				"Add-on not supported %s"
			) % addonPath
		)
	return bundle


def getPreviouslyInstalledAddonById(addon: addonHandler.AddonBundle) -> Optional[addonHandler.Addon]:
	assert addonHandler.state._addonHandlerCache
	installedAddon = addonHandler.state._addonHandlerCache.installedAddons.get(addon.name)
	if installedAddon is None or installedAddon.isPendingRemove:
		return None
	return installedAddon


def installAddon(addonPath: PathLike) -> None:
	""" Installs the addon at path.
	Any error messages / warnings are presented to the user via a GUI message box.
	If attempting to install an addon that is pending removal, it will no longer be pending removal.
	@note See also L{gui.addonGui.installAddon}
	@raise DisplayableError on failure
	"""
	addonPath = cast(str, addonPath)
	bundle = getAddonBundleToInstallIfValid(addonPath)
	prevAddon = getPreviouslyInstalledAddonById(bundle)

	try:
		if prevAddon:
			prevAddon.requestRemove()
		addonHandler.installAddonBundle(bundle)
	except addonHandler.AddonError:  # Handle other exceptions as they are known
		log.error("Error installing addon bundle from %s" % addonPath, exc_info=True)
		raise DisplayableError(
			displayMessage=pgettext(
				"addonStore",
				# Translators: The message displayed when an error occurs when installing an add-on package.
				# The %s will be replaced with the path to the add-on that could not be installed.
				"Failed to install add-on from %s"
			) % addonPath
		)
