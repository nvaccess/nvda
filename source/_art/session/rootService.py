# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""The root service core exposes to the host over the control connection."""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Literal

import rpyc
from logHandler import log

from ..exceptions import PermissionNotGrantedError
from ..transport import Service


@rpyc.service
class CoreRootService(Service):
	"""The irreducible API core hands down to an add-on.

	This is the host's entry point into core,
	and the object through which an add-on asks for the capabilities it wants.
	"""

	def __init__(self, onReady: Callable[[str | None], None] | None = None) -> None:
		"""Initializer.

		:param onReady: Called with the outcome of the host's readiness signal:
			``None`` if the host is ready, or why launch failed.
			Called at most once, on the connection's serving thread, so it must not block.
		"""
		super().__init__()
		self._onReady = onReady
		self._readinessLock = threading.Lock()
		self._readinessReported = False

	@Service.exposed
	def ping(self) -> Literal["pong"]:
		"""Report that core is serving requests.

		:returns: "pong"
		"""
		return "pong"

	@Service.exposed
	def _ready(self, failure: str | None = None) -> None:
		"""Receive the host's readiness signal, which ends launch.

		Exposed under a sunder name to mark it as ART's own launch plumbing,
		rather than part of the API that add-ons build on.

		Only the first signal counts.
		The add-on shares the host's process, so it can send this too;
		anything after the first is treated as untrusted noise, and logged and ignored.

		:param failure: Why launch failed, or ``None`` if the host is ready to serve.
		:raises TypeError: If ``failure`` is neither ``None`` nor a ``str``.
			A malformed signal does not count as the first one.
		"""
		# Exact type check: a ``str`` subclass would arrive as a netref to an object in the host.
		if failure is not None and type(failure) is not str:
			raise TypeError(f"Readiness failure must be a str or None, not {type(failure).__name__}")
		with self._readinessLock:
			if self._readinessReported:
				log.debugWarning("Ignoring repeated readiness signal from ART host")
				return
			self._readinessReported = True
		if self._onReady is not None:
			self._onReady(failure)

	@Service.exposed
	def requestCapability(self, name: str) -> Service:
		"""Request a capability, returning a handle to it if the permission is granted.

		:param name: Name of the capability being requested.
		:raises PermissionNotGrantedError: Always, for now.
		"""
		log.debug(f"Capability requested before the broker exists: {name!r}")
		raise PermissionNotGrantedError(f"No capability named {name!r} has been granted")
