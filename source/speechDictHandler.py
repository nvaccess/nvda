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

dictionaries = {}
dictTypes = ("temp", "smart", "voice", "default") # ordered by their priority E.G. voice specific speech dictionary is processed before the default
speechDictsPath="speechdicts"
smartDicts = []

class SpeechDictEntry:

	def __init__(self, pattern, replacement,comment,caseSensitive=True,regexp=False):
		self.pattern = pattern
		flags=re.IGNORECASE if not caseSensitive else 0
		tempPattern=pattern if regexp else re.escape(pattern)
		flags = flags | re.U
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
		if fileName:
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

class SmartDict(SpeechDict):
	fileName = ""
	compiled = None
	pattern = ""
	loaded = False

	def __init__(self, fileName):
		"""loads regexpr from the file"""
		super(list,self).__init__()
		self.fileName = fileName
		file = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		s = file.readline()
		if not s.startswith("#!"): raise RuntimeError("No regexpr found at starting of file %s"%fileName)
		s = s[2:]
		self.pattern = s.rstrip('\r\n')
		self.compiled = re.compile(self.pattern)
		file.close()

	def matches(self, value):
		return self.compiled.search(value) is not None

	def save(self,fileName=None):
		if fileName is not None:
			self.fileName = fileName
		file = codecs.open(fileName,"w","utf_8_sig",errors="replace")
		file.write("#!%s\r\n" % self.pattern)
		for entry in self:
			if entry.comment:
				file.write("#%s\r\n"%entry.comment)
			file.write("%s\t%s\t%s\t%s\r\n"%(entry.pattern,entry.replacement,int(entry.caseSensitive),int(entry.regexp)))
		file.close()

	def load(self):
		if not self.loaded: SpeechDict.load(self,self.fileName)
		self.loaded = True

def processText(text):
	if not globalVars.speechDictionaryProcessing:
		return text
	for type in dictTypes:
		if type != "smart":
			text=dictionaries[type].sub(text)
	for smart in dictionaries["smart"]: text=smart.sub(text) 
	return text

def getFileName(type, synth=synthDriverHandler.getSynth()):
	if type is "default":
		return "%s/default.dic"%speechDictsPath
	elif type is "voice":
		return "%s/%s-%s.dic"%(speechDictsPath,api.validateFile(synth.name),api.validateFile(synth.getVoiceInfoByID(voice).name)))
	return None

def reflectVoiceChange(synth):
	"""updates the speech dictionaries reflecting voice change"""
	dictionaries["voice"].load(getFileName("voice", synth))
	name = "%s-%s" %(synth.name, synth.getVoiceInfoByID(voice).name)
	del dictionaries["smart"][:]
	[(dict.load(), dictionaries["smart"].append(dict)) for dict in smartDicts if dict.matches(name)]

def initialize():
	#search for the smart dictionaries
	counter = 0
	for name in os.listdir(speechDictsPath):
		if not name.endswith(".sdic"): continue
		smartDicts.append(SmartDict("%s/%s"%(speechDictsPath, name)))
		counter += 1
	if counter > 0:
		log.info("found %d smart dictionaries"%counter)
	#create the speechDict objects for all excluding smart
	for type in [x for x in dictTypes if x != "smart"]:
		dictionaries[type]=SpeechDict()
	dictionaries["smart"] = []
	dictionaries["default"].load(getFileName("default"))
