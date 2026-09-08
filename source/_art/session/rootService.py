# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""The root service core exposes to the host over the control connection."""

from __future__ import annotations

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

	@Service.exposed
	def ping(self) -> Literal["pong"]:
		"""Report that core is serving requests.

		:returns: "pong"
		"""
		return "pong"

	@Service.exposed
	def requestCapability(self, name: str) -> Service:
		"""Request a capability, returning a handle to it if the permission is granted.

		:param name: Name of the capability being requested.
		:raises PermissionNotGrantedError: Always, for now.
		"""
		log.debug(f"Capability requested before the broker exists: {name!r}")
		raise PermissionNotGrantedError(f"No capability named {name!r} has been granted")
