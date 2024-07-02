# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited, World Light Information Limited,
# Hong Kong Blind Union, Babbage B.V., Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


from characterDescriptions import CharacterDescriptions, getCharacterDescription
from symbols import (
	SymbolLevel,
	SPEECH_SYMBOL_LEVEL_LABELS,
	CONFIGURABLE_SPEECH_SYMBOL_LEVELS,
	SPEECH_SYMBOL_LEVELS,
	SYMPRES_ALWAYS,
	SYMPRES_NOREP,
	SYMPRES_NEVER,
	SPEECH_SYMBOL_PRESERVE_LABELS,
	SPEECH_SYMBOL_PRESERVES,
	SpeechSymbol,
	SpeechSymbols,
	SpeechSymbolProcessor,
	processSpeechSymbols,
	processSpeechSymbol,
	clearSpeechSymbols,
	handlePostConfigProfileSwitch,
)

# Override (and limit) the symbols exported by the characterProcessing package
# These are the symbols available when `from characterProcessing import *` is used.
__all__ = [
	CharacterDescriptions,
	getCharacterDescription,
	SymbolLevel,
	SPEECH_SYMBOL_LEVEL_LABELS,
	CONFIGURABLE_SPEECH_SYMBOL_LEVELS,
	SPEECH_SYMBOL_LEVELS,
	SYMPRES_ALWAYS,
	SYMPRES_NOREP,
	SYMPRES_NEVER,
	SPEECH_SYMBOL_PRESERVE_LABELS,
	SPEECH_SYMBOL_PRESERVES,
	SpeechSymbol,
	SpeechSymbols,
	SpeechSymbolProcessor,
	processSpeechSymbols,
	processSpeechSymbol,
	clearSpeechSymbols,
	handlePostConfigProfileSwitch,
]
