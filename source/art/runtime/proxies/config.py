# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Config module proxy for add-ons running in ART."""

from typing import Any
from .base import ServiceProxyMixin


class ConfigProxy(ServiceProxyMixin):
	"""Proxy for config.conf that forwards to ConfigService."""
	
	_service_env_var = "NVDA_ART_CONFIG_SERVICE_URI"
	
	def __getitem__(self, section: str):
		"""Get a configuration section."""
		if self._get_service():
			return ConfigSectionProxy(section)
		return {}
	
	def __contains__(self, section: str) -> bool:
		"""Check if a section exists."""
		section_data = self._call_service("getConfigSection", section)
		return bool(section_data) if section_data is not None else False
	
	def save(self):
		"""Save the configuration."""
		self._call_service("saveConfig")


class ConfigSectionProxy(ServiceProxyMixin):
	"""Proxy for a configuration section."""
	
	_service_env_var = "NVDA_ART_CONFIG_SERVICE_URI"
	
	def __init__(self, section: str):
		self._section = section
	
	def __getitem__(self, key: str) -> Any:
		"""Get a configuration value."""
		return self._call_service("getConfigValue", self._section, key)
	
	def __setitem__(self, key: str, value: Any):
		"""Set a configuration value."""
		self._call_service("setConfigValue", self._section, key, value)
	
	def get(self, key: str, default=None) -> Any:
		"""Get a configuration value with default."""
		result = self._call_service("getConfigValue", self._section, key, default)
		return result if result is not None else default
	
	def __contains__(self, key: str) -> bool:
		"""Check if a key exists."""
		section_data = self._call_service("getConfigSection", self._section)
		return key in section_data if section_data else False


# Create the main config object
conf = ConfigProxy()

isAppX = False
