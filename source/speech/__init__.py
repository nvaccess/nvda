# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Babbage B.V., Bill Dengler,
# Julien Cochuyt

from .speech import (
	_extendSpeechSequence_addMathForTextInfo,
	_getSpellingSpeechAddCharMode,
	_getSpellingCharAddCapNotification,
	_getSpellingSpeechWithoutCharMode,
	_getPlaceholderSpeechIfTextEmpty,
	_getSelectionMessageSpeech,
	_getSpeakMessageSpeech,
	_manager,
	_objectSpeech_calculateAllowedProps,
	_suppressSpeakTypedCharacters,
	BLANK_CHUNK_CHARS,
	cancelSpeech,
	CHUNK_SEPARATOR,
	clearTypedWordBuffer,
	FIRST_NONCONTROL_CHAR,
	getCharDescListFromText,
	getControlFieldSpeech,
	getCurrentLanguage,
	getFormatFieldSpeech,
	getIndentationSpeech,
	getObjectPropertiesSpeech,
	getObjectSpeech,
	getPreselectedTextSpeech,
	getPropertiesSpeech,
	getSpellingSpeech,
	getState,
	getTableInfoSpeech,
	getTextInfoSpeech,
	IDT_BASE_FREQUENCY,
	IDT_MAX_SPACES,
	IDT_TONE_DURATION,
	isBlank,
	LANGS_WITH_CONJUNCT_CHARS,
	pauseSpeech,
	processText,
	PROTECTED_CHAR,
	RE_CONVERT_WHITESPACE,
	RE_INDENTATION_CONVERT,
	RE_INDENTATION_SPLIT,
	setSpeechMode,
	speak,
	speakMessage,
	speakObject,
	speakObjectProperties,
	speakPreselectedText,
	speakSelectionChange,
	speakSelectionMessage,
	speakSpelling,
	speakText,
	speakTextInfo,
	SpeakTextInfoState,
	speakTextSelected,
	speakTypedCharacters,
	SpeechMode,
	spellTextInfo,
	splitTextIndentation,
)

from .priorities import Spri

from .types import (
	SpeechSequence,
	SequenceItemT,
	logBadSequenceTypes,
	GeneratorWithReturn,
	_flattenNestedSequences
)

__all__ = [
	# from .priorities
	"Spri",
	# from .types
	"SpeechSequence",
	"SequenceItemT",
	"logBadSequenceTypes",
	"GeneratorWithReturn",
	"_flattenNestedSequences",
	# from .speech
	"_getSpellingSpeechAddCharMode",
	"_getSpellingCharAddCapNotification",
	"_getSpellingSpeechWithoutCharMode",
	"_extendSpeechSequence_addMathForTextInfo",
	"_getPlaceholderSpeechIfTextEmpty",
	"_getSelectionMessageSpeech",
	"_getSpeakMessageSpeech",
	"_manager",
	"_objectSpeech_calculateAllowedProps",
	"_suppressSpeakTypedCharacters",
	"BLANK_CHUNK_CHARS",
	"cancelSpeech",
	"CHUNK_SEPARATOR",
	"clearTypedWordBuffer",
	"FIRST_NONCONTROL_CHAR",
	"getCharDescListFromText",
	"getControlFieldSpeech",
	"getCurrentLanguage",
	"getFormatFieldSpeech",
	"getIndentationSpeech",
	"getObjectPropertiesSpeech",
	"getObjectSpeech",
	"getPreselectedTextSpeech",
	"getPropertiesSpeech",
	"getSpellingSpeech",
	"getState",
	"getTableInfoSpeech",
	"getTextInfoSpeech",
	"IDT_BASE_FREQUENCY",
	"IDT_MAX_SPACES",
	"IDT_TONE_DURATION",
	"isBlank",
	"LANGS_WITH_CONJUNCT_CHARS",
	"pauseSpeech",
	"processText",
	"PROTECTED_CHAR",
	"RE_CONVERT_WHITESPACE",
	"RE_INDENTATION_CONVERT",
	"RE_INDENTATION_SPLIT",
	"setSpeechMode",
	"speak",
	"speakMessage",
	"speakObject",
	"speakObjectProperties",
	"speakPreselectedText",
	"speakSelectionChange",
	"speakSelectionMessage",
	"speakSpelling",
	"speakText",
	"speakTextInfo",
	"SpeakTextInfoState",
	"speakTextSelected",
	"speakTypedCharacters",
	"SpeechMode",
	"spellTextInfo",
	"splitTextIndentation",
]

import synthDriverHandler
import config
from .speech import initialize as speechInitialize
from .sayAll import initialize as sayAllInitialize


def initialize():
	""" Loads and sets the synth driver configured in nvda.ini.
	Initializes the state of speech and initializes the sayAllHandler
	"""
	synthDriverHandler.initialize()
	synthDriverHandler.setSynth(config.conf["speech"]["synth"])
	speechInitialize()
	sayAllInitialize(
		speak,
		speakObject,
		getTextInfoSpeech,
		SpeakTextInfoState,
	)


def terminate():
	synthDriverHandler.setSynth(None)
