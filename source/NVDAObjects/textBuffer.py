import winsound
from config import conf
import autoPropertyType
import core
from keyboardHandler import key, sendKey
import audio
import debug
import globalVars

class NVDAObject_textBuffer:

	__metaclass__=autoPropertyType.autoPropertyType

	def __init__(self,*args):
		self.reviewPosition=0
		self._presentationTable={}
		self._lastReviewPresentationValues={}

	def registerPresentationAttribute(self,name,func,config):
		self._presentationTable[name]=(func,config)

	def getPresentationValues(self,pos):
		values={}
		for name in self._presentationTable:
			if self._presentationTable[name][1]():   
				values[name]=self._presentationTable[name][0](pos)
		return values

	def getChangedPresentationValues(self,newValues,oldValues):
		changedValues={}
		for name in newValues.keys():
			if (oldValues.has_key(name) and (newValues[name]!=oldValues[name])) or not oldValues.has_key(name):
				changedValues[name]=newValues[name]
		return changedValues

	def speakPresentationValues(self,values):
		for name in values.keys():
			if values[name] is not None:
				audio.speakMessage("%s"%values[name])

	def getTextRange(self,start,end):
		text=self.text
		if (start>=end) or (end>len(text)):
			return None
		return text[start:end]

	def _get_startPosition(self):
		return 0

	def _get_endPosition(self):
		return len(self.text)-1

	def _get_visibleRange(self):
		return (self.startPosition,self.endPosition)

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
		text=self.text
		if startPos>0 and startPos<len(text) and (text[startPos]=='\n'):
			startPos=startPos-1
		while (startPos>-1) and (startPos<len(text)) and (text[startPos] not in ['\r','\n']):
			startPos-=1
		return startPos+1

	def getLineLength(self,pos):
		startPos=self.getLineStart(pos)
		endPos=startPos
		text=self.text
		while (endPos<len(text)) and (text[endPos] not in ['\n','\r']):
			endPos+=1
		if (endPos<len(text)-1) and (text[endPos]=='\r') and (endPos+1<=len(text)) and (text[endPos+1]=='\n'): 
			endPos+=1
		return (endPos-startPos)

	def getLineEnd(self,pos):
		return self.getLineStart(pos)+self.getLineLength(pos)

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
		if (pos<=endPos) and (pos>=startPos):
			return self.getTextRange(startPos,endPos)
		else:
			return None

	def inWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.getCharacter(pos) not in whitespace:
			return True
		else:
			return False

	def getWordStart(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		text=self.text
		if self.inWord(pos):
			while (pos is not None) and (text[pos] not in whitespace):
				oldPos=pos
				pos=self.previousCharacter(pos)
			if pos is None:
				pos=oldPos
			else:
				pos=self.nextCharacter(pos)
		return pos

	def getWordEnd(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		text=self.text
		while (pos is not None) and (text[pos] not in whitespace):
			oldPos=pos
			pos=self.nextCharacter(pos)
		if pos is not None:
			return pos
		else:
			return oldPos

	def nextWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			pos=self.getWordEnd(pos)
		while (pos is not None) and (self.getCharacter(pos) in whitespace):
			pos=self.nextCharacter(pos)
		return pos

	def previousWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			pos=self.getWordStart(pos)
			pos=self.previousCharacter(pos)
		while (pos is not None) and (self.getCharacter(pos) in whitespace):
			pos=self.previousCharacter(pos)
		if pos:
			pos=self.getWordStart(pos)
		return pos

	def getWord(self,pos):
		wordStart=self.getWordStart(pos)
		wordEnd=self.getWordEnd(pos)
		return self.getTextRange(wordStart,wordEnd)

	def speakCharacter(self,pos):
		audio.speakSymbol(self.getCharacter(pos))

	def speakWord(self,pos):
		audio.speakText(self.getWord(pos),index=pos)

	def speakLine(self,pos):
		audio.speakText(self.getLine(pos),index=pos)

	def review_top(self):
		"""Move the review cursor to the top and read the line"""
		self.reviewPosition=self.visibleRange[0]
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakLine(self.reviewPosition)

	def review_bottom(self):
		"""Move the review cursor to the bottom and read the line"""
		self.reviewPosition=self.visibleRange[1]-1
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakLine(self.reviewPosition)

	def review_currentLine(self):
		"""Reads the line at the review cursor position""" 
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakLine(self.reviewPosition)

	def review_nextLine(self):
		"""Moves the review cursor to the next line and reads it"""
		pos=self.reviewPosition
		nextPos=self.nextLine(pos)
		if (pos<self.visibleRange[1]) and (nextPos is not None):
			self.reviewPosition=nextPos
		else:
			audio.speakMessage(_("bottom"))
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakLine(self.reviewPosition)

	def review_previousLine(self):
		"""Moves the review cursor to the previous line and reads it"""
		pos=self.reviewPosition
		prevPos=self.previousLine(pos)
		if (pos>self.visibleRange[0]) and (prevPos is not None):
			self.reviewPosition=prevPos
		else:
			audio.speakMessage(_("top"))
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakLine(self.reviewPosition)

	def review_startOfLine(self):
		"""Move review cursor to start of line and read the current character"""
		self.reviewPosition=self.getLineStart(self.reviewPosition)
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakCharacter(self.reviewPosition)

	def review_endOfLine(self):
		"""Move review cursor to start of line and read the current character"""
		self.reviewPosition=self.getLineEnd(self.reviewPosition)
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakCharacter(self.reviewPosition)

	def review_currentWord(self):
		"""Reads the word at the review cursor position"""
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakWord(self.reviewPosition)

	def review_nextWord(self):
		"""Moves the review cursor to the next word and reads it"""
		pos=self.reviewPosition
		nextPos=self.nextWord(pos)
		if (pos<self.visibleRange[1]) and (nextPos is not None):
			self.reviewPosition=nextPos
			if self.getLineNumber(nextPos)!=self.getLineNumber(pos):
				winsound.Beep(440,20)
		else:
			audio.speakMessage(_("bottom"))
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakWord(self.reviewPosition)

	def review_previousWord(self):
		"""Moves the review cursor to the previous word and reads it"""
		pos=self.reviewPosition
		prevPos=self.previousWord(pos)
		if (prevPos is not None) and (prevPos>=self.visibleRange[0]):
			self.reviewPosition=prevPos
			if self.getLineNumber(prevPos)!=self.getLineNumber(pos):
				winsound.Beep(440,20)
		else:
			audio.speakMessage(_("top"))
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakWord(self.reviewPosition)

	def review_currentCharacter(self):
		"""Reads the character at the review cursor position"""
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakCharacter(self.reviewPosition)

	def review_nextCharacter(self):
		"""Moves the review cursor to the next character and reads it"""
		pos=self.reviewPosition
		nextPos=self.nextCharacter(pos)
		lineStart=self.getLineStart(pos)
		lineEnd=self.getLineEnd(pos)
		if (nextPos<lineEnd) and (nextPos is not None): 
			self.reviewPosition=nextPos
		else:
			audio.speakMessage(_("right"))
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakCharacter(self.reviewPosition)

	def review_previousCharacter(self):
		"""Moves the review cursor to the previous character and reads it"""
		pos=self.reviewPosition
		prevPos=self.previousCharacter(pos)
		lineStart=self.getLineStart(pos)
		if (prevPos>=lineStart) and (prevPos is not None):
			self.reviewPosition=prevPos
		else:
			audio.speakMessage(_("left"))
		reviewPresentationValues=self.getPresentationValues(self.reviewPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(reviewPresentationValues,self._lastReviewPresentationValues))
		self._lastReviewPresentationValues=reviewPresentationValues
		self.speakCharacter(self.reviewPosition)

class NVDAObject_editableTextBuffer(NVDAObject_textBuffer):

	def __init__(self,*args):
		NVDAObject_textBuffer.__init__(self,*args)
		self._lastCaretPresentationValues={}
		self.reviewPosition=self.caretPosition
		self.registerScriptKeys({
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
		})

	def _get_caretRange(self):
		return None

	def _get_caretPosition(self):
		return self.startPosition

	def _set_caretPosition(self,pos):
		pass

	def _get_currentCharacter(self):
		return self.getCharacter(self.caretPosition)

	def _get_currentWord(self):
		return self.getWord(self.caretPosition)

	def _get_currentLine(self):
		return self.getLine(self.caretPosition)

	def event_caret(self):
		self.reviewPosition=self.caretPosition

	def sayAllGenerator(self):
		#Setup the initial info (count, caret position, index etc)
		count=0 #Used to see when we need to start yielding
		startPos=endPos=curPos=self.caretPosition
		lastPresentationValues=self.getPresentationValues(curPos)
		index=lastIndex=None
		lastKeyCount=globalVars.keyCounter
		#A loop that runs while no key is pressed and while we are not at the end of the text
		while (curPos is not None) and (curPos<self.endPosition):
			#report any changed presentation values
			curPresentationValues=self.getPresentationValues(curPos)
			self.speakPresentationValues(self.getChangedPresentationValues(curPresentationValues,lastPresentationValues))
			lastPresentationValues=curPresentationValues
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

	def script_moveByLine(self,keyPress):
		"""Moves and then reads the current line"""
		sendKey(keyPress)
		caretPresentationValues=self.getPresentationValues(self.caretPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(caretPresentationValues,self._lastCaretPresentationValues))
		self._lastCaretPresentationValues=caretPresentationValues
		self.speakLine(self.caretPosition)
		self.reviewPosition=self.caretPosition

	def script_moveByCharacter(self,keyPress):
		"""Moves and reads the current character"""
		sendKey(keyPress)
		caretPresentationValues=self.getPresentationValues(self.caretPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(caretPresentationValues,self._lastCaretPresentationValues))
		self._lastCaretPresentationValues=caretPresentationValues
		self.speakCharacter(self.caretPosition)
		self.reviewPosition=self.caretPosition

	def script_moveByWord(self,keyPress):
		"""Moves and reads the current word"""
		sendKey(keyPress)
		caretPresentationValues=self.getPresentationValues(self.caretPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(caretPresentationValues,self._lastCaretPresentationValues))
		self._lastCaretPresentationValues=caretPresentationValues
		self.speakWord(self.caretPosition)
		self.reviewPosition=self.caretPosition

	def script_changeSelection(self,keyPress):
		"""Moves and reads the current selection"""
		selectionPoints=self.caretRange
		sendKey(keyPress)
		newSelectionPoints=self.caretRange
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
		self.reviewPosition=self.caretPosition

	def script_delete(self,keyPress):
		"""Deletes the character and reads the new current character"""
		sendKey(keyPress)
		caretPresentationValues=self.getPresentationValues(self.caretPosition)
		self.speakPresentationValues(self.getChangedPresentationValues(caretPresentationValues,self._lastCaretPresentationValues))
		self._lastCaretPresentationValues=caretPresentationValues
		self.speakCharacter(self.caretPosition)
		self.reviewPosition=self.caretPosition

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
		self.reviewPosition=self.caretPosition

	def reportFormatInfo(self):
		"""Reports the current formatting information"""
		pos=self.caretPosition
		if len(self._presentationTable)>0:
			for name in self._presentationTable.keys():
				message=self._presentationTable[name][0](pos)
				if message is not None:
					audio.speakMessage(message)
		else:
			audio.speakText(_("No format types to report"))
