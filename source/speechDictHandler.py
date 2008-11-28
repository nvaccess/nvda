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
dictTypes = ("temp", "smart", "voice", "default", "builtin") # ordered by their priority E.G. voice specific speech dictionary is processed before the default
speechDictsPath=os.path.join(globalVars.appArgs.configPath, "speechdicts")
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
		if not fileName:
			return
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
	fileName = None
	compiled = None
	pattern = ""
	loaded = False
	name = ""

	def __init__(self, fileName=None, name=""):
		"""loads regexpr from the file"""
		super(list,self).__init__()
		self.fileName = fileName
		self.name = name
		if fileName is None: return
		file = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		s = file.readline()
		if not s.startswith("#!"): raise RuntimeError("No regexpr found at starting of file %s"%fileName)
		s = s[2:]
		self.pattern = s.rstrip('\r\n')
		self.compiled = re.compile(self.pattern)
		file.close()

	def setPattern(self, pattern):
		self.pattern = pattern
		self.compiled = re.compile(self.pattern)

	def setName(self,name):
		self.name = name
		self.fileName= getFileName("smart", name=self.name)

	def matches(self, value):
		return self.compiled.search(value) is not None

	def save(self,fileName=None):
		if fileName is not None:
			self.fileName = fileName
		file = codecs.open(self.fileName,"w","utf_8_sig",errors="replace")
		file.write("#!%s\r\n\r\n" % self.pattern)
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
		if type == "smart": continue
		text=dictionaries[type].sub(text)
	for smart in dictionaries["smart"]: text=smart.sub(text) 
	return text

def getFileName(type, synth=synthDriverHandler.getSynth(), name=None):
	if type is "default":
		return os.path.join(speechDictsPath, "default.dic")
	elif type is "smart":
		return "%s/%s.sdic" % (speechDictsPath, api.filterFileName(name))
	elif type is "voice":
		return "%s/%s-%s.dic"%(speechDictsPath,api.filterFileName(synth.name),api.filterFileName(synth.getVoiceInfoByID(synth.voice).name))
	elif type is "builtin": return "builtin.dic"
	return None

def reflectVoiceChange(synth=None):
	"""updates the speech dictionaries reflecting voice change"""
	if synth == None:
		synth = synthDriverHandler.getSynth()
	dictionaries["voice"].load(getFileName("voice", synth))
	name = "%s-%s" %(synth.name, synth.getVoiceInfoByID(synth.voice).name)
	del dictionaries["smart"][:]
	[(dict.load(), dictionaries["smart"].append(dict)) for dict in smartDicts if dict.matches(name)]

def initialize():
	#create speechDicts folder if appropriate
	if not os.path.isdir(speechDictsPath):
		os.makedirs(speechDictsPath)
	#search for the smart dictionaries
	counter = 0
	for name in os.listdir(speechDictsPath):
		if not name.endswith(".sdic"): continue
		smartDicts.append(SmartDict("%s/%s"%(speechDictsPath, name), name[:-5]))
		counter += 1
	if counter > 0:
		log.info("found %d smart dictionaries"%counter)
	#create the speechDict objects for all excluding smart
	for type in [x for x in dictTypes if x != "smart"]:
		dictionaries[type]=SpeechDict()
	dictionaries["smart"] = []
	dictionaries["default"].load(getFileName("default"))
	dictionaries["builtin"].load(getFileName("builtin"))
