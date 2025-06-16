# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Base classes for core services."""

import Pyro5.api
from logHandler import log


@Pyro5.api.expose
class BaseService:
	"""Base class for core services exposed to ART."""

	def __init__(self, service_name: str):
		self.service_name = service_name
		log.info(f"{service_name} initialized")

	def _log_error(self, operation: str, details: str = ""):
		"""Log an error with consistent formatting."""
		msg = f"Error in {self.service_name}.{operation}"
		if details:
			msg += f": {details}"
		log.exception(msg)
