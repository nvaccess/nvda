#userDictHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import globalVars
import os
import codecs
import synthDriverHandler

dictionaries = {}
dictTypes = ("temp", "voice", "default") # ordered by their priority E.G. voice specific user dictionary is processed before the default
userDictsPath="userdicts"

class UserDictEntry:

	def __init__(self, pattern, replacement):
		self.pattern = pattern
		self.compiled = re.compile(pattern)
		self.replacement = replacement

	def sub(self, text):
		return self.compiled.sub(self.replacement, text)

class UserDict(list):

	def load(self, fileName):
		del self[:]
		globalVars.log.debug("Loading user dictionary '%s'..." % fileName)
		if not os.path.isfile(fileName): 
			globalVars.log.debug("file '%s' not found." % fileName)
			return
		file = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		for line in filter(lambda x: not x.startswith('#') and not x.isspace(), file.readlines()):
			temp = line.replace("\n","").split("\t")
			if len(temp) ==2:
				self.append(UserDictEntry(temp[0],temp[1]))
			else:
				globalVars.log.warning("can't parse line '%s'" % line)
		globalVars.log.debug("%d loaded records." % len(self))
		file.close()
		return

	def sub(self, text):
		for entry in self:
			text = entry.sub(text)
		return text

def processText(text):
	for entry in dictionaries.values():
		text=entry.sub(text)
	return text

def getFileName(type):
	if type is "default":
		return "%s/default.dic"%userDictsPath
	elif type is "voice":
		s=synthDriverHandler.getSynth()
		return "%s/%s-%s.dic"%(userDictsPath,s.name,s.getVoiceName(s.voice))
	return None

def initialize():
	for type in dictTypes:
		dictionaries[type]=UserDict()
	dictionaries["default"].load(getFileName("default"))

