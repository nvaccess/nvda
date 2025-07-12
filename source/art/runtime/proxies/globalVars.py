# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""GlobalVars module proxy for add-ons running in ART."""

import os
import sys
from pathlib import Path
from .base import ServiceProxyMixin


class AppArgsProxy(ServiceProxyMixin):
	"""Proxy for globalVars.appArgs."""
	
	_service_env_var = "NVDA_ART_GLOBALVARS_SERVICE_URI"
	
	def __init__(self):
		self._cached_args = None
	
	def _get_args(self):
		"""Get appArgs, using cache if available."""
		if self._cached_args is None:
			self._cached_args = self._call_service("getAppArgs") or {}
		return self._cached_args
	
	@property
	def secure(self) -> bool:
		return self._get_args().get('secure', False)
	
	@property
	def configPath(self) -> str:
		return self._get_args().get('configPath', "")
	
	@property
	def launcher(self) -> bool:
		return self._get_args().get('launcher', False)
	
	@property
	def debugLogging(self) -> bool:
		return self._get_args().get('debugLogging', False)


# Create the appArgs proxy object
appArgs = AppArgsProxy()

if getattr(sys, "frozen", None) is None:
	appDir = str(Path(__file__).parent.parent.parent.parent.resolve())
else:
	appDir = sys.prefix

# For compatibility - ART doesn't use these but some code might expect them
appPid = os.getpid()
