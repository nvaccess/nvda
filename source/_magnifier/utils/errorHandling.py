# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Error handling helpers for the magnifier module.
"""

from collections.abc import Callable
from functools import wraps
from logHandler import log
from typing import ParamSpec, TypeVar, cast
from ..config import _isDebug


# ParamSpec captures the full parameter signature of a callable (names, types, defaults).
# TypeVar captures the return type.
# Together they allow the decorator to preserve the exact signature of the wrapped function,
# so callers and type checkers see the original parameters and return type unchanged.
_P = ParamSpec("_P")
_R = TypeVar("_R")


class MagnifierStartError(Exception):
	"""Raised when the magnifier fails to start.

	Carries a user-facing, translatable message describing why the start failed
	(e.g. another magnifier application is already running, or screen curtain is active),
	so callers can present it appropriately: spoken for keyboard commands, or in a message
	box for GUI actions.
	"""

	def __init__(self, message: str):
		"""
		:param message: The user-facing, translatable message describing the failure.
		"""
		super().__init__(message)
		self.message = message


def trackNativeMagnifierErrors(func: Callable[_P, _R]) -> Callable[_P, _R]:
	"""
	Decorator for native magnifier API calls.

	This decorator handles only OSError, which is what our Windows/native
	bindings raise when an API call fails. Any other exception is re-raised,
	so programming bugs are not hidden.

	On OSError, the failure is logged at debug level using the function's
	qualified path and execution continues (returns None).
	"""

	# @wraps copies __name__, __doc__, __module__ and __qualname__ from func
	# onto _wrapped, so the wrapped method keeps its original identity in
	# logs, debuggers and stack traces.
	@wraps(func)
	def _wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _R:
		try:
			return func(*args, **kwargs)
		except OSError:
			if _isDebug():
				functionPath = f"{func.__module__}.{func.__qualname__}"
				log.debug(f"Native magnifier operation failed: {functionPath}", exc_info=True)
			return cast(_R, None)

	return _wrapped
