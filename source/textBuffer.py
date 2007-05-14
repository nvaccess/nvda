import globalVars
import baseObject
import config
import speech
import debug
from keyUtils import sendKey, key, isKeyWaiting
import api

class textBufferObject(baseObject.scriptableObject):

	def __init__(self):
		self._reviewOffset=0
		self._text_lastReportedPresentation={}
		self.text_reviewOffset=0

	def _get_text_characterCount(self):
		return len(self.text_getText())

	def text_getText(self,start=None,end=None):
		"""Gets either all the text the object has, or the text from a certain offset, or to a certain offset.
@param start: the start offset
@type start: int
@param end: the end offset
@type end: int
@returns: the text
@rtype: string
"""
		return ""

	def _get_text_caretOffset(self):
		return 0

	def _set_text_caretOffset(self,offset):
		pass

	def _get_text_reviewOffset(self):
		return self._reviewOffset

	def _set_text_reviewOffset(self,offset):
		self._reviewOffset=offset

	def _get_text_selectionCount(self):
		return 0

	def text_getSelectionOffsets(self,index):
		"""Gets (start,end) tuple of the chosen selection.
@param index: The number of the selection you want
@type index: int
@returns: the start and end offsets of the selection or None if bad selection number
@rtype: 2-tuple
"""
		return None

	def _get_text_lineCount(self):
		return None

	def text_getLineOffsets(self,offset):
		"""Gets the start and end offsets for the line at given offset.
@param offset: the ofset where the line is located
@type offset: int
@returns: start and end offsets
@rtype: 2-tuple
"""
		text=self.text_getText()
		start=offset
		while (text is not None) and (len(text)>=start) and (start>0) and not (text[start-1] in ['\r','\n']):
  			start-=1
		end=offset+1
		while (end<self.text_characterCount) and (text[end] not in ['\r','\n']):
			end+=1
		if (end<len(text)-1) and (text[end]=='\r') and (text[end+1]=='\n'):
			end+=2
		elif (end<len(text)) and (text[end] in ['\r','\n']):
			end+=1
		return (start,end)

	def text_getNextLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		if end<self.text_characterCount:
			return self.text_getLineOffsets(end)
		else:
			return None

	def text_getPrevLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		if start>0:
			return self.text_getLineOffsets(start-1)
		else:
			return None

	def text_getWordOffsets(self,offset):
		"""Gets the start and end offsets for the word at given offset.
@param offset: the ofset where the word is located
@type offset: int
@returns: start and end offsets
@rtype: 2-tuple
"""
		(lineStart,lineEnd)=self.text_getLineOffsets(offset)
		start=offset
		while (start>lineStart) and not self.text_getText(start=start,end=start+1).isspace() and not self.text_getText(start=start-1,end=start).isspace():
			start-=1
 		end=offset+1
		while (end<lineEnd) and not self.text_getText(start=end,end=end+1).isspace():
			end+=1
		return (start,end)

	def text_getNextWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		while end<self.text_characterCount:
			if not self.text_getText(start=end,end=end+1).isspace():
				return self.text_getWordOffsets(end)
			end+=1
		return None

	def text_getPrevWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		start-=1
		while start>=0:
			if not self.text_getText(start=start,end=start+1).isspace():
				return self.text_getWordOffsets(start)
			start-=1
		return None

	def text_getSentenceOffsets(self,offset):
		return self.text_getLineOffsets(offset)

	def text_getNextSentenceOffsets(self,offset):
		return self.text_getNextLineOffsets(offset)

	def text_getPrevSentenceOffsets(self,offset):
		return self.text_getPrevLineOffsets(offset)

	def text_getParagraphOffsets(self,offset):
		return self.text_getLineOffsets(offset)

	def text_getNextParagraphOffsets(self,offset):
		return self.text_getNextLineOffsets(offset)

	def text_getPrevParagraphOffsets(self,offset):
		return self.text_getPrevLineOffsets(offset)

	def text_getPageNumber(self,offset):
		return None

	def text_getLineNumber(self,offset):
		return None

	def text_getStyle(self,offset):
		return None

	def text_getAlignment(self,offset):
		return None

	def text_getFontName(self,offset):
		return None

	def text_getFontSize(self,offset):
		return None

	def text_isBold(self,offset):
		return False

	def text_isItalic(self,offset):
		return False

	def text_isUnderline(self,offset):
		return None

	def text_isSubscript(self,offset):
		return False

	def text_isSuperscript(self,offset):
		return False

	def text_getTableRowNumber(self,offset):
		return None

	def text_getTableColumnNumber(self,offset):
		return None

	def text_getTableCellOffsets(self,row,column):
		return None

	def text_getTableRowCount(self,offset):
		return None

	def text_getTableColumnCount(self,offset):
		return None

	def text_inTable(self,offset):
		return None

	def text_getFieldOffsets(self,offset):
		return self.text_getLineOffsets(offset)

	def text_getNextFieldOffsets(self,offset):
		return self.text_getNextLineOffsets(offset)

	def text_getPrevFieldOffsets(self,offset):
		return self.text_getPrevLineOffsets(offset)

	def text_reportNewPresentation(self,offset):
		if config.conf["documentFormatting"]["reportPage"]:
			pageNumber=self.text_getPageNumber(offset)
			lastPageNumber=self._text_lastReportedPresentation.get('pageNumber',None)
			if isinstance(pageNumber,int) and pageNumber!=lastPageNumber:
				speech.speakMessage(_("page %d")%pageNumber)
			self._text_lastReportedPresentation["pageNumber"]=pageNumber
		if config.conf["documentFormatting"]["reportLineNumber"]:
			lineNumber=self.text_getLineNumber(offset)
			lastLineNumber=self._text_lastReportedPresentation.get('lineNumber',None)
			if isinstance(lineNumber,int) and lineNumber!=lastLineNumber:
				speech.speakMessage(_("line %d")%lineNumber)
			self._text_lastReportedPresentation["lineNumber"]=lineNumber
		if config.conf["documentFormatting"]["reportTables"]:
			inTable=self.text_inTable(offset)
			wasInTable=self._text_lastReportedPresentation.get('inTable',None)
			if not inTable and wasInTable:
				speech.speakMessage(_("out of table"))
				self._text_lastReportedPresentation['tableRowNumber']=None
				self._text_lastReportedPresentation['tableColumnNumber']=None
			elif inTable and not wasInTable:
				rowCount=self.text_getTableRowCount(offset)
				columnCount=self.text_getTableColumnCount(offset)
				speech.speakMessage(_("table with %d columns and %d rows")%(columnCount,rowCount))
			self._text_lastReportedPresentation["inTable"]=inTable
			if inTable:
				rowNumber=self.text_getTableRowNumber(offset)
				lastRowNumber=self._text_lastReportedPresentation.get('tableRowNumber',None)
				if isinstance(rowNumber,int) and rowNumber!=lastRowNumber:
					speech.speakMessage(_("row %d")%rowNumber)
				self._text_lastReportedPresentation["tableRowNumber"]=rowNumber
				columnNumber=self.text_getTableColumnNumber(offset)
				lastColumnNumber=self._text_lastReportedPresentation.get('tableColumnNumber',None)
				if isinstance(columnNumber,int) and columnNumber!=lastColumnNumber:
					speech.speakMessage(_("column %d")%columnNumber)
				self._text_lastReportedPresentation["tableColumnNumber"]=columnNumber
		if config.conf["documentFormatting"]["reportStyle"]:
			style=self.text_getStyle(offset)
			lastStyle=self._text_lastReportedPresentation.get('style',None)
			if isinstance(style,basestring) and style!=lastStyle:
				speech.speakMessage(_("style %s")%style)
			self._text_lastReportedPresentation["style"]=style
		if config.conf["documentFormatting"]["reportAlignment"]:
			alignment=self.text_getAlignment(offset)
			lastAlignment=self._text_lastReportedPresentation.get('alignment',None)
			if isinstance(alignment,basestring) and alignment!=lastAlignment:
				speech.speakMessage(_("alignment %s")%alignment)
			self._text_lastReportedPresentation["alignment"]=alignment
		if config.conf["documentFormatting"]["reportFontName"]:
			fontName=self.text_getFontName(offset)
			lastFontName=self._text_lastReportedPresentation.get('fontName',None)
			if isinstance(fontName,basestring) and fontName!=lastFontName:
				speech.speakMessage(_("font name %s")%fontName)
			self._text_lastReportedPresentation["fontName"]=fontName
		if config.conf["documentFormatting"]["reportFontSize"]:
			fontSize=self.text_getFontSize(offset)
			lastFontSize=self._text_lastReportedPresentation.get('fontSize',None)
			if isinstance(fontSize,int) and fontSize!=lastFontSize:
				speech.speakMessage(_("font size %d")%fontSize)
			self._text_lastReportedPresentation["fontSize"]=fontSize
		if config.conf["documentFormatting"]["reportFontAttributes"]:
			isBold=self.text_isBold(offset)
			wasBold=self._text_lastReportedPresentation.get('isBold',None)
			if isinstance(isBold,bool) and isBold and not wasBold:
				speech.speakMessage(_("bold"))
			elif isinstance(isBold,bool) and not isBold and wasBold:
				speech.speakMessage(_("not bold"))
			self._text_lastReportedPresentation["isBold"]=isBold
			isItalic=self.text_isItalic(offset)
			wasItalic=self._text_lastReportedPresentation.get('isItalic',None)
			if isinstance(isItalic,bool) and isItalic and not wasItalic:
				speech.speakMessage(_("italic"))
			elif isinstance(isItalic,bool) and not isItalic and wasItalic:
				speech.speakMessage(_("not italic"))
			self._text_lastReportedPresentation["isItalic"]=isItalic
			isUnderline=self.text_isUnderline(offset)
			wasUnderline=self._text_lastReportedPresentation.get('isUnderline',None)
			if isinstance(isUnderline,bool) and isUnderline and not wasUnderline:
				speech.speakMessage(_("underline"))
			elif isinstance(isUnderline,bool) and not isUnderline and wasUnderline:
				speech.speakMessage(_("not underline"))
			self._text_lastReportedPresentation["isUnderline"]=isUnderline
			isSuperscript=self.text_isSuperscript(offset)
			wasSuperscript=self._text_lastReportedPresentation.get('isSuperscript',None)
			if isinstance(isSuperscript,bool) and isSuperscript and not wasSuperscript:
				speech.speakMessage(_("superscript"))
			elif isinstance(isSuperscript,bool) and not isSuperscript and wasSuperscript:
				speech.speakMessage(_("not superscript"))
			self._text_lastReportedPresentation["isSuperscript"]=isSuperscript
			isSubscript=self.text_isSubscript(offset)
			wasSubscript=self._text_lastReportedPresentation.get('isSubscript',None)
			if isinstance(isSubscript,bool) and isSubscript and not wasSubscript:
				speech.speakMessage(_("superscript"))
			elif isinstance(isSubscript,bool) and not isSubscript and wasSubscript:
				speech.speakMessage(_("not subscript"))
			self._text_lastReportedPresentation["isSubscript"]=isSubscript

	def text_reportPresentation(self,offset):
		style=self.text_getStyle(offset)
		alignment=self.text_getAlignment(offset)
		fontName=self.text_getFontName(offset)
		fontSize=self.text_getFontSize(offset)
		isBold=self.text_isBold(offset)
		isItalic=self.text_isItalic(offset)
		isUnderline=self.text_isUnderline(offset)
		isSuperscript=self.text_isSuperscript(offset)
		isSubscript=self.text_isSubscript(offset)
		if isinstance(style,basestring):
			speech.speakMessage(_("style %s")%style)
		if isinstance(alignment,basestring):
			speech.speakMessage(_("alignment %s")%alignment)
		if isinstance(fontName,basestring):
			speech.speakMessage(_("font name %s")%fontName)
		if isinstance(fontSize,int):
			speech.speakMessage(_("font size %d")%fontSize)
		if isinstance(isBold,bool) and isBold:
			speech.speakMessage(_("bold"))
		if isinstance(isItalic,bool) and isItalic:
			speech.speakMessage(_("italic"))
		if isinstance(isUnderline,bool) and isUnderline:
			speech.speakMessage(_("underline"))
		if isinstance(isSuperscript,bool) and isSuperscript:
			speech.speakMessage(_("superscript"))
		if isinstance(isSubscript,bool) and isSubscript:
			speech.speakMessage(_("subscript"))

	def text_speakLine(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getLineOffsets(offset)
		if r is not None:
			speech.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def text_speakWord(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getWordOffsets(offset)
		if r is not None:
			speech.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def text_speakCharacter(self,offset):
		self.text_reportNewPresentation(offset)
		speech.speakSymbol(self.text_getText(offset,offset+1),index=offset)

	def text_speakSentence(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getSentenceOffsets(offset)
		if r is not None:
			speech.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def text_speakParagraph(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getParagraphOffsets(offset)
		if r is not None:
			speech.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def _get_text_reviewOffsetLimits(self):
		return (0,self.text_characterCount-1)

	def script_text_review_moveToCaret(self,keyPress,nextScript):
		self.text_reviewOffset=self.text_caretOffset
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_top(self,keyPress,nextScript):
		speech.speakMessage(_("top"))
		self.text_reviewOffset=self.text_reviewOffsetLimits[0]
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_bottom(self,keyPress,nextScript):
		speech.speakMessage(_("bottom"))
		self.text_reviewOffset=self.text_reviewOffsetLimits[1]
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_currentLine(self,keyPress,nextScript):
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_nextLine(self,keyPress,nextScript):
		r=self.text_getNextLineOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			speech.speakMessage(_("bottom"))
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_prevLine(self,keyPress,nextScript):
		r=self.text_getPrevLineOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			speech.speakMessage(_("top"))
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_currentWord(self,keyPress,nextScript):
		self.text_speakWord(self.text_reviewOffset)

	def script_text_review_nextWord(self,keyPress,nextScript):
		r=self.text_getNextWordOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			speech.speakMessage(_("bottom"))
		self.text_speakWord(self.text_reviewOffset)

	def script_text_review_prevWord(self,keyPress,nextScript):
		r=self.text_getPrevWordOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			speech.speakMessage(_("top"))
		self.text_speakWord(self.text_reviewOffset)

	def script_text_review_currentCharacter(self,keyPress,nextScript):
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_nextCharacter(self,keyPress,nextScript):
		newOffset=self.text_reviewOffset+1
		limits=self.text_reviewOffsetLimits
		if newOffset>=limits[0] and newOffset<=limits[1]:
			self.text_reviewOffset=newOffset
		else:
			speech.speakMessage(_("bottom"))
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_prevCharacter(self,keyPress,nextScript):
		newOffset=self.text_reviewOffset-1
		limits=self.text_reviewOffsetLimits
		if newOffset>=limits[0] and newOffset<=limits[1]:
			self.text_reviewOffset=newOffset
		else:
			speech.speakMessage(_("top"))
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_startOfLine(self,keyPress,nextScript):
		r=self.text_getLineOffsets(self.text_reviewOffset)
		self.text_reviewOffset=r[0]
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_endOfLine(self,keyPress,nextScript):
		r=self.text_getLineOffsets(self.text_reviewOffset)
		self.text_reviewOffset=r[1]-1
		self.text_speakCharacter(self.text_reviewOffset)

	def text_sayAll_generator(self,offset):
		curPos=offset
		chunkOffsetsFunc=self.text_getLineOffsets
		nextChunkOffsetsFunc=self.text_getNextLineOffsets
		lastKeyCount=globalVars.keyCounter
		while (curPos<self.text_characterCount) and (lastKeyCount==globalVars.keyCounter):
			r=chunkOffsetsFunc(curPos)
			if r is None:
				break
			text=self.text_getText(r[0],r[1])
			if text and not text.isspace():
				speech.speakText(text,index=r[0])
			r=nextChunkOffsetsFunc(curPos)
			if r is None:
				break
			curPos=r[0]
			yield

	def script_text_moveByLine(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			self.text_speakLine(self.text_caretOffset)
		if globalVars.caretMovesReviewCursor:
			self.text_reviewOffset=self.text_caretOffset
	script_text_moveByLine.__doc__=_("Moves and then reads the current line")

	def script_text_reportCurrentLine(self,keyPress,nextScript):
		self.text_speakLine(self.text_caretOffset)
	script_text_reportCurrentLine.__doc__=_("reads the current line")

	def script_text_moveByCharacter(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			self.text_speakCharacter(self.text_caretOffset)
		if globalVars.caretMovesReviewCursor:
			self.text_reviewOffset=self.text_caretOffset
	script_text_moveByCharacter.__doc__=_("Moves and reads the current character")

	def script_text_moveByWord(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			self.text_speakWord(self.text_caretOffset)
		if globalVars.caretMovesReviewCursor:
			self.text_reviewOffset=self.text_caretOffset
	script_text_moveByWord.__doc__=_("Moves and reads the current word")

	def script_text_moveBySentence(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			self.text_speakSentence(self.text_caretOffset)
		if globalVars.caretMovesReviewCursor:
			self.text_reviewOffset=self.text_caretOffset
	script_text_moveBySentence.__doc__=_("Moves and then reads the current line")

	def script_text_moveByParagraph(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			self.text_speakParagraph(self.text_caretOffset)
		if globalVars.caretMovesReviewCursor:
			self.text_reviewOffset=self.text_caretOffset
	script_text_moveByParagraph.__doc__=_("Moves and then reads the current line")

	def script_text_nextParagraph(self,keyPress,nextScript):
		r=self.text_getNextParagraphOffsets(self.text_caretOffset)
		if r:
			self.text_caretOffset=r[0]
			self.text_speakParagraph(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset
	script_text_nextParagraph.__doc__=_("Manually moves to the next paragraph and then speaks it")

	def script_text_prevParagraph(self,keyPress,nextScript):
		r=self.text_getPrevParagraphOffsets(self.text_caretOffset)
		if r:
			self.text_caretOffset=r[0]
			self.text_speakParagraph(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset
	script_text_prevParagraph.__doc__=_("Manually moves to the previous paragraph and then speaks it")

	def script_text_changeSelection(self,keyPress,nextScript):
		oldSelections=[]
		for selNum in xrange(self.text_selectionCount):
			oldSelections.append(self.text_getSelectionOffsets(selNum))
		sendKey(keyPress)
		newSelections=[]
		for selNum in xrange(self.text_selectionCount):
			newSelections.append(self.text_getSelectionOffsets(selNum))
		if len(oldSelections)>0 and len(newSelections)==0:
			self.text_speakCharacter(self.text_caretOffset)
			speech.speakMessage(_("no selections"))
		elif len(newSelections)>0 and len(oldSelections)==0:
			for selNum in xrange(len(newSelections)):
					speech.speakMessage(_("selected %s")%self.text_getText(newSelections[selNum][0],newSelections[selNum][1]))
		elif len(newSelections)>0 and len(oldSelections)>0:
			for selNum in xrange(max(len(newSelections),len(oldSelections))):
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][1]>oldSelections[selNum][1]:
   					speech.speakMessage(_("selected %s")%self.text_getText(oldSelections[selNum][1],newSelections[selNum][1]))
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][0]>oldSelections[selNum][0]:
   					speech.speakMessage(_("selected %s")%self.text_getText(oldSelections[selNum][0],newSelections[selNum][0]))
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][1]<oldSelections[selNum][1]:
   					speech.speakMessage(_("unselected %s")%self.text_getText(newSelections[selNum][1],oldSelections[selNum][1]))
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][0]<oldSelections[selNum][0]:
   					speech.speakMessage(_("unselected %s")%self.text_getText(newSelections[selNum][0],oldSelections[selNum][0]))
				if selNum<len(newSelections) and selNum>=len(oldSelections):
   					speech.speakMessage(_("selected %s")%self.text_getText(newSelections[selNum][0],newSelections[selNum][1]))
				if selNum>=len(newSelections) and selNum<len(oldSelections):
   					speech.speakMessage(_("unselected %s")%self.text_getText(oldSelections[selNum][0],oldSelections[selNum][1]))
		self.text_reviewOffset=self.text_caretOffset
	script_text_changeSelection.__doc__=_("Moves and reads the current selection")

	def script_text_delete(self,keyPress,nextScript):
		sendKey(keyPress)
		self.text_speakCharacter(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset
	script_text_delete.__doc__=_("Deletes the character and reads the new current character")

	def script_text_backspace(self,keyPress,nextScript):
		point=self.text_caretOffset
		if point>0:
			delChar=self.text_getText(point-1,point)
			sendKey(keyPress)
			newPoint=self.text_caretOffset
			if newPoint<point:
				speech.speakSymbol(delChar)
		else:
			sendKey(keyPress)
			speech.speakText("")
		self.text_reviewOffset=self.text_caretOffset
	script_text_backspace.__doc__=_("Reads the character before the current character and then deletes it")

