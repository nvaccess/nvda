# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import importlib
import threading
from collections.abc import Callable
from typing import Any

from logHandler import log

from . import wordSegStrategy


def _runInitializer(
	initializer: Callable[..., Any],
	moduleName: str,
	qualname: str,
	args: tuple[Any, ...],
	kwargs: dict[str, Any],
) -> None:
	try:
		initializer(*args, **kwargs)
	except Exception:
		log.exception(f"Initializer {moduleName}.{qualname} failed")


def initialize() -> None:
	"""
	Call all registered initializer functions recorded in wordSegStrategy.

	Each entry is a tuple: (moduleName, qualname, funcObj, args, kwargs).
	We try to resolve the callable from the module and qualname at runtime
	(this handles classmethod/staticmethod wrapping order).
	If resolution fails, we fall back to the stored funcObj.

	Exceptions from individual initializers are caught and logged so that one
	failing initializer doesn't stop the rest.
	"""

	log.debug("Initializing word segmentation module")

	for moduleName, qualname, funcObj, args, kwargs in wordSegStrategy.iterInitializers():
		callableToCall: Callable[..., Any] = funcObj
		try:
			mod = importlib.import_module(moduleName)
			obj = mod
			for part in qualname.split("."):
				obj = getattr(obj, part)
			callableToCall = obj
		except Exception:
			log.debugWarning(
				f"Could not resolve initializer {moduleName}.{qualname}; falling back to the registered function",
				exc_info=True,
			)

		if not callable(callableToCall):
			log.debugWarning(f"Resolved initializer {moduleName}.{qualname} is not callable; skipping")
			continue
		try:
			threading.Thread(
				target=_runInitializer,
				args=(callableToCall, moduleName, qualname, args, kwargs),
				name=f"wordSeg initializer {moduleName}.{qualname}",
				daemon=True,
			).start()
		except Exception:
			log.exception(f"Failed to start initializer {moduleName}.{qualname}")
