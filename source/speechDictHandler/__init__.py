# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import typing
import globalVars
from logHandler import log
from utils._deprecate import MovedSymbol, RemovedSymbol, handleDeprecations

from . import definitions
from .types import (
	DictionaryType,
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
	RemovedSymbol(
		"dictionaries",
		lambda: {
			d.source: d.dictionary for d in definitions._speechDictDefinitions if d.source in DictionaryType
		},
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
	for definition in definitions._speechDictDefinitions:
		if not definition.enabled:
			continue
		text = definition.sub(text)
	return text


def initialize() -> None:
	definitions._addSpeechDictionaries()


def terminate() -> None:
	definitions._speechDictDefinitions.clear()


def loadVoiceDict(synth: "synthDriverHandler.SynthDriver") -> None:
	"""Loads appropriate dictionary for the given synthesizer.
	It handles case when the synthesizer doesn't support voice setting.
	"""
	definition = next(
		(d for d in definitions._speechDictDefinitions if isinstance(d, VoiceSpeechDictDefinition)),
		None,
	)
	if definition is None:
		log.error(
			"No VoiceSpeechDictDefinition found in _speechDictDefinitions. "
			"Speech dictionaries may not have been initialized.",
		)
		raise RuntimeError("No voice speech dictionary definition is available to load.")
	definition.load(synth)
