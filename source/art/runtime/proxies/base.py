# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Base classes for runtime proxies."""

import os
import threading
from typing import Optional

import Pyro5.api


class ServiceProxyMixin:
	"""Mixin for accessing service proxies."""

	_thread_local = threading.local()
	_service_env_var = None
	_service_timeout = 2.0

	@classmethod
	def _get_service(cls) -> Optional[Pyro5.api.Proxy]:
		"""Get or create the service proxy."""
		if cls._service_env_var is None:
			raise NotImplementedError("_service_env_var must be set")

		# Get thread-local cache
		if not hasattr(cls._thread_local, 'service_cache'):
			cls._thread_local.service_cache = {}
		service_cache = cls._thread_local.service_cache

		service_name = cls._service_env_var

		if service_name not in service_cache:
			uri = os.environ.get(service_name)
			if uri:
				proxy = Pyro5.api.Proxy(uri)
				proxy._pyroTimeout = cls._service_timeout
				service_cache[service_name] = proxy
			else:
				service_cache[service_name] = None

		return service_cache[service_name]

	@classmethod
	def _call_service(cls, method: str, *args, **kwargs):
		"""Call a service method, returning None on failure."""
		service = cls._get_service()
		if service:
			try:
				return getattr(service, method)(*args, **kwargs)
			except Exception as e:
				from logHandler import log
				log.exception(f"Service call failed: {cls._service_env_var}.{method}")
				return None
		return None
