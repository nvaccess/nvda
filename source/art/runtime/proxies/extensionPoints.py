# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

from typing import Any, Callable, Generator, Generic, TypeVar

from .base import ServiceProxyMixin

HandlerT = TypeVar("HandlerT")
FilterValueT = TypeVar("FilterValueT")
ChainValueTypeT = TypeVar("ChainValueTypeT")


class ExtensionPointProxyBase(ServiceProxyMixin):
	"""Base class for extension point proxies."""

	_service_env_var = "NVDA_ART_HANDLERS_SERVICE_URI"

	def __init__(self, name: str, epType: str) -> None:
		self.name = name
		self.epType = epType

	def register(self, handler: Callable) -> None:
		"""Register a handler for this extension point."""
		handlerService = self._get_service()
		if handlerService:
			try:
				handlerService.registerHandler(self.name, handler, self.epType)
			except Exception:
				pass


class ActionProxy(ExtensionPointProxyBase):
	"""Proxy for Action extension points."""

	def __init__(self, name: str) -> None:
		super().__init__(name, "action")

	def notify(self, **kwargs: Any) -> None:
		"""Notify handlers - this is called from NVDA core, not add-ons."""
		pass


class FilterProxy(ExtensionPointProxyBase, Generic[FilterValueT]):
	"""Proxy for Filter extension points."""

	def __init__(self, name: str) -> None:
		super().__init__(name, "filter")

	def apply(self, value: FilterValueT, **kwargs: Any) -> FilterValueT:
		"""Apply filters - this is called from NVDA core, not add-ons."""
		return value


class DeciderProxy(ExtensionPointProxyBase):
	"""Proxy for Decider extension points."""

	def __init__(self, name: str) -> None:
		super().__init__(name, "decider")

	def decide(self, **kwargs: Any) -> bool:
		"""Make decision - this is called from NVDA core, not add-ons."""
		return True


class AccumulatingDeciderProxy(ExtensionPointProxyBase):
	"""Proxy for AccumulatingDecider extension points."""

	def __init__(self, name: str, defaultDecision: bool) -> None:
		super().__init__(name, "accumulating_decider")
		self.defaultDecision = defaultDecision

	def decide(self, **kwargs: Any) -> bool:
		"""Make decision - this is called from NVDA core, not add-ons."""
		return self.defaultDecision


class ChainProxy(ExtensionPointProxyBase, Generic[ChainValueTypeT]):
	"""Proxy for Chain extension points."""

	def __init__(self, name: str) -> None:
		super().__init__(name, "chain")

	def iter(self, **kwargs: Any) -> Generator[ChainValueTypeT, None, None]:
		"""Iterate values - this is called from NVDA core, not add-ons."""
		return
		yield


class ConfigExtensionPoints:
	post_configProfileSwitch = ActionProxy("config.post_configProfileSwitch")
	pre_configProfileSwitch = ActionProxy("config.pre_configProfileSwitch")
	configProfileSwitched = ActionProxy("config.configProfileSwitched")


class InputCoreExtensionPoints:
	decide_executeGesture = DeciderProxy("inputCore.decide_executeGesture")


config = ConfigExtensionPoints()
inputCore = InputCoreExtensionPoints()
