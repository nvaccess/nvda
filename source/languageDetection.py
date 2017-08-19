#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 Dinesh Kaushal, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.



"""Handles detection of languages in Unicode text.
"""

import speech
from speech import SpeechCommand
from speech import LangChangeCommand
import languageHandler
import config
from unicodeScriptData import scriptCode
from collections import OrderedDict
from logHandler import log
import unicodedata

# maintains list of priority languages as a list of languageID, ScriptName, and LanguageDescription
languagePriorityListSpec = []

scriptIDToLangID = {}

def initialize():
	#reverse of langIDToScriptID, required to obtain language id for a specific script 
	for languageID in langIDToScriptID:
		langIDToScriptID[languageID] = (langIDToScriptID[languageID] + ('Number',)) if isinstance(langIDToScriptID[languageID], tuple) else (langIDToScriptID[languageID], 'Number')
		#log.debugWarning("script name: {} data type: {}".format( langIDToScriptID[languageID] , type( langIDToScriptID[languageID]) ) )
		if(isinstance(langIDToScriptID[languageID] ,tuple ) ):
			for scriptName in langIDToScriptID[languageID]: 
				if not (scriptName in scriptIDToLangID): scriptIDToLangID[ scriptName ] =  languageID 
		else:
			if not (langIDToScriptID[languageID] in scriptIDToLangID):
				scriptIDToLangID[ langIDToScriptID[languageID] ] =  languageID 
	# following 2 loops are only for log, they should be removed before final code
	for languageID in langIDToScriptID:
		log.debugWarning("script name: {} for language {}".format( langIDToScriptID[languageID] , languageID ) )
	for scriptName in scriptIDToLangID:
		log.debugWarning("language code: {} for script {}".format( scriptIDToLangID[ scriptName ] , scriptName ) ) 	
	updateLanguagePriorityFromConfig()

def updateLanguagePriorityFromConfig():
	"""read string from config and convert it to list"""
	global languagePriorityListSpec 
	tempList = []
	try:
		languageList = config.conf["languageDetection"]["preferredLanguages"]
		for language in languageList: 
			tempList.append( [ language , getScriptIDFromLangID(language) , getLanguageDescription( language ) ]) 
		languagePriorityListSpec = tempList 
	except KeyError:
		pass

langIDToScriptID = OrderedDict([
	("en" , "Latin"),
	("af_ZA" , "Latin"),
	("ca" , "Latin"),
	("cs" , "Latin"),
	("da" , "Latin"),
	("de" , "Latin"),
	("el" , "Latin"),
	("es" , "Latin"),
	("fr" , "Latin"),
	("am" , "Armenian"),
	("ar" , "Arabic"),
	("as" , "Bengali"),
	("bg" , "Cyrillic"),
	("bn" , "Bengali"),
	("gu" , "Gujarati"),
	("kn" , "Kannada"),
	("ml" , "Malayalam"),
	("mn" , "Mongolian"),
	("hi" , "Devanagari"),
	("mr" , "Devanagari"),
	("ne" , "Devanagari"),
	("sa" , "Devanagari"),
	("or" , "Oriya"),
	("pa" , "Gurmukhi"),
	("sq" , "Caucasian_Albanian"),
	("ta" , "Tamil"),
	("te" , "Telugu"),
	("ja" , ("Han", "Hiragana", "Katakana", "FullWidthNumber")), 
	("zh" , ("Han", "Hiragana", "Katakana")), 
])

def getLanguagesWithDescriptions(ignoreLanguages=None):
	"""generates a list of locale names, plus their full localized language and country names.
	@rtype: list of tuples
	"""
	#Make a list of all the languages found for language to script mapping
	allLanguages  = langIDToScriptID.keys()
	allLanguages.sort()
	languageDescriptions = []
	if ignoreLanguages is None:
		ignoreLanguages = {lang[0] for lang in languagePriorityListSpec}
	for language in allLanguages:  
		if language in ignoreLanguages: 
			continue
		else:
			desc=languageHandler.getLanguageDescription(language )
			label="%s, %s"%(desc,language ) if desc else language 
			languageDescriptions.append((language , label))
	return languageDescriptions

def getScriptCode(chr):
	"""performs a binary search in scripCodes for unicode ranges
	@param chr: character for which a script should be found
	@type chr: string
	@return: script code
	@rtype: int"""
	mStart = 0
	mEnd = len(scriptCode)-1
	characterUnicodeCode = ord(chr)
	# Number should respect preferred language setting
	# FullWidthNumber is in Common category, however, it indicates Japanese language context
	if 0x30 <= characterUnicodeCode <= 0x39:
		return "Number"
	elif 0xff10 <= characterUnicodeCode <= 0xff19:
		return "FullWidthNumber"
	while( mEnd >= mStart ):
		midPoint = (mStart + mEnd ) >> 1
		if characterUnicodeCode < scriptCode[midPoint][0]: 
			mEnd = midPoint -1
		elif characterUnicodeCode > scriptCode[midPoint][1]: 
			mStart = midPoint + 1
		else:
			return scriptCode[midPoint][2] 
	return None

def getLangID(scriptName ):
	"""This function is the heart of determining which language is selected for a script
	@param scriptName: the unicode name of the  script
	@type scriptName: string
	@return: It returns languageID for a script. it first checks whether there is a language for the script in the languagePriorityListSpec. If not, then it checks whether default language script is same as the script. At last it returns languageID for the script from scriptIDToLangID.
	@rtype: string"""
	# we are using loop during search to maintain priority
	for priorityLanguage, priorityScript, priorityDescription in  languagePriorityListSpec:
		log.debugWarning(u"priorityLanguage {}, priorityScript {}, priorityDescription {}".format(priorityLanguage, priorityScript, priorityDescription )  )
		if scriptName in priorityScript: 
			return priorityLanguage
	#language not found in the languagePriorityListSpec, so check if default language can be applied for the script
	if scriptName == getScriptIDFromLangID(languageHandler.getLanguage() ):
		return  languageHandler.getLanguage()
	# default language is not applicable for this script, so look up in the scriptIDToLangID
	return scriptIDToLangID.get (scriptName )

def getLanguageDescription(language ):
	desc=languageHandler.getLanguageDescription(language )
	label="%s, %s"%(desc,language ) if desc else language 
	return label

def getScriptIDFromLangID(langID ):
	# Strip the dialect (if any).
	return langIDToScriptID.get (langID.split("_", 1)[0])

class ScriptChangeCommand(SpeechCommand):
	"""A command to switch the script during script detection ."""

	def __init__(self, scriptCode):
		"""
		@param scriptCode: the script identifier
		@type scriptCode: int
		"""
		self.scriptCode =scriptCode 

	def __repr__(self):
		return "ScriptChangeCommand (%r)"%self.scriptCode

def detectScript(text):
	"""splits a string if there are multiple scripts in it
	@param text: the text string
	@type string
	@return: sequence of script commands and text
	@rtype: list"""
	unicodeSequence = []
	outerScripts  = []
	currentScript = getScriptCode(  text[0])
	oldScript = currentScript
	unicodeSequence.append(ScriptChangeCommand(currentScript)) 
	beginIndex = 0
	for index in xrange( len(text) ) :
		currentScript = getScriptCode( text[index] ) 
		# handling script property for paired punctuation: see UAX 24 section 5.1
		if unicodedata.category(text[index] ) == "Ps":
			outerScripts.append(oldScript ) 
		elif unicodedata.category(text[index] ) == "Pe" and len(outerScripts) > 0:
			currentScript = outerScripts.pop()

		# don't change script for combining marks as per UAX 24 section 5.2
		if unicodedata.category(text[index] ) in ["Mn" , "Mc", "Me"]: 
			continue

		# don't change scripts for Common, inherited and Unknown characters 
		if currentScript in ["Common" , "Inherited", "Unknown"]: 
			continue

		if currentScript != oldScript:
			newText = text[beginIndex:index] 
			unicodeSequence.append( newText )
			beginIndex= index
			unicodeSequence.append(ScriptChangeCommand(currentScript)) 
		oldScript = currentScript

	unicodeSequence.append( text[beginIndex:] )
	return unicodeSequence

def detectLanguage(text, defaultLanguage =None):
	"""splits a string if there are multiple languages in it. uses detectScript
	@param text: the text string
	@type text: string
	@param defaultLanguage: The default language for NVDA 
	@type preferredLanguage: string or None
	@return: sequence of language commands and text
	@rtype: list"""
	sequenceWithLanguage= []
	tempSequence = detectScript(text)
	scriptCode = ""
	for item in tempSequence: 
		if isinstance(item,ScriptChangeCommand):
			scriptCode = item.scriptCode
		else:
			log.debugWarning(u"script: {} for text {} ".format( scriptCode , unicode(item) ) )

	if defaultLanguage:
		scriptIDForDefaultLanguage = getScriptIDFromLangID( defaultLanguage )
	else:
		scriptIDForDefaultLanguage = None

	previousLanguageCode = ""
	for index in xrange(len(tempSequence )):
		item= tempSequence [index]
		if isinstance(item,ScriptChangeCommand):
			# check if default language for a script is available, if yes, add that language instead of language from priority list
			if scriptIDForDefaultLanguage and (item.scriptCode in scriptIDForDefaultLanguage ):
				if index == 0: continue # if it is first item and same as the default language, language code is already added.
				languageCode = defaultLanguage 
			else:
				languageCode = getLangID( item.scriptCode  )  
			#end if scriptIDForPreferredLanguage and (item.scriptCode == scriptIDForPreferredLanguage):

			if languageCode:
				if (languageCode == previousLanguageCode) or ( ( previousLanguageCode == "") and  (languageCode == defaultLanguage ) ): continue # if 2 scripts have same language, we don't need to add additional language. 
				sequenceWithLanguage.append( LangChangeCommand( languageHandler.normalizeLanguage( languageCode ) ) )
				previousLanguageCode = languageCode 
			# end if languageCode
		else:
			if( len(sequenceWithLanguage) > 0) and ( not isinstance(sequenceWithLanguage[-1],LangChangeCommand) ): 
				sequenceWithLanguage[-1] = sequenceWithLanguage[-1] + item
			else:
				sequenceWithLanguage.append(item)	
			#end if( len(sequenceWithLanguage) > 0) and ( not isinstance(sequenceWithLanguage[-1],LangChangeCommand) ): 
		#end if isinstance(item,ScriptChangeCommand):
	#end for index in xrange(len(tempSequence )):

	tempLanguageCode = ""
	for item in sequenceWithLanguage: 
		if isinstance(item,LangChangeCommand):
			tempLanguageCode = item.lang
		else:
			log.debugWarning(u"language: {} for text {} ".format( tempLanguageCode , unicode(item) ) )
	log.debugWarning("number of items in script list: {}, number of items in language list: {} preferredLanguage: {}".format(len(tempSequence ) , len(sequenceWithLanguage) , defaultLanguage ) )
	return sequenceWithLanguage
