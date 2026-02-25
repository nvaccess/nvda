# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import globalVars
from .types import DictionaryType
from utils._deprecate import MovedSymbol, RemovedSymbol, handleDeprecations

from . import definitions
from .definitions import loadVoiceDict, listAvailableSpeechDictDefinitions

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


__all__ = [
	"processText",
	"initialize",
	"terminate",
	"loadVoiceDict",
	"listAvailableSpeechDictDefinitions",
]
