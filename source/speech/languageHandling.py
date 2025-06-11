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
			or item.lang == speech._speechState.lastReportedLanguage
			or index == len(speechSequence) - 1
		):
			filteredSpeechSequence.append(item)
			continue
		langDesc = languageHandler.getLanguageDescription(item.lang)
		if langDesc is None:
			langDesc = item.lang
		# Ensure that the language description is pronnounced in the default language.
		filteredSpeechSequence.append(LangChangeCommand(None))
		match curSynth.languageIsSupported(item.lang):
			case True if config.conf["speech"]["reportLanguage"]:
				# If reportLanguage is False, we still change speech._speechState.lastReportedLanguage to report not supported language if it appears multiple times.
				filteredSpeechSequence.append(langDesc)
			case False if shouldReportNotSupported():
				if (
					config.conf["speech"]["reportNotSupportedLanguage"]
					== ReportNotSupportedLanguage.SPEECH.value
				):
					filteredSpeechSequence.append(
						# Translators: Reported when the language of the text being read is not supported by the current synthesizer.
						pgettext("languageNotSupported", "{lang} (not supported)").format(lang=langDesc),
					)
				elif (
					config.conf["speech"]["reportNotSupportedLanguage"]
					== ReportNotSupportedLanguage.BEEP.value
				):
					filteredSpeechSequence.append(langDesc)
					filteredSpeechSequence.append(BeepCommand(500, 50))
			case False if (not shouldReportNotSupported() and config.conf["speech"]["reportLanguage"]):
				# We need this to use the formatted string when appropriate, to avoid appending (not supported).
				filteredSpeechSequence.append(langDesc)
		speech._speechState.lastReportedLanguage = item.lang
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
