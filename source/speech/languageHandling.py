# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Noelia Ruiz Martínez
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import languageHandler
import synthDriverHandler
import config
from config.configFlags import ReportNotSupportedLanguage
from . import speech
from .types import SpeechSequence
from .commands import LangChangeCommand, BeepCommand


def getSpeechSequenceWithLangs(speechSequence: SpeechSequence) -> SpeechSequence:
	"""Get a speech sequence with the language description for each non default language of the read text.

	:param speechSequence: The original speech sequence.
	:return: A speech sequence containing descriptions for each non default language, indicating if the language is not supported by the current synthesizer.
	"""
	if not shouldMakeLangChangeCommand():
		return speechSequence
	curSynth = synthDriverHandler.getSynth()
	filteredSpeechSequence = list()
	for index, item in enumerate(speechSequence):
		if (
			not isinstance(item, LangChangeCommand)
			or item.isDefault
			or getLangToReport(item.lang) == speech._speechState.lastReportedLanguage
			or index == len(speechSequence) - 1
		):
			filteredSpeechSequence.append(item)
			continue
		langDesc = languageHandler.getLanguageDescription(getLangToReport(item.lang))
		if langDesc is None:
			langDesc = getLangToReport(item.lang)
		# Ensure that the language description is pronnounced in the default language.
		filteredSpeechSequence.append(LangChangeCommand(None))
		if shouldReportNotSupported() and not curSynth.languageIsSupported(getLangToReport(item.lang)):
			if config.conf["speech"]["reportNotSupportedLanguage"] == ReportNotSupportedLanguage.SPEECH.value:
				filteredSpeechSequence.append(
					# Translators: Reported when the language of the text being read is not supported by the current synthesizer.
					pgettext("languageNotSupported", "{lang} (not supported)").format(lang=langDesc),
				)
			else:  # Beep
				filteredSpeechSequence.append(langDesc)
				filteredSpeechSequence.append(BeepCommand(500, 50))
		elif config.conf["speech"]["reportLanguage"]:
			filteredSpeechSequence.append(langDesc)
		speech._speechState.lastReportedLanguage = getLangToReport(item.lang)
		filteredSpeechSequence.append(item)
	return filteredSpeechSequence


def shouldSwitchVoice() -> bool:
	"""Determines if the current synthesizer should switch to the voice corresponding to the language of the text been read."""
	return config.conf["speech"]["autoLanguageSwitching"]


def shouldMakeLangChangeCommand() -> bool:
	"""Determines if NVDA should get the language of the text been read."""
	return config.conf["speech"]["autoLanguageSwitching"] or config.conf["speech"]["reportLanguage"]


def shouldReportNotSupported() -> bool:
	"""Determines if NVDA should report if the language is not supported by the synthesizer."""
	return (
		config.conf["speech"]["autoLanguageSwitching"]
		and config.conf["speech"]["reportNotSupportedLanguage"] != ReportNotSupportedLanguage.OFF.value
	)


def getLangToReport(lang: str) -> str:
	"""Gets the language to report by NVDA, according to speech settings.

	:param lang: A language code corresponding to the text been read.
	:return: A language code corresponding to the language to be reported.
	"""
	# Ensure the language is in a standard form of xx[_YY],
	# E.g. en_AU rather than en-au.
	lang = languageHandler.normalizeLanguage(lang)
	if config.conf["speech"]["autoLanguageSwitching"] and not config.conf["speech"]["autoDialectSwitching"]:
		return lang.split("_")[0]
	return lang
