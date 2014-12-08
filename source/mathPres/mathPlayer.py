#mathPlayer.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""Support for math presentation using MathPlayer 2014.
"""

import comtypes.client
from comtypes import COMError
from comtypes.gen.MathPlayer import MPInterface, IMathSpeech, IMathNavigation, IMathBraille
import speech
from keyboardHandler import KeyboardInputGesture
import braille
import mathPres

def _processMpSpeech(text):
	# todo
	return [text]

class MathPlayerInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(MathPlayerInteraction, self).__init__(provider=provider, mathMl=mathMl)
		provider._mpSpeech.SetMathML(mathMl)

	def reportFocus(self):
		super(MathPlayerInteraction, self).reportFocus()
		speech.speak(_processMpSpeech(self.provider._mpSpeech.GetSpokenText()))

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
		speech.speak(_processMpSpeech(text))

class MathPlayer(mathPres.MathPresentationProvider):

	def __init__(self):
		mpSpeech = self._mpSpeech = comtypes.client.CreateObject(MPInterface, interface=IMathSpeech)
		self._mpNavigation = mpSpeech.QueryInterface(IMathNavigation)
		self._mpBraille = mpSpeech.QueryInterface(IMathBraille)

	def getSpeechForMathMl(self, mathMl):
		self._mpSpeech.SetMathML(mathMl)
		return _processMpSpeech(self._mpSpeech.GetSpokenText())

	def getBrailleForMathMl(self, mathMl):
		self._mpSpeech.SetMathML(mathMl)
		self._mpBraille.SetBrailleWidth(braille.handler.displaySize)
		return self._mpBraille.GetBraille()

	def interactWithMathMl(self, mathMl):
		MathPlayerInteraction(provider=self, mathMl=mathMl).setFocus()
