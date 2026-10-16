# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2026 NV Access Limited, Neil Soiffer, Ryan McCleary, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import re

from speech import getCurrentLanguage
from speech.commands import (
	BaseProsodyCommand,
	BeepCommand,
	BreakCommand,
	CharacterModeCommand,
	LangChangeCommand,
	PhonemeCommand,
	PitchCommand,
	RateCommand,
	SpeechCommand,
	SynthCommand,
	VolumeCommand,
)
from speechXml import toXmlLang
from synthDriverHandler import SynthDriver, getSynth

from .localization import getLanguageToUse

PROSODY_COMMANDS: dict[str, type[BaseProsodyCommand]] = {
	"pitch": PitchCommand,
	"volume": VolumeCommand,
	"rate": RateCommand,
}

RE_MATHML_SPEECH: re.Pattern = re.compile(
	# Break.
	r"<break time='(?P<break>\d+)ms'/> ?"
	# Pronunciation of characters.
	r"|<say-as interpret-as='characters'>(?P<char>[^<]+)</say-as> ?"
	# Specific pronunciation.
	r"|<phoneme alphabet='ipa' ph='(?P<ipa>[^']+)'>(?P<phonemeText>[^ <]+)</phoneme> ?"
	# Prosody.
	r"|(?P<prosody><prosody(?: pitch='(?P<pitch>\d+)%')?(?: volume='(?P<volume>\d+)%')?"
	r"(?: rate='(?P<rate>\d+)%')?>) ?"
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
	Nested prosody restores the enclosing settings when a tag closes.

	:param text: The SSML text to convert.
	:returns: A list of strings and SpeechCommand objects.
	"""
	# MathCAT's default rate is 180 wpm.
	# Assume that 0% is 80 wpm and 100% is 450 wpm and scale accordingly.

	language: str = getLanguageToUse()
	nvdaLanguage: str = toXmlLang(getCurrentLanguage())
	synth: SynthDriver = getSynth()
	# I tried the engines on a 180 word excerpt. The speeds do not change linearly and differ a it between engines
	# At "50" espeak finished in 46 sec, sapi in 75 sec, and one core in 70; at '100' one core was much slower than the others
	wpm: int = 2 * getSynth()._get_rate()
	breakMulti: float = 180.0 / wpm
	supportedCommands: set[type[SynthCommand]] = synth.supportedCommands
	useBreak: bool = BreakCommand in supportedCommands
	usePhoneme: bool = PhonemeCommand in supportedCommands
	useCharacter: bool = CharacterModeCommand in supportedCommands
	out: list[str | SpeechCommand] = []
	if language != nvdaLanguage:
		out.append(LangChangeCommand(language))

	currentProsody: dict[type[BaseProsodyCommand], float] = {}
	prosodyStack: list[dict[type[BaseProsodyCommand], float]] = []
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
		elif m.lastgroup == "prosody":
			previousProsody: dict[type[BaseProsodyCommand], float] = {}
			for attribute, command in PROSODY_COMMANDS.items():
				value: str | None = m.group(attribute)
				if value is not None and command in supportedCommands:
					previousProsody[command] = currentProsody.get(command, 1)
					# Retain the existing MathCAT pitch conversion in this rate-restoration fix.
					multiplier: float = int(value) if command is PitchCommand else int(value) / 100.0
					out.append(command(multiplier=multiplier))
					currentProsody[command] = multiplier
			# Every tag needs a frame, even if its attributes are unsupported.
			prosodyStack.append(previousProsody)
		elif m.lastgroup == "prosodyReset":
			if prosodyStack:
				# A capital's pitch reset must not reset the enclosing math rate.
				for command, multiplier in reversed(prosodyStack.pop().items()):
					out.append(command(multiplier=multiplier))
					currentProsody[command] = multiplier
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

	if language.casefold() != nvdaLanguage.casefold():
		out.append(LangChangeCommand(None))
	return out
