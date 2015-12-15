#textInfos/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2014 NV Access Limited

"""Framework for accessing text content in widgets.
The core component of this framework is the L{TextInfo} class.
In order to access text content for a widget, a L{TextInfo} implementation is required.
A default implementation, L{NVDAObjects.NVDAObjectTextInfo}, is used to enable text review of information about a widget which does not have or support text content.
"""

import weakref
import re
import baseObject
import config
import speech
import controlTypes

class Field(dict):
	"""Provides information about a piece of text."""

class FormatField(Field):
	"""Provides information about the formatting of text; e.g. font information and hyperlinks."""

class ControlField(Field):
	"""Provides information about a control which encompasses text.
	For example, a piece of text might be contained within a table, button, form, etc.
	This field contains information about such a control, such as its role, name and description.
	"""

	#: This field is usually a single line item; e.g. a link or heading.
	PRESCAT_SINGLELINE = "singleLine"
	#: This field is a marker; e.g. a separator or footnote.
	PRESCAT_MARKER = "marker"
	#: This field is a container, usually multi-line.
	PRESCAT_CONTAINER = "container"
	#: This field is a section of a larger container which is adjacent to another similar section;
	#: e.g. a table cell.
	PRESCAT_CELL = "cell"
	#: This field is just for layout.
	PRESCAT_LAYOUT = None

	def getPresentationCategory(self, ancestors, formatConfig, reason=controlTypes.REASON_CARET):
		role = self.get("role", controlTypes.ROLE_UNKNOWN)
		states = self.get("states", set())

		# Honour verbosity configuration.
		if role in (controlTypes.ROLE_TABLE, controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLEROWHEADER, controlTypes.ROLE_TABLECOLUMNHEADER):
			# The user doesn't want layout tables.
			# Find the nearest table.
			if role == controlTypes.ROLE_TABLE:
				# This is the nearest table.
				table = self
			else:
				# Search ancestors for the nearest table.
				for anc in reversed(ancestors):
					if anc.get("role") == controlTypes.ROLE_TABLE:
						table = anc
						break
				else:
					table = None
			if table and ((not formatConfig["includeLayoutTables"] and table.get("table-layout", None)) or table.get('isHidden',False)):
				return self.PRESCAT_LAYOUT
		if reason in (controlTypes.REASON_CARET, controlTypes.REASON_SAYALL, controlTypes.REASON_FOCUS) and (
			(role == controlTypes.ROLE_LINK and not formatConfig["reportLinks"])
			or (role == controlTypes.ROLE_HEADING and not formatConfig["reportHeadings"])
			or (role == controlTypes.ROLE_BLOCKQUOTE and not formatConfig["reportBlockQuotes"])
			or (role in (controlTypes.ROLE_TABLE, controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLEROWHEADER, controlTypes.ROLE_TABLECOLUMNHEADER) and not formatConfig["reportTables"])
			or (role in (controlTypes.ROLE_LIST, controlTypes.ROLE_LISTITEM) and controlTypes.STATE_READONLY in states and not formatConfig["reportLists"])
			or (role in (controlTypes.ROLE_FRAME, controlTypes.ROLE_INTERNALFRAME) and not formatConfig["reportFrames"])
		):
			# This is just layout as far as the user is concerned.
			return self.PRESCAT_LAYOUT

		if (
			role in (controlTypes.ROLE_LINK, controlTypes.ROLE_HEADING, controlTypes.ROLE_BUTTON, controlTypes.ROLE_RADIOBUTTON, controlTypes.ROLE_CHECKBOX, controlTypes.ROLE_GRAPHIC, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_TAB, controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_SLIDER, controlTypes.ROLE_SPINBUTTON, controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_PROGRESSBAR, controlTypes.ROLE_TOGGLEBUTTON, controlTypes.ROLE_MENUBUTTON, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_CHECKMENUITEM, controlTypes.ROLE_RADIOMENUITEM)
			or (role == controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_MULTILINE not in states and (controlTypes.STATE_READONLY not in states or controlTypes.STATE_FOCUSABLE in states))
			or (role == controlTypes.ROLE_LIST and controlTypes.STATE_READONLY not in states)
		):
			return self.PRESCAT_SINGLELINE
		elif role in (controlTypes.ROLE_SEPARATOR, controlTypes.ROLE_FOOTNOTE, controlTypes.ROLE_ENDNOTE, controlTypes.ROLE_EMBEDDEDOBJECT, controlTypes.ROLE_APPLICATION, controlTypes.ROLE_DIALOG, controlTypes.ROLE_MATH):
			return self.PRESCAT_MARKER
		elif role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER):
			return self.PRESCAT_CELL
		elif (
			role in (controlTypes.ROLE_BLOCKQUOTE, controlTypes.ROLE_FRAME, controlTypes.ROLE_INTERNALFRAME, controlTypes.ROLE_TOOLBAR, controlTypes.ROLE_MENUBAR, controlTypes.ROLE_POPUPMENU, controlTypes.ROLE_TABLE)
			or (role == controlTypes.ROLE_EDITABLETEXT and (controlTypes.STATE_READONLY not in states or controlTypes.STATE_FOCUSABLE in states) and controlTypes.STATE_MULTILINE in states)
			or (role == controlTypes.ROLE_LIST and controlTypes.STATE_READONLY in states)
			or (controlTypes.STATE_FOCUSABLE in states and controlTypes.STATE_EDITABLE in states)
		):
			return self.PRESCAT_CONTAINER

		return self.PRESCAT_LAYOUT

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

	def __repr__(self):
		return "FieldCommand %s with %s"%(self.command,self.field)

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

class Rect(object):
	"""Represents a rectangle on the screen."""

	def __init__(self, left, top, right, bottom):
		"""
		@param left: The x coordinate of the upper left corner of the rectangle.
		@type left: int
		@param top: The y coordinate of the upper left corner of the rectangle.
		@type top: int
		@param right: The x coordinate of the lower right corner of the rectangle.
		@type right: int
		@param bottom: The y coordinate of the lower right corner of the rectangle.
		@type bottom: int
		"""
		self.left = left
		self.top = top
		self.right = right
		self.bottom = bottom

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
UNIT_OFFSET="offset"

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
		@return: The text.
		@rtype: unicode
		@note: The text is not guaranteed to be the exact length of the range in offsets.
		"""
		raise NotImplementedError

	def getTextWithFields(self,formatConfig=None):
		"""Retreaves the text in this range, as well as any control/format fields associated therewith.
		Subclasses may override this. The base implementation just returns the text.
		@param formatConfig: Document formatting configuration, useful if you wish to force a particular configuration for a particular task.
		@type formatConfig: dict
		@return: A sequence of text strings interspersed with associated field commands.
		@rtype: list of unicode and L{FieldCommand}
		""" 
		return [self.text]

	def _get_locationText(self):
		"""A message that explains the location of the text position in friendly terms."""
		return None

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
		return self.compareEndPoints(other,"startToStart") == 0 or (self.compareEndPoints(other, "endToStart") > 0 and other.compareEndPoints(self, "endToStart") > 0)

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
		@param unit: the unit to move by; one of the UNIT_* constants.
		@param direction: a positive value moves forward by a number of units, a negative value moves back a number of units
		@type: int
		@param endPoint: Either None, "start" or "end". If "start" then the start of the range is moved, if "end" then the end of the range is moved, if None - not specified then collapse to start and move both start and end.
		@return: The number of units moved;
			negative indicates backward movement, positive indicates forward movement,
			0 means no movement.
		@rtype: int
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

	def _get_clipboardText(self):
		"""Text suitably formatted for copying to the clipboard. E.g. crlf characters inserted between lines."""
		return convertToCrlf(self.text)

	def copyToClipboard(self):
		"""Copy the content of this instance to the clipboard.
		@return: C{True} if successful, C{False} otherwise.
		@rtype: bool
		"""
		import api
		return api.copyToClip(self.clipboardText)

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

	def getControlFieldBraille(self, field, ancestors, reportStart, formatConfig):
		# Import late to avoid circular import.
		import braille
		return braille.getControlFieldBraille(self, field, ancestors, reportStart, formatConfig)

	def activate(self):
		"""Activate this position.
		For example, this might activate the object at this position or click the point at this position.
		@raise NotImplementedError: If not supported.
		"""
		if not self.obj.isInForeground:
			raise NotImplementedError
		import winUser
		p=self.pointAtStart
		oldX,oldY=winUser.getCursorPos()
		winUser.setCursorPos(p.x,p.y)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		winUser.setCursorPos(oldX,oldY)

	def getMathMl(self, field):
		"""Get MathML for a math control field.
		This will only be called for control fields with a role of L{controlTypes.ROLE_MATH}.
		@raise LookupError: If MathML can't be retrieved for this field.
		"""
		raise NotImplementedError

RE_EOL = re.compile("\r\n|[\n\r]")
def convertToCrlf(text):
	"""Convert a string so that it contains only CRLF line endings.
	@param text: The text to convert.
	@type text: str
	@return: The converted text.
	@rtype: str
	"""
	return RE_EOL.sub("\r\n", text)

class DocumentWithPageTurns(baseObject.ScriptableObject):
	"""A document which supports multiple pages of text, but only exposes one page at a time.
	"""

	def turnPage(self, previous=False):
		"""Switch to the next/previous page of text.
		@param previous: C{True} to turn to the previous page, C{False} to turn to the next.
		@type previous: bool
		@raise RuntimeError: If there are no further pages.
		"""
		raise NotImplementedError
