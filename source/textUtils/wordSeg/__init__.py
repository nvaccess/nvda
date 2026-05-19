# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import importlib
import threading
from collections.abc import Callable
from typing import Any

from logHandler import log


def _runInitializer(
	initializer: Callable[..., Any],
	module_name: str,
	qualname: str,
	args: tuple[Any, ...],
	kwargs: dict[str, Any],
) -> None:
	try:
		initializer(*args, **kwargs)
	except Exception:
		log.exception(f"Initializer {module_name}.{qualname} failed")


def initialize() -> None:
	"""
	Call all registered initializer functions recorded in wordSegStrategy.initializerList.

	Each entry is a tuple: (module_name, qualname, func_obj, args, kwargs).
	We try to resolve the callable from the module and qualname at runtime
	(this handles classmethod/staticmethod wrapping order). If resolution fails,
	we fall back to the stored func_obj.

	Exceptions from individual initializers are caught and logged so that one
	failing initializer doesn't stop the rest.
	"""

	log.debug("Initializing word segmentation module")
	from . import wordSegStrategy

	for module_name, qualname, func_obj, args, kwargs in wordSegStrategy.initializerList:
		callable_to_call: Callable[..., Any] = func_obj
		try:
			mod = importlib.import_module(module_name)
			obj = mod
			for part in qualname.split("."):
				obj = getattr(obj, part)
			callable_to_call = obj
		except Exception:
			log.debugWarning(
				f"Could not resolve initializer {module_name}.{qualname}; falling back to the registered function",
				exc_info=True,
			)

		if not callable(callable_to_call):
			log.debugWarning(f"Resolved initializer {module_name}.{qualname} is not callable; skipping")
			continue
		try:
			threading.Thread(
				target=_runInitializer,
				args=(callable_to_call, module_name, qualname, args, kwargs),
				daemon=True,
			).start()
		except Exception:
			log.exception(f"Failed to start initializer {module_name}.{qualname}")
