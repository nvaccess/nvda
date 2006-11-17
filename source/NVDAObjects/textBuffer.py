import winsound
from config import conf
import core
from keyboardHandler import key, sendKey
import audio
import debug
import lang
import globalVars

class NVDAObject_textBuffer:

	def __init__(self,*args):
		self._reviewCursor=0
		self._presentationTable=[]
		pass

	def getTextRange(self,start,end):
		text=self.text
		if (start>=end) or (end>len(text)):
			return None
		return text[start:end]

	def getStartPosition(self):
		return 0
	startPosition=property(fget=getStartPosition)

	def getEndPosition(self):
		return len(self.text)-1
	endPosition=property(fget=getEndPosition)

	def getVisibleRange(self):
		return (self.startPosition,self.endPosition)
	visibleRange=property(fget=getVisibleRange)

	def getPositionFromScreenCoords(self,x,y):
		return 0

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

	def getCharacter(self,pos):
		if pos is not None:
			return self.getTextRange(pos,pos+1)

	def getLineStart(self,pos):
		startPos=pos
		if startPos>0 and (self.getCharacter(startPos)=='\n'):
			startPos=startPos-1
		while (startPos>-1) and (self.getCharacter(startPos)!='\n'):
			startPos-=1
		return startPos+1

	def getLineLength(self,pos):
		startPos=self.getLineStart(pos)
		endPos=startPos
		text=self.text
		while (endPos<=len(text)) and (self.getCharacter(endPos)!='\n'):
			endPos+=1
		return (endPos-startPos)

	def getLineEnd(self,pos):
		return self.getLineStart(pos)+self.getLineLength(pos)

	def nextLine(self,pos):
		lineLength=self.getLineLength(pos)
		lineStart=self.getLineStart(pos)
		lineEnd=lineStart+lineLength
		newPos=lineEnd
		if newPos<self.endPosition:
			return newPos
		else:
			return None

	def previousLine(self,pos):
		lineStart=self.getLineStart(pos)
		pos=lineStart-1
		if pos<0:
			return None
		lineStart=self.getLineStart(pos)
		if (lineStart>=self.startPosition) and (lineStart<pos):
			return lineStart
		else:
			return None

	def getLineNumber(self,pos):
		return -1

	def getLine(self,pos):
		startPos=self.getLineStart(pos)
		endPos=self.getLineEnd(pos)
		return self.getTextRange(startPos,endPos)

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

	def getWord(self,pos):
		wordStart=self.wordStart(pos)
		wordEnd=self.wordEnd(pos)
		return self.getTextRange(wordStart,wordEnd)

	def reportReviewPresentation(self):
		#The old values are at index 2
		pos=self._reviewCursor
		for ruleNum in range(len(self._presentationTable)):
			messageFunc=self._presentationTable[ruleNum][0]
			reportWhen=conf
			for item in self._presentationTable[ruleNum][1]:
				reportWhen=reportWhen.get(item,{})
			if reportWhen=="always":
				message=messageFunc(pos)
				if message is not None:
					audio.speakMessage(messageFunc(pos))
			elif reportWhen=="changes":
				message=messageFunc(pos)
				if (message is not None) and (message!=self._presentationTable[ruleNum][2]):
					audio.speakMessage(message)
				self._presentationTable[ruleNum][2]=message

	def review_top(self):
		"""Move the review cursor to the top and read the line"""
		self._reviewCursor=self.visibleRange[0]
		self.reportReviewPresentation()
		line=self.getLine(self._reviewCursor)
		audio.speakText(line)

	def review_bottom(self):
		"""Move the review cursor to the bottom and read the line"""
		self._reviewCursor=self.visibleRange[1]-1
		self.reportReviewPresentation()
		line=self.getLine(self._reviewCursor)
		audio.speakText(line)

	def review_currentLine(self):
		"""Reads the line at the review cursor position""" 
		self.reportReviewPresentation()
		line=self.getLine(self._reviewCursor)
		audio.speakText(line)

	def review_nextLine(self):
		"""Moves the review cursor to the next line and reads it"""
		pos=self._reviewCursor
		nextPos=self.nextLine(pos)
		if (pos<self.visibleRange[1]) and (nextPos is not None):
			self._reviewCursor=nextPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage(lang.messages["bottom"])
		audio.speakText(self.getLine(self._reviewCursor))

	def review_previousLine(self):
		"""Moves the review cursor to the previous line and reads it"""
		pos=self._reviewCursor
		prevPos=self.previousLine(pos)
		if (pos>self.visibleRange[0]) and (prevPos is not None):
			self._reviewCursor=prevPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage(lang.messages["top"])
		audio.speakText(self.getLine(self._reviewCursor))

	def review_startOfLine(self):
		"""Move review cursor to start of line and read the current character"""
		self._reviewCursor=self.getLineStart(self._reviewCursor)
		self.reportReviewPresentation()
		character=self.getCharacter(self._reviewCursor)
		audio.speakText(character)

	def review_endOfLine(self):
		"""Move review cursor to start of line and read the current character"""
		self._reviewCursor=self.getLineStart(self._reviewCursor)+self.getLineLength(self._reviewCursor)-1
		self.reportReviewPresentation()
		character=self.getCharacter(self._reviewCursor)
		audio.speakText(character)

	def review_currentWord(self):
		"""Reads the word at the review cursor position"""
		self.reportReviewPresentation()
		word=self.getWord(self._reviewCursor)
		audio.speakText(word)

	def review_nextWord(self):
		"""Moves the review cursor to the next word and reads it"""
		pos=self._reviewCursor
		nextPos=self.nextWord(pos)
		if (pos<self.visibleRange[1]) and (nextPos is not None):
			self._reviewCursor=nextPos
			self.reportReviewPresentation()
			if self.getLineNumber(nextPos)!=self.getLineNumber(pos):
				winsound.Beep(440,20)
		else:
			audio.speakMessage(lang.messages["bottom"])
		audio.speakText(self.getWord(self._reviewCursor))

	def review_previousWord(self):
		"""Moves the review cursor to the previous word and reads it"""
		pos=self._reviewCursor
		prevPos=self.previousWord(pos)
		if (prevPos is not None) and (prevPos>=self.visibleRange[0]):
			self._reviewCursor=prevPos
			self.reportReviewPresentation()
			if self.getLineNumber(prevPos)!=self.getLineNumber(pos):
				winsound.Beep(440,20)
		else:
			audio.speakMessage(lang.messages["top"])
		audio.speakText(self.getWord(self._reviewCursor))

	def review_currentCharacter(self):
		"""Reads the character at the review cursor position"""
		self.reportReviewPresentation()
		character=self.getCharacter(self._reviewCursor)
		audio.speakText(character)

	def review_nextCharacter(self):
		"""Moves the review cursor to the next character and reads it"""
		pos=self._reviewCursor
		nextPos=self.nextCharacter(pos)
		lineStart=self.getLineStart(pos)
		lineEnd=lineStart+self.getLineLength(pos)
		if (nextPos<=lineEnd) and (nextPos is not None): 
			self._reviewCursor=nextPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage(lang.messages["right"])
		audio.speakText(self.getCharacter(self._reviewCursor))

	def review_previousCharacter(self):
		"""Moves the review cursor to the previous character and reads it"""
		pos=self._reviewCursor
		prevPos=self.previousCharacter(pos)
		lineStart=self.getLineStart(pos)
		if (prevPos>=lineStart) and (prevPos is not None):
			self._reviewCursor=prevPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage(lang.messages["left"])
		audio.speakText(self.getCharacter(self._reviewCursor))

class NVDAObject_editableTextBuffer(NVDAObject_textBuffer):

	def __init__(self,*args):
		NVDAObject_textBuffer.__init__(self)
		self._reviewCursor=self.caretPosition
		self.registerScriptKeys({
			key("insert+extendedDown"):self.script_sayAll,
			key("ExtendedUp"):self.script_moveByLine,
			key("ExtendedDown"):self.script_moveByLine,
			key("ExtendedLeft"):self.script_moveByCharacter,
			key("ExtendedRight"):self.script_moveByCharacter,
			key("Control+ExtendedLeft"):self.script_moveByWord,
			key("Control+ExtendedRight"):self.script_moveByWord,
			key("Shift+ExtendedRight"):self.script_changeSelection,
			key("Shift+ExtendedLeft"):self.script_changeSelection,
			key("Shift+ExtendedHome"):self.script_changeSelection,
			key("Shift+ExtendedEnd"):self.script_changeSelection,
			key("Shift+ExtendedUp"):self.script_changeSelection,
			key("Shift+ExtendedDown"):self.script_changeSelection,
			key("Control+Shift+ExtendedLeft"):self.script_changeSelection,
			key("Control+Shift+ExtendedRight"):self.script_changeSelection,
			key("ExtendedHome"):self.script_moveByCharacter,
			key("ExtendedEnd"):self.script_moveByCharacter,
			key("control+extendedHome"):self.script_moveByLine,
			key("control+extendedEnd"):self.script_moveByLine,
			key("control+shift+extendedHome"):self.script_changeSelection,
			key("control+shift+extendedEnd"):self.script_changeSelection,
			key("ExtendedDelete"):self.script_delete,
			key("Back"):self.script_backspace,
			key("insert+f"):self.script_formatInfo,
		})

	def getCaretRange(self):
		return None
	caretRange=property(fget=getCaretRange)

	def getCaretPosition(self):
		return self.startPosition

	def setCaretPosition(self,pos):
		pass

	caretPosition=property(fget=getCaretPosition,fset=setCaretPosition)

	def getCurrentCharacter(self):
		return self.getCharacter(self.caretPosition)

	def getCurrentWord(self):
		return self.getWord(self.caretPosition)

	def getCurrentLine(self):
		return self.getLine(self.caretPosition)

	def reportPresentation(self):
		#The old values are at index 3
		pos=self.caretPosition
		for ruleNum in range(len(self._presentationTable)):
			messageFunc=self._presentationTable[ruleNum][0]
			reportWhen=conf
			for item in self._presentationTable[ruleNum][1]:
				reportWhen=reportWhen.get(item,{})
			if reportWhen=="always":
				message=messageFunc(pos)
				if message is not None:
					audio.speakMessage(messageFunc(pos))
			elif reportWhen=="changes":
				message=messageFunc(pos)
				if (message is not None) and (message!=self._presentationTable[ruleNum][3]):
					audio.speakMessage(message)
				self._presentationTable[ruleNum][3]=message

	def event_caret(self):
		self._reviewCursor=self.caretPosition

	def sayAllGenerator(self):
		#Setup the initial info (count, caret position, index etc)
		count=0 #Used to see when we need to start yielding
		startPos=endPos=curPos=self.caretPosition
		index=lastIndex=None
		lastKeyCount=globalVars.keyCounter
		#A loop that runs while no key is pressed and while we are not at the end of the text
		while (curPos is not None) and (curPos<self.endPosition):
			#Speak the current line (if its not blank) with an speech index of its position
			text=self.getLine(curPos)
			if text and (text not in ['\n','\r',""]):
				audio.speakText(text,index=curPos)
			#Move our current position down by one line
				endPos=curPos
			curPos=self.nextLine(curPos)
			#Grab the current speech index from the synth, and if different to last, move the caret there
			index=audio.getLastIndex()
			if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
		 		self.setCaretPosition(index)
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
			 		self.setCaretPosition(index)
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
			 		self.setCaretPosition(index)
			audio.cancel()

	def script_sayAll(self,keyPress):
		core.newThread(self.sayAllGenerator())


	def script_moveByLine(self,keyPress):
		"""Moves and then reads the current line"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakText(self.getCurrentLine())

	def script_moveByCharacter(self,keyPress):
		"""Moves and reads the current character"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakSymbol(self.getCurrentCharacter())
		self._reviewCursor=self.caretPosition

	def script_moveByWord(self,keyPress):
		"""Moves and reads the current word"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakText(self.getCurrentWord())
		self._reviewCursor=self.caretPosition

	def script_changeSelection(self,keyPress):
		"""Moves and reads the current selection"""
		selectionPoints=self.getCaretRange()
		sendKey(keyPress)
		newSelectionPoints=self.getCaretRange()
		if newSelectionPoints and not selectionPoints:
			audio.speakText("selected %s"%self.getTextRange(newSelectionPoints[0],newSelectionPoints[1]))
		elif not newSelectionPoints:
			audio.speakSymbol(self.getCharacter(self.caretPosition))
		elif selectionPoints and newSelectionPoints: 
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%self.getTextRange(selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%self.getTextRange(selectionPoints[0],newSelectionPoints[0]))
			elif newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%self.getTextRange(newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%self.getTextRange(newSelectionPoints[0],selectionPoints[0]))
		self._reviewCursor=self.caretPosition

	def script_delete(self,keyPress):
		"""Deletes the character and reads the new current character"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakSymbol(self.getCurrentCharacter())
		self._reviewCursor=self.caretPosition

	def script_backspace(self,keyPress):
		"""Reads the character before the current character and then deletes it"""
		point=self.caretPosition
		if not point==self.startPosition:
			delChar=self.getCharacter(self.previousCharacter(point))
			sendKey(keyPress)
			newPoint=self.caretPosition
			if newPoint<point:
				audio.speakSymbol(delChar)
		else:
			sendKey(keyPress)
		self._reviewCursor=self.caretPosition

	def script_formatInfo(self,keyPress):
		"""Reports the current formatting information"""
		pos=self.caretPosition
		for rule in self._presentationTable:
			message=rule[0](pos)
			if message is not None:
				audio.speakMessage(message)


