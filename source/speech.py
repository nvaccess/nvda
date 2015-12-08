# -*- coding: UTF-8 -*-
#speech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2014 NV Access Limited, Peter Vágner, Aleksey Sadovoy

"""High-level functions to speak information.
""" 

import itertools
import weakref
import unicodedata
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
# The REASON_* constants in this module are deprecated and will be removed in a future release.
# Use controlTypes.REASON_* instead.
from controlTypes import REASON_FOCUS, REASON_FOCUSENTERED, REASON_MOUSE, REASON_QUERY, REASON_CHANGE, REASON_MESSAGE, REASON_SAYALL, REASON_CARET, REASON_ONLYCACHE

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
	"""Gets the last index passed by the synthesizer. Indexing is used so that its possible to find out when a certain peace of text has been spoken yet. Usually the character position of the text is passed to speak functions as the index.
@returns: the last index encountered
@rtype: int
"""
	return getSynth().lastIndex

def cancelSpeech():
	"""Interupts the synthesizer from currently speaking"""
	global beenCanceled, isPaused, _speakSpellingGenerator
	# Import only for this function to avoid circular import.
	import sayAllHandler
	sayAllHandler.stop()
	speakWithoutPauses._pendingSpeechSequence=[]
	speakWithoutPauses.lastSentIndex=None
	if _speakSpellingGenerator:
		_speakSpellingGenerator.close()
	if beenCanceled:
		return
	elif speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		return
	getSynth().cancel()
	beenCanceled=True
	isPaused=False

def pauseSpeech(switch):
	global isPaused, beenCanceled
	getSynth().pause(switch)
	isPaused=switch
	beenCanceled=False

def speakMessage(text,index=None):
	"""Speaks a given message.
@param text: the message to speak
@type text: string
@param index: the index to mark this current text with, its best to use the character position of the text if you know it 
@type index: int
"""
	speakText(text,index=index,reason=controlTypes.REASON_MESSAGE)

def getCurrentLanguage():
	try:
		language=getSynth().language if config.conf['speech']['trustVoiceLanguage'] else None
	except NotImplementedError:
		language=None
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

_speakSpellingGenerator=None

def speakSpelling(text,locale=None,useCharacterDescriptions=False):
	global beenCanceled, _speakSpellingGenerator
	import speechViewer
	if speechViewer.isActive:
		speechViewer.appendText(text)
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	defaultLanguage=getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		return getSynth().speak((_("blank"),))
	if not text.isspace():
		text=text.rstrip()
	if _speakSpellingGenerator and _speakSpellingGenerator.gi_frame:
		_speakSpellingGenerator.send((text,locale,useCharacterDescriptions))
	else:
		_speakSpellingGenerator=_speakSpellingGen(text,locale,useCharacterDescriptions)
		try:
			# Speak the first character before this function returns.
			next(_speakSpellingGenerator)
		except StopIteration:
			return
		queueHandler.registerGeneratorObject(_speakSpellingGenerator)

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

def _speakSpellingGen(text,locale,useCharacterDescriptions):
	synth=getSynth()
	synthConfig=config.conf["speech"][synth.name]
	buf=[(text,locale,useCharacterDescriptions)]
	for text,locale,useCharacterDescriptions in buf:
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
				#Consider changing to multiple synth speech calls
				char=charDesc[0] if textLength>1 else u"\u3001".join(charDesc)
			else:
				char=characterProcessing.processSpeechSymbol(locale,char)
			if uppercase and synthConfig["sayCapForCapitals"]:
				# Translators: cap will be spoken before the given letter when it is capitalized.
				char=_("cap %s")%char
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				oldPitch=synthConfig["pitch"]
				synth.pitch=max(0,min(oldPitch+synthConfig["capPitchChange"],100))
			count = len(char)
			index=count+1
			log.io("Speaking character %r"%char)
			speechSequence=[LangChangeCommand(locale)] if config.conf['speech']['autoLanguageSwitching'] else []
			if len(char) == 1 and synthConfig["useSpellingFunctionality"]:
				speechSequence.append(CharacterModeCommand(True))
			if index is not None:
				speechSequence.append(IndexCommand(index))
			speechSequence.append(char)
			synth.speak(speechSequence)
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				synth.pitch=oldPitch
			while textLength>1 and (isPaused or getLastSpeechIndex()!=index):
				for x in xrange(2):
					args=yield
					if args: buf.append(args)
			if uppercase and  synthConfig["beepForCapitals"]:
				tones.beep(2000,50)
		args=yield
		if args: buf.append(args)

def speakObjectProperties(obj,reason=controlTypes.REASON_QUERY,index=None,**allowedProperties):
	if speechMode==speechMode_off:
		return
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
	#Get the speech text for the properties we want to speak, and then speak it
	text=getSpeechTextForProperties(reason,**newPropertyValues)
	if text:
		speakText(text,index=index)

def speakObject(obj,reason=controlTypes.REASON_QUERY,index=None):
	from NVDAObjects import NVDAObjectTextInfo
	role=obj.role
	isEditable=(reason!=controlTypes.REASON_FOCUSENTERED and obj.TextInfo!=NVDAObjectTextInfo and (role in (controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_TERMINAL) or controlTypes.STATE_EDITABLE in obj.states))
	allowProperties={'name':True,'role':True,'states':True,'value':True,'description':True,'keyboardShortcut':True,'positionInfo_level':True,'positionInfo_indexInGroup':True,'positionInfo_similarItemsInGroup':True,"cellCoordsText":True,"rowNumber":True,"columnNumber":True,"includeTableCellCoords":True,"columnCount":True,"rowCount":True,"rowHeaderText":True,"columnHeaderText":True}

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
	if isEditable:
		allowProperties['value']=False

	speakObjectProperties(obj,reason=reason,index=index,**allowProperties)
	if reason==controlTypes.REASON_ONLYCACHE:
		return
	if isEditable:
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
			if not info.isCollapsed:
				# Translators: This is spoken to indicate what has been selected. for example 'selected hello world'
				speakSelectionMessage(_("selected %s"),info.text)
			else:
				info.expand(textInfos.UNIT_LINE)
				speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		except:
			newInfo=obj.makeTextInfo(textInfos.POSITION_ALL)
			speakTextInfo(newInfo,unit=textInfos.UNIT_PARAGRAPH,reason=controlTypes.REASON_CARET)
	elif role==controlTypes.ROLE_MATH:
		import mathPres
		mathPres.ensureInit()
		if mathPres.speechProvider:
			try:
				speak(mathPres.speechProvider.getSpeechForMathMl(obj.mathMl))
			except (NotImplementedError, LookupError):
				pass

def speakText(text,index=None,reason=controlTypes.REASON_MESSAGE,symbolLevel=None):
	"""Speaks some text.
	@param text: The text to speak.
	@type text: str
	@param index: The index to mark this text with, which can be used later to determine whether this piece of text has been spoken.
	@type index: int
	@param reason: The reason for this speech; one of the controlTypes.REASON_* constants.
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
	"""
	speechSequence=[]
	if index is not None:
		speechSequence.append(IndexCommand(index))
	if text is not None:
		if isBlank(text):
			# Translators: This is spoken when the line is considered blank.
			text=_("blank")
		speechSequence.append(text)
	speak(speechSequence,symbolLevel=symbolLevel)

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
def getIndentationSpeech(indentation):
	"""Retrieves the phrase to be spoken for a given string of indentation.
	@param indentation: The string of indentation.
	@type indentation: basestring
	@return: The phrase to be spoken.
	@rtype: unicode
	"""
	# Translators: no indent is spoken when the user moves from a line that has indentation, to one that 
	# does not.
	if not indentation:
		# Translators: This is spoken when the given line has no indentation.
		return _("no indent")

	res = []
	locale=languageHandler.getLanguage()
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

	return " ".join(res)

def speak(speechSequence,symbolLevel=None):
	"""Speaks a sequence of text and speech commands
	@param speechSequence: the sequence of text and L{SpeechCommand} objects to speak
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
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
	getSynth().speak(speechSequence)

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
	locale=languageHandler.getLanguage()
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

def speakTypedCharacters(ch):
	global curWordChars;
	typingIsProtected=api.isTypingProtected()
	if typingIsProtected:
		realChar="*"
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
	if config.conf["keyboard"]["speakTypedCharacters"] and ord(ch)>=32:
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

def speakTextInfo(info,useCache=True,formatConfig=None,unit=None,reason=controlTypes.REASON_QUERY,index=None,onlyInitialFields=False,suppressBlanks=False):
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
	reportIndentation=unit==textInfos.UNIT_LINE and formatConfig["reportLineIndentation"]

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

	#Get speech text for any fields in the old controlFieldStack that are not in the new controlFieldStack 
	endingBlock=False
	for count in reversed(xrange(commonFieldCount,len(controlFieldStackCache))):
		text=info.getControlFieldSpeech(controlFieldStackCache[count],controlFieldStackCache[0:count],"end_removedFromControlFieldStack",formatConfig,extraDetail,reason=reason)
		if text:
			speechSequence.append(text)
		if not endingBlock and reason==controlTypes.REASON_SAYALL:
			endingBlock=bool(int(controlFieldStackCache[count].get('isBlock',0)))
	if endingBlock:
		speechSequence.append(SpeakWithoutPausesBreakCommand())
	# The TextInfo should be considered blank if we are only exiting fields (i.e. we aren't entering any new fields and there is no text).
	isTextBlank=True

	# Even when there's no speakable text, we still need to notify the synth of the index.
	if index is not None:
		speechSequence.append(IndexCommand(index))

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
	text=getFormatFieldSpeech(newFormatField,formatFieldAttributesCache,formatConfig,unit=unit,extraDetail=extraDetail)
	if text:
		speechSequence.append(text)
	if autoLanguageSwitching:
		language=newFormatField.get('language')
		speechSequence.append(LangChangeCommand(language))
		lastLanguage=language

	if onlyInitialFields or (unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD) and len(textWithFields)>0 and len(textWithFields[0])==1 and all((isinstance(x,textInfos.FieldCommand) and x.command=="controlEnd") for x in itertools.islice(textWithFields,1,None) )): 
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
				fieldText=getFormatFieldSpeech(command.field,formatFieldAttributesCache,formatConfig,unit=unit,extraDetail=extraDetail)
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
		indentationSpeech=getIndentationSpeech(allIndentation)
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

	if speechSequence:
		if reason==controlTypes.REASON_SAYALL:
			speakWithoutPauses(speechSequence)
		else:
			speak(speechSequence)

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
	if speakRole and (reason not in (controlTypes.REASON_SAYALL,controlTypes.REASON_CARET,controlTypes.REASON_FOCUS) or not (name or value or cellCoordsText or rowNumber or columnNumber) or role not in controlTypes.silentRolesOnFocus) and (role!=controlTypes.ROLE_MATH or reason not in (controlTypes.REASON_CARET,controlTypes.REASON_SAYALL)):
		textList.append(controlTypes.roleLabels[role])
	if value:
		textList.append(value)
	states=propertyValues.get('states')
	realStates=propertyValues.get('_states',states)
	if states is not None:
		positiveStates=controlTypes.processPositiveStates(role,realStates,reason,states)
		textList.extend([controlTypes.stateLabels[x] for x in positiveStates])
	if 'negativeStates' in propertyValues:
		negativeStates=propertyValues['negativeStates']
	else:
		negativeStates=None
	if negativeStates is not None or (reason != controlTypes.REASON_CHANGE and states is not None):
		negativeStates=controlTypes.processNegativeStates(role, realStates, reason, negativeStates)
		if controlTypes.STATE_DROPTARGET in negativeStates:
			# "not drop target" doesn't make any sense, so use a custom message.
			# Translators: Reported when drag and drop is finished.
			# This is only reported for objects which support accessible drag and drop.
			textList.append(_("done dragging"))
			negativeStates.discard(controlTypes.STATE_DROPTARGET)
		# Translators: Indicates that a particular state on an object is negated.
		# Separate strings have now been defined for commonly negated states (e.g. not selected and not checked),
		# but this still might be used in some other cases.
		# %s will be replaced with the negated state.
		textList.extend([controlTypes.negativeStateLabels.get(x, _("not %s")%controlTypes.stateLabels[x]) for x in negativeStates])
	if 'description' in propertyValues:
		textList.append(propertyValues['description'])
	if 'keyboardShortcut' in propertyValues:
		textList.append(propertyValues['keyboardShortcut'])
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
	if includeTableCellCoords and cellCoordsText:
		textList.append(cellCoordsText)
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
		return " ".join((roleText, getSpeechTextForProperties(_tableID=tableID, rowCount=attrs.get("table-rowcount"), columnCount=attrs.get("table-columncount")),levelText))
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
			+ (" %s" % stateText if stateText else ""))

	# General cases
	elif (
		(speakEntry and ((speakContentFirst and fieldType in ("end_relative","end_inControlFieldStack")) or (not speakContentFirst and fieldType in ("start_addedToControlFieldStack","start_relative"))))
		or (speakWithinForLine and not speakContentFirst and not extraDetail and fieldType=="start_inControlFieldStack")
	):
		return CHUNK_SEPARATOR.join([x for x in nameText,(stateText if speakStatesFirst else roleText),(roleText if speakStatesFirst else stateText),valueText,descriptionText,levelText,keyboardShortcutText if x])
	elif fieldType in ("end_removedFromControlFieldStack","end_relative") and roleText and ((not extraDetail and speakExitForLine) or (extraDetail and speakExitForOther)):
		# Translators: Indicates end of something (example output: at the end of a list, speaks out of list).
		return _("out of %s")%roleText

	# Special cases
	elif not extraDetail and not speakEntry and fieldType in ("start_addedToControlFieldStack","start_relative")  and controlTypes.STATE_CLICKABLE in states: 
		# Clickable.
		return getSpeechTextForProperties(states=set([controlTypes.STATE_CLICKABLE]))

	else:
		return ""

def getFormatFieldSpeech(attrs,attrsCache=None,formatConfig=None,unit=None,extraDetail=False):
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]
	textList=[]
	if formatConfig["reportTables"]:
		tableInfo=attrs.get("table-info")
		oldTableInfo=attrsCache.get("table-info") if attrsCache is not None else None
		text=getTableInfoSpeech(tableInfo,oldTableInfo,extraDetail=extraDetail)
		if text:
			textList.append(text)
	if  formatConfig["reportPage"]:
		pageNumber=attrs.get("page-number")
		oldPageNumber=attrsCache.get("page-number") if attrsCache is not None else None
		if pageNumber and pageNumber!=oldPageNumber:
			# Translators: Indicates the page number in a document.
			# %s will be replaced with the page number.
			text=_("page %s")%pageNumber
			textList.append(text)
	if  formatConfig["reportHeadings"]:
		headingLevel=attrs.get("heading-level")
		oldHeadingLevel=attrsCache.get("heading-level") if attrsCache is not None else None
		if headingLevel and headingLevel!=oldHeadingLevel:
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
		backgroundColorTwo=attrs.get("background-colorTwo")
		oldBackgroundColorTwo=attrsCache.get("background-colorTwo") if attrsCache is not None else None
		backgroundPattern=attrs.get("background-pattern")
		oldBackgroundPattern=attrsCache.get("background-pattern") if attrsCache is not None else None
		if color and backgroundColor and backgroundColorTwo and color!=oldColor and backgroundColor!=oldBackgroundColor and backgroundColorTwo!=oldBackgroundColorTwo:
			# Translators: Reported when both the text and the two background colors change .Two background colors are present when gradient pattern is applied to cell
			# {color} will be replaced with the text color.
			# {backgroundColor} will be replaced with the first background color.
			# {backgroundColorTwo} will be replaced with the second background color.
			textList.append(_("{color} on {backgroundColor} to {backgroundColorTwo}").format(color=color.name if isinstance(color,colors.RGB) else unicode(color),backgroundColor=backgroundColor.name if isinstance(backgroundColor,colors.RGB) else unicode(backgroundColor),backgroundColorTwo=backgroundColorTwo.name if isinstance(backgroundColorTwo,colors.RGB) else unicode(backgroundColorTwo)))
		elif color and backgroundColor and color!=oldColor and backgroundColor!=oldBackgroundColor:
			# Translators: Reported when both the text and background colors change.
			# {color} will be replaced with the text color.
			# {backgroundColor} will be replaced with the background color.
			textList.append(_("{color} on {backgroundColor}").format(
				color=color.name if isinstance(color,colors.RGB) else unicode(color),
				backgroundColor=backgroundColor.name if isinstance(backgroundColor,colors.RGB) else unicode(backgroundColor)))
		elif color and color!=oldColor:
			# Translators: Reported when the text color changes (but not the background color).
			# {color} will be replaced with the text color.
			textList.append(_("{color}").format(color=color.name if isinstance(color,colors.RGB) else unicode(color)))
		elif backgroundColor and backgroundColor!=oldBackgroundColor:
			# Translators: Reported when the background color changes (but not the text color).
			# {backgroundColor} will be replaced with the background color.
			textList.append(_("{backgroundColor} background").format(backgroundColor=backgroundColor.name if isinstance(backgroundColor,colors.RGB) else unicode(backgroundColor)))
		if backgroundPattern and backgroundPattern!=oldBackgroundPattern:
			textList.append(_("{pattern} background pattern").format(pattern=backgroundPattern))
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
			# Translators: Reported when text is formatted with strikethrough.
			# See http://en.wikipedia.org/wiki/Strikethrough
			text=(_("strikethrough") if strikethrough
				# Translators: Reported when text is formatted without strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				else _("no strikethrough"))
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
	if unit in (textInfos.UNIT_LINE,textInfos.UNIT_SENTENCE,textInfos.UNIT_PARAGRAPH,textInfos.UNIT_READINGCHUNK):
		linePrefix=attrs.get("line-prefix")
		if linePrefix:
			textList.append(linePrefix)
	if attrsCache is not None:
		attrsCache.clear()
		attrsCache.update(attrs)
	return CHUNK_SEPARATOR.join(textList)

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
	"""
	lastStartIndex=0
	#Break on all explicit break commands
	if detectBreaks and speechSequence:
		sequenceLen=len(speechSequence)
		for index in xrange(sequenceLen):
			if isinstance(speechSequence[index],SpeakWithoutPausesBreakCommand):
				if index>0 and lastStartIndex<index:
					speakWithoutPauses(speechSequence[lastStartIndex:index],detectBreaks=False)
				speakWithoutPauses(None)
				lastStartIndex=index+1
		if lastStartIndex<sequenceLen:
			speakWithoutPauses(speechSequence[lastStartIndex:],detectBreaks=False)
		return
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
	#Scan the final speech sequence backwards
	for item in reversed(finalSpeechSequence):
		if isinstance(item,IndexCommand):
			speakWithoutPauses.lastSentIndex=item.index
			break
	if finalSpeechSequence:
		speak(finalSpeechSequence)
speakWithoutPauses.lastSentIndex=None
speakWithoutPauses._pendingSpeechSequence=[]


class SpeechCommand(object):
	"""
	The base class for objects that can be inserted between string of text for parituclar speech functions that convey  things such as indexing or voice parameter changes.
	"""

class IndexCommand(SpeechCommand):
	"""Represents an index within some speech."""

	def __init__(self,index):
		"""
		@param index: the value of this index
		@type index: integer
		"""
		if not isinstance(index,int): raise ValueError("index must be int, not %s"%type(index))
		self.index=index

	def __repr__(self):
		return "IndexCommand(%r)" % self.index

class CharacterModeCommand(object):
	"""Turns character mode on and off for speech synths."""

	def __init__(self,state):
		"""
		@param state: if true character mode is on, if false its turned off.
		@type state: boolean
		"""
		if not isinstance(state,bool): raise ValueError("state must be boolean, not %s"%type(state))
		self.state=state

	def __repr__(self):
		return "CharacterModeCommand(%r)" % self.state

class LangChangeCommand(SpeechCommand):
	"""A command to switch the language within speech."""

	def __init__(self,lang):
		"""
		@param lang: the language to switch to: If None then the NVDA locale will be used.
		@type lang: string
		"""
		self.lang=lang # if lang else languageHandler.getLanguage()

	def __repr__(self):
		return "LangChangeCommand (%r)"%self.lang

class SpeakWithoutPausesBreakCommand(SpeechCommand):
	"""Forces speakWithoutPauses to flush its buffer and therefore break the sentence at this point.
	This should only be used with the L{speakWithoutPauses} function.
	This will be removed during processing.
	"""

class BreakCommand(SpeechCommand):
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

class PitchCommand(SpeechCommand):
	"""Change the pitch of the voice.
	"""

	def __init__(self, multiplier=1):
		"""
		@param multiplier: The number by which to multiply the current pitch setting;
			e.g. 0.5 is half, 1 returns to the current pitch setting.
		@param multiplier: int/float
		"""
		self.multiplier = multiplier

	def __repr__(self):
		return "PitchCommand(multiplier=%g)" % self.multiplier

class VolumeCommand(SpeechCommand):
	"""Change the volume of the voice.
	"""

	def __init__(self, multiplier=1):
		"""
		@param multiplier: The number by which to multiply the current volume setting;
			e.g. 0.5 is half, 1 returns to the current volume setting.
		@param multiplier: int/float
		"""
		self.multiplier = multiplier

	def __repr__(self):
		return "VolumeCommand(multiplier=%g)" % self.multiplier

class RateCommand(SpeechCommand):
	"""Change the rate of the voice.
	"""

	def __init__(self, multiplier=1):
		"""
		@param multiplier: The number by which to multiply the current rate setting;
			e.g. 0.5 is half, 1 returns to the current rate setting.
		@param multiplier: int/float
		"""
		self.multiplier = multiplier

	def __repr__(self):
		return "RateCommand(multiplier=%g)" % self.multiplier

class PhonemeCommand(SpeechCommand):
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
