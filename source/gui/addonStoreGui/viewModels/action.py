# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from abc import ABC, abstractmethod
from typing import (
	Callable,
	Generic,
	Iterable,
	Optional,
	TypeVar,
	TYPE_CHECKING,
)

import extensionPoints
from logHandler import log

if TYPE_CHECKING:
	from .addonList import AddonListItemVM


ActionTargetT = TypeVar("ActionTargetT", Optional["AddonListItemVM"], Iterable["AddonListItemVM"])


class _AddonAction(Generic[ActionTargetT], ABC):
	def __init__(
		self,
		displayName: str,
		actionHandler: Callable[[ActionTargetT], None],
		validCheck: Callable[[ActionTargetT], bool],
		actionTarget: ActionTargetT,
	):
		"""
		@param displayName: Translated string, to be displayed to the user. Should describe the action / behaviour.
		@param actionHandler: Call when the action is triggered.
		@param validCheck: Is the action valid for the current target
		@param actionTarget: The target this action will be applied to. L{updated} notifies of modification.
		"""
		self.displayName = displayName
		self.actionHandler = actionHandler
		self._validCheck = validCheck
		self._actionTarget = actionTarget
		self.updated = extensionPoints.Action()
		"""Notify of changes to the action"""

	@abstractmethod
	def _listItemChanged(self, addonListItemVM: "AddonListItemVM"): ...

	@property
	def isValid(self) -> bool:
		return self._validCheck(self._actionTarget)

	@property
	def actionTarget(self) -> ActionTargetT:
		return self._actionTarget

	def _notify(self):
		# ensure calling on the main thread.
		from core import callLater

		callLater(delay=0, callable=self.updated.notify, addonActionVM=self)


class AddonActionVM(_AddonAction[Optional["AddonListItemVM"]]):
	"""Actions/behaviour that can be embedded within other views/viewModels that can apply to a single
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
		actionHandler: Callable[["AddonListItemVM"], None],
		validCheck: Callable[["AddonListItemVM"], bool],
		actionTarget: Optional["AddonListItemVM"],
	):
		"""
		@param displayName: Translated string, to be displayed to the user. Should describe the action / behaviour.
		@param actionHandler: Call when the action is triggered.
		@param validCheck: Is the action valid for the current listItemVM
		@param actionTarget: The listItemVM this action will be applied to. L{updated} notifies of modification.
		"""

		def _validCheck(listItemVM: Optional["AddonListItemVM"]) -> bool:
			# Handle the None case so that each validCheck doesn't have to.
			return listItemVM is not None and validCheck(listItemVM)

		def _actionHandler(listItemVM: Optional["AddonListItemVM"]):
			# Handle the None case so that each actionHandler doesn't have to.
			if listItemVM is not None:
				actionHandler(listItemVM)
			else:
				log.warning(f"Action triggered for invalid None listItemVM: {self.displayName}")

		super().__init__(displayName, _actionHandler, _validCheck, actionTarget)
		if actionTarget:
			actionTarget.updated.register(self._listItemChanged)

	def _listItemChanged(self, addonListItemVM: Optional["AddonListItemVM"]):
		"""Something inside the AddonListItemVM has changed"""
		assert self._actionTarget == addonListItemVM
		self._notify()

	@_AddonAction.actionTarget.setter
	def actionTarget(self, newActionTarget: Optional["AddonListItemVM"]):
		if self._actionTarget == newActionTarget:
			return
		if self._actionTarget:
			self._actionTarget.updated.unregister(self._listItemChanged)
		if newActionTarget:
			newActionTarget.updated.register(self._listItemChanged)
		self._actionTarget = newActionTarget
		self._notify()


class BatchAddonActionVM(_AddonAction[Iterable["AddonListItemVM"]]):
	"""
	Actions/behaviour that can be embedded within other views/viewModels
	that can apply to a group of L{AddonListItemVM}.
	Use the L{BatchAddonActionVM.updated} extensionPoint.Action to be notified about changes.
	E.G.:
	- Updates within the AddonListItemVM (perhaps changing the action validity)
	- Entirely changing the AddonListItemVM action will be applied to, the validity can be checked for the new
	item.
	"""

	def __init__(
		self,
		displayName: str,
		actionHandler: Callable[[Iterable["AddonListItemVM"]], None],
		validCheck: Callable[[Iterable["AddonListItemVM"]], bool],
		actionTarget: Iterable["AddonListItemVM"],
	):
		"""
		@param displayName: Translated string, to be displayed to the user. Should describe the action / behaviour.
		@param actionHandler: Call when the action is triggered.
		@param validCheck: Is the action valid for the current listItemVMs
		@param actionTarget: The listItemVMs this action will be applied to. L{updated} notifies of modification.
		"""
		super().__init__(displayName, actionHandler, validCheck, actionTarget)
		for listItemVM in self._actionTarget:
			listItemVM.updated.register(self._listItemChanged)

	def _listItemChanged(self, addonListItemVM: "AddonListItemVM"):
		"""Something inside the AddonListItemVM has changed"""
		assert addonListItemVM in self._actionTarget
		self._notify()

	@_AddonAction.actionTarget.setter
	def actionTarget(self, newActionTarget: Iterable["AddonListItemVM"]):
		if self._actionTarget == newActionTarget:
			return

		for oldListItemVM in self._actionTarget:
			if oldListItemVM not in newActionTarget:
				oldListItemVM.updated.unregister(self._listItemChanged)

		for newListItemVM in newActionTarget:
			if newListItemVM not in self._actionTarget:
				newListItemVM.updated.register(self._listItemChanged)

		self._actionTarget = newActionTarget
		self._notify()
