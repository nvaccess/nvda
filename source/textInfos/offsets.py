#textInfos/offsets.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import textInfos

class Offsets(object):
	"""Represents two offsets."""

	def __init__(self,startOffset,endOffset):
		"""
		@param startOffset: the first offset.
		@type startOffset: integer
		@param endOffset: the second offset.
		@type endOffset: integer
		"""
		self.startOffset=startOffset
		self.endOffset=endOffset

	def __eq__(self,other):
		if isinstance(other,self.__class__) and self.startOffset==other.startOffset and self.endOffset==other.endOffset:
			return True
		else:
			return False

	def __ne__(self,other):
		return not self==other
 
def findStartOfLine(text,offset,lineLength=None):
	"""Searches backwards through the given text from the given offset, until it finds the offset that is the start of the line. With out a set line length, it searches for new line / cariage return characters, with a set line length it simply moves back to sit on a multiple of the line length.
@param text: the text to search
@type text: string
@param offset: the offset of the text to start at
@type offset: int
@param lineLength: The number of characters that makes up a line, None if new line characters should be looked at instead
@type lineLength: int or None
@return: the found offset
@rtype: int 
"""
	if offset>=len(text):
		offset=len(text)-1
	start=offset
	if isinstance(lineLength,int):
		return offset-(offset%lineLength)
	if text[start]=='\n' and start>=0 and text[start-1]=='\r':
		start-=1
	start=text.rfind('\n',0,offset)
	if start<0:
		start=text.rfind('\r',0,offset)
	if start<0:
		start=-1
	return start+1

def findEndOfLine(text,offset,lineLength=None):
	"""Searches forwards through the given text from the given offset, until it finds the offset that is the start of the next line. With out a set line length, it searches for new line / cariage return characters, with a set line length it simply moves forward to sit on a multiple of the line length.
@param text: the text to search
@type text: string
@param offset: the offset of the text to start at
@type offset: int
@param lineLength: The number of characters that makes up a line, None if new line characters should be looked at instead
@type lineLength: int or None
@return: the found offset
@rtype: int 
"""
	if offset>=len(text):
		offset=len(text)-1
	if isinstance(lineLength,int):
		return (offset-(offset%lineLength)+lineLength)
	end=offset
	if text[end]!='\n':
		end=text.find('\n',offset)
	if end<0:
		if text[offset]!='\r':
			end=text.find('\r',offset)
	if end<0:
		end=len(text)-1
	return end+1

def findStartOfWord(text,offset,lineLength=None):
	"""Searches backwards through the given text from the given offset, until it finds the offset that is the start of the word. It checks to see if a character is alphanumeric, or is another symbol , or is white space.
@param text: the text to search
@type text: string
@param offset: the offset of the text to start at
@type offset: int
@param lineLength: The number of characters that makes up a line, None if new line characters should be looked at instead
@type lineLength: int or None
@return: the found offset
@rtype: int 
"""
	if offset>=len(text):
		return offset
	while offset>0 and text[offset].isspace():
		offset-=1
	if not text[offset].isalnum():
		return offset
	else:
		while offset>0 and text[offset-1].isalnum():
			offset-=1
	return offset

def findEndOfWord(text,offset,lineLength=None):
	"""Searches forwards through the given text from the given offset, until it finds the offset that is the start of the next word. It checks to see if a character is alphanumeric, or is another symbol , or is white space.
@param text: the text to search
@type text: string
@param offset: the offset of the text to start at
@type offset: int
@param lineLength: The number of characters that makes up a line, None if new line characters should be looked at instead
@type lineLength: int or None
@return: the found offset
@rtype: int 
"""
	if offset>=len(text):
		return offset+1
	if text[offset].isalnum():
		while offset<len(text) and text[offset].isalnum():
			offset+=1
	elif not text[offset].isspace() and not text[offset].isalnum():
		offset+=1
	while offset<len(text) and text[offset].isspace():
		offset+=1
	return offset

class OffsetsTextInfo(textInfos.TextInfo):

	def __eq__(self,other):
		if self is other or (isinstance(other,OffsetsTextInfo) and self._startOffset==other._startOffset and self._endOffset==other._endOffset):
			return True
		else:
			return False

	def _getCaretOffset(self):
		raise NotImplementedError

	def _setCaretOffset(self,offset):
		raise NotImplementedError

	def _getSelectionOffsets(self):
		raise NotImplementedError

	def _setSelectionOffsets(self,start,end):
		raise NotImplementedError

	def _getStoryLength(self):
		raise NotImplementedError

	def _getTextRange(self,start,end):
		raise NotImplementedError

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		formatField=textInfos.FormatField()
		startOffset,endOffset=self._startOffset,self._endOffset
		if formatConfig["reportLineNumber"]:
			if calculateOffsets:
				startOffset,endOffset=self._getLineOffsets(offset)
			lineNum=self._getLineNumFromOffset(offset)
			if lineNum is not None:
				formatField["line-number"]=lineNum+1
		return formatField,(startOffset,endOffset)

	def _getCharacterOffsets(self,offset):
		return [offset,offset+1]

	def _getWordOffsets(self,offset):
		lineStart,lineEnd=self._getLineOffsets(offset)
		lineText=self._getTextRange(lineStart,lineEnd)
		start=findStartOfWord(lineText,offset-lineStart)+lineStart
		end=findEndOfWord(lineText,offset-lineStart)+lineStart
		return [start,end]

	def _getLineNumFromOffset(self,offset):
		raise NotImplementedError

	def _getLineOffsets(self,offset):
		raise NotImplementedError

	def _getParagraphOffsets(self,offset):
		raise NotImplementedError

	def _getReadingChunkOffsets(self,offset):
		return self._getLineOffsets(offset)

	def _getPointFromOffset(self,offset):
		raise NotImplementedError

	def _getOffsetFromPoint(self,x,y):
		raise NotImplementedError

	def __init__(self,obj,position):
		super(OffsetsTextInfo,self).__init__(obj,position)
		if isinstance(position,textInfos.Point):
			offset=self._getOffsetFromPoint(position.x,position.y)
			position=Offsets(offset,offset)
		if position==textInfos.POSITION_FIRST:
			self._startOffset=self._endOffset=0
		elif position==textInfos.POSITION_LAST:
			self._startOffset=self._endOffset=max(self._getStoryLength()-1,0)
		elif position==textInfos.POSITION_CARET:
			self._startOffset=self._endOffset=self._getCaretOffset()
		elif position==textInfos.POSITION_SELECTION:
			(self._startOffset,self._endOffset)=self._getSelectionOffsets()
		elif position==textInfos.POSITION_ALL:
			self._startOffset=0
			self._endOffset=self._getStoryLength()
		elif isinstance(position,Offsets):
			self._startOffset=max(min(position.startOffset,self._getStoryLength()-1),0)
			self._endOffset=max(min(position.endOffset,self._getStoryLength()),0)
		else:
			raise NotImplementedError("position: %s not supported"%position)

	def _getUnitOffsets(self,unit,offset):
		if unit==textInfos.UNIT_CHARACTER:
			offsetsFunc=self._getCharacterOffsets
		elif unit==textInfos.UNIT_WORD:
			offsetsFunc=self._getWordOffsets
		elif unit==textInfos.UNIT_LINE:
			offsetsFunc=self._getLineOffsets
		elif unit==textInfos.UNIT_PARAGRAPH:
			offsetsFunc=self._getParagraphOffsets
		elif unit==textInfos.UNIT_READINGCHUNK:
			offsetsFunc=self._getReadingChunkOffsets
		else:
			raise ValueError("unknown unit: %s"%unit)
		return offsetsFunc(offset)

	def _get_pointAtStart(self):
		return self._getPointFromOffset(self._startOffset)

	def _get_isCollapsed(self):
		if self._startOffset==self._endOffset:
			return True
		else:
			return False

	def collapse(self,end=False):
		if not end:
			self._endOffset=self._startOffset
		else:
			self._startOffset=self._endOffset

	def expand(self,unit):
		self._startOffset,self._endOffset=self._getUnitOffsets(unit,self._startOffset)

	def copy(self):
		o=self.__class__(self.obj,self.bookmark)
		for item in self.__dict__.keys():
			if item.startswith('_'):
				o.__dict__[item]=self.__dict__[item]
		return o

	def compareEndPoints(self,other,which):
		if which=="startToStart":
			diff=self._startOffset-other._startOffset
		elif which=="startToEnd":
			diff=self._startOffset-other._endOffset
		elif which=="endToStart":
			diff=self._endOffset-other._startOffset
		elif which=="endToEnd":
			diff=self._endOffset-other._endOffset
		else:
			raise ValueError("bad argument - which: %s"%which)
		if diff<0:
			diff=-1
		elif diff>0:
			diff=1
		return diff

	def setEndPoint(self,other,which):
		if which=="startToStart":
			self._startOffset=other._startOffset
		elif which=="startToEnd":
			self._startOffset=other._endOffset
		elif which=="endToStart":
			self._endOffset=other._startOffset
		elif which=="endToEnd":
			self._endOffset=other._endOffset
		else:
			raise ValueError("bad argument - which: %s"%which)

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		if not formatConfig['detectFormatAfterCursor']:
			field,(boundStart,boundEnd)=self._getFormatFieldAndOffsets(self._startOffset,formatConfig,calculateOffsets=False)
			text=self.text
			return [textInfos.FieldCommand('formatChange',field),text]
		commandList=[]
		offset=self._startOffset
		while offset<self._endOffset:
			field,(boundStart,boundEnd)=self._getFormatFieldAndOffsets(offset,formatConfig)
			if boundEnd<=boundStart:
				boundEnd=boundStart+1
			if boundEnd<=offset:
				boundEnd=offset+1
			command=textInfos.FieldCommand("formatChange",field)
			commandList.append(command)
			text=self._getTextRange(offset,min(boundEnd,self._endOffset))
			commandList.append(text)
			offset=boundEnd
		return commandList

	def _get_text(self):
		return self._getTextRange(self._startOffset,self._endOffset)

	def unitIndex(self,unit):
		if unit==textInfos.UNIT_LINE:  
			return self._lineNumFromOffset(self._startOffset)
		else:
			raise NotImplementedError

	def unitCount(self,unit):
		if unit==textInfos.UNIT_LINE:
			return self._getLineCount()
		else:
			raise NotImplementedError

	def move(self,unit,direction,endPoint=None):
		if direction==0:
			return 0;
		if endPoint=="end":
			offset=self._endOffset
		elif endPoint=="start":
			offset=self._startOffset
		else:
			self.collapse()
			offset=self._startOffset
		lastOffset=None
		count=0
		lowLimit=0
		highLimit=self._getStoryLength()
		while count!=direction and (lastOffset is None or (direction>0 and offset>lastOffset) or (direction<0 and offset<lastOffset)) and (offset<highLimit or direction<0) and (offset>lowLimit or direction>0):
			lastOffset=offset
			if direction<0 and offset>lowLimit:
				offset-=1
			newStart,newEnd=self._getUnitOffsets(unit,offset)
			if direction<0:
				offset=newStart
			elif direction>0:
				offset=newEnd
			count=count+1 if direction>0 else count-1
		if endPoint=="start":
			if (direction>0 and offset<=self._startOffset) or (direction<0 and offset>=self._startOffset) or offset<lowLimit or offset>=highLimit:
				return 0
			self._startOffset=offset
		elif endPoint=="end":
			if (direction>0 and offset<=self._endOffset) or (direction<0 and offset>=self._endOffset) or offset<lowLimit or offset>highLimit:
				return 0
			self._endOffset=offset
		else:
			if (direction>0 and offset<=self._startOffset) or (direction<0 and offset>=self._startOffset) or offset<lowLimit or offset>=highLimit:
				return 0
			self._startOffset=self._endOffset=offset
		if self._startOffset>self._endOffset:
			tempOffset=self._startOffset
			self._startOffset=self._endOffset
			self._endOffset=tempOffset
		return count

	def find(self,text,caseSensitive=False,reverse=False):
		if reverse:
			# When searching in reverse, we reverse both strings and do a forwards search.
			text = text[::-1]
			# Start searching one before the start to avoid finding the current match.
			inText=self._getTextRange(0,self._startOffset)[::-1]
		else:
			# Start searching one past the start to avoid finding the current match.
			inText=self._getTextRange(self._startOffset+1,self._getStoryLength())
		m=re.search(re.escape(text),inText,re.IGNORECASE)
		if not m:
			return False
		if reverse:
			offset=self._startOffset-m.end()
		else:
			offset=self._startOffset+1+m.start()
		self._startOffset=self._endOffset=offset
		return True

	def updateCaret(self):
		return self._setCaretOffset(self._startOffset)

	def updateSelection(self):
		return self._setSelectionOffsets(self._startOffset,self._endOffset)

	def _get_bookmark(self):
		return Offsets(self._startOffset,self._endOffset)
