# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Babbage B.V., Accessolutions, Julien Cochuyt

"""Framework for accessing text content in widgets.
The core component of this framework is the L{TextInfo} class.
In order to access text content for a widget, a L{TextInfo} implementation is required.
A default implementation, L{NVDAObjects.NVDAObjectTextInfo}, is used to enable text review of information about a widget which does not have or support text content.
"""

from abc import abstractmethod
from enum import Enum
import weakref
import re
import typing
from typing import (
	Any,
	Union,
	List,
	Optional,
	Dict,
	Tuple,
)

import baseObject
import config
import controlTypes
from controlTypes import OutputReason
import locationHelper
from logHandler import log

if typing.TYPE_CHECKING:
	import NVDAObjects

SpeechSequence = List[Union[Any, str]]

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

	def getPresentationCategory(
			self,
			ancestors,
			formatConfig,
			reason=OutputReason.CARET,
			extraDetail=False
	):
		role = self.get("role", controlTypes.Role.UNKNOWN)
		states = self.get("states", set())

		# Honour verbosity configuration.
		if role in (controlTypes.Role.TABLE, controlTypes.Role.TABLECELL, controlTypes.Role.TABLEROWHEADER, controlTypes.Role.TABLECOLUMNHEADER):
			# The user doesn't want layout tables.
			# Find the nearest table.
			if role == controlTypes.Role.TABLE:
				# This is the nearest table.
				table = self
			else:
				# Search ancestors for the nearest table.
				for anc in reversed(ancestors):
					if anc.get("role") == controlTypes.Role.TABLE:
						table = anc
						break
				else:
					table = None
			if not table or (not formatConfig["includeLayoutTables"] and table.get("table-layout", None)) or table.get('isHidden',False):
				return self.PRESCAT_LAYOUT

		name = self.get("name")
		landmark = self.get("landmark")
		if reason in (OutputReason.CARET, OutputReason.SAYALL, OutputReason.FOCUS, OutputReason.QUICKNAV) and (
			(role == controlTypes.Role.LINK and not formatConfig["reportLinks"])
			or (role == controlTypes.Role.GRAPHIC and not formatConfig["reportGraphics"])
			or (role == controlTypes.Role.HEADING and not formatConfig["reportHeadings"])
			or (role == controlTypes.Role.BLOCKQUOTE and not formatConfig["reportBlockQuotes"])
			or (role == controlTypes.Role.GROUPING and (not name or not formatConfig["reportGroupings"]))
			or (role in (controlTypes.Role.TABLE, controlTypes.Role.TABLECELL, controlTypes.Role.TABLEROWHEADER, controlTypes.Role.TABLECOLUMNHEADER) and not formatConfig["reportTables"])
			or (role in (controlTypes.Role.LIST, controlTypes.Role.LISTITEM) and controlTypes.State.READONLY in states and not formatConfig["reportLists"])
			or (role == controlTypes.Role.ARTICLE and not formatConfig["reportArticles"])
			or (role == controlTypes.Role.MARKED_CONTENT and not formatConfig["reportHighlight"])
			or (role in (controlTypes.Role.FRAME, controlTypes.Role.INTERNALFRAME) and not formatConfig["reportFrames"])
			or (role in (controlTypes.Role.DELETED_CONTENT,controlTypes.Role.INSERTED_CONTENT) and not formatConfig["reportRevisions"])
			or (
				(role == controlTypes.Role.LANDMARK or landmark)
				and not formatConfig["reportLandmarks"]
			)
			or (role == controlTypes.Role.REGION and (not name or not formatConfig["reportLandmarks"]))
		):
			# This is just layout as far as the user is concerned.
			return self.PRESCAT_LAYOUT

		if (
			role in (
				controlTypes.Role.DELETED_CONTENT,
				controlTypes.Role.INSERTED_CONTENT,
				controlTypes.Role.LINK, 
				controlTypes.Role.HEADING, 
				controlTypes.Role.BUTTON, 
				controlTypes.Role.RADIOBUTTON, 
				controlTypes.Role.CHECKBOX, 
				controlTypes.Role.GRAPHIC, 
				controlTypes.Role.CHART, 
				controlTypes.Role.MENUITEM, 
				controlTypes.Role.TAB, 
				controlTypes.Role.COMBOBOX, 
				controlTypes.Role.SLIDER, 
				controlTypes.Role.SPINBUTTON, 
				controlTypes.Role.PROGRESSBAR,
				controlTypes.Role.BUSY_INDICATOR,
				controlTypes.Role.TOGGLEBUTTON, 
				controlTypes.Role.MENUBUTTON, 
				controlTypes.Role.TREEVIEW, 
				controlTypes.Role.CHECKMENUITEM, 
				controlTypes.Role.RADIOMENUITEM,
				controlTypes.Role.CAPTION,
			)
			or (role == controlTypes.Role.EDITABLETEXT and controlTypes.State.MULTILINE not in states and (controlTypes.State.READONLY not in states or controlTypes.State.FOCUSABLE in states))
			or (role == controlTypes.Role.LIST and controlTypes.State.READONLY not in states)
		):
			return self.PRESCAT_SINGLELINE
		elif (
			role in (
				controlTypes.Role.SEPARATOR,
				controlTypes.Role.FOOTNOTE,
				controlTypes.Role.ENDNOTE,
				controlTypes.Role.EMBEDDEDOBJECT,
				controlTypes.Role.MATH
			)
			or (
				extraDetail and role == controlTypes.Role.LISTITEM
			)
		):
			return self.PRESCAT_MARKER
		elif role in (controlTypes.Role.APPLICATION, controlTypes.Role.DIALOG):
			# Applications and dialogs should be reported as markers when embedded within content, but not when they themselves are the root
			return self.PRESCAT_MARKER if ancestors else self.PRESCAT_LAYOUT 
		elif role in (controlTypes.Role.TABLECELL, controlTypes.Role.TABLECOLUMNHEADER, controlTypes.Role.TABLEROWHEADER):
			return self.PRESCAT_CELL
		elif (
			role in (
				controlTypes.Role.BLOCKQUOTE,
				controlTypes.Role.GROUPING,
				controlTypes.Role.FIGURE,
				controlTypes.Role.REGION,
				controlTypes.Role.FRAME,
				controlTypes.Role.INTERNALFRAME,
				controlTypes.Role.TOOLBAR,
				controlTypes.Role.MENUBAR,
				controlTypes.Role.POPUPMENU,
				controlTypes.Role.TABLE,
				controlTypes.Role.ARTICLE,
				controlTypes.Role.MARKED_CONTENT,
			)
			or (role == controlTypes.Role.EDITABLETEXT and (
				controlTypes.State.READONLY not in states
				or controlTypes.State.FOCUSABLE in states
			) and controlTypes.State.MULTILINE in states)
			or (role == controlTypes.Role.LIST and controlTypes.State.READONLY in states)
			or (role == controlTypes.Role.LANDMARK or landmark)
			or (controlTypes.State.FOCUSABLE in states and controlTypes.State.EDITABLE in states)
		):
			return self.PRESCAT_CONTAINER

		# If the author has provided specific role text, then this should be presented either as container or singleLine depending on whether the field is block or not. 
		if self.get('roleText'):
			if self.get('isBlock'):
				return self.PRESCAT_CONTAINER
			else:
				return self.PRESCAT_SINGLELINE

		return self.PRESCAT_LAYOUT

class FieldCommand(object):
	"""A command indicating a L{Field} in a sequence of text and fields.
	When retrieving text with its associated fields, a L{TextInfo} provides a sequence of text strings and L{FieldCommand}s.
	A command indicates the start or end of a control or that the formatting of the text has changed.
	"""

	def __init__(self, command: str, field: Optional[Union[ControlField, FormatField]]):
		"""Constructor.
		@param command: The command; one of:
			"controlStart", indicating the start of a L{ControlField};
			"controlEnd", indicating the end of a L{ControlField}; or
			"formatChange", indicating a L{FormatField} change.
		@param field: The field associated with this command; may be C{None} for controlEnd.
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

	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	# The default hash implementation is fine for  our purposes.
	def __hash__(self):
		return super().__hash__()

	def __ne__(self,other):
		return not self==other


#Unit constants
UNIT_CHARACTER = "character"
UNIT_WORD = "word"
UNIT_LINE = "line"
UNIT_SENTENCE = "sentence"
UNIT_PARAGRAPH = "paragraph"
UNIT_PAGE = "page"
UNIT_TABLE = "table"
UNIT_ROW = "row"
UNIT_COLUMN = "column"
UNIT_CELL = "cell"
UNIT_SCREEN = "screen"
UNIT_STORY = "story"
UNIT_READINGCHUNK = "readingChunk"
UNIT_OFFSET = "offset"
UNIT_CONTROLFIELD = "controlField"
UNIT_FORMATFIELD = "formatField"

MOUSE_TEXT_RESOLUTION_UNITS = (UNIT_CHARACTER,UNIT_WORD,UNIT_LINE,UNIT_PARAGRAPH)

unitLabels={
	UNIT_CHARACTER:_("character"),
	UNIT_WORD:_("word"),
	UNIT_LINE:_("line"),
	UNIT_PARAGRAPH:_("paragraph"),
}


def _logBadSequenceTypes(sequence: SpeechSequence, shouldRaise: bool = True):
	import speech.types
	return speech.types.logBadSequenceTypes(sequence, raiseExceptionOnError=shouldRaise)


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
	To support routing to a screen point from a given position, L{pointAtStart} or L{boundingRects} must be implemented.
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

	#: Typing information for auto-property: start
	start: "TextInfoEndpoint"

	def _get_start(self) -> "TextInfoEndpoint":
		return TextInfoEndpoint(self, True)

	def _set_start(self, otherEndpoint: "TextInfoEndpoint"):
		self.start.moveTo(otherEndpoint)

	#: Typing information for auto-property: end
	end: "TextInfoEndpoint"

	def _get_end(self) -> "TextInfoEndpoint":
		return TextInfoEndpoint(self, False)

	def _set_end(self, otherEndpoint: "TextInfoEndpoint"):
		self.end.moveTo(otherEndpoint)

	#: Typing information for auto-property: _get_obj
	obj: "NVDAObjects.NVDAObject"

	def _get_obj(self) -> "NVDAObjects.NVDAObject":
		"""The object containing the range of text being represented."""
		return self._obj()

	def _get_unit_mouseChunk(self):
		return config.conf["mouse"]["mouseTextUnit"]

	#: Typing information for auto-property: _get_text
	text: str

	_abstract_text = True

	def _get_text(self) -> str:
		"""The text with in this range.
		Subclasses must implement this.
		@return: The text.
		@note: The text is not guaranteed to be the exact length of the range in offsets.
		"""
		raise NotImplementedError

	TextWithFieldsT = List[Union[str, FieldCommand]]

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> "TextInfo.TextWithFieldsT":
		"""Retrieves the text in this range, as well as any control/format fields associated therewith.
		Subclasses may override this. The base implementation just returns the text.
		@param formatConfig: Document formatting configuration, useful if you wish to force a particular
			configuration for a particular task.
		@return: A sequence of text strings interspersed with associated field commands.
		""" 
		return [self.text]

	def _get_locationText(self):
		"""A message that explains the location of the text position in friendly terms."""
		try:
			curPoint = self.pointAtStart
		except (NotImplementedError, LookupError):
			return None
		# Translators: the current position's screen coordinates in pixels
		return _("Positioned at {x}, {y}").format(x=curPoint.x,y=curPoint.y)

	def _get_boundingRects(self):
		"""Per line bounding rectangles for the visible text in this range.
		Implementations should ensure that the bounding rectangles don't contain off screen coordinates.
		@rtype: [L{locationHelper.RectLTWH}]
		@raise NotImplementedError: If not supported.
		@raise LookupError: If not available (i.e. off screen, hidden, etc.)
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

	@abstractmethod
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

	@abstractmethod
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

	@abstractmethod
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

	@abstractmethod
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

	_abstract_bookmark = True
	def _get_bookmark(self):
		raise NotImplementedError

	@abstractmethod
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

	#: Typing information for auto-property: _get_NVDAObjectAtStart
	NVDAObjectAtStart: "NVDAObjects.NVDAObject"

	def _get_NVDAObjectAtStart(self) -> "NVDAObjects.NVDAObject":
		"""Get the NVDAObject related to the start of the range.
		Usually it is just the owner NVDAObject, but in the case of virtualBuffers it may be a descendant object.
		@returns: the NVDAObject at the start
		"""
		return self.obj

	def _get_focusableNVDAObjectAtStart(self):
		"""retreaves the deepest focusable NVDAObject related to the start of the range. Usually it is just the owner NVDAObject, but in the case of virtualBuffers it may be a descendant object.
		@returns: the NVDAObject at the start
		"""
		return self.obj

	def _get_pointAtStart(self):
		"""Retrieves x and y coordinates corresponding with the textInfo start. It should return Point.
		The base implementation uses L{boundingRects}.
		@rtype: L{locationHelper.Point}
		"""
		if self.isCollapsed:
			copy = self.copy()
			# Expand the copy to character.
			copy.expand(UNIT_CHARACTER)
			boundingRects = copy.boundingRects
		else:
			boundingRects = self.boundingRects
		if not boundingRects:
			raise LookupError
		return boundingRects[0].topLeft

	def _get_clipboardText(self):
		"""Text suitably formatted for copying to the clipboard. E.g. crlf characters inserted between lines."""
		return convertToCrlf(self.text)

	def copyToClipboard(self, notify=False):
		"""Copy the content of this instance to the clipboard.
		@return: C{True} if successful, C{False} otherwise.
		@rtype: bool
		@param notify: whether to emit a confirmation message
		@type notify: boolean
		"""
		import api
		return api.copyToClip(self.clipboardText, notify)

	def getTextInChunks(self, unit):
		"""Retrieve the text of this instance in chunks of a given unit.
		@param unit: The unit at which chunks should be split.
		@return: Chunks of text.
		@rtype: generator of str
		"""
		unitInfo=self.copy()
		unitInfo.collapse()
		while unitInfo.start < self.end:
			unitInfo.expand(unit)
			chunkInfo=unitInfo.copy()
			if chunkInfo.start < self.start:
				chunkInfo.start = self.start
			if chunkInfo.end > self.end:
				chunkInfo.end = self.end
			yield chunkInfo.text
			unitInfo.collapse(end=True)
			if unitInfo.start < chunkInfo.end:
				log.debugWarning("Could not move TextInfo completely to end, breaking")
				break

	def getControlFieldSpeech(
			self,
			attrs: ControlField,
			ancestorAttrs: List[Field],
			fieldType: str,
			formatConfig: Optional[Dict[str, bool]] = None,
			extraDetail: bool = False,
			reason: Optional[OutputReason] = None
	) -> SpeechSequence:
		# Import late to avoid circular import.
		import speech
		sequence = speech.getControlFieldSpeech(
			attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason
		)
		_logBadSequenceTypes(sequence)
		return sequence

	def getControlFieldBraille(self, field, ancestors, reportStart, formatConfig):
		# Import late to avoid circular import.
		import braille
		return braille.getControlFieldBraille(self, field, ancestors, reportStart, formatConfig)

	def getFormatFieldSpeech(
			self,
			attrs: Field,
			attrsCache: Optional[Field] = None,
			formatConfig: Optional[Dict[str, bool]] = None,
			reason: Optional[OutputReason] = None,
			unit: Optional[str] = None,
			extraDetail: bool = False,
			initialFormat: bool = False,
	) -> SpeechSequence:
		"""Get the spoken representation for given format information.
		The base implementation just calls L{speech.getFormatFieldSpeech}.
		This can be extended in order to support implementation specific attributes.
		If extended, the superclass should be called first.
		"""
		# Import late to avoid circular import.
		import speech
		return speech.getFormatFieldSpeech(
			attrs=attrs,
			attrsCache=attrsCache,
			formatConfig=formatConfig,
			reason=reason,
			unit=unit,
			extraDetail=extraDetail,
			initialFormat=initialFormat
		)

	def activate(self):
		"""Activate this position.
		For example, this might activate the object at this position or click the point at this position.
		@raise NotImplementedError: If not supported.
		"""
		if not self.obj.isInForeground:
			raise NotImplementedError
		import mouseHandler
		import winUser
		p=self.pointAtStart
		oldX,oldY=winUser.getCursorPos()
		winUser.setCursorPos(p.x,p.y)
		mouseHandler.doPrimaryClick()
		winUser.setCursorPos(oldX,oldY)

	def getMathMl(self, field):
		"""Get MathML for a math control field.
		This will only be called for control fields with a role of L{controlTypes.Role.MATH}.
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


class TextInfoEndpoint:
	"""
	Represents one end of a TextInfo instance.
	This object can be compared with another end from the same or a different TextInfo instance,
	Using the standard math comparison operators:
	< <= == != >= >
	"""

	_whichMap: Dict[Tuple[bool, bool], str] = {
		(True, True): "startToStart",
		(True, False): "startToEnd",
		(False, True): "endToStart",
		(False, False): "endToEnd",
	}

	def _cmp(self, other: "TextInfoEndpoint") -> int:
		"""
		A standard cmp function returning:
		-1 for less than, 0 for equal and 1 for greater than.
		"""
		if (
			not isinstance(other, TextInfoEndpoint)
			or not isinstance(other.textInfo, type(self.textInfo))
		):
			raise ValueError(f"Cannot compare endpoint with different type: {other}")
		return self.textInfo.compareEndPoints(other.textInfo, self._whichMap[self.isStart, other.isStart])

	def __init__(
			self,
			textInfo: TextInfo,
			isStart: bool
	):
		"""
		@param textInfo: the TextInfo instance you wish to represent an endpoint of.
		@param isStart: true to represent the start, false for the end.
		"""
		self.textInfo = textInfo
		self.isStart = isStart

	def __lt__(self, other) -> bool:
		return self._cmp(other) < 0

	def __le__(self, other) -> bool:
		return self._cmp(other) <= 0

	def __eq__(self, other) -> bool:
		return self._cmp(other) == 0

	def __ne__(self, other) -> bool:
		return self._cmp(other) != 0

	def __ge__(self, other) -> bool:
		return self._cmp(other) >= 0

	def __gt__(self, other) -> bool:
		return self._cmp(other) > 0

	def moveTo(self, other: "TextInfoEndpoint") -> None:
		"""
		Moves the end of the TextInfo this endpoint represents to the position of the given endpoint.
		"""
		if (
			not isinstance(other, TextInfoEndpoint)
			or not isinstance(other.textInfo, type(self.textInfo))
		):
			raise ValueError(f"Cannot move endpoint to different type: {other}")
		self.textInfo.setEndPoint(other.textInfo, self._whichMap[(self.isStart, other.isStart)])

	def __repr__(self):
		endpointLabel = "start" if self.isStart else "end"
		return f"{endpointLabel} endpoint of {self.textInfo}"


class CommentType(Enum):
	"""
	a value exposed by the 'comment' key of a L{Formatfield}.
	"""
	GENERAL = "general"
	DRAFT = "draft"
	RESOLVED = "resolved"
