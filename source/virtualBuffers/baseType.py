from textwrap import TextWrapper
import autoPropertyType
from keyboardHandler import key
import audio
import globalVars
import debug
from constants import *
import core
from config import conf

fieldType_other=0
fieldType_button=1
fieldType_link=2
fieldType_list=3
fieldType_listItem=4
fieldType_heading=5
fieldType_table=6
fieldType_row=7
fieldType_column=8
fieldType_edit=9
fieldType_comboBox=10
fieldType_graphic=11
fieldType_frame=12
fieldType_document=13
fieldType_blockQuote=14
fieldType_paragraph=15
fieldType_form=16
fieldType_checkBox=17
fieldType_radioButton=18
fieldType_editArea=19
fieldType_cell=20
fieldType_tableHeader=21
fieldType_tableFooter=22
fieldType_tableBody=23

fieldNames={
	fieldType_other:"",
	fieldType_button:_("button"),
	fieldType_link:_("link"),
	fieldType_list:_("list"),
	fieldType_listItem:_("list item"),
	fieldType_heading:_("heading"),
	fieldType_table:_("table"),
	fieldType_row:_("row"),
	fieldType_column:_("column"),
	fieldType_edit:_("edit"),
	fieldType_comboBox:_("combo box"),
	fieldType_graphic:_("graphic"),
	fieldType_frame:_("frame"),
	fieldType_document:_("document"),
	fieldType_blockQuote:_("block quote"),
	fieldType_paragraph:_("paragraph"),
	fieldType_form:_("form"),
	fieldType_checkBox:_("check box"),
	fieldType_radioButton:_("radio button"),
	fieldType_editArea:_("edit area"),
	fieldType_cell:_("cell"),
	fieldType_tableHeader:_("table header"),
	fieldType_tableFooter:_("table footer"),
	fieldType_tableBody:_("table body"),
}

fieldInfo={
	"fieldType":fieldType_other,
	"node":None,
	"typeString":"",
	"stateTextFunc":None,
	"descriptionFunc":None,
	"accessKey":None,
}

class virtualBuffer(object):

	__metaclass__=autoPropertyType.autoPropertyType

	def __init__(self,NVDAObject):
		self.neverLoaded=True
		self.NVDAObject=NVDAObject
		self._keyMap={}
		self._allowCaretMovement=True
		self._IDsToRanges={}
		self.text=""
		self.caretPosition=0
		self._lastCaretIDs=[]
		self.registerScriptKeys({
			key("extendedLeft"):self.script_previousCharacter,
			key("extendedRight"):self.script_nextCharacter,
			key("control+extendedLeft"):self.script_previousWord,
			key("control+extendedRight"):self.script_nextWord,
			key("extendedUp"):self.script_previousLine,
			key("extendedDown"):self.script_nextLine,
			key("extendedHome"):self.script_startOfLine,
			key("extendedEnd"):self.script_endOfLine,
			key("control+extendedHome"):self.script_top,
			key("control+extendedEnd"):self.script_bottom,
			key("return"):self.script_activatePosition,
			key("space"):self.script_activatePosition,
			key("extendedPrior"):self.script_pageUp,
			key("extendedNext"):self.script_pageDown,
		})

	def getScript(self,keyPress):
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def registerScriptKey(self,keyPress,methodName):
		self._keyMap[keyPress]=methodName

	def registerScriptKeys(self,keyDict):
		self._keyMap.update(keyDict)

	def getIDsFromPosition(self,pos):
		shortList=filter(lambda x: pos>=self._IDsToRanges[x][0] and pos<self._IDsToRanges[x][1],self._IDsToRanges)
		if shortList:
			return min(shortList,key=lambda x: self._IDsToRanges[x][1]-self._IDsToRanges[x][0])
		else:
			return ()



	def getRangeFromID(self,ID):
		startPos=None
		endPos=None
		for key in filter(lambda x: ID in x,self._IDsToRanges):
			r=self._IDsToRanges[key]
			if (startPos is None) or (r[0]<startPos):
				startPos=r[0]
			if (endPos is None) or (r[1]>endPos):
				endPos=r[1]
		if (startPos is not None) and (endPos is not None):
			return (startPos,endPos)
		else:
			return None

	def getIDsFromID(self,ID):
		for key in self._IDsToRanges:
			if ID in key:
 				index=list(key).index(ID)
				return key[0:index+1]

	def addText(self,IDs,text,position=None):
		maxLineLength=conf["virtualBuffers"]["maxLineLength"]
		if len(text)>maxLineLength:
			wrapper = TextWrapper(width=conf["virtualBuffers"]["maxLineLength"], expand_tabs=False, replace_whitespace=False, break_long_words=False)
			text=wrapper.fill(text)
		#If no position given, assume end of buffer
		if position is None:
			position=len(self.text)
		#If this ID path already has a range, expand it to fit the new text
		if self._IDsToRanges.has_key(IDs) and self._IDsToRanges[IDs][1]<=position:
			(oldStart,oldEnd)=self._IDsToRanges[IDs]
			if oldEnd==position:
				position=position-1
			self.text=self.text[0:position]+text+"\n"+self.text[position+1:]
			extraLength=len(text)+1
			self._IDsToRanges[IDs]=(oldStart,position+extraLength)
		else:
			self.text=self.text[0:position]+text+"\n"+self.text[position:]
			extraLength=len(text)+1
			self._IDsToRanges[IDs]=(position,position+extraLength)
		for item in filter(lambda x: (self._IDsToRanges[x][0]>=position) and (x!=IDs),self._IDsToRanges):
			(start,end)=self._IDsToRanges[item]
			self._IDsToRanges[item]=(start+extraLength,end+extraLength)
		return position+len(text)+1
 
	def removeID(self,ID):
		r=self.getRangeFromID(ID)
		if r:
			(start,end)=r
			self.text=self.text[0:start]+self.text[end:]
		for IDs in filter(lambda x: ID in x,self._IDsToRanges):
			del self._IDsToRanges[IDs]
		del self._IDs[ID]
		for IDs in filter(lambda x: self._IDsToRanges[x][0]>=start,self._IDsToRanges):
			r=self._IDsToRanges[IDs]
			self._IDsToRanges[IDs]=(r[0]-(end-start),r[1]-(end-start))

	def resetBuffer(self):
		self.text=""
		self._IDsToRanges={}
		self._IDs={}
		self.caretPosition=0
		self._lastCaretIDs=[]

	def addID(self,ID,**info):
		self._IDs[ID]=info

	def getIDEnterMessage(self,ID):
		if not self._IDs.has_key(ID):
			return ""
		info=self._IDs[ID]
		fieldType=info["fieldType"]
		vbc=conf["virtualBuffers"]
		if (fieldType==fieldType_link and vbc["reportLinks"]) or (fieldType==fieldType_list and vbc["reportLists"]) or (fieldType==fieldType_listItem and vbc["reportListItems"]) or (fieldType==fieldType_heading and vbc["reportHeadings"]) or (fieldType==fieldType_table and vbc["reportTables"]) or (fieldType==fieldType_tableHeader and vbc["reportTables"]) or (fieldType==fieldType_tableFooter and vbc["reportTables"]) or (fieldType==fieldType_row and vbc["reportTables"]) or (fieldType==fieldType_cell and vbc["reportTables"]) or (fieldType==fieldType_graphic and vbc["reportGraphics"]) or (fieldType==fieldType_form and vbc["reportForms"]) or ((fieldType in [fieldType_button,fieldType_edit,fieldType_editArea,fieldType_checkBox,fieldType_radioButton,fieldType_comboBox]) and vbc["reportFormFields"]) or (fieldType==fieldType_paragraph and vbc["reportParagraphs"]) or (fieldType==fieldType_blockQuote and vbc["reportBlockQuotes"]) or (fieldType==fieldType_frame and vbc["reportFrames"]):
			msg=info["typeString"]
			if callable(info["stateTextFunc"]):
				msg+=" "+info["stateTextFunc"](info["node"])
			if callable(info["descriptionFunc"]):
				msg+=" "+info["descriptionFunc"](info["node"])
			if info["accessKey"]:
				msg+=" "+info["accessKey"]
			return msg
		else:
			return ""

	def getIDExitMessage(self,ID):
		if not self._IDs.has_key(ID):
			return ""
		info=self._IDs[ID]
		fieldType=info["fieldType"]
		vbc=conf["virtualBuffers"]
		if (fieldType==fieldType_list and vbc["reportLists"]) or (fieldType==fieldType_table and vbc["reportTables"]) or (fieldType==fieldType_form and vbc["reportForms"]) or (fieldType==fieldType_editArea and vbc["reportFormFields"]) or (fieldType==fieldType_blockQuote and vbc["reportBlockQuotes"]) or (fieldType==fieldType_paragraph and vbc["reportParagraphs"]) or (fieldType==fieldType_frame and vbc["reportFrames"]):
			return _("out of")+" "+info["typeString"]

	def reportIDMessages(self,newIDs,oldIDs):
		for ID in filter(lambda x: x not in newIDs,oldIDs):
			msg=self.getIDExitMessage(ID)
			if msg:
				audio.speakMessage(msg)
		for ID in filter(lambda x: x not in oldIDs,newIDs):
			msg=self.getIDEnterMessage(ID)
			if msg:
				audio.speakMessage(msg)

	def reportCaretIDMessages(self):
		caretIDs=self.getIDsFromPosition(self.caretPosition)
		self.reportIDMessages(caretIDs,self._lastCaretIDs)
		self._lastCaretIDs=caretIDs

	def _get_startPosition(self):
		return 0

	def _get_endPosition(self):
		return len(self.text)

	def _get_lineCount(self):
		return -1

	def getLineNumber(self,pos):
		return -1

	def getLineStart(self,pos):
		startPos=pos
		if startPos>0 and (self.text[startPos]=='\n'):
			startPos=startPos-1
		while (startPos>-1) and (self.text[startPos]!='\n'):
			startPos-=1
		return startPos+1

	def getLineLength(self,pos):
		startPos=self.getLineStart(pos)
		endPos=startPos
		while (endPos<len(self.text)) and (self.text[endPos]!='\n'):
			endPos+=1
		return (endPos-startPos)

	def getLineEnd(self,pos):
		return self.getLineStart(pos)+self.getLineLength(pos)

	def getLine(self,pos):
		startPos=self.getLineStart(pos)
		length=self.getLineLength(pos)
		endPos=startPos+length
		return self.getTextRange(startPos,endPos)

	def getCharacter(self,pos):
		if pos is not None:
			return self.getTextRange(pos,pos+1)

	def getWord(self,pos):
		wordStart=self.wordStart(pos)
		wordEnd=self.wordEnd(pos)
		return self.getTextRange(wordStart,wordEnd)

	def getTextRange(self,start,end):
		if (start>=end) or (end>len(self.text)):
			return None
		return self.text[start:end]

	def nextCharacter(self,pos):
		if pos<self.endPosition:
			return pos+1
		else:
			return None

	def previousCharacter(self,pos):
		if pos>self.startPosition:
			return pos-1
		else:
			return None

	def inWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.getCharacter(pos) not in whitespace:
			return True
		else:
			return False

	def wordStart(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			while (pos is not None) and (self.getCharacter(pos) not in whitespace):
				oldPos=pos
				pos=self.previousCharacter(pos)
			if pos is None:
				pos=oldPos
			else:
				pos=self.nextCharacter(pos)
		return pos

	def wordEnd(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		while (pos is not None) and (self.getCharacter(pos) not in whitespace):
			oldPos=pos
			pos=self.nextCharacter(pos)
		if pos is not None:
			return pos
		else:
			return oldPos

	def nextWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			pos=self.wordEnd(pos)
		while (pos is not None) and (self.getCharacter(pos) in whitespace):
			pos=self.nextCharacter(pos)
		return pos

	def previousWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			pos=self.wordStart(pos)
			pos=self.previousCharacter(pos)
		while (pos is not None) and (self.getCharacter(pos) in whitespace):
			pos=self.previousCharacter(pos)
		if pos:
			pos=self.wordStart(pos)
		return pos

	def nextLine(self,pos):
		lineLength=self.getLineLength(pos)
		lineStart=self.getLineStart(pos)
		lineEnd=lineStart+lineLength
		newPos=lineEnd+1
		if newPos<self.endPosition:
			return newPos
		else:
			return None

	def previousLine(self,pos):
		lineStart=self.getLineStart(pos)
		pos=lineStart-1
		lineStart=self.getLineStart(pos)
		if lineStart>=self.startPosition:
			return lineStart
		else:
			return None

	def speakCharacter(self,pos):
		audio.speakSymbol(self.getCharacter(pos))

	def speakWord(self,pos):
		#self.getTextRange(self.wordStart(pos),self.wordEnd(pos))
		audio.speakText(self.getWord(pos),index=pos)

	def speakLine(self,pos):
		#self.speakTextRange(self.getLineStart(pos),self.getLineEnd(pos))
		audio.speakText(self.getLine(pos),index=pos)

	def sayAllGenerator(self):
		#Setup the initial info (count, caret position, index etc)
		self._allowCaretMovement=False
		count=0 #Used to see when we need to start yielding
		startPos=endPos=curPos=self.caretPosition
		lastIDs=()
		index=lastIndex=None
		lastKeyCount=globalVars.keyCounter
		#A loop that runs while no key is pressed and while we are not at the end of the text
		while (curPos is not None) and (curPos<self.endPosition):
			#Report any ID messages
			curIDs=self.getIDsFromPosition(curPos)
			self.reportIDMessages(curIDs,lastIDs)
			lastIDs=curIDs
			#Speak the current line (if its not blank) with an speech index of its position
			text=self.getLine(curPos)
			if text and not text.isspace() and (text not in ['\n','\r',""]):
				self.speakLine(curPos)
			#Move our current position down by one line
				endPos=curPos
			curPos=self.nextLine(curPos)
			#Grab the current speech index from the synth, and if different to last, move the caret there
			index=audio.getLastIndex()
			if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
		 		self.caretPosition=index
			lastIndex=index
			#We don't want to yield for the first 4 loops so the synth can get a good run up
			if count>4:
				yield None
			count+=1
			#If the current keyPress count has changed, we need to stop
			if lastKeyCount!=globalVars.keyCounter:
				break
		else: #We fell off the end of the loop (keyPress count didn't change)
			#We are at the end of the document, but the speech most likely isn't yet, so loop so it can catch up
			while (index<endPos):
				index=audio.getLastIndex()
				if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
			 		self.caretPosition=index
				lastIndex=index
				if count>4:
					yield None
				count+=1
				if lastKeyCount!=globalVars.keyCounter:
					break
		#If we did see a keyPress, then we still have to give the speech index a chance to catch up to our current location
		if lastKeyCount!=globalVars.keyCounter:
			for num in range(2):
				yield None
				index=audio.getLastIndex()
				if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
			 		self.caretPosition=index
			audio.cancel()
		self._allowCaretMovement=True

	def script_top(self,keyPress):
		self.caretPosition=0
		self.reportCaretIDMessages()
		audio.speakMessage(_("top"))
		self.speakLine(self.caretPosition)

	def script_bottom(self,keyPress):
		self.caretPosition=len(self.text)-1
		self.reportCaretIDMessages()
		audio.speakMessage(_("bottom"))
		self.speakLine(self.caretPosition)

	def script_pageUp(self,keyPress):
		pageLength=conf["virtualBuffers"]["linesPerPage"]
		curPos=self.caretPosition
		lineCount=0
		while (curPos>0) and (lineCount<=pageLength):
			curPos=curPos-1
			if self.text[curPos]=='\n':
				lineCount+=1
		self.caretPosition=curPos
		if self.caretPosition==0:
			audio.speakMessage(_("top"))
		self.speakLine(self.caretPosition)

	def script_pageDown(self,keyPress):
		pageLength=conf["virtualBuffers"]["linesPerPage"]
		curPos=self.caretPosition
		lineCount=0
		while (curPos<len(self.text)-1) and (lineCount<=pageLength):
			curPos=curPos+1
			if self.text[curPos]=='\n':
				lineCount+=1
		self.caretPosition=curPos
		if self.caretPosition>=len(self.text)-1:
			audio.speakMessage(_("bottom"))
		self.speakLine(self.caretPosition)

	def script_nextLine(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextLine(pos)
		if (pos<len(self.text)) and (nextPos is not None):
			self.caretPosition=nextPos
		else:
			audio.speakMessage(_("bottom"))
		self.reportCaretIDMessages()
		self.speakLine(self.caretPosition)

	def script_previousLine(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousLine(pos)
		if (pos>0) and (prevPos is not None):
			self.caretPosition=prevPos
		else:
			audio.speakMessage(_("top"))
		self.reportCaretIDMessages()
		self.speakLine(self.caretPosition)

	def script_startOfLine(self,keyPress):
		self.caretPosition=self.getLineStart(self.caretPosition)
		self.reportCaretIDMessages()
		self.speakCharacter(self.caretPosition)

	def script_endOfLine(self,keyPress):
		self.caretPosition=(self.getLineStart(self.caretPosition)+self.getLineLength(self.caretPosition)-1)
		self.reportCaretIDMessages()
		self.speakCharacter(self.caretPosition)

	def script_nextWord(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextWord(pos)
		if (pos<len(self.text)) and (nextPos is not None):
			self.caretPosition=(nextPos)
		self.reportCaretIDMessages()
		self.speakWord(self.caretPosition)

	def script_previousWord(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousWord(pos)
		if (prevPos is not None) and (prevPos>=0):
			self.caretPosition=(prevPos)
		self.reportCaretIDMessages()
		self.speakWord(self.caretPosition)

	def script_nextCharacter(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextCharacter(pos)
		if (nextPos<len(self.text)) and (nextPos is not None):
			self.caretPosition=(nextPos)
		self.reportCaretIDMessages()
		self.speakCharacter(self.caretPosition)

	def script_previousCharacter(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousCharacter(pos)
		if (prevPos<len(self.text)) and (prevPos is not None):
			self.caretPosition=prevPos
		self.reportCaretIDMessages()
		self.speakCharacter(self.caretPosition)

	def script_activatePosition(self,keyPress):
		self.activatePosition(self.caretPosition)

	def reportFormatInfo(self):
		IDs=self.getIDsFromPosition(self.caretPosition)
		for ID in IDs[::-1]:
			info=self._IDs[ID]
			audio.speakMessage(info["typeString"])
			debug.writeMessage("ID typeString: %s"%info["typeString"])
			if callable(info["stateTextFunc"]):
				audio.speakMessage(info["stateTextFunc"](info["node"]))
			if callable(info["descriptionFunc"]):
				audio.speakMessage(info["descriptionFunc"](info["node"]))



