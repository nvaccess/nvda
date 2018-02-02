# -*- coding: UTF-8 -*-
#speech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2017 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Babbage B.V.

"""High-level functions to speak information.
""" 

import itertools
import weakref
import unicodedata
import time
import warnings
import colors
import globalVars
from logHandler import log
import api
import controlTypes
import config
import tones
import synthDriverHandler
from synthDriverHandler import *
import re
import textInfos
import queueHandler
import speechDictHandler
import characterProcessing
import languageHandler

speechMode_off=0
speechMode_beeps=1
speechMode_talk=2
#: How speech should be handled; one of speechMode_off, speechMode_beeps or speechMode_talk.
speechMode=speechMode_talk
speechMode_beeps_ms=15
beenCanceled=True
isPaused=False
curWordChars=[]

#Set containing locale codes for languages supporting conjunct characters
LANGS_WITH_CONJUNCT_CHARS = {'hi', 'as', 'bn', 'gu', 'kn', 'kok', 'ml', 'mni', 'mr', 'pa', 'te', 'ur', 'ta'}

#: The string used to separate distinct chunks of text when multiple chunks should be spoken without pauses.
# #555: Use two spaces so that numbers from adjacent chunks aren't treated as a single number
# for languages such as French and German which use space as a thousands separator.
CHUNK_SEPARATOR = "  "

oldTreeLevel=None
oldTableID=None
oldRowNumber=None
oldColumnNumber=None

def initialize():
	"""Loads and sets the synth driver configured in nvda.ini."""
	synthDriverHandler.initialize()
	setSynth(config.conf["speech"]["synth"])

def terminate():
	setSynth(None)
	speechViewerObj=None

#: If a chunk of text contains only these characters, it will be considered blank.
BLANK_CHUNK_CHARS = frozenset((" ", "\n", "\r", "\0", u"\xa0"))
def isBlank(text):
	"""Determine whether text should be reported as blank.
	@param text: The text in question.
	@type text: str
	@return: C{True} if the text is blank, C{False} if not.
	@rtype: bool
	"""
	return not text or set(text) <= BLANK_CHUNK_CHARS

RE_CONVERT_WHITESPACE = re.compile("[\0\r\n]")

def processText(locale,text,symbolLevel):
	text = speechDictHandler.processText(text)
	text = characterProcessing.processSpeechSymbols(locale, text, symbolLevel)
	text = RE_CONVERT_WHITESPACE.sub(u" ", text)
	return text.strip()

def getLastSpeechIndex():
	"""@deprecated: Use L{CallbackCommand} (or one of the other subclasses of L{BaseCallbackCommand}) instead.
	"""
	return None

def cancelSpeech():
	"""Interupts the synthesizer from currently speaking"""
	global beenCanceled, isPaused
	# Import only for this function to avoid circular import.
	import sayAllHandler
	sayAllHandler.stop()
	speakWithoutPauses._pendingSpeechSequence=[]
	speakWithoutPauses._lastSentIndex=None
	if beenCanceled:
		return
	elif speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		return
	_manager.cancel()
	beenCanceled=True
	isPaused=False

def pauseSpeech(switch):
	global isPaused, beenCanceled
	getSynth().pause(switch)
	isPaused=switch
	beenCanceled=False

def speakMessage(text):
	"""Speaks a given message.
@param text: the message to speak
@type text: string
"""
	speakText(text,reason=controlTypes.REASON_MESSAGE)

def getCurrentLanguage():
	synth=getSynth()
	language=None
	if  synth:
		try:
			language=synth.language if config.conf['speech']['trustVoiceLanguage'] else None
		except NotImplementedError:
			pass
	if language:
		language=languageHandler.normalizeLanguage(language)
	if not language:
		language=languageHandler.getLanguage()
	return language

def spellTextInfo(info,useCharacterDescriptions=False):
	"""Spells the text from the given TextInfo, honouring any LangChangeCommand objects it finds if autoLanguageSwitching is enabled."""
	if not config.conf['speech']['autoLanguageSwitching']:
		speakSpelling(info.text,useCharacterDescriptions=useCharacterDescriptions)
		return
	curLanguage=None
	for field in info.getTextWithFields({}):
		if isinstance(field,basestring):
			speakSpelling(field,curLanguage,useCharacterDescriptions=useCharacterDescriptions)
		elif isinstance(field,textInfos.FieldCommand) and field.command=="formatChange":
			curLanguage=field.field.get('language')

def shouldUseCompatCodeForIndexing():
	synth = getSynth()
	if synthDriverHandler.synthIndexReached in synth.supportedNotifications:
		return False
	warnings.warn(DeprecationWarning(
		"Synth %s does not support synthIndexReached notifications. "
		"Using old speech code (which will be removed in future)."
		% synth.name))
	return True

def speakSpelling(text, locale=None, useCharacterDescriptions=False):
	if shouldUseCompatCodeForIndexing():
		# Import late to avoid circular import.
		import speechCompat
		return speechCompat.speakSpelling(text, locale=locale, useCharacterDescriptions=useCharacterDescriptions)
	seq = list(getSpeechForSpelling(text, locale=locale, useCharacterDescriptions=useCharacterDescriptions))
	speak(seq)

def getSpeechForSpelling(text, locale=None, useCharacterDescriptions=False):
	defaultLanguage=getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		yield _("blank")
		return
	if not text.isspace():
		text=text.rstrip()

	synth = getSynth()
	synthConfig=config.conf["speech"][synth.name]
	charMode = False
	textLength=len(text)
	count = 0
	localeHasConjuncts = True if locale.split('_',1)[0] in LANGS_WITH_CONJUNCT_CHARS else False
	charDescList = getCharDescListFromText(text,locale) if localeHasConjuncts else text
	for item in charDescList:
		if localeHasConjuncts:
			# item is a tuple containing character and its description
			char = item[0]
			charDesc = item[1]
		else:
			# item is just a character.
			char = item
			if useCharacterDescriptions:
				charDesc=characterProcessing.getCharacterDescription(locale,char.lower())
		uppercase=char.isupper()
		if useCharacterDescriptions and charDesc:
			char=charDesc[0] if textLength>1 else u"\u3001".join(charDesc)
		else:
			char=characterProcessing.processSpeechSymbol(locale,char)
		if uppercase and synthConfig["sayCapForCapitals"]:
			# Translators: cap will be spoken before the given letter when it is capitalized.
			char=_("cap %s")%char
		if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
			yield PitchCommand(offset=synthConfig["capPitchChange"])
		if config.conf['speech']['autoLanguageSwitching']:
			yield LangChangeCommand(locale)
		if len(char) == 1 and synthConfig["useSpellingFunctionality"]:
			if not charMode:
				yield CharacterModeCommand(True)
				charMode = True
		elif charMode:
			yield CharacterModeCommand(False)
			charMode = False
		if uppercase and  synthConfig["beepForCapitals"]:
			yield BeepCommand(2000, 50)
		yield char
		if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
			yield PitchCommand()
		yield EndUtteranceCommand()

def getCharDescListFromText(text,locale):
	"""This method prepares a list, which contains character and its description for all characters the text is made up of, by checking the presence of character descriptions in characterDescriptions.dic of that locale for all possible combination of consecutive characters in the text.
	This is done to take care of conjunct characters present in several languages such as Hindi, Urdu, etc.
	"""
	charDescList = []
	charDesc=None
	i = len(text)
	while i:
		subText = text[:i]
		charDesc = characterProcessing.getCharacterDescription(locale,subText)
		if charDesc or i==1:
			if not charDesc:
				# #5375: We're down to a single character (i == 1) and we don't have a description.
				# Try converting to lower case.
				# This provides for upper case English characters (which only have lower case descriptions).
				charDesc = characterProcessing.getCharacterDescription(locale,subText.lower())
			charDescList.append((subText,charDesc))
			text = text[i:]
			i = len(text)
		else:
			i = i - 1
	return charDescList

def speakObjectProperties(obj, reason=controlTypes.REASON_QUERY, _prefixSpeechCommand=None, **allowedProperties):
	#Fetch the values for all wanted properties
	newPropertyValues={}
	positionInfo=None
	for name,value in allowedProperties.iteritems():
		if name=="includeTableCellCoords":
			# This is verbosity info.
			newPropertyValues[name]=value
		elif name.startswith('positionInfo_') and value:
			if positionInfo is None:
				positionInfo=obj.positionInfo
		elif value:
			try:
				newPropertyValues[name]=getattr(obj,name)
			except NotImplementedError:
				pass
	if positionInfo:
		if allowedProperties.get('positionInfo_level',False) and 'level' in positionInfo:
			newPropertyValues['positionInfo_level']=positionInfo['level']
		if allowedProperties.get('positionInfo_indexInGroup',False) and 'indexInGroup' in positionInfo:
			newPropertyValues['positionInfo_indexInGroup']=positionInfo['indexInGroup']
		if allowedProperties.get('positionInfo_similarItemsInGroup',False) and 'similarItemsInGroup' in positionInfo:
			newPropertyValues['positionInfo_similarItemsInGroup']=positionInfo['similarItemsInGroup']
	#Fetched the cached properties and update them with the new ones
	oldCachedPropertyValues=getattr(obj,'_speakObjectPropertiesCache',{}).copy()
	cachedPropertyValues=oldCachedPropertyValues.copy()
	cachedPropertyValues.update(newPropertyValues)
	obj._speakObjectPropertiesCache=cachedPropertyValues
	#If we should only cache we can stop here
	if reason==controlTypes.REASON_ONLYCACHE:
		return
	#If only speaking change, then filter out all values that havn't changed
	if reason==controlTypes.REASON_CHANGE:
		for name in set(newPropertyValues)&set(oldCachedPropertyValues):
			if newPropertyValues[name]==oldCachedPropertyValues[name]:
				del newPropertyValues[name]
			elif name=="states": #states need specific handling
				oldStates=oldCachedPropertyValues[name]
				newStates=newPropertyValues[name]
				newPropertyValues['states']=newStates-oldStates
				newPropertyValues['negativeStates']=oldStates-newStates
	#properties such as states need to know the role to speak properly, give it as a _ name
	newPropertyValues['_role']=newPropertyValues.get('role',obj.role)
	# The real states are needed also, as the states entry might be filtered.
	newPropertyValues['_states']=obj.states
	if "rowNumber" in newPropertyValues or "columnNumber" in newPropertyValues:
		# We're reporting table cell info, so pass the table ID.
		try:
			newPropertyValues["_tableID"]=obj.tableID
		except NotImplementedError:
			pass
	newPropertyValues['current']=obj.isCurrent
	if allowedProperties.get('placeholder', False):
		newPropertyValues['placeholder']=obj.placeholder
	#Get the speech text for the properties we want to speak, and then speak it
	text=getSpeechTextForProperties(reason,**newPropertyValues)
	if text:
		speechSequence = []
		if _prefixSpeechCommand is not None:
			speechSequence.append(_prefixSpeechCommand)
		speechSequence.append(text)
		speak(speechSequence)

def _speakPlaceholderIfEmpty(info, obj, reason):
	""" attempt to speak placeholder attribute if the textInfo 'info' is empty
	@return: True if info was considered empty, and we attempted to speak the placeholder value.
	False if info was not considered empty.
	"""
	textEmpty = obj._isTextEmpty
	if textEmpty:
		speakObjectProperties(obj,reason=reason,placeholder=True)
		return True
	return False

def speakObject(obj, reason=controlTypes.REASON_QUERY, _prefixSpeechCommand=None):
	from NVDAObjects import NVDAObjectTextInfo
	role=obj.role
	# Choose when we should report the content of this object's textInfo, rather than just the object's value
	import browseMode
	shouldReportTextContent=not (
		# focusEntered should never present text content
		(reason==controlTypes.REASON_FOCUSENTERED) or
		# The rootNVDAObject of a browseMode document in browse mode (not passThrough) should never present text content
		(isinstance(obj.treeInterceptor,browseMode.BrowseModeDocumentTreeInterceptor) and not obj.treeInterceptor.passThrough and obj==obj.treeInterceptor.rootNVDAObject) or
		# objects that do not report as having navigableText should not report their text content either
		not obj._hasNavigableText
	)
	allowProperties={'name':True,'role':True,'roleText':True,'states':True,'value':True,'description':True,'keyboardShortcut':True,'positionInfo_level':True,'positionInfo_indexInGroup':True,'positionInfo_similarItemsInGroup':True,"cellCoordsText":True,"rowNumber":True,"columnNumber":True,"includeTableCellCoords":True,"columnCount":True,"rowCount":True,"rowHeaderText":True,"columnHeaderText":True}

	if reason==controlTypes.REASON_FOCUSENTERED:
		allowProperties["value"]=False
		allowProperties["keyboardShortcut"]=False
		allowProperties["positionInfo_level"]=False
		# Aside from excluding some properties, focus entered should be spoken like focus.
		reason=controlTypes.REASON_FOCUS

	if not config.conf["presentation"]["reportObjectDescriptions"]:
		allowProperties["description"]=False
	if not config.conf["presentation"]["reportKeyboardShortcuts"]:
		allowProperties["keyboardShortcut"]=False
	if not config.conf["presentation"]["reportObjectPositionInformation"]:
		allowProperties["positionInfo_level"]=False
		allowProperties["positionInfo_indexInGroup"]=False
		allowProperties["positionInfo_similarItemsInGroup"]=False
	if reason!=controlTypes.REASON_QUERY:
		allowProperties["rowCount"]=False
		allowProperties["columnCount"]=False
	formatConf=config.conf["documentFormatting"]
	if not formatConf["reportTableCellCoords"]:
		allowProperties["cellCoordsText"]=False
		# rowNumber and columnNumber might be needed even if we're not reporting coordinates.
		allowProperties["includeTableCellCoords"]=False
	if not formatConf["reportTableHeaders"]:
		allowProperties["rowHeaderText"]=False
		allowProperties["columnHeaderText"]=False
	if (not formatConf["reportTables"]
			or (not formatConf["reportTableCellCoords"] and not formatConf["reportTableHeaders"])):
		# We definitely aren't reporting any table info at all.
		allowProperties["rowNumber"]=False
		allowProperties["columnNumber"]=False
	if shouldReportTextContent:
		allowProperties['value']=False

	speakObjectProperties(obj, reason=reason, _prefixSpeechCommand=_prefixSpeechCommand, **allowProperties)
	if reason==controlTypes.REASON_ONLYCACHE:
		return
	if shouldReportTextContent:
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
			if not info.isCollapsed:
				# if there is selected text, then there is a value and we do not report placeholder
				# Translators: This is spoken to indicate what has been selected. for example 'selected hello world'
				speakSelectionMessage(_("selected %s"),info.text)
			else:
				info.expand(textInfos.UNIT_LINE)
				_speakPlaceholderIfEmpty(info, obj, reason)
				speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		except:
			newInfo=obj.makeTextInfo(textInfos.POSITION_ALL)
			if not _speakPlaceholderIfEmpty(newInfo, obj, reason):
				speakTextInfo(newInfo,unit=textInfos.UNIT_PARAGRAPH,reason=controlTypes.REASON_CARET)
	elif role==controlTypes.ROLE_MATH:
		import mathPres
		mathPres.ensureInit()
		if mathPres.speechProvider:
			try:
				speak(mathPres.speechProvider.getSpeechForMathMl(obj.mathMl))
			except (NotImplementedError, LookupError):
				pass

def speakText(text,reason=controlTypes.REASON_MESSAGE,symbolLevel=None):
	"""Speaks some text.
	@param text: The text to speak.
	@type text: str
	@param reason: The reason for this speech; one of the controlTypes.REASON_* constants.
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
	"""
	if text is None:
		return
	if isBlank(text):
		# Translators: This is spoken when the line is considered blank.
		text=_("blank")
	speak([text],symbolLevel=symbolLevel)

RE_INDENTATION_SPLIT = re.compile(r"^([^\S\r\n\f\v]*)(.*)$", re.UNICODE | re.DOTALL)
def splitTextIndentation(text):
	"""Splits indentation from the rest of the text.
	@param text: The text to split.
	@type text: basestring
	@return: Tuple of indentation and content.
	@rtype: (basestring, basestring)
	"""
	return RE_INDENTATION_SPLIT.match(text).groups()

RE_INDENTATION_CONVERT = re.compile(r"(?P<char>\s)(?P=char)*", re.UNICODE)
IDT_BASE_FREQUENCY = 220 #One octave below middle A.
IDT_TONE_DURATION = 80 #Milleseconds
IDT_MAX_SPACES = 72
def getIndentationSpeech(indentation, formatConfig):
	"""Retrieves the phrase to be spoken for a given string of indentation.
	@param indentation: The string of indentation.
	@type indentation: unicode
	@param formatConfig: The configuration to use.
	@type formatConfig: dict
	@return: The phrase to be spoken.
	@rtype: unicode
	"""
	speechIndentConfig = formatConfig["reportLineIndentation"]
	toneIndentConfig = formatConfig["reportLineIndentationWithTones"] and speechMode == speechMode_talk
	if not indentation:
		if toneIndentConfig:
			tones.beep(IDT_BASE_FREQUENCY, IDT_TONE_DURATION)
		# Translators: This is spoken when the given line has no indentation.
		return (_("no indent") if speechIndentConfig else "")

	#The non-breaking space is semantically a space, so we replace it here.
	indentation = indentation.replace(u"\xa0", u" ")
	res = []
	locale=languageHandler.getLanguage()
	quarterTones = 0
	for m in RE_INDENTATION_CONVERT.finditer(indentation):
		raw = m.group()
		symbol = characterProcessing.processSpeechSymbol(locale, raw[0])
		count = len(raw)
		if symbol == raw[0]:
			# There is no replacement for this character, so do nothing.
			res.append(raw)
		elif count == 1:
			res.append(symbol)
		else:
			res.append(u"{count} {symbol}".format(count=count, symbol=symbol))
		quarterTones += (count*4 if raw[0]== "\t" else count)

	speak = speechIndentConfig
	if toneIndentConfig: 
		if quarterTones <= IDT_MAX_SPACES:
			#Remove me during speech refactor.
			pitch = IDT_BASE_FREQUENCY*2**(quarterTones/24.0) #24 quarter tones per octave.
			tones.beep(pitch, IDT_TONE_DURATION)
		else: 
			#we have more than 72 spaces (18 tabs), and must speak it since we don't want to hurt the users ears.
			speak = True
	return (" ".join(res) if speak else "")

# Speech priorities.
#: Indicates that a speech sequence should have normal priority.
SPRI_NORMAL = 0
#: Indicates that a speech sequence should be spoken after the next utterance of lower priority is complete.
SPRI_NEXT = 1
#: Indicates that a speech sequence is very important and should be spoken right now,
#: interrupting low priority speech.
#: After it is spoken, interrupted speech will resume.
#: Note that this does not interrupt previously queued speech at the same priority.
SPRI_NOW = 2
#: The speech priorities ordered from highest to lowest.
SPEECH_PRIORITIES = (SPRI_NOW, SPRI_NEXT, SPRI_NORMAL)

def speak(speechSequence, symbolLevel=None, priority=SPRI_NORMAL):
	"""Speaks a sequence of text and speech commands
	@param speechSequence: the sequence of text and L{SpeechCommand} objects to speak
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
	@param priority: The speech priority.
	@type priority: One of the C{SPRI_*} constants.
	"""
	if not speechSequence: #Pointless - nothing to speak 
		return
	import speechViewer
	if speechViewer.isActive:
		for item in speechSequence:
			if isinstance(item,basestring):
				speechViewer.appendText(item)
	global beenCanceled, curWordChars
	curWordChars=[]
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	#Filter out redundant LangChangeCommand objects 
	#And also fill in default values
	autoLanguageSwitching=config.conf['speech']['autoLanguageSwitching']
	autoDialectSwitching=config.conf['speech']['autoDialectSwitching']
	curLanguage=defaultLanguage=getCurrentLanguage()
	prevLanguage=None
	defaultLanguageRoot=defaultLanguage.split('_')[0]
	oldSpeechSequence=speechSequence
	speechSequence=[]
	for item in oldSpeechSequence:
		if isinstance(item,LangChangeCommand):
			if not autoLanguageSwitching: continue
			curLanguage=item.lang
			if not curLanguage or (not autoDialectSwitching and curLanguage.split('_')[0]==defaultLanguageRoot):
				curLanguage=defaultLanguage
		elif isinstance(item,basestring):
			if not item: continue
			if autoLanguageSwitching and curLanguage!=prevLanguage:
				speechSequence.append(LangChangeCommand(curLanguage))
				prevLanguage=curLanguage
			speechSequence.append(item)
		else:
			speechSequence.append(item)
	if not speechSequence:
		# After normalisation, the sequence is empty.
		# There's nothing to speak.
		return
	log.io("Speaking %r" % speechSequence)
	if symbolLevel is None:
		symbolLevel=config.conf["speech"]["symbolLevel"]
	curLanguage=defaultLanguage
	inCharacterMode=False
	for index in xrange(len(speechSequence)):
		item=speechSequence[index]
		if isinstance(item,CharacterModeCommand):
			inCharacterMode=item.state
		if autoLanguageSwitching and isinstance(item,LangChangeCommand):
			curLanguage=item.lang
		if isinstance(item,basestring):
			speechSequence[index]=processText(curLanguage,item,symbolLevel)
			if not inCharacterMode:
				speechSequence[index]+=CHUNK_SEPARATOR
	if shouldUseCompatCodeForIndexing():
		return getSynth().speak(speechSequence)
	_manager.speak(speechSequence, priority)

def speakSelectionMessage(message,text):
	if len(text) < 512:
		speakMessage(message % text)
	else:
		# Translators: This is spoken when the user has selected a large portion of text. Example output "1000 characters"
		speakMessage(message % _("%d characters") % len(text))

def speakSelectionChange(oldInfo,newInfo,speakSelected=True,speakUnselected=True,generalize=False):
	"""Speaks a change in selection, either selected or unselected text.
	@param oldInfo: a TextInfo instance representing what the selection was before
	@type oldInfo: L{textInfos.TextInfo}
	@param newInfo: a TextInfo instance representing what the selection is now
	@type newInfo: L{textInfos.TextInfo}
	@param generalize: if True, then this function knows that the text may have changed between the creation of the oldInfo and newInfo objects, meaning that changes need to be spoken more generally, rather than speaking the specific text, as the bounds may be all wrong.
	@type generalize: boolean
	"""
	selectedTextList=[]
	unselectedTextList=[]
	if newInfo.isCollapsed and oldInfo.isCollapsed:
		return
	startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
	startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
	endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
	endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
	if speakSelected and oldInfo.isCollapsed:
		selectedTextList.append(newInfo.text)
	elif speakUnselected and newInfo.isCollapsed:
		unselectedTextList.append(oldInfo.text)
	else:
		if startToEnd>0 or endToStart<0:
			if speakSelected and not newInfo.isCollapsed:
				selectedTextList.append(newInfo.text)
			if speakUnselected and not oldInfo.isCollapsed:
				unselectedTextList.append(oldInfo.text)
		else:
			if speakSelected and startToStart<0 and not newInfo.isCollapsed:
				tempInfo=newInfo.copy()
				tempInfo.setEndPoint(oldInfo,"endToStart")
				selectedTextList.append(tempInfo.text)
			if speakSelected and endToEnd>0 and not newInfo.isCollapsed:
				tempInfo=newInfo.copy()
				tempInfo.setEndPoint(oldInfo,"startToEnd")
				selectedTextList.append(tempInfo.text)
			if startToStart>0 and not oldInfo.isCollapsed:
				tempInfo=oldInfo.copy()
				tempInfo.setEndPoint(newInfo,"endToStart")
				unselectedTextList.append(tempInfo.text)
			if endToEnd<0 and not oldInfo.isCollapsed:
				tempInfo=oldInfo.copy()
				tempInfo.setEndPoint(newInfo,"startToEnd")
				unselectedTextList.append(tempInfo.text)
	locale=getCurrentLanguage()
	if speakSelected:
		if not generalize:
			for text in selectedTextList:
				if  len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				# Translators: This is spoken while the user is in the process of selecting something, For example: "hello selected"
				speakSelectionMessage(_("%s selected"),text)
		elif len(selectedTextList)>0:
			text=newInfo.text
			if len(text)==1:
				text=characterProcessing.processSpeechSymbol(locale,text)
			# Translators: This is spoken to indicate what has been selected. for example 'selected hello world'
			speakSelectionMessage(_("selected %s"),text)
	if speakUnselected:
		if not generalize:
			for text in unselectedTextList:
				if  len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				# Translators: This is spoken to indicate what has been unselected. for example 'hello unselected'
				speakSelectionMessage(_("%s unselected"),text)
		elif len(unselectedTextList)>0:
			if not newInfo.isCollapsed:
				text=newInfo.text
				if len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				# Translators: This is spoken to indicate when the previous selection was removed and a new selection was made. for example 'hello world selected instead'
				speakSelectionMessage(_("%s selected instead"),text)
			else:
				# Translators: Reported when selection is removed.
				speakMessage(_("selection removed"))

#: The number of typed characters for which to suppress speech.
_suppressSpeakTypedCharactersNumber = 0
#: The time at which suppressed typed characters were sent.
_suppressSpeakTypedCharactersTime = None
def _suppressSpeakTypedCharacters(number):
	"""Suppress speaking of typed characters.
	This should be used when sending a string of characters to the system
	and those characters should not be spoken individually as if the user were typing them.
	@param number: The number of characters to suppress.
	@type number: int
	"""
	global _suppressSpeakTypedCharactersNumber, _suppressSpeakTypedCharactersTime
	_suppressSpeakTypedCharactersNumber += number
	_suppressSpeakTypedCharactersTime = time.time()

#: The character to use when masking characters in protected fields.
PROTECTED_CHAR = "*"
#: The first character which is not a Unicode control character.
#: This is used to test whether a character should be spoken as a typed character;
#: i.e. it should have a visual or spatial representation.
FIRST_NONCONTROL_CHAR = u" "
def speakTypedCharacters(ch):
	global curWordChars
	typingIsProtected=api.isTypingProtected()
	if typingIsProtected:
		realChar=PROTECTED_CHAR
	else:
		realChar=ch
	if unicodedata.category(ch)[0] in "LMN":
		curWordChars.append(realChar)
	elif ch=="\b":
		# Backspace, so remove the last character from our buffer.
		del curWordChars[-1:]
	elif ch==u'\u007f':
		# delete character produced in some apps with control+backspace
		return
	elif len(curWordChars)>0:
		typedWord="".join(curWordChars)
		curWordChars=[]
		if log.isEnabledFor(log.IO):
			log.io("typed word: %s"%typedWord)
		if config.conf["keyboard"]["speakTypedWords"] and not typingIsProtected:
			speakText(typedWord)
	global _suppressSpeakTypedCharactersNumber, _suppressSpeakTypedCharactersTime
	if _suppressSpeakTypedCharactersNumber > 0:
		# We primarily suppress based on character count and still have characters to suppress.
		# However, we time out after a short while just in case.
		suppress = time.time() - _suppressSpeakTypedCharactersTime <= 0.1
		if suppress:
			_suppressSpeakTypedCharactersNumber -= 1
		else:
			_suppressSpeakTypedCharactersNumber = 0
			_suppressSpeakTypedCharactersTime = None
	else:
		suppress = False
	if not suppress and config.conf["keyboard"]["speakTypedCharacters"] and ch >= FIRST_NONCONTROL_CHAR:
		speakSpelling(realChar)

class SpeakTextInfoState(object):
	"""Caches the state of speakTextInfo such as the current controlField stack, current formatfield and indentation."""

	__slots__=[
		'objRef',
		'controlFieldStackCache',
		'formatFieldAttributesCache',
		'indentationCache',
	]

	def __init__(self,obj):
		if isinstance(obj,SpeakTextInfoState):
			oldState=obj
			self.objRef=oldState.objRef
		else:
			self.objRef=weakref.ref(obj)
			oldState=getattr(obj,'_speakTextInfoState',None)
		self.controlFieldStackCache=list(oldState.controlFieldStackCache) if oldState else []
		self.formatFieldAttributesCache=oldState.formatFieldAttributesCache if oldState else {}
		self.indentationCache=oldState.indentationCache if oldState else ""

	def updateObj(self):
		obj=self.objRef()
		if obj:
			obj._speakTextInfoState=self.copy()

	def copy(self):
		return self.__class__(self)

def _speakTextInfo_addMath(speechSequence, info, field):
	import mathPres
	mathPres.ensureInit()
	if not mathPres.speechProvider:
		return
	try:
		speechSequence.extend(mathPres.speechProvider.getSpeechForMathMl(info.getMathMl(field)))
	except (NotImplementedError, LookupError):
		return

def speakTextInfo(info, useCache=True, formatConfig=None, unit=None, reason=controlTypes.REASON_QUERY, _prefixSpeechCommand=None, onlyInitialFields=False, suppressBlanks=False):
	onlyCache=reason==controlTypes.REASON_ONLYCACHE
	if isinstance(useCache,SpeakTextInfoState):
		speakTextInfoState=useCache
	elif useCache:
		speakTextInfoState=SpeakTextInfoState(info.obj)
	else:
		speakTextInfoState=None
	autoLanguageSwitching=config.conf['speech']['autoLanguageSwitching']
	extraDetail=unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD)
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]
	if extraDetail:
		formatConfig=formatConfig.copy()
		formatConfig['extraDetail']=True
	reportIndentation=unit==textInfos.UNIT_LINE and ( formatConfig["reportLineIndentation"] or formatConfig["reportLineIndentationWithTones"])

	speechSequence=[]
	#Fetch the last controlFieldStack, or make a blank one
	controlFieldStackCache=speakTextInfoState.controlFieldStackCache if speakTextInfoState else []
	formatFieldAttributesCache=speakTextInfoState.formatFieldAttributesCache if speakTextInfoState else {}
	textWithFields=info.getTextWithFields(formatConfig)
	# We don't care about node bounds, especially when comparing fields.
	# Remove them.
	for command in textWithFields:
		if not isinstance(command,textInfos.FieldCommand):
			continue
		field=command.field
		if not field:
			continue
		try:
			del field["_startOfNode"]
		except KeyError:
			pass
		try:
			del field["_endOfNode"]
		except KeyError:
			pass

	#Make a new controlFieldStack and formatField from the textInfo's initialFields
	newControlFieldStack=[]
	newFormatField=textInfos.FormatField()
	initialFields=[]
	for field in textWithFields:
		if isinstance(field,textInfos.FieldCommand) and field.command in ("controlStart","formatChange"):
			initialFields.append(field.field)
		else:
			break
	if len(initialFields)>0:
		del textWithFields[0:len(initialFields)]
	endFieldCount=0
	for field in reversed(textWithFields):
		if isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd":
			endFieldCount+=1
		else:
			break
	if endFieldCount>0:
		del textWithFields[0-endFieldCount:]
	for field in initialFields:
		if isinstance(field,textInfos.ControlField):
			newControlFieldStack.append(field)
		elif isinstance(field,textInfos.FormatField):
			newFormatField.update(field)
		else:
			raise ValueError("unknown field: %s"%field)
	#Calculate how many fields in the old and new controlFieldStacks are the same
	commonFieldCount=0
	for count in xrange(min(len(newControlFieldStack),len(controlFieldStackCache))):
		# #2199: When comparing controlFields try using uniqueID if it exists before resorting to compairing the entire dictionary
		oldUniqueID=controlFieldStackCache[count].get('uniqueID')
		newUniqueID=newControlFieldStack[count].get('uniqueID')
		if ((oldUniqueID is not None or newUniqueID is not None) and newUniqueID==oldUniqueID) or (newControlFieldStack[count]==controlFieldStackCache[count]):
			commonFieldCount+=1
		else:
			break

	# #2591: Only if the reason is not focus, Speak the exit of any controlFields not in the new stack.
	# We don't do this for focus because hearing "out of list", etc. isn't useful when tabbing or using quick navigation and makes navigation less efficient.
	if reason!=controlTypes.REASON_FOCUS:
		endingBlock=False
		for count in reversed(xrange(commonFieldCount,len(controlFieldStackCache))):
			text=info.getControlFieldSpeech(controlFieldStackCache[count],controlFieldStackCache[0:count],"end_removedFromControlFieldStack",formatConfig,extraDetail,reason=reason)
			if text:
				speechSequence.append(text)
			if not endingBlock and reason==controlTypes.REASON_SAYALL:
				endingBlock=bool(int(controlFieldStackCache[count].get('isBlock',0)))
		if endingBlock:
			speechSequence.append(EndUtteranceCommand())
	# The TextInfo should be considered blank if we are only exiting fields (i.e. we aren't entering any new fields and there is no text).
	isTextBlank=True

	if _prefixSpeechCommand is not None:
		speechSequence.append(_prefixSpeechCommand)

	#Get speech text for any fields that are in both controlFieldStacks, if extra detail is not requested
	if not extraDetail:
		for count in xrange(commonFieldCount):
			field=newControlFieldStack[count]
			text=info.getControlFieldSpeech(field,newControlFieldStack[0:count],"start_inControlFieldStack",formatConfig,extraDetail,reason=reason)
			if text:
				speechSequence.append(text)
				isTextBlank=False
			if field.get("role")==controlTypes.ROLE_MATH:
				isTextBlank=False
				_speakTextInfo_addMath(speechSequence,info,field)

	#Get speech text for any fields in the new controlFieldStack that are not in the old controlFieldStack
	for count in xrange(commonFieldCount,len(newControlFieldStack)):
		field=newControlFieldStack[count]
		text=info.getControlFieldSpeech(field,newControlFieldStack[0:count],"start_addedToControlFieldStack",formatConfig,extraDetail,reason=reason)
		if text:
			speechSequence.append(text)
			isTextBlank=False
		if field.get("role")==controlTypes.ROLE_MATH:
			isTextBlank=False
			_speakTextInfo_addMath(speechSequence,info,field)
		commonFieldCount+=1

	#Fetch the text for format field attributes that have changed between what was previously cached, and this textInfo's initialFormatField.
	text=info.getFormatFieldSpeech(newFormatField,formatFieldAttributesCache,formatConfig,reason=reason,unit=unit,extraDetail=extraDetail,initialFormat=True)
	if text:
		speechSequence.append(text)
	if autoLanguageSwitching:
		language=newFormatField.get('language')
		speechSequence.append(LangChangeCommand(language))
		lastLanguage=language

	if onlyInitialFields or (unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD) and len(textWithFields)>0 and len(textWithFields[0])==1 and all((isinstance(x,textInfos.FieldCommand) and x.command=="controlEnd") for x in itertools.islice(textWithFields,1,None) )): 
		if not onlyCache:
			if onlyInitialFields or any(isinstance(x,basestring) for x in speechSequence):
				speak(speechSequence)
			if not onlyInitialFields: 
				speakSpelling(textWithFields[0],locale=language if autoLanguageSwitching else None)
		if useCache:
			speakTextInfoState.controlFieldStackCache=newControlFieldStack
			speakTextInfoState.formatFieldAttributesCache=formatFieldAttributesCache
			if not isinstance(useCache,SpeakTextInfoState):
				speakTextInfoState.updateObj()
		return

	#Move through the field commands, getting speech text for all controlStarts, controlEnds and formatChange commands
	#But also keep newControlFieldStack up to date as we will need it for the ends
	# Add any text to a separate list, as it must be handled differently.
	#Also make sure that LangChangeCommand objects are added before any controlField or formatField speech
	relativeSpeechSequence=[]
	inTextChunk=False
	allIndentation=""
	indentationDone=False
	for command in textWithFields:
		if isinstance(command,basestring):
			if reportIndentation and not indentationDone:
				indentation,command=splitTextIndentation(command)
				# Combine all indentation into one string for later processing.
				allIndentation+=indentation
				if command:
					# There was content after the indentation, so there is no more indentation.
					indentationDone=True
			if command:
				if inTextChunk:
					relativeSpeechSequence[-1]+=command
				else:
					relativeSpeechSequence.append(command)
					inTextChunk=True
		elif isinstance(command,textInfos.FieldCommand):
			newLanguage=None
			if  command.command=="controlStart":
				# Control fields always start a new chunk, even if they have no field text.
				inTextChunk=False
				fieldText=info.getControlFieldSpeech(command.field,newControlFieldStack,"start_relative",formatConfig,extraDetail,reason=reason)
				newControlFieldStack.append(command.field)
			elif command.command=="controlEnd":
				# Control fields always start a new chunk, even if they have no field text.
				inTextChunk=False
				fieldText=info.getControlFieldSpeech(newControlFieldStack[-1],newControlFieldStack[0:-1],"end_relative",formatConfig,extraDetail,reason=reason)
				del newControlFieldStack[-1]
				if commonFieldCount>len(newControlFieldStack):
					commonFieldCount=len(newControlFieldStack)
			elif command.command=="formatChange":
				fieldText=info.getFormatFieldSpeech(command.field,formatFieldAttributesCache,formatConfig,reason=reason,unit=unit,extraDetail=extraDetail)
				if fieldText:
					inTextChunk=False
				if autoLanguageSwitching:
					newLanguage=command.field.get('language')
					if lastLanguage!=newLanguage:
						# The language has changed, so this starts a new text chunk.
						inTextChunk=False
			if not inTextChunk:
				if fieldText:
					if autoLanguageSwitching and lastLanguage is not None:
						# Fields must be spoken in the default language.
						relativeSpeechSequence.append(LangChangeCommand(None))
						lastLanguage=None
					relativeSpeechSequence.append(fieldText)
				if command.command=="controlStart" and command.field.get("role")==controlTypes.ROLE_MATH:
					_speakTextInfo_addMath(relativeSpeechSequence,info,command.field)
				if autoLanguageSwitching and newLanguage!=lastLanguage:
					relativeSpeechSequence.append(LangChangeCommand(newLanguage))
					lastLanguage=newLanguage
	if reportIndentation and speakTextInfoState and allIndentation!=speakTextInfoState.indentationCache:
		indentationSpeech=getIndentationSpeech(allIndentation, formatConfig)
		if autoLanguageSwitching and speechSequence[-1].lang is not None:
			# Indentation must be spoken in the default language,
			# but the initial format field specified a different language.
			# Insert the indentation before the LangChangeCommand.
			speechSequence.insert(-1, indentationSpeech)
		else:
			speechSequence.append(indentationSpeech)
		if speakTextInfoState: speakTextInfoState.indentationCache=allIndentation
	# Don't add this text if it is blank.
	relativeBlank=True
	for x in relativeSpeechSequence:
		if isinstance(x,basestring) and not isBlank(x):
			relativeBlank=False
			break
	if not relativeBlank:
		speechSequence.extend(relativeSpeechSequence)
		isTextBlank=False

	#Finally get speech text for any fields left in new controlFieldStack that are common with the old controlFieldStack (for closing), if extra detail is not requested
	if autoLanguageSwitching and lastLanguage is not None:
		speechSequence.append(LangChangeCommand(None))
		lastLanguage=None
	if not extraDetail:
		for count in reversed(xrange(min(len(newControlFieldStack),commonFieldCount))):
			text=info.getControlFieldSpeech(newControlFieldStack[count],newControlFieldStack[0:count],"end_inControlFieldStack",formatConfig,extraDetail,reason=reason)
			if text:
				speechSequence.append(text)
				isTextBlank=False

	# If there is nothing  that should cause the TextInfo to be considered non-blank, blank should be reported, unless we are doing a say all.
	if not suppressBlanks and reason != controlTypes.REASON_SAYALL and isTextBlank:
		# Translators: This is spoken when the line is considered blank.
		speechSequence.append(_("blank"))

	#Cache a copy of the new controlFieldStack for future use
	if useCache:
		speakTextInfoState.controlFieldStackCache=list(newControlFieldStack)
		speakTextInfoState.formatFieldAttributesCache=formatFieldAttributesCache
		if not isinstance(useCache,SpeakTextInfoState):
			speakTextInfoState.updateObj()

	if not onlyCache and speechSequence:
		if reason==controlTypes.REASON_SAYALL:
			return speakWithoutPauses(speechSequence)
		else:
			speak(speechSequence)
			return True

def getSpeechTextForProperties(reason=controlTypes.REASON_QUERY,**propertyValues):
	global oldTreeLevel, oldTableID, oldRowNumber, oldColumnNumber
	textList=[]
	name=propertyValues.get('name')
	if name:
		textList.append(name)
	if 'role' in propertyValues:
		role=propertyValues['role']
		speakRole=True
	elif '_role' in propertyValues:
		speakRole=False
		role=propertyValues['_role']
	else:
		speakRole=False
		role=controlTypes.ROLE_UNKNOWN
	value=propertyValues.get('value') if role not in controlTypes.silentValuesForRoles else None
	cellCoordsText=propertyValues.get('cellCoordsText')
	rowNumber=propertyValues.get('rowNumber')
	columnNumber=propertyValues.get('columnNumber')
	includeTableCellCoords=propertyValues.get('includeTableCellCoords',True)
	if role==controlTypes.ROLE_CHARTELEMENT:
		speakRole=False
	roleText=propertyValues.get('roleText')
	if speakRole and (roleText or reason not in (controlTypes.REASON_SAYALL,controlTypes.REASON_CARET,controlTypes.REASON_FOCUS) or not (name or value or cellCoordsText or rowNumber or columnNumber) or role not in controlTypes.silentRolesOnFocus) and (role!=controlTypes.ROLE_MATH or reason not in (controlTypes.REASON_CARET,controlTypes.REASON_SAYALL)):
		textList.append(roleText if roleText else controlTypes.roleLabels[role])
	if value:
		textList.append(value)
	states=propertyValues.get('states',set())
	realStates=propertyValues.get('_states',states)
	negativeStates=propertyValues.get('negativeStates',set())
	if states or negativeStates:
		textList.extend(controlTypes.processAndLabelStates(role, realStates, reason, states, negativeStates))
	if 'description' in propertyValues:
		textList.append(propertyValues['description'])
	if 'keyboardShortcut' in propertyValues:
		textList.append(propertyValues['keyboardShortcut'])
	if includeTableCellCoords and cellCoordsText:
		textList.append(cellCoordsText)
	if cellCoordsText or rowNumber or columnNumber:
		tableID = propertyValues.get("_tableID")
		# Always treat the table as different if there is no tableID.
		sameTable = (tableID and tableID == oldTableID)
		# Don't update the oldTableID if no tableID was given.
		if tableID and not sameTable:
			oldTableID = tableID
		if rowNumber and (not sameTable or rowNumber != oldRowNumber):
			rowHeaderText = propertyValues.get("rowHeaderText")
			if rowHeaderText:
				textList.append(rowHeaderText)
			if includeTableCellCoords and not cellCoordsText: 
				# Translators: Speaks current row number (example output: row 3).
				textList.append(_("row %s")%rowNumber)
			oldRowNumber = rowNumber
		if columnNumber and (not sameTable or columnNumber != oldColumnNumber):
			columnHeaderText = propertyValues.get("columnHeaderText")
			if columnHeaderText:
				textList.append(columnHeaderText)
			if includeTableCellCoords and not cellCoordsText:
				# Translators: Speaks current column number (example output: column 3).
				textList.append(_("column %s")%columnNumber)
			oldColumnNumber = columnNumber
	rowCount=propertyValues.get('rowCount',0)
	columnCount=propertyValues.get('columnCount',0)
	if rowCount and columnCount:
		# Translators: Speaks number of columns and rows in a table (example output: with 3 rows and 2 columns).
		textList.append(_("with {rowCount} rows and {columnCount} columns").format(rowCount=rowCount,columnCount=columnCount))
	elif columnCount and not rowCount:
		# Translators: Speaks number of columns (example output: with 4 columns).
		textList.append(_("with %s columns")%columnCount)
	elif rowCount and not columnCount:
		# Translators: Speaks number of rows (example output: with 2 rows).
		textList.append(_("with %s rows")%rowCount)
	if rowCount or columnCount:
		# The caller is entering a table, so ensure that it is treated as a new table, even if the previous table was the same.
		oldTableID = None
	ariaCurrent = propertyValues.get('current', False)
	if ariaCurrent:
		try:
			textList.append(controlTypes.isCurrentLabels[ariaCurrent])
		except KeyError:
			log.debugWarning("Aria-current value not handled: %s"%ariaCurrent)
			textList.append(controlTypes.isCurrentLabels[True])
	placeholder = propertyValues.get('placeholder', None)
	if placeholder:
		textList.append(placeholder)
	indexInGroup=propertyValues.get('positionInfo_indexInGroup',0)
	similarItemsInGroup=propertyValues.get('positionInfo_similarItemsInGroup',0)
	if 0<indexInGroup<=similarItemsInGroup:
		# Translators: Spoken to indicate the position of an item in a group of items (such as a list).
		# {number} is replaced with the number of the item in the group.
		# {total} is replaced with the total number of items in the group.
		textList.append(_("{number} of {total}").format(number=indexInGroup, total=similarItemsInGroup))
	if 'positionInfo_level' in propertyValues:
		level=propertyValues.get('positionInfo_level',None)
		role=propertyValues.get('role',None)
		if level is not None:
			if role in (controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM) and level!=oldTreeLevel:
				textList.insert(0,_("level %s")%level)
				oldTreeLevel=level
			else:
				# Translators: Speaks the item level in treeviews (example output: level 2).
				textList.append(_('level %s')%propertyValues['positionInfo_level'])
	return CHUNK_SEPARATOR.join([x for x in textList if x])

def getControlFieldSpeech(attrs,ancestorAttrs,fieldType,formatConfig=None,extraDetail=False,reason=None):
	if attrs.get('isHidden'):
		return u""
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]

	presCat=attrs.getPresentationCategory(ancestorAttrs,formatConfig, reason=reason)
	childControlCount=int(attrs.get('_childcontrolcount',"0"))
	if reason==controlTypes.REASON_FOCUS or attrs.get('alwaysReportName',False):
		name=attrs.get('name',"")
	else:
		name=""
	role=attrs.get('role',controlTypes.ROLE_UNKNOWN)
	states=attrs.get('states',set())
	keyboardShortcut=attrs.get('keyboardShortcut', "")
	ariaCurrent=attrs.get('current', None)
	placeholderValue=attrs.get('placeholder', None)
	value=attrs.get('value',"")
	if reason==controlTypes.REASON_FOCUS or attrs.get('alwaysReportDescription',False):
		description=attrs.get('description',"")
	else:
		description=""
	level=attrs.get('level',None)

	if presCat != attrs.PRESCAT_LAYOUT:
		tableID = attrs.get("table-id")
	else:
		tableID = None

	roleText=getSpeechTextForProperties(reason=reason,role=role)
	stateText=getSpeechTextForProperties(reason=reason,states=states,_role=role)
	keyboardShortcutText=getSpeechTextForProperties(reason=reason,keyboardShortcut=keyboardShortcut) if config.conf["presentation"]["reportKeyboardShortcuts"] else ""
	ariaCurrentText=getSpeechTextForProperties(reason=reason,current=ariaCurrent)
	placeholderText=getSpeechTextForProperties(reason=reason,placeholder=placeholderValue)
	nameText=getSpeechTextForProperties(reason=reason,name=name)
	valueText=getSpeechTextForProperties(reason=reason,value=value)
	descriptionText=(getSpeechTextForProperties(reason=reason,description=description)
		if config.conf["presentation"]["reportObjectDescriptions"] else "")
	levelText=getSpeechTextForProperties(reason=reason,positionInfo_level=level)

	# Determine under what circumstances this node should be spoken.
	# speakEntry: Speak when the user enters the control.
	# speakWithinForLine: When moving by line, speak when the user is already within the control.
	# speakExitForLine: When moving by line, speak when the user exits the control.
	# speakExitForOther: When moving by word or character, speak when the user exits the control.
	speakEntry=speakWithinForLine=speakExitForLine=speakExitForOther=False
	if presCat == attrs.PRESCAT_SINGLELINE:
		speakEntry=True
		speakWithinForLine=True
		speakExitForOther=True
	elif presCat in (attrs.PRESCAT_MARKER, attrs.PRESCAT_CELL):
		speakEntry=True
	elif presCat == attrs.PRESCAT_CONTAINER:
		speakEntry=True
		speakExitForLine=True
		speakExitForOther=True

	# Determine the order of speech.
	# speakContentFirst: Speak the content before the control field info.
	speakContentFirst = reason == controlTypes.REASON_FOCUS and presCat != attrs.PRESCAT_CONTAINER and role not in (controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_COMBOBOX) and not tableID and controlTypes.STATE_EDITABLE not in states
	# speakStatesFirst: Speak the states before the role.
	speakStatesFirst=role==controlTypes.ROLE_LINK

	# Determine what text to speak.
	# Special cases
	if speakEntry and childControlCount and fieldType=="start_addedToControlFieldStack" and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
		# List.
		# Translators: Speaks number of items in a list (example output: list with 5 items).
		return roleText+" "+_("with %s items")%childControlCount
	elif fieldType=="start_addedToControlFieldStack" and role==controlTypes.ROLE_TABLE and tableID:
		# Table.
		return " ".join((nameText,roleText,stateText, getSpeechTextForProperties(_tableID=tableID, rowCount=attrs.get("table-rowcount"), columnCount=attrs.get("table-columncount")),levelText))
	elif nameText and reason==controlTypes.REASON_FOCUS and fieldType == "start_addedToControlFieldStack" and role==controlTypes.ROLE_GROUPING:
		# #3321: Report the name of groupings (such as fieldsets) for quicknav and focus jumps
		return " ".join((nameText,roleText))
	elif fieldType in ("start_addedToControlFieldStack","start_relative") and role in (controlTypes.ROLE_TABLECELL,controlTypes.ROLE_TABLECOLUMNHEADER,controlTypes.ROLE_TABLEROWHEADER) and tableID:
		# Table cell.
		reportTableHeaders = formatConfig["reportTableHeaders"]
		reportTableCellCoords = formatConfig["reportTableCellCoords"]
		getProps = {
			'rowNumber': attrs.get("table-rownumber"),
			'columnNumber': attrs.get("table-columnnumber"),
			'includeTableCellCoords': reportTableCellCoords
		}
		if reportTableHeaders:
			getProps['rowHeaderText'] = attrs.get("table-rowheadertext")
			getProps['columnHeaderText'] = attrs.get("table-columnheadertext")
		return (getSpeechTextForProperties(_tableID=tableID, **getProps)
			+ (" %s" % stateText if stateText else "")
			+ (" %s" % ariaCurrentText if ariaCurrent else ""))

	# General cases
	elif (
		(speakEntry and ((speakContentFirst and fieldType in ("end_relative","end_inControlFieldStack")) or (not speakContentFirst and fieldType in ("start_addedToControlFieldStack","start_relative"))))
		or (speakWithinForLine and not speakContentFirst and not extraDetail and fieldType=="start_inControlFieldStack")
	):
		out = []
		content = attrs.get("content")
		if content and speakContentFirst:
			out.append(content)
		if placeholderValue:
			if valueText:
				log.error("valueText exists when expected none: valueText:'%s' placeholderText:'%s'"%(valueText,placeholderText))
			valueText = placeholderText
		out.extend(x for x in (nameText,(stateText if speakStatesFirst else roleText),(roleText if speakStatesFirst else stateText),ariaCurrentText,valueText,descriptionText,levelText,keyboardShortcutText) if x)
		if content and not speakContentFirst:
			out.append(content)
		return CHUNK_SEPARATOR.join(out)
		
	elif fieldType in ("end_removedFromControlFieldStack","end_relative") and roleText and ((not extraDetail and speakExitForLine) or (extraDetail and speakExitForOther)):
		# Translators: Indicates end of something (example output: at the end of a list, speaks out of list).
		return _("out of %s")%roleText

	# Special cases
	elif not speakEntry and fieldType in ("start_addedToControlFieldStack","start_relative"):
		out = []
		if not extraDetail and controlTypes.STATE_CLICKABLE in states: 
			# Clickable.
			out.append(getSpeechTextForProperties(states=set([controlTypes.STATE_CLICKABLE])))
		if ariaCurrent:
			out.append(ariaCurrentText)
		return CHUNK_SEPARATOR.join(out)
	else:
		return ""

def getFormatFieldSpeech(attrs,attrsCache=None,formatConfig=None,reason=None,unit=None,extraDetail=False , initialFormat=False, separator=CHUNK_SEPARATOR):
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]
	textList=[]
	if formatConfig["reportTables"]:
		tableInfo=attrs.get("table-info")
		oldTableInfo=attrsCache.get("table-info") if attrsCache is not None else None
		text=getTableInfoSpeech(tableInfo,oldTableInfo,extraDetail=extraDetail)
		if text:
			textList.append(text)
	if formatConfig["reportPage"]:
		pageNumber=attrs.get("page-number")
		oldPageNumber=attrsCache.get("page-number") if attrsCache is not None else None
		if pageNumber and pageNumber!=oldPageNumber:
			# Translators: Indicates the page number in a document.
			# %s will be replaced with the page number.
			text=_("page %s")%pageNumber
			textList.append(text)
		sectionNumber=attrs.get("section-number")
		oldSectionNumber=attrsCache.get("section-number") if attrsCache is not None else None
		if sectionNumber and sectionNumber!=oldSectionNumber:
			# Translators: Indicates the section number in a document.
			# %s will be replaced with the section number.
			text=_("section %s")%sectionNumber
			textList.append(text)

		textColumnCount=attrs.get("text-column-count")
		oldTextColumnCount=attrsCache.get("text-column-count") if attrsCache is not None else None
		textColumnNumber=attrs.get("text-column-number")
		oldTextColumnNumber=attrsCache.get("text-column-number") if attrsCache is not None else None

		# Because we do not want to report the number of columns when a document is just opened and there is only 
		# one column. This would be verbose, in the standard case.
		# column number has changed, or the columnCount has changed
		# but not if the columnCount is 1 or less and there is no old columnCount.
		if (((textColumnNumber and textColumnNumber!=oldTextColumnNumber) or
			(textColumnCount and textColumnCount!=oldTextColumnCount)) and not
			(textColumnCount and int(textColumnCount) <=1 and oldTextColumnCount == None)) :
			if textColumnNumber and textColumnCount:
				# Translators: Indicates the text column number in a document.
				# {0} will be replaced with the text column number.
				# {1} will be replaced with the number of text columns.
				text=_("column {0} of {1}").format(textColumnNumber,textColumnCount)
				textList.append(text)
			elif textColumnCount:
				# Translators: Indicates the text column number in a document.
				# %s will be replaced with the number of text columns.
				text=_("%s columns")%(textColumnCount)
				textList.append(text)

	sectionBreakType=attrs.get("section-break")
	if sectionBreakType:
		if sectionBreakType == "0" : # Continuous section break.
			text=_("continuous section break")
		elif sectionBreakType == "1" : # New column section break.
			text=_("new column section break")
		elif sectionBreakType == "2" : # New page section break.
			text=_("new page section break")
		elif sectionBreakType == "3" : # Even pages section break.
			text=_("even pages section break")
		elif sectionBreakType == "4" : # Odd pages section break.
			text=_("odd pages section break")
		else:
			text=""
		textList.append(text)
	columnBreakType=attrs.get("column-break")
	if columnBreakType:
		textList.append(_("column break"))
	if  formatConfig["reportHeadings"]:
		headingLevel=attrs.get("heading-level")
		oldHeadingLevel=attrsCache.get("heading-level") if attrsCache is not None else None
		# headings should be spoken not only if they change, but also when beginning to speak lines or paragraphs
		# Ensuring a similar experience to if a heading was a controlField
		if headingLevel and (initialFormat and (reason==controlTypes.REASON_FOCUS or unit in (textInfos.UNIT_LINE,textInfos.UNIT_PARAGRAPH)) or headingLevel!=oldHeadingLevel):
			# Translators: Speaks the heading level (example output: heading level 2).
			text=_("heading level %d")%headingLevel
			textList.append(text)
	if  formatConfig["reportStyle"]:
		style=attrs.get("style")
		oldStyle=attrsCache.get("style") if attrsCache is not None else None
		if style!=oldStyle:
			if style:
				# Translators: Indicates the style of text.
				# A style is a collection of formatting settings and depends on the application.
				# %s will be replaced with the name of the style.
				text=_("style %s")%style
			else:
				# Translators: Indicates that text has reverted to the default style.
				# A style is a collection of formatting settings and depends on the application.
				text=_("default style")
			textList.append(text)
	if  formatConfig["reportBorderStyle"]:
		borderStyle=attrs.get("border-style")
		oldBorderStyle=attrsCache.get("border-style") if attrsCache is not None else None
		if borderStyle!=oldBorderStyle:
			if borderStyle:
				text=borderStyle
			else:
				# Translators: Indicates that cell does not have border lines.
				text=_("no border lines")
			textList.append(text)
	if  formatConfig["reportFontName"]:
		fontFamily=attrs.get("font-family")
		oldFontFamily=attrsCache.get("font-family") if attrsCache is not None else None
		if fontFamily and fontFamily!=oldFontFamily:
			textList.append(fontFamily)
		fontName=attrs.get("font-name")
		oldFontName=attrsCache.get("font-name") if attrsCache is not None else None
		if fontName and fontName!=oldFontName:
			textList.append(fontName)
	if  formatConfig["reportFontSize"]:
		fontSize=attrs.get("font-size")
		oldFontSize=attrsCache.get("font-size") if attrsCache is not None else None
		if fontSize and fontSize!=oldFontSize:
			textList.append(fontSize)
	if  formatConfig["reportColor"]:
		color=attrs.get("color")
		oldColor=attrsCache.get("color") if attrsCache is not None else None
		backgroundColor=attrs.get("background-color")
		oldBackgroundColor=attrsCache.get("background-color") if attrsCache is not None else None
		backgroundColor2=attrs.get("background-color2")
		oldBackgroundColor2=attrsCache.get("background-color2") if attrsCache is not None else None
		bgColorChanged=backgroundColor!=oldBackgroundColor or backgroundColor2!=oldBackgroundColor2
		bgColorText=backgroundColor.name if isinstance(backgroundColor,colors.RGB) else unicode(backgroundColor)
		if backgroundColor2:
			bg2Name=backgroundColor2.name if isinstance(backgroundColor2,colors.RGB) else unicode(backgroundColor2)
			# Translators: Reported when there are two background colors.
			# This occurs when, for example, a gradient pattern is applied to a spreadsheet cell.
			# {color1} will be replaced with the first background color.
			# {color2} will be replaced with the second background color.
			bgColorText=_("{color1} to {color2}").format(color1=bgColorText,color2=bg2Name)
		if color and backgroundColor and color!=oldColor and bgColorChanged:
			# Translators: Reported when both the text and background colors change.
			# {color} will be replaced with the text color.
			# {backgroundColor} will be replaced with the background color.
			textList.append(_("{color} on {backgroundColor}").format(
				color=color.name if isinstance(color,colors.RGB) else unicode(color),
				backgroundColor=bgColorText))
		elif color and color!=oldColor:
			# Translators: Reported when the text color changes (but not the background color).
			# {color} will be replaced with the text color.
			textList.append(_("{color}").format(color=color.name if isinstance(color,colors.RGB) else unicode(color)))
		elif backgroundColor and bgColorChanged:
			# Translators: Reported when the background color changes (but not the text color).
			# {backgroundColor} will be replaced with the background color.
			textList.append(_("{backgroundColor} background").format(backgroundColor=bgColorText))
		backgroundPattern=attrs.get("background-pattern")
		oldBackgroundPattern=attrsCache.get("background-pattern") if attrsCache is not None else None
		if backgroundPattern and backgroundPattern!=oldBackgroundPattern:
			textList.append(_("background pattern {pattern}").format(pattern=backgroundPattern))
	if  formatConfig["reportLineNumber"]:
		lineNumber=attrs.get("line-number")
		oldLineNumber=attrsCache.get("line-number") if attrsCache is not None else None
		if lineNumber is not None and lineNumber!=oldLineNumber:
			# Translators: Indicates the line number of the text.
			# %s will be replaced with the line number.
			text=_("line %s")%lineNumber
			textList.append(text)
	if  formatConfig["reportRevisions"]:
		# Insertion
		revision=attrs.get("revision-insertion")
		oldRevision=attrsCache.get("revision-insertion") if attrsCache is not None else None
		if (revision or oldRevision is not None) and revision!=oldRevision:
			# Translators: Reported when text is marked as having been inserted
			text=(_("inserted") if revision
				# Translators: Reported when text is no longer marked as having been inserted.
				else _("not inserted"))
			textList.append(text)
		revision=attrs.get("revision-deletion")
		oldRevision=attrsCache.get("revision-deletion") if attrsCache is not None else None
		if (revision or oldRevision is not None) and revision!=oldRevision:
			# Translators: Reported when text is marked as having been deleted
			text=(_("deleted") if revision
				# Translators: Reported when text is no longer marked as having been  deleted.
				else _("not deleted"))
			textList.append(text)
		revision=attrs.get("revision")
		oldRevision=attrsCache.get("revision") if attrsCache is not None else None
		if (revision or oldRevision is not None) and revision!=oldRevision:
			# Translators: Reported when text is revised.
			text=(_("revised %s"%revision) if revision
				# Translators: Reported when text is not revised.
				else _("no revised %s")%oldRevision)
			textList.append(text)
	if  formatConfig["reportEmphasis"]:
		# marked text 
		marked=attrs.get("marked")
		oldMarked=attrsCache.get("marked") if attrsCache is not None else None
		if (marked or oldMarked is not None) and marked!=oldMarked:
			# Translators: Reported when text is marked
			text=(_("marked") if marked
				# Translators: Reported when text is no longer marked
				else _("not marked"))
			textList.append(text)
		# strong text
		strong=attrs.get("strong")
		oldStrong=attrsCache.get("strong") if attrsCache is not None else None
		if (strong or oldStrong is not None) and strong!=oldStrong:
			# Translators: Reported when text is marked as strong (e.g. bold)
			text=(_("strong") if strong
				# Translators: Reported when text is no longer marked as strong (e.g. bold) 
				else _("not strong"))
			textList.append(text)
		# emphasised text 
		emphasised=attrs.get("emphasised")
		oldEmphasised=attrsCache.get("emphasised") if attrsCache is not None else None
		if (emphasised or oldEmphasised is not None) and emphasised!=oldEmphasised:
			# Translators: Reported when text is marked as emphasised
			text=(_("emphasised") if emphasised
				# Translators: Reported when text is no longer marked as emphasised 
				else _("not emphasised"))
			textList.append(text)
	if  formatConfig["reportFontAttributes"]:
		bold=attrs.get("bold")
		oldBold=attrsCache.get("bold") if attrsCache is not None else None
		if (bold or oldBold is not None) and bold!=oldBold:
			# Translators: Reported when text is bolded.
			text=(_("bold") if bold
				# Translators: Reported when text is not bolded.
				else _("no bold"))
			textList.append(text)
		italic=attrs.get("italic")
		oldItalic=attrsCache.get("italic") if attrsCache is not None else None
		if (italic or oldItalic is not None) and italic!=oldItalic:
			# Translators: Reported when text is italicized.
			text=(_("italic") if italic
				# Translators: Reported when text is not italicized.
				else _("no italic"))
			textList.append(text)
		strikethrough=attrs.get("strikethrough")
		oldStrikethrough=attrsCache.get("strikethrough") if attrsCache is not None else None
		if (strikethrough or oldStrikethrough is not None) and strikethrough!=oldStrikethrough:
			if strikethrough:
				# Translators: Reported when text is formatted with double strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				text=(_("double strikethrough") if strikethrough=="double"
				# Translators: Reported when text is formatted with strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				else _("strikethrough"))
			else:
				# Translators: Reported when text is formatted without strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				text=_("no strikethrough")
			textList.append(text)
		underline=attrs.get("underline")
		oldUnderline=attrsCache.get("underline") if attrsCache is not None else None
		if (underline or oldUnderline is not None) and underline!=oldUnderline:
			# Translators: Reported when text is underlined.
			text=(_("underlined") if underline
				# Translators: Reported when text is not underlined.
				else _("not underlined"))
			textList.append(text)
		textPosition=attrs.get("text-position")
		oldTextPosition=attrsCache.get("text-position") if attrsCache is not None else None
		if (textPosition or oldTextPosition is not None) and textPosition!=oldTextPosition:
			textPosition=textPosition.lower() if textPosition else textPosition
			if textPosition=="super":
				# Translators: Reported for superscript text.
				text=_("superscript")
			elif textPosition=="sub":
				# Translators: Reported for subscript text.
				text=_("subscript")
			else:
				# Translators: Reported for text which is at the baseline position;
				# i.e. not superscript or subscript.
				text=_("baseline")
			textList.append(text)
	if formatConfig["reportAlignment"]:
		textAlign=attrs.get("text-align")
		oldTextAlign=attrsCache.get("text-align") if attrsCache is not None else None
		if (textAlign or oldTextAlign is not None) and textAlign!=oldTextAlign:
			textAlign=textAlign.lower() if textAlign else textAlign
			if textAlign=="left":
				# Translators: Reported when text is left-aligned.
				text=_("align left")
			elif textAlign=="center":
				# Translators: Reported when text is centered.
				text=_("align center")
			elif textAlign=="right":
				# Translators: Reported when text is right-aligned.
				text=_("align right")
			elif textAlign=="justify":
				# Translators: Reported when text is justified.
				# See http://en.wikipedia.org/wiki/Typographic_alignment#Justified
				text=_("align justify")
			elif textAlign=="distribute":
				# Translators: Reported when text is justified with character spacing (Japanese etc) 
				# See http://kohei.us/2010/01/21/distributed-text-justification/
				text=_("align distributed")
			else:
				# Translators: Reported when text has reverted to default alignment.
				text=_("align default")
			textList.append(text)
		verticalAlign=attrs.get("vertical-align")
		oldverticalAlign=attrsCache.get("vertical-align") if attrsCache is not None else None
		if (verticalAlign or oldverticalAlign is not None) and verticalAlign!=oldverticalAlign:
			verticalAlign=verticalAlign.lower() if verticalAlign else verticalAlign
			if verticalAlign=="top":
				# Translators: Reported when text is vertically top-aligned.
				text=_("vertical align top")
			elif verticalAlign in("center","middle"):
				# Translators: Reported when text is vertically middle aligned.
				text=_("vertical align middle")
			elif verticalAlign=="bottom":
				# Translators: Reported when text is vertically bottom-aligned.
				text=_("vertical align bottom")
			elif verticalAlign=="baseline":
				# Translators: Reported when text is vertically aligned on the baseline. 
				text=_("vertical align baseline")
			elif verticalAlign=="justify":
				# Translators: Reported when text is vertically justified.
				text=_("vertical align justified")
			elif verticalAlign=="distributed":
				# Translators: Reported when text is vertically justified but with character spacing (For some Asian content). 
				text=_("vertical align distributed") 
			else:
				# Translators: Reported when text has reverted to default vertical alignment.
				text=_("vertical align default")
			textList.append(text)
	if formatConfig["reportParagraphIndentation"]:
		indentLabels={
			'left-indent':(
				# Translators: the label for paragraph format left indent
				_("left indent"),
				# Translators: the message when there is no paragraph format left indent
				_("no left indent"),
			),
			'right-indent':(
				# Translators: the label for paragraph format right indent
				_("right indent"),
				# Translators: the message when there is no paragraph format right indent
				_("no right indent"),
			),
			'hanging-indent':(
				# Translators: the label for paragraph format hanging indent
				_("hanging indent"),
				# Translators: the message when there is no paragraph format hanging indent
				_("no hanging indent"),
			),
			'first-line-indent':(
				# Translators: the label for paragraph format first line indent 
				_("first line indent"),
				# Translators: the message when there is no paragraph format first line indent
				_("no first line indent"),
			),
		}
		for attr,(label,noVal) in indentLabels.iteritems():
			newVal=attrs.get(attr)
			oldVal=attrsCache.get(attr) if attrsCache else None
			if (newVal or oldVal is not None) and newVal!=oldVal:
				if newVal:
					textList.append(u"%s %s"%(label,newVal))
				else:
					textList.append(noVal)
	if formatConfig["reportLineSpacing"]:
		lineSpacing=attrs.get("line-spacing")
		oldLineSpacing=attrsCache.get("line-spacing") if attrsCache is not None else None
		if (lineSpacing or oldLineSpacing is not None) and lineSpacing!=oldLineSpacing:
			# Translators: a type of line spacing (E.g. single line spacing)
			textList.append(_("line spacing %s")%lineSpacing)
	if  formatConfig["reportLinks"]:
		link=attrs.get("link")
		oldLink=attrsCache.get("link") if attrsCache is not None else None
		if (link or oldLink is not None) and link!=oldLink:
			text=_("link") if link else _("out of %s")%_("link")
			textList.append(text)
	if  formatConfig["reportComments"]:
		comment=attrs.get("comment")
		oldComment=attrsCache.get("comment") if attrsCache is not None else None
		if (comment or oldComment is not None) and comment!=oldComment:
			if comment:
				# Translators: Reported when text contains a comment.
				text=_("has comment")
				textList.append(text)
			elif extraDetail:
				# Translators: Reported when text no longer contains a comment.
				text=_("out of comment")
				textList.append(text)
	if formatConfig["reportSpellingErrors"]:
		invalidSpelling=attrs.get("invalid-spelling")
		oldInvalidSpelling=attrsCache.get("invalid-spelling") if attrsCache is not None else None
		if (invalidSpelling or oldInvalidSpelling is not None) and invalidSpelling!=oldInvalidSpelling:
			if invalidSpelling:
				# Translators: Reported when text contains a spelling error.
				text=_("spelling error")
			elif extraDetail:
				# Translators: Reported when moving out of text containing a spelling error.
				text=_("out of spelling error")
			else:
				text=""
			if text:
				textList.append(text)
		invalidGrammar=attrs.get("invalid-grammar")
		oldInvalidGrammar=attrsCache.get("invalid-grammar") if attrsCache is not None else None
		if (invalidGrammar or oldInvalidGrammar is not None) and invalidGrammar!=oldInvalidGrammar:
			if invalidGrammar:
				# Translators: Reported when text contains a grammar error.
				text=_("grammar error")
			elif extraDetail:
				# Translators: Reported when moving out of text containing a grammar error.
				text=_("out of grammar error")
			else:
				text=""
			if text:
				textList.append(text)
	if unit in (textInfos.UNIT_LINE,textInfos.UNIT_SENTENCE,textInfos.UNIT_PARAGRAPH,textInfos.UNIT_READINGCHUNK):
		linePrefix=attrs.get("line-prefix")
		if linePrefix:
			textList.append(linePrefix)
	if attrsCache is not None:
		attrsCache.clear()
		attrsCache.update(attrs)
	return separator.join(textList)

def getTableInfoSpeech(tableInfo,oldTableInfo,extraDetail=False):
	if tableInfo is None and oldTableInfo is None:
		return ""
	if tableInfo is None and oldTableInfo is not None:
		# Translators: Indicates end of a table.
		return _("out of table")
	if not oldTableInfo or tableInfo.get("table-id")!=oldTableInfo.get("table-id"):
		newTable=True
	else:
		newTable=False
	textList=[]
	if newTable:
		columnCount=tableInfo.get("column-count",0)
		rowCount=tableInfo.get("row-count",0)
		# Translators: reports number of columns and rows in a table (example output: table with 3 columns and 5 rows).
		text=_("table with {columnCount} columns and {rowCount} rows").format(columnCount=columnCount,rowCount=rowCount)
		textList.append(text)
	oldColumnNumber=oldTableInfo.get("column-number",0) if oldTableInfo else 0
	columnNumber=tableInfo.get("column-number",0)
	if columnNumber!=oldColumnNumber:
		textList.append(_("column %s")%columnNumber)
	oldRowNumber=oldTableInfo.get("row-number",0) if oldTableInfo else 0
	rowNumber=tableInfo.get("row-number",0)
	if rowNumber!=oldRowNumber:
		textList.append(_("row %s")%rowNumber)
	return " ".join(textList)

re_last_pause=re.compile(ur"^(.*(?<=[^\s.!?])[.!?][\"'”’)]?(?:\s+|$))(.*$)",re.DOTALL|re.UNICODE)

def speakWithoutPauses(speechSequence,detectBreaks=True):
	"""
	Speaks the speech sequences given over multiple calls, only sending to the synth at acceptable phrase or sentence boundaries, or when given None for the speech sequence.
	@return: C{True} if something was actually spoken,
		C{False} if only buffering occurred.
	@rtype: bool
	"""
	lastStartIndex=0
	#Break on all explicit break commands
	if detectBreaks and speechSequence:
		sequenceLen=len(speechSequence)
		spoke = False
		for index in xrange(sequenceLen):
			if isinstance(speechSequence[index],EndUtteranceCommand):
				if index>0 and lastStartIndex<index:
					speakWithoutPauses(speechSequence[lastStartIndex:index],detectBreaks=False)
				speakWithoutPauses(None)
				spoke = True
				lastStartIndex=index+1
		if lastStartIndex<sequenceLen:
			spoke = speakWithoutPauses(speechSequence[lastStartIndex:],detectBreaks=False)
		return spoke
	finalSpeechSequence=[] #To be spoken now
	pendingSpeechSequence=[] #To be saved off for speaking  later
	if speechSequence is None: #Requesting flush
		if speakWithoutPauses._pendingSpeechSequence: 
			#Place the last incomplete phrase in to finalSpeechSequence to be spoken now
			finalSpeechSequence=speakWithoutPauses._pendingSpeechSequence
			speakWithoutPauses._pendingSpeechSequence=[]
	else: #Handling normal speech
		#Scan the given speech and place all completed phrases in finalSpeechSequence to be spoken,
		#And place the final incomplete phrase in pendingSpeechSequence
		for index in xrange(len(speechSequence)-1,-1,-1): 
			item=speechSequence[index]
			if isinstance(item,basestring):
				m=re_last_pause.match(item)
				if m:
					before,after=m.groups()
					if after:
						pendingSpeechSequence.append(after)
					if before:
						finalSpeechSequence.extend(speakWithoutPauses._pendingSpeechSequence)
						speakWithoutPauses._pendingSpeechSequence=[]
						finalSpeechSequence.extend(speechSequence[0:index])
						finalSpeechSequence.append(before)
						# Apply the last language change to the pending sequence.
						# This will need to be done for any other speech change commands introduced in future.
						for changeIndex in xrange(index-1,-1,-1):
							change=speechSequence[changeIndex]
							if not isinstance(change,LangChangeCommand):
								continue
							pendingSpeechSequence.append(change)
							break
						break
				else:
					pendingSpeechSequence.append(item)
			else:
				pendingSpeechSequence.append(item)
		if pendingSpeechSequence:
			pendingSpeechSequence.reverse()
			speakWithoutPauses._pendingSpeechSequence.extend(pendingSpeechSequence)
	if shouldUseCompatCodeForIndexing():
		# Compat code to support speechCompat.sayAll_readText.
		#Scan the final speech sequence backwards
		for item in reversed(finalSpeechSequence):
			if isinstance(item,IndexCommand):
				speakWithoutPauses._lastSentIndex=item.index
				break
	if finalSpeechSequence:
		speak(finalSpeechSequence)
		return True
	return False
speakWithoutPauses._lastSentIndex=None # For speechCompat.sayAll_readText
speakWithoutPauses._pendingSpeechSequence=[]

class SpeechCommand(object):
	"""The base class for objects that can be inserted between strings of text to perform actions, change voice parameters, etc.
	Note that some of these commands are processed by NVDA and are not directly passed to synth drivers.
	synth drivers will only receive commands derived from L{SynthCommand}.
	"""

class SynthCommand(SpeechCommand):
	"""Commands that can be passed to synth drivers.
	"""

class IndexCommand(SynthCommand):
	"""Marks this point in the speech with an index.
	When speech reaches this index, the synthesizer notifies NVDA,
	thus allowing NVDA to perform actions at specific points in the speech;
	e.g. synchronizing the cursor, beeping or playing a sound.
	Callers should not use this directly.
	Instead, use one of the subclasses of L{BaseCallbackCommand}.
	NVDA handles the indexing and dispatches callbacks as appropriate.
	"""

	def __init__(self,index):
		"""
		@param index: the value of this index
		@type index: integer
		"""
		if not isinstance(index,int): raise ValueError("index must be int, not %s"%type(index))
		self.index=index

	def __repr__(self):
		return "IndexCommand(%r)" % self.index

class SynthParamCommand(SynthCommand):
	"""A synth command which changes a parameter for subsequent speech.
	"""
	#: Whether this command returns the parameter to its default value.
	#: Note that the default might be configured by the user;
	#: e.g. for pitch, rate, etc.
	#: @type: bool
	isDefault = False

class CharacterModeCommand(SynthParamCommand):
	"""Turns character mode on and off for speech synths."""

	def __init__(self,state):
		"""
		@param state: if true character mode is on, if false its turned off.
		@type state: boolean
		"""
		if not isinstance(state,bool): raise ValueError("state must be boolean, not %s"%type(state))
		self.state=state
		self.isDefault = not state

	def __repr__(self):
		return "CharacterModeCommand(%r)" % self.state

class LangChangeCommand(SynthParamCommand):
	"""A command to switch the language within speech."""

	def __init__(self,lang):
		"""
		@param lang: the language to switch to: If None then the NVDA locale will be used.
		@type lang: string
		"""
		self.lang=lang # if lang else languageHandler.getLanguage()
		self.isDefault = not lang

	def __repr__(self):
		return "LangChangeCommand (%r)"%self.lang

class BreakCommand(SynthCommand):
	"""Insert a break between words.
	"""

	def __init__(self, time=0):
		"""
		@param time: The duration of the pause to be inserted in milliseconds.
		@param time: int
		"""
		self.time = time

	def __repr__(self):
		return "BreakCommand(time=%d)" % self.time

class EndUtteranceCommand(SpeechCommand):
	"""End the current utterance at this point in the speech.
	Any text after this will be sent to the synthesizer as a separate utterance.
	"""

	def __repr__(self):
		return "EndUtteranceCommand()"

class BaseProsodyCommand(SynthParamCommand):
	"""Base class for commands which change voice prosody; i.e. pitch, rate, etc.
	The change to the setting is specified using either an offset or a multiplier, but not both.
	The L{offset} and L{multiplier} properties convert between the two if necessary.
	To return to the default value, specify neither.
	This base class should not be instantiated directly.
	"""
	#: The name of the setting in the configuration; e.g. pitch, rate, etc.
	settingName = None

	def __init__(self, offset=0, multiplier=1):
		"""Constructor.
		Either of C{offset} or C{multiplier} may be specified, but not both.
		@param offset: The amount by which to increase/decrease the user configured setting;
			e.g. 30 increases by 30, -10 decreases by 10, 0 returns to the configured setting.
		@type offset: int
		@param multiplier: The number by which to multiply the user configured setting;
			e.g. 0.5 is half, 1 returns to the configured setting.
		@param multiplier: int/float
		"""
		if offset != 0 and multiplier != 1:
			raise ValueError("offset and multiplier both specified")
		self._offset = offset
		self._multiplier = multiplier
		self.isDefault = offset == 0 and multiplier == 1

	@property
	def defaultValue(self):
		"""The default value for the setting as configured by the user.
		"""
		synth = getSynth()
		synthConf = config.conf["speech"][synth.name]
		return synthConf[self.settingName]

	@property
	def multiplier(self):
		"""The number by which to multiply the default value.
		"""
		if self._multiplier != 1:
			# Constructed with multiplier. Just return it.
			return self._multiplier
		if self._offset == 0:
			# Returning to default.
			return 1
		# Calculate multiplier from default value and offset.
		defaultVal = self.defaultValue
		newVal = defaultVal + self._offset
		return float(newVal) / defaultVal

	@property
	def offset(self):
		"""The amount by which to increase/decrease the default value.
		"""
		if self._offset != 0:
			# Constructed with offset. Just return it.
			return self._offset
		if self._multiplier == 1:
			# Returning to default.
			return 0
		# Calculate offset from default value and multiplier.
		defaultVal = self.defaultValue
		newVal = defaultVal * self._multiplier
		return int(newVal - defaultVal)

	@property
	def newValue(self):
		"""The new absolute value after the offset or multiplier is applied to the default value.
		"""
		if self._offset != 0:
			# Calculate using offset.
			return self.defaultValue + self._offset
		if self._multiplier != 1:
			# Calculate using multiplier.
			return int(self.defaultValue * self._multiplier)
		# Returning to default.
		return self.defaultValue

	def __repr__(self):
		if self._offset != 0:
			param = "offset=%d" % self._offset
		elif self._multiplier != 1:
			param = "multiplier=%g" % self._multiplier
		else:
			param = ""
		return "{type}({param})".format(
			type=type(self).__name__, param=param)

class PitchCommand(BaseProsodyCommand):
	"""Change the pitch of the voice.
	"""
	settingName = "pitch"

class VolumeCommand(BaseProsodyCommand):
	"""Change the volume of the voice.
	"""
	settingName = "volume"

class RateCommand(BaseProsodyCommand):
	"""Change the rate of the voice.
	"""
	settingName = "rate"

class PhonemeCommand(SynthCommand):
	"""Insert a specific pronunciation.
	This command accepts Unicode International Phonetic Alphabet (IPA) characters.
	Note that this is not well supported by synthesizers.
	"""

	def __init__(self, ipa, text=None):
		"""
		@param ipa: Unicode IPA characters.
		@type ipa: unicode
		@param text: Text to speak if the synthesizer does not support
			some or all of the specified IPA characters,
			C{None} to ignore this command instead.
		@type text: unicode
		"""
		self.ipa = ipa
		self.text = text

	def __repr__(self):
		out = "PhonemeCommand(%r" % self.ipa
		if self.text:
			out += ", text=%r" % self.text
		return out + ")"

class BaseCallbackCommand(SpeechCommand):
	"""Base class for commands which cause a function to be called when speech reaches them.
	This class should not be instantiated directly.
	It is designed to be subclassed to provide specific functionality;
	e.g. L{BeepCommand}.
	To supply a generic function to run, use L{CallbackCommand}.
	This command is never passed to synth drivers.
	"""

	def run(self):
		"""Code to run when speech reaches this command.
		"""

class CallbackCommand(BaseCallbackCommand):
	"""Call a function when speech reaches this point.
	"""

	def __init__(self, callback):
		self.run = callback

class BeepCommand(BaseCallbackCommand):
	"""Produce a beep.
	"""

	def __init__(self, hz, length, left=50, right=50):
		self.hz = hz
		self.length = length
		self.left = left
		self.right = right

	def run(self):
		import tones
		tones.beep(self.hz, self.length, left=self.left, right=self.right)

	def __repr__(self):
		return "BeepCommand({hz}, {length}, left={left}, right={right})".format(
			hz=self.hz, length=self.length, left=self.left, right=self.right)

class WaveFileCommand(BaseCallbackCommand):
	"""Play a wave file.
	"""

	def __init__(self, fileName):
		self.fileName = fileName

	def run(self):
		import nvwave
		nvwave.playWaveFile(self.fileName, async=False)

	def __repr__(self):
		return "WaveFileCommand(%r)" % self.fileName

class ConfigProfileTriggerCommand(SpeechCommand):
	"""Applies (or stops applying) a configuration profile trigger to subsequent speech.
	"""

	def __init__(self, trigger, enter=True):
		"""
		@param trigger: The configuration profile trigger.
		@type trigger: L{config.ProfileTrigger}
		@param enter: C{True} to apply the trigger, C{False} to stop applying it.
		@type enter: bool
		"""
		self.trigger = trigger
		self.enter = enter
		trigger._shouldNotifyProfileSwitch = False

class ParamChangeTracker(object):
	"""Keeps track of commands which change parameters from their defaults.
	This is useful when an utterance needs to be split.
	As you are processing a sequence,
	you update the tracker with a parameter change using the L{update} method.
	When you split the utterance, you use the L{getChanged} method to get
	the parameters which have been changed from their defaults.
	"""

	def __init__(self):
		self._commands = {}

	def update(self, command):
		"""Update the tracker with a parameter change.
		@param command: The parameter change command.
		@type command: L{SynthParamCommand}
		"""
		paramType = type(command)
		if command.isDefault:
			# This no longer applies.
			self._commands.pop(paramType, None)
		else:
			self._commands[paramType] = command

	def getChanged(self):
		"""Get the commands for the parameters which have been changed from their defaults.
		@return: List of parameter change commands.
		@type: list of L{SynthParamCommand}
		"""
		return self._commands.values()

class _ManagerPriorityQueue(object):
	"""A speech queue for a specific priority.
	This is intended for internal use by L{_SpeechManager} only.
	Each priority has a separate queue.
	It holds the pending speech sequences to be spoken,
	as well as other information necessary to restore state when this queue
	is preempted by a higher priority queue.
	"""

	def __init__(self, priority):
		self.priority = priority
		#: The pending speech sequences to be spoken.
		#: These are split at indexes,
		#: so a single utterance might be split over multiple sequences.
		self.pendingSequences = []
		#: The configuration profile triggers that have been entered during speech.
		self.enteredProfileTriggers = []
		#: Keeps track of parameters that have been changed during an utterance.
		self.paramTracker = ParamChangeTracker()

class _SpeechManager(object):
	"""Manages queuing of speech utterances, calling callbacks at desired points in the speech, profile switching, prioritization, etc.
	This is intended for internal use only.
	It is used by higher level functions such as L{speak}.

	The high level flow of control is as follows:
	1. A speech sequence is queued with L{speak}, which in turn calls L{_queueSpeechSequence}.
	2. L{_processSpeechSequence} is called to normalize, process and split the input sequence.
		It converts callbacks to indexes.
		All indexing is assigned and managed by this class.
		It maps any indexes to their corresponding callbacks.
		It splits the sequence at indexes so we easily know what has completed speaking.
		If there are end utterance commands, the sequence is split at that point.
		We ensure there is an index at the end of all utterances so we know when they've finished speaking.
		We ensure any config profile trigger commands are preceded by an utterance end.
		Parameter changes are re-applied after utterance breaks.
		We ensure any entered profile triggers are exited at the very end.
	3. L{_queueSpeechSequence} places these processed sequences in the queue
		for the priority specified by the caller in step 1.
		There is a separate queue for each priority.
	4. L{_pushNextSpeech} is called to begin pushing speech.
		It looks for the highest priority queue with pending speech.
		Because there's no other speech queued, that'll be the queue we just touched.
	5. If the input begins with a profile switch, it is applied immediately.
	6. L{_buildNextUtterance} is called to build a full utterance and it is sent to the synth.
	7. For every index reached, L{_handleIndex} is called.
		The completed sequence is removed from L{_pendingSequences}.
		If there is an associated callback, it is run.
		If the index marks the end of an utterance, L{_pushNextSpeech} is called to push more speech.
	8. If there is another utterance before a profile switch, it is built and sent as per steps 6 and 7.
	9. In L{_pushNextSpeech}, if a profile switch is next, we wait for the synth to finish speaking before pushing more.
		This is because we don't want to start speaking too early with a different synth.
		L{_handleDoneSpeaking} is called when the synth finishes speaking.
		It pushes more speech, which includes applying the profile switch.
	10. The flow then repeats from step 6 onwards until there are no more pending sequences.
	11. If another sequence is queued via L{speak} during speech,
		it is processed and queued as per steps 2 and 3.
	12. If this is the first utterance at priority now, speech is interrupted
		and L{_pushNextSpeech} is called.
		Otherwise, L{_pushNextSpeech} is called when the current utterance completes
		as per step 7.
	13. When L{_pushNextSpeech} is next called, it looks for the highest priority queue with pending speech.
		If that priority is different to the priority of the utterance just spoken,
		any relevant profile switches are applied to restore the state for this queue.
	14. If a lower priority utterance was interrupted in the middle,
		L{_buildNextUtterance} applies any parameter changes that applied before the interruption.
	15. The flow then repeats from step 6 onwards until there are no more pending sequences.

	Note:
	All of this activity is (and must be) synchronized and serialized on the main thread.
	"""

	def __init__(self):
		#: A counter for indexes sent to the synthesizer for callbacks, etc.
		self._indexCounter = self._generateIndexes()
		self._reset()
		synthDriverHandler.synthIndexReached.register(self._onSynthIndexReached)
		synthDriverHandler.synthDoneSpeaking.register(self._onSynthDoneSpeaking)

	#: Maximum index number to pass to synthesizers.
	MAX_INDEX = 9999
	def _generateIndexes(self):
		"""Generator of index numbers.
		We don't want to reuse index numbers too quickly,
		as there can be race conditions when cancelling speech which might result
		in an index from a previous utterance being treated as belonging to the current utterance.
		However, we don't want the counter increasing indefinitely,
		as some synths might not be able to handle huge numbers.
		Therefore, we use a counter which starts at 1, counts up to L{MAX_INDEX},
		wraps back to 1 and continues cycling thus.
		This maximum is arbitrary, but
		it's small enough that any synth should be able to handle it
		and large enough that previous indexes won't reasonably get reused
		in the same or previous utterance.
		"""
		while True:
			for index in xrange(1, self.MAX_INDEX + 1):
				yield index

	def _reset(self):
		#: The queues for each priority.
		self._priQueues = {}
		#: The priority queue for the utterance currently being spoken.
		self._curPriQueue = None
		#: Maps indexes to BaseCallbackCommands.
		self._indexesToCallbacks = {}
		#: Whether to push more speech when the synth reports it is done speaking.
		self._shouldPushWhenDoneSpeaking = False

	def speak(self, speechSequence, priority):
		# If speech isn't already in progress, we need to push the first speech.
		push = self._curPriQueue is None
		interrupt = self._queueSpeechSequence(speechSequence, priority)
		if interrupt:
			getSynth().cancel()
			push = True
		if push:
			self._pushNextSpeech(True)

	def _queueSpeechSequence(self, inSeq, priority):
		"""
		@return: Whether to interrupt speech.
		@rtype: bool
		"""
		outSeq = self._processSpeechSequence(inSeq)
		queue = self._priQueues.get(priority)
		if not queue:
			queue = self._priQueues[priority] = _ManagerPriorityQueue(priority)
		first = len(queue.pendingSequences) == 0
		queue.pendingSequences.extend(outSeq)
		if priority is SPRI_NOW and first:
			# If this is the first sequence at SPRI_NOW, interrupt speech.
			return True
		return False

	def _processSpeechSequence(self, inSeq):
		paramTracker = ParamChangeTracker()
		enteredTriggers = []
		outSeq = []
		outSeqs = []

		def ensureEndUtterance(outSeq):
			# We split at EndUtteranceCommands so the ends of utterances are easily found.
			if outSeq:
				# There have been commands since the last split.
				outSeqs.append(outSeq)
				lastOutSeq = outSeq
				# Re-apply parameters that have been changed from their defaults.
				outSeq = paramTracker.getChanged()
			else:
				lastOutSeq = outSeqs[-1] if outSeqs else None
			lastCommand = lastOutSeq[-1] if lastOutSeq else None
			if not lastCommand or isinstance(lastCommand, (EndUtteranceCommand, ConfigProfileTriggerCommand)):
				# It doesn't make sense to start with or repeat EndUtteranceCommands.
				# We also don't want an EndUtteranceCommand immediately after a ConfigProfileTriggerCommand.
				return outSeq
			if not isinstance(lastCommand, IndexCommand):
				# Add an index so we know when we've reached the end of this utterance.
				speechIndex = next(self._indexCounter)
				lastOutSeq.append(IndexCommand(speechIndex))
			outSeqs.append([EndUtteranceCommand()])
			return outSeq

		for command in inSeq:
			if isinstance(command, BaseCallbackCommand):
				# When the synth reaches this point, we want to call the callback.
				speechIndex = next(self._indexCounter)
				outSeq.append(IndexCommand(speechIndex))
				self._indexesToCallbacks[speechIndex] = command
				# We split at indexes so we easily know what has completed speaking.
				outSeqs.append(outSeq)
				outSeq = []
				continue
			if isinstance(command, ConfigProfileTriggerCommand):
				if not command.trigger.hasProfile:
					# Ignore triggers that have no associated profile.
					continue
				if command.enter and command.trigger in enteredTriggers:
					log.debugWarning("Request to enter trigger which has already been entered: %r" % command.trigger.spec)
					continue
				if not command.enter and command.trigger not in enteredTriggers:
					log.debugWarning("Request to exit trigger which wasn't entered: %r" % command.trigger.spec)
					continue
				outSeq = ensureEndUtterance(outSeq)
				outSeqs.append([command])
				if command.enter:
					enteredTriggers.append(command.trigger)
				else:
					enteredTriggers.remove(command.trigger)
				continue
			if isinstance(command, EndUtteranceCommand):
				outSeq = ensureEndUtterance(outSeq)
				continue
			if isinstance(command, SynthParamCommand):
				paramTracker.update(command)
			outSeq.append(command)
		# Add the last sequence and make sure the sequence ends the utterance.
		ensureEndUtterance(outSeq)
		# Exit any profile triggers the caller didn't exit.
		for trigger in reversed(enteredTriggers):
			command = ConfigProfileTriggerCommand(trigger, False)
			outSeqs.append([command])
		return outSeqs

	def _pushNextSpeech(self, doneSpeaking):
		queue = self._getNextPriority()
		if not queue:
			# No more speech.
			self._curPriQueue = None
			return
		if not self._curPriQueue:
			# First utterance after no speech.
			self._curPriQueue = queue
		elif queue.priority > self._curPriQueue.priority:
			# Preempted by higher priority speech.
			if self._curPriQueue.enteredProfileTriggers:
				if not doneSpeaking:
					# Wait for the synth to finish speaking.
					# _handleDoneSpeaking will call us again.
					self._shouldPushWhenDoneSpeaking = True
					return
				self._exitProfileTriggers(self._curPriQueue.enteredProfileTriggers)
			self._curPriQueue = queue
		elif queue.priority < self._curPriQueue.priority:
			# Resuming a preempted, lower priority queue.
			if queue.enteredProfileTriggers:
				if not doneSpeaking:
					# Wait for the synth to finish speaking.
					# _handleDoneSpeaking will call us again.
					self._shouldPushWhenDoneSpeaking = True
					return
				self._restoreProfileTriggers(queue.enteredProfileTriggers)
			self._curPriQueue = queue
		while queue.pendingSequences and isinstance(queue.pendingSequences[0][0], ConfigProfileTriggerCommand):
			if not doneSpeaking:
				# Wait for the synth to finish speaking.
				# _handleDoneSpeaking will call us again.
				self._shouldPushWhenDoneSpeaking = True
				return
			self._switchProfile()
		if not queue.pendingSequences:
			# The last commands in this queue were profile switches.
			# Call this method again in case other queues are waiting.
			return self._pushNextSpeech(True)
		seq = self._buildNextUtterance()
		if seq:
			getSynth().speak(seq)

	def _getNextPriority(self):
		"""Get the highest priority queue containing pending speech.
		"""
		for priority in SPEECH_PRIORITIES:
			queue = self._priQueues.get(priority)
			if not queue:
				continue
			if queue.pendingSequences:
				return queue
		return None

	def _buildNextUtterance(self):
		"""Since an utterance might be split over several sequences,
		build a complete utterance to pass to the synth.
		"""
		utterance = []
		# If this utterance was preempted by higher priority speech,
		# apply any parameters changed before the preemption.
		params = self._curPriQueue.paramTracker.getChanged()
		utterance.extend(params)
		for seq in self._curPriQueue.pendingSequences:
			if isinstance(seq[0], EndUtteranceCommand):
				# The utterance ends here.
				break
			utterance.extend(seq)
		return utterance

	def _onSynthIndexReached(self, synth=None, index=None):
		if synth != getSynth():
			return
		# This needs to be handled in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self._handleIndex, index)

	def _removeCompletedFromQueue(self, index):
		"""Removes completed speech sequences from the queue.
		@param index: The index just reached indicating a completed sequence.
		@return: Tuple of (valid, endOfUtterance),
			where valid indicates whether the index was valid and
			endOfUtterance indicates whether this sequence was the end of the current utterance.
		@rtype: (bool, bool)
		"""
		# Find the sequence that just completed speaking.
		if not self._curPriQueue:
			# No speech in progress. Probably from a previous utterance which was cancelled.
			return False, False
		for seqIndex, seq in enumerate(self._curPriQueue.pendingSequences):
			lastCommand = seq[-1] if isinstance(seq, list) else None
			if isinstance(lastCommand, IndexCommand) and index >= lastCommand.index:
				endOfUtterance = isinstance(self._curPriQueue.pendingSequences[seqIndex + 1][0], EndUtteranceCommand)
				if endOfUtterance:
					# Remove the EndUtteranceCommand as well.
					seqIndex += 1
				break # Found it!
		else:
			# Unknown index. Probably from a previous utterance which was cancelled.
			return False, False
		if endOfUtterance:
			# These params may not apply to the next utterance if it was queued separately,
			# so reset the tracker.
			# The next utterance will include the commands again if they do still apply.
			self._curPriQueue.paramTracker = ParamChangeTracker()
		else:
			# Keep track of parameters changed so far.
			# This is necessary in case this utterance is preempted by higher priority speech.
			for seqIndex in xrange(seqIndex + 1):
				seq = self._curPriQueue.pendingSequences[seqIndex]
				for command in seq:
					if isinstance(command, SynthParamCommand):
						self._curPriQueue.paramTracker.update(command)
		# This sequence is done, so we don't need to track it any more.
		del self._curPriQueue.pendingSequences[:seqIndex + 1]
		return True, endOfUtterance

	def _handleIndex(self, index):
		valid, endOfUtterance = self._removeCompletedFromQueue(index)
		if not valid:
			return
		callbackCommand = self._indexesToCallbacks.pop(index, None)
		if callbackCommand:
			try:
				callbackCommand.run()
			except:
				log.exception("Error running speech callback")
		if endOfUtterance:
			self._pushNextSpeech(False)

	def _onSynthDoneSpeaking(self, synth=None):
		if synth != getSynth():
			return
		# This needs to be handled in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self._handleDoneSpeaking)

	def _handleDoneSpeaking(self):
		if self._shouldPushWhenDoneSpeaking:
			self._shouldPushWhenDoneSpeaking = False
			self._pushNextSpeech(True)

	def _switchProfile(self):
		command = self._curPriQueue.pendingSequences.pop(0)[0]
		assert isinstance(command, ConfigProfileTriggerCommand), "First pending command should be a ConfigProfileTriggerCommand"
		if not command.enter and command.trigger not in self._curPriQueue.enteredProfileTriggers:
			# speechCompat: We already exited this profile due to synth incompatibility.
			return
		if command.enter:
			try:
				command.trigger.enter()
			except:
				log.exception("Error entering new trigger %r" % command.trigger.spec)
			self._curPriQueue.enteredProfileTriggers.append(command.trigger)
		else:
			try:
				command.trigger.exit()
			except:
				log.exception("Error exiting active trigger %r" % command.trigger.spec)
			self._curPriQueue.enteredProfileTriggers.remove(command.trigger)
		synthDriverHandler.handleConfigProfileSwitch()
		if command.enter and shouldUseCompatCodeForIndexing():
			log.debugWarning("Synth in new profile doesn't support indexing. Exiting trigger.")
			try:
				command.trigger.exit()
			except:
				log.exception("Error exiting trigger %r" % command.trigger.spec)
			assert self._curPriQueue.enteredProfileTriggers[-1] is command.trigger, "Last profile trigger should be the trigger just entered"
			del self._curPriQueue.enteredProfileTriggers[-1]
			synthDriverHandler.handleConfigProfileSwitch()

	def _exitProfileTriggers(self, triggers):
		for trigger in reversed(triggers):
			try:
				trigger.exit()
			except:
				log.exception("Error exiting profile trigger %r" % command.trigger.spec)
		synthDriverHandler.handleConfigProfileSwitch()

	def _restoreProfileTriggers(self, triggers):
		for trigger in triggers:
			try:
				trigger.enter()
			except:
				log.exception("Error entering profile trigger %r" % command.trigger.spec)
		synthDriverHandler.handleConfigProfileSwitch()

	def cancel(self):
		getSynth().cancel()
		if self._curPriQueue and self._curPriQueue.enteredProfileTriggers:
			self._exitProfileTriggers(self._curPriQueue.enteredProfileTriggers)
		self._reset()

#: The singleton _SpeechManager instance used for speech functions.
#: @type: L{_SpeechManager}
_manager = _SpeechManager()
