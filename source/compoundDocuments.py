# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2010-2021 NV Access Limited, Bram Duvigneau
from typing import (
	Optional,
	Dict,
)

import textUtils
import winUser
import textInfos
import controlTypes
import eventHandler
from NVDAObjects import NVDAObject
from editableText import EditableText
from treeInterceptorHandler import DocumentTreeInterceptor
import speech
import braille
from NVDAObjects import behaviors
import api
import config
import review
import vision
from logHandler import log
from locationHelper import RectLTWH

class CompoundTextInfo(textInfos.TextInfo):

	def _makeRawTextInfo(self, obj, position):
		return obj.makeTextInfo(position)

	def _normalizeStartAndEnd(self):
		if (self._start.isCollapsed and self._startObj != self._endObj
				and self._start.compareEndPoints(self._makeRawTextInfo(self._startObj, textInfos.POSITION_ALL), "endToEnd") == 0):
			# Start it is at the end of its object.
			# This is equivalent to the start of the next content.
			# Aside from being pointless, we don't want a collapsed start object, as this will cause bogus control fields to be emitted.
			try:
				self._start, self._startObj = self._findNextContent(self._startObj)
			except LookupError:
				pass

		if (self._end.isCollapsed and self._endObj != self._startObj
				and self._end.compareEndPoints(self._makeRawTextInfo(self._endObj, textInfos.POSITION_FIRST), "startToStart") == 0):
			# End is at the start of its object.
			# This is equivalent to the end of the previous content.
			# Aside from being pointless, we don't want a collapsed end object, as this will cause bogus control fields to be emitted.
			try:
				self._end, self._endObj = self._findNextContent(self._endObj, moveBack=True)
				# _end is now on the last character, but we want it collapsed after this.
				self._end.move(textInfos.UNIT_OFFSET, 1, endPoint="end")
				self._end.collapse(end=True)
			except LookupError:
				pass

		if self._startObj == self._endObj:
			# There should only be a single TextInfo and it should cover the entire range.
			self._start.setEndPoint(self._end, "endToEnd")
			self._end = self._start
			self._endObj = self._startObj
		else:
			# start needs to cover the rest of the text to the end of its object.
			self._start.setEndPoint(self._makeRawTextInfo(self._startObj, textInfos.POSITION_ALL), "endToEnd")
			# end needs to cover the rest of the text to the start of its object.
			self._end.setEndPoint(self._makeRawTextInfo(self._endObj, textInfos.POSITION_FIRST), "startToStart")

	def setEndPoint(self, other, which):
		if which == "startToStart":
			self._start = other._start.copy()
			self._startObj = other._startObj
		elif which == "startToEnd":
			self._start = other._end.copy()
			self._start.setEndPoint(other._end, which)
			self._startObj = other._endObj
		elif which == "endToStart":
			self._end = other._start.copy()
			self._end.setEndPoint(other._start, which)
			self._endObj = other._startObj
		elif which == "endToEnd":
			self._end = other._end.copy()
			self._endObj = other._endObj
		else:
			raise ValueError("which=%s" % which)
		self._normalizeStartAndEnd()

	def collapse(self, end=False):
		if end:
			if self._end.compareEndPoints(self._makeRawTextInfo(self._endObj, textInfos.POSITION_ALL), "endToEnd") == 0:
				# The end TextInfo is at the end of its object.
				# The end of this object is equivalent to the start of the next content.
				# As well as being silly, collapsing to the end of  this object causes say all to move the caret to the end of paragraphs.
				# Therefore, collapse to the start of the next content instead.
				try:
					self._end, self._endObj = self._findNextContent(self._endObj)
				except LookupError:
					# There are no more objects, so just collapse to the end of this object.
					self._end.collapse(end=True)
			else:
				# The end TextInfo is not at the end of its object, so just collapse to the end of the end TextInfo.
				self._end.collapse(end=True)
			self._start = self._end
			self._startObj = self._endObj

		else:
			self._start.collapse()
			self._end = self._start
			self._endObj = self._startObj

	def copy(self):
		return self.__class__(self.obj, self)

	def updateCaret(self):
		self._startObj.setFocus()
		self._start.updateCaret()

	def updateSelection(self):
		self._startObj.setFocus()
		self._start.updateSelection()
		if self._end is not self._start:
			self._end.updateSelection()

	def _get_bookmark(self):
		return self.copy()

	def _get_NVDAObjectAtStart(self):
		return self._startObj

	def _get_pointAtStart(self):
		return self._start.pointAtStart

	def _isObjectEditableText(self, obj: NVDAObject) -> bool:
		return obj.role in (
			controlTypes.Role.PARAGRAPH,
			controlTypes.Role.EDITABLETEXT,
		)

	def _isNamedlinkDestination(self, obj: NVDAObject) -> bool:
		return (  # Named link destination, not a link that can be activated.
			obj.role == controlTypes.Role.LINK
			and controlTypes.State.LINKED not in obj.states
		)

	def _getControlFieldForObject(self, obj: NVDAObject, ignoreEditableText=True):
		if ignoreEditableText and self._isObjectEditableText(obj):
			# This is basically just a text node.
			return None
		role = obj.role
		states = obj.states
		if role == controlTypes.Role.LINK and controlTypes.State.LINKED not in states:
			# Named link destination, not a link that can be activated.
			return None
		field = textInfos.ControlField()
		field["role"] = role
		field['roleText'] = obj.roleText
		field['description'] = obj.description
		field['_description-from'] = obj.descriptionFrom
		field['hasDetails'] = obj.hasDetails
		# The user doesn't care about certain states, as they are obvious.
		states.discard(controlTypes.State.EDITABLE)
		states.discard(controlTypes.State.MULTILINE)
		states.discard(controlTypes.State.FOCUSED)
		field["states"] = states
		field["_childcount"] = obj.childCount
		field["level"] = obj.positionInfo.get("level")
		if role == controlTypes.Role.TABLE:
			field["table-id"] = 1 # FIXME
			field["table-rowcount"] = obj.rowCount
			field["table-columncount"] = obj.columnCount
		if role in (controlTypes.Role.TABLECELL, controlTypes.Role.TABLECOLUMNHEADER, controlTypes.Role.TABLEROWHEADER):
			field["table-id"] = 1 # FIXME
			field["table-rownumber"] = obj.rowNumber
			field["table-columnnumber"] = obj.columnNumber
			# Row/column span is not supported by all implementations (e.g. LibreOffice)
			try:
				field['table-rowsspanned']=obj.rowSpan
			except NotImplementedError:
				log.debug("Row span not supported")
				pass
			try:
				field['table-columnsspanned']=obj.columnSpan
			except NotImplementedError:
				log.debug("Column span not supported")
				pass
		return field

	def __eq__(self, other):
		if self is other:
			return True
		if type(self) is not type(other):
			return False
		return self._start == other._start and self._startObj == other._startObj and self._end == other._end and self._endObj == other._endObj

	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	# The default hash implementation is fine for  our purposes.
	def __hash__(self):
		return super().__hash__()

	def __ne__(self, other):
		return not self == other

class TreeCompoundTextInfo(CompoundTextInfo):
	#: Units contained within a single TextInfo.
	SINGLE_TEXTINFO_UNITS = (textInfos.UNIT_CHARACTER, textInfos.UNIT_WORD, textInfos.UNIT_LINE, textInfos.UNIT_SENTENCE, textInfos.UNIT_PARAGRAPH)

	def __init__(self, obj, position):
		super(TreeCompoundTextInfo, self).__init__(obj, position)
		rootObj = obj.rootNVDAObject
		if isinstance(position, NVDAObject):
			# FIXME
			position = textInfos.POSITION_CARET
		if isinstance(position, self.__class__):
			self._start = position._start.copy()
			self._startObj = position._startObj
			if position._end is position._start:
				self._end = self._start
			else:
				self._end = position._end.copy()
			self._endObj = position._endObj
		elif position == textInfos.POSITION_FIRST:
			self._startObj = self._endObj = self._findContentDescendant(rootObj.firstChild)
			self._start = self._end = self._startObj.makeTextInfo(position)
		elif position == textInfos.POSITION_LAST:
			self._startObj = self._endObj = self._findContentDescendant(rootObj.lastChild)
			self._start = self._end = self._startObj.makeTextInfo(position)
		elif position == textInfos.POSITION_ALL:
			self._startObj = self._findContentDescendant(rootObj.firstChild)
			self._endObj = self._findContentDescendant(rootObj.lastChild)
			self._start = self._startObj.makeTextInfo(position)
			self._end = self._endObj.makeTextInfo(position)
		elif position == textInfos.POSITION_CARET:
			self._startObj = self._endObj = obj.caretObject
			self._start = self._end = self._startObj.makeTextInfo(position)
		elif position == textInfos.POSITION_SELECTION:
			# Start from the caret.
			self._startObj = self._endObj = self.obj.caretObject
			# Find the objects which start and end the selection.
			tempObj = self._startObj
			while tempObj and controlTypes.State.SELECTED in tempObj.states:
				self._startObj = tempObj
				tempObj = tempObj.flowsFrom
			tempObj = self._endObj
			while tempObj and controlTypes.State.SELECTED in tempObj.states:
				self._endObj = tempObj
				tempObj = tempObj.flowsTo
			self._start = self._startObj.makeTextInfo(position)
			if self._startObj is self._endObj:
				self._end = self._start
			else:
				self._end = self._endObj.makeTextInfo(position)
		else:
			raise NotImplementedError

	def _findContentDescendant(self, obj):
		while obj and controlTypes.State.FOCUSABLE not in obj.states:
			obj = obj.firstChild
		return obj

	def _getTextInfos(self):
		yield self._start
		if self._startObj == self._endObj:
			return
		obj = self._startObj.flowsTo
		while obj and obj != self._endObj:
			yield obj.makeTextInfo(textInfos.POSITION_ALL)
			obj = obj.flowsTo
		yield self._end

	def _get_text(self):
		return "".join(ti.text for ti in self._getTextInfos())

	def _getFirstEmbedIndex(self, info):
		if info._startOffset == 0:
			return 0
		# Get the number of embeds before the start.
		# The index is 0 based, so this is the index of the first embed after start.
		text = info._getTextRange(0, info._startOffset)
		return text.count(textUtils.OBJ_REPLACEMENT_CHAR)

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.TextInfo.TextWithFieldsT:
		# Get the initial control fields.
		fields = []
		rootObj = self.obj.rootNVDAObject
		obj = self._startObj
		while obj and obj != rootObj:
			field = self._getControlFieldForObject(obj)
			if field:
				fields.insert(0, textInfos.FieldCommand("controlStart", field))
			obj = obj.parent

		embedIndex = None
		for ti in self._getTextInfos():
			for textWithEmbeddedObjectsItem in ti._iterTextWithEmbeddedObjects(True, formatConfig=formatConfig):
				if isinstance(textWithEmbeddedObjectsItem, int):  # Embedded object
					if embedIndex is None:
						embedIndex = self._getFirstEmbedIndex(ti)
					else:
						embedIndex += 1
					childObject: NVDAObject = ti.obj.getChild(embedIndex)
					controlField = self._getControlFieldForObject(childObject, ignoreEditableText=False)
					controlField["content"] = childObject.name
					fields.extend((
						textInfos.FieldCommand("controlStart", controlField),
						textUtils.OBJ_REPLACEMENT_CHAR,
						textInfos.FieldCommand("controlEnd", None)
					))
				else:  # str or fieldCommand
					if not isinstance(textWithEmbeddedObjectsItem, (str, textInfos.FieldCommand)):
						log.error(f"Unexpected type: {textWithEmbeddedObjectsItem!r}")
					fields.append(textWithEmbeddedObjectsItem)
		return fields

	def _findNextContent(self, origin, moveBack=False):
		obj = origin.flowsFrom if moveBack else origin.flowsTo
		if not obj:
			raise LookupError
		ti = obj.makeTextInfo(textInfos.POSITION_LAST if moveBack else textInfos.POSITION_FIRST)
		return ti, obj

	def _getObjectPosition(self, obj):
		indexes = []
		rootObj = self.obj.rootNVDAObject
		while obj and obj != rootObj:
			indexes.insert(0, obj.indexInParent)
			obj = obj.parent
		return indexes

	def compareEndPoints(self, other, which):
		if which in ("startToStart", "startToEnd"):
			selfTi = self._start
			selfObj = self._startObj
		else:
			selfTi = self._end
			selfObj = self._endObj
		if which in ("startToStart", "endToStart"):
			otherTi = other._start
			otherObj = other._startObj
		else:
			otherTi = other._end
			otherObj = other._endObj

		if selfObj == otherObj:
			# Same object, so just compare the two TextInfos normally.
			return selfTi.compareEndPoints(otherTi, which)

		# Different objects, so we have to compare the hierarchical positions of the objects.
		# cmp no longer exists in Python3.
	# Per the Python3 What's New docs:
	# cmp can be replaced with (a>b)-(a<b).
	# In other words, False and True coerce to 0 and 1 respectively.
		selfPosition=self._getObjectPosition(selfObj)
		otherPosition=other._getObjectPosition(otherObj)
		return (selfPosition>otherPosition)-(selfPosition<otherPosition)

	def expand(self, unit):
		if unit == textInfos.UNIT_READINGCHUNK:
			unit = textInfos.UNIT_LINE

		if unit in self.SINGLE_TEXTINFO_UNITS:
			# This unit is definitely contained within a single chunk.
			self._start.expand(unit)
			self._end = self._start
			self._endObj = self._startObj
		else:
			raise NotImplementedError

	def move(self, unit, direction, endPoint=None):
		if direction == 0:
			return 0

		if unit == textInfos.UNIT_READINGCHUNK:
			unit = textInfos.UNIT_LINE

		if unit not in self.SINGLE_TEXTINFO_UNITS:
			raise NotImplementedError

		if not endPoint or endPoint == "start":
			moveTi = self._start
			moveObj = self._startObj
		elif endPoint == "end":
			moveTi = self._end
			moveObj = self._endObj

		goPrevious = direction < 0
		remainingMovement = direction
		count0MoveAs = 0
		while True:
			movement = moveTi.move(unit, remainingMovement, endPoint=endPoint)
			if movement == 0 and count0MoveAs != 0:
				movement = count0MoveAs
			remainingMovement -= movement
			count0MoveAs = 0
			if remainingMovement == 0:
				# The requested destination was within moveTi.
				break

			# The requested destination is not in this object, so move to the next.
			tempObj = moveObj.flowsFrom if goPrevious else moveObj.flowsTo
			if tempObj:
				moveObj = tempObj
			else:
				break
			if goPrevious:
				moveTi = moveObj.makeTextInfo(textInfos.POSITION_ALL)
				moveTi.collapse(end=True)
				# We haven't moved anywhere yet, as the end of this object (where we are now) is equivalent to the start of the one we just left.
				# Blank objects should still count as 1 step.
				# Therefore, the next move must count as 1 even if it is 0.
				count0MoveAs = -1
			else:
				moveTi = moveObj.makeTextInfo(textInfos.POSITION_FIRST)
				if endPoint == "end":
					# If we're moving the end, the previous move would have taken us to the end of the previous object,
					# which is equivalent to the start of this object (where we are now).
					# Therefore, moving to this new object shouldn't be counted as a move.
					# However, ensure that blank objects will still be counted as 1 step.
					count0MoveAs = 1
				else:
					# We've moved to the start of the next unit.
					remainingMovement -= 1
					if remainingMovement == 0:
						# We just hit the requested destination.
						break

		if not endPoint or endPoint == "start":
			self._start = moveTi
			self._startObj = moveObj
		if not endPoint or endPoint == "end":
			self._end = moveTi
			self._endObj = moveObj
		self._normalizeStartAndEnd()

		return direction - remainingMovement

	def _get_boundingRects(self):
		rects = []
		for ti in self._getTextInfos():
			if ti.obj.hasIrrelevantLocation:
				continue
			try:
				rects.extend(ti.boundingRects)
			except LookupError:
				continue
		return rects

class CompoundDocument(EditableText, DocumentTreeInterceptor):
	TextInfo = TreeCompoundTextInfo

	def __init__(self, rootNVDAObject):
		super(CompoundDocument, self).__init__(rootNVDAObject)

	def _get_isAlive(self):
		root = self.rootNVDAObject
		return winUser.isWindow(root.windowHandle)

	def __contains__(self, obj):
		root = self.rootNVDAObject
		while obj:
			if obj.windowHandle != root.windowHandle:
				return False
			if obj == root:
				return True
			obj = obj.parent
		return False

	def _get_caretObject(self):
		return eventHandler.lastQueuedFocusObject

	def event_treeInterceptor_gainFocus(self):
		speech.speakObject(self.rootNVDAObject, reason=controlTypes.OutputReason.FOCUS)
		try:
			info = self.makeTextInfo(textInfos.POSITION_SELECTION)
		except RuntimeError:
			pass
		else:
			if info.isCollapsed:
				info.expand(textInfos.UNIT_LINE)
				speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
			else:
				speech.speakPreselectedText(info.text)
			braille.handler.handleGainFocus(self)
			self.initAutoSelectDetection()

	def event_caret(self, obj, nextHandler):
		self.detectPossibleSelectionChange()
		braille.handler.handleCaretMove(self)
		vision.handler.handleCaretMove(self)
		caret = self.makeTextInfo(textInfos.POSITION_CARET)
		review.handleCaretMove(caret)

	def event_gainFocus(self, obj, nextHandler):
		if not isinstance(obj, behaviors.EditableText):
			# This object isn't part of the editable text; e.g. a graphic.
			# Report it normally.
			nextHandler()

	def event_focusEntered(self, obj, nextHandler):
		pass

	def event_stateChange(self, obj, nextHandler):
		pass

	def event_selection(self, obj, nextHandler):
		pass

	def event_selectionAdd(self, obj, nextHandler):
		pass

	def event_selectionRemove(self, obj, nextHandler):
		pass
