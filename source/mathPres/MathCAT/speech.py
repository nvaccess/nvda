import re
from speech.commands import (
	BaseProsodyCommand,
	BeepCommand,
	BreakCommand,
	CharacterModeCommand,
	LangChangeCommand,
	PhonemeCommand,
	PitchCommand,
	SpeechCommand,
	SynthCommand,
)
from logHandler import log
from synthDriverHandler import getSynth, SynthDriver
import libmathcat_py as libmathcat
from collections.abc import Type
from .MathCAT import PROSODY_COMMANDS
from localization import getLanguageToUse
from languageHandler import getCurrentLanguage

RE_MATHML_SPEECH: re.Pattern = re.compile(
	# Break.
	r"<break time='(?P<break>\d+)ms'/> ?"
	# Pronunciation of characters.
	r"|<say-as interpret-as='characters'>(?P<char>[^<]+)</say-as> ?"
	# Specific pronunciation.
	r"|<phoneme alphabet='ipa' ph='(?P<ipa>[^']+)'>(?P<phonemeText>[^ <]+)</phoneme> ?"
	# Prosody.
	r"|<prosody(?: pitch='(?P<pitch>\d+)%')?(?: volume='(?P<volume>\d+)%')?(?: rate='(?P<rate>\d+)%')?> ?"
	r"|(?P<prosodyReset></prosody>) ?"
	r"|<audio src='(?P<beep>beep.mp4)'>.*?</audio> ?"  # hack for beeps
	# Other tags, which we don't care about.
	r"|<[^>]+> ?"
	# Actual content.
	r"|(?P<content>[^<]+)",
)

def convertSSMLTextForNVDA(text: str) -> list[str | SpeechCommand]:
	"""
	Change the SSML in the text into NVDA's command structure.
	The environment is examined to determine whether a language switch is needed.

	:param text: The SSML text to convert.
	:returns: A list of strings and SpeechCommand objects.
	"""
	# MathCAT's default rate is 180 wpm.
	# Assume that 0% is 80 wpm and 100% is 450 wpm and scale accordingly.

	# find MathCAT's language setting and store it away (could be "Auto")
	# if MathCAT's setting doesn't match NVDA's language setting, change the language that is used
	mathCATLanguageSetting: str = "en"  # set in case GetPreference fails
	try:
		mathCATLanguageSetting = libmathcat.GetPreference("Language")
	except Exception as e:
		log.exception(e)
	language: str = getLanguageToUse()
	nvdaLanguage: str = getCurrentLanguage().replace("_", "-")

	synth: SynthDriver = getSynth()
	# I tried the engines on a 180 word excerpt. The speeds do not change linearly and differ a it between engines
	# At "50" espeak finished in 46 sec, sapi in 75 sec, and one core in 70; at '100' one core was much slower than the others
	wpm: int = 2 * getSynth()._get_rate()
	breakMulti: float = 180.0 / wpm
	supportedCommands: set[Type["SynthCommand"]] = synth.supportedCommands
	useBreak: bool = BreakCommand in supportedCommands
	usePitch: bool = PitchCommand in supportedCommands
	usePhoneme: bool = PhonemeCommand in supportedCommands
	# as of 7/23, oneCore voices do not implement the CharacterModeCommand despite it being in supported_commands
	useCharacter: bool = CharacterModeCommand in supportedCommands and synth.name != "oneCore"
	out: list[str | SpeechCommand] = []
	if mathCATLanguageSetting != language:
		try:
			libmathcat.SetPreference("Language", language)
		except Exception as e:
			log.exception(e)
			language = mathCATLanguageSetting  # didn't set the language
	if language != nvdaLanguage:
		out.append(LangChangeCommand(language))

	resetProsody: list[Type["BaseProsodyCommand"]] = []
	for m in RE_MATHML_SPEECH.finditer(text):
		if m.lastgroup == "break":
			if useBreak:
				out.append(BreakCommand(time=int(int(m.group("break")) * breakMulti)))
		elif m.lastgroup == "char":
			ch: str = m.group("char")
			if useCharacter:
				out.extend((CharacterModeCommand(True), ch, CharacterModeCommand(False)))
			else:
				out.extend((" ", "eigh" if ch == "a" and language.startswith("en") else ch, " "))
		elif m.lastgroup == "beep":
			out.append(BeepCommand(2000, 50))
		elif m.lastgroup == "pitch":
			if usePitch:
				out.append(PitchCommand(multiplier=int(m.group(m.lastgroup))))
				resetProsody.append(PitchCommand)
		elif m.lastgroup in PROSODY_COMMANDS:
			command: Type["BaseProsodyCommand"] = PROSODY_COMMANDS[m.lastgroup]
			if command in supportedCommands:
				out.append(command(multiplier=int(m.group(m.lastgroup)) / 100.0))
				resetProsody.append(command)
		elif m.lastgroup == "prosodyReset":
			# for command in resetProsody:    # only supported commands were added, so no need to check
			command: Type["BaseProsodyCommand"] = resetProsody.pop()
			out.append(command(multiplier=1))
		elif m.lastgroup == "phonemeText":
			if usePhoneme:
				out.append(PhonemeCommand(m.group("ipa"), text=m.group("phonemeText")))
			else:
				out.append(m.group("phonemeText"))
		elif m.lastgroup == "content":
			# MathCAT puts out spaces between words, the speak command seems to want to glom the strings together at times,
			#  so we need to add individual " "s to the output
			out.extend((" ", m.group(0), " "))
	# there is a bug in MS Word that concats the math and the next character outside of math, so we add a space
	out.append(" ")

	if mathCATLanguageSetting != language:
		# restore the old value (probably "Auto")
		try:
			libmathcat.SetPreference("Language", mathCATLanguageSetting)
		except Exception:
			log.exception()
	if language != nvdaLanguage:
		out.append(LangChangeCommand(None))
	return out
