#speech.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""High-level functions to speak information.
@var speechMode: allows speech if true
@type speechMode: boolean
""" 

import time
import debug
import api
import controlTypes
import config
import tones
from synthDriverHandler import *
import re
import characterSymbols

speechMode_off=0
speechMode_beeps=1
speechMode_talk=2
speechMode=2
speechMode_beeps_ms=15
beenCanceled=True
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
REASON_QUERY=2
REASON_CHANGE=3
REASON_MESSAGE=4
REASON_DEBUG=5

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
	global beenCanceled
	if beenCanceled:
		return
	elif speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		return
	getSynth().cancel()
	beenCanceled=True

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

def speakObjectProperties(obj,groupName=False,name=False,role=False,states=False,value=False,description=False,keyboardShortcut=False,positionString=False,level=False,contains=False,reason=REASON_QUERY):
	global beenCanceled
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
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
		if isinstance(roleNum,int) and (reason!=REASON_FOCUS or roleNum not in silentRolesOnFocus):
			textList.append(controlTypes.speechRoleLabels[roleNum])
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
		elif reason==REASON_FOCUS:
			positiveStateSet=positiveStateSet-silentPositiveStatesOnFocus[controlTypes.ROLE_UNKNOWN]
			if roleNum!=controlTypes.ROLE_UNKNOWN and silentPositiveStatesOnFocus.has_key(roleNum):
				positiveStateSet=positiveStateSet-silentPositiveStatesOnFocus[roleNum]
			textList.extend([controlTypes.speechStateLabels[state] for state in positiveStateSet])
		else:
			textList.extend([controlTypes.speechStateLabels[state] for state in positiveStateSet])
		if spokenNegativeStates.has_key(roleNum):
			negativeStateSet=negativeStateSet|(spokenNegativeStates[roleNum]-stateSet)
			if reason==REASON_CHANGE:
				oldNegativeStateSet=oldNegativeStateSet|(spokenNegativeStates[roleNum]-oldStateSet)
		textList.extend([_("not %s")%controlTypes.speechStateLabels[state] for state in (negativeStateSet-oldNegativeStateSet)])
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
	if keyboardShortcut:
		keyboardShortcutText=obj.keyboardShortcut
		if isinstance(keyboardShortcutText,basestring) and len(keyboardShortcutText)>0 and not keyboardShortcutText.isspace():
			textList.append(keyboardShortcutText)
	if positionString:
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
	text=" ".join(textList)
	if len(text)>0 and not text.isspace():
		text=processText(text)
		getSynth().speakText(text)

def speakObject(obj,reason=REASON_QUERY):
	speakObjectProperties(obj,groupName=True,name=True,role=True,states=True,value=True,description=True,keyboardShortcut=True,positionString=True,level=True,contains=True,reason=reason)

def speakSymbol(symbol,wait=False,index=None):
	"""Speaks a given single character.
This function will not speak if L{speechMode} is false.
If the character is uppercase, then the pitch of the synthesizer will be altered by a value in nvda.ini and then set back to its origional value. This is to audibly denote capital letters.
Before passing the symbol to the synthersizer, L{textProcessing.processSymbol} is used to expand the symbol to a  speakable word.
@param symbol: the symbol to speak
@type symbol: string
@param wait: if true, the function will not return until the text has finished being spoken. If false, the function will return straight away.
@type wait: boolean
@param index: the index to mark this current text with 
@type index: int
"""
	global beenCanceled
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	beenCanceled=False
	text=processSymbol(symbol)
	if symbol is not None and len(symbol)==1 and symbol.isupper(): 
		uppercase=True
	else:
		uppercase=False
	if uppercase:
		if config.conf["speech"][getSynth().name]["sayCapForCapitals"]:
			text=_("cap %s")%text
		oldPitch=config.conf["speech"][getSynth().name]["pitch"]
		getSynth().pitch=max(0,min(oldPitch+config.conf["speech"][getSynth().name]["capPitchChange"],100))
	getSynth().speakText(text,wait=wait,index=index)
	if uppercase:
		getSynth().pitch=oldPitch

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
	beenCanceled=False
	text=processText(text)
	if text and not text.isspace():
		getSynth().speakText(text,wait=wait,index=index)

def speakTypedCharacters(ch):
	global typedWord
	if api.isTypingProtected():
		ch="*"
	if config.conf["keyboard"]["speakTypedCharacters"]:
		speakSymbol(ch)
	if config.conf["keyboard"]["speakTypedWords"]: 
		if ch.isalnum():
			typedWord="".join([typedWord,ch])
		elif len(typedWord)>0:
			speakText(typedWord)
			typedWord=""
	else:
		typedWord=""

silentRolesOnFocus=frozenset([
	controlTypes.ROLE_LISTITEM,
	controlTypes.ROLE_MENUITEM,
	controlTypes.ROLE_TREEVIEWITEM,
])

silentPositiveStatesOnFocus={
	controlTypes.ROLE_UNKNOWN:frozenset([controlTypes.STATE_FOCUSED]),
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
}
