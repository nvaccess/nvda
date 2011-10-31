#speech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>, Peter Vágner <peter.v@datagate.sk>, Aleksey Sadovoy <lex@onm.su>

"""High-level functions to speak information.
""" 

import colors
import XMLFormatting
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

REASON_FOCUS=1
REASON_MOUSE=2
REASON_QUERY=3
REASON_CHANGE=4
REASON_MESSAGE=5
REASON_SAYALL=6
REASON_CARET=7
REASON_DEBUG=8
REASON_ONLYCACHE=9
REASON_FOCUSENTERED=10

#: The string used to separate distinct chunks of text when multiple chunks should be spoken without pauses.
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
	speakText(text,index=index,reason=REASON_MESSAGE)

def getCurrentLanguage():
	language=getSynth().language if config.conf['speech']['autoLanguageSwitching'] else None
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

def _speakSpellingGen(text,locale,useCharacterDescriptions):
	synth=getSynth()
	synthConfig=config.conf["speech"][synth.name]
	buf=[(text,locale,useCharacterDescriptions)]
	for text,locale,useCharacterDescriptions in buf:
		textLength=len(text)
		for count,char in enumerate(text): 
			uppercase=char.isupper()
			charDesc=None
			if useCharacterDescriptions:
				charDesc=characterProcessing.getCharacterDescription(locale,char.lower())
			if charDesc:
				#Consider changing to multiple synth speech calls
				char=charDesc[0] if textLength>1 else u"\u3001".join(charDesc)
			else:
				char=characterProcessing.processSpeechSymbol(locale,char)
			if uppercase and synthConfig["sayCapForCapitals"]:
				char=_("cap %s")%char
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				oldPitch=synthConfig["pitch"]
				synth.pitch=max(0,min(oldPitch+synthConfig["capPitchChange"],100))
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

def speakObjectProperties(obj,reason=REASON_QUERY,index=None,**allowedProperties):
	if speechMode==speechMode_off:
		return
	#Fetch the values for all wanted properties
	newPropertyValues={}
	positionInfo=None
	for name,value in allowedProperties.iteritems():
		if name.startswith('positionInfo_') and value:
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
	if reason==REASON_ONLYCACHE:
		return
	#If only speaking change, then filter out all values that havn't changed
	if reason==REASON_CHANGE:
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
	#Get the speech text for the properties we want to speak, and then speak it
	text=getSpeechTextForProperties(reason,**newPropertyValues)
	if text:
		speakText(text,index=index)

def speakObject(obj,reason=REASON_QUERY,index=None):
	from NVDAObjects import NVDAObjectTextInfo
	isEditable=(reason!=REASON_FOCUSENTERED and obj.TextInfo!=NVDAObjectTextInfo and (obj.role in (controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_TERMINAL) or controlTypes.STATE_EDITABLE in obj.states))
	allowProperties={'name':True,'role':True,'states':True,'value':True,'description':True,'keyboardShortcut':True,'positionInfo_level':True,'positionInfo_indexInGroup':True,'positionInfo_similarItemsInGroup':True,"rowNumber":True,"columnNumber":True,"columnCount":True,"rowCount":True}

	if reason==REASON_FOCUSENTERED:
		allowProperties["value"]=False
		allowProperties["keyboardShortcut"]=False
		allowProperties["positionInfo_level"]=False
		# Aside from excluding some properties, focus entered should be spoken like focus.
		reason=REASON_FOCUS

	if not config.conf["presentation"]["reportObjectDescriptions"]:
		allowProperties["description"]=False
	if not config.conf["presentation"]["reportKeyboardShortcuts"]:
		allowProperties["keyboardShortcut"]=False
	if not config.conf["presentation"]["reportObjectPositionInformation"]:
		allowProperties["positionInfo_level"]=False
		allowProperties["positionInfo_indexInGroup"]=False
		allowProperties["positionInfo_similarItemsInGroup"]=False
	if reason!=REASON_QUERY:
		allowProperties["rowCount"]=False
		allowProperties["columnCount"]=False
		if (not config.conf["documentFormatting"]["reportTables"]
				or not config.conf["documentFormatting"]["reportTableCellCoords"]
				or obj.tableCellCoordsInName):
			allowProperties["rowNumber"]=False
			allowProperties["columnNumber"]=False
	if isEditable:
		allowProperties['value']=False

	speakObjectProperties(obj,reason=reason,index=index,**allowProperties)
	if reason!=REASON_ONLYCACHE and isEditable:
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
			if not info.isCollapsed:
				speakSelectionMessage(_("selected %s"),info.text)
			else:
				info.expand(textInfos.UNIT_LINE)
				speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=reason)
		except:
			newInfo=obj.makeTextInfo(textInfos.POSITION_ALL)
			speakTextInfo(newInfo,unit=textInfos.UNIT_PARAGRAPH,reason=reason)

def speakText(text,index=None,reason=REASON_MESSAGE,symbolLevel=None):
	"""Speaks some text.
	@param text: The text to speak.
	@type text: str
	@param index: The index to mark this text with, which can be used later to determine whether this piece of text has been spoken.
	@type index: int
	@param reason: The reason for this speech; one of the REASON_* constants.
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
	"""
	speechSequence=[]
	if index is not None:
		speechSequence.append(IndexCommand(index))
	if text is not None:
		if isBlank(text):
			text=_("blank")
		speechSequence.append(text)
	speak(speechSequence,symbolLevel=symbolLevel)

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
	for index in xrange(len(speechSequence)):
		item=speechSequence[index]
		if autoLanguageSwitching and isinstance(item,LangChangeCommand):
			curLanguage=item.lang
		if isinstance(item,basestring):
			speechSequence[index]=processText(curLanguage,item,symbolLevel)+" "
	getSynth().speak(speechSequence)

def speakSelectionMessage(message,text):
	if len(text) < 512:
		speakMessage(message % text)
	else:
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
				speakSelectionMessage(_("selecting %s"),text)
		elif len(selectedTextList)>0:
			text=newInfo.text
			if len(text)==1:
				text=characterProcessing.processSpeechSymbol(locale,text)
			speakSelectionMessage(_("selected %s"),text)
	if speakUnselected:
		if not generalize:
			for text in unselectedTextList:
				if  len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				speakSelectionMessage(_("unselecting %s"),text)
		elif len(unselectedTextList)>0:
			speakMessage(_("selection removed"))
			if not newInfo.isCollapsed:
				text=newInfo.text
				if len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				speakSelectionMessage(_("selected %s"),text)

def speakTypedCharacters(ch):
	global curWordChars;
	if api.isTypingProtected():
		realChar="*"
	else:
		realChar=ch
	if ch.isalnum():
		curWordChars.append(realChar)
	elif ch=="\b":
		# Backspace, so remove the last character from our buffer.
		del curWordChars[-1:]
	elif len(curWordChars)>0:
		typedWord="".join(curWordChars)
		curWordChars=[]
		if log.isEnabledFor(log.IO):
			log.io("typed word: %s"%typedWord)
		if config.conf["keyboard"]["speakTypedWords"]: 
			speakText(typedWord)
	if config.conf["keyboard"]["speakTypedCharacters"] and ord(ch)>=32:
		speakSpelling(realChar)

silentRolesOnFocus=set([
	controlTypes.ROLE_PANE,
	controlTypes.ROLE_ROOTPANE,
	controlTypes.ROLE_FRAME,
	controlTypes.ROLE_UNKNOWN,
	controlTypes.ROLE_APPLICATION,
	controlTypes.ROLE_TABLECELL,
	controlTypes.ROLE_LISTITEM,
	controlTypes.ROLE_MENUITEM,
	controlTypes.ROLE_CHECKMENUITEM,
	controlTypes.ROLE_TREEVIEWITEM,
])

silentValuesForRoles=set([
	controlTypes.ROLE_CHECKBOX,
	controlTypes.ROLE_RADIOBUTTON,
	controlTypes.ROLE_LINK,
	controlTypes.ROLE_MENUITEM,
	controlTypes.ROLE_APPLICATION,
])

def processPositiveStates(role, states, reason, positiveStates):
	positiveStates = positiveStates.copy()
	# The user never cares about certain states.
	if role==controlTypes.ROLE_EDITABLETEXT:
		positiveStates.discard(controlTypes.STATE_EDITABLE)
	if role!=controlTypes.ROLE_LINK:
		positiveStates.discard(controlTypes.STATE_VISITED)
	positiveStates.discard(controlTypes.STATE_SELECTABLE)
	positiveStates.discard(controlTypes.STATE_FOCUSABLE)
	positiveStates.discard(controlTypes.STATE_CHECKABLE)
	if controlTypes.STATE_DRAGGING in positiveStates:
		# It's obvious that the control is draggable if it's being dragged.
		positiveStates.discard(controlTypes.STATE_DRAGGABLE)
	if role == controlTypes.ROLE_COMBOBOX:
		# Combo boxes inherently have a popup, so don't report it.
		positiveStates.discard(controlTypes.STATE_HASPOPUP)
	if reason == REASON_QUERY:
		return positiveStates
	positiveStates.discard(controlTypes.STATE_DEFUNCT)
	positiveStates.discard(controlTypes.STATE_MODAL)
	positiveStates.discard(controlTypes.STATE_FOCUSED)
	positiveStates.discard(controlTypes.STATE_OFFSCREEN)
	positiveStates.discard(controlTypes.STATE_INVISIBLE)
	if reason != REASON_CHANGE:
		positiveStates.discard(controlTypes.STATE_LINKED)
		if role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_TABLEROW) and controlTypes.STATE_SELECTABLE in states:
			positiveStates.discard(controlTypes.STATE_SELECTED)
	if role != controlTypes.ROLE_EDITABLETEXT:
		positiveStates.discard(controlTypes.STATE_READONLY)
	if role == controlTypes.ROLE_CHECKBOX:
		positiveStates.discard(controlTypes.STATE_PRESSED)
	if role == controlTypes.ROLE_MENUITEM:
		# The user doesn't usually care if a menu item is expanded or collapsed.
		positiveStates.discard(controlTypes.STATE_COLLAPSED)
		positiveStates.discard(controlTypes.STATE_EXPANDED)
	return positiveStates

def processNegativeStates(role, states, reason, negativeStates):
	speakNegatives = set()
	# Add the negative selected state if the control is selectable,
	# but only if it is either focused or this is something other than a change event.
	# The condition stops "not selected" from being spoken in some broken controls
	# when the state change for the previous focus is issued before the focus change.
	if role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_TABLEROW) and controlTypes.STATE_SELECTABLE in states and (reason != REASON_CHANGE or controlTypes.STATE_FOCUSED in states):
		speakNegatives.add(controlTypes.STATE_SELECTED)
	# Restrict "not checked" in a similar way to "not selected".
	if (role in (controlTypes.ROLE_CHECKBOX, controlTypes.ROLE_RADIOBUTTON, controlTypes.ROLE_CHECKMENUITEM) or controlTypes.STATE_CHECKABLE in states)  and (controlTypes.STATE_HALFCHECKED not in states) and (reason != REASON_CHANGE or controlTypes.STATE_FOCUSED in states):
		speakNegatives.add(controlTypes.STATE_CHECKED)
	if reason == REASON_CHANGE:
		# We want to speak this state only if it is changing to negative.
		speakNegatives.add(controlTypes.STATE_DROPTARGET)
		# We were given states which have changed to negative.
		# Return only those supplied negative states which should be spoken;
		# i.e. the states in both sets.
		speakNegatives &= negativeStates
		if controlTypes.STATES_SORTED & negativeStates and not controlTypes.STATES_SORTED & states:
			# If the object has just stopped being sorted, just report not sorted.
			# The user doesn't care how it was sorted before.
			speakNegatives.add(controlTypes.STATE_SORTED)
		return speakNegatives
	else:
		# This is not a state change; only positive states were supplied.
		# Return all negative states which should be spoken, excluding the positive states.
		return speakNegatives - states

def speakTextInfo(info,useCache=True,formatConfig=None,unit=None,reason=REASON_QUERY,index=None):
	autoLanguageSwitching=config.conf['speech']['autoLanguageSwitching']
	extraDetail=unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD)
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]
	speechSequence=[]
	#Fetch the last controlFieldStack, or make a blank one
	controlFieldStackCache=getattr(info.obj,'_speakTextInfo_controlFieldStackCache',[]) if useCache else []
	formatFieldAttributesCache=getattr(info.obj,'_speakTextInfo_formatFieldAttributesCache',{}) if useCache else {}
	#Make a new controlFieldStack and formatField from the textInfo's initialFields
	newControlFieldStack=[]
	newFormatField=textInfos.FormatField()
	textWithFields=info.getTextWithFields(formatConfig)
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
		if newControlFieldStack[count]==controlFieldStackCache[count]:
			commonFieldCount+=1
		else:
			break

	#Get speech text for any fields in the old controlFieldStack that are not in the new controlFieldStack 
	endingBlock=False
	for count in reversed(xrange(commonFieldCount,len(controlFieldStackCache))):
		text=info.getControlFieldSpeech(controlFieldStackCache[count],controlFieldStackCache[0:count],"end_removedFromControlFieldStack",formatConfig,extraDetail,reason=reason)
		if text:
			speechSequence.append(text)
		if not endingBlock and reason==REASON_SAYALL:
			endingBlock=bool(int(controlFieldStackCache[count].get('isBlock',0)))
	if endingBlock:
		speechSequence.append(BreakCommand())
	# The TextInfo should be considered blank if we are only exiting fields (i.e. we aren't entering any new fields and there is no text).
	isTextBlank=True

	# Even when there's no speakable text, we still need to notify the synth of the index.
	if index is not None:
		speechSequence.append(IndexCommand(index))

	#Get speech text for any fields that are in both controlFieldStacks, if extra detail is not requested
	if not extraDetail:
		for count in xrange(commonFieldCount):
			text=info.getControlFieldSpeech(newControlFieldStack[count],newControlFieldStack[0:count],"start_inControlFieldStack",formatConfig,extraDetail,reason=reason)
			if text:
				speechSequence.append(text)
				isTextBlank=False

	#Get speech text for any fields in the new controlFieldStack that are not in the old controlFieldStack
	for count in xrange(commonFieldCount,len(newControlFieldStack)):
		text=info.getControlFieldSpeech(newControlFieldStack[count],newControlFieldStack[0:count],"start_addedToControlFieldStack",formatConfig,extraDetail,reason=reason)
		if text:
			speechSequence.append(text)
			isTextBlank=False
		commonFieldCount+=1

	#Fetch the text for format field attributes that have changed between what was previously cached, and this textInfo's initialFormatField.
	text=getFormatFieldSpeech(newFormatField,formatFieldAttributesCache,formatConfig,unit=unit,extraDetail=extraDetail)
	if text:
		speechSequence.append(text)
	if autoLanguageSwitching:
		language=newFormatField.get('language')
		speechSequence.append(LangChangeCommand(language))
		lastLanguage=language

	if unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD) and len(textWithFields)>0 and len(textWithFields[0])==1 and len([x for x in textWithFields if isinstance(x,basestring)])==1:
		if any(isinstance(x,basestring) for x in speechSequence):
			speak(speechSequence)
		speakSpelling(textWithFields[0],locale=language if autoLanguageSwitching else None)
		info.obj._speakTextInfo_controlFieldStackCache=list(newControlFieldStack)
		info.obj._speakTextInfo_formatFieldAttributesCache=formatFieldAttributesCache
		return

	#Move through the field commands, getting speech text for all controlStarts, controlEnds and formatChange commands
	#But also keep newControlFieldStack up to date as we will need it for the ends
	# Add any text to a separate list, as it must be handled differently.
	#Also make sure that LangChangeCommand objects are added before any controlField or formatField speech
	relativeSpeechSequence=[]
	inTextChunk=False
	for command in textWithFields:
		if isinstance(command,basestring):
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
				if autoLanguageSwitching and newLanguage!=lastLanguage:
					relativeSpeechSequence.append(LangChangeCommand(newLanguage))
					lastLanguage=newLanguage
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
	if reason != REASON_SAYALL and isTextBlank:
		speechSequence.append(_("blank"))

	#Cache a copy of the new controlFieldStack for future use
	if useCache:
		info.obj._speakTextInfo_controlFieldStackCache=list(newControlFieldStack)
		info.obj._speakTextInfo_formatFieldAttributesCache=formatFieldAttributesCache

	if speechSequence:
		if reason==REASON_SAYALL:
			speakWithoutPauses(speechSequence)
		else:
			speak(speechSequence)

def getSpeechTextForProperties(reason=REASON_QUERY,**propertyValues):
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
	value=propertyValues.get('value') if role not in silentValuesForRoles else None
	rowNumber=propertyValues.get('rowNumber')
	columnNumber=propertyValues.get('columnNumber')
	includeTableCellCoords=propertyValues.get('includeTableCellCoords',True)
	if speakRole and (reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or not (name or value or rowNumber or columnNumber) or role not in silentRolesOnFocus):
		textList.append(controlTypes.speechRoleLabels[role])
	if value:
		textList.append(value)
	states=propertyValues.get('states')
	realStates=propertyValues.get('_states',states)
	if states is not None:
		positiveStates=processPositiveStates(role,realStates,reason,states)
		textList.extend([controlTypes.speechStateLabels[x] for x in positiveStates])
	if 'negativeStates' in propertyValues:
		negativeStates=propertyValues['negativeStates']
	else:
		negativeStates=None
	if negativeStates is not None or (reason != REASON_CHANGE and states is not None):
		negativeStates=processNegativeStates(role, realStates, reason, negativeStates)
		if controlTypes.STATE_DROPTARGET in negativeStates:
			# "not drop target" doesn't make any sense, so use a custom message.
			textList.append(_("done dragging"))
			negativeStates.discard(controlTypes.STATE_DROPTARGET)
		textList.extend([_("not %s")%controlTypes.speechStateLabels[x] for x in negativeStates])
	if 'description' in propertyValues:
		textList.append(propertyValues['description'])
	if 'keyboardShortcut' in propertyValues:
		textList.append(propertyValues['keyboardShortcut'])
	indexInGroup=propertyValues.get('positionInfo_indexInGroup',0)
	similarItemsInGroup=propertyValues.get('positionInfo_similarItemsInGroup',0)
	if 0<indexInGroup<=similarItemsInGroup:
		textList.append(_("%s of %s")%(indexInGroup,similarItemsInGroup))
	if 'positionInfo_level' in propertyValues:
		level=propertyValues.get('positionInfo_level',None)
		role=propertyValues.get('role',None)
		if level is not None:
			if role in (controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM) and level!=oldTreeLevel:
				textList.insert(0,_("level %s")%level)
				oldTreeLevel=level
			else:
				textList.append(_('level %s')%propertyValues['positionInfo_level'])
	if rowNumber or columnNumber:
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
			if includeTableCellCoords: 
				textList.append(_("row %s")%rowNumber)
			oldRowNumber = rowNumber
		if columnNumber and (not sameTable or columnNumber != oldColumnNumber):
			columnHeaderText = propertyValues.get("columnHeaderText")
			if columnHeaderText:
				textList.append(columnHeaderText)
			if includeTableCellCoords:
				textList.append(_("column %s")%columnNumber)
			oldColumnNumber = columnNumber
	rowCount=propertyValues.get('rowCount',0)
	columnCount=propertyValues.get('columnCount',0)
	if rowCount and columnCount:
		textList.append(_("with %s rows and %s columns")%(rowCount,columnCount))
	elif columnCount and not rowCount:
		textList.append(_("with %s columns")%columnCount)
	elif rowCount and not columnCount:
		textList.append(_("with %s rows")%rowCount)
	if rowCount or columnCount:
		# The caller is entering a table, so ensure that it is treated as a new table, even if the previous table was the same.
		oldTableID = None
	return CHUNK_SEPARATOR.join([x for x in textList if x])

def getControlFieldSpeech(attrs,ancestorAttrs,fieldType,formatConfig=None,extraDetail=False,reason=None):
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]

	childCount=int(attrs.get('_childcount',"0"))
	if reason==REASON_FOCUS or attrs.get('alwaysReportName',False):
		name=attrs.get('name',"")
	else:
		name=""
	role=attrs.get('role',controlTypes.ROLE_UNKNOWN)
	states=attrs.get('states',set())
	keyboardShortcut=attrs.get('keyboardShortcut', "")
	if reason==REASON_FOCUS or attrs.get('alwaysReportDescription',False):
		description=attrs.get('description',"")
	else:
		description=""
	level=attrs.get('level',None)

	# Remove the clickable state from controls that are clearly clickable according to their role
	# or where it just isn't useful.
	if role in (controlTypes.ROLE_LINK,controlTypes.ROLE_BUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_TOGGLEBUTTON,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_TAB,controlTypes.ROLE_SLIDER,controlTypes.ROLE_DOCUMENT):
		states=states.copy()
		states.discard(controlTypes.STATE_CLICKABLE)

	if formatConfig["includeLayoutTables"]:
		tableLayout=None
	else:
		# Find the nearest table.
		if role==controlTypes.ROLE_TABLE:
			# This is the nearest table.
			tableLayout=attrs.get('table-layout',None)
		else:
			# Search ancestors for the nearest table.
			for x in reversed(ancestorAttrs):
				if x.get("role")==controlTypes.ROLE_TABLE:
					tableLayout=x.get('table-layout',None)
					break
			else:
				# No table in the ancestors.
				tableLayout=None
	if not tableLayout:
		tableID=attrs.get('table-id')
	else:
		tableID=None

	# Honour verbosity configuration.
	if reason in (REASON_CARET,REASON_SAYALL,REASON_FOCUS) and (
		(role==controlTypes.ROLE_LINK and not formatConfig["reportLinks"]) or 
		(role==controlTypes.ROLE_HEADING and not formatConfig["reportHeadings"]) or
		(role==controlTypes.ROLE_BLOCKQUOTE and not formatConfig["reportBlockQuotes"]) or
		(role in (controlTypes.ROLE_TABLE,controlTypes.ROLE_TABLECELL,controlTypes.ROLE_TABLEROWHEADER,controlTypes.ROLE_TABLECOLUMNHEADER) and not formatConfig["reportTables"]) or
		(role in (controlTypes.ROLE_LIST,controlTypes.ROLE_LISTITEM) and controlTypes.STATE_READONLY in states and not formatConfig["reportLists"])
	):
		return ""

	roleText=getSpeechTextForProperties(reason=reason,role=role)
	stateText=getSpeechTextForProperties(reason=reason,states=states,_role=role)
	keyboardShortcutText=getSpeechTextForProperties(reason=reason,keyboardShortcut=keyboardShortcut) if config.conf["presentation"]["reportKeyboardShortcuts"] else ""
	nameText=getSpeechTextForProperties(reason=reason,name=name)
	descriptionText=(getSpeechTextForProperties(reason=reason,description=description)
		if config.conf["presentation"]["reportObjectDescriptions"] else "")
	levelText=getSpeechTextForProperties(reason=reason,positionInfo_level=level)

	# Determine under what circumstances this node should be spoken.
	# speakEntry: Speak when the user enters the control.
	# speakWithinForLine: When moving by line, speak when the user is already within the control.
	# speakExitForLine: When moving by line, speak when the user exits the control.
	# speakExitForOther: When moving by word or character, speak when the user exits the control.
	speakEntry=speakWithinForLine=speakExitForLine=speakExitForOther=False
	if (
		role in (controlTypes.ROLE_LINK,controlTypes.ROLE_HEADING,controlTypes.ROLE_BUTTON,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_TAB,controlTypes.ROLE_COMBOBOX,controlTypes.ROLE_SLIDER,controlTypes.ROLE_SPINBUTTON,controlTypes.ROLE_COMBOBOX,controlTypes.ROLE_PROGRESSBAR,controlTypes.ROLE_TOGGLEBUTTON)
		or (role==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_MULTILINE not in states and (controlTypes.STATE_READONLY not in states or controlTypes.STATE_FOCUSABLE in states))
		or (role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY not in states)
	):
		# This node is usually a single line.
		speakEntry=True
		speakWithinForLine=True
		speakExitForOther=True
	elif role in (controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_EMBEDDEDOBJECT):
		# This node is only ever a marker; i.e. single character.
		speakEntry=True
	elif (
		role in (controlTypes.ROLE_BLOCKQUOTE,controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_TOOLBAR,controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU)
		or (role==controlTypes.ROLE_EDITABLETEXT and (controlTypes.STATE_READONLY not in states or controlTypes.STATE_FOCUSABLE in states) and controlTypes.STATE_MULTILINE in states)
		or (role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states)
		or (role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)
		or (role==controlTypes.ROLE_TABLE and tableID)
	):
		# This node is usually a multiline container.
		speakEntry=True
		speakExitForLine=True
		speakExitForOther=True

	# Determine the order of speech.
	# speakContentFirst: Speak the content before the control field info.
	speakContentFirst=reason==REASON_FOCUS and role not in (controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_COMBOBOX) and controlTypes.STATE_EDITABLE not in states
	# speakStatesFirst: Speak the states before the role.
	speakStatesFirst=role==controlTypes.ROLE_LINK

	if speakContentFirst and speakExitForOther and not speakWithinForLine and role!=controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_EDITABLE not in states:
		# If content is to be spoken first, don't speak containers at all.
		speakEntry=False

	# Determine what text to speak.
	# Special cases
	if fieldType=="start_addedToControlFieldStack" and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
		# List.
		return roleText+" "+_("with %s items")%childCount
	elif fieldType=="start_addedToControlFieldStack" and role==controlTypes.ROLE_TABLE and tableID:
		# Table.
		return " ".join((roleText, getSpeechTextForProperties(_tableID=tableID, rowCount=attrs.get("table-rowcount"), columnCount=attrs.get("table-columncount"))))
	elif fieldType=="start_addedToControlFieldStack" and role in (controlTypes.ROLE_TABLECELL,controlTypes.ROLE_TABLECOLUMNHEADER,controlTypes.ROLE_TABLEROWHEADER) and tableID:
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
		return CHUNK_SEPARATOR.join([x for x in nameText,(stateText if speakStatesFirst else roleText),(roleText if speakStatesFirst else stateText),descriptionText,levelText,keyboardShortcutText if x])
	elif fieldType in ("end_removedFromControlFieldStack","end_relative") and roleText and ((not extraDetail and speakExitForLine) or (extraDetail and speakExitForOther)):
		return _("out of %s")%roleText

	# Special cases
	elif not extraDetail and fieldType in ("start_addedToControlFieldStack","start_relative")  and controlTypes.STATE_CLICKABLE in states: 
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
			text=_("page %s")%pageNumber
			textList.append(text)
	if  formatConfig["reportStyle"]:
		style=attrs.get("style")
		oldStyle=attrsCache.get("style") if attrsCache is not None else None
		if style!=oldStyle:
			if style:
				text=_("style %s")%style
			else:
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
		if color and color!=oldColor:
			textList.append(color.name if isinstance(color,colors.RGB) else unicode(color))
		backgroundColor=attrs.get("background-color")
		oldBackgroundColor=attrsCache.get("background-color") if attrsCache is not None else None
		if backgroundColor and backgroundColor!=oldBackgroundColor:
			# Translators: This is used to indicate a background color after the text color.
			# The {backgroundColor} text will be replaced by the background color.
			# For example, if the text is white on a black background,
			# the output of this message in English would be "on black".
			textList.append(_("on {backgroundColor}").format(backgroundColor=backgroundColor.name if isinstance(backgroundColor,colors.RGB) else unicode(backgroundColor)))
	if  formatConfig["reportLineNumber"]:
		lineNumber=attrs.get("line-number")
		oldLineNumber=attrsCache.get("line-number") if attrsCache is not None else None
		if lineNumber is not None and lineNumber!=oldLineNumber:
			text=_("line %s")%lineNumber
			textList.append(text)
	if  formatConfig["reportFontAttributes"]:
		bold=attrs.get("bold")
		oldBold=attrsCache.get("bold") if attrsCache is not None else None
		if (bold or oldBold is not None) and bold!=oldBold:
			text=_("bold") if bold else _("no bold")
			textList.append(text)
		italic=attrs.get("italic")
		oldItalic=attrsCache.get("italic") if attrsCache is not None else None
		if (italic or oldItalic is not None) and italic!=oldItalic:
			text=_("italic") if italic else _("no italic")
			textList.append(text)
		strikethrough=attrs.get("strikethrough")
		oldStrikethrough=attrsCache.get("strikethrough") if attrsCache is not None else None
		if (strikethrough or oldStrikethrough is not None) and strikethrough!=oldStrikethrough:
			text=_("strikethrough") if strikethrough else _("no strikethrough")
			textList.append(text)
		underline=attrs.get("underline")
		oldUnderline=attrsCache.get("underline") if attrsCache is not None else None
		if (underline or oldUnderline is not None) and underline!=oldUnderline:
			text=_("underlined") if underline else _("not underlined")
			textList.append(text)
		textPosition=attrs.get("text-position")
		oldTextPosition=attrsCache.get("text-position") if attrsCache is not None else None
		if (textPosition or oldTextPosition is not None) and textPosition!=oldTextPosition:
			textPosition=textPosition.lower() if textPosition else textPosition
			if textPosition=="super":
				text=_("superscript")
			elif textPosition=="sub":
				text=_("subscript")
			else:
				text=_("baseline")
			textList.append(text)
	if formatConfig["reportAlignment"]:
		textAlign=attrs.get("text-align")
		oldTextAlign=attrsCache.get("text-align") if attrsCache is not None else None
		if (textAlign or oldTextAlign is not None) and textAlign!=oldTextAlign:
			textAlign=textAlign.lower() if textAlign else textAlign
			if textAlign=="left":
				text=_("align left")
			elif textAlign=="center":
				text=_("align center")
			elif textAlign=="right":
				text=_("align right")
			elif textAlign=="justify":
				text=_("align justify")
			else:
				text=_("align default")
			textList.append(text)
	if  formatConfig["reportLinks"]:
		link=attrs.get("link")
		oldLink=attrsCache.get("link") if attrsCache is not None else None
		if (link or oldLink is not None) and link!=oldLink:
			text=_("link") if link else _("out of %s")%_("link")
			textList.append(text)
	if formatConfig["reportSpellingErrors"]:
		invalidSpelling=attrs.get("invalid-spelling")
		oldInvalidSpelling=attrsCache.get("invalid-spelling") if attrsCache is not None else None
		if (invalidSpelling or oldInvalidSpelling is not None) and invalidSpelling!=oldInvalidSpelling:
			if invalidSpelling:
				text=_("spelling error")
			elif extraDetail:
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
		return _("out of table")
	if not oldTableInfo or tableInfo.get("table-id")!=oldTableInfo.get("table-id"):
		newTable=True
	else:
		newTable=False
	textList=[]
	if newTable:
		columnCount=tableInfo.get("column-count",0)
		rowCount=tableInfo.get("row-count",0)
		text=_("table with %s columns and %s rows")%(columnCount,rowCount)
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
			if isinstance(speechSequence[index],BreakCommand):
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

class BreakCommand(object):
	"""Forces speakWithoutPauses to flush its buffer and therefore break the sentence at this point."""
