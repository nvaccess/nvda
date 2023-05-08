# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Needed for type hinting CaseInsensitiveDict
# Can be removed in a future version of python (3.8+)
from __future__ import annotations

from locale import strxfrm
from typing import (
	Callable,
	List,
	Optional,
	TYPE_CHECKING,
)

from requests.structures import CaseInsensitiveDict

from _addonStore.models.addon import (
	AddonGUIModel,
)
from _addonStore.models.status import (
	AvailableAddonStatus,
)
import core
import extensionPoints
from logHandler import log


if TYPE_CHECKING:
	# Remove when https://github.com/python/typing/issues/760 is resolved
	from _typeshed import SupportsLessThan  # noqa: F401


class AddonListItemVM:
	def __init__(
			self,
			model: AddonGUIModel,
			status: AvailableAddonStatus = AvailableAddonStatus.AVAILABLE
	):
		self._model: AddonGUIModel = model  # read-only
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
			return strxfrm(self._getAddonAttrText(listItemVM, self._sortByModelFieldName))

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
