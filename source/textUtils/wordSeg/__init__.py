# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import importlib
from logHandler import log


def initialize():
	"""
	Call all registered initializer functions recorded in wordSegStrategy.initializerList.

	Each entry is a tuple: (module_name, qualname, func_obj, args, kwargs).
	We try to resolve the callable from the module and qualname at runtime
	(this handles classmethod/staticmethod wrapping order). If resolution fails,
	we fall back to the stored func_obj.

	Exceptions from individual initializers are caught and logged so that one
	failing initializer doesn't stop the rest.
	"""

	from . import wordSegStrategy

	for module_name, qualname, func_obj, args, kwargs in getattr(wordSegStrategy, "initializerList", []):
		callable_to_call = None
		# try to resolve module + qualname to a current attribute (handles classmethod/staticmethod)
		try:
			mod = importlib.import_module(module_name)
			obj = mod
			for part in qualname.split("."):
				obj = getattr(obj, part)
			callable_to_call = obj
		except Exception:
			# fallback to original function object captured during decoration
			callable_to_call = func_obj

		# Final call with its args/kwargs and exception handling
		try:
			if not callable(callable_to_call):
				raise TypeError(f"Resolved initializer is not callable: {module_name}.{qualname}")
			callable_to_call(*args, **kwargs)
		except Exception as e:
			log.debug("Initializer %s.%s failed: %s", module_name, qualname, e)
		return
