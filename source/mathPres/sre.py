# -*- coding: UTF-8 -*-
#sre.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014-2016 NV Access Limited

"""Support for math presentation using Speech Rule Engine.
"""

import os
import json
import subprocess
import re
import wx
import mathPres
from keyboardHandler import KeyboardInputGesture
import speech

RE_NAMESPACE = re.compile(r"<([^:>]+):math[>\s]")
def _processMathMl(mathMl):
	# Strip the XML namespace, if any.
	m = RE_NAMESPACE.search(mathMl)
	if m:
		mathMl = mathMl.replace(m.group(1) + ":", "")
	return mathMl

RE_SRE_SPEECH = re.compile(
	# Break.
	r'<break time = "(?P<break>\d+)ms"/> ?'
	# Pronunciation of characters.
	ur"|<say-as interpret-as='characters'>(?P<char>[^<])</say-as> ?"
	# Specific pronunciation.
	ur"|<phoneme alphabet='ipa' ph='(?P<ipa>[^']+)'> (?P<phonemeText>[^ <]+)</phoneme> ?"
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
	"pitch": speech.PitchCommand,
	"volume": speech.VolumeCommand,
	"rate": speech.RateCommand,
}
RE_HYPHEN = re.compile(r"(?<=\w)-(?=\w)")
def _processSreSpeech(text, language):
	# hack: SRE doesn't yet indicate that the letter "a" should be spoken as a character.
	text += " "
	text = text.replace(" a ", "<say-as interpret-as='characters'>a</say-as>")
	# SRE's default rate is 180 wpm.
	# Assume that 0% is 80 wpm and 100% is 450 wpm and scale accordingly.
	synth = speech.getSynth()
	wpm = synth._percentToParam(synth.rate, 80, 450)
	breakMulti = 180.0 / wpm
	out = []
	if language:
		out.append(speech.LangChangeCommand(language))
	resetProsody = set()
	for m in RE_SRE_SPEECH.finditer(text):
		if m.lastgroup == "break":
			out.append(speech.BreakCommand(time=int(m.group("break")) * breakMulti))
		elif m.lastgroup == "char":
			out.extend((speech.CharacterModeCommand(True),
				m.group("char"), speech.CharacterModeCommand(False)))
		elif m.lastgroup == "comma":
			out.append(speech.BreakCommand(time=100))
		elif m.lastgroup in PROSODY_COMMANDS:
			command = PROSODY_COMMANDS[m.lastgroup]
			out.append(command(multiplier=int(m.group(m.lastgroup)) / 100.0))
			resetProsody.add(command)
		elif m.lastgroup == "prosodyReset":
			for command in resetProsody:
				out.append(command(multiplier=1))
			resetProsody.clear()
		elif m.lastgroup == "phonemeText":
			out.append(speech.PhonemeCommand(m.group("ipa"),
				text=m.group("phonemeText")))
		elif m.lastgroup == "content":
			content = m.group(0)
			# Convert hyphens in words to spaces.
			content = RE_HYPHEN.sub(" ", content)
			out.append(content)
	if language:
		out.append(speech.LangChangeCommand(None))
	return out

class SreInteraction(mathPres.MathInteractionNVDAObject):

	def __init__(self, provider=None, mathMl=None):
		super(SreInteraction, self).__init__(provider=provider, mathMl=mathMl)
		self._speech = _processSreSpeech(provider._call("sre.walk", mathMl), None)
		self._provider = provider

	def reportFocus(self):
		super(SreInteraction, self).reportFocus()
		speech.speak(self._speech)

	def getScript(self, gesture):
		# Pass most keys to SRE. Pretty ugly.
		if isinstance(gesture, KeyboardInputGesture) and "NVDA" not in gesture.modifierNames and (
			gesture.mainKeyName in {
				"leftArrow", "rightArrow", "upArrow", "downArrow",
			}
		):
			return self.script_navigate
		return super(SreInteraction, self).getScript(gesture)

	def script_navigate(self, gesture):
		ret = self._provider._call("sre.move", gesture.vkCode)
		if ret:
			speech.speak(_processSreSpeech(ret, None))
		else:
			wx.Bell()

class Sre(mathPres.MathPresentationProvider):

	def __init__(self):
		# Start our Node.js bridge.
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		si.wShowWindow = subprocess.SW_HIDE
		self._proc = subprocess.Popen(
			["node.exe", os.path.join(os.path.dirname(__file__), "sre.js")],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
			startupinfo=si)

	def _exec(self, code):
		# Pass code to our Node.js bridge to eval.
		code = json.dumps(code)
		self._proc.stdin.write(code + "\n")
		self._proc.stdin.flush()
		# Get and parse the response.
		ret = self._proc.stdout.readline()
		cmd, arg = ret.rstrip().split(" ", 1)
		if cmd == "ret":
			# Normal return.
			if arg.rstrip() == "undefined":
				# JSON doesn't support undefined.
				return None
			return json.loads(arg)
		elif cmd == "exc":
			# Exception.
			raise RuntimeError(arg)

	def _call(self, func, *args):
		args = json.dumps(args)
		return self._exec("{func}.apply(this, {args});".format(func=func, args=args))

	def getSpeechForMathMl(self, mathMl):
		mathMl = _processMathMl(mathMl)
		return _processSreSpeech(self._call("sre.toSpeech", mathMl), None)

	def interactWithMathMl(self, mathMl):
		mathMl = _processMathMl(mathMl)
		SreInteraction(provider=self, mathMl=mathMl).setFocus()
