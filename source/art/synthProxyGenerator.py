# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Dynamic proxy generator for ART synthesizers."""

import sys
from typing import Dict, Type

from logHandler import log
from synthDrivers._artProxy import ARTProxySynthDriver


class ARTSynthProxyGenerator:
	"""Generates proxy synthesizer classes for ART synthesizers."""

	_generatedProxies: Dict[str, Type[ARTProxySynthDriver]] = {}

	@classmethod
	def generateProxy(
		cls, addon_name: str, synth_name: str, synth_description: str
	) -> Type[ARTProxySynthDriver]:
		"""Generate a proxy synthesizer class for an ART synth.

		@param addon_name: The addon providing the synth
		@param synth_name: The synthesizer module name
		@param synth_description: Human-readable description
		@return: A proxy synthesizer class
		"""
		proxy_key = f"{addon_name}.{synth_name}"

		if proxy_key in cls._generatedProxies:
			return cls._generatedProxies[proxy_key]

		# Create a new proxy class dynamically
		class_name = f"ARTProxy_{synth_name}"

		proxy_class = type(
			class_name,
			(ARTProxySynthDriver,),
			{
				"name": synth_name,
				"description": f"{synth_description} (via ART)",
				"_artAddonName": addon_name,
				"_artSynthName": synth_name,
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
