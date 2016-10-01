#NVDAObjects/IAccessible/ia2TextMozilla.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015-2016 NV Access Limited

"""Support for the IAccessible2 rich text model first implemented by Mozilla.
This is now used by other applications as well.
"""

import itertools
from comtypes import COMError
import winUser
import textInfos
import controlTypes
import IAccessibleHandler
import api
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
from . import IA2TextTextInfo, IAccessible
from compoundDocuments import CompoundTextInfo

class FakeEmbeddingTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getStoryLength(self):
		return self.obj.childCount

	def _iterTextWithEmbeddedObjects(self, withFields, formatConfig=None):
		return xrange(self._startOffset, self._endOffset)

	def _getUnitOffsets(self,unit,offset):
		if unit in (textInfos.UNIT_WORD,textInfos.UNIT_LINE):
			unit=textInfos.UNIT_CHARACTER
		return super(FakeEmbeddingTextInfo,self)._getUnitOffsets(unit,offset)

def _getRawTextInfo(obj):
	if not hasattr(obj, "IAccessibleTextObject") and obj.role in (controlTypes.ROLE_TABLE, controlTypes.ROLE_TABLEROW):
		return FakeEmbeddingTextInfo
	elif obj.TextInfo is NVDAObjectTextInfo:
		return NVDAObjectTextInfo
	return IA2TextTextInfo

def _getEmbedded(obj, offset):
	if not hasattr(obj, "IAccessibleTextObject"):
		return obj.getChild(offset)
	# Mozilla uses IAccessibleHypertext to facilitate quick retrieval of embedded objects.
	try:
		ht = obj.iaHypertext
		hi = ht.hyperlinkIndex(offset)
		if hi != -1:
			hl = ht.hyperlink(hi)
			return IAccessible(IAccessibleObject=hl.QueryInterface(IAccessibleHandler.IAccessible2), IAccessibleChildID=0)
	except COMError:
		pass
	return None

class MozillaCompoundTextInfo(CompoundTextInfo):

	def __init__(self, obj, position):
		super(MozillaCompoundTextInfo, self).__init__(obj, position)
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
			self._start, self._startObj = self._findContentDescendant(obj, position)
			self._end = self._start
			self._endObj = self._startObj
		elif position == textInfos.POSITION_ALL:
			self._start, self._startObj = self._findContentDescendant(obj, textInfos.POSITION_FIRST)
			self._start.expand(textInfos.UNIT_STORY)
			self._end, self._endObj = self._findContentDescendant(obj, textInfos.POSITION_LAST)
			self._end.expand(textInfos.UNIT_STORY)
		elif position == textInfos.POSITION_CARET:
			try:
				caretTi, caretObj = self._findContentDescendant(obj, textInfos.POSITION_CARET)
			except LookupError:
				raise RuntimeError("No caret")
			if caretObj is not obj and caretObj.IA2Attributes.get("display") == "inline" and caretTi.compareEndPoints(self._makeRawTextInfo(caretObj, textInfos.POSITION_ALL), "startToEnd") == 0:
				# The caret is at the end of an inline object.
				# This will report "blank", but we want to report the character just after the caret.
				try:
					caretTi, caretObj = self._findNextContent(caretTi)
				except LookupError:
					pass
			self._start = self._end = caretTi
			self._startObj = self._endObj = caretObj
		elif position == textInfos.POSITION_SELECTION:
			# The caret is usually within the selection,
			# so start from the caret for better performance/tolerance of server brokenness.
			tempTi, tempObj = self._findContentDescendant(obj, textInfos.POSITION_CARET)
			try:
				tempTi = self._makeRawTextInfo(tempObj, position)
			except RuntimeError:
				# The caret is just before this object.
				# There is never a selection in this case.
				pass
			else:
				if tempTi.isCollapsed:
					# No selection, but perhaps the caret is at the start of the next/previous object.
					# This happens when you, for example, press shift+rightArrow at the end of a block.
					# Try from the root.
					rootTi = self._makeRawTextInfo(obj, position)
					if not rootTi.isCollapsed:
						# There is definitely a selection.
						tempTi, tempObj = rootTi, obj
			if tempTi.isCollapsed:
				# No selection, so use the caret.
				self._start = self._end = tempTi
				self._startObj = self._endObj = tempObj
			else:
				self._start, self._startObj, self._end, self._endObj = self._findUnitEndpoints(tempTi, position)
		elif isinstance(position, textInfos.Point):
			startObj = api.getDesktopObject().objectFromPoint(position.x, position.y)
			while startObj and startObj.role == controlTypes.ROLE_STATICTEXT:
				# Skip text leaf nodes.
				startObj = startObj.parent
			if not startObj:
				raise LookupError
			self._startObj = startObj
			self._start = self._makeRawTextInfo(startObj, position)
			self._end = self._start
			self._endObj = self._startObj
		else:
			raise NotImplementedError

	def _makeRawTextInfo(self, obj, position):
		return _getRawTextInfo(obj)(obj, position)

	def _getEmbedding(self, obj):
		# optimisation: Passing an Offsets position checks nCharacters, which is an extra call we don't need.
		info = self._makeRawTextInfo(obj.parent, textInfos.POSITION_FIRST)
		if isinstance(info, FakeEmbeddingTextInfo):
			info._startOffset = obj.indexInParent
			info._endOffset = info._startOffset + 1
			return info
		try:
			hl = obj.IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleHyperlink)
			hlOffset = hl.startIndex
			info._startOffset = hlOffset
			info._endOffset = hlOffset + 1
			return info
		except COMError:
			pass
		return None

	POSITION_SELECTION_START = 3
	POSITION_SELECTION_END = 4
	FINDCONTENTDESCENDANT_POSITIONS = {
		textInfos.POSITION_FIRST: 0,
		textInfos.POSITION_CARET: 1,
		textInfos.POSITION_LAST: 2,
	}
	def _findContentDescendant(self, obj, position):
		import ctypes
		import NVDAHelper
		import NVDAObjects.IAccessible
		descendantID=ctypes.c_int()
		descendantOffset=ctypes.c_int()
		what = self.FINDCONTENTDESCENDANT_POSITIONS.get(position, position)
		NVDAHelper.localLib.nvdaInProcUtils_IA2Text_findContentDescendant(obj.appModule.helperLocalBindingHandle,obj.windowHandle,obj.IAccessibleObject.uniqueID,what,ctypes.byref(descendantID),ctypes.byref(descendantOffset))
		if descendantID.value == 0:
			# No descendant.
			raise LookupError("Object has no text descendants")
		if position == self.POSITION_SELECTION_END:
			# As we descend, we need the last offset (not the exclusive end offset),
			# but we want the exclusive end as the final result.
			descendantOffset.value += 1
		# optimisation: If we already have the target obj, don't make a new instance.
		for cached in obj, getattr(self.obj, "_lastCaretObj", None):
			if cached and descendantID.value == cached.IA2UniqueID:
				obj = cached
				break
		else:
			obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(obj.windowHandle,winUser.OBJID_CLIENT,descendantID.value)
		if position == textInfos.POSITION_CARET:
			# Cache for later use.
			self.obj._lastCaretObj = obj
		# optimisation: Passing an Offsets position checks nCharacters, which is an extra call we don't need.
		ti=self._makeRawTextInfo(obj,textInfos.POSITION_FIRST)
		ti._startOffset=ti._endOffset=descendantOffset.value
		return ti,obj

	def _iterRecursiveText(self, ti, controlStack, formatConfig):
		if ti.obj == self._endObj:
			end = True
			ti.setEndPoint(self._end, "endToEnd")
		else:
			end = False

		for item in ti._iterTextWithEmbeddedObjects(controlStack is not None, formatConfig=formatConfig):
			if item is None:
				yield u""
			elif isinstance(item, basestring):
				yield item
			elif isinstance(item, int): # Embedded object.
				embedded = _getEmbedded(ti.obj, item)
				if controlStack is not None:
					controlField = self._getControlFieldForObject(embedded)
					controlStack.append(controlField)
					if controlField:
						controlField["_startOfNode"] = True
						yield textInfos.FieldCommand("controlStart", controlField)
				if _getRawTextInfo(embedded) is NVDAObjectTextInfo: # No text
					yield embedded.basicText
				else:
					for subItem in self._iterRecursiveText(self._makeRawTextInfo(embedded, textInfos.POSITION_ALL), controlStack, formatConfig):
						yield subItem
						if subItem is None:
							return
				if controlStack is not None and controlField:
					controlField["_endOfNode"] = True
					del controlStack[-1]
					yield textInfos.FieldCommand("controlEnd", None)
			else:
				yield item

		if end:
			# None means the end has been reached and text retrieval should stop.
			yield None

	def _getText(self, withFields, formatConfig=None):
		fields = []
		if self.isCollapsed:
			return fields

		if withFields:
			# Get the initial control fields.
			controlStack = []
			rootObj = self.obj
			obj = self._startObj
			ti = self._start
			cannotBeStart = False
			while obj and obj != rootObj:
				field = self._getControlFieldForObject(obj)
				if field:
					if ti._startOffset == 0:
						if not cannotBeStart:
							field["_startOfNode"] = True
					else:
						# We're not at the start of this object, which also means we're not at the start of any ancestors.
						cannotBeStart = True
					fields.insert(0, textInfos.FieldCommand("controlStart", field))
				controlStack.insert(0, field)
				ti = self._getEmbedding(obj)
				obj = ti.obj
		else:
			controlStack = None

		# Get the fields for start.
		fields += list(self._iterRecursiveText(self._start, controlStack, formatConfig))
		if not fields:
			# We're not getting anything, so the object must be dead.
			# (We already handled collapsed above.)
			return fields
		obj = self._startObj
		while fields[-1] is not None:
			# The end hasn't yet been reached, which means it isn't a descendant of obj.
			# Therefore, continue from where obj was embedded.
			if withFields:
				field = controlStack.pop()
				if field:
					# This object had a control field.
					field["_endOfNode"] = True
					fields.append(textInfos.FieldCommand("controlEnd", None))
			ti = self._getEmbedding(obj)
			obj = ti.obj
			if ti.move(textInfos.UNIT_OFFSET, 1) == 0:
				# There's no more text in this object.
				continue
			ti.setEndPoint(self._makeRawTextInfo(obj, textInfos.POSITION_ALL), "endToEnd")
			fields.extend(self._iterRecursiveText(ti, controlStack, formatConfig))
		del fields[-1]

		if withFields:
			# Determine whether the range covers the end of any ancestors of endObj.
			obj = self._endObj
			ti = self._end
			while obj and obj != rootObj:
				field = controlStack.pop()
				if field:
					fields.append(textInfos.FieldCommand("controlEnd", None))
					if ti.compareEndPoints(self._makeRawTextInfo(obj, textInfos.POSITION_ALL), "endToEnd") == 0:
						field["_endOfNode"] = True
					else:
						# We're not at the end of this object, which also means we're not at the end of any ancestors.
						break
				ti = self._getEmbedding(obj)
				obj = ti.obj

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
				expandTi = self._makeRawTextInfo(obj, unit)
			else:
				expandTi = baseTi.copy()
				expandTi.expand(unit)
				if expandTi.isCollapsed:
					# This shouldn't happen, but can due to server implementation bugs; e.g. MozillaBug:1149415.
					expandTi.expand(textInfos.UNIT_OFFSET)
			allTi = self._makeRawTextInfo(obj, textInfos.POSITION_ALL)

			if not start and findStart and expandTi.compareEndPoints(allTi, "startToStart") != 0:
				# The unit definitely starts within this object.
				start = expandTi
				startObj = start.obj
				if unit == textInfos.POSITION_SELECTION:
					startDescPos = self.POSITION_SELECTION_START
				elif baseTi.compareEndPoints(expandTi, "startToStart") == 0:
					startDescPos = textInfos.POSITION_FIRST
				else:
					# The unit expands beyond the base point,
					# so only include the nearest descendant unit.
					startDescPos = textInfos.POSITION_LAST

			if not end and findEnd and expandTi.compareEndPoints(allTi, "endToEnd") != 0:
				# The unit definitely ends within this object.
				end = expandTi
				endObj = end.obj
				if unit == textInfos.POSITION_SELECTION:
					endDescPos = self.POSITION_SELECTION_END
				elif baseTi.compareEndPoints(expandTi, "endToEnd") == 0:
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
			if obj == self.obj:
				# We're at the root. Don't go any further.
				embedTi = None
			else:
				embedTi = self._getEmbedding(obj)
				if isinstance(embedTi, FakeEmbeddingTextInfo):
					# hack: Selection in Mozilla table/table rows is broken (MozillaBug:1169238), so just ignore it.
					embedTi = None
			if not embedTi:
				# There is no embedding object.
				# The unit starts and/or ends at the start and/or end of this last object.
				if findStart and not start:
					start = expandTi
					startObj = start.obj
					if unit == textInfos.POSITION_SELECTION:
						startDescPos = self.POSITION_SELECTION_START
					elif baseTi.compareEndPoints(expandTi, "startToStart") == 0:
						startDescPos = textInfos.POSITION_FIRST
					else:
						# The unit expands beyond the base point,
						# so only include the nearest descendant unit.
						startDescPos = textInfos.POSITION_LAST
				if findEnd and not end:
					end = expandTi
					endObj = end.obj
					if unit == textInfos.POSITION_SELECTION:
						endDescPos = self.POSITION_SELECTION_END
					elif baseTi.compareEndPoints(expandTi, "endToEnd") == 0:
						endDescPos = textInfos.POSITION_LAST
					else:
						# The unit expands beyond the base point,
						# so only include the nearest descendant unit.
						endDescPos = textInfos.POSITION_FIRST
				break

			obj = embedTi.obj
			baseTi = embedTi

		if findStart:
			embedded = _getEmbedded(startObj, start._startOffset)
			if embedded:
				try:
					start, startObj = self._findContentDescendant(embedded, startDescPos)
				except LookupError:
					# No text descendants, so we don't descend.
					pass
				else:
					if unit == textInfos.POSITION_SELECTION:
						start = self._makeRawTextInfo(startObj, unit)
					else:
						start.expand(unit)
			if not findEnd:
				return start, startObj
		if findEnd:
			embedded = _getEmbedded(endObj, end._endOffset - 1)
			if embedded:
				try:
					end, endObj = self._findContentDescendant(embedded, endDescPos)
				except LookupError:
					# No text descendants, so we don't descend.
					pass
				else:
					if unit == textInfos.POSITION_SELECTION:
						end = self._makeRawTextInfo(endObj, unit)
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
			if obj == self.obj:
				# We're at the root. Don't go any further.
				raise LookupError
			ti = self._getEmbedding(obj)
			if not ti:
				raise LookupError
			obj = ti.obj

		embedded = _getEmbedded(obj, ti._startOffset)
		if embedded:
			try:
				return self._findContentDescendant(embedded, textInfos.POSITION_LAST if moveBack else textInfos.POSITION_FIRST)
			except LookupError:
				# No text descendants, so we don't descend.
				pass
		return ti, obj

	def move(self, unit, direction, endPoint=None):
		if direction == 0:
			return 0

		if not endPoint or endPoint == "start":
			moveTi = self._start
			moveObj = self._startObj
			if endPoint and moveTi is self._end:
				# We're just moving start. We don't want end to be affected.
				moveTi = moveTi.copy()
			moveTi.collapse()
		elif endPoint == "end":
			moveTi = self._end
			moveObj = self._endObj
			if endPoint and moveTi is self._start:
				# We're just moving end. We don't want start to be affected.
				moveTi = moveTi.copy()
			moveTi.collapse(end=True)
			if moveTi.compareEndPoints(self._makeRawTextInfo(moveObj, textInfos.POSITION_ALL), "endToEnd") == 0:
				# We're at the end of the object, so move to the start of the next.
				try:
					moveTi, moveObj = self._findNextContent(moveObj)
				except LookupError:
					# Can't move forward any further.
					return 0

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
				if moveTi.compareEndPoints(self._makeRawTextInfo(moveObj, textInfos.POSITION_ALL), "endToEnd") == 0:
					# We're at the end of the object.
					if remainingMovement == 1 and endPoint == "end":
						# We've moved the required number of units.
						# Stop here, as we don't want end to be the start of the next object,
						# which would cause bogus control fields to be emitted.
						remainingMovement -= 1
						break
					# We haven't finished moving, so move to the start of the next object.
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
					embedded = _getEmbedded(moveObj, moveTi._startOffset)
					if embedded:
						try:
							moveTi, moveObj = self._findContentDescendant(embedded, textInfos.POSITION_FIRST)
						except LookupError:
							# No text descendants, so we don't descend.
							pass

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
			if obj == self.obj:
				# We're at the root. Don't go any further.
				break
			ti = self._getEmbedding(obj)
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
