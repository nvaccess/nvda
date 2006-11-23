from keyboardHandler import key
import audio

class virtualBuffer(object):

	def __init__(self,NVDAObject):
		self._keyMap={}
		self.NVDAObject=NVDAObject
		self.text=""
		self.caretPosition=0
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
		})

	def getScript(self,keyPress):
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def registerScriptKey(self,keyPress,methodName):
		self._keyMap[keyPress]=methodName

	def registerScriptKeys(self,keyDict):
		self._keyMap.update(keyDict)

	def getStartPosition(self):
		return 0
	startPosition=property(fget=getStartPosition)

	def getEndPosition(self):
		return len(self.text)
	endPosition=property(fget=getEndPosition)

	def getLineCount(self):
		return -1
	lineCount=property(fget=getLineCount)

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
		if pos<self.getEndPosition():
			return pos+1
		else:
			return None

	def previousCharacter(self,pos):
		if pos>self.getStartPosition():
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
		if newPos<self.getEndPosition():
			return newPos
		else:
			return None

	def previousLine(self,pos):
		lineStart=self.getLineStart(pos)
		pos=lineStart-1
		lineStart=self.getLineStart(pos)
		if lineStart>=self.getStartPosition():
			return lineStart
		else:
			return None

	def script_top(self,keyPress):
		self.caretPosition=0
		audio.speakText(self.getLine(self.caretPosition))

	def script_bottom(self,keyPress):
		self.caretPosition=len(self.text)-1
		audio.speakText(self.getLine(self.caretPosition))

	def script_nextLine(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextLine(pos)
		if (pos<len(self.text)) and (nextPos is not None):
			self.caretPosition=nextPos
		audio.speakText(self.getLine(self.caretPosition))

	def script_previousLine(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousLine(pos)
		if (pos>0) and (prevPos is not None):
			self.caretPosition=prevPos
		audio.speakText(self.getLine(self.caretPosition))

	def script_startOfLine(self,keyPress):
		self.caretPosition=self.getLineStart(self.caretPosition)
		audio.speakText(self.getCharacter(self.caretPosition))

	def script_endOfLine(self,keyPress):
		self.caretPosition=(self.getLineStart(self.caretPosition)+self.getLineLength(self.caretPosition)-1)
		audio.speakText(self.getCharacter(self.caretPosition))

	def script_nextWord(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextWord(pos)
		if (pos<len(self.text)) and (nextPos is not None):
			self.caretPosition=(nextPos)
		audio.speakText(self.getWord(self.caretPosition))

	def script_previousWord(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousWord(pos)
		if (prevPos is not None) and (prevPos>=0):
			self.caretPosition=(prevPos)
		audio.speakText(self.getWord(self.caretPosition))

	def script_nextCharacter(self,keyPress):
		pos=self.caretPosition
		nextPos=self.nextCharacter(pos)
		if (nextPos<len(self.text)) and (nextPos is not None):
			self.caretPosition=(nextPos)
		audio.speakText(self.getCharacter(self.caretPosition))

	def script_previousCharacter(self,keyPress):
		pos=self.caretPosition
		prevPos=self.previousCharacter(pos)
		if (prevPos<len(self.text)) and (prevPos is not None):
			self.caretPosition=prevPos
		audio.speakText(self.getCharacter(self.caretPosition))

