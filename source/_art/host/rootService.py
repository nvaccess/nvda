# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""The root service the host exposes to core over the control connection."""

from __future__ import annotations

from typing import Literal

import rpyc

from .._log import log
from ..transport import Service


@rpyc.service
class HostRootService(Service):
	"""The host's entry point, as seen from core.

	This is ART's own code, not the add-on's.
	Add-ons implement feature components; this service is the registry that hands them out.
	"""

	def __init__(self) -> None:
		super().__init__()
		self._conn: rpyc.Connection | None = None

	def on_connect(self, conn: rpyc.Connection) -> None:
		"""Record the connection so :attr:`coreRoot` can reach core.

		:param conn: The rpyc connection this service is being served over.
		"""
		super().on_connect(conn)
		self._conn = conn

	@property
	def coreRoot(self) -> rpyc.Service:
		"""Core's root service, through which capabilities are requested.

		:raises RuntimeError: If the control connection has not been established.
		"""
		if self._conn is None:
			raise RuntimeError("Host root service is not connected")
		return self._conn.root

	@Service.exposed
	def ping(self) -> Literal["pong"]:
		"""Report that the host process is serving requests.

		Answered by ART itself rather than by add-on code, so it measures the health of the host's
		transport rather than the health of whatever the add-on is doing.

		:returns: "pong"
		"""
		return "pong"

	@Service.exposed
	def loadComponent(self, name: str) -> Service:
		"""Instantiate one of the add-on's feature components and expose it to core.

		:param name: Name of the feature component to load.
		:raises NotImplementedError: Always, for now.
		"""
		log.debug(f"Component load requested before components exist: {name!r}")
		raise NotImplementedError("Component loading arrives with the manifest and component registry")
