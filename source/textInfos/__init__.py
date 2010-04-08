#textInfos/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import re
import baseObject
import config
import speech

class Field(dict):
	"""The base type for fields in textInfo objects"""

class FormatField(Field):
	pass

class ControlField(Field):
	pass

class FieldCommand(object):

	def __init__(self,command,field):
		if command not in ("controlStart","controlEnd","formatChange"):
			raise ValueError("Unknown command: %s"%command)
		elif command=="controlStart" and not isinstance(field,ControlField):
			raise ValueError("command: %s needs a controlField"%command)
		elif command=="formatChange" and not isinstance(field,FormatField):
			raise ValueError("command: %s needs a formatField"%command)
		self.command=command
		self.field=field

#Position constants
POSITION_FIRST="first"
POSITION_LAST="last"
POSITION_CARET="caret"
POSITION_SELECTION="selection"
POSITION_ALL="all"

class Point(object):
	"""Represents a set of X Y coordinates."""

	def __init__(self,x,y):
		"""
		@param x: the x coordinate
		@type x: integer
		@param y: The y coordinate
		@type y: integer
		"""
		self.x=x
		self.y=y

class Points(object):
	"""Represents two sets of X Y coordinates."""

	def __init__(self,startX,startY,endX,endY):
		"""
		@param startX: the x coordinate of the first point.
		@type startX: integer
		@param xstartY: The y coordinate of the first point.
		@type startY: integer
		@param endX: the x coordinate of the second point.
		@type endX: integer
		@param endY: the y coordinate of the second point.
		@type endY: integer
		"""
		self.startX=startX
		self.startY=startY
		self.endX=endX
		self.endY=endY

class Bookmark(baseObject.AutoPropertyObject):
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
UNIT_READINGCHUNK="readingChunk"

unitLabels={
	UNIT_CHARACTER:_("character"),
	UNIT_WORD:_("word"),
	UNIT_LINE:_("line"),
	UNIT_PARAGRAPH:_("paragraph"),
}

class TextInfo(baseObject.AutoPropertyObject):
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
		super(TextInfo,self).__init__()
		self._obj=weakref.ref(obj) if type(obj)!=weakref.ProxyType else obj
		self.basePosition=position

	def _get_obj(self):
		return self._obj()

	def _get_unit_mouseChunk(self):
		return config.conf["mouse"]["mouseTextUnit"]

	def _get_text(self):
		raise NotImplementedError

	def getInitialFields(self,formatConfig=None):
		"""Retreaves the control fields, and the format field, that the start of this text range is currently positioned.
		@param formatConfig: a documentFormatting config key, useful if you wish to force a particular configuration for a particular task.
		@type formatConfig: dictionary
		@returns: a list of control fields and a format field
		@rtype: list
		""" 
		return []

	def getTextWithFields(self,formatConfig=None):
		"""Retreaves the text in this range, also including fields to indicate when controls start and end, and when format changes occure.
		@param formatConfig: a documentFormatting config key, useful if you wish to force a particular configuration for a particular task.
		@type formatConfig: dictionary
		@returns: a list of text strings and field commands
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

	def compareEndPoints(self,other,which):
		""" compares an end of this object to an end of another object
@param other: the text info object to compare with
@type other: L{TextInfo}
@param which: one of the strings startToStart startToEnd endToStart endToEnd
@TYPE WHICH: STRING
@returns: -1 if this end is before other end, or 1 if this end is after other end or 0 if this end and other end are the same. 
@rtype: int
"""
		raise NotImplementedError

	def isOverlapping(self, other):
		"""Determines whether this object overlaps another object in any way.
		Note that collapsed objects can cause some confusion.
		For example, in terms of offsets, (4, 4) and (4, 5) are not considered as overlapping.
		Therefore, collapsed objects should probably be expanded to at least 1 character when using this method.
		@param other: The TextInfo object being compared.
		@type other: L{TextInfo}
		@return: C{True} if the objects overlap, C{False} if not.
		@rtype: bool
		"""
		return self.compareEndPoints(other, "endToStart") > 0 and other.compareEndPoints(self, "endToStart") > 0

	def setEndPoint(self,other,which):
		"""Sets one end of this object to one end of the other object
@param other: the text info object to get the end from 
@type other: L{TextInfo}
@param which: one of the strings startToStart startToEnd endToStart endToEnd
@TYPE WHICH: STRING
"""
		raise NotImplementedError

	def _get_isCollapsed(self):
		return self.compareEndPoints(self,"startToEnd")==0

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

	def move(self,unit,direction,endPoint=None):
		"""Moves one or both of the endpoints of this object by the given unit and direction.
@param unit: the unit to move by
@type unit: string
@param direction: a positive value moves forward by a number of units, a negative value moves back a number of units
@type: int
@param: endPoint: Either None, "start" or "end". If "start" then the start of the range is moved, if "end" then the end of the range is moved, if None - not specified then collapse to start and move both start and end.
"""
		raise NotImplementedError

	def find(self,text,caseSensitive=False,reverse=False):
		"""Locates the given text and positions this TextInfo object at the start.
@param text: the text to search for
@type text: string
@param caceSensitive: true if case sensitivity search should be used, False if not
@type caseSensitive: bool
@param reverse: true then the search will go from current position towards the start of the text, if false then  towards the end.
@type reverse: bool
@returns: True if text is found, false otherwise
@rtype: bool
""" 
		raise NotImplementedError

	def _get_NVDAObjectAtStart(self):
		"""retreaves the NVDAObject related to the start of the range. Usually it is just the owner NVDAObject, but in the case of virtualBuffers it may be a descendant object.
		@returns: the NVDAObject at the start
		"""
		return self.obj

	def _get_pointAtStart(self):
		"""Retrieves x and y coordinates corresponding with the textInfo start. It should return Point"""
		raise NotImplementedError

	def copyToClipboard(self):
		"""Copy the content of this instance to the clipboard.
		@return: C{True} if successful, C{False} otherwise.
		@rtype: bool
		"""
		import api
		return api.copyToClip(convertToCrlf(self.text))

	def getTextInChunks(self, unit):
		"""Retrieve the text of this instance in chunks of a given unit.
		@param unit: The unit at which chunks should be split.
		@return: Chunks of text.
		@rtype: generator of str
		"""
		unitInfo=self.copy()
		unitInfo.collapse()
		while unitInfo.compareEndPoints(self,"startToEnd")<0:
			unitInfo.expand(unit)
			chunkInfo=unitInfo.copy()
			if chunkInfo.compareEndPoints(self,"startToStart")<0:
				chunkInfo.setEndPoint(self,"startToStart")
			if chunkInfo.compareEndPoints(self,"endToEnd")>0:
				chunkInfo.setEndPoint(self,"endToEnd")
			yield chunkInfo.text
			unitInfo.collapse(end=True)

	def getControlFieldSpeech(self, attrs, ancestorAttrs, fieldType, formatConfig=None, extraDetail=False, reason=None):
		return speech.getControlFieldSpeech(attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason)

RE_EOL = re.compile("\r\n|[\n\r]")
def convertToCrlf(text):
	"""Convert a string so that it contains only CRLF line endings.
	@param text: The text to convert.
	@type text: str
	@return: The converted text.
	@rtype: str
	"""
	return RE_EOL.sub("\r\n", text)
