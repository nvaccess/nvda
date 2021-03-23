#speechDictHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2017 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import globalVars
from logHandler import log
import os
import codecs
import api
import config
from . import dictFormatUpgrade
from .speechDictVars import speechDictsPath

dictionaries = {}
dictTypes = ("temp", "voice", "default", "builtin") # ordered by their priority E.G. voice specific speech dictionary is processed before the default

# Types of speech dictionary entries:
ENTRY_TYPE_ANYWHERE = 0 # String can match anywhere
ENTRY_TYPE_WORD = 2 # String must have word boundaries on both sides to match
ENTRY_TYPE_REGEXP = 1 # Regular expression

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

	def getPattern(self):
		return self.pattern

	def sub(self, text):
		replacement=self.replacement
		return self.compiled.sub(replacement, text)

class SpeechDict(list):

	fileName = None

	def create(self, fileName):
		if os.path.exists(fileName):
			raise FileExistsError(f"can not create dictionary backed by file {fileName}")
		self.fileName = fileName
		log.debug("creating dictionary with file '%s'." % fileName)
	
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

	def syncFrom(self, source):
		for entry in source:
			if not next((x for x in self if x.pattern == entry.pattern), None):
				self.append(entry)
	
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
		invalidEntries = []
		for index, entry in enumerate(self):
			try:
				text = entry.sub(text)
			except re.error as exc:
				dictName = self.fileName or "temporary dictionary"
				log.error(f"Invalid dictionary entry {index+1} in {dictName}: \"{entry.pattern}\", {exc}")
				invalidEntries.append(index)
			for index in reversed(invalidEntries):
				del self[index]
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
	dictionaries["builtin"].load(os.path.join(globalVars.appDir, "builtin.dic"))
	config.post_configProfileSwitch.register(_handlePostConfigProfileSwitch)


def _handlePostConfigProfileSwitch(resetSpeechIfNeeded=True):
	reloadDictionaries()


def reloadDictionaries():
	from synthDriverHandler import getSynth
	synth = getSynth()
	loadProfileDict()
	loadVoiceDict(synth)
	log.debug(f"loaded dictionaries for profile {config.conf.getActiveProfile().name or 'default'}")


def _getVoiceDictionary(profile):
	from synthDriverHandler import getSynth
	synth = getSynth()
	dictionaryFilename = _getVoiceDictionaryFileName(synth)
	# if we are on default profile or the specific dictionary profile is already loaded
	if not profile.name or _hasVoiceDictionaryProfile(profile.name, synth.name, dictionaryFilename):
		# we are with the correct dictionary loaded. Just return it.
		log.debug(f"Voice dictionary, backed by {dictionaries['voice'].fileName} was requested")
		return dictionaries["voice"]
	# we are on a user profile for which there is no dictionary created for the current voice.
	# The current loaded dictionary is the default profile one.
	# As we have been called to get the profile dictionary for the current voice and it still does not exist,
	# We will create it now and pass the new, empty dictionary to the caller, but won't save it.
	# This is a task the caller should do when and if they wish
	dic = SpeechDict()
	dic.create(os.path.join(dictFormatUpgrade.getProfileVoiceDictsPath(), synth.name, dictionaryFilename))
	log.debug(
		f"voice dictionary was requested for profile {profile.name}, but the backing file does not exist."
		f" A New dictionary was created, set to be backed by {dic.fileName} if it is ever saved."
	)
	return dic


def getDictionary(type):
	profile = config.conf.getActiveProfile()
	if(type == "voice"):
		return _getVoiceDictionary(profile)
	# if we are om default profile or the specific dictionary profile is already loaded
	if not profile.name or _hasDictionaryProfile(profile.name, f"{type}.dic"):
		# we are with the correct dictionary loaded. Just return it.
		log.debug(f"{type} dictionary, backed by {dictionaries[type].fileName} was requested")
		return dictionaries[type]
	# we are on a user profile for which there is no dictionary created.
	# The current loaded dictionary is the default profile one.
	# As we have been called to get the current profile dictionary and it still does not exist,
	# We will create it now and pass the new, empty dictionary to the caller, but won't save it.
	# This is a task the caller should do when and if they wish
	dic = SpeechDict()
	dic.create(os.path.join(speechDictsPath, profile.name, f"{type}.dic"))
	log.debug(
		f"{type} dictionary was requested for profile {profile.name}, but the backing file does not exist."
		f" A New dictionary was created, set to be backed by {dic.fileName} if it is ever saved."
	)
	return dic


def loadProfileDict():
	profile = config.conf.getActiveProfile()
	if _hasDictionaryProfile(profile.name, "default.dic"):
		_loadProfileDictionary(dictionaries["default"], profile.name, "default.dic")
	else:
		dictionaries["default"].load(os.path.join(speechDictsPath, "default.dic"))
	dictionaries["builtin"].load("builtin.dic")


def loadVoiceDict(synth):
	"""Loads appropriate dictionary for the given synthesizer.
It handles case when the synthesizer doesn't support voice setting.
"""
	dictionaryFileName = _getVoiceDictionaryFileName(synth)
	profile = config.conf.getActiveProfile()
	if(_hasVoiceDictionaryProfile(profile.name, synth.name, dictionaryFileName)):
		_loadProfileVoiceDictionary(dictionaries["voice"], synth.name, dictionaryFileName)
	else:
		voiceDictsPath = dictFormatUpgrade.voiceDictsPath
		fileName = os.path.join(voiceDictsPath, synth.name, dictionaryFileName)
		dictionaries["voice"].load(fileName)


def _getVoiceDictionaryFileName(synth):
	try:
		dictFormatUpgrade.doAnyUpgrades(synth)
	except:
		log.error("error trying to upgrade dictionaries", exc_info=True)
		pass
	if synth.isSupported("voice"):
		voice = synth.availableVoices[synth.voice].displayName
		baseName = dictFormatUpgrade.createVoiceDictFileName(synth.name, voice)
	else:
		baseName=r"{synth}.dic".format(synth=synth.name)
	return baseName


def _hasDictionaryProfile(profileName, dictionaryName):
	return os.path.exists(os.path.join(speechDictsPath, profileName or "", dictionaryName))


def _hasVoiceDictionaryProfile(profileName, synthName, voiceName):
	return os.path.exists(os.path.join(dictFormatUpgrade.getProfileVoiceDictsPath(), synthName, voiceName))


def _loadProfileDictionary(target, profileName, dictionaryName):
	target.load(os.path.join(speechDictsPath, profileName or "", dictionaryName))


def _loadProfileVoiceDictionary(target, synthName, voiceName):
	target.load(os.path.join(dictFormatUpgrade.getProfileVoiceDictsPath(), synthName, voiceName))
