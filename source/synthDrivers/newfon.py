#synthDrivers/newfon.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
from synthDriverHandler import SynthDriver,VoiceInfo
from ctypes import *
import os
import re

re_englishLetter = re.compile(r"([a-z])", re.I)
re_individualLetters = re.compile(r"\b([a-z])\b", re.I)
re_abbreviations = re.compile(r"\b([bcdfghjklmnpqrstvwxz]+)\d*\b", re.I)
re_letterAfterNumber = re.compile(r"(\d)(\D)", re.LOCALE)
newfon_lib = None

letters = {
'a': u"эй",
'b' : u"би",
'c': u"си",
'd': u"ди",
'e': u"и",
'f': u"эф",
'g': u"джи",
'h': u"эйчь",
'i': u"ай",
'j': u"джей",
'k': u"кэй",
'l': u"эль",
'm': u"эм",
'n': u"эн",
'o': u"оу",
'p': u"пи",
'q': u"къю",
'r': u"ар",
's': u"эс",
't': u"ти",
'u': u"ю",
'v': u"ви",
'w': u"да+блъю",
'x': u"экс",
'y': u"вай",
'z': u"зи",
u"б": u"бэ",
u"в": u"вэ",
u"к": u"ка",
u"с": u"эс",
u"ь": u"мя",
u"ъ": u"твё"
}

def replaceEnglishLetter(match):
	return "%s " % letters[match.group(1)]

def replaceEnglishLetters(match):
	return re_englishLetter.sub(replaceEnglishLetter, match.group(1))

def preprocessText(text):
	text = text.lower()
	if len(text) == 1:
		return letters[text] if letters.has_key(text) else text
	text = re_letterAfterNumber.sub(r"\1 \2", text)
	text = re_abbreviations.sub(replaceEnglishLetters, text)
	text = re_individualLetters.sub(replaceEnglishLetter, text)
	text = text.replace("x", u"кс")
	text = text.replace("e", u"э")
	text = text.replace("y", u"ы")
	text = text.replace("j", u"дж")
	return text

class SynthDriver(SynthDriver):
	name="newfon"
	description = _("russian newfon synthesizer by Sergey Shishmintzev")
	hasVoice=True
	hasRate=True
	hasVolume = True
	hasPitch = True
	_pitch = 50
	availableVoices = (VoiceInfo("0", _("male 1")), VoiceInfo("1", _("female 1")), VoiceInfo("2", _("male 2")), VoiceInfo("3", _("female 2")))

	@classmethod
	def check(cls):
		if os.path.isfile('synthDrivers/newfon_nvda.dll'):
			return True
		else:
			return False

	def __init__(self):
		global newfon_lib
		newfon_lib = windll.LoadLibrary(r"synthDrivers\newfon_nvda.dll")
		newfon_lib.getVoiceName.restype = c_char_p
		newfon_lib.speakText.argtypes = [c_char_p, c_int]
		if not newfon_lib.initialize(): raise Exception

	def terminate(self):
		global newfon_lib
		newfon_lib.terminate()
		newfon_lib=None

	def speakText(self, text, index=None):
		text = preprocessText(text)
		global newfon_lib
		if index is not None: 
			newfon_lib.speakText(text,index)
		else:
			newfon_lib.speakText(text,-1)

	def _get_lastIndex(self):
		global newfon_lib
		return newfon_lib.get_lastIndex()

	def cancel(self):
		global newfon_lib
		newfon_lib.cancel()

	def _get_voice(self):
		global newfon_lib
		return str(newfon_lib.get_voice())

	def _set_voice(self, value):
		global newfon_lib
		newfon_lib.set_voice(int(value))

	def _get_rate(self):
		global newfon_lib
		return newfon_lib.get_rate()

	def _set_rate(self, value):
		global newfon_lib
		newfon_lib.set_rate(value)

	def _get_volume(self):
		global newfon_lib
		return newfon_lib.get_volume()

	def _set_volume(self, value):
		global newfon_lib
		newfon_lib.set_volume(value)

	def _set_pitch(self, value):
		global newfon_lib
		if value <= 50: value = 50
		newfon_lib.set_accel(value/5 -10 )
		self._pitch = value

	def _get_pitch(self):
		return self._pitch

	def pause(self, switch):
		if switch: self.cancel()
