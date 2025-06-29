# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Dynamic proxy generator for ART synthesizers."""

import sys
from typing import Dict, Type, Any, Tuple

from logHandler import log
from synthDrivers._artProxy import ARTProxySynthDriver

# Import setting classes for the security allowlist
try:
	from autoSettingsUtils.driverSetting import DriverSetting, NumericDriverSetting, BooleanDriverSetting
except ImportError:
	# Fallback if module structure is different
	log.warning("Could not import from autoSettingsUtils.driverSetting, trying synthDriverHandler")
	try:
		from synthDriverHandler import DriverSetting, NumericDriverSetting, BooleanDriverSetting
	except ImportError:
		log.error("Could not import DriverSetting classes - dynamic settings will not work")
		DriverSetting = None
		NumericDriverSetting = None
		BooleanDriverSetting = None


class ARTSynthProxyGenerator:
	"""Generates proxy synthesizer classes for ART synthesizers."""

	_generatedProxies: Dict[str, Type[ARTProxySynthDriver]] = {}
	
	# Security allowlist for Phase 1 - only allow known, safe setting types
	_ALLOWED_SETTING_TYPES = {
		"DriverSetting": DriverSetting,
		"NumericDriverSetting": NumericDriverSetting,
		"BooleanDriverSetting": BooleanDriverSetting,
		# Phase 2 will add "DynamicVoiceSetting" here
	}

	@classmethod
	def _create_settings(cls, settings_metadata: Dict[str, Any]) -> Tuple[Any, ...]:
		"""Create DriverSetting instances from serialized metadata.
		
		@param settings_metadata: Dictionary containing supportedSettings metadata
		@return: Tuple of DriverSetting instances for use as supportedSettings
		"""
		if not settings_metadata or "supportedSettings" not in settings_metadata:
			log.warning("No supportedSettings metadata provided, using empty tuple")
			return tuple()
		
		settings_objects = []
		
		for setting_spec in settings_metadata["supportedSettings"]:
			setting_type_name = setting_spec.get("type")
			setting_name = setting_spec.get("name")
			setting_params = {
				k: v for k, v in setting_spec.items()
				if k not in ("type", "name")
			}
			
			if not setting_type_name or not setting_name:
				log.warning(f"Invalid setting spec - missing type or name: {setting_spec}")
				continue
			
			# Security check - only allow known setting types
			if setting_type_name not in cls._ALLOWED_SETTING_TYPES:
				log.warning(f"Unknown/disallowed setting type '{setting_type_name}' for setting '{setting_name}' - skipping")
				continue
			
			setting_class = cls._ALLOWED_SETTING_TYPES[setting_type_name]
			if setting_class is None:
				log.warning(f"Setting class {setting_type_name} not available - skipping setting '{setting_name}'")
				continue
			
			try:
				# Extract required positional arguments based on setting type
				if setting_type_name in ["DriverSetting", "NumericDriverSetting", "BooleanDriverSetting"]:
					# These require displayNameWithAccelerator as second positional argument
					displayNameWithAccelerator = setting_params.pop('displayNameWithAccelerator', setting_name)
					setting_instance = setting_class(setting_name, displayNameWithAccelerator, **setting_params)
				else:
					# For other setting types, use original approach
					setting_instance = setting_class(setting_name, **setting_params)
				
				settings_objects.append(setting_instance)
				log.debug(f"Created setting instance: {setting_name} ({setting_type_name})")
			except Exception as e:
				log.error(f"Failed to create setting '{setting_name}' of type '{setting_type_name}': {e}")
				# Continue with other settings rather than failing entirely
				continue
		
		return tuple(settings_objects)
	
	@classmethod
	def generateProxy(
		cls, addon_name: str, synth_name: str, synth_description: str, 
		settings_metadata: Dict[str, Any] = None
	) -> Type[ARTProxySynthDriver]:
		"""Generate a proxy synthesizer class for an ART synth.

		@param addon_name: The addon providing the synth
		@param synth_name: The synthesizer module name
		@param synth_description: Human-readable description
		@param settings_metadata: Settings metadata for dynamic supportedSettings
		@return: A proxy synthesizer class
		"""
		proxy_key = f"{addon_name}.{synth_name}"

		if proxy_key in cls._generatedProxies:
			return cls._generatedProxies[proxy_key]

		# Create a new proxy class dynamically
		class_name = f"ARTProxy_{synth_name}"
		
		# Generate supportedSettings from metadata
		supported_settings = cls._create_settings(settings_metadata or {})
		log.debug(f"Generated {len(supported_settings)} settings for {synth_name}: {[s.id if hasattr(s, 'id') else str(s) for s in supported_settings]}")

		proxy_class = type(
			class_name,
			(ARTProxySynthDriver,),
			{
				"name": synth_name,
				"description": f"{synth_description} (via ART)",
				"_artAddonName": addon_name,
				"_artSynthName": synth_name,
				"supportedSettings": supported_settings,
			},
		)

		cls._generatedProxies[proxy_key] = proxy_class

		# Register in synthDrivers module so it can be found
		module_name = f"synthDrivers.{synth_name}"
		module = type(sys)("synthDrivers." + synth_name)
		module.SynthDriver = proxy_class
		sys.modules[module_name] = module

		log.info(f"Generated proxy synthesizer: {synth_name} from addon {addon_name}")

		return proxy_class

	@classmethod
	def unregisterProxy(cls, addon_name: str, synth_name: str):
		"""Remove a generated proxy when addon is unloaded."""
		proxy_key = f"{addon_name}.{synth_name}"

		if proxy_key in cls._generatedProxies:
			del cls._generatedProxies[proxy_key]

		module_name = f"synthDrivers.{synth_name}"
		if module_name in sys.modules:
			del sys.modules[module_name]
