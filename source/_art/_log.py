# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Logging indirection shared by both sides of the ART boundary.

Core-side ART code must log through NVDA's ``logHandler.log``,
but the host process is isolated from core and must not import from it.

The host entry point sets :data:`._HOST_MARKER_ENV` at run time, before any shared module is imported,
and this module reads it to tell the two sides apart.
Using an explicit signal rather than testing if ``logHandler`` can be imported
allows host processes to behave the same when running from source.

.. warning::
	This module must be imported lazily on the host,
	after :func:`.host.entrypoint.main` has set the marker.
	That includes transitive imports.
	Practically, that means that ``host.entrypoint`` should avoid importing ART code at module-scope.
"""

import os

from . import _HOST_MARKER_ENV

__all__ = ["log"]


if os.environ.get(_HOST_MARKER_ENV):
	# The isolated host: log to our own stdlib logger, never NVDA's.
	import logging

	#: The numeric level of NVDA's ``DEBUGWARNING``.
	#: Duplicated because the host must not import ``logHandler`` to read it; keep the two in sync.
	_DEBUGWARNING_LEVEL = 15
	logging.addLevelName(_DEBUGWARNING_LEVEL, "DEBUGWARNING")

	class _HostLogger(logging.LoggerAdapter):
		"""A stdlib logger extended with the NVDA ``Logger`` methods ART's shared code uses.

		Only ``debugWarning`` is needed today.
		Extend this if shared code starts calling more NVDA-specific logging methods.
		"""

		def debugWarning(self, msg: object, *args: object, **kwargs: object) -> None:
			"""Log ``msg`` at NVDA's ``DEBUGWARNING`` level."""
			self.log(_DEBUGWARNING_LEVEL, msg, *args, **kwargs)

	#: The logger shared ART code uses in the host process.
	#: The host writes to standard error, which NVDA drains into its own log.
	log = _HostLogger(logging.getLogger("_art"), {})
else:
	# Core, or an in-process test host: log through NVDA's own logger.
	from logHandler import log
