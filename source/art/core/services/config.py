# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Configuration service for ART - provides config access to add-ons."""

import Pyro5.api
import config
from logHandler import log
from .base import BaseService


@Pyro5.api.expose
class ConfigService(BaseService):
	"""Provides access to NVDA configuration for add-ons running in ART."""
	
	def __init__(self):
		super().__init__("ConfigService")
	
	def getConfigValue(self, section: str, key: str, default=None):
		"""Get a configuration value."""
		try:
			if section in config.conf:
				return config.conf[section].get(key, default)
			return default
		except Exception:
			self._log_error("getConfigValue", f"{section}.{key}")
			return default
	
	def setConfigValue(self, section: str, key: str, value):
		"""Set a configuration value."""
		try:
			if section not in config.conf:
				config.conf[section] = {}
			config.conf[section][key] = value
		except Exception:
			self._log_error("setConfigValue", f"{section}.{key}")
			raise
	
	def getConfigSection(self, section: str) -> dict:
		"""Get an entire configuration section."""
		try:
			if section in config.conf:
				return dict(config.conf[section])
			return {}
		except Exception:
			self._log_error("getConfigSection", section)
			return {}
	
	def saveConfig(self):
		"""Save the configuration to disk."""
		try:
			config.conf.save()
			log.debug("Configuration saved")
		except Exception:
			self._log_error("saveConfig")
			raise
