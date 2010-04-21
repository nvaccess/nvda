#compoundDocuments.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

import textInfos
import controlTypes
import eventHandler
from NVDAObjects import NVDAObject
from editableText import EditableText
from treeInterceptorHandler import TreeInterceptor
import speech

class CompoundTextInfo(textInfos.TextInfo):

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

	def setEndPoint(self, other, which):
		if which == "startToStart":
			self._start = other._start
			self._startObj = other._startObj
		elif which == "startToEnd":
			self._start = other._end
			self._startObj = other._endObj
		elif which == "endToStart":
			self._end = other._start
			self._endObj = other._starttObj
		elif which == "endToEnd":
			self._end = other._end
			self._endObj = other._endObj
		else:
			raise ValueError("which=%s" % which)

	def collapse(self, end=False):
		if end:
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

	def _get_bookmark(self):
		return self.copy()

	def _get_NVDAObjectAtStart(self):
		return self._startObj

	def _get_pointAtStart(self):
		return self._start.pointAtStart

	def _getControlFieldForObject(self, obj):
		field = textInfos.ControlField()
		role = obj.role
		field["role"] = obj.role
		field["states"] = obj.states
		field["name"] = obj.name
		field["_childcount"] = obj.childCount
		if role == controlTypes.ROLE_TABLE:
			field["table-id"] = 1 # FIXME
			field["table-rowcount"] = obj.rowCount
			field["table-columncount"] = obj.columnCount
		if role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER):
			field["table-id"] = 1 # FIXME
			field["table-rownumber"] = obj.rowNumber
			field["table-columnnumber"] = obj.columnNumber
		return field

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
			self._startObj = self._endObj = rootObj.firstChild
			self._start = self._end = self._startObj.makeTextInfo(position)
		elif position == textInfos.POSITION_LAST:
			self._startObj = self._endObj = rootObj.lastChild
			self._start = self._end = self._startObj.makeTextInfo(position)
		elif position == textInfos.POSITION_ALL:
			self._startObj = rootObj.firstChild
			self._endObj = rootObj.lastChild
			self._start = self._startObj.makeTextInfo(position)
			self._end = self._endObj.makeTextInfo(position)
		elif position == textInfos.POSITION_CARET:
			self._startObj = self._endObj = obj.caretObject
			self._start = self._end = self._startObj.makeTextInfo(position)
		else:
			raise NotImplementedError

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
		# Get the initial control fields.
		fields = []
		rootObj = self.obj.rootNVDAObject
		obj = self._startObj
		while obj and obj != rootObj:
			field = self._getControlFieldForObject(obj)
			fields.insert(0, textInfos.FieldCommand("controlStart", field))
			obj = obj.parent
		fields.extend(f for ti in self._getTextInfos() for f in ti.getTextWithFields(formatConfig=formatConfig))
		return fields

	def expand(self, unit):
		if unit == textInfos.UNIT_READINGCHUNK:
			unit = textInfos.UNIT_LINE

		if unit in self.SINGLE_TEXTINFO_UNITS:
			# This unit is definitely contained within a single chunk.
			self._start.expand(unit)
			self._end = self._start
			self._endObj = self._startObj
		elif unit == textInfos.UNIT_STORY:
			self._startObj = obj.firstChild
			self._endObj = obj.lastChild
			self._start = self._startObj.makeTextInfo(position)
			self._end = self._endObj.makeTextInfo(position)
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
		while True:
			remainingMovement -= moveTi.move(unit, remainingMovement, endPoint=endPoint)
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
				moveTi = moveObj.makeTextInfo(textInfos.POSITION_LAST)
			else:
				moveTi = moveObj.makeTextInfo(textInfos.POSITION_FIRST)
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

		return direction - remainingMovement

class CompoundDocument(EditableText, TreeInterceptor):
	TextInfo = TreeCompoundTextInfo

	def __init__(self, rootNVDAObject):
		super(CompoundDocument, self).__init__(rootNVDAObject)
		EditableText.initClass(self)

	def _get_isAlive(self):
		return True

	def __contains__(self, obj):
		return obj.windowHandle == self.rootNVDAObject.windowHandle

	def makeTextInfo(self, position):
		return self.TextInfo(self, position)

	def _get_caretObject(self):
		return eventHandler.lastQueuedFocusObject

	def event_treeInterceptor_gainFocus(self):
		speech.speakObject(self.rootNVDAObject, reason=speech.REASON_FOCUS)
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info)

	def event_caret(self, obj, nextHandler):
		pass

	def event_gainFocus(self, obj, nextHandler):
		pass

	def event_focusEntered(self, obj, nextHandler):
		pass

	def event_stateChange(self, obj, nextHandler):
		pass

	def event_selection(self, obj, nextHandler):
		pass
