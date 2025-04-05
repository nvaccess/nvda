import languageHandler
import config
from . import speech
from .types import SpeechSequence
from .commands import LangChangeCommand
from synthDriverHandler import getSynth


def getSpeechSequenceWithLangs(speechSequence: SpeechSequence) -> SpeechSequence:
	"""Get a speech sequence with the language description for each non default language of the read text.

	:param speechSequence: The original speech sequence.
	:return: A speech sequence containing descriptions for each non default language, indicating if the language is not supported by the current synthesizer.
	"""
	if not config.conf["speech"]["reportLanguage"]:
		return speechSequence
	filteredSpeechSequence = list()
	for index, item in enumerate(speechSequence):
		if (
			not isinstance(item, LangChangeCommand)
			or item.isDefault
			or index == len(speechSequence) - 1
			or item.lang == speech._speechState.lastReportedLanguage
		):
			filteredSpeechSequence.append(item)
			continue
		langDesc = languageHandler.getLanguageDescription(item.lang)
		if langDesc is None:
			langDesc = item.lang
		# Ensure that the language description is pronnounced in the default language.
		filteredSpeechSequence.append(LangChangeCommand(None))
		curSynth = getSynth()
		if curSynth.languageIsSupported(item.lang):
			filteredSpeechSequence.append(langDesc)
		else:
			# Translators: Reported when the language of the text being read is not supported by the current synthesizer.
			filteredSpeechSequence.append(_("{lang} not supported").format(lang=langDesc))
		speech._speechState.lastReportedLanguage = item.lang
		filteredSpeechSequence.append(item)
	return filteredSpeechSequence
