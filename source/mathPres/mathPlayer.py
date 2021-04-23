# -*- coding: UTF-8 -*-
#mathPlayer.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014-2015 NV Access Limited

"""Support for math presentation using MathPlayer 4.
"""

import re
import comtypes.client
from comtypes import COMError
from comtypes.gen.MathPlayer import MPInterface, IMathSpeech, IMathSpeechSettings, IMathNavigation, IMathBraille
import speech
from synthDriverHandler import getSynth
from keyboardHandler import KeyboardInputGesture
import braille
import mathPres

from speech.commands import (
	PitchCommand,
	VolumeCommand,
	RateCommand,
	LangChangeCommand,
	BreakCommand,
	CharacterModeCommand,
	PhonemeCommand,
)

RE_MP_SPEECH = re.compile(
	# Break.
	r"<break time='(?P<break>\d+)ms'/> ?"
	# Pronunciation of characters.
	r"|<say-as interpret-as='characters'>(?P<char>[^<])</say-as> ?"
	# Specific pronunciation.
	r"|<phoneme alphabet='ipa' ph='(?P<ipa>[^']+)'> (?P<phonemeText>[^ <]+)</phoneme> ?"
	# Prosody.
	r"|<prosody(?: pitch='(?P<pitch>\d+)%')?(?: volume='(?P<volume>\d+)%')?(?: rate='(?P<rate>\d+)%')?> ?"
	r"|(?P<prosodyReset></prosody>) ?"
	# Other tags, which we don't care about.
	r"|<[^>]+> ?"
	# Commas indicating pauses in navigation messages.
	r"| ?(?P<comma>,) ?"
	# Actual content.
	r"|(?P<content>[^<,]+)")
PROSODY_COMMANDS = {
	"pitch": PitchCommand,
	"volume": VolumeCommand,
	"rate": RateCommand,
}
def _processMpSpeech(text, language):
	# MathPlayer's default rate is 180 wpm.
	# Assume that 0% is 80 wpm and 100% is 450 wpm and scale accordingly.
	synth = getSynth()
	wpm = synth._percentToParam(synth.rate, 80, 450)
	breakMulti = 180.0 / wpm
	out = []
	if language:
		out.append(LangChangeCommand(language))
	resetProsody = set()
	for m in RE_MP_SPEECH.finditer(text):
		if m.lastgroup == "break":
			out.append(BreakCommand(time=int(m.group("break")) * breakMulti))
		elif m.lastgroup == "char":
			out.extend((CharacterModeCommand(True), m.group("char"), CharacterModeCommand(False)))
		elif m.lastgroup == "comma":
			out.append(BreakCommand(time=100))
		elif m.lastgroup in PROSODY_COMMANDS:
			command = PROSODY_COMMANDS[m.lastgroup]
			out.append(command(multiplier=int(m.group(m.lastgroup)) / 100.0))
			resetProsody.add(command)
		elif m.lastgroup == "prosodyReset":
			for command in resetProsody:
				out.append(command(multiplier=1))
			resetProsody.clear()
		elif m.lastgroup == "phonemeText":
			out.append(PhonemeCommand(m.group("ipa"), text=m.group("phonemeText")))
		elif m.lastgroup == "content":
			out.append(m.group(0))
	if language:
		out.append(LangChangeCommand(None))
	return out

class MathPlayerInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(MathPlayerInteraction, self).__init__(provider=provider, mathMl=mathMl)
		provider._setSpeechLanguage(mathMl)
		provider._mpSpeech.SetMathML(mathMl)

	def reportFocus(self):
		super(MathPlayerInteraction, self).reportFocus()
		speech.speak(_processMpSpeech(self.provider._mpSpeech.GetSpokenText(),
			self.provider._language))

	def getBrailleRegions(self, review=False):
		yield braille.NVDAObjectRegion(self, appendText=" ")
		region = braille.Region()
		region.focusToHardLeft = True
		self.provider._mpBraille.SetBrailleWidth(braille.handler.displaySize)
		region.rawText = self.provider._mpBraille.GetBraille()
		yield region

	def getScript(self, gesture):
		# Pass most keys to MathPlayer. Pretty ugly.
		if isinstance(gesture, KeyboardInputGesture) and "NVDA" not in gesture.modifierNames and (
			gesture.mainKeyName in {
				"leftArrow", "rightArrow", "upArrow", "downArrow",
				"home", "end",
				"space", "backspace", "enter",
			}
			or len(gesture.mainKeyName) == 1
		):
			return self.script_navigate
		return super(MathPlayerInteraction, self).getScript(gesture)

	def script_navigate(self, gesture):
		modNames = gesture.modifierNames
		try:
			text = self.provider._mpNavigation.DoNavigateKeyPress(gesture.vkCode,
				"shift" in modNames, "control" in modNames, "alt" in modNames, False)
		except COMError:
			return
		speech.speak(_processMpSpeech(text, self.provider._language))

class MathPlayer(mathPres.MathPresentationProvider):

	def __init__(self):
		mpSpeech = self._mpSpeech = comtypes.client.CreateObject(MPInterface, interface=IMathSpeech)
		mpSpeechSettings = self._mpSpeechSettings = mpSpeech.QueryInterface(IMathSpeechSettings)
		mpSpeechSettings.SetSpeechTags("SSML")
		self._mpNavigation = mpSpeech.QueryInterface(IMathNavigation)
		self._mpBraille = mpSpeech.QueryInterface(IMathBraille)

	def _setSpeechLanguage(self, mathMl):
		lang = mathPres.getLanguageFromMath(mathMl)
		if not lang:
			lang = speech.getCurrentLanguage()
		self._mpSpeechSettings.SetLanguage(lang.replace("_", "-"))
		self._language = lang

	def getSpeechForMathMl(self, mathMl):
		self._setSpeechLanguage(mathMl)
		self._mpSpeech.SetMathML(mathMl)
		return _processMpSpeech(self._mpSpeech.GetSpokenText(), self._language)

	def getBrailleForMathMl(self, mathMl):
		self._mpSpeech.SetMathML(mathMl)
		self._mpBraille.SetBrailleWidth(braille.handler.displaySize)
		return self._mpBraille.GetBraille()

	def interactWithMathMl(self, mathMl):
		MathPlayerInteraction(provider=self, mathMl=mathMl).setFocus()
