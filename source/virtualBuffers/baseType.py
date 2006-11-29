import autoPropertyType
from keyboardHandler import key
import audio
import globalVars
import debug

class virtualBuffer(object):

	__metaclass__=autoPropertyType.autoPropertyType

	def __init__(self,NVDAObject):
		self.NVDAObject=NVDAObject
		self._keyMap={}
		self._allowCaretMovement=True
		self._IDsCollection={}
		self._text=""
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
		})

	def getScript(self,keyPress):
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def registerScriptKey(self,keyPress,methodName):
		self._keyMap[keyPress]=methodName

	def registerScriptKeys(self,keyDict):
		self._keyMap.update(keyDict)

	def getIDsFromPosition(self,pos):
 		for IDs in self._IDsCollection:
			(startPos,endPos)=self._IDsCollection[IDs]
			if (pos>=startPos) and (pos<endPos):
				return IDs
		return []

	def getRangeFromID(self,ID):
		startPos=None
		endPos=None
		for key in filter(lambda x: ID in x,self._IDsCollection):
			r=self._IDsCollection[key]
			if (startPos is None) or (r[0]<startPos):
				startPos=r[0]
			if (endPos is None) or (r[1]>endPos):
				endPos=r[1]
		if (startPos is not None) and (endPos is not None):
			return (startPos,endPos)
		else:
			return None

	def getIDsFromID(self,ID):
		for key in self._IDsCollection:
			if ID in key:
 				index=list(key).index(ID)
				return key[0:index+1]


	def appendText(self,IDs,text):
		if self.getIDsFromPosition(len(self._text)-1)==IDs:
			(startPos,endPos)=self._IDsCollection[IDs]
			self._text=self._text[0:-1]+" "+text+"\n"
			self._IDsCollection[IDs]=(startPos,len(self._text))
		else:
			startPos=len(self._text)
			self._text+=text+"\n"
			endPos=len(self._text)
			self._IDsCollection[IDs]=(startPos,endPos)

	def insertText(self,pos,IDs,text):
		startPos=pos
		endPos=startPos+len(text)
		self._text="%s%s\n%s"%(self._text[0:startPos],text,self._text[startPos:])
		for i in self._IDsCollection:
			if self._IDsCollection[i][0]>=startPos:
				self._IDsCollection[i]=(self._IDsCollection[i][0]+(endPos-startPos)+1,self._IDsCollection[i][1]+(endPos-startPos)+1)
		self._IDsCollection[IDs]=(startPos,endPos+1)

	def removeText(self,ID):
		r=self.getRangeFromID(ID)
		if not r:
			return
		self._text=self._text[0:r[0]]+self._text[r[1]:]
		for key in filter(lambda x: ID in x,self._IDsCollection):
			del self._IDsCollection[key]
			for i in self._IDsCollection:
				if self._IDsCollection[i][0]>=r[1]:
					self._IDsCollection[i]=(self._IDsCollection[i][0]-(r[1]-r[0]),self._IDsCollection[i][1]-(r[1]-r[0]))

	def resetBuffer(self):
		self._text=""
		self._IDsCollection={}
		self.caretPosition=0
		self._lastCaretIDs=[]

	def getIDEnterMessage(self,ID):
		return ""

	def getIDExitMessage(self,ID):
		return ""


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

	def _get_text(self):
		return self._text

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
			if text and (text not in ['\n','\r',""]):
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
		self.speakLine(self.caretPosition)

	def script_bottom(self,keyPress):
		self.caretPosition=len(self.text)-1
		self.reportCaretIDMessages()
		self.speakLine(self.caretPosition)

	def script_nextLine(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextLine(pos)
		if (pos<len(self.text)) and (nextPos is not None):
			self.caretPosition=nextPos
		self.reportCaretIDMessages()
		self.speakLine(self.caretPosition)

	def script_previousLine(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousLine(pos)
		if (pos>0) and (prevPos is not None):
			self.caretPosition=prevPos
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

