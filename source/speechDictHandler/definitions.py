# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os.path
from locale import strxfrm

import globalVars
from logHandler import log
from NVDAState import WritePaths

from .types import DictionaryType, SpeechDictDefinition, VoiceSpeechDictDefinition

_speechDictDefinitions: list[SpeechDictDefinition] = []
"""
A list of available speech dictionary definitions.
These definitions are used to load speech dictionaries.
The list is filled with definitions from core and add-ons using _addSpeechDictionaries.
With listAvailableSpeechDictDefinitions, there is a public interface to retrieve definitions.
"""


def listAvailableSpeechDictDefinitions(forDisplay: bool = False) -> list[SpeechDictDefinition]:
	"""Get available speech dictionary definitions.
	Note that this function returns both mandatory and optional speech dictionaries, and does not filter based on whether the dictionary is currently enabled.
	:param forDisplay: If True, the returned list is sorted for display order.
		Such a list is sorted alphabetically by display name, with built-in dictionaries listed first.
	"""
	defs = list(_speechDictDefinitions)
	if not forDisplay:
		return defs
	return sorted(
		defs,
		key=lambda dct: (dct.source not in DictionaryType, strxfrm(dct.displayName or dct.name)),
	)


def _addSpeechDictionaries():
	"""
	Adds speech dictionary definitions to the global _speechDictDefinitions list.

	This function is responsible for initializing the available speech dictionaries.
	It adds definitions for the built-in speech dictionaries, as well as any speech dictionaries in add-ons.

	The built-in dictionaries include:
	- "builtin": Built-in speech dictionary that assists in breaking up words that contain capital letters.
	- "default": Default speech dictionary in the user profile.
	- "voice": Voice-specific speech dictionary that adapts to the currently active voice.

	For each installed add-on, the function checks the add-on's manifest for any defined speech dictionaries,
	and adds those to the _speechDictDefinitions list as well.
	"""
	_speechDictDefinitions.extend(
		(
			SpeechDictDefinition(
				name=DictionaryType.TEMP.value,
				source=DictionaryType.TEMP,
				mandatory=True,
				# Translators: Title for the temporary speech dictionary (the dictionary that is active as long
				# as NvDA is running).
				displayName=_("Temporary dictionary"),
			),
			VoiceSpeechDictDefinition(),
			SpeechDictDefinition(
				name=DictionaryType.DEFAULT.value,
				source=DictionaryType.DEFAULT,
				path=WritePaths.speechDictDefaultFile,
				# Translators: Name of the default speech dictionary.
				displayName=_("Default Dictionary"),
			),
			SpeechDictDefinition(
				name=DictionaryType.BUILTIN.value,
				source=DictionaryType.BUILTIN,
				path=os.path.join(globalVars.appDir, "builtin.dic"),
				mandatory=True,
			),
		),
	)
	# Add add-on speech dictionaries
	import addonHandler

	for addon in addonHandler.getRunningAddons():
		speechDicts = addon.manifest.get("speechDictionaries")
		if not speechDicts:
			continue
		log.debug(
			f"Found {len(speechDicts)} speech dictionary entries in manifest for add-on {addon.name!r}",
		)
		directory = os.path.join(addon.path, "speechDicts")
		for name, dictConfig in speechDicts.items():
			try:
				definition = SpeechDictDefinition(
					name=name,
					path=os.path.join(directory, f"{name}.dic"),
					source=addon.name,
					displayName=dictConfig["displayName"],
					mandatory=dictConfig["mandatory"],
				)
			except Exception:
				log.exception(
					f"Error while applying custom speech dictionaries config from addon {addon.name!r}",
				)
				continue
			else:
				_speechDictDefinitions.append(definition)


def _getDictionaryDefinition(source: DictionaryType | str) -> SpeechDictDefinition:
	"""Get the speech dictionary definition for a given source.
	:param source: The source of the speech dictionary, which can be a DictionaryType or a string (e.g., add-on name).
	:return: The corresponding SpeechDictDefinition.
	:raises KeyError: If no definition is found for the given source.
	"""
	for definition in _speechDictDefinitions:
		if definition.source == source:
			return definition
	raise KeyError(f"No speech dictionary definition found for source {source!r}")
