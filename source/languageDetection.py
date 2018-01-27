#languageDetection.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Dinesh Kaushal

"""Handles detection of languages in Unicode text.
"""

from speech import SpeechCommand
from speech import LangChangeCommand
import languageHandler
import config
from unicodeScriptData import scriptCode
from collections import OrderedDict
from collections import namedtuple
import unicodedata

# unicode digit constants
DIGIT_ZERO = 0x30
DIGIT_NINE = 0x39
FULLWIDTH_ZERO = 0xFF10
FULLWIDTH_NINE = 0xFF19

# maintains list of priority languages as a list of languageID, ScriptName, and LanguageDescription
languagePriorityListSpec = []

scriptIDToLangID = {}

LanguageDescription = namedtuple("LanguageDescription" , "languageID description")
LanguageScriptDescription = namedtuple("LanguageScriptDescription" , "languageID scriptID description")

def initialize():
	#reverse of langIDToScriptID, required to obtain language id for a specific script 
	for languageID in langIDToScriptID:
		# Since every entry in langIDToScriptID is a tuple of scripts, we need to iterate all 
		for scriptName in langIDToScriptID[languageID]: 
			if not (scriptName in scriptIDToLangID): scriptIDToLangID[ scriptName ] =  languageID 
	updateLanguagePriorityFromConfig()

def updateLanguagePriorityFromConfig():
	"""read string from config and convert it to list"""
	global languagePriorityListSpec 
	tempList = []
	try:
		languageList = config.conf["languageDetection"]["preferredLanguages"]
		for language in languageList: 
			tempList.append( LanguageScriptDescription(languageID   = language , scriptID = getScriptIDFromLangID(language) , description = getLanguageDescription( language ) )) 
		languagePriorityListSpec = tempList 
	except KeyError:
		pass

langIDToScriptID = OrderedDict([
	("en" , ("Latin", "Number" ) ),
	("af_ZA" , ( "Latin", "Number" ) ),
	("ca" , ( "Latin", "Number" ) ),
	("cs" , ( "Latin" , "Number" ) ),
	("da" , ( "Latin" , "Number" ) ),
	("de" , ( "Latin" , "Number" ) ),
	("el" , ("Latin" , "Greek" , "Number" ) ),
	("es" , ( "Latin" , "Number" ) ),
	("fi" , ( "Latin" , "Number" ) ),
	("fr" , ( "Latin" , "Number" ) ),
	("ga" , ( "Latin" , "Number" ) ),
	("gl" , ( "Latin" , "Number" ) ),
	("hr" , ( "Latin" , "Number" ) ),
	("nl" , ( "Latin" , "Number" ) ),
	("pl" , ( "Latin" , "Number" ) ),
	("pt_br" , ( "Latin" , "Number" ) ),
	("sl" , ( "Latin" , "Number" ) ),
	("am" , ( "Armenian" , "Number" ) ),
	("ar" , ( "Arabic" , "Number" ) ),
	("as" , ( "Bengali" , "Number" ) ),
	("bg" , ( "Cyrillic" , "Number" ) ),
	("bn" , ( "Bengali" , "Number" ) ),
	("fa" , ( "Arabic" , "Number" ) ),
	("gu" , ( "Gujarati" , "Number" ) ),
	("ka" , ( "Georgian" , "Number" ) ),
	("kn" , ( "Kannada" , "Number" ) ),
	("mk" , ( "Cyrillic" , "Number" ) ),
	("ml" , ( "Malayalam" , "Number" ) ),
	("mn" , ( "Mongolian" , "Number" ) ),
	("he" , ( "Hebrew" , "Number" ) ),
	("hi" , ( "Devanagari" , "Number" ) ),
	("mr" , ( "Devanagari" , "Number" ) ),
	("ne" , ( "Devanagari" , "Number" ) ),
	("sa" , ( "Devanagari" , "Number" ) ),
	("or" , ( "Oriya" , "Number" ) ),
	("pa" , ( "Gurmukhi" , "Number" ) ),
	("ru" , ( "Cyrillic" , "Number" ) ),
	("sq" , ( "Caucasian_Albanian" , "Number" ) ),
	("ta" , ( "Tamil" , "Number" ) ),
	("te" , ( "Telugu" , "Number" ) ),
	("sr" , ("Latin" , "Cyrillic" , "Number" ) ),
	("ja" , ("Han", "Hiragana", "Katakana", "FullWidthNumber" , "Number" ) ), 
	("ko" , ("Han", "Hiragana", "Katakana", "Hangul" , "FullWidthNumber" , "Number" ) ), 
	("zh" , ("Han", "Hiragana", "Katakana", "FullWidthNumber"  , "Number" ) ), 
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
		ignoreLanguages = {lang.languageID for lang in languagePriorityListSpec}
	for language in allLanguages:  
		if language in ignoreLanguages: 
			continue
		else:
			desc=languageHandler.getLanguageDescription(language )
			label="%s, %s"%(desc,language ) if desc else language 
			languageDescriptions.append( LanguageDescription(languageID= language , description = label))
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
	if DIGIT_ZERO  <= characterUnicodeCode <= DIGIT_NINE:
		return "Number"
	elif FULLWIDTH_ZERO <= characterUnicodeCode <= FULLWIDTH_NINE: 
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
	for priorityLanguage in  languagePriorityListSpec:
		if scriptName in priorityLanguage.scriptID:
			return priorityLanguage.languageID
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
	if config.conf["languageDetection"]["disableScriptDetection"]:  
		sequenceWithLanguage.append( text)
		return sequenceWithLanguage

	tempSequence = detectScript(text)
	scriptCode = ""

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

	return sequenceWithLanguage
