# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited.

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from time import monotonic
from typing import Any, ParamSpec
from weakref import WeakKeyDictionary

from logHandler import log
import wx


P = ParamSpec("P")


@dataclass
class _DebounceState:
	lastExecutionTimeMs: float | None = None
	pendingHandle: wx.CallLater | None = None
	pendingArgs: tuple[Any, ...] = ()
	pendingKwargs: dict[str, Any] | None = None


def _getStateForCall(
	instanceStates: WeakKeyDictionary[object, _DebounceState],
	globalState: _DebounceState,
	args: tuple[Any, ...],
) -> _DebounceState:
	if not args:
		return globalState
	instanceCandidate = args[0]
	try:
		return instanceStates.setdefault(instanceCandidate, _DebounceState())
	except TypeError:
		return globalState


def _executeDelayedCall(func: Callable[..., Any], state: _DebounceState) -> None:
	args = state.pendingArgs
	kwargs = state.pendingKwargs or {}
	state.pendingArgs = ()
	state.pendingKwargs = None
	state.pendingHandle = None
	state.lastExecutionTimeMs = monotonic() * 1000
	func(*args, **kwargs)


def _scheduleDelayedCall(
	state: _DebounceState,
	delayTimeMs: int,
	func: Callable[..., Any],
) -> None:
	state.pendingHandle = wx.CallLater(delayTimeMs, _executeDelayedCall, func, state)


def debounceLimiter(
	cooldownTimeMs: int = 50,
	delayTimeMs: int = 50,
) -> Callable[[Callable[P, Any]], Callable[P, None]]:
	"""
	:param cooldownTimeMs: Time in milliseconds during which subsequent calls are considered to be within the cooldown period.
	:param delayTimeMs: Time in milliseconds to delay the execution of a call received during the
	cooldown period.
	:returns: A decorator that debounces calls to the decorated function.

	Executes calls immediately when outside the cooldown period (when there is no
	pending delayed call), and debounces calls received within `cooldownTimeMs`
	by delaying their execution by `delayTimeMs`.
	"""
	if cooldownTimeMs < 0:
		raise ValueError("cooldownTimeMs must be non-negative")
	if delayTimeMs < 0:
		raise ValueError("delayTimeMs must be non-negative")

	def decorator(func: Callable[P, Any]) -> Callable[P, None]:
		instanceStates: WeakKeyDictionary[object, _DebounceState] = WeakKeyDictionary()
		globalState = _DebounceState()

		@wraps(func)
		def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
			state = _getStateForCall(instanceStates, globalState, args)
			nowMs = monotonic() * 1000
			withinCooldown = (
				state.lastExecutionTimeMs is not None and (nowMs - state.lastExecutionTimeMs) < cooldownTimeMs
			)
			if not withinCooldown and state.pendingHandle is None:
				state.lastExecutionTimeMs = nowMs
				func(*args, **kwargs)
				return

			state.pendingArgs = args
			state.pendingKwargs = kwargs
			_scheduleDelayedCall(state, delayTimeMs, func)

		return wrapper

	return decorator
