# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import re
from collections.abc import Callable, Generator
from ctypes import (
	Array,
	WinError,
	c_wchar,
	windll,
)
from os import path
from typing import Type

import braille
import config
import gui
import libmathcat_py as libmathcat
import speech
import ui
import winKernel
import winUser
from api import getClipData
from keyboardHandler import KeyboardInputGesture
from logHandler import log
from scriptHandler import script
from NVDAState import WritePaths

from speech.commands import (
	BaseProsodyCommand,
	BeepCommand,
	PitchCommand,
	RateCommand,
	SpeechCommand,
	SynthCommand,
	VolumeCommand,
)
from synthDriverHandler import (
	SynthDriver,
	getSynth,
)
from textUtils import WCHAR_ENCODING

import mathPres
from .localization import getLanguageToUse
from .speech import convertSSMLTextForNVDA

PROSODY_COMMANDS: dict[str, BaseProsodyCommand] = {
	"pitch": PitchCommand,
	"volume": VolumeCommand,
	"rate": RateCommand,
}


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
		try:
			text: str = libmathcat.DoNavigateCommand("ZoomIn")
			speech.speak(convertSSMLTextForNVDA(text))
		except Exception:
			log.exception()
			# Translators: this message reports an error in starting navigation of math.
			ui.message(pgettext("math", "Error in starting navigation of math."))

	def getBrailleRegions(
		self,
		review: bool = False,
	) -> Generator[braille.Region, None, None]:
		"""Yields braille.Region objects for this MathCATInteraction object."""
		yield braille.NVDAObjectRegion(self, appendText=" ")
		region: braille.Region = braille.Region()
		region.focusToHardLeft = True
		try:
			region.rawText = libmathcat.GetBraille("")
		except Exception:
			log.exception()
			# Translators: this message alerts users to an error in brailling math.
			ui.message(pgettext("math", "Error in brailling math: see NVDA error log for details"))
			region.rawText = ""

		yield region

	def getScript(
		self,
		gesture: KeyboardInputGesture,
	) -> Callable[[KeyboardInputGesture], None] | None:
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
		):
			return self.script_navigate
		else:
			return super().getScript(gesture)

	def script_navigate(self, gesture: KeyboardInputGesture) -> None:
		"""Performs the specified navigation command.

		:param gesture: The keyboard command which specified the navigation command to perform.
		"""
		try:
			if gesture is not None:  # == None when initial focus -- handled in reportFocus()
				modNames: list[str] = gesture.modifierNames
				text = libmathcat.DoNavigateKeyPress(
					gesture.vkCode,
					"shift" in modNames,
					"control" in modNames,
					"alt" in modNames,
					False,
				)
				speech.speak(convertSSMLTextForNVDA(text))
		except Exception:
			log.exception()
			# Translators: this message alerts users to an error in navigating math.
			ui.message(pgettext("math", "Error in navigating math"))

		if not braille.handler.enabled:
			return

		try:
			# update the braille to reflect the nav position (might be excess code, but it works)
			navNode: tuple[str, int] = libmathcat.GetNavigationMathMLId()
			brailleChars = libmathcat.GetBraille(navNode[0])
			region: braille.Region = braille.Region()
			region.rawText = brailleChars
			region.focusToHardLeft = True
			region.update()
			braille.handler.buffer.regions.append(region)
			braille.handler.buffer.focus(region)
			braille.handler.buffer.update()
			braille.handler.update()
		except Exception:
			log.exception()
			# Translators: this message alerts users to an error brailling math.
			ui.message(pgettext("math", "Error in brailling math"))

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
			except Exception:
				log.exception("Not able to get 'CopyAs' preference.")
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
			ui.message(pgettext("math", "copy as ") + copyAs)
		except Exception:
			log.exception()
			# Translators: alerts users to an error copying math.
			ui.message(pgettext("unable to copy math"))

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
		# Need to support MathML Presentation, so this is copied from winUser.py and the first two lines are removed
		# For now only unicode is a supported format
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

		try:
			# IMPORTANT -- SetRulesDir must be the first call to libmathcat besides GetVersion()
			rulesDir: str = path.join(
				WritePaths.mathCATDir,
				"Rules",
			)
			log.info(f"MathCAT {libmathcat.GetVersion()} installed. Using rules dir: {rulesDir}")
			libmathcat.SetRulesDir(rulesDir)
			libmathcat.SetPreference("TTS", "SSML")
		except Exception:
			log.exception()
			# Translators: this message directs users to look in the log file
			ui.message(pgettext("math", "Error navigating math"))

	def getSpeechForMathMl(
		self,
		mathml: str,
	) -> list[str | SpeechCommand]:
		"""Outputs a MathML string as speech.

		:param mathml: A MathML string.
		:returns: A list of speech commands and strings representing the given MathML.
		"""
		synth: SynthDriver = getSynth()
		synthConfig = config.conf["speech"][synth.name]
		try:
			# need to set Language before the MathML for DecimalSeparator canonicalization
			language: str = getLanguageToUse(mathml)
			# MathCAT should probably be extended to accept "extlang" tagging, but it uses lang-region tagging at the moment
			libmathcat.SetPreference("Language", language)
			libmathcat.SetMathML(mathml)
		except Exception:
			log.exception()
			log.exception(f"MathML is {mathml}")
			# Translators: this message reports when invalid math is found.
			ui.message(pgettext("math", "Invalid math formatting found"))
			libmathcat.SetMathML("<math></math>")
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

		except Exception:
			log.exception()
			# Translators: this message reports an error in speaking math.
			ui.message(pgettext("math", "Error in speaking math."))
			return [""]

	def _addSounds(self) -> bool:
		"""Queries the user preferences to determine whether or not sounds should be added.

		:returns: True if MathCAT's `SpeechSound` preference is set, and False otherwise.
		"""
		try:
			return libmathcat.GetPreference("SpeechSound") != "None"
		except Exception:
			log.exception()
			return False

	def getBrailleForMathMl(self, mathml: str) -> str:
		"""Gets the braille representation of a given MathML string by calling MathCAT's GetBraille function.

		:param mathml: A MathML string.
		:returns: A braille string representing the input MathML.
		"""
		try:
			libmathcat.SetMathML(mathml)
		except Exception:
			log.exception()
			log.exception(f"MathML is {mathml}")
			# Translators: this message reports illegal MathML.
			ui.message(pgettext("math", "Illegal MathML found."))
			libmathcat.SetMathML("<math></math>")
		try:
			return libmathcat.GetBraille("")
		except Exception:
			log.exception()
			# Translators: this message reports an error in brailling math.
			ui.message(pgettext("math", "Error in brailling math."))
			return ""

	def interactWithMathMl(self, mathml: str) -> None:
		"""Interact with a MathML string, creating a MathCATInteraction object.

		:param mathml: The MathML representing the math to interact with.
		"""
		MathCATInteraction(provider=self, mathMl=mathml).setFocus()
		interaction = MathCATInteraction(provider=self, mathMl=mathml)
		interaction.setFocus()
		interaction.script_navigate(None)
