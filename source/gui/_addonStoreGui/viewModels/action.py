# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Callable,
	Iterable,
	Optional,
	TYPE_CHECKING,
)

import extensionPoints

if TYPE_CHECKING:
	from .addonList import AddonListItemVM


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
			actionHandler: Callable[["AddonListItemVM", ], None],
			validCheck: Callable[["AddonListItemVM", ], bool],
			listItemVM: Optional["AddonListItemVM"],
	):
		"""
		@param displayName: Translated string, to be displayed to the user. Should describe the action / behaviour.
		@param actionHandler: Call when the action is triggered.
		@param validCheck: Is the action valid for the current listItemVM
		@param listItemVM: The listItemVM this action will be applied to. L{updated} notifies of modification.
		"""
		self.displayName: str = displayName
		self.actionHandler: Callable[["AddonListItemVM", ], None] = actionHandler
		self._validCheck: Callable[["AddonListItemVM", ], bool] = validCheck
		self._listItemVM: Optional["AddonListItemVM"] = listItemVM
		if listItemVM:
			listItemVM.updated.register(self._listItemChanged)
		self.updated = extensionPoints.Action()
		"""Notify of changes to the action"""

	def _listItemChanged(self, addonListItemVM: "AddonListItemVM"):
		"""Something inside the AddonListItemVM has changed"""
		assert self._listItemVM == addonListItemVM
		self._notify()

	def _notify(self):
		# ensure calling on the main thread.
		from core import callLater
		callLater(delay=0, callable=self.updated.notify, addonActionVM=self)

	@property
	def isValid(self) -> bool:
		return (
			self._listItemVM is not None
			and self._validCheck(self._listItemVM)
		)

	@property
	def listItemVM(self) -> Optional["AddonListItemVM"]:
		return self._listItemVM

	@listItemVM.setter
	def listItemVM(self, listItemVM: Optional["AddonListItemVM"]):
		if self._listItemVM == listItemVM:
			return
		if self._listItemVM:
			self._listItemVM.updated.unregister(self._listItemChanged)
		if listItemVM:
			listItemVM.updated.register(self._listItemChanged)
		self._listItemVM = listItemVM
		self._notify()


class BulkAddonActionVM:
	"""
	Actions/behaviour that can be embedded within other views/viewModels
	that can apply to a group of L{AddonListItemVM}.
	Use the L{BulkAddonActionVM.updated} extensionPoint.Action to be notified about changes.
	E.G.:
	- Updates within the AddonListItemVM (perhaps changing the action validity)
	- Entirely changing the AddonListItemVM action will be applied to, the validity can be checked for the new
	item.
	"""
	def __init__(
			self,
			displayName: str,
			actionHandler: Callable[[Iterable["AddonListItemVM"], ], None],
			validCheck: Callable[[Iterable["AddonListItemVM"], ], bool],
			listItemVMs: Iterable["AddonListItemVM"],
	):
		"""
		@param displayName: Translated string, to be displayed to the user. Should describe the action / behaviour.
		@param actionHandler: Call when the action is triggered.
		@param validCheck: Is the action valid for the current listItemVMs
		@param listItemVMs: The listItemVMs this action will be applied to. L{updated} notifies of modification.
		"""
		self.displayName = displayName
		self.actionHandler = actionHandler
		self._validCheck = validCheck
		self._listItemVMs = listItemVMs
		for listItemVM in listItemVMs:
			listItemVM.updated.register(self._listItemChanged)
		self.updated = extensionPoints.Action()
		"""Notify of changes to the action"""

	def _listItemChanged(self, addonListItemVM: "AddonListItemVM"):
		"""Something inside the AddonListItemVM has changed"""
		assert addonListItemVM in self._listItemVMs, f"{addonListItemVM} {list(self._listItemVMs)}"
		self._notify()

	def _notify(self):
		# ensure calling on the main thread.
		from core import callLater
		callLater(delay=0, callable=self.updated.notify, addonActionVM=self)

	@property
	def isValid(self) -> bool:
		return self._validCheck(self._listItemVMs)

	@property
	def listItemVMs(self) -> Iterable["AddonListItemVM"]:
		return self._listItemVMs

	@listItemVMs.setter
	def listItemVMs(self, newListItemVMs: Iterable["AddonListItemVM"]):
		if self._listItemVMs == newListItemVMs:
			return
		for oldListItemVM in self._listItemVMs:
			if oldListItemVM not in newListItemVMs:
				oldListItemVM.updated.unregister(self._listItemChanged)
		
		for newListItemVM in newListItemVMs:
			if newListItemVM not in self._listItemVMs:
				newListItemVM.updated.register(self._listItemChanged)

		self._listItemVMs = newListItemVMs
		self._notify()
