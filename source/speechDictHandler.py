#speechDictHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import globalVars
from logHandler import log
import os
import codecs
import synthDriverHandler
import api
import config

dictionaries = {}
dictTypes = ("temp", "voice", "default", "builtin") # ordered by their priority E.G. voice specific speech dictionary is processed before the default
speechDictsPath=os.path.join(globalVars.appArgs.configPath, "speechdicts")

class SpeechDictEntry:

	def __init__(self, pattern, replacement,comment,caseSensitive=True,regexp=False):
		self.pattern = pattern
		flags = re.U
		if not caseSensitive: flags=re.IGNORECASE
		tempPattern=pattern if regexp else re.escape(pattern)
		self.compiled = re.compile(tempPattern,flags)
		self.replacement = replacement
		self.comment=comment
		self.caseSensitive=caseSensitive
		self.regexp=regexp

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
					self.append(SpeechDictEntry(temp[0],temp[1],comment,bool(int(temp[2])),bool(int(temp[3]))))
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
			file.write("%s\t%s\t%s\t%s\r\n"%(entry.pattern,entry.replacement,int(entry.caseSensitive),int(entry.regexp)))
		file.close()

	def sub(self, text):
		for entry in self:
			text = entry.sub(text)
		return text

def processText(text):
	if not globalVars.speechDictionaryProcessing:
		return text
	for type in dictTypes:
		text=dictionaries[type].sub(text)
	return text

def initialize():
	for type in dictTypes:
		dictionaries[type]=SpeechDict()
	dictionaries["default"].load(os.path.join(speechDictsPath, "default.dic"))
	dictionaries["builtin"].load("builtin.dic")
