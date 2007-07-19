#text.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import baseObject

#exceptions
class E_noRelatedUnit(RuntimeError):
	pass

#Field stuff

FORMAT_CMD_ON=1
FORMAT_CMD_OFF=2
FORMAT_CMD_SINGLETON=3

class FormatCommand(object):

	def __init__(self,cmd,format):
 		self.cmd=cmd
		self.format=format

class Format(object):

	def __init__(self,role,value="",states=frozenset(),contains="",uniqueID=""):
		self.role=role
		self.value=value
		self.states=states
		self.contains=contains
		self.uniqueID=uniqueID

#position types

class Position(baseObject.autoPropertyObject):
	pass

class OffsetsPosition(Position):

	def __init__(self,start,end=None):
		if end is None:
			end=start
		self.start=start
		self.end=end


class pointsPosition(Position):

	def __init__(self,startX,startY,endX=None,endY=None):
		if endX is None:
			endX=startX
		if endY is None:
			endY=startY
		self.startX=startX
		self.startY=startY
		self.endX=endX
		self.endY=endY

#Position constants
POSITION_FIRST="first"
POSITION_LAST="last"
POSITION_CARET="caret"
POSITION_SELECTION="selection"
POSITION_ALL="all"

class Bookmark(baseObject.autoPropertyObject):

	def __init__(self,data):
		self.data=data

#Selection mode constants
SELECTIONMODE_SELECTED="selected"
SELECTIONMODE_UNSELECTED="unselected"

#Unit constants
UNIT_CHARACTER="character"
UNIT_WORD="word"
UNIT_LINE="line"
UNIT_SENTENCE="sentence"
UNIT_PARAGRAPH="paragraph"
UNIT_PAGE="page"
UNIT_TABLE="table"
UNIT_ROW="row"
UNIT_COLUMN="column"
UNIT_CELL="cell"
UNIT_SCREEN="screen"
UNIT_STORY="story"
UNIT_READINGCHUNK="readingChunck"

class TextSelectionChangedInfo(baseObject.autoPropertyObject):

	def _get_text(self):
		raise NotImplementedError

	def _get_mode(self):
		raise NotImplementedError

class TextInfo(baseObject.autoPropertyObject):
	"""Contains information about the text at the given position or unit
@ivar obj: The NVDA object this object is representing text from
@type: L{NVDAObject}
"""
 
	def __init__(self,obj,position):
		"""
@param position: the position (offset or point) this object was based on. Can also be one of the position constants to be caret or selection
@type position: int, tuple or string
@param obj: The NVDA object this object is representing text from
@type: L{NVDAObject}
"""
		self.obj=obj
		self.basePosition=position


	def _get_text(self):
		"""
@returns: The text with in the set range. It is not garenteed to be the exact length of the range in offsets
@rtype: string
"""
		raise NotImplementedError

	def _get_formattedText(self):
		"""
@returns: The text (containing formatting markup) with in the set range
@rtype: string
"""
		return [self.text]


	def _get_FGColor(self):
		"""
@returns: The foreground color at the start of the set range
@rtype: string
"""
		raise NotImplementedError

	def _get_BGColor(self):
		"""
@returns: The background color at the start of the set range
@rtype: string
"""
		raise NotImplementedError

	def _get_format(self):
		"""
@returns: The format at the start of the set range
@rtype: dict (string:string)
"""
		raise NotImplementedError

	def unitIndex(self,unit):
		"""
@param unit: a unit constant for which you want to retreave an index
@type: string
@returns: The 1-based index of this unit, out of all the units of this type in the object
@rtype: int
"""  
		raise NotImplementedError

	def unitCount(self,unit):
		"""
@param unit: a unit constant
@type unit: string
@returns: the number of units of this type in the object
@rtype: int
"""
		raise NotImplementedError

	def compareStart(self,info):
		"""
@param info: the text info object to compare with
@type info: L{TextInfo}
@returns: the start of this text info object relative to the start of the given text info object
@rtype: int
"""
		raise NotImplementedError

	def compareEnd(self,info):
		"""
@param info: the text info object to compare with
@type info: L{TextInfo}
@returns: the end of this text info object relative to the end of the given text info object
@rtype: int
"""
		raise NotImplementedError

	def expand(self,unit):
		"""Expands the start and end of this text info object to a given unit
@param unit: a unit constant
@type unit: string
"""
		raise NotImplementedError

	def collapse(self):
		"""Sets the end of this text info object so its equal to the start (collapsing it to a point)
"""
		raise NotImplementedError

	def copy(self):
		"""duplicates this text info object so that changes can be made to either one with out afecting the other 
"""
		raise NotImplementedError

	def updateCaret(self):
		"""Moves the system caret to the position of this text info object"""
		raise NotImplementedError

	def updateSelection(self):
		"""Moves the system caret to the position of this text info object"""
		raise NotImplementedError

	def _get_bookmark(self):
		"""Returns a unique identifier that can be used to make another textInfo object at this position
@returns: a bookmark
@rtype: L{Bookmark}
"""
		raise NotImplementedError

def findStartOfLine(text,offset,lineLength=None):
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
	if offset>=len(text):
		offset=len(text)-1
	while offset>0 and text[offset].isspace():
		offset-=1
	if not text[offset].isalnum():
		return offset
	else:
		while offset>0 and text[offset-1].isalnum():
			offset-=1
	return offset

def findEndOfWord(text,offset,lineLength=None):
	if offset>=len(text):
		offset=len(text)-1
	if text[offset].isalnum():
		while offset<len(text) and text[offset].isalnum():
			offset+=1
	elif not text[offset].isspace() and not text[offset].isalnum():
		offset+=1
	while offset<len(text) and text[offset].isspace():
		offset+=1
	return offset
