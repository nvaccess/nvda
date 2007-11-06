#textHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import baseObject

def isFormatEnabled(role,includes=set(),excludes=set()):
	"""Checks to see if a role is in an includes list (if given), or not in an excludes list (if given).
@param role: an NVDA object or format role
@type role: int
@param includes: a set of 0 or more roles, or None
@type includes: set, None
@param excludes: a set of 0 or more roles, or None
@type excludes: set, None
@rtype: bool
"""
	if len(includes)>0 and len(excludes)>0:
		raise ValueError("Only one of includes or excludes can be used")
	elif role in excludes:
		return False
	elif len(includes)>0 and role not in includes:
		return False
	else: 
		return True
   
#Field stuff

FORMAT_CMD_CHANGE=0
FORMAT_CMD_INFIELD=1
FORMAT_CMD_OUTOFFIELD=2
FORMAT_CMD_SWITCHON=3
FORMAT_CMD_SWITCHOFF=4

class FormatCommand(object):
	"""A container to hold a format, and also communicates whether the format is once off, is being turned on, or is being turned off.
@ivar cmd: the command type (one of the FORMAT_CMD_* constants)
@type cmd: int
 @ivar format: the format
@type format: L{Format}
"""

	def __init__(self,cmd,format):
		"""
@param cmd: the command type (one of the FORMAT_CMD_* constants)
@type cmd: int
 @param format: the format
@type format: L{Format}
"""
 		self.cmd=cmd
		self.format=format

class Format(object):
	"""Represents a field or format with in text.
@ivar role: The format's role (a control role or format role)
@type role: int
@ivar value: a line's number, a link's URL, a font name field's  name
@type value: string
@ivar states: a set of state constants (the checked state for a checkbox etc)
@type states: set
@ivar uniqueID: either a value unique to this format field, or None
"""

	def __init__(self,role,value="",states=frozenset(),contains="",uniqueID=""):
		"""
@param role: The format's role (a control role or format role)
@type role: int
@param value: a line's number, a link's URL, a font name field's  name
@type value: string
@param states: a set of state constants (the checked state for a checkbox etc)
@type states: set
@param uniqueID: either a value unique to this format field, or None
"""
		self.role=role
		self.value=value
		self.states=states
		self.contains=contains
		self.uniqueID=uniqueID

#Position constants
POSITION_FIRST="first"
POSITION_LAST="last"
POSITION_CARET="caret"
POSITION_SELECTION="selection"
POSITION_ALL="all"

class Bookmark(baseObject.autoPropertyObject):
	"""The type for representing a static absolute position from a L{TextInfo} object
@ivar infoClass: the class of the TextInfo object
@type infoClass: type
@ivar data: data that can be used to reconstruct the position the textInfo object was in when it generated the bookmark
"""

	def __init__(self,infoClass,data):
		"""
@param infoClass: the class of the TextInfo object
@type infoClass: type
@param data: data that can be used to reconstruct the position the textInfo object was in when it generated the bookmark
"""
		self.infoClass=infoClass
		self.data=data

	def __eq__(self,other):
		if isinstance(other,Bookmark) and self.infoClass==other.infoClass and self.data==other.data:
			return True

	def __ne__(self,other):
		return not self==other


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

class TextInfo(baseObject.autoPropertyObject):
	"""Contains information about the text at the given position or unit
@ivar position: the position (offset or point) this object was based on. Can also be one of the position constants to be caret or selection etc
@type position: int, tuple or string
@ivar obj: The NVDA object this object is representing text from
@type: L{NVDAObjects.NVDAObject}
@ivar isCollapsed: True if this textInfo object represents a collapsed range, False if the range is expanded to cover one or more characters 
@type isCollapsed: bool
@ivar text: The text with in the set range. It is not garenteed to be the exact length of the range in offsets
@type text: string
@ivar bookmark: a unique identifier that can be used to make another textInfo object at this position
@type bookmark: L{Bookmark}
"""
 
	def __init__(self,obj,position):
		"""
@param position: the position (offset or point) this object was based on. Can also be one of the position constants to be caret or selection etc
@type position: int, tuple or string
@param obj: The NVDA object this object is representing text from
@type: L{NVDAObject}
"""
		self._NVDAObject=weakref.ref(obj)
		self.basePosition=position

	def _get_obj(self):
		return self._NVDAObject()
 
	def _get_text(self):
		raise NotImplementedError

	def getFormattedText(self,searchRange=False,includes=set(),excludes=set()):
		"""
@returns: A sequence of L{FormatCommand} objects and strings of text.
@rtype: list
"""
		return [self.text]

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
		""" gives the difference in offsets of the start position for this object compared to the start position for the given l{info} object
@param info: the text info object to compare with
@type info: L{TextInfo}
@returns: the start of this text info object relative to the start of the given text info object
@rtype: int
"""
		raise NotImplementedError

	def compareEnd(self,info):
		""" gives the difference in offsets of the end position for this object compared to the end position for the given l{info} object
@param info: the text info object to compare with
@type info: L{TextInfo}
@returns: the end of this text info object relative to the end of the given text info object
@rtype: int
"""
		raise NotImplementedError

	def _get_isCollapsed(self):
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
		"""Moves the selection (usually the system caret) to the position of this text info object"""
		raise NotImplementedError

	def _get_bookmark(self):
		raise NotImplementedError

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
		offset=len(text)-1
	if text[offset].isalnum():
		while offset<len(text) and text[offset].isalnum():
			offset+=1
	elif not text[offset].isspace() and not text[offset].isalnum():
		offset+=1
	while offset<len(text) and text[offset].isspace():
		offset+=1
	return offset
