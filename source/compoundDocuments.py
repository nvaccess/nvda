#compoundDocuments.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2013 NV Access Limited

import itertools
import winUser
import textInfos
import controlTypes
import eventHandler
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
from editableText import EditableText
from treeInterceptorHandler import TreeInterceptor
import speech
import braille
from NVDAObjects import behaviors
import api
import config
import review

class CompoundTextInfo(textInfos.TextInfo):

	def _normalizeStartAndEnd(self):
		if (self._start.isCollapsed and self._startObj != self._endObj
				and self._start.compareEndPoints(self._startObj.makeTextInfo(textInfos.POSITION_ALL), "endToEnd") == 0):
			# Start it is at the end of its object.
			# This is equivalent to the start of the next content.
			# Aside from being pointless, we don't want a collapsed start object, as this will cause bogus control fields to be emitted.
			try:
				self._start, self._startObj = self._findNextContent(self._startObj)
			except LookupError:
				pass

		if self._startObj == self._endObj:
			# There should only be a single TextInfo and it should cover the entire range.
			self._start.setEndPoint(self._end, "endToEnd")
			self._end = self._start
			self._endObj = self._startObj
		else:
			# start needs to cover the rest of the text to the end of its object.
			self._start.setEndPoint(self._startObj.makeTextInfo(textInfos.POSITION_ALL), "endToEnd")
			# end needs to cover the rest of the text to the start of its object.
			self._end.setEndPoint(self._endObj.makeTextInfo(textInfos.POSITION_ALL), "startToStart")

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
			if self._end.compareEndPoints(self._endObj.makeTextInfo(textInfos.POSITION_ALL), "endToEnd") == 0:
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

	def _isObjectEditableText(self, obj):
		return obj.role in (controlTypes.ROLE_PARAGRAPH, controlTypes.ROLE_EDITABLETEXT)

	def _getControlFieldForObject(self, obj, ignoreEditableText=True):
		if ignoreEditableText and self._isObjectEditableText(obj):
			# This is basically just a text node.
			return None
		role = obj.role
		states = obj.states
		if role == controlTypes.ROLE_LINK and controlTypes.STATE_LINKED not in states:
			# Named link destination, not a link that can be activated.
			return None
		field = textInfos.ControlField()
		field["role"] = role
		# The user doesn't care about certain states, as they are obvious.
		states.discard(controlTypes.STATE_EDITABLE)
		states.discard(controlTypes.STATE_MULTILINE)
		states.discard(controlTypes.STATE_FOCUSED)
		field["states"] = states
		field["name"] = obj.name
		field["_childcount"] = obj.childCount
		field["level"] = obj.positionInfo.get("level")
		if role == controlTypes.ROLE_TABLE:
			field["table-id"] = 1 # FIXME
			field["table-rowcount"] = obj.rowCount
			field["table-columncount"] = obj.columnCount
		if role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER):
			field["table-id"] = 1 # FIXME
			field["table-rownumber"] = obj.rowNumber
			field["table-columnnumber"] = obj.columnNumber
		return field

	def _iterTextWithEmbeddedObjects(self, text, ti, fieldStart=0, textLength=None):
		if textLength is None:
			textLength = len(text)
		chunkStart = 0
		while chunkStart < textLength:
			try:
				chunkEnd = text.index(u"\uFFFC", chunkStart)
			except ValueError:
				yield text[chunkStart:]
				break
			if chunkStart != chunkEnd:
				yield text[chunkStart:chunkEnd]
			yield ti.getEmbeddedObject(fieldStart + chunkEnd)
			chunkStart = chunkEnd + 1

	def __eq__(self, other):
		return self._start == other._start and self._startObj == other._startObj and self._end == other._end and self._endObj == other._endObj

	def __ne__(self, other):
		return not self == other

	def _getInitialControlFields(self):
		fields = []
		rootObj = self.obj.rootNVDAObject
		obj = self._startObj
		while obj and obj != rootObj:
			field = self._getControlFieldForObject(obj)
			if field:
				fields.insert(0, textInfos.FieldCommand("controlStart", field))
			obj = obj.parent
		return fields

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
			while tempObj and controlTypes.STATE_SELECTED in tempObj.states:
				self._startObj = tempObj
				tempObj = tempObj.flowsFrom
			tempObj = self._endObj
			while tempObj and controlTypes.STATE_SELECTED in tempObj.states:
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
		while obj and controlTypes.STATE_FOCUSABLE not in obj.states:
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

	def getTextWithFields(self, formatConfig=None):
		fields = self._getInitialControlFields()

		for ti in self._getTextInfos():
			fieldStart = 0
			for field in ti.getTextWithFields(formatConfig=formatConfig):
				if isinstance(field, basestring):
					textLength = len(field)
					for chunk in self._iterTextWithEmbeddedObjects(field, ti, fieldStart, textLength=textLength):
						if isinstance(chunk, basestring):
							fields.append(chunk)
						else:
							controlField = self._getControlFieldForObject(chunk, ignoreEditableText=False)
							controlField["alwaysReportName"] = True
							fields.extend((textInfos.FieldCommand("controlStart", controlField),
								u"\uFFFC",
								textInfos.FieldCommand("controlEnd", None)))
					fieldStart += textLength

				else:
					fields.append(field)
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
		return cmp(self._getObjectPosition(selfObj), other._getObjectPosition(otherObj))

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

class EmbeddedObjectCompoundTextInfo(CompoundTextInfo):

	def __init__(self, obj, position):
		super(EmbeddedObjectCompoundTextInfo, self).__init__(obj, position)
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
		elif position in (textInfos.POSITION_FIRST, textInfos.POSITION_LAST):
			self._start, self._startObj = self._findContentDescendant(rootObj, position)
			self._end = self._start
			self._endObj = self._startObj
		elif position == textInfos.POSITION_ALL:
			self._start, self._startObj = self._findContentDescendant(rootObj, textInfos.POSITION_FIRST)
			self._start.expand(textInfos.UNIT_STORY)
			self._end, self._endObj = self._findContentDescendant(rootObj, textInfos.POSITION_LAST)
			self._end.expand(textInfos.UNIT_STORY)
		elif position == textInfos.POSITION_CARET:
			self._start, self._startObj = self._findContentDescendant(obj.caretObject, textInfos.POSITION_CARET)
			self._end = self._start
			self._endObj = self._startObj
		elif position == textInfos.POSITION_SELECTION:
			self._start, self._startObj, self._end, self._endObj = self._findUnitEndpoints(obj.caretObject.makeTextInfo(position), position)
		else:
			raise NotImplementedError

	def _findContentDescendant(self, obj, position):
		while True:
			try:
				ti = obj.makeTextInfo(position)
			except RuntimeError:
				if position == textInfos.POSITION_CARET:
					# The insertion point is before this object, so this object has no caret.
					# We always want to report the character immediately after the insertion point.
					ti = obj.makeTextInfo(textInfos.POSITION_FIRST)
			ti.expand(textInfos.UNIT_OFFSET)
			if ti.text != u"\uFFFC":
				# We've descended as far as we can go.
				break
			embObj = ti.getEmbeddedObject()
			if embObj.TextInfo is NVDAObjectTextInfo:
				# This is an embedded object, but it has no text,
				# so we don't descend into it.
				break
			obj = embObj

		ti.collapse()
		return ti, obj

	def _iterRecursiveText(self, ti, withFields, formatConfig):
		if ti.obj == self._endObj:
			end = True
			ti.setEndPoint(self._end, "endToEnd")
		else:
			end = False
		if withFields:
			fields = ti.getTextWithFields(formatConfig=formatConfig)
		else:
			fields = [ti.text]

		fieldStart = 0
		for field in fields:
			if not field:
				yield u""
			elif isinstance(field, basestring):
				textLength = len(field)
				for chunk in self._iterTextWithEmbeddedObjects(field, ti, fieldStart, textLength=textLength):
					if isinstance(chunk, basestring):
						yield chunk
					else:
						if withFields:
							controlField = self._getControlFieldForObject(chunk)
							if controlField:
								yield textInfos.FieldCommand("controlStart", controlField)
						if not isinstance(chunk.TextInfo, NVDAObjectTextInfo): # Has text
							for subChunk in self._iterRecursiveText(chunk.makeTextInfo("all"), withFields, formatConfig):
								yield subChunk
								if subChunk is None:
									return
						if withFields and controlField:
							yield textInfos.FieldCommand("controlEnd", None)
				fieldStart += textLength
			else:
				yield field

		if end:
			# None means the end has been reached and text retrieval should stop.
			yield None

	def _getText(self, withFields, formatConfig=None):
		ti = self._start
		obj = self._startObj
		if withFields:
			fields = self._getInitialControlFields()
		else:
			fields = []
		fields += list(self._iterRecursiveText(ti, withFields, formatConfig))

		while fields[-1] is not None:
			# The end hasn't yet been reached, which means it isn't a descendant of obj.
			# Therefore, continue from where obj was embedded.
			if withFields and not self._isObjectEditableText(obj):
				# Add a controlEnd if this field had a controlStart.
				fields.append(textInfos.FieldCommand("controlEnd", None))
			from logHandler import log; log.info("%d" % obj.role)
			ti = obj.embeddingTextInfo
			obj = ti.obj
			if ti.move(textInfos.UNIT_OFFSET, 1) == 0:
				# There's no more text in this object.
				continue
			ti.setEndPoint(obj.makeTextInfo(textInfos.POSITION_ALL), "endToEnd")
			fields.extend(self._iterRecursiveText(ti, withFields, formatConfig))
		del fields[-1]
		return fields

	def _get_text(self):
		return "".join(self._getText(False))

	def getTextWithFields(self, formatConfig=None):
		return self._getText(True, formatConfig)

	def _findUnitEndpoints(self, baseTi, unit, findStart=True, findEnd=True):
		start = startObj = end = endObj = None
		baseTi.collapse()
		obj = baseTi.obj

		# Walk up the hierarchy until we find the start and end points.
		while True:
			if unit == textInfos.POSITION_SELECTION:
				expandTi = obj.makeTextInfo(unit)
				if expandTi.isCollapsed:
					# There is no selection, only a caret.
					if not findEnd:
						return expandTi, obj
					if not findEnd:
						return expandTi, obj
					return expandTi, obj, expandTi, obj
			else:
				expandTi = baseTi.copy()
				expandTi.expand(unit)
				if expandTi.isCollapsed:
					# This shouldn't happen, but can due to server implementation bugs; e.g. MozillaBug:1149415.
					expandTi.expand(textInfos.UNIT_OFFSET)
			allTi = obj.makeTextInfo(textInfos.POSITION_ALL)

			if not start and findStart and expandTi.compareEndPoints(allTi, "startToStart") != 0:
				# The unit definitely starts within this object.
				start = expandTi
				startObj = start.obj
				if baseTi.compareEndPoints(expandTi, "startToStart") == 0:
					startDescPos = textInfos.POSITION_FIRST
				else:
					# The unit expands beyond the base point,
					# so only include the nearest descendant unit.
					startDescPos = textInfos.POSITION_LAST

			if not end and findEnd and expandTi.compareEndPoints(allTi, "endToEnd") != 0:
				# The unit definitely ends within this object.
				end = expandTi
				endObj = end.obj
				if baseTi.compareEndPoints(expandTi, "endToEnd") == 0:
					endDescPos = textInfos.POSITION_LAST
				else:
					# The unit expands beyond the base point,
					# so only include the nearest descendant unit.
					endDescPos = textInfos.POSITION_FIRST

			if (start or not findStart) and (end or not findEnd):
				# Required endpoint(s) have been found, so stop walking.
				break

			# start and/or end hasn't yet been found,
			# so it must be higher in the hierarchy.
			embedTi = obj.embeddingTextInfo
			if not embedTi:
				# There is no embedding object.
				# The unit starts and/or ends at the start and/or end of this last object.
				if findStart and not start:
					start = expandTi
					startObj = start.obj
					if baseTi.compareEndPoints(expandTi, "startToStart") == 0:
						startDescPos = textInfos.POSITION_FIRST
					else:
						# The unit expands beyond the base point,
						# so only include the nearest descendant unit.
						startDescPos = textInfos.POSITION_LAST
				if findEnd and not end:
					end = expandTi
					endObj = end.obj
					if baseTi.compareEndPoints(expandTi, "endToEnd") == 0:
						endDescPos = textInfos.POSITION_LAST
					else:
						# The unit expands beyond the base point,
						# so only include the nearest descendant unit.
						endDescPos = textInfos.POSITION_FIRST
				break

			obj = embedTi.obj
			baseTi = embedTi

		if findStart:
			ti = start.copy()
			ti.expand(textInfos.UNIT_OFFSET)
			if ti.text == u"\uFFFC":
				start, startObj = self._findContentDescendant(ti.getEmbeddedObject(), startDescPos)
				if unit == textInfos.POSITION_SELECTION:
					start = startObj.makeTextInfo(unit)
				else:
					start.expand(unit)
			if not findEnd:
				return start, startObj
		if findEnd:
			ti = end.copy()
			ti.collapse(end=True)
			ti.move(textInfos.UNIT_OFFSET, -1, "start")
			if ti.text == u"\uFFFC":
				end, endObj = self._findContentDescendant(ti.getEmbeddedObject(), endDescPos)
				if unit == textInfos.POSITION_SELECTION:
					end = endObj.makeTextInfo(unit)
				else:
					end.expand(unit)
			if not findStart:
				return end, endObj

		return start, startObj, end, endObj

	def expand(self, unit):
		if unit in ( textInfos.UNIT_CHARACTER, textInfos.UNIT_OFFSET):
			self._end = self._start
			self._endObj = self._startObj
			self._start.expand(unit)
			return

		start, startObj, end, endObj = self._findUnitEndpoints(self._start, unit)
		if startObj == endObj:
			end = start
			endObj = startObj

		self._start = start
		self._startObj = startObj
		self._end = end
		self._endObj = endObj

	def _findNextContent(self, origin, moveBack=False):
		if isinstance(origin, textInfos.TextInfo):
			ti = origin
			obj = ti.obj
		else:
			ti = None
			obj = origin

		# Ascend until we can move to the next offset.
		direction = -1 if moveBack else 1
		while True:
			if ti and ti.move(textInfos.UNIT_OFFSET, direction) != 0:
				break
			ti = obj.embeddingTextInfo
			if not ti:
				raise LookupError
			obj = ti.obj

		ti.expand(textInfos.UNIT_OFFSET)
		if ti.text == u"\uFFFC":
			return self._findContentDescendant(ti.getEmbeddedObject(), textInfos.POSITION_LAST if moveBack else textInfos.POSITION_FIRST)
		return ti, obj

	def move(self, unit, direction, endPoint=None):
		if direction == 0:
			return 0

		if not endPoint or endPoint == "start":
			moveTi = self._start
			moveObj = self._startObj
			moveTi.collapse()
		elif endPoint == "end":
			moveTi = self._end
			moveObj = self._endObj
			moveTi.collapse(end=True)

		remainingMovement = direction
		moveBack = direction < 0
		while remainingMovement != 0:
			if moveBack:
				# Move back 1 offset to move into the previous unit.
				try:
					moveTi, moveObj = self._findNextContent(moveTi, moveBack=True)
				except LookupError:
					# Can't move back any further.
					break

			# Find the edge of the current unit in the requested direction.
			moveTi, moveObj = self._findUnitEndpoints(moveTi, unit, findStart=moveBack, findEnd=not moveBack)

			if not moveBack:
				# Collapse to the start of the next unit.
				moveTi.collapse(end=True)
				if moveTi.compareEndPoints(moveObj.makeTextInfo(textInfos.POSITION_ALL), "endToEnd") == 0:
					# If at the end of the object, move to the start of the next object.
					try:
						moveTi, moveObj = self._findNextContent(moveObj)
					except LookupError:
						# Can't move forward any further.
						if endPoint == "end" and moveTi.compareEndPoints(self._end, "endToEnd") != 0:
							# Moving the end to the end of the document counts as a move.
							remainingMovement -= 1
						break
				else:
					# We may have landed on an embedded object.
					ti = moveTi.copy()
					ti.expand(textInfos.UNIT_OFFSET)
					if ti.text == u"\uFFFC":
						moveTi, moveObj = self._findContentDescendant(ti.getEmbeddedObject(), textInfos.POSITION_FIRST)

			remainingMovement -= -1 if moveBack else 1

		if not endPoint or endPoint == "start":
			self._start = moveTi
			self._startObj = moveObj
		if not endPoint or endPoint == "end":
			self._end = moveTi
			self._endObj = moveObj
		self._normalizeStartAndEnd()
		return direction - remainingMovement

	def _getAncestors(self, ti, obj):
		data = []
		while True:
			data.insert(0, (ti, obj))
			ti = obj.embeddingTextInfo
			if not ti:
				break
			obj = ti.obj
		return data

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

		# Different objects, so we have to compare ancestors.
		selfAncs = self._getAncestors(selfTi, selfObj)
		otherAncs = self._getAncestors(otherTi, otherObj)
		# Find the first common ancestor.
		maxAncIndex = min(len(selfAncs), len(otherAncs)) - 1
		for (selfAncTi, selfAncObj), (otherAncTi, otherAncObj) in itertools.izip(selfAncs[maxAncIndex::-1], otherAncs[maxAncIndex::-1]):
			if selfAncObj == otherAncObj:
				break
		else:
			# No common ancestor.
			return 1
		return selfAncTi.compareEndPoints(otherAncTi, which)

class CompoundDocument(EditableText, TreeInterceptor):
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

	def makeTextInfo(self, position):
		return self.TextInfo(self, position)

	def _get_caretObject(self):
		return eventHandler.lastQueuedFocusObject

	def event_treeInterceptor_gainFocus(self):
		# Don't use speakObject because this may speak the text using the object's TextInfo.
		speech.speakObjectProperties(self.rootNVDAObject, name=True, description=True, role=True, states=True, reason=controlTypes.REASON_FOCUS)
		try:
			info = self.makeTextInfo(textInfos.POSITION_SELECTION)
		except RuntimeError:
			pass
		else:
			if info.isCollapsed:
				info.expand(textInfos.UNIT_LINE)
				speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.REASON_CARET)
			else:
				speech.speakSelectionMessage(_("selected %s"), info.text)
			braille.handler.handleGainFocus(self)
			self.initAutoSelectDetection()

	def event_caret(self, obj, nextHandler):
		self.detectPossibleSelectionChange()
		braille.handler.handleCaretMove(self)
		try:
			caret = self.makeTextInfo(textInfos.POSITION_CARET)
		except RuntimeError:
			return
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

class EmbeddedObjectCompoundDocument(CompoundDocument):
	TextInfo = EmbeddedObjectCompoundTextInfo
