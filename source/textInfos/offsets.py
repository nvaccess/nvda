#textInfos/offsets.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import re
import ctypes
import unicodedata
import NVDAHelper
import config
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
	if not text:
		return 0
	if offset>=len(text):
		offset=len(text)-1
	if isinstance(lineLength,int):
		return offset-(offset%lineLength)
	if text[offset]=='\n' and offset>=0 and text[offset-1]=='\r':
		offset-=1
	start=text.rfind('\n',0,offset)
	if start<0:
		start=text.rfind('\r',0,offset)
	if start<0:
		start=-1
	return start+1

def findEndOfLine(text,offset,lineLength=None):
	"""Searches forwards through the given text from the given offset, until it finds the offset that is the start of the next line. With out a set line length, it searches for new line / cariage return characters, with a set line length it simply moves forward to sit on a multiple of the line length.
@param text: the text to search
@type text: unicode
@param offset: the offset of the text to start at
@type offset: int
@param lineLength: The number of characters that makes up a line, None if new line characters should be looked at instead
@type lineLength: int or None
@return: the found offset
@rtype: int 
"""
	if not text:
		return 0
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
@type text: unicode
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
	if unicodedata.category(text[offset])[0] not in "LMN":
		return offset
	else:
		while offset>0 and unicodedata.category(text[offset-1])[0] in "LMN":
			offset-=1
	return offset

def findEndOfWord(text,offset,lineLength=None):
	"""Searches forwards through the given text from the given offset, until it finds the offset that is the start of the next word. It checks to see if a character is alphanumeric, or is another symbol , or is white space.
@param text: the text to search
@type text: unicode
@param offset: the offset of the text to start at
@type offset: int
@param lineLength: The number of characters that makes up a line, None if new line characters should be looked at instead
@type lineLength: int or None
@return: the found offset
@rtype: int 
"""
	if offset>=len(text):
		return offset+1
	if unicodedata.category(text[offset])[0] in "LMN":
		while offset<len(text) and unicodedata.category(text[offset])[0] in "LMN":
			offset+=1
	elif unicodedata.category(text[offset])[0] not in "LMNZ":
		offset+=1
	while offset<len(text) and text[offset].isspace():
		offset+=1
	return offset

class OffsetsTextInfo(textInfos.TextInfo):
	"""An abstract TextInfo for text implementations which represent ranges using numeric offsets relative to the start of the text.
	In such implementations, the start of the text is represented by 0 and the end is the length of the entire text.
	
	All subclasses must implement L{_getStoryLength}.
	Aside from this, there are two possible implementations:
		* If the underlying text implementation does not support retrieval of line offsets, L{_getStoryText} should be implemented.
		In this case, the base implementation of L{_getLineOffsets} will retrieve the entire text of the object and use text searching algorithms to find line offsets.
		This is very inefficient and should be avoided if possible.
		* Otherwise, subclasses must implement at least L{_getTextRange} and L{_getLineOffsets}.
		Retrieval of other offsets (e.g. L{_getWordOffsets}) should also be implemented if possible for greatest accuracy and efficiency.
	
	If a caret and/or selection should be supported, L{_getCaretOffset} and/or L{_getSelectionOffsets} should be implemented, respectively.
	To support conversion from/to screen points (e.g. for mouse tracking), L{_getOffsetFromPoint}/L{_getPointFromOffset} should be implemented.
	"""

	detectFormattingAfterCursorMaybeSlow=True #: honours documentFormatting config option if true - set to false if this is not at all slow.
	useUniscribe=True #Use uniscribe to calculate word offsets etc
 

	def __eq__(self,other):
		if self is other or (isinstance(other,OffsetsTextInfo) and self._startOffset==other._startOffset and self._endOffset==other._endOffset):
			return True
		else:
			return False

	def _get_locationText(self):
		textList=[]
		storyLength=self._getStoryLength() or 1
		curPercent=(self._startOffset/float(storyLength))*100
		# Translators: current position in a document as a percentage of the document length
		textList.append(_("{curPercent:.0f}%").format(curPercent=curPercent))
		try:
			curPoint=self.pointAtStart
		except (NotImplementedError,LookupError):
			curPoint=None
		if curPoint is not None:
			# Translators: the current position's screen coordinates in pixels
			textList.append(_("at {x}, {y}").format(x=curPoint.x,y=curPoint.y))
		return ", ".join(textList)

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

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		raise NotImplementedError

	def _getTextRange(self,start,end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text=self._getStoryText()
		return text[start:end] if text else u""

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		"""Retrieve the formatting information for a given offset and the offsets spanned by that field.
		Subclasses must override this if support for text formatting is desired.
		The base implementation associates text with line numbers if possible.
		"""
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
		#Convert NULL and non-breaking space to space to make sure that words will break on them
		lineText=lineText.translate({0:u' ',0xa0:u' '})
		if self.useUniscribe:
			start=ctypes.c_int()
			end=ctypes.c_int()
			#uniscribe does some strange things when you give it a string  with not more than two alphanumeric chars in a row.
			#Inject two alphanumeric characters at the end to fix this 
			lineText+="xx"
			if NVDAHelper.localLib.calculateWordOffsets(lineText,len(lineText),offset-lineStart,ctypes.byref(start),ctypes.byref(end)):
				return start.value+lineStart,min(end.value+lineStart,lineEnd)
		#Fall back to the older word offsets detection that only breaks on non alphanumeric
		start=findStartOfWord(lineText,offset-lineStart)+lineStart
		end=findEndOfWord(lineText,offset-lineStart)+lineStart
		return [start,end]

	def _getLineNumFromOffset(self,offset):
		return None


	def _getLineOffsets(self,offset):
		text=self._getStoryText()
		start=findStartOfLine(text,offset)
		end=findEndOfLine(text,offset)
		return [start,end]

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)


	def _getReadingChunkOffsets(self,offset):
		return self._getLineOffsets(offset)

	def _getPointFromOffset(self,offset):
		raise NotImplementedError

	def _getOffsetFromPoint(self,x,y):
		raise NotImplementedError

	def _getNVDAObjectFromOffset(self,offset):
		raise NotImplementedError

	def _getOffsetsFromNVDAObject(self,obj):
		raise NotImplementedError

	def __init__(self,obj,position):
		"""Constructor.
		Subclasses may extend this to perform implementation specific initialisation, calling their superclass method afterwards.
		"""
		super(OffsetsTextInfo,self).__init__(obj,position)
		from NVDAObjects import NVDAObject
		if isinstance(position,textInfos.Point):
			offset=self._getOffsetFromPoint(position.x,position.y)
			position=Offsets(offset,offset)
		elif isinstance(position,NVDAObject):
			start,end=self._getOffsetsFromNVDAObject(position)
			position=textInfos.offsets.Offsets(start,end)

		if type(position) is type(self):
			# This is a direct TextInfo to TextInfo copy.
			# Copy over the contents of the property cache, and any private instance variables (includes the TextInfo's offsets) 
			self._propertyCache.update(position._propertyCache)
			self.__dict__.update({x:y for x,y in position.__dict__.iteritems() if x.startswith('_') and x!='_propertyCache'})
		elif position==textInfos.POSITION_FIRST:
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
			self._startOffset=max(min(position.startOffset,self._getStoryLength()),0)
			self._endOffset=max(min(position.endOffset,self._getStoryLength()),0)
		else:
			raise NotImplementedError("position: %s not supported"%position)

	def _get_NVDAObjectAtStart(self):
		return self._getNVDAObjectFromOffset(self._startOffset)

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
		elif unit==textInfos.UNIT_STORY:
			return 0,self._getStoryLength()
		elif unit==textInfos.UNIT_OFFSET:
			return offset,offset+1
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
		return self.__class__(self.obj,self)

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
		if self._startOffset>self._endOffset:
			# start should never be after end.
			if which in ("startToStart","startToEnd"):
				self._endOffset=self._startOffset
			else:
				self._startOffset=self._endOffset

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		if self.detectFormattingAfterCursorMaybeSlow and not formatConfig['detectFormatAfterCursor']:
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

	allowMoveToOffsetPastEnd=True #: move with unit_character can move 1 past story length to allow braille routing to end insertion point. (#2096)

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
		if self.allowMoveToOffsetPastEnd and unit==textInfos.UNIT_CHARACTER:
			# #2096: There is often an uncounted character at the end of the text
			# where the caret is placed to append text.
			highLimit+=1
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
		m=re.search(re.escape(text),inText,(0 if caseSensitive else re.IGNORECASE)|re.UNICODE)
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
