# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
# Modified from: https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/get-started?tabs=python

from importlib import metadata
import os
from pathlib import Path

from winui3.microsoft.windows.applicationmodel.dynamicdependency.bootstrap import (
	InitializeOptions,
	initialize
)
import winui3.microsoft.windows.ai.machinelearning as winml

from logHandler import log

_WINML_INSTANCE = None


class _WinML:
	def __new__(cls, *args, **kwargs):
		global _WINML_INSTANCE
		if _WINML_INSTANCE is None:
			_WINML_INSTANCE = super(_WinML, cls).__new__(cls, *args, **kwargs)
			_WINML_INSTANCE._initialized = False
		return _WINML_INSTANCE

	def __init__(self):
		if self._initialized:
			return
		self._initialized = True

		self._fixWinRTRuntime()
		self._winAppSDKHandle = initialize(options=InitializeOptions.ON_NO_MATCH_SHOW_UI)
		self._winAppSDKHandle.__enter__()
		catalog = winml.ExecutionProviderCatalog.get_default()
		self._providers = catalog.find_all_providers()
		self._epPaths: dict[str, str] = {}
		for provider in self._providers:
			provider.ensure_ready_async().get()
			if provider.library_path == "":
				continue
			self._epPaths[provider.name] = provider.library_path
		self._registeredEps: list[str] = []

	def __del__(self):
		self._providers = None
		self._winAppSDKHandle.__exit__(None, None, None)

	def _fixWinRTRuntime(self):
		"""
		This function removes the msvcp140.dll from the winrt-runtime package.
		So it does not cause issues with other libraries.
		"""
		site_packages_path = str(metadata.distribution("winrt-runtime").locate_file(""))
		dllPath = Path(os.path.join(site_packages_path, "winrt", "msvcp140.dll"))
		if dllPath.exists():
			dllPath.unlink()

	def registerExecutionProvidersToOrt(self) -> list[str]:
		import onnxruntime as ort
		for name, path in self._epPaths.items():
			if name not in self._registeredEps:
				try:
					ort.register_execution_provider_library(name, path)
					self._registeredEps.append(name)
				except Exception as e:
					log.exception(f"Failed to register execution provider {name}: {e}")
		return self._registeredEps
