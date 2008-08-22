#speech.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""High-level functions to speak information.
@var speechMode: allows speech if true
@type speechMode: boolean
""" 

import XMLFormatting
import globalVars
from logHandler import log
import api
import controlTypes
import config
import tones
from synthDriverHandler import *
import re
import textHandler
import characterSymbols
import queueHandler
import speechDictHandler

speechMode_off=0
speechMode_beeps=1
speechMode_talk=2
speechMode=2
speechMode_beeps_ms=15
beenCanceled=True
isPaused=False
typedWord=""
REASON_FOCUS=1
REASON_MOUSE=2
REASON_QUERY=3
REASON_CHANGE=4
REASON_MESSAGE=5
REASON_SAYALL=6
REASON_CARET=7
REASON_DEBUG=8
REASON_ONLYCACHE=9


def initialize():
	"""Loads and sets the synth driver configured in nvda.ini."""
	setSynth(config.conf["speech"]["synth"])

def terminate():
	setSynth(None)

RE_PROCESS_SYMBOLS = re.compile(
	# Groups 1-3: expand symbols where the actual symbol should be preserved to provide correct entonation.
	# Group 1: sentence endings.
	r"(?:(?<=[^\s.!?])([.!?])(?=[\"')\s]|$))"
	# Group 2: comma.
	+ r"|(,)"
	# Group 3: semi-colon and colon.
	+ r"|(?:(?<=[^\s;:])([;:])(?=\s|$))"
	# Group 4: expand all other symbols without preserving.
	+ r"|([%s])" % re.escape("".join(frozenset(characterSymbols.names) - frozenset(characterSymbols.blankList)))
)
def _processSymbol(m):
	symbol = m.group(1) or m.group(2) or m.group(3)
	if symbol:
		# Preserve symbol.
		return " %s%s " % (characterSymbols.names[symbol], symbol)
	else:
		# Expand without preserving.
		return " %s " % characterSymbols.names[m.group(4)]
RE_CONVERT_WHITESPACE = re.compile("[\0\r\n]")

def processTextSymbols(text,expandPunctuation=False):
	if (text is None) or (len(text)==0) or (isinstance(text,basestring) and (set(text)<=set(characterSymbols.blankList))):
		return _("blank") 
	#Convert non-breaking spaces to spaces
	text=text.replace(u'\xa0',u' ')
	text = speechDictHandler.processText(text)
	if expandPunctuation:
		text = RE_PROCESS_SYMBOLS.sub(_processSymbol, text)
	text = RE_CONVERT_WHITESPACE.sub(u" ", text)
	return text.strip()

def processSymbol(symbol):
	if isinstance(symbol,basestring):
		symbol=symbol.replace(u'\xa0',u' ')
	newSymbol=characterSymbols.names.get(symbol,symbol)
	return newSymbol

def getLastSpeechIndex():
	"""Gets the last index passed by the synthesizer. Indexing is used so that its possible to find out when a certain peace of text has been spoken yet. Usually the character position of the text is passed to speak functions as the index.
@returns: the last index encountered
@rtype: int
"""
	return getSynth().lastIndex

def processText(text):
	"""Processes the text using the L{textProcessing} module which converts punctuation so it is suitable to be spoken by the synthesizer. This function makes sure that all punctuation is included if it is configured so in nvda.ini.
@param text: the text to be processed
@type text: string
"""
	text=processTextSymbols(text,expandPunctuation=config.conf["speech"]["speakPunctuation"])
	return text

def cancelSpeech():
	"""Interupts the synthesizer from currently speaking"""
	global beenCanceled, isPaused
	# Import only for this function to avoid circular import.
	import sayAllHandler
	sayAllHandler.stop()
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
This function will not speak if L{speechMode} is false.
@param text: the message to speak
@type text: string
@param index: the index to mark this current text with, its best to use the character position of the text if you know it 
@type index: int
"""
	global beenCanceled
	speakText(text,index=index,reason=REASON_MESSAGE)

def speakSpelling(text):
	global beenCanceled
	if not isinstance(text,basestring) or len(text)==0:
		return getSynth().speakText(processSymbol(""))
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	if not text.isspace():
		text=text.rstrip()
	gen=_speakSpellingGen(text)
	try:
		# Speak the first character before this function returns.
		gen.next()
	except StopIteration:
		return
	queueHandler.registerGeneratorObject(gen)

def _speakSpellingGen(text):
	lastKeyCount=globalVars.keyCounter
	textLength=len(text)
	for count,char in enumerate(text): 
		uppercase=char.isupper()
		char=processSymbol(char)
		if uppercase and config.conf["speech"][getSynth().name]["sayCapForCapitals"]:
			char=_("cap %s")%char
		if uppercase and config.conf["speech"][getSynth().name]["raisePitchForCapitals"]:
			oldPitch=config.conf["speech"][getSynth().name]["pitch"]
			getSynth().pitch=max(0,min(oldPitch+config.conf["speech"][getSynth().name]["capPitchChange"],100))
		index=count+1
		if log.isEnabledFor(log.IO): log.io("Speaking \"%s\""%char)
		getSynth().speakText(char,index=index)
		if uppercase and config.conf["speech"][getSynth().name]["raisePitchForCapitals"]:
			getSynth().pitch=oldPitch
		while textLength>1 and globalVars.keyCounter==lastKeyCount and (isPaused or getLastSpeechIndex()!=index): 
			yield
			yield
		if globalVars.keyCounter!=lastKeyCount:
			break
		if uppercase and  config.conf["speech"][getSynth().name]["beepForCapitals"]:
			tones.beep(2000,50)

def speakObjectProperties(obj,reason=REASON_QUERY,index=None,**allowedProperties):
	global beenCanceled
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	#Fetch the values for all wanted properties
	newPropertyValues={}
	for name,value in allowedProperties.iteritems():
		if value:
			newPropertyValues[name]=getattr(obj,name)
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
	#Get the speech text for the properties we want to speak, and then speak it
	#properties such as states need to know the role to speak properly, give it as a _ name
	newPropertyValues['_role']=newPropertyValues.get('role',obj.role)
	# The real states are needed also, as the states entry might be filtered.
	newPropertyValues['_states']=obj.states
	text=getSpeechTextForProperties(reason,**newPropertyValues)
	if text:
		speakText(text,index=index)

def speakObject(obj,reason=REASON_QUERY,index=None):
	isEditable=bool(obj.role==controlTypes.ROLE_EDITABLETEXT or controlTypes.STATE_EDITABLE in obj.states)
	allowProperties={'name':True,'role':True,'states':True,'value':True,'description':True,'keyboardShortcut':True,'positionString':True}
	if not config.conf["presentation"]["reportObjectDescriptions"]:
		allowProperties["description"]=False
	if not config.conf["presentation"]["reportKeyboardShortcuts"]:
		allowProperties["keyboardShortcut"]=False
	if not config.conf["presentation"]["reportObjectPositionInformation"]:
		allowProperties["positionString"]=False
	if isEditable:
		allowProperties['value']=False
	speakObjectProperties(obj,reason=reason,index=index,**allowProperties)
	if reason!=REASON_ONLYCACHE and isEditable and not globalVars.inCaretMovement:
		try:
			info=obj.makeTextInfo(textHandler.POSITION_SELECTION)
			if not info.isCollapsed:
				speakMessage(_("selected %s")%info.text)
			else:
				info.expand(textHandler.UNIT_READINGCHUNK)
				speakMessage(info.text)
		except:
			newInfo=obj.makeTextInfo(textHandler.POSITION_ALL)
			speakMessage(newInfo.text)


def speakText(text,index=None,reason=REASON_MESSAGE):
	"""Speaks some given text.
This function will not speak if L{speechMode} is false.
@param text: the message to speak
@type text: string
@param index: the index to mark this current text with, its best to use the character position of the text if you know it 
@type index: int
"""
	global beenCanceled
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	text=processText(text)
	if text and not text.isspace():
		getSynth().speakText(text,index=index)

def getExcludedAutoSpeakFormats():
	formats=set()
	if not config.conf["documentFormatting"]["reportFontName"]:
		formats.add(controlTypes.ROLE_FONTNAME)
	if not config.conf["documentFormatting"]["reportFontSize"]:
		formats.add(controlTypes.ROLE_FONTSIZE)
	if not config.conf["documentFormatting"]["reportFontAttributes"]:
		formats.add(controlTypes.ROLE_BOLD)
		formats.add(controlTypes.ROLE_ITALIC)
		formats.add(controlTypes.ROLE_UNDERLINE)
	if not config.conf["documentFormatting"]["reportStyle"]:
		formats.add(controlTypes.ROLE_STYLE)
	if not config.conf["documentFormatting"]["reportPage"]:
		formats.add(controlTypes.ROLE_PAGE)
	if not config.conf["documentFormatting"]["reportLineNumber"]:
		formats.add(controlTypes.ROLE_LINE)
	if not config.conf["documentFormatting"]["reportTables"]:
		formats.add(controlTypes.ROLE_TABLE)
		formats.add(controlTypes.ROLE_TABLEROW)
		formats.add(controlTypes.ROLE_TABLECOLUMN)
		formats.add(controlTypes.ROLE_TABLECELL)
	if not config.conf["documentFormatting"]["reportAlignment"]:
		formats.add(controlTypes.ROLE_ALIGNMENT)
	return formats

def speakFormattedText(textInfo,handleSymbols=False,includeBlankText=True,index=None):
	global beenCanceled
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	formattedText=textInfo.getFormattedText(searchRange=config.conf["documentFormatting"]["detectFormatAfterCursor"],excludes=getExcludedAutoSpeakFormats())
	if not hasattr(textInfo.obj,"_lastInitialSpokenFormats"):
		textInfo.obj._lastInitialSpokenFormats={}
	initialSpokenFormats={}
	checkFormats=True
	for item in formattedText:
		if isinstance(item,textHandler.FormatCommand):
			itemKey="%d, %s, %s"%(item.format.role,item.format.value,item.format.uniqueID)
			if item.cmd==textHandler.FORMAT_CMD_CHANGE:
				if not checkFormats or itemKey not in textInfo.obj._lastInitialSpokenFormats: 
					speechText=" ".join([controlTypes.speechRoleLabels.get(item.format.role,""),item.format.value])
					speakMessage(speechText)
				if checkFormats:
					initialSpokenFormats[itemKey]=item
			elif item.cmd==textHandler.FORMAT_CMD_INFIELD:
				if not checkFormats or itemKey not in textInfo.obj._lastInitialSpokenFormats: 
					speechText=" ".join([_("in"),controlTypes.speechRoleLabels.get(item.format.role,""),item.format.value])
					speakMessage(speechText)
				if checkFormats:
					initialSpokenFormats[itemKey]=item
			elif item.cmd==textHandler.FORMAT_CMD_OUTOFFIELD:
				speechText=" ".join([_("out of"),controlTypes.speechRoleLabels.get(item.format.role,""),])
				speakMessage(speechText)
			elif item.cmd==textHandler.FORMAT_CMD_SWITCHON:
				if not checkFormats or itemKey not in textInfo.obj._lastInitialSpokenFormats: 
					speechText=" ".join([controlTypes.speechRoleLabels.get(item.format.role,""),item.format.value,_("on")])
					speakMessage(speechText)
				if checkFormats:
					initialSpokenFormats[itemKey]=item
			elif item.cmd==textHandler.FORMAT_CMD_SWITCHOFF:
				speechText=" ".join([controlTypes.speechRoleLabels.get(item.format.role,""),_("off")])
				speakMessage(speechText)
		elif isinstance(item,basestring):
			checkFormats=False
			for oldItemKey,oldItem in textInfo.obj._lastInitialSpokenFormats.items():
				if oldItem.cmd==textHandler.FORMAT_CMD_SWITCHON and oldItemKey not in initialSpokenFormats:
					speechText=" ".join([controlTypes.speechRoleLabels.get(oldItem.format.role,""),_("off")])
					speakMessage(speechText)
				if oldItem.cmd==textHandler.FORMAT_CMD_INFIELD and oldItemKey not in initialSpokenFormats:
					speechText=" ".join([_("out of"),controlTypes.speechRoleLabels.get(oldItem.format.role,"")])
					speakMessage(speechText)
			if len(item)>1 or not handleSymbols:
				if includeBlankText or not set(item)<=set(characterSymbols.blankList):
					speakText(item,index=index)
			else:
				speakSpelling(item)
	textInfo.obj._lastInitialSpokenFormats=initialSpokenFormats

def speakSelectionChange(oldInfo,newInfo,speakSelected=True,speakUnselected=True,generalize=False):
	"""Speaks a change in selection, either selected or unselected text.
	@param oldInfo: a TextInfo instance representing what the selection was before
	@type oldInfo: L{TextHandler.TextInfo}
	@param newInfo: a TextInfo instance representing what the selection is now
	@type newInfo: L{textHandler.TextInfo}
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
	if speakSelected:
		if not generalize:
			for text in selectedTextList:
				if  len(text)==1:
					text=processSymbol(text)
				speakMessage(_("selecting %s")%text)
		elif len(selectedTextList)>0:
			text=newInfo.text
			if len(text)==1:
				text=processSymbol(text)
			speakMessage(_("selected %s")%text)
	if speakUnselected:
		if not generalize:
			for text in unselectedTextList:
				if  len(text)==1:
					text=processSymbol(text)
				speakMessage(_("unselecting %s")%text)
		elif len(unselectedTextList)>0:
			speakMessage(_("selection removed"))
			if not newInfo.isCollapsed:
				text=newInfo.text
				if len(text)==1:
					text=processSymbol(text)
				speakMessage(_("selected %s")%text)

def speakTypedCharacters(ch):
	global typedWord
	if api.isTypingProtected():
		ch="*"
	if config.conf["keyboard"]["speakTypedCharacters"]:
		speakSpelling(ch)
	if config.conf["keyboard"]["speakTypedWords"]: 
		if ch.isalnum():
			typedWord="".join([typedWord,ch])
		elif len(typedWord)>0:
			speakText(typedWord)
			if log.isEnabledFor(log.IO): log.io("typedword: %s"%typedWord)
			typedWord=""
	else:
		typedWord=""

silentRolesOnFocus=set([
	controlTypes.ROLE_LISTITEM,
	controlTypes.ROLE_MENUITEM,
	controlTypes.ROLE_TREEVIEWITEM,
])

silentValuesForRoles=set([
	controlTypes.ROLE_CHECKBOX,
	controlTypes.ROLE_RADIOBUTTON,
])

userDisabledRoles=[]

def updateUserDisabledRoles():
	del userDisabledRoles[:]
	if not config.conf["virtualBuffers"]["reportLinks"]:
		userDisabledRoles.append(controlTypes.ROLE_LINK)
	if not config.conf["virtualBuffers"]["reportLists"]:
		userDisabledRoles.append(controlTypes.ROLE_LIST)
		userDisabledRoles.append(controlTypes.ROLE_LISTITEM)
	if not config.conf["virtualBuffers"]["reportHeadings"]:
		userDisabledRoles.append(controlTypes.ROLE_HEADING)
	if not config.conf["virtualBuffers"]["reportTables"]:
		userDisabledRoles.append(controlTypes.ROLE_TABLE)
	if not config.conf["virtualBuffers"]["reportGraphics"]:
		userDisabledRoles.append(controlTypes.ROLE_GRAPHIC)
	if not config.conf["virtualBuffers"]["reportForms"]:
		userDisabledRoles.append(controlTypes.ROLE_FORM)
	if not config.conf["virtualBuffers"]["reportFormFields"]:
		userDisabledRoles.append(controlTypes.ROLE_BUTTON)
		userDisabledRoles.append(controlTypes.ROLE_RADIOBUTTON)
		userDisabledRoles.append(controlTypes.ROLE_CHECKBOX)
		userDisabledRoles.append(controlTypes.ROLE_COMBOBOX)
		userDisabledRoles.append(controlTypes.ROLE_TREEVIEW)
		userDisabledRoles.append(controlTypes.ROLE_EDITABLETEXT)
	if not config.conf["virtualBuffers"]["reportBlockQuotes"]:
		userDisabledRoles.append(controlTypes.ROLE_BLOCKQUOTE)
	if not config.conf["virtualBuffers"]["reportParagraphs"]:
		userDisabledRoles.append(controlTypes.ROLE_PARAGRAPH)
	if not config.conf["virtualBuffers"]["reportFrames"]:
		userDisabledRoles.append(controlTypes.ROLE_FRAME)
		userDisabledRoles.append(controlTypes.ROLE_INTERNALFRAME)

updateUserDisabledRoles()

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
	if reason == REASON_QUERY:
		return positiveStates
	positiveStates.discard(controlTypes.STATE_MODAL)
	positiveStates.discard(controlTypes.STATE_FOCUSED)
	if reason in (REASON_FOCUS, REASON_CARET, REASON_SAYALL):
		positiveStates.difference_update(frozenset((controlTypes.STATE_INVISIBLE, controlTypes.STATE_READONLY, controlTypes.STATE_LINKED)))
		if role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_MENUITEM) and controlTypes.STATE_SELECTABLE in states:
			positiveStates.discard(controlTypes.STATE_SELECTED)
	if role == controlTypes.ROLE_CHECKBOX:
		positiveStates.discard(controlTypes.STATE_PRESSED)
	return positiveStates

def processNegativeStates(role, states, reason, negativeStates):
	speakNegatives = set()
	# Add the negative selected state if the control is selectable,
	# but only if it is either focused or this is something other than a change event.
	# The condition stops "not selected" from being spoken in some broken controls
	# when the state change for the previous focus is issued before the focus change.
	if role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_TREEVIEWITEM) and controlTypes.STATE_SELECTABLE in states and (reason != REASON_CHANGE or controlTypes.STATE_FOCUSED in states):
		speakNegatives.add(controlTypes.STATE_SELECTED)
	# Restrict "not checked" in a similar way to "not selected".
	if (role in (controlTypes.ROLE_CHECKBOX, controlTypes.ROLE_RADIOBUTTON) or controlTypes.STATE_CHECKABLE in states)  and (controlTypes.STATE_HALFCHECKED not in states) and (reason != REASON_CHANGE or controlTypes.STATE_FOCUSED in states):
		speakNegatives.add(controlTypes.STATE_CHECKED)
	if reason == REASON_CHANGE:
		# We were given states which have changed to negative.
		# Return only those supplied negative states which should be spoken;
		# i.e. the states in both sets.
		return negativeStates & speakNegatives
	else:
		# This is not a state change; only positive states were supplied.
		# Return all negative states which should be spoken, excluding the positive states.
		return speakNegatives - states

def speakTextInfo(info,useCache=True,extraDetail=False,handleSymbols=False,reason=REASON_QUERY,index=None):
	textList=[]
	#Fetch the last controlFieldStack, or make a blank one
	controlFieldStackCache=getattr(info.obj,'_speakTextInfo_controlFieldStackCache',[]) if useCache else {}
	formatFieldAttributesCache=getattr(info.obj,'_speakTextInfo_formatFieldAttributesCache',{}) if useCache else {}
	#Make a new controlFieldStack from the textInfo's initialControlFieldAncestry
	newControlFieldStack=info.initialControlFieldAncestry
	#Calculate how many fields in the old and new controlFieldStacks are the same
	commonFieldCount=0
	for count in range(min(len(newControlFieldStack),len(controlFieldStackCache))):
		if newControlFieldStack[count]==controlFieldStackCache[count]:
			commonFieldCount+=1
		else:
			break

	#Get speech text for any fields in the old controlFieldStack that are not in the new controlFieldStack 
	for count in reversed(range(commonFieldCount,len(controlFieldStackCache))):
		text=getControlFieldSpeech(controlFieldStackCache[count],"end_removedFromControlFieldStack",extraDetail,reason=reason)
		if text:
			textList.append(text)
	# The TextInfo should be considered blank if we are only exiting fields (i.e. we aren't entering any new fields and there is no text).
	textListBlankLen=len(textList)

	#Get speech text for any fields that are in both controlFieldStacks, if extra detail is not requested
	if not extraDetail:
		for count in range(commonFieldCount):
			text=getControlFieldSpeech(newControlFieldStack[count],"start_inControlFieldStack",extraDetail,reason=reason)
			if text:
				textList.append(text)

	#Get speech text for any fields in the new controlFieldStack that are not in the old controlFieldStack
	for count in range(commonFieldCount,len(newControlFieldStack)):
		text=getControlFieldSpeech(newControlFieldStack[count],"start_addedToControlFieldStack",extraDetail,reason=reason)
		if text:
			textList.append(text)
		commonFieldCount+=1

	#Fetch the text for format field attributes that have changed between what was previously cached, and this textInfo's initialFormatField.
	text=getFormatFieldSpeech(info.initialFormatField,formatFieldAttributesCache)
	if text:
		if textListBlankLen==len(textList):
			# If the TextInfo is considered blank so far, it should still be considered blank if there is only formatting thereafter.
			textListBlankLen+=1
		textList.append(text)

	if handleSymbols:
		text=" ".join(textList)
		if text:
			speakText(text,index=index)
		text=info.text
		if len(text)==1:
			speakSpelling(text)
		else:
			speakText(text,index=index)
		info.obj._speakTextInfo_controlFieldStackCache=list(newControlFieldStack)
		info.obj._speakTextInfo_formatFieldAttributesCache=formatFieldAttributesCache
		return

	#Fetch a command list for the text and fields for this textInfo
	commandList=info.textWithFields
	#Move through the command list, getting speech text for all controlStarts, controlEnds and formatChange commands
	#But also keep newControlFieldStack up to date as we will need it for the ends
	# Add any text to a separate list, as it must be handled differently.
	relativeTextList=[]
	for count in range(len(commandList)):
		if isinstance(commandList[count],basestring):
			text=commandList[count]
			if text:
				relativeTextList.append(text)
		elif isinstance(commandList[count],textHandler.FieldCommand) and commandList[count].command=="controlStart":
			text=getControlFieldSpeech(commandList[count].field,"start_relative",extraDetail,reason=reason)
			if text:
				relativeTextList.append(text)
			newControlFieldStack.append(commandList[count].field)
		elif isinstance(commandList[count],textHandler.FieldCommand) and commandList[count].command=="controlEnd":
			text=getControlFieldSpeech(newControlFieldStack[-1],"end_relative",extraDetail,reason=reason)
			if text:
				relativeTextList.append(text)
			del newControlFieldStack[-1]
			if commonFieldCount>len(newControlFieldStack):
				commonFieldCount=len(newControlFieldStack)
		elif isinstance(commandList[count],textHandler.FieldCommand) and commandList[count].command=="formatChange":
			text=getFormatFieldSpeech(commandList[count].field,formatFieldAttributesCache)
			if text:
				relativeTextList.append(text)

	text=" ".join(relativeTextList)
	if text and not text.isspace():
		textList.append(text)

	#Finally get speech text for any fields left in new controlFieldStack that are common with the old controlFieldStack (for closing), if extra detail is not requested
	if not extraDetail:
		for count in reversed(range(min(len(newControlFieldStack),commonFieldCount))):
			text=getControlFieldSpeech(newControlFieldStack[count],"end_inControlFieldStack",extraDetail,reason=reason)
			if text:
				textList.append(text)

	# If there is nothing  that should cause the TextInfo to be considered non-blank, blank should be reported, unless we are doing a say all.
	if reason != REASON_SAYALL and len(textList)==textListBlankLen:
		textList.append(_("blank"))

	#Cache a copy of the new controlFieldStack for future use
	if useCache:
		info.obj._speakTextInfo_controlFieldStackCache=list(newControlFieldStack)
		info.obj._speakTextInfo_formatFieldAttributesCache=formatFieldAttributesCache
	text=" ".join(textList)
	# Only speak if there is speakable text. Reporting of blank text is handled above.
	if text and not text.isspace():
		speakText(text,index=index)

def getSpeechTextForProperties(reason=REASON_QUERY,**propertyValues):
	textList=[]
	if 'name' in propertyValues:
		textList.append(propertyValues['name'])
		del propertyValues['name']
	if 'role' in propertyValues:
		role=propertyValues['role']
		if reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or (role not in silentRolesOnFocus and role not in userDisabledRoles):
			textList.append(controlTypes.speechRoleLabels[role])
		del propertyValues['role']
	elif '_role' in propertyValues:
		role=propertyValues['_role']
	else:
		role=controlTypes.ROLE_UNKNOWN
	if 'value' in propertyValues:
		if not role in silentValuesForRoles:
			textList.append(propertyValues['value'])
		del propertyValues['value']
	states=propertyValues.get('states')
	realStates=propertyValues.get('_states',states)
	if states is not None:
		positiveStates=processPositiveStates(role,realStates,reason,states)
		if reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or (role and role not in userDisabledRoles):
			textList.extend([controlTypes.speechStateLabels[x] for x in positiveStates])
		del propertyValues['states']
	if 'negativeStates' in propertyValues:
		negativeStates=propertyValues['negativeStates']
		del propertyValues['negativeStates']
	else:
		negativeStates=None
	if negativeStates is not None or (reason != REASON_CHANGE and states is not None):
		negativeStates=processNegativeStates(role, realStates, reason, negativeStates)
		if reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or (role and role not in userDisabledRoles):
			textList.extend([_("not %s")%controlTypes.speechStateLabels[x] for x in negativeStates])
	if 'description' in propertyValues:
		textList.append(propertyValues['description'])
		del propertyValues['description']
	if 'keyboardShortcut' in propertyValues:
		textList.append(propertyValues['keyboardShortcut'])
		del propertyValues['keyboardShortcut']
	if 'positionString' in propertyValues:
		if reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or (role and role not in userDisabledRoles):
			textList.append(propertyValues['positionString'])
		del propertyValues['positionString']
	if 'level' in propertyValues:
		levelNo=propertyValues['level']
		del propertyValues['level']
		if levelNo is not None or reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or (role and role not in userDisabledRoles):
			textList.append(_("level %s")%levelNo)
	for name,value in propertyValues.items():
		if not name.startswith('_') and value is not None and value is not "":
			textList.append(name)
			textList.append(unicode(value))
	return " ".join([x for x in textList if x])

def getControlFieldSpeech(attrs,fieldType,extraDetail=False,reason=None):
	childCount=int(attrs['_childcount'])
	indexInParent=int(attrs['_indexinparent'])
	parentChildCount=int(attrs['_parentchildcount'])
	if reason==REASON_FOCUS:
		name=attrs.get('name',"")
	else:
		name=""
	role=attrs['role']
	states=attrs['states']
	keyboardShortcut=attrs['keyboardshortcut']
	level=attrs.get('level',None)
	roleText=getSpeechTextForProperties(reason=reason,role=role)
	stateText=getSpeechTextForProperties(reason=reason,states=states,_role=role)
	keyboardShortcutText=getSpeechTextForProperties(reason=reason,keyboardShortcut=keyboardShortcut)
	nameText=getSpeechTextForProperties(reason=reason,name=name)
	levelText=getSpeechTextForProperties(reason=reason,level=level)
	if role in userDisabledRoles:
		return None
	if not extraDetail and ((reason==REASON_FOCUS and fieldType in ("end_relative","end_inControlFieldStack")) or (reason in (REASON_CARET,REASON_SAYALL) and fieldType in ("start_inControlFieldStack","start_addedToControlFieldStack","start_relative"))) and role in (controlTypes.ROLE_LINK,controlTypes.ROLE_HEADING,controlTypes.ROLE_BUTTON,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_MENUITEM):
		if role==controlTypes.ROLE_LINK:
			return " ".join([x for x in stateText,roleText,keyboardShortcutText])
		else:
			return " ".join([x for x in nameText,roleText,stateText,levelText,keyboardShortcutText if x])
	elif not extraDetail and fieldType in ("start_addedToControlFieldStack","start_relative","start_inControlFieldStack") and ((role==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_MULTILINE not in states and controlTypes.STATE_READONLY not in states) or role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_COMBOBOX,controlTypes.ROLE_SLIDER)): 
		return " ".join([x for x in nameText,roleText,stateText,keyboardShortcutText if x])
	elif not extraDetail and fieldType in ("start_addedToControlFieldStack","start_relative") and role==controlTypes.ROLE_EDITABLETEXT and not controlTypes.STATE_READONLY in states and controlTypes.STATE_MULTILINE in states: 
		return " ".join([x for x in nameText,roleText,stateText,keyboardShortcutText if x])
	elif not extraDetail and fieldType in ("end_removedFromControlFieldStack") and role==controlTypes.ROLE_EDITABLETEXT and not controlTypes.STATE_READONLY in states and controlTypes.STATE_MULTILINE in states: 
		return _("out of %s")%roleText
	elif not extraDetail and fieldType=="start_addedToControlFieldStack" and reason in (REASON_CARET,REASON_SAYALL) and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
		return roleText+_("with %s items")%childCount
	elif not extraDetail and fieldType=="end_removedFromControlFieldStack" and reason in (REASON_CARET,REASON_SAYALL) and role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states:
		return _("out of %s")%roleText
	elif not extraDetail and fieldType=="start_addedToControlFieldStack" and role==controlTypes.ROLE_BLOCKQUOTE:
		return roleText
	elif not extraDetail and fieldType=="end_removedFromControlFieldStack" and role==controlTypes.ROLE_BLOCKQUOTE:
		return _("out of %s")%roleText
	elif not extraDetail and fieldType in ("start_addedToControlFieldStack","start_relative") and ((role==controlTypes.ROLE_LIST and controlTypes.STATE_READONLY not in states) or  role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_COMBOBOX)):
		return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
	elif not extraDetail and fieldType=="start_addedToControlFieldStack" and (role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_TOOLBAR,controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU) or (role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)):
		return " ".join([x for x in roleText,stateText,keyboardShortcutText if x])
	elif not extraDetail and fieldType=="end_removedFromControlFieldStack" and (role in (controlTypes.ROLE_FRAME,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_TOOLBAR,controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU) or (role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)):
		return _("out of %s")%roleText
	elif not extraDetail and fieldType in ("start_addedToControlFieldStack","start_relative")  and controlTypes.STATE_CLICKABLE in states: 
		return getSpeechTextForProperties(states=set([controlTypes.STATE_CLICKABLE]))
	elif extraDetail and fieldType in ("start_addedToControlFieldStack","start_relative") and roleText:
		return _("in %s")%roleText
	elif extraDetail and fieldType in ("end_removedFromControlFieldStack","end_relative") and roleText:
		return _("out of %s")%roleText
	else:
		return ""

def getFormatFieldSpeech(fieldAttrs,attrsCache):
	textList=[]
	for attr,value in fieldAttrs.iteritems():
		if attr not in attrsCache or attrsCache[attr]!=value:
			if isinstance(value,bool):
				if not value and  attr not in attrsCache:
					continue
				if value==True: value=_("on")
				if value==False: value=_("off")
			textList.append("%s %s"%(attr,value))
	attrsCache.update(fieldAttrs)
	return " ".join(textList)
