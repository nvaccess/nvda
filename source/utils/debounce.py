# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from time import monotonic
from typing import Any, ParamSpec
from weakref import WeakKeyDictionary

import wx


P = ParamSpec("P")


@dataclass
class _DebounceState:
	lastCallTimeMs: float | None = None
	pendingHandle: wx.CallLater | None = None
	pendingArgs: tuple[Any, ...] = ()
	pendingKwargs: dict[str, Any] = field(default_factory=dict)


def _getStateForCall(
	instanceStates: WeakKeyDictionary[object, _DebounceState],
	defaultState: _DebounceState,
	args: tuple[Any, ...],
) -> _DebounceState:
	if not args:
		return defaultState
	instanceCandidate = args[0]
	try:
		return instanceStates.setdefault(instanceCandidate, _DebounceState())
	except TypeError:
		return defaultState


def _executeDelayedCall(func: Callable[..., Any], state: _DebounceState) -> None:
	args = state.pendingArgs
	kwargs = state.pendingKwargs
	func(*args, **kwargs)
	state.pendingArgs = ()
	state.pendingKwargs = {}
	state.pendingHandle = None


def _scheduleDelayedCall(
	state: _DebounceState,
	delayTimeMs: int,
	func: Callable[..., Any],
) -> None:
	if state.pendingHandle is None:
		state.pendingHandle = wx.CallLater(delayTimeMs, _executeDelayedCall, func, state)
	else:
		state.pendingHandle.Start(delayTimeMs)
	state.lastCallTimeMs = monotonic() * 1000


def debounceLimiter(
	*,
	cooldownTimeMs: int = 50,
	delayTimeMs: int = 50,
	runImmediateFirstCall: bool = True,
) -> Callable[[Callable[P, Any]], Callable[P, None]]:
	"""
	Limit the rate at which expensive functions are called.

	Executes calls immediately when outside the cooldown period (when there is no
	pending delayed call), and debounces calls received within ``cooldownTimeMs``
	by delaying their execution by ``delayTimeMs``.

	:param cooldownTimeMs: Time in milliseconds during which subsequent calls are considered to be within the cooldown period.
	:param delayTimeMs: Time in milliseconds to delay the execution of a call received during the cooldown period.
	:param runImmediateFirstCall: Whether the first call in a burst should execute immediately.
		If False, all calls are trailing-debounced by `delayTimeMs`.
	:returns: A decorator that debounces calls to the decorated function.
	:raises ValueError: If ``cooldownTimeMs`` or ``delayTimeMs`` is negative.
	"""
	if cooldownTimeMs < 0:
		raise ValueError("cooldownTimeMs must be non-negative")
	if delayTimeMs < 0:
		raise ValueError("delayTimeMs must be non-negative")

	def decorator(func: Callable[P, Any]) -> Callable[P, None]:
		instanceStates: WeakKeyDictionary[object, _DebounceState] = WeakKeyDictionary()
		stateForDecorated = _DebounceState()

		@wraps(func)
		def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
			state = _getStateForCall(instanceStates, stateForDecorated, args)
			nowMs = monotonic() * 1000
			withinCooldown = (
				state.lastCallTimeMs is not None and (nowMs - state.lastCallTimeMs) < cooldownTimeMs
			)
			if runImmediateFirstCall and not withinCooldown and state.pendingHandle is None:
				state.lastCallTimeMs = nowMs
				func(*args, **kwargs)
				return

			state.pendingArgs = args
			state.pendingKwargs = kwargs
			_scheduleDelayedCall(state, delayTimeMs, func)

		return wrapper

	return decorator
