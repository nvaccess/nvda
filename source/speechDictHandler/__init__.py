# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import typing

import globalVars
from logHandler import log
from NVDAState import WritePaths
from utils._deprecate import MovedSymbol, handleDeprecations

from . import dictFormatUpgrade
from .types import DictionaryType
from .types import SpeechDict as _SpeechDict

if typing.TYPE_CHECKING:
	import synthDriverHandler

__getattr__ = handleDeprecations(
	MovedSymbol("speechDictsPath", "NVDAState", "WritePaths", "speechDictsDir"),
	MovedSymbol("ENTRY_TYPE_ANYWHERE", "speechDictHandler.types", "EntryType", "ANYWHERE"),
	MovedSymbol("ENTRY_TYPE_WORD", "speechDictHandler.types", "EntryType", "WORD"),
	MovedSymbol("ENTRY_TYPE_REGEXP", "speechDictHandler.types", "EntryType", "REGEXP"),
	MovedSymbol("SpeechDict", "speechDictHandler.types"),
	MovedSymbol("SpeechDictEntry", "speechDictHandler.types"),
)

dictionaries: dict[DictionaryType | str, _SpeechDict] = {}
dictTypes = (
	DictionaryType.TEMP.value,
	DictionaryType.VOICE.value,
	DictionaryType.DEFAULT.value,
	DictionaryType.BUILTIN.value,
)
"""Types ordered by their priority E.G. voice specific speech dictionary is processed before the default."""


def processText(text: str) -> str:
	"""Processes the given text through all speech dictionaries."""
	if not globalVars.speechDictionaryProcessing:
		return text
	for type in dictTypes:
		text = dictionaries[type].sub(text)
	return text


def initialize() -> None:
	for type in dictTypes:
		dictionaries[type] = _SpeechDict()
	dictionaries[DictionaryType.DEFAULT].load(WritePaths.speechDictDefaultFile)
	dictionaries[DictionaryType.BUILTIN].load(os.path.join(globalVars.appDir, "builtin.dic"))


def loadVoiceDict(synth: "synthDriverHandler.SynthDriver") -> None:
	"""Loads appropriate dictionary for the given synthesizer.
	It handles case when the synthesizer doesn't support voice setting.
	"""
	try:
		dictFormatUpgrade.doAnyUpgrades(synth)
	except:  # noqa: E722
		log.error("error trying to upgrade dictionaries", exc_info=True)
		pass
	if synth.isSupported("voice"):
		voice = synth.availableVoices[synth.voice].displayName
		baseName = dictFormatUpgrade.createVoiceDictFileName(synth.name, voice)
	else:
		baseName = f"{synth.name}.dic"
	fileName = os.path.join(WritePaths.voiceDictsDir, synth.name, baseName)
	dictionaries[DictionaryType.VOICE].load(fileName)
