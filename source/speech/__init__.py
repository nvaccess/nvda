# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Babbage B.V., Bill Dengler,
# Julien Cochuyt, Leonard de Ruijter

import languageHandler
from .commands import LangChangeCommand
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
	speakSsml,
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
from .extensions import speechCanceled, post_speechPaused, pre_speechQueued, filter_speechSequence
from .priorities import Spri

from .types import (
	SpeechSequence,
	SequenceItemT,
	logBadSequenceTypes,
	GeneratorWithReturn,
	_flattenNestedSequences,
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
	"speakSsml",
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
	"speechCanceled",
	"post_speechPaused",
	"pre_speechQueued",
]

import synthDriverHandler
import config
from .speech import initialize as speechInitialize
from .sayAll import initialize as sayAllInitialize


class SpeechSequenceState:
	lastReportedLang = None


def initialize():
	"""Loads and sets the synth driver configured in nvda.ini.
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
	filter_speechSequence.register(getSpeechSequenceWithLangs)


def terminate():
	synthDriverHandler.setSynth(None)
	filter_speechSequence.unregister(getSpeechSequenceWithLangs)


def getSpeechSequenceWithLangs(speechSequence: SpeechSequence):
	"""Get a speech sequence with the language description for each non default language of the read text.

	:param speechSequence: The original speech sequence.
	:return: A speech sequence containing descriptions for each non default language, indicating if the language is not supported by the current synthesizer.
	"""
	filteredSpeechSequence = list()
	for index, item in enumerate(speechSequence):
		if (
			not isinstance(item, LangChangeCommand)
			or item.isDefault
			or index == len(speechSequence) - 1
			or item.lang == SpeechSequenceState.lastReportedLang
		):
			filteredSpeechSequence.append(item)
			continue
		langDesc = languageHandler.getLanguageDescription(item.lang)
		if langDesc is None:
			langDesc = item.lang
		filteredSpeechSequence.append(LangChangeCommand(None))
		filteredSpeechSequence.append(langDesc)
		SpeechSequenceState.lastReportedLang = item.lang
		if not languageIsSupported(item.lang):
			filteredSpeechSequence.append("not supported")
		filteredSpeechSequence.append(item)
	return filteredSpeechSequence


def languageIsSupported(language: str | None) -> bool:
	"""Determines if the specified language is supported.
	:param language: A language code or None.
	:return: True if the language is supported, False otherwise.
	"""
	if language is None:
		return True
	for lang in synthDriverHandler.getSynth().availableLanguages:
		if language == lang or language == languageHandler.normalizeLanguage(lang).split("_")[0]:
			return True
	return False
