#textInfos/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import weakref
import re
import baseObject
import config
import speech

"""Framework for accessing text content in widgets.
The core component of this framework is the L{TextInfo} class.
In order to access text content for a widget, a L{TextInfo} implementation is required.
A default implementation, L{NVDAObjects.NVDAObjectTextInfo}, is used to enable text review of information about a widget which does not have or support text content.
"""

class Field(dict):
	"""Provides information about a piece of text."""

class FormatField(Field):
	"""Provides information about the formatting of text; e.g. font information and hyperlinks."""

class ControlField(Field):
	"""Provides information about a control which encompasses text.
	For example, a piece of text might be contained within a table, button, form, etc.
	This field contains information about such a control, such as its role, name and description.
	"""

class FieldCommand(object):
	"""A command indicating a L{Field} in a sequence of text and fields.
	When retrieving text with its associated fields, a L{TextInfo} provides a sequence of text strings and L{FieldCommand}s.
	A command indicates the start or end of a control or that the formatting of the text has changed.
	"""

	def __init__(self,command,field):
		"""Constructor.
		@param command: The command; one of:
			"controlStart", indicating the start of a L{ControlField};
			"controlEnd", indicating the end of a L{ControlField}; or
			"formatChange", indicating a L{FormatField} change.
		@param field: The field associated with this command; may be C{None} for controlEnd.
		@type field: L{Field}
		"""
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
	"""Represents a point on the screen.
	This is used when associating a point on the screen with a piece of text.
	"""

	def __init__(self,x,y):
		"""
		@param x: the x coordinate
		@type x: int
		@param y: The y coordinate
		@type y: int
		"""
		self.x=x
		self.y=y

class Points(object):
	"""Represents two points on the screen."""

	def __init__(self,startX,startY,endX,endY):
		"""
		@param startX: the x coordinate of the first point.
		@type startX: int
		@param startY: The y coordinate of the first point.
		@type startY: int
		@param endX: the x coordinate of the second point.
		@type endX: int
		@param endY: the y coordinate of the second point.
		@type endY: int
		"""
		self.startX=startX
		self.startY=startY
		self.endX=endX
		self.endY=endY

class Bookmark(baseObject.AutoPropertyObject):
	"""Represents a static absolute position in some text.
	This is used to construct a L{TextInfo} at an exact previously obtained position.
	"""

	def __init__(self,infoClass,data):
		"""
		@param infoClass: The class of the L{TextInfo} object.
		@type infoClass: type; subclass of L{TextInfo}
		@param data: Data that can be used to reconstruct the position the textInfo object was in when it generated the bookmark.
		"""
		#: The class of the L{TextInfo} object.
		#: @type: type; subclass of L{TextInfo}
		self.infoClass=infoClass
		#: Data that can be used to reconstruct the position the textInfo object was in when it generated the bookmark.
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
	"""Provides information about a range of text in an object and facilitates access to all text in the widget.
	A TextInfo represents a specific range of text, providing access to the text itself, as well as information about the text such as its formatting and any associated controls.
	This range can be moved within the object's text relative to the initial position.
	
	At a minimum, subclasses must:
		* Extend the constructor so that it can set up the range at the specified position.
		* Implement the L{move}, L{expand}, L{compareEndPoints}, L{setEndPoint} and L{copy} methods.
		* Implement the L{text} and L{bookmark} attributes.
		* Support at least the L{UNIT_CHARACTER}, L{UNIT_WORD} and L{UNIT_LINE} units.
		* Support at least the L{POSITION_FIRST}, L{POSITION_LAST} and L{POSITION_ALL} positions.
	If an implementation should support tracking with the mouse,
	L{Points} must be supported as a position.
	To support routing to a screen point from a given position, L{pointAtStart} must be implemented.
	In order to support text formatting or control information, L{getTextWithFields} should be overridden.
	
	@ivar bookmark: A unique identifier that can be used to make another textInfo object at this position.
	@type bookmark: L{Bookmark}
	"""
 
	def __init__(self,obj,position):
		"""Constructor.
		Subclasses must extend this, calling the superclass method first.
		@param position: The initial position of this range; one of the POSITION_* constants or a position object supported by the implementation.
		@type position: int, tuple or string
		@param obj: The object containing the range of text being represented.
		"""
		super(TextInfo,self).__init__()
		self._obj=weakref.ref(obj) if type(obj)!=weakref.ProxyType else obj
		#: The position with which this instance was constructed.
		self.basePosition=position

	def _get_obj(self):
		"""The object containing the range of text being represented."""
		return self._obj()

	def _get_unit_mouseChunk(self):
		return config.conf["mouse"]["mouseTextUnit"]

	def _get_text(self):
		"""The text with in this range.
		Subclasses must implement this.
		@note: The text is not guaranteed to be the exact length of the range in offsets.
		"""
		raise NotImplementedError

	def getTextWithFields(self,formatConfig=None):
		"""Retreaves the text in this range, as well as any control/format fields associated therewith.
		Subclasses may override this. The base implementation just returns the text.
		@param formatConfig: Document formatting configuration, useful if you wish to force a particular configuration for a particular task.
		@type formatConfig: dict
		@return: A sequence of text strings interspersed with associated field commands.
		@rtype: list of str and L{FieldCommand}
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
		""" compares one end of this range to one end of another range.
		Subclasses must implement this.
		@param other: the text range to compare with.
		@type other: L{TextInfo}
		@param which: The ends to compare; one of "startToStart", "startToEnd", "endToStart", "endToEnd".
		@return: -1 if this end is before other end, 1 if this end is after other end or 0 if this end and other end are the same. 
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
		"""Sets one end of this range to one end of another range.
		Subclasses must implement this.
		@param other: The range from which an end is being obtained.
		@type other: L{TextInfo}
		@param which: The ends to use; one of "startToStart", "startToEnd", "endToStart", "endToEnd".
		"""
		raise NotImplementedError

	def _get_isCollapsed(self):
		"""
		@return: C{True} if representing a collapsed range, C{False} if the range is expanded to cover one or more characters.
		@rtype: bool
		"""
		return self.compareEndPoints(self,"startToEnd")==0

	def expand(self,unit):
		"""Expands the start and end of this text info object to a given unit
@param unit: a unit constant
@type unit: string
"""
		raise NotImplementedError

	def collapse(self, end=False):
		"""Collapses this text info object so that both endpoints are the same.
		@param end: Whether to collapse to the end; C{True} to collapse to the end, C{False} to collapse to the start.
		@type end: bool
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
