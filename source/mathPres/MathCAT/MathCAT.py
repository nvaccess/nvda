# -*- coding: UTF-8 -*-

"""MathCAT add-on: generates speech, braille, and allows exploration of expressions written in MathML.
The goal of this add-on is to replicate/improve upon the functionality of MathPlayer which has been discontinued."""
# Author: Neil Soiffer
# Copyright: this file is copyright GPL2
#   The code additionally makes use of the MathCAT library (written in Rust) which is covered by the MIT license
#   and also (obviously) requires external speech engines and braille drivers.
#   The plugin also requires the use of a small python dll: python3.dll
#   python3.dll has "Copyright © 2001-2022 Python Software Foundation; All Rights Reserved"

# Note: this code is a lot of cut/paste from other code and very likely could be substantially improved/cleaned.
import braille  # we generate braille
import mathPres  # math plugin stuff
import re  # regexp patter match
import speech  # speech commands
import config  # look up caps setting
import ui  # copy message
import winUser  # clipboard manipulation
import gettext
import addonHandler
import winKernel
import gui

from . import libmathcat_py as libmathcat
from typing import Type
from collections.abc import Generator, Callable
from keyboardHandler import KeyboardInputGesture  # navigation key strokes
from logHandler import log  # logging
from os import path  # set rule dir path
from scriptHandler import script  # copy MathML via ctrl-c
from synthDriverHandler import (
	getSynth,
	SynthDriver,
)
from ctypes import windll  # register clipboard formats
from speech import getCurrentLanguage
from speech.types import SpeechSequence

# speech/SSML processing borrowed from NVDA's mathPres/mathPlayer.py
from speech.commands import (
	BeepCommand,
	PitchCommand,
	VolumeCommand,
	RateCommand,
	LangChangeCommand,
	BreakCommand,
	CharacterModeCommand,
	PhonemeCommand,
	IndexCommand,
	ProsodyCommand,
	SpeechCommand,
	SynthCommand,
)

from textUtils import WCHAR_ENCODING
from ctypes import c_wchar, WinError, Array
from api import getClipData
from synthDrivers import _espeak

_ = gettext.gettext

addonHandler.initTranslation()

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

PROSODY_COMMANDS: dict[str, ProsodyCommand] = {
	"pitch": PitchCommand,
	"volume": VolumeCommand,
	"rate": RateCommand,
}
RE_MATH_LANG: re.Pattern = re.compile(r"""<math .*(xml:)?lang=["']([^'"]+)["'].*>""")

# try to get around espeak bug where voice slows down (for other voices, just a waste of time)
# we use a global that gets set at a time when the rate is probably good (SetMathML)
_synthesizerRate: int | None = None


def getLanguageToUse(mathMl: str = "") -> str:
	"""Get the language specified in a math tag if the language pref is Auto, else the language preference.

	:param mathMl: The MathML string to examine for language. Defaults to an empty string.
	:returns: The language string to use.
	"""
	mathCATLanguageSetting: str = "Auto"
	try:
		# ignore regional differences if the MathCAT language setting doesn't have it.
		mathCATLanguageSetting = libmathcat.GetPreference("Language")
	except Exception as e:
		log.exception(e)

	# log.info(f"getLanguageToUse: {mathCATLanguageSetting}")
	if mathCATLanguageSetting != "Auto":
		return mathCATLanguageSetting

	languageMatch: re.Match | None = RE_MATH_LANG.search(mathMl)
	language: str = (
		languageMatch.group(2) if languageMatch else getCurrentLanguage()
	)  # seems to be current voice's language
	language = language.lower().replace("_", "-")
	if language == "cmn":
		language = "zh-cmn"
	elif language == "yue":
		language = "zh-yue"
	return language


def convertSSMLTextForNVDA(text: str) -> list[str | SpeechCommand]:
	"""
	Change the SSML in the text into NVDA's command structure.
	The environment is examined to determine whether a language switch is needed.

	:param text: The SSML text to convert.
	:returns: A list of strings and SpeechCommand objects.
	"""
	# MathCAT's default rate is 180 wpm.
	# Assume that 0% is 80 wpm and 100% is 450 wpm and scale accordingly.
	# log.info(f"\nSpeech str: '{text}'")

	# find MathCAT's language setting and store it away (could be "Auto")
	# if MathCAT's setting doesn't match NVDA's language setting, change the language that is used
	mathCATLanguageSetting: str = "en"  # set in case GetPreference fails
	try:
		mathCATLanguageSetting = libmathcat.GetPreference("Language")
	except Exception as e:
		log.exception(e)
	language: str = getLanguageToUse()
	nvdaLanguage: str = getCurrentLanguage().replace("_", "-")
	# log.info(f"mathCATLanguageSetting={mathCATLanguageSetting}, lang={language}, NVDA={nvdaLanguage}")

	_monkeyPatchESpeak()

	synth: SynthDriver = getSynth()
	# I tried the engines on a 180 word excerpt. The speeds do not change linearly and differ a it between engines
	# At "50" espeak finished in 46 sec, sapi in 75 sec, and one core in 70; at '100' one core was much slower than the others
	wpm: int = 2 * getSynth()._get_rate()
	breakMulti: float = 180.0 / wpm
	supportedCommands: set[Type["SynthCommand"]] = synth.supportedCommands
	useBreak: bool = BreakCommand in supportedCommands
	usePitch: bool = PitchCommand in supportedCommands
	# use_rate = RateCommand in supported_commands
	# use_volume = VolumeCommand in supported_commands
	usePhoneme: bool = PhonemeCommand in supportedCommands
	# as of 7/23, oneCore voices do not implement the CharacterModeCommand despite it being in supported_commands
	useCharacter: bool = CharacterModeCommand in supportedCommands and synth.name != "oneCore"
	out: list[str | SpeechCommand] = []
	if mathCATLanguageSetting != language:
		# log.info(f"Setting language to {language}")
		try:
			libmathcat.SetPreference("Language", language)
		except Exception as e:
			log.exception(e)
			language = mathCATLanguageSetting  # didn't set the language
	if language != nvdaLanguage:
		out.append(LangChangeCommand(language))

	resetProsody: list[Type["ProsodyCommand"]] = []
	# log.info(f"\ntext: {text}")
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
			command: Type["ProsodyCommand"] = PROSODY_COMMANDS[m.lastgroup]
			if command in supportedCommands:
				out.append(command(multiplier=int(m.group(m.lastgroup)) / 100.0))
				resetProsody.append(command)
		elif m.lastgroup == "prosodyReset":
			# for command in resetProsody:    # only supported commands were added, so no need to check
			command: Type["ProsodyCommand"] = resetProsody.pop()
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
		except Exception as e:
			log.exception(e)
	if language != nvdaLanguage:
		out.append(LangChangeCommand(None))
	# log.info(f"Speech commands: '{out}'")
	return out


class MathCATInteraction(mathPres.MathInteractionNVDAObject):
	"""An NVDA object used to interact with MathML."""

	# Put MathML or other formats on the clipboard.
	# MathML is put on the clipboard using the two formats below (defined by MathML spec)
	# We use both formats because some apps may only use one or the other
	# Note: filed https://github.com/nvaccess/nvda/issues/13240 to make this usable outside of MathCAT
	CF_MathML: int = windll.user32.RegisterClipboardFormatW("MathML")
	CF_MathML_Presentation: int = windll.user32.RegisterClipboardFormatW(
		"MathML Presentation",
	)
	# log.info("2**** MathCAT registering data formats:
	#   CF_MathML %x, CF_MathML_Presentation %x" % (CF_MathML, CF_MathML_Presentation))

	def __init__(
		self,
		provider: mathPres.MathPresentationProvider | None = None,
		mathMl: str | None = None,
	):
		"""Initialize the MathCATInteraction object.

		:param provider: Optional presentation provider.
		:param mathMl: Optional initial MathML string.
		"""
		super(MathCATInteraction, self).__init__(provider=provider, mathMl=mathMl)
		if mathMl is None:
			self.initMathML = "<math></math>"
		else:
			self.initMathML = mathMl

	def reportFocus(self) -> None:
		"""Calls MathCAT's ZoomIn command and speaks the resulting text."""
		super(MathCATInteraction, self).reportFocus()
		# try to get around espeak bug where voice slows down
		if _synthesizerRate and getSynth().name == "espeak":
			getSynth()._set_rate(_synthesizerRate)
		try:
			text: str = libmathcat.DoNavigateCommand("ZoomIn")
			speech.speak(convertSSMLTextForNVDA(text))
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Error in starting navigation of math: see NVDA error log for details"))
		finally:
			# try to get around espeak bug where voice slows down
			if _synthesizerRate and getSynth().name == "espeak":
				# log.info(f'reportFocus: reset to {_synthesizer_rate}')
				getSynth()._set_rate(_synthesizerRate)

	def getBrailleRegions(
		self,
		review: bool = False,
	) -> Generator[braille.Region, None, None]:
		"""Yields braille.Region objects for this MathCATInteraction object."""
		# log.info("***MathCAT start getBrailleRegions")
		yield braille.NVDAObjectRegion(self, appendText=" ")
		region: braille.Region = braille.Region()
		region.focusToHardLeft = True
		# libmathcat.SetBrailleWidth(braille.handler.displaySize)
		try:
			region.rawText = libmathcat.GetBraille("")
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Error in brailling math: see NVDA error log for details"))
			region.rawText = ""

		# log.info("***MathCAT end getBrailleRegions ***")
		yield region

	def getScript(
		self,
		gesture: KeyboardInputGesture,
	) -> Callable[KeyboardInputGesture, None] | None:
		"""
		Returns the script function bound to the given gesture.

		:param gesture: A KeyboardInputGesture sent to this object.
		:returns: The script bound to that gesture.
		"""
		if (
			isinstance(gesture, KeyboardInputGesture)
			and "NVDA" not in gesture.modifierNames
			and gesture.mainKeyName
			in {
				"leftArrow",
				"rightArrow",
				"upArrow",
				"downArrow",
				"home",
				"end",
				"space",
				"backspace",
				"enter",
				"0",
				"1",
				"2",
				"3",
				"4",
				"5",
				"6",
				"7",
				"8",
				"9",
			}
			# or len(gesture.mainKeyName) == 1
		):
			return self.script_navigate
		else:
			return super().getScript(gesture)

	def script_navigate(self, gesture: KeyboardInputGesture) -> None:
		"""Performs the specified navigation command.

		:param gesture: They keyboard command which specified the navigation command to perform.
		"""
		try:
			# try to get around espeak bug where voice slows down
			if _synthesizerRate and getSynth().name == "espeak":
				getSynth()._set_rate(_synthesizerRate)
			if gesture is not None:  # == None when initial focus -- handled in reportFocus()
				modNames: list[str] = gesture.modifierNames
				text = libmathcat.DoNavigateKeyPress(
					gesture.vkCode,
					"shift" in modNames,
					"control" in modNames,
					"alt" in modNames,
					False,
				)
				# log.info(f"Navigate speech for {gesture.vkCode}/(s={'shift' in modNames}, c={'control' in modNames}): '{text}'")
				speech.speak(convertSSMLTextForNVDA(text))
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Error in navigating math: see NVDA error log for details"))
		finally:
			# try to get around espeak bug where voice slows down
			if _synthesizerRate and getSynth().name == "espeak":
				# log.info(f'script_navigate: reset to {_synthesizer_rate}')
				getSynth()._set_rate(_synthesizerRate)

		if not braille.handler.enabled:
			return

		try:
			# update the braille to reflect the nav position (might be excess code, but it works)
			navNode: tuple[str, int] = libmathcat.GetNavigationMathMLId()
			brailleChars = libmathcat.GetBraille(navNode[0])
			# log.info(f'braille display = {config.conf["braille"]["display"]}, braille_chars: {braille_chars}')
			region: braille.Region = braille.Region()
			region.rawText = brailleChars
			region.focusToHardLeft = True
			region.update()
			braille.handler.buffer.regions.append(region)
			braille.handler.buffer.focus(region)
			braille.handler.buffer.update()
			braille.handler.update()
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Error in brailling math: see NVDA error log for details"))

	_startsWithMath: re.Pattern = re.compile("\\s*?<math")

	@script(
		# Translators: Message to be announced during Keyboard Help
		description=_("Copy navigation focus to clipboard"),
		# Translators: Name of the section in "Input gestures" dialog.
		category=_("Clipboard"),
		gesture="kb:control+c",
	)
	def script_rawdataToClip(self, gesture: KeyboardInputGesture) -> None:
		"""Copies the raw data to the clipboard, either as MathML, ASCII math, or LaTeX, depending on user preferences.

		:param gesture: The gesture which activated this script.
		"""
		try:
			copyAs: str = "mathml"  # value used even if "CopyAs" pref is invalid
			textToCopy: str = ""
			try:
				copyAs = libmathcat.GetPreference("CopyAs").lower()
			except Exception as e:
				log.exception(f"Not able to get 'CopyAs' preference: {e}")
			if copyAs == "asciimath" or copyAs == "latex":
				# save the old braille code, set the new one, get the braille, then reset the code
				savedBrailleCode: str = libmathcat.GetPreference("BrailleCode")
				libmathcat.SetPreference("BrailleCode", "LaTeX" if copyAs == "latex" else "ASCIIMath")
				textToCopy = libmathcat.GetNavigationBraille()
				libmathcat.SetPreference("BrailleCode", savedBrailleCode)
				if copyAs == "asciimath":
					copyAs = "ASCIIMath"  # speaks better in at least some voices
			else:
				mathml: str = libmathcat.GetNavigationMathML()[0]
				if not re.match(self._startsWithMath, mathml):
					mathml = "<math>\n" + mathml + "</math>"  # copy will fix up name spacing
				elif self.initMathML != "":
					mathml = self.initMathML
				if copyAs == "speech":
					# save the old MathML, set the navigation MathML as MathMl, get the speech, then reset the MathML
					savedMathML: str = self.initMathML
					savedTTS: str = libmathcat.GetPreference("TTS")
					if savedMathML == "":  # shouldn't happen
						raise Exception("Internal error -- MathML not set for copy")
					libmathcat.SetPreference("TTS", "None")
					libmathcat.SetMathML(mathml)
					# get the speech text and collapse the whitespace
					textToCopy = " ".join(libmathcat.GetSpokenText().split())
					libmathcat.SetPreference("TTS", savedTTS)
					libmathcat.SetMathML(savedMathML)
				else:
					textToCopy = self._wrapMathMLForClipBoard(mathml)

			self._copyToClipAsMathML(textToCopy, copyAs == "mathml")
			# Translators: copy to clipboard
			ui.message(_("copy as ") + copyAs)
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("unable to copy math: see NVDA error log for details"))

	# not a perfect match sequence, but should capture normal MathML
	# not a perfect match sequence, but should capture normal MathML
	_mathTagHasNameSpace: re.Pattern = re.compile("<math .*?xmlns.+?>")
	_hasAddedId: re.Pattern = re.compile(" id='[^'].+' data-id-added='true'")
	_hasDataAttr: re.Pattern = re.compile(" data-[^=]+='[^']*'")

	def _wrapMathMLForClipBoard(self, text: str) -> str:
		"""Cleanup the MathML a little."""
		text = re.sub(self._hasAddedId, "", text)
		mathMLWithNS: str = re.sub(self._hasDataAttr, "", text)
		if not re.match(self._mathTagHasNameSpace, mathMLWithNS):
			mathMLWithNS = mathMLWithNS.replace(
				"math",
				"math xmlns='http://www.w3.org/1998/Math/MathML'",
				1,
			)
		return mathMLWithNS

	def _copyToClipAsMathML(
		self,
		text: str,
		isMathML: bool,
		notify: bool | None = False,
	) -> bool:
		"""Copies the given text to the windows clipboard.

		:param text: the text which will be copied to the clipboard.
		:param notify: whether to emit a confirmation message.
		:returns: True if it succeeds, False otherwise.
		"""
		# copied from api.py and modified to use CF_MathML_Presentation
		if not isinstance(text, str) or len(text) == 0:
			return False

		try:
			with winUser.openClipboard(gui.mainFrame.Handle):
				winUser.emptyClipboard()
				if isMathML:
					self._setClipboardData(self.CF_MathML, '<?xml version="1.0"?>' + text)
					self._setClipboardData(self.CF_MathML_Presentation, '<?xml version="1.0"?>' + text)
				self._setClipboardData(winUser.CF_UNICODETEXT, text)
			got: str = getClipData()
		except OSError:
			if notify:
				ui.reportTextCopiedToClipboard()  # No argument reports a failure.
			return False
		if got == text:
			if notify:
				ui.reportTextCopiedToClipboard(text)
			return True
		if notify:
			ui.reportTextCopiedToClipboard()  # No argument reports a failure.
		return False

	def _setClipboardData(self, format: int, data: str) -> None:
		"""Sets the clipboard data to the given data with the specified format.

		:param format: The format for the clipboard data.
			This is an integer format code returned by windll.user32.RegisterClipboardFormatW.
		:param data: The data to set on the clipboard.
		"""
		# Need to support MathML Presentation, so this copied from winUser.py and the first two lines are commented out
		# For now only unicode is a supported format
		# if format!=CF_UNICODETEXT:
		#     raise ValueError("Unsupported format")
		text: str = data
		bufLen: int = len(text.encode(WCHAR_ENCODING, errors="surrogatepass")) + 2
		# Allocate global memory
		h: winKernel.HGLOBAL = winKernel.HGLOBAL.alloc(winKernel.GMEM_MOVEABLE, bufLen)
		# Acquire a lock to the global memory receiving a local memory address
		with h.lock() as addr:
			# Write the text into the allocated memory
			buf: Array[c_wchar] = (c_wchar * bufLen).from_address(addr)
			buf.value = text
		# Set the clipboard data with the global memory
		if not windll.user32.SetClipboardData(format, h):
			raise WinError()
		# NULL the global memory handle so that it is not freed at the end of scope as the clipboard now has it.
		h.forget()


class MathCAT(mathPres.MathPresentationProvider):
	def __init__(self):
		"""Initializes MathCAT, loading the rules specified in the rules directory."""
		# super(MathCAT, self).__init__(*args, **kwargs)

		try:
			# IMPORTANT -- SetRulesDir must be the first call to libmathcat besides GetVersion()
			rulesDir: str = path.join(path.dirname(path.abspath(__file__)), "Rules")
			log.info(f"MathCAT {libmathcat.GetVersion()} installed. Using rules dir: {rulesDir}")
			libmathcat.SetRulesDir(rulesDir)
			libmathcat.SetPreference("TTS", "SSML")
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("MathCAT initialization failed: see NVDA error log for details"))

	def getSpeechForMathMl(
		self,
		mathml: str,
	) -> list[str | SpeechCommand]:
		"""Outputs a MathML string as speech.

		:param mathml: A MathML string.
		:returns: A list of speech commands and strings representing the given MathML.
		"""
		global _synthesizerRate
		synth: SynthDriver = getSynth()
		synthConfig = config.conf["speech"][synth.name]
		if synth.name == "espeak":
			_synthesizerRate: int = synthConfig["rate"]
			# log.info(f'_synthesizer_rate={_synthesizer_rate}, get_rate()={getSynth()._get_rate()}')
			getSynth()._set_rate(_synthesizerRate)
		# log.info(f'..............get_rate()={getSynth()._get_rate()}, name={synth.name}')
		try:
			# need to set Language before the MathML for DecimalSeparator canonicalization
			language: str = getLanguageToUse(mathml)
			# MathCAT should probably be extended to accept "extlang" tagging, but it uses lang-region tagging at the moment
			libmathcat.SetPreference("Language", language)
			libmathcat.SetMathML(mathml)
		except Exception as e:
			log.exception(e)
			log.exception(f"MathML is {mathml}")
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Illegal MathML found: see NVDA error log for details"))
			libmathcat.SetMathML("<math></math>")  # set it to something
		try:
			supportedCommands: set[Type["SynthCommand"]] = synth.supportedCommands
			# Set preferences for capital letters
			libmathcat.SetPreference(
				"CapitalLetters_Beep",
				"true" if synthConfig["beepForCapitals"] else "false",
			)
			libmathcat.SetPreference(
				"CapitalLetters_UseWord",
				"true" if synthConfig["sayCapForCapitals"] else "false",
			)
			# log.info(f"Speech text: {libmathcat.GetSpokenText()}")
			if PitchCommand in supportedCommands:
				libmathcat.SetPreference("CapitalLetters_Pitch", str(synthConfig["capPitchChange"]))
			if self._addSounds():
				return (
					[BeepCommand(800, 25)]
					+ convertSSMLTextForNVDA(libmathcat.GetSpokenText())
					+ [BeepCommand(600, 15)]
				)
			else:
				return convertSSMLTextForNVDA(libmathcat.GetSpokenText())

		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Error in speaking math: see NVDA error log for details"))
			return [""]
		finally:
			# try to get around espeak bug where voice slows down
			if _synthesizerRate and getSynth().name == "espeak":
				# log.info(f'getSpeechForMathMl: reset to {_synthesizer_rate}')
				getSynth()._set_rate(_synthesizerRate)

	def _addSounds(self) -> bool:
		"""Queries the user preferences to determine whether or not sounds should be added.

		:returns: True if MathCAT's `SpeechSound` preference is set, and False otherwise.
		"""
		try:
			return libmathcat.GetPreference("SpeechSound") != "None"
		except Exception as e:
			log.exception(f"MathCAT: An exception occurred in _add_sounds: {e}")
			return False

	def getBrailleForMathMl(self, mathml: str) -> str:
		"""Gets the braille representation of a given MathML string by calling MathCAT's GetBraille function.

		:param mathml: A MathML string.
		:returns: A braille string representing the input MathML.
		"""
		# log.info("***MathCAT getBrailleForMathMl")
		try:
			libmathcat.SetMathML(mathml)
		except Exception as e:
			log.exception(e)
			log.exception(f"MathML is {mathml}")
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Illegal MathML found: see NVDA error log for details"))
			libmathcat.SetMathML("<math></math>")  # set it to something
		try:
			return libmathcat.GetBraille("")
		except Exception as e:
			log.exception(e)
			# Translators: this message directs users to look in the log file
			speech.speakMessage(_("Error in brailling math: see NVDA error log for details"))
			return ""

	def interactWithMathMl(self, mathml: str) -> None:
		"""Interact with a MathML string, creating a MathCATInteraction object.

		:param mathml: The MathML representing the math to interact with.
		"""
		MathCATInteraction(provider=self, mathMl=mathml).setFocus()
		MathCATInteraction(provider=self, mathMl=mathml).script_navigate(None)


CACHED_SYNTH: SynthDriver | None = None


def _monkeyPatchESpeak() -> None:
	"""Patches an eSpeak bug where the voice slows down."""
	global CACHED_SYNTH
	currentSynth: SynthDriver = getSynth()
	if currentSynth.name != "espeak" or CACHED_SYNTH == currentSynth:
		return  # already patched

	CACHED_SYNTH = currentSynth
	currentSynth.speak = patchedSpeak.__get__(currentSynth, type(currentSynth))


def patchedSpeak(self, speechSequence: SpeechSequence) -> None:  # noqa: C901
	# log.info(f"\npatched_speak input: {speechSequence}")
	textList: list[str] = []
	langChanged = False
	prosody: dict[str, int] = {}
	# We output malformed XML, as we might close an outer tag after opening an inner one; e.g.
	# <voice><prosody></voice></prosody>.
	# However, eSpeak doesn't seem to mind.
	for item in speechSequence:
		if isinstance(item, str):
			textList.append(self._processText(item))
		elif isinstance(item, IndexCommand):
			textList.append('<mark name="%d" />' % item.index)
		elif isinstance(item, CharacterModeCommand):
			textList.append('<say-as interpret-as="characters">' if item.state else "</say-as>")
		elif isinstance(item, LangChangeCommand):
			langChangeXML = self._handleLangChangeCommand(item, langChanged)
			textList.append(langChangeXML)
			langChanged = True
		elif isinstance(item, BreakCommand):
			textList.append(f'<break time="{item.time}ms" />')
		elif isinstance(item, RateCommand):
			if item.multiplier == 1:
				textList.append("<prosody/>")
			else:
				textList.append(f"<prosody rate={int(item.multiplier * 100)}%>")
		elif type(item) in self.PROSODY_ATTRS:
			if prosody:
				# Close previous prosody tag.
				textList.append('<break time="1ms" />')  # hack added for cutoff speech (issue #55)
				textList.append("</prosody>")
			attr = self.PROSODY_ATTRS[type(item)]
			if item.multiplier == 1:
				# Returning to normal.
				try:
					del prosody[attr]
				except KeyError:
					pass
			else:
				prosody[attr] = int(item.multiplier * 100)
			if not prosody:
				continue
			textList.append("<prosody")
			for attr, val in prosody.items():
				textList.append(' %s="%d%%"' % (attr, val))
			textList.append(">")
		elif isinstance(item, PhonemeCommand):
			# We can't use str.translate because we want to reject unknown characters.
			try:
				phonemes: str = "".join([self.IPA_TO_ESPEAK[char] for char in item.ipa])
				# There needs to be a space after the phoneme command.
				# Otherwise, eSpeak will announce a subsequent SSML tag instead of processing it.
				textList.append("[[%s]] " % phonemes)
			except KeyError:
				log.debugWarning("Unknown character in IPA string: %s" % item.ipa)
				if item.text:
					textList.append(self._processText(item.text))
		else:
			log.exception("Unknown speech: %s" % item)
	# Close any open tags.
	if langChanged:
		textList.append("</voice>")
	if prosody:
		textList.append("</prosody>")
	text = "".join(textList)
	# log.info(f"monkey-patched text={text}")
	oldRate: int = getSynth()._get_rate()
	_espeak.speak(text)
	# try to get around espeak bug where voice slows down
	getSynth()._set_rate(oldRate)
