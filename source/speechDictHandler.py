# -*- coding: UTF-8 -*-
#speechDictHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2016 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Aaron Cannon, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import os
import codecs
import globalVars
from logHandler import log
import api
import config

dictionaries = {}
dictTypes = ("temp", "voice", "default", "builtin") # ordered by their priority E.G. voice specific speech dictionary is processed before the default
speechDictsPath=os.path.join(globalVars.appArgs.configPath, "speechDicts")

# Types of speech dictionary entries:
ENTRY_TYPE_ANYWHERE = 0 # String can match anywhere
ENTRY_TYPE_WORD = 2 # String must have word boundaries on both sides to match
ENTRY_TYPE_REGEXP = 1 # Regular expression

#Types of regexp for parsing numbers:
RE_SINGLE_DIGITS = re.compile(r"(\d)(?=\d+(\D|\b))", re.UNICODE)
RE_DOUBLE_DIGITS = re.compile(r"(\d{0,2})(?=(\d{2})+(\D|\b))", re.UNICODE)
RE_TRIPLE_DIGITS = re.compile(r"(\d{0,3})(?=(\d{3})+(\D|\b))", re.UNICODE)

class SpeechDictEntry:

	def __init__(self, pattern, replacement,comment,caseSensitive=True,type=ENTRY_TYPE_ANYWHERE):
		self.pattern = pattern
		flags = re.U
		if not caseSensitive: flags|=re.IGNORECASE
		if type == ENTRY_TYPE_REGEXP:
			tempPattern = pattern
		elif type == ENTRY_TYPE_WORD:
			tempPattern = r"\b" + re.escape(pattern) + r"\b"
		else:
			tempPattern= re.escape(pattern)
			type = ENTRY_TYPE_ANYWHERE # Insure sane values.
		self.compiled = re.compile(tempPattern,flags)
		self.replacement = replacement
		self.comment=comment
		self.caseSensitive=caseSensitive
		self.type=type

	def sub(self, text):
		replacement=self.replacement
		return self.compiled.sub(replacement, text)

class SpeechDict(list):

	def load(self, fileName):
		self.fileName=fileName
		comment=""
		del self[:]
		log.debug("Loading speech dictionary '%s'..." % fileName)
		if not os.path.isfile(fileName): 
			log.debug("file '%s' not found." % fileName)
			return
		file = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		for line in file:
			if line.isspace():
				comment=""
				continue
			line=line.rstrip('\r\n')
			if line.startswith('#'):
				if comment:
					comment+=" "
				comment+=line[1:]
			else:
				temp=line.split("\t")
				if len(temp) ==4:
					pattern = temp[0].replace(r'\#','#')
					replace = temp[1].replace(r'\#','#')
					try:
						dictionaryEntry=SpeechDictEntry(pattern, replace, comment, caseSensitive=bool(int(temp[2])), type=int(temp[3]))
						self.append(dictionaryEntry)
					except Exception as e:
						log.exception("Dictionary (\"%s\") entry invalid for \"%s\" error raised: \"%s\"" % (fileName, line, e))
					comment=""
				else:
					log.warning("can't parse line '%s'" % line)
		log.debug("%d loaded records." % len(self))
		file.close()
		return

	def save(self,fileName=None):
		if not fileName:
			fileName=getattr(self,'fileName',None)
		if not fileName:
			return
		dirName=os.path.dirname(fileName)
		if not os.path.isdir(dirName):
			os.makedirs(dirName)
		file = codecs.open(fileName,"w","utf_8_sig",errors="replace")
		for entry in self:
			if entry.comment:
				file.write("#%s\r\n"%entry.comment)
			file.write("%s\t%s\t%s\t%s\r\n"%(entry.pattern.replace('#',r'\#'),entry.replacement.replace('#',r'\#'),int(entry.caseSensitive),entry.type))
		file.close()

	def sub(self, text):
		for entry in self:
			text = entry.sub(text)
		return text

def processNumbers(numberSetting, text):
	#0: processes default behavior. 1-3: splits on single-triple digits.
	#Use two spaces instead of one, because some locales use space as thousands separator.
	if numberSetting == 1:
		text = RE_SINGLE_DIGITS.sub(r"  \1  ", text)
	elif numberSetting == 2:
		text = RE_DOUBLE_DIGITS.sub(r"  \1  ", text)
	elif numberSetting == 3:
		text = RE_TRIPLE_DIGITS.sub(r"  \1  ", text)
	return text


def processText(text):
	if globalVars.speechDictionaryProcessing:
		for type in dictTypes:
			text=dictionaries[type].sub(text)
	numberSetting = config.conf["speech"]["readNumbersAs"]
	return processNumbers(numberSetting, text)

def initialize():
	for type in dictTypes:
		dictionaries[type]=SpeechDict()
	dictionaries["default"].load(os.path.join(speechDictsPath, "default.dic"))
	dictionaries["builtin"].load("builtin.dic")

def loadVoiceDict(synth):
	"""Loads appropriate dictionary for the given synthesizer.
It handles case when the synthesizer doesn't support voice setting.
"""
	if synth.isSupported("voice"):
		voiceName = synth.availableVoices[synth.voice].name
		fileName=r"%s\%s-%s.dic"%(speechDictsPath,synth.name,api.filterFileName(voiceName))
	else:
		fileName=r"%s\%s.dic"%(speechDictsPath,synth.name)
	dictionaries["voice"].load(fileName)
