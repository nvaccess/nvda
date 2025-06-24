# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.


import importlib
from importlib.machinery import SourceFileLoader
import logging
import os
import sys
from pathlib import Path
from typing import List

import Pyro5.api


@Pyro5.api.expose
class AddOnLifecycleService:
	"""Service for managing add-on lifecycle in the ART process."""

	def __init__(self, addon_spec=None):
		self.loadedAddon = None
		self.addon_name = addon_spec["name"] if addon_spec else None
		self.addon_path = addon_spec["path"] if addon_spec else None
		self.logger = logging.getLogger(f"ART.AddOnLifecycleService.{self.addon_name or 'unknown'}")

	def loadAddon(self, addonPath: str) -> bool:
		addonPathObj = Path(addonPath)
		self.logger.debug(f"Loading add-on from path: {addonPathObj}")
		
		if not addonPathObj.exists():
			self.logger.error(f"Add-on path does not exist: {addonPathObj}")
			return False

		manifestFile = addonPathObj / "manifest.ini"
		if not manifestFile.exists():
			self.logger.error(f"Add-on manifest.ini not found: {manifestFile}")
			raise RuntimeError(f"No manifest.ini found at {manifestFile}")

		sys.path.insert(0, str(addonPathObj))
		
		try:
			self._loadPlugins(addonPathObj)
			
			self.loadedAddon = {
				"name": self.addon_name or addonPathObj.name,
				"path": str(addonPathObj)
			}
			
			self.logger.debug(f"Add-on loaded successfully: {self.addon_name}")
			return True
			
		except Exception:
			self.logger.exception(f"Error loading add-on from {addonPath}")
			return False

	def _setupPackagePaths(self, addon_path):
		"""Set up package paths for addon plugin directories, matching main NVDA behavior."""
		plugin_types = [
			"globalPlugins",
			"appModules", 
			"synthDrivers",
			"brailleDisplayDrivers",
			"visionEnhancementProviders",
		]
		
		for plugin_type in plugin_types:
			plugin_dir = addon_path / plugin_type
			if not plugin_dir.exists():
				continue
				
			try:
				package_module = importlib.import_module(plugin_type)
				
				addon_plugin_path = str(plugin_dir)
				if hasattr(package_module, '__path__'):
					if not isinstance(package_module.__path__, list):
						package_module.__path__ = list(package_module.__path__) if package_module.__path__ else []
					
					if addon_plugin_path not in package_module.__path__:
						package_module.__path__.insert(0, addon_plugin_path)
						self.logger.debug(f"Added {addon_plugin_path} to {plugin_type}.__path__")
				else:
					self.logger.warning(f"Package {plugin_type} has no __path__ attribute")
					
			except ImportError:
				self.logger.exception(f"Failed to import package {plugin_type}")

	def _loadPlugins(self, addon_path):
		self._setupPackagePaths(addon_path)
		
		plugin_types = [
			("globalPlugins", "GlobalPlugin"),
			("appModules", "AppModule"),
			("synthDrivers", "SynthDriver"),
			("brailleDisplayDrivers", "BrailleDisplayDriver"),
			("visionEnhancementProviders", "VisionEnhancementProvider"),
		]
		
		for plugin_dir_name, expected_class in plugin_types:
			plugin_dir = addon_path / plugin_dir_name
			if not plugin_dir.exists():
				self.logger.debug(f"No {plugin_dir_name} directory found for {self.addon_name}")
				continue
				
			self.logger.info(f"Found {plugin_dir_name} directory for {self.addon_name}")
			
			for py_file in plugin_dir.glob("*.py"):
				if py_file.name.startswith("__"):
					continue
					
				module_name = py_file.stem
				full_module_name = f"{plugin_dir_name}.{module_name}"
				self.logger.debug(f"Loading {plugin_dir_name} module: {module_name}")
				
				try:
					self.logger.info(f"=== Attempting to import {plugin_dir_name} module: {module_name} ===")
					try:
						if module_name.isidentifier():
							self.logger.debug(f"Using importlib.import_module for {full_module_name}")
							module = importlib.import_module(full_module_name)
						else:
							sanitised = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in module_name)
							sanitised_full = f"{plugin_dir_name}.{sanitised}"
							self.logger.debug(f"Using SourceFileLoader for {sanitised_full}")
							loader = SourceFileLoader(sanitised_full, str(py_file))
							module = importlib.util.module_from_spec(importlib.machinery.ModuleSpec(sanitised_full, loader))
							loader.exec_module(module)
							sys.modules[sanitised_full] = module
							sys.modules[full_module_name] = module
						
						if plugin_dir_name == "synthDrivers":
							sys.modules[f"synthDrivers.{module_name}"] = module
							self.logger.info(f"Successfully imported synthDriver module: {module_name}")
							
							# Check if module has SynthDriver class
							if hasattr(module, 'SynthDriver'):
								self.logger.info(f"Found SynthDriver class in {module_name}")
								synth_class = getattr(module, 'SynthDriver')
								self.logger.debug(f"SynthDriver class: {synth_class}")
								
								# Instantiate the synthesizer to trigger registration (like NVDA does)
								self.logger.debug(f"Instantiating SynthDriver from {module_name}")
								self.logger.debug(f"SynthDriver class type: {type(synth_class)}")
								self.logger.debug(f"SynthDriver class MRO: {synth_class.__mro__}")
								self.logger.debug(f"SynthDriver class bases: {synth_class.__bases__}")
								self.logger.debug(f"SynthDriver class module: {synth_class.__module__}")
								try:
									synth_instance = synth_class()
									self.logger.info(f"Successfully instantiated SynthDriver: {module_name}")
									
									# Register the synthesizer with NVDA Core to generate proxy
									self._registerSynthWithCore(synth_instance, module_name)
								except Exception:
									self.logger.exception(f"Failed to instantiate SynthDriver: {module_name}")
							else:
								self.logger.warning(f"No SynthDriver class found in {module_name}")
					
					except Exception:
						self.logger.exception(f"Error importing {plugin_dir_name} module: {module_name}")
						continue
					
					if plugin_dir_name == "globalPlugins" and hasattr(module, expected_class):
						plugin_class = getattr(module, expected_class)
						self.logger.debug(f"Instantiating {expected_class} from {module_name}")
						plugin_instance = plugin_class()
						
				except Exception:
					self.logger.exception(f"Failed to load {plugin_dir_name} module: {module_name}")

	def _registerSynthWithCore(self, synth_instance, module_name):
		"""Register a synthesizer instance with NVDA Core to generate proxy."""
		try:
			self.logger.info(f"Registering synthesizer {module_name} with NVDA Core")
			
			# Get speech service URI from environment
			speech_uri = os.environ.get("NVDA_ART_SPEECH_SERVICE_URI")
			if not speech_uri:
				self.logger.error("No NVDA_ART_SPEECH_SERVICE_URI found in environment")
				return False
			
			# Connect to NVDA Core's speech service
			import Pyro5.api
			speech_service = Pyro5.api.Proxy(speech_uri)
			speech_service._pyroTimeout = 5.0
			
			# Get addon name from environment
			addon_name = os.environ.get("NVDA_ART_ADDON_NAME", self.addon_name or "unknown")
			
			# Extract metadata from synthesizer instance
			synth_name = getattr(synth_instance, 'name', module_name)
			synth_description = getattr(synth_instance, 'description', f"{module_name} Synthesizer")
			
			# Get supported commands and notifications
			supported_commands = []
			if hasattr(synth_instance, 'supportedCommands'):
				supported_commands = [cmd.__name__ for cmd in synth_instance.supportedCommands]
			
			supported_notifications = []
			if hasattr(synth_instance, 'supportedNotifications'):
				supported_notifications = list(synth_instance.supportedNotifications)
			
			# Get supported settings metadata
			settings_metadata = {}
			synth_class = synth_instance.__class__
			if hasattr(synth_class, 'getSupportedSettingsMetadata'):
				try:
					settings_metadata = synth_class.getSupportedSettingsMetadata()
					self.logger.debug(f"Got settings metadata for {synth_name}: {settings_metadata}")
				except Exception:
					self.logger.exception(f"Failed to get settings metadata for {synth_name}")
			else:
				# Provide default settings for regular NVDA synthesizers
				settings_metadata = {
					"supportedSettings": [
						{
							"name": "rate",
							"type": "NumericDriverSetting",
							"params": {
								"displayNameWithAccelerator": "&Rate",
								"minVal": 0,
								"maxVal": 100,
								"defaultVal": 50
							}
						},
						{
							"name": "pitch",
							"type": "NumericDriverSetting", 
							"params": {
								"displayNameWithAccelerator": "&Pitch",
								"minVal": 0,
								"maxVal": 100,
								"defaultVal": 50
							}
						},
						{
							"name": "volume",
							"type": "NumericDriverSetting",
							"params": {
								"displayNameWithAccelerator": "&Volume",
								"minVal": 0,
								"maxVal": 100,
								"defaultVal": 100
							}
						}
					]
				}
				self.logger.debug(f"Using default settings metadata for {synth_name}")
			
			# Register with NVDA Core
			self.logger.debug(f"Calling registerSynthDriver for {synth_name}")
			result = speech_service.registerSynthDriver(
				name=synth_name,
				description=synth_description,
				addon_name=addon_name,
				supportedCommands=supported_commands,
				supportedNotifications=supported_notifications,
				supportedSettings=settings_metadata
			)
			
			if result:
				self.logger.info(f"Successfully registered {synth_name} with NVDA Core")
				return True
			else:
				self.logger.error(f"Failed to register {synth_name} - registerSynthDriver returned False")
				return False
				
		except Exception:
			self.logger.exception(f"Error registering synthesizer {module_name} with NVDA Core")
			return False

	def getLoadedAddons(self) -> List[str]:
		return [self.loadedAddon["name"]] if self.loadedAddon else []
	
	def loadAddonIfNeeded(self) -> bool:
		self.logger.info(f"=== loadAddonIfNeeded() called for addon: {self.addon_name} ===")
		
		if self.loadedAddon:
			self.logger.debug(f"Add-on {self.addon_name} already loaded")
			return True
		
		if not self.addon_path:
			self.logger.error("No addon path specified")
			return False
		
		self.logger.info(f"About to load addon {self.addon_name} from path: {self.addon_path}")
		try:
			result = self.loadAddon(self.addon_path)
			if result:
				self.logger.info(f"Successfully loaded addon {self.addon_name}")
			else:
				self.logger.error(f"Failed to load addon {self.addon_name}")
			return result
		except Exception:
			self.logger.exception(f"Exception while loading addon {self.addon_name}")
			return False
