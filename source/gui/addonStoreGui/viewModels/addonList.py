# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from dataclasses import dataclass
from enum import Enum

from locale import strxfrm
from typing import (
	FrozenSet,
	Generic,
	List,
	Optional,
	TYPE_CHECKING,
	TypeVar,
)

from requests.structures import CaseInsensitiveDict

from addonStore.models.addon import (
	_AddonGUIModel,
	_AddonStoreModel,
	_AddonManifestModel,
)
from addonStore.models.status import (
	_installedAddonStatuses,
	_StatusFilterKey,
	AvailableAddonStatus,
)
import core
import extensionPoints
from logHandler import log


if TYPE_CHECKING:
	# Remove when https://github.com/python/typing/issues/760 is resolved
	from _typeshed import SupportsLessThan  # noqa: F401
	from .store import AddonStoreVM


@dataclass
class _AddonListFieldData:
	displayString: str
	width: int
	hideStatuses: FrozenSet[_StatusFilterKey] = frozenset()
	"""Hide this field if the current tab filter is in hideStatuses."""


class AddonListField(_AddonListFieldData, Enum):
	"""An ordered enum of fields to use as columns in the add-on list."""

	displayName = (
		# Translators: The name of the column that contains names of addons.
		pgettext("addonStore", "Name"),
		150,
	)
	status = (
		# Translators: The name of the column that contains the status of the addon.
		# e.g. available, downloading installing
		pgettext("addonStore", "Status"),
		150
	)
	currentAddonVersionName = (
		# Translators: The name of the column that contains the installed addon's version string.
		pgettext("addonStore", "Installed version"),
		100,
		frozenset({_StatusFilterKey.AVAILABLE}),
	)
	availableAddonVersionName = (
		# Translators: The name of the column that contains the available addon's version string.
		pgettext("addonStore", "Available version"),
		100,
		frozenset({_StatusFilterKey.INCOMPATIBLE, _StatusFilterKey.INSTALLED}),
	)
	channel = (
		# Translators: The name of the column that contains the channel of the addon (e.g stable, beta, dev).
		pgettext("addonStore", "Channel"),
		50,
	)
	publisher = (
		# Translators: The name of the column that contains the addon's publisher.
		pgettext("addonStore", "Publisher"),
		100,
		frozenset({_StatusFilterKey.INCOMPATIBLE, _StatusFilterKey.INSTALLED})
	)
	author = (
		# Translators: The name of the column that contains the addon's author.
		pgettext("addonStore", "Author"),
		100,
		frozenset({_StatusFilterKey.AVAILABLE, _StatusFilterKey.UPDATE})
	)


_AddonModelT = TypeVar("_AddonModelT", bound=_AddonGUIModel)


class AddonListItemVM(Generic[_AddonModelT]):
	def __init__(
			self,
			model: _AddonModelT,
			status: AvailableAddonStatus = AvailableAddonStatus.AVAILABLE
	):
		self._model: _AddonModelT = model  # read-only
		self._status: AvailableAddonStatus = status  # modifications triggers L{updated.notify}
		self.updated = extensionPoints.Action()  # Notify of changes to VM, argument: addonListItemVM

	@property
	def model(self) -> _AddonModelT:
		return self._model

	@property
	def status(self) -> AvailableAddonStatus:
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

	def canUseInstallAction(self) -> bool:
		return self.status == AvailableAddonStatus.AVAILABLE

	def canUseInstallOverrideIncompatibilityAction(self) -> bool:
		return self.status == AvailableAddonStatus.INCOMPATIBLE and self.model.canOverrideCompatibility

	def canUseUpdateAction(self) -> bool:
		return self.status == AvailableAddonStatus.UPDATE

	def canUseUpdateOverrideIncompatibilityAction(self) -> bool:
		return self.status == AvailableAddonStatus.UPDATE_INCOMPATIBLE and self.model.canOverrideCompatibility

	def canUseReplaceAction(self) -> bool:
		return self.status == AvailableAddonStatus.REPLACE_SIDE_LOAD

	def canUseRemoveAction(self) -> bool:
		return (
			self.model.isInstalled
			and self.status in _installedAddonStatuses
			and self.status != AvailableAddonStatus.PENDING_REMOVE
		)

	def canUseEnableAction(self) -> bool:
		return self.status == AvailableAddonStatus.DISABLED or self.status == AvailableAddonStatus.PENDING_DISABLE

	def canUseEnableOverrideIncompatibilityAction(self) -> bool:
		return self.status in (
			AvailableAddonStatus.INCOMPATIBLE_DISABLED,
			AvailableAddonStatus.PENDING_INCOMPATIBLE_DISABLED,
		) and self.model.canOverrideCompatibility

	def canUseDisableAction(self) -> bool:
		return (
			self.model.isInstalled
			and self.status in _installedAddonStatuses
			and self.status not in (
				AvailableAddonStatus.DISABLED,
				AvailableAddonStatus.PENDING_DISABLE,
				AvailableAddonStatus.INCOMPATIBLE_DISABLED,
				AvailableAddonStatus.PENDING_INCOMPATIBLE_DISABLED,
				AvailableAddonStatus.PENDING_REMOVE,
			)
		)

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}: {self.Id}, {self.status}"


class AddonDetailsVM:
	def __init__(self, listVM: "AddonListVM"):
		self._listVM = listVM
		self._listItem: Optional[AddonListItemVM] = listVM.getSelection()
		self.updated = extensionPoints.Action()  # triggered by setting L{self._listItem}

	@property
	def listItem(self) -> Optional[AddonListItemVM]:
		return self._listItem

	@listItem.setter
	def listItem(self, newListItem: Optional[AddonListItemVM]):
		self._listItem = newListItem
		# ensure calling on the main thread.
		core.callLater(delay=0, callable=self.updated.notify, addonDetailsVM=self)


class AddonListVM:
	def __init__(
			self,
			addons: List[AddonListItemVM],
			storeVM: "AddonStoreVM",
	):
		self._isLoading: bool = False
		self._addons: CaseInsensitiveDict[AddonListItemVM[_AddonGUIModel]] = CaseInsensitiveDict()
		self._storeVM = storeVM
		self.itemUpdated = extensionPoints.Action()
		self.updated = extensionPoints.Action()
		self.selectionChanged = extensionPoints.Action()
		self.selectedAddonId: Optional[str] = None
		self.lastSelectedAddonId = self.selectedAddonId
		self._sortByModelField: AddonListField = AddonListField.displayName
		self._filterString: Optional[str] = None

		self._setSelectionPending = False
		self._addonsFilteredOrdered: List[str] = self._getFilteredSortedIds()
		self._validate(
			sortField=self._sortByModelField,
			selectionIndex=self.getSelectedIndex(),
			selectionId=self.selectedAddonId
		)
		self.selectedAddonId = self._tryPersistSelection(self._addonsFilteredOrdered)
		self.resetListItems(addons)

	@property
	def presentedFields(self) -> List[AddonListField]:
		return [c for c in AddonListField if self._storeVM._filteredStatusKey not in c.hideStatuses]

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

	def getAddonFieldText(self, index: int, field: AddonListField) -> Optional[str]:
		""" Get the text for an item's attribute.
		@param index: The index of the item in _addonsFilteredOrdered
		@param field: The field attribute for the addon. See L{AddonList.presentedFields}
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
		return self._getAddonFieldText(listItemVM, field)

	def _getAddonFieldText(self, listItemVM: AddonListItemVM, field: AddonListField) -> str:
		assert field in AddonListField
		if field is AddonListField.currentAddonVersionName:
			return listItemVM.model._addonHandlerModel.version
		if field is AddonListField.availableAddonVersionName:
			return listItemVM.model.addonVersionName
		if field is AddonListField.status:  # special handling, not on the model.
			return listItemVM.status.displayString
		if field is AddonListField.channel:
			return listItemVM.model.channel.displayString
		return getattr(listItemVM.model, field.name)

	def getCount(self) -> int:
		return len(self._addonsFilteredOrdered)

	def getSelectedIndex(self) -> Optional[int]:
		if self._addonsFilteredOrdered and self.selectedAddonId in self._addonsFilteredOrdered:
			return self._addonsFilteredOrdered.index(self.selectedAddonId)
		return None

	def getAddonAtIndex(self, index: int) -> AddonListItemVM:
		self._validate(selectionIndex=index)
		selectedAddonId = self._addonsFilteredOrdered[index]
		return self._addons[selectedAddonId]

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
			sortField: Optional[AddonListField] = None,
			selectionIndex: Optional[int] = None,
			selectionId: Optional[str] = None,
	):
		if sortField is not None:
			assert sortField in AddonListField
		if selectionIndex is not None:
			assert 0 <= selectionIndex and selectionIndex < len(self._addonsFilteredOrdered)
		if selectionId is not None:
			assert selectionId in self._addons.keys()

	def setSortField(self, modelField: AddonListField):
		oldOrder = self._addonsFilteredOrdered
		self._validate(sortField=modelField)
		self._sortByModelField = modelField
		self._updateAddonListing()
		if oldOrder != self._addonsFilteredOrdered:
			# ensure calling on the main thread.
			core.callLater(delay=0, callable=self.updated.notify)

	def _getFilteredSortedIds(self) -> List[str]:
		def _getSortFieldData(listItemVM: AddonListItemVM) -> "SupportsLessThan":
			return strxfrm(self._getAddonFieldText(listItemVM, self._sortByModelField))

		def _containsTerm(detailsVM: AddonListItemVM, term: str) -> bool:
			term = term.casefold()
			model = detailsVM.model
			inPublisher = isinstance(model, _AddonStoreModel) and term in model.publisher.casefold()
			inAuthor = isinstance(model, _AddonManifestModel) and term in model.author.casefold()
			return (
				term in model.displayName.casefold()
				or term in model.description.casefold()
				or term in model.addonId.casefold()
				or inPublisher
				or inAuthor
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
