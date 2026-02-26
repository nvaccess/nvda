# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited.

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from functools import wraps
import threading
from time import monotonic
from typing import Any, ParamSpec
from weakref import WeakKeyDictionary

from logHandler import log
import wx


P = ParamSpec("P")

class ThreadTarget(Enum):
	"""
	When debouncing a task, specify the thread to run the task on.
	"""

	GUI = auto()
	"""
	Uses wx.CallLater to run the job on the GUI thread.
	This is encouraged for tasks that interact with the GUI, such as dialogs.
	"""

	DAEMON = auto()
	"""
	Uses threading.Thread(daemon=True) to run the job in the background.
	"""


@dataclass
class _DebounceState:
	lastExecutionTimeMs: float | None = None
	pendingHandle: wx.Timer | threading.Timer | None = None
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
	callLater: Callable[..., Any],
	threadTarget: ThreadTarget,
	delayTimeMs: int,
	func: Callable[..., Any],
) -> None:
	handle = state.pendingHandle
	if handle is not None:
		match threadTarget:
			case ThreadTarget.GUI:
				assert isinstance(handle, wx.Timer)
				handle.Stop()
			case ThreadTarget.DAEMON:
				assert isinstance(handle, threading.Timer)
				handle.cancel()
			case _:
				raise ValueError(f"Invalid threadTarget value: {threadTarget}")
	state.pendingHandle = callLater(delayTimeMs, _executeDelayedCall, func, state)


def _debounceThreadDecider(
	threadTarget: ThreadTarget,
) -> Callable[..., Any]:
	match threadTarget:
		case ThreadTarget.GUI:
			def callJobOnThread(delayTimeMs: int, func: Callable[..., Any], *args, **kwargs):
				log.debug(f"Scheduling delayed job on GUI thread in {delayTimeMs}ms")
				return wx.CallLater(delayTimeMs, func, *args, **kwargs)
		case ThreadTarget.DAEMON:
			def callJobOnThread(delayTimeMs: int, func: Callable[..., Any], *args, **kwargs):
				log.debug(f"Executing delayed job on thread {threading.get_ident()}")
				timer = threading.Timer(delayTimeMs / 1000, func, args=args, kwargs=kwargs)
				timer.daemon = True
				timer.name = f"DebounceTimer-{func.__name__}"
				timer.start()
				return timer
		case _:
			raise ValueError(f"Invalid threadTarget value: {threadTarget}")
	return callJobOnThread


def debounceLimiter(
	cooldownTimeMs: int = 50,
	delayTimeMs: int = 50,
	threadTarget: ThreadTarget = ThreadTarget.GUI,
) -> Callable[[Callable[P, Any]], Callable[P, None]]:
	"""
	:param cooldownTimeMs: Time in milliseconds during which subsequent calls are considered to be within the cooldown period.
	:param delayTimeMs: Time in milliseconds to delay the execution of a call received during the
	cooldown period.
	:param threadTarget: The thread to run the task on.
	:returns: A decorator that debounces calls to the decorated function.

	Create a decorator that executes the first call immediately, then debounces
	subsequent calls received within `cooldownTimeMs` by delaying execution by
	`delayTimeMs`.
	"""
	if cooldownTimeMs < 0:
		raise ValueError("cooldownTimeMs must be non-negative")
	if delayTimeMs < 0:
		raise ValueError("delayTimeMs must be non-negative")

	def decorator(func: Callable[P, Any]) -> Callable[P, None]:
		instanceStates: WeakKeyDictionary[object, _DebounceState] = WeakKeyDictionary()
		globalState = _DebounceState()
		callLater = _debounceThreadDecider(threadTarget)

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
			_scheduleDelayedCall(state, callLater, threadTarget, delayTimeMs, func)

		return wrapper

	return decorator
