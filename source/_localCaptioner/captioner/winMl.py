from importlib import metadata
import sys
from pathlib import Path
import traceback

from winui3.microsoft.windows.applicationmodel.dynamicdependency.bootstrap import (
	InitializeOptions,
	initialize
)
import winui3.microsoft.windows.ai.machinelearning as winml

_winml_instance = None

class WinML:
	def __new__(cls, *args, **kwargs):
		global _winml_instance
		if _winml_instance is None:
			_winml_instance = super(WinML, cls).__new__(cls, *args, **kwargs)
			_winml_instance._initialized = False
		return _winml_instance

	def __init__(self):
		if self._initialized:
			return
		self._initialized = True

		self._fix_winrt_runtime()
		self._win_app_sdk_handle = initialize(options=InitializeOptions.ON_NO_MATCH_SHOW_UI)
		self._win_app_sdk_handle.__enter__()
		catalog = winml.ExecutionProviderCatalog.get_default()
		self._providers = catalog.find_all_providers()
		self._ep_paths : dict[str, str] = {}
		for provider in self._providers:
			provider.ensure_ready_async().get()
			if provider.library_path == '':
				continue
			self._ep_paths[provider.name] = provider.library_path
		self._registered_eps : list[str] = []

	def __del__(self):
		self._providers = None
		self._win_app_sdk_handle.__exit__(None, None, None)

	def _fix_winrt_runtime(self):
		"""
		This function removes the msvcp140.dll from the winrt-runtime package.
		So it does not cause issues with other libraries.
		"""
		site_packages_path = Path(str(metadata.distribution('winrt-runtime').locate_file('')))
		dll_path = site_packages_path / 'winrt' / 'msvcp140.dll'
		if dll_path.exists():
			dll_path.unlink()

	def register_execution_providers_to_ort(self) -> list[str]:
		import onnxruntime as ort
		for name, path in self._ep_paths.items():
			if name not in self._registered_eps:
				try:
					ort.register_execution_provider_library(name, path)
					self._registered_eps.append(name)
				except Exception as e:
					print(f"Failed to register execution provider {name}: {e}", file=sys.stderr)
					traceback.print_exc()
		return self._registered_eps
