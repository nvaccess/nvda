# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import typing
from locale import strxfrm

import globalVars
from logHandler import log
from NVDAState import WritePaths
from utils._deprecate import MovedSymbol, RemovedSymbol, handleDeprecations

from .types import (
	DictionaryType,
	SpeechDictDefinition,
	VoiceSpeechDictDefinition,
)

if typing.TYPE_CHECKING:
	import synthDriverHandler

__getattr__ = handleDeprecations(
	MovedSymbol("speechDictsPath", "NVDAState", "WritePaths", "speechDictsDir"),
	MovedSymbol("ENTRY_TYPE_ANYWHERE", "speechDictHandler.types", "EntryType", "ANYWHERE"),
	MovedSymbol("ENTRY_TYPE_WORD", "speechDictHandler.types", "EntryType", "WORD"),
	MovedSymbol("ENTRY_TYPE_REGEXP", "speechDictHandler.types", "EntryType", "REGEXP"),
	MovedSymbol("SpeechDict", "speechDictHandler.types"),
	MovedSymbol("SpeechDictEntry", "speechDictHandler.types"),
	MovedSymbol("SpeechDict", "speechDictHandler.types"),
	RemovedSymbol(
		"dictionaries",
		lambda: {d.source: d.dictionary for d in _speechDictDefinitions if d.source in DictionaryType},
		callValue=True,
	),
	RemovedSymbol("dictTypes", tuple(t.value for t in DictionaryType)),
)


def processText(text: str) -> str:
	"""Processes the given text through all speech dictionaries.
	:param text: The text to process.
	:returns: The processed text.
	"""
	if not globalVars.speechDictionaryProcessing:
		return text
	for definition in reversed(_speechDictDefinitions):
		if not definition.enabled:
			continue
		text = definition.sub(text)
	return text


def initialize() -> None:
	_addSpeechDictionaries()


def terminate() -> None:
	_speechDictDefinitions.clear()


def loadVoiceDict(synth: "synthDriverHandler.SynthDriver") -> None:
	"""Loads appropriate dictionary for the given synthesizer.
	It handles case when the synthesizer doesn't support voice setting.
	"""
	definition = next(d for d in _speechDictDefinitions if isinstance(d, VoiceSpeechDictDefinition))
	definition.load(synth)


_speechDictDefinitions: list[SpeechDictDefinition] = []
"""
A list of available speech dictionary definitions.
These definitions are used to load speech dictionaries.
The list is filled with definitions from core and add-ons using _addSpeechDictionaries.
With listAvailableSpeechDictDefinitions, there is a public interface to retrieve definitions.
"""


def listAvailableSpeechDictDefinitions(alphabetized: bool = False) -> list[SpeechDictDefinition]:
	"""Get available speech dictionary definitions.
	:param alphabetized: If True, the returned list is sorted alphabetically by display name.
	"""
	defs = list(_speechDictDefinitions)
	if not alphabetized:
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
				name=DictionaryType.BUILTIN.value,
				source=DictionaryType.BUILTIN,
				path=os.path.join(globalVars.appDir, "builtin.dic"),
				mandatory=True,
			),
			SpeechDictDefinition(
				name=DictionaryType.DEFAULT.value,
				source=DictionaryType.DEFAULT,
				path=WritePaths.speechDictDefaultFile,
				# Translators: Name of the default speech dictionary.
				displayName=_("Default Dictionary"),
			),
			VoiceSpeechDictDefinition(),
		),
	)
	# Add add-on symbols
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
	_speechDictDefinitions.append(
		SpeechDictDefinition(
			name=DictionaryType.TEMP.value,
			source=DictionaryType.TEMP,
			mandatory=True,
		),
	)
