# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import typing
import dataclasses
from typing import (
	List,
	Optional,
)
from logHandler import log

from addonStore.models import (
	AddonDetailsModel,
	AvailableAddonsModel,
)

if typing.TYPE_CHECKING:
	# Remove when https://github.com/python/typing/issues/760 is resolved
	from _typeshed import SupportsLessThan


class AddonListVM:
	presentedAttributes = [
		"displayName",
		"versionName",
		"publisher",
	]

	def __init__(
			self,
			addonsModel: AvailableAddonsModel,
			selectedAddonId: Optional[str] = None,
	):
		self._addonsModel = addonsModel
		self._onSelectionChanged: callable(AddonDetailsModel)
		self.selectedAddonId = selectedAddonId
		self.lastSelectedAddonId = selectedAddonId
		self._sortByModelFieldName: str = "displayName"
		self._filterString: typing.Optional[str] = None

		self._setSelectionPending = False
		self._addonsFilteredOrdered: typing.List[str] = self._getFilteredSortedIds()
		self._validate(
			sortField=self._sortByModelFieldName,
			selectionIndex=self.getSelectedIndex(),
			selectionId=self.selectedAddonId
		)
		self.selectedAddonId = self._tryPersistSelection(self._addonsFilteredOrdered)
		self._updateAddonListing()

	def getAddonAttrText(self, index: int, attrName: str) -> str:
		""" Get the text for an item's attribute.
		@param index: The index of the item in _addonsFilteredOrdered
		@param attrName: The exposed attribute for the addon. See L{AddonList.presentedAttributes}
		@return: The text for the addon attribute
		"""
		assert attrName in AddonListVM.presentedAttributes
		addonItem = self._addonsModel[self._addonsFilteredOrdered[index]]
		return getattr(addonItem, attrName)

	def getCount(self) -> int:
		return len(self._addonsFilteredOrdered)

	def getSelectedIndex(self) -> Optional[int]:
		if self._addonsFilteredOrdered and self.selectedAddonId in self._addonsFilteredOrdered:
			return self._addonsFilteredOrdered.index(self.selectedAddonId)
		return None

	def setSelection(self, index: Optional[int]) -> Optional[AddonDetailsModel]:
		self._validate(selectionIndex=index)
		self.selectedAddonId = self._addonsFilteredOrdered[index] if index is not None else None
		return self.getSelection()

	def getSelection(self) -> Optional[AddonDetailsModel]:
		return self._addonsModel.get(self.selectedAddonId, None)

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
			assert (selectionId in self._addonsModel.keys())

	def setSortField(self, modelFieldName: str):
		self._validate(sortField=modelFieldName)
		self._sortByModelFieldName = modelFieldName
		self._updateAddonListing()

	def _getFilteredSortedIds(self) -> List[str]:
		def _getSortFieldData(model: AddonDetailsModel) -> "SupportsLessThan":
			return getattr(model, self._sortByModelFieldName)

		def _containsTerm(addonModel: AddonDetailsModel, term: str) -> bool:
			term = term.casefold()
			return (
				term in addonModel.displayName.casefold()
				or term in addonModel.description.casefold()
				or term in addonModel.publisher.casefold()
			)

		filtered = (
			a for a in self._addonsModel.values()
			if self._filterString is None or _containsTerm(a, self._filterString)
		)
		filteredSorted = list([
			a.addonId for a in sorted(filtered, key=_getSortFieldData)
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
		elif 1 > len(newOrder):
			log.debug(f"No entries in new order")
			# no entries after filter, select None
			return None
		elif selectedIndex is not None:
			# select the addon at the closest index
			oldMaxIndex: int = len(self._addonsFilteredOrdered) - 1
			oldIndexNorm: float = selectedIndex / oldMaxIndex  # min-max scaling / normalization
			newMaxIndex: int = len(newOrder) - 1
			approxNewIndex = int(oldIndexNorm * newMaxIndex)
			newSelectedIndex = max(0, min(approxNewIndex, newMaxIndex))
			log.debug(
				f"Approximate from position "
				f"oldSelectedIndex: {selectedIndex}, "
				f"oldMaxIndex: {oldMaxIndex}, "
				f"newSelectedIndex: {newSelectedIndex}, "
				f"newMaxIndex: {newMaxIndex}"
			)
			return newOrder[newSelectedIndex]
		elif self.lastSelectedAddonId in newOrder:
			log.debug(f"lastSelected in new order: {self.lastSelectedAddonId}")
			return self.lastSelectedAddonId
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
		if not filterText:
			filterText = None
		self._filterString = filterText
		self._updateAddonListing()


@dataclasses.dataclass
class AddonDetailsVM:
	display: Optional[AddonDetailsModel]

	def getAddonId(self) -> Optional[str]:
		return self.display.addonId if self.display else None


@dataclasses.dataclass
class AddonStoreVM:
	availableAddonsModel: AvailableAddonsModel
