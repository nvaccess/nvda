#mathPres/pymathspeak.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import wx
import mathspeak.en
from mathspeak.interaction import InteractiveMathSpeak
import mathPres
import speech

RE_HYPHEN = re.compile(r"(?<=[^\W\d_])-(?=[^\W\d_])")
RE_SINGLE_ALPHA = re.compile(r"\b[^\W\d_]\b")
def _processSpeech(text):
	# Replace hyphenated operator names with spaces.
	text = RE_HYPHEN.sub(" ", text)
	# Use CharacterModeCommand for single alphabetic characters
	# to ensure they're pronounced correctly.
	out = []
	end = 0
	for m in RE_SINGLE_ALPHA.finditer(text):
		start = m.start()
		# Output the chunk between the last match and this one.
		chunk = text[end:start]
		if chunk:
			out.append(chunk)
		out.extend((speech.CharacterModeCommand(True), m.group(0),
			speech.CharacterModeCommand(False)))
		end = m.end()
	# Output the remaining text after the last match.
	chunk = text[end:]
	if chunk:
		out.append(chunk)
	return out

class PyMathSpeakInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(PyMathSpeakInteraction, self).__init__(provider=provider, mathMl=None)
		self.interactive = InteractiveMathSpeak(provider.mathSpeak, mathMl.encode("UTF-8"))

	def reportNode(self):
		speech.speak(_processSpeech(self.interactive.node.text))

	def reportFocus(self):
		super(PyMathSpeakInteraction, self).reportFocus()
		self.reportNode()

	def _movementScript(self, func):
		try:
			text = func()
		except LookupError:
			wx.Bell()
			return
		speech.speak(_processSpeech(text))

	def script_moveNext(self, gesture):
		self._movementScript(self.interactive.nextNode)

	def script_movePrevious(self, gesture):
		self._movementScript(self.interactive.previousNode)

	def script_moveIn(self, gesture):
		self._movementScript(self.interactive.childNode)

	def script_moveOut(self, gesture):
		self._movementScript(self.interactive.parentNode)

	def script_nextColumn(self, gesture):
		self._movementScript(self.interactive.nextColumn)

	def script_previousColumn(self, gesture):
		self._movementScript(self.interactive.previousColumn)

	def script_nextRow(self, gesture):
		self._movementScript(self.interactive.nextRow)

	def script_previousRow(self, gesture):
		self._movementScript(self.interactive.previousRow)

	__gestures = {
		"kb:rightArrow": "moveNext",
		"kb:leftArrow": "movePrevious",
		"kb:downArrow": "moveIn",
		"kb:upArrow": "moveOut",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+alt+leftArrow": "previousColumn",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+upArrow": "previousRow",
	}

class PyMathSpeak(mathPres.MathPresentationProvider):

	def __init__(self):
		self.mathSpeak = mathspeak.en.MathSpeak()

	def getSpeechForMathMl(self, mathMl):
		return _processSpeech(self.mathSpeak.translate(mathMl.encode("UTF-8")))

	def interactWithMathMl(self, mathMl):
		PyMathSpeakInteraction(provider=self, mathMl=mathMl).setFocus()
