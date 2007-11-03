#speech.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""High-level functions to speak information.
@var speechMode: allows speech if true
@type speechMode: boolean
""" 

from xml.parsers import expat
import time
import debug
import globalVars
import api
import controlTypes
import config
import tones
from synthDriverHandler import *
import re
import textHandler
import characterSymbols
import NVDAObjects
import queueHandler

speechMode_off=0
speechMode_beeps=1
speechMode_talk=2
speechMode=2
speechMode_beeps_ms=15
beenCanceled=True
isPaused=False
re_capAfterNoCapsInWord=re.compile(r"([a-z])([A-Z])")
re_singleCapAfterCapsInWord=re.compile(r"([A-Z])([A-Z][a-z])")
re_numericAfterAlphaInWord=re.compile(r"([a-zA-Z])([0-9])")
re_sentence_dot=re.compile(r"(\w|\)|\"|')\.(\s|$)")
re_sentence_comma=re.compile(r"(\w|\)|\"|'),(\s|$)")
re_sentence_question=re.compile(r"(\w|\))\?(\s|$)")
re_sentence_colon=re.compile(r"(\w|\)|\"|'):(\s|$)")
re_sentence_semiColon=re.compile(r"(\w|\)|\"|');(\s|$)")
re_sentence_exclimation=re.compile(r"(\w|\)|\"|')!(\s|$)")
re_word_apostraphy=re.compile(r"(\w)'(\w)")
typedWord=""
REASON_FOCUS=1
REASON_MOUSE=2
REASON_QUERY=3
REASON_CHANGE=4
REASON_MESSAGE=5
REASON_SAYALL=6
REASON_DEBUG=7

globalXMLFieldStack=[]
XMLFIELD_COMMON=1
XMLFIELD_WASCOMMON=2

def initialize():
	"""Loads and sets the synth driver configured in nvda.ini."""
	setSynth(config.conf["speech"]["synth"])

def terminate():
	setSynth(None)

def processTextSymbols(text,expandPunctuation=False):
	if (text is None) or (len(text)==0) or (isinstance(text,basestring) and (set(text)<=set(characterSymbols.blankList))):
		return _("blank") 
	#Convert non-breaking spaces to spaces
	if isinstance(text,basestring):
		text=text.replace(u'\xa0',u' ')
	#Limit groups of the same character to 5 or less.
	trunkatedText=""
	lastChar=""
	sameCharCount=0
	for char in text:
		if char==lastChar:
			sameCharCount+=1
		else:
			sameCharCount=1
		if sameCharCount<11:
			trunkatedText="".join([trunkatedText,char])
		lastChar=char
	text=trunkatedText
	#breaks up words that use a capital letter to denote another word
	text=re_capAfterNoCapsInWord.sub(r"\1 \2",text)
	#Like the last one, but this breaks away the last capital letter from an entire group of capital letters imbedded in a word (e.g. NVDAObject) 
	text=re_singleCapAfterCapsInWord.sub(r"\1 \2",text)
	#Breaks words that have numbers at the end
	text=re_numericAfterAlphaInWord.sub(r"\1 \2",text)
	#expands ^ and ~ so they can be used as protector symbols
	#Expands special sentence punctuation keeping the origional physical symbol but protected by ^ and ~
	#Expands any other symbols and removes ^ and ~ protectors
	if expandPunctuation is False:
		return text 
	protector=False
	buf=""
	for char in text:
		if (char=="^") or (char=="~"):
			buf+=" %s "%characterSymbols.names[char]
		else:
			buf+=char
	text=buf
	text=re_sentence_dot.sub(r"\1 ^%s.~ \2"%characterSymbols.names["."],text)
	text=re_sentence_comma.sub(r"\1 ^%s,~ \2"%characterSymbols.names[","],text)
	text=re_sentence_question.sub(r"\1 ^%s?~ \2"%characterSymbols.names["?"],text)
	text=re_sentence_colon.sub(r"\1 ^%s:~ \2"%characterSymbols.names[":"],text)
	text=re_sentence_semiColon.sub(r"\1 ^%s;~ \2"%characterSymbols.names[";"],text)
	text=re_sentence_exclimation.sub(r"\1 ^%s!~ \2"%characterSymbols.names["!"],text)
	#text=re_word_apostraphy.sub(r"\1 %s^.~ \2"%characterSymbols.names["'"],text)
	buf=""
	for char in text:
		if char=="^":
			protector=True
			buf+="^"
			continue
		if char=="~":
			protector=False
			buf+="~"
			continue
		if not protector:
			if (char not in characterSymbols.blankList) and characterSymbols.names.has_key(char):
				buf+=" ^%s~ "%characterSymbols.names[char]
			else:
				buf+=char
		else:
			buf+=char
	text=buf
	text=text.replace("^","")
	text=text.replace("~","")
	return text

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

def speakMessage(text,wait=False,index=None):
	"""Speaks a given message.
This function will not speak if L{speechMode} is false.
@param text: the message to speak
@type text: string
@param wait: if true, the function will not return until the text has finished being spoken. If false, the function will return straight away.
@type wait: boolean
@param index: the index to mark this current text with, its best to use the character position of the text if you know it 
@type index: int
"""
	global beenCanceled
	speakText(text,wait=wait,index=index,reason=REASON_MESSAGE)

def speakSpelling(text):
	global beenCanceled
	if not isinstance(text,basestring) or len(text)==0:
		return
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	lastKeyCount=globalVars.keyCounter
	if text[0].isupper() and config.conf["speech"][getSynth().name]["beepForCapitals"]:
		tones.beep(2000,50)
	for count,char in enumerate(text): 
		uppercase=char.isupper()
		char=processSymbol(char)
		if uppercase and config.conf["speech"][getSynth().name]["sayCapForCapitals"]:
			char=_("cap %s")%char
		if uppercase and config.conf["speech"][getSynth().name]["raisePitchForCapitals"]:
			oldPitch=config.conf["speech"][getSynth().name]["pitch"]
			getSynth().pitch=max(0,min(oldPitch+config.conf["speech"][getSynth().name]["capPitchChange"],100))
		index=count+1
		getSynth().speakText(char,index=index)
		if uppercase and config.conf["speech"][getSynth().name]["raisePitchForCapitals"]:
			getSynth().pitch=oldPitch
		while globalVars.keyCounter==lastKeyCount and (isPaused or getLastSpeechIndex()!=index): 
			time.sleep(0.05)
			api.processPendingEvents()
			queueHandler.flushQueue(queueHandler.interactiveQueue)
		if globalVars.keyCounter!=lastKeyCount:
			break
		if count>0 and uppercase and  config.conf["speech"][getSynth().name]["beepForCapitals"]:
			tones.beep(2000,50)

def speakObjectProperties(obj,groupName=False,name=False,role=False,states=False,value=False,description=False,keyboardShortcut=False,positionString=False,level=False,contains=False,textInfo=False,reason=REASON_QUERY,index=None):
	global beenCanceled
	del globalXMLFieldStack[:]
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	textList=[]
	if groupName:
		groupNameText=obj.groupName
		if isinstance(groupNameText,basestring) and len(groupNameText)>0 and not groupNameText.isspace():
			textList.append(groupNameText)
	if name:
		nameText=obj.name
		if isinstance(nameText,basestring) and len(nameText)>0 and not nameText.isspace():
			textList.append(nameText)
	if role:
		roleNum=obj.role
		if isinstance(roleNum,int) and (reason not in (REASON_FOCUS,REASON_SAYALL) or roleNum not in silentRolesOnFocus):
			textList.append(controlTypes.speechRoleLabels[roleNum])
	stateList=[]
	if states:
		stateSet=obj.states
		oldStateSet=obj._oldStates
		positiveStateSet=stateSet
		oldPositiveStateSet=oldStateSet
		negativeStateSet=set()
		oldNegativeStateSet=set()
		if not role:
			roleNum=obj.role
		if reason==REASON_CHANGE:
			positiveStateSet=positiveStateSet-silentPositiveStatesOnStateChange[controlTypes.ROLE_UNKNOWN]
			oldPositiveStateSet=oldPositiveStateSet-silentPositiveStatesOnStateChange[controlTypes.ROLE_UNKNOWN]
			if roleNum!=controlTypes.ROLE_UNKNOWN and silentPositiveStatesOnStateChange.has_key(roleNum):
				positiveStateSet=positiveStateSet-silentPositiveStatesOnStateChange[roleNum]
				oldPositiveStateSet=oldPositiveStateSet-silentPositiveStatesOnStateChange[roleNum]
			textList.extend([controlTypes.speechStateLabels[state] for state in (positiveStateSet-oldPositiveStateSet)])
		elif reason in (REASON_FOCUS,REASON_SAYALL):
			positiveStateSet=positiveStateSet-silentPositiveStatesOnFocus[controlTypes.ROLE_UNKNOWN]
			if roleNum!=controlTypes.ROLE_UNKNOWN and silentPositiveStatesOnFocus.has_key(roleNum):
				positiveStateSet=positiveStateSet-silentPositiveStatesOnFocus[roleNum]
			stateList.extend([controlTypes.speechStateLabels[state] for state in positiveStateSet])
		else:
			stateList.extend([controlTypes.speechStateLabels[state] for state in positiveStateSet])
		if spokenNegativeStates.has_key(roleNum):
			negativeStateSet=negativeStateSet|(spokenNegativeStates[roleNum]-stateSet)
			if reason==REASON_CHANGE:
				oldNegativeStateSet=oldNegativeStateSet|(spokenNegativeStates[roleNum]-oldStateSet)
		stateList.extend([_("not %s")%controlTypes.speechStateLabels[state] for state in (negativeStateSet-oldNegativeStateSet)])
	if config.conf["presentation"]["sayStateFirst"]:
		textList.insert(0," ".join(stateList))
	else:
		textList.append(" ".join(stateList))
	if value:
		valueText=obj.value
		if isinstance(valueText,basestring) and len(valueText)>0 and not valueText.isspace():
			textList.append(valueText)
	if description:
		descriptionText=obj.description
		if not name:
			nameText=obj.name
		if descriptionText!=nameText and isinstance(descriptionText,basestring) and len(descriptionText)>0 and not descriptionText.isspace():
			textList.append(descriptionText)
	if keyboardShortcut and (reason not in (REASON_FOCUS,REASON_SAYALL) or config.conf["presentation"]["reportKeyboardShortcuts"]):
		keyboardShortcutText=obj.keyboardShortcut
		if isinstance(keyboardShortcutText,basestring) and len(keyboardShortcutText)>0 and not keyboardShortcutText.isspace():
			textList.append(keyboardShortcutText)
	if positionString and (reason not in (REASON_FOCUS,REASON_SAYALL) or config.conf["presentation"]["reportObjectPositionInformation"]):
		positionStringText=obj.positionString
		if isinstance(positionStringText,basestring) and len(positionStringText)>0 and not positionStringText.isspace():
			textList.append(positionStringText)
	if level:
		levelNum=obj.level
		if isinstance(levelNum,int):
			textList.append(_("level %d")%levelNum)
	if contains:
		containsText=obj.contains
		if isinstance(containsText,basestring) and len(containsText)>0 and not containsText.isspace():
			textList.append(_("contains %s")%containsText)
	if textInfo and obj.TextInfo!=NVDAObjects.NVDAObjectTextInfo:
		info=obj.makeTextInfo(textHandler.POSITION_SELECTION)
		if not info.isCollapsed:
			textList.append(_("selected %s")%info.text)
		else:
			info.expand(textHandler.UNIT_READINGCHUNK)
			textList.append(info.text)
	text=" ".join(textList)
	if len(text)>0 and not text.isspace():
		text=processText(text)
		getSynth().speakText(text,index=index)

def speakObject(obj,reason=REASON_QUERY,index=None):
	speakObjectProperties(obj,groupName=True,name=True,role=True,states=True,value=True,description=True,keyboardShortcut=True,positionString=True,level=True,contains=True,textInfo=True,reason=reason,index=index)

def speakText(text,index=None,wait=False,reason=REASON_MESSAGE):
	"""Speaks some given text.
This function will not speak if L{speechMode} is false.
@param text: the message to speak
@type text: string
@param wait: if true, the function will not return until the text has finished being spoken. If false, the function will return straight away.
@type wait: boolean
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
		getSynth().speakText(text,wait=wait,index=index)

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

def speakFormattedText(textInfo,handleSymbols=False,includeBlankText=True,wait=False,index=None):
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
					speakText(item,wait=wait,index=index)
			else:
				speech.speakSpelling(item)
	textInfo.obj._lastInitialSpokenFormats=initialSpokenFormats

def speakSelectionChange(oldInfo,newInfo,speakSelected=True,speakUnselected=True,speakSelectionDeleted=True):
	if newInfo.isCollapsed and oldInfo.isCollapsed:
		return
	leftDelta=newInfo.compareStart(oldInfo)
	rightDelta=newInfo.compareEnd(oldInfo)
	leftSelectedText=None
	leftUnselectedText=None
	rightSelectedText=None
	rightUnselectedText=None
	selectionDeleted=False
	if speakSelected and leftDelta<0 and not newInfo.isCollapsed:
		tempInfo=newInfo.copy()
		tempInfo.collapse()
		tempInfo.moveByUnit(textHandler.UNIT_CHARACTER,abs(leftDelta),start=False)
		leftSelectedText=tempInfo.text
	if speakSelected and rightDelta>0 and not newInfo.isCollapsed:
		tempInfo=newInfo.copy()
		tempInfo.collapse(end=True)
		tempInfo.moveByUnit(textHandler.UNIT_CHARACTER,0-rightDelta,end=False)
		rightSelectedText=tempInfo.text
	if leftDelta>0 and not oldInfo.isCollapsed:
		tempInfo=newInfo.copy()
		tempInfo.collapse()
		res=tempInfo.moveByUnit(textHandler.UNIT_CHARACTER,0-leftDelta,end=False)
		if res!=(0-leftDelta):
			selectionDeleted=True
		else:
			leftUnselectedText=tempInfo.text
	if rightDelta<0 and not oldInfo.isCollapsed:
		tempInfo=newInfo.copy()
		tempInfo.collapse(end=True)
		res=tempInfo.moveByUnit(textHandler.UNIT_CHARACTER,abs(rightDelta),start=False)
		if res!=abs(rightDelta):
			selectionDeleted=True
		else:
			rightUnselectedText=tempInfo.text
	if speakSelected:
		for selected in (leftSelectedText,rightSelectedText):
			if isinstance(selected,basestring):
				if  len(selected)==1:
					selected=processSymbol(selected)
				speakMessage(_("selected %s")%selected)
	if speakUnselected:
		for unselected in (leftUnselectedText,rightUnselectedText):
			if isinstance(unselected,basestring):
				if  len(unselected)==1:
					unselected=processSymbol(unselected)
				speakMessage(_("unselected %s")%unselected)
	if speakSelectionDeleted and selectionDeleted:
		speech.speakMessage(_("selection deleted"))


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
			debug.writeMessage("typedword: %s"%typedWord)
			typedWord=""
	else:
		typedWord=""

silentRolesOnFocus=frozenset([
	controlTypes.ROLE_LISTITEM,
	controlTypes.ROLE_MENUITEM,
	controlTypes.ROLE_TREEVIEWITEM,
])

silentPositiveStatesOnFocus={
	controlTypes.ROLE_UNKNOWN:frozenset([controlTypes.STATE_FOCUSED,controlTypes.STATE_INVISIBLE]),
	controlTypes.ROLE_LISTITEM:frozenset([controlTypes.STATE_SELECTED]),
	controlTypes.ROLE_TREEVIEWITEM:frozenset([controlTypes.STATE_SELECTED]),
	controlTypes.ROLE_LINK:frozenset([controlTypes.STATE_LINKED]),
}

silentPositiveStatesOnStateChange={
	controlTypes.ROLE_UNKNOWN:frozenset([controlTypes.STATE_FOCUSED]),
	controlTypes.ROLE_CHECKBOX:frozenset([controlTypes.STATE_PRESSED]),
}

spokenNegativeStates={
	controlTypes.ROLE_LISTITEM:frozenset([controlTypes.STATE_SELECTED]),
	controlTypes.ROLE_CHECKBOX: frozenset([controlTypes.STATE_CHECKED]),
	controlTypes.ROLE_RADIOBUTTON: frozenset([controlTypes.STATE_CHECKED]),
}

class XMLFieldParser(object):

	def __init__(self):
		self.parser=expat.ParserCreate()
		self.parser.StartElementHandler=self._StartElementHandler
		self.parser.EndElementHandler=self._EndElementHandler
		self.parser.CharacterDataHandler=self._CharacterDataHandler
		self._commandList=[]
		self._fieldStack=[]

	def parse(self,xml):
		#parse the xml, creating a list of fields and text
		self.parser.Parse(xml)
		return self._commandList

	def _StartElementHandler(self,name,attrs):
		field=(name,attrs)
		self._fieldStack.append(field)
		cmd=["start",field,False]
		if len(self._commandList)>0 and self._commandList[-1][0]=="end" and field==self._commandList[-1][1]:
			del self._commandList[-1]
		else:
			self._commandList.append(["start",field,False])

	def _EndElementHandler(self,name):
		field=self._fieldStack[-1]
		del self._fieldStack[-1]
		self._commandList.append(["end",field,False])

	def _CharacterDataHandler(self,data):
		self._commandList.append(("text",data))

def getFormatCommandText(cmd):
	if cmd[0]=="text":
		return cmd[1]
	elif cmd[0]=="start" and not cmd[2]&XMLFIELD_COMMON:
		return "%s %s"%(controlTypes.speechRoleLabels[int(cmd[1][1]['role'])],cmd[1][1]['value'])
	elif cmd[0]=="end" and not cmd[2]&XMLFIELD_COMMON:
		return "%s end"%controlTypes.speechRoleLabels[int(cmd[1][1]['role'])]
	else:
		return ""

def newSpeakFormattedText(data):
	p=XMLFieldParser()
	commandList=p.parse(data)
	#Find and mark the common fields in the list
	commonFieldCount=0
	globalXMLFieldStackLen=len(globalXMLFieldStack)
	commandListLen=len(commandList)
	for index in range(min(commandListLen,globalXMLFieldStackLen)):
		if commandList[index][0]=="start" and commandList[index][1]==globalXMLFieldStack[index]:
			commandList[index][2]=XMLFIELD_COMMON
			commonFieldCount+=1
		else:
			break
	#Find the initial fields that should be added to the common fields 
	addedGlobalFields=[]
	for index in range(commonFieldCount,commandListLen):
		if commandList[index][0]=="start":
			addedGlobalFields.append(commandList[index][1])
		else:
			break
	#Prepend end field commands to the field list for the common fields we are no longer a part of
	if globalXMLFieldStackLen>0:
		for index in range(commonFieldCount,globalXMLFieldStackLen):
			commandList.insert(0,["end",globalXMLFieldStack[index],XMLFIELD_WASCOMMON])
		del globalXMLFieldStack[commonFieldCount:]
	globalXMLFieldStack.extend(addedGlobalFields)
	fieldListLen=len(commandList)
	globalXMLFieldStackLen=len(globalXMLFieldStack)
	for index in range(min(fieldListLen,globalXMLFieldStackLen)):
		fieldListIndex=(fieldListLen-1)-index
		if index<globalXMLFieldStackLen and commandList[fieldListIndex][0]=='end':
			commandList[fieldListIndex][2]=XMLFIELD_COMMON
		else:
			break
	textList=[]
	for cmd in commandList:
		textList.append(getFormatCommandText(cmd))
	speakText(" ".join(textList))

def speakFormat(data):
	p=XMLFieldParser()
	commandList=p.parse(data)
	textList=[]
	for cmd in commandList:
		if cmd[0]=="start":
			textList.append(getFormatCommandText(cmd))
		else:
			break
	speakText(" ".join(textList))
