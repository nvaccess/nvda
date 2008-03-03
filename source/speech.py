#speech.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""High-level functions to speak information.
@var speechMode: allows speech if true
@type speechMode: boolean
""" 

import sgmllib
from xml.parsers import expat
import time
import globalVars
import logging
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
import userDictHandler

speechMode_off=0
speechMode_beeps=1
speechMode_talk=2
speechMode=2
speechMode_beeps_ms=15
beenCanceled=True
isPaused=False
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
REASON_CARET=7
REASON_DEBUG=8
REASON_ONLYCACHE=9

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
	text = userDictHandler.processText(text)
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
			if (char not in characterSymbols.blankList) and char in characterSymbols.names:
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
		return getSynth().speakText(processSymbol(""))
	if speechMode==speechMode_off:
		return
	elif speechMode==speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if isPaused:
		cancelSpeech()
	beenCanceled=False
	lastKeyCount=globalVars.keyCounter
	if not text.isspace():
		text=text.rstrip()
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
		if globalVars.log.getEffectiveLevel() <= logging.INFO: globalVars.log.info("Speaking \"%s\""%char)
		getSynth().speakText(char,index=index)
		if uppercase and config.conf["speech"][getSynth().name]["raisePitchForCapitals"]:
			getSynth().pitch=oldPitch
		while textLength>1 and globalVars.keyCounter==lastKeyCount and (isPaused or getLastSpeechIndex()!=index): 
			time.sleep(0.05)
			api.processPendingEvents()
			queueHandler.flushQueue(queueHandler.interactiveQueue)
		if globalVars.keyCounter!=lastKeyCount:
			break
		if uppercase and  config.conf["speech"][getSynth().name]["beepForCapitals"]:
			tones.beep(2000,50)

def speakObjectProperties(obj,reason=REASON_QUERY,index=None,**allowedProperties):
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
	allowProperties={'name':True,'role':True,'states':True,'value':True,'description':True,'keyboardShortcut':True,'positionString':True}
	if not config.conf["presentation"]["reportObjectDescriptions"]:
		allowProperties["description"]=False
	if not config.conf["presentation"]["reportKeyboardShortcuts"]:
		allowProperties["keyboardShortcut"]=False
	if not config.conf["presentation"]["reportObjectPositionInformation"]:
		allowProperties["positionString"]=False
	speakObjectProperties(obj,reason=reason,index=index,**allowProperties)
 	if reason not in (REASON_SAYALL,REASON_CARET,REASON_MOUSE) and obj.TextInfo!=NVDAObjects.NVDAObjectTextInfo:
		info=obj.makeTextInfo(textHandler.POSITION_SELECTION)
		if not info.isCollapsed:
			speakMessage(_("selected %s")%info.text)
		else:
			info.expand(textHandler.UNIT_READINGCHUNK)
			speakMessage(info.text)

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
	selectedTextList=[]
	unselectedTextList=[]
	if newInfo.isCollapsed and oldInfo.isCollapsed:
		return
	if newInfo.compareEndPoints(oldInfo,"startToEnd")>=0 or newInfo.compareEndPoints(oldInfo,"endToStart")<=0:
		if speakSelected and not newInfo.isCollapsed:
			selectedTextList.append(newInfo.text)
		if speakUnselected and not oldInfo.isCollapsed:
			unselectedTextList.append(oldInfo.text)
	else:
		leftDiff=newInfo.compareEndPoints(oldInfo,"startToStart")
		rightDiff=newInfo.compareEndPoints(oldInfo,"endToEnd")
		if speakSelected and leftDiff<0 and not newInfo.isCollapsed:
			tempInfo=newInfo.copy()
			tempInfo.setEndPoint(oldInfo,"endToStart")
			selectedTextList.append(tempInfo.text)
		if speakSelected and rightDiff>0 and not newInfo.isCollapsed:
			tempInfo=newInfo.copy()
			tempInfo.setEndPoint(oldInfo,"startToEnd")
			selectedTextList.append(tempInfo.text)
		if leftDiff>0 and not oldInfo.isCollapsed:
			tempInfo=oldInfo.copy()
			tempInfo.setEndPoint(newInfo,"endToStart")
			unselectedTextList.append(tempInfo.text)
		if rightDiff<0 and not oldInfo.isCollapsed:
			tempInfo=oldInfo.copy()
			tempInfo.setEndPoint(newInfo,"startToEnd")
			unselectedTextList.append(tempInfo.text)
	if speakSelected:
		for text in selectedTextList:
			if  len(text)==1:
				text=processSymbol(text)
			speakMessage(_("selected %s")%text)
	if speakUnselected:
		for text in unselectedTextList:
			if  len(text)==1:
				text=processSymbol(text)
			speakMessage(_("unselected %s")%text)

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
			if globalVars.log.getEffectiveLevel() <= logging.INFO: globalVars.log.info("typedword: %s"%typedWord)
			typedWord=""
	else:
		typedWord=""

silentRolesOnFocus=set([
	controlTypes.ROLE_LISTITEM,
	controlTypes.ROLE_MENUITEM,
	controlTypes.ROLE_TREEVIEWITEM,
])

def processPositiveStates(role, states, reason, positiveStates):
	positiveStates = positiveStates.copy()
	# The user never cares about certain states.
	positiveStates.discard(controlTypes.STATE_SELECTABLE)
	if reason == REASON_QUERY:
		return positiveStates
	positiveStates.discard(controlTypes.STATE_FOCUSED)
	if reason in (REASON_FOCUS, REASON_CARET, REASON_SAYALL):
		positiveStates.difference_update(frozenset((controlTypes.STATE_INVISIBLE, controlTypes.STATE_READONLY, controlTypes.STATE_LINKED)))
		if role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_TREEVIEWITEM) and controlTypes.STATE_SELECTABLE in states:
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
	if role in (controlTypes.ROLE_CHECKBOX, controlTypes.ROLE_RADIOBUTTON):
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

class XMLContextParser(object): 

	def __init__(self):
		self.parser=expat.ParserCreate()
		self.parser.StartElementHandler=self._startElementHandler
		#self.parser.EndElementHandler=self._EndElementHandler
		#self.parser.CharacterDataHandler=self._CharacterDataHandler
		self._fieldStack=[]

	def _startElementHandler(self,name,attrs):
		newAttrs={}
		for name,value in attrs.items():
			newAttrs[name.lower()]=value
		self._fieldStack.append(newAttrs)

	def parse(self,XMLContext):
		try:
			self.parser.Parse(XMLContext)
		except:
			globalVars.log.warn("XML: %s"%XMLContext,exc_info=True)
		return self._fieldStack

class RelativeXMLParser(object):

	def __init__(self):
		self.parser=sgmllib.SGMLParser()
		self.parser.unknown_starttag=self._startElementHandler
		self.parser.unknown_endtag=self._endElementHandler
		self.parser.handle_data=self._characterDataHandler
		self._commandList=[]

	def _startElementHandler(self,tag,attrs):
		newAttrs={}
		for attr in attrs:
			newAttrs[attr[0]]=attr[1]
		attrs=newAttrs
		self._commandList.append(("start",attrs))

	def _endElementHandler(self,tag):
		self._commandList.append(("end",None))

	def _characterDataHandler(self,data):
		self._commandList.append(("text",data))

	def parse(self,relativeXML):
		self.parser.feed(relativeXML)
		return self._commandList

def speakFormattedTextWithXML(XMLContext,relativeXML,cacheObject,getFieldSpeechFunc,extraDetail=False,cacheFinalStack=False,reason=REASON_QUERY,wait=False,index=None):
		textList=[]
		#Fetch the last stack, or make a blank one
		oldStack=getattr(cacheObject,'_speech_XMLCache',[])
		#Create a new stack from the XML context
		stackParser=XMLContextParser()
		globalVars.log.warning("type: %s"%type(XMLContext))
		newStack=stackParser.parse(XMLContext)
		#Cache a copy of the new stack for future use
		if not cacheFinalStack:
			cacheObject._speech_XMLCache=list(newStack)
		#Calculate how many fields in the old and new stacks are the same
		commonFieldCount=0
		for count in range(min(len(newStack),len(oldStack))):
			if newStack[count]==oldStack[count]:
				commonFieldCount+=1
			else:
				break
		#Get speech text for any fields in the old stack that are not in the new stack 
		for count in reversed(range(commonFieldCount,len(oldStack))):
			textList.append(getFieldSpeechFunc(oldStack[count],"end_removedFromStack",extraDetail,reason=reason))
		#Get speech text for any fields that are in both stacks, if extra detail is not requested
		if not extraDetail:
			for count in range(commonFieldCount):
				textList.append(getFieldSpeechFunc(newStack[count],"start_inStack",extraDetail,reason=reason))
		#Get speech text for any fields in the new stack that are not in the old stack
		for count in range(commonFieldCount,len(newStack)):
			textList.append(getFieldSpeechFunc(newStack[count],"start_addedToStack",extraDetail,reason=reason))
			commonFieldCount+=1
		#Fetch a command list for the relative XML
		commandParser=RelativeXMLParser()
		commandList=commandParser.parse(relativeXML) if relativeXML is not None else []
		#Move through the command list, getting speech text for all starts and ends
		#But also keep newStack up to date as we will need it for the ends
		# Add any text to a separate list, as it must be handled differently.
		relativeTextList=[]
		for count in range(len(commandList)):
			if commandList[count][0]=="text":
				relativeTextList.append(commandList[count][1])
			elif commandList[count][0]=="start":
				relativeTextList.append(getFieldSpeechFunc(commandList[count][1],"start_relative",extraDetail,reason=reason))
				newStack.append(commandList[count][1])
			elif commandList[count][0]=="end" and len(newStack)>0:
				relativeTextList.append(getFieldSpeechFunc(newStack[-1],"end_relative",extraDetail,reason=reason))
				del newStack[-1]
				if commonFieldCount>len(newStack):
					commonFieldCount=len(newStack)
		if relativeTextList:
			text=" ".join(relativeTextList)
			# We are handling relative XML. Any actual text content will be produced here.
			# Therefore, if no speakable text was produced, this should be reported as blank, unless we're doing a say all.
			if reason != REASON_SAYALL and (not text or text.isspace()):
				textList.append(_("blank"))
			else:
				textList.append(text)
		#Finally get speech text for any fields left in new stack that are common with the old stack (for closing), if extra detail is not requested
		if not extraDetail:
			for count in reversed(range(min(len(newStack),commonFieldCount))):
				textList.append(getFieldSpeechFunc(newStack[count],"end_inStack",extraDetail,reason=reason))
		#Cache a copy of the new stack for future use
		if cacheFinalStack:
			cacheObject._speech_XMLCache=list(newStack)
		text=" ".join(textList)
		# Only speak if there is speakable text. Reporting of blank text is handled above.
		if text and not text.isspace():
			speakText(text,wait=wait,index=index)

def getFieldSpeech(attrs,fieldType,extraDetail=False):
		if not extraDetail and fieldType in ("end_relative","end_inStack") and attrs['role']==controlTypes.ROLE_LINK:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_LINK]
		if not extraDetail and fieldType in ("end_relative","end_inStack") and attrs['role']==controlTypes.ROLE_HEADING:
			return controlTypes.speechRoleLabels[controlTypes.ROLE_HEADING]
		elif extraDetail and fieldType in ("start_addedToStack","start_relative"):
			return "in %s"%controlTypes.speechRoleLabels[attrs['role']]
		elif extraDetail and fieldType in ("end_removedFromStack","end_relative"):
			return "out of %s"%controlTypes.speechRoleLabels[attrs['role']]
		else:
			return ""

def getSpeechTextForProperties(reason=REASON_QUERY,**propertyValues):
	textList=[]
	if 'name' in propertyValues:
		textList.append(propertyValues['name'])
		del propertyValues['name']
	if 'role' in propertyValues:
		role=propertyValues['role']
		if reason not in (REASON_SAYALL,REASON_CARET,REASON_FOCUS) or  role not in silentRolesOnFocus:
			textList.append(controlTypes.speechRoleLabels[role])
		del propertyValues['role']
	elif '_role' in propertyValues:
		role=propertyValues['_role']
	else:
		role=controlTypes.ROLE_UNKNOWN
	if 'value' in propertyValues:
		textList.append(propertyValues['value'])
		del propertyValues['value']
	states=propertyValues.get('states')
	realStates=propertyValues.get('_states',states)
	if states is not None:
		positiveStates=processPositiveStates(role,realStates,reason,states)
		textList.extend([controlTypes.speechStateLabels[x] for x in positiveStates])
		del propertyValues['states']
	if 'negativeStates' in propertyValues:
		negativeStates=propertyValues['negativeStates']
		del propertyValues['negativeStates']
	else:
		negativeStates=None
	if negativeStates is not None or (reason != REASON_CHANGE and states is not None):
		negativeStates=processNegativeStates(role, realStates, reason, negativeStates)
		textList.extend([_("not %s")%controlTypes.speechStateLabels[x] for x in negativeStates])
	if 'description' in propertyValues:
		textList.append(propertyValues['description'])
		del propertyValues['description']
	if 'keyboardShortcut' in propertyValues:
		textList.append(propertyValues['keyboardShortcut'])
		del propertyValues['keyboardShortcut']
	if 'positionString' in propertyValues:
		textList.append(propertyValues['positionString'])
		del propertyValues['positionString']
	for name,value in propertyValues.items():
		if not name.startswith('_') and value is not None and value is not "":
			textList.append(name)
			textList.append(unicode(value))
	return " ".join([x for x in textList if x])
