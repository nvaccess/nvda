# -*- coding: UTF-8 -*-
#virtualBuffers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2015 NV Access Limited, Peter Vágner

import time
import threading
import ctypes
import collections
import itertools
import weakref
import wx
import review
import NVDAHelper
import XMLFormatting
import scriptHandler
from scriptHandler import isScriptWaiting, willSayAllResume
import speech
import NVDAObjects
import api
import sayAllHandler
import controlTypes
import textInfos.offsets
import config
import cursorManager
import browseMode
import gui
import eventHandler
import braille
import queueHandler
from logHandler import log
import ui
import aria
import nvwave
import treeInterceptorHandler
import watchdog

VBufStorage_findDirection_forward=0
VBufStorage_findDirection_back=1
VBufStorage_findDirection_up=2
VBufRemote_nodeHandle_t=ctypes.c_ulonglong


class VBufStorage_findMatch_word(unicode):
	pass
VBufStorage_findMatch_notEmpty = object()

FINDBYATTRIBS_ESCAPE_TABLE = {
	# Symbols that are escaped in the attributes string.
	ord(u":"): ur"\\:",
	ord(u";"): ur"\\;",
	ord(u"\\"): u"\\\\\\\\",
}
# Symbols that must be escaped for a regular expression.
FINDBYATTRIBS_ESCAPE_TABLE.update({(ord(s), u"\\" + s) for s in u"^$.*+?()[]{}|"})
def _prepareForFindByAttributes(attribs):
	escape = lambda text: unicode(text).translate(FINDBYATTRIBS_ESCAPE_TABLE)
	reqAttrs = []
	regexp = []
	if isinstance(attribs, dict):
		# Single option.
		attribs = (attribs,)
	# All options will match against all requested attributes,
	# so first build the list of requested attributes.
	for option in attribs:
		for name in option:
			reqAttrs.append(unicode(name))
	# Now build the regular expression.
	for option in attribs:
		optRegexp = []
		for name in reqAttrs:
			optRegexp.append("%s:" % escape(name))
			values = option.get(name)
			if not values:
				# The value isn't tested for this attribute, so match any (or no) value.
				optRegexp.append(r"(?:\\;|[^;])*;")
			elif values[0] is VBufStorage_findMatch_notEmpty:
				# There must be a value for this attribute.
				optRegexp.append(r"(?:\\;|[^;])+;")
			elif isinstance(values[0], VBufStorage_findMatch_word):
				# Assume all are word matches.
				optRegexp.append(r"(?:\\;|[^;])*\b(?:")
				optRegexp.append("|".join(escape(val) for val in values))
				optRegexp.append(r")\b(?:\\;|[^;])*;")
			else:
				# Assume all are exact matches or None (must not exist).
				optRegexp.append("(?:" )
				optRegexp.append("|".join((escape(val)+u';') if val is not None else u';' for val in values))
				optRegexp.append(")")
		regexp.append("".join(optRegexp))
	return u" ".join(reqAttrs), u"|".join(regexp)

class VirtualBufferQuickNavItem(browseMode.TextInfoQuickNavItem):

	def __init__(self,itemType,document,vbufNode,startOffset,endOffset):
		textInfo=document.makeTextInfo(textInfos.offsets.Offsets(startOffset,endOffset))
		super(VirtualBufferQuickNavItem,self).__init__(itemType,document,textInfo)
		docHandle=ctypes.c_int()
		ID=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getIdentifierFromControlFieldNode(document.VBufHandle, vbufNode, ctypes.byref(docHandle), ctypes.byref(ID))
		self.vbufFieldIdentifier=(docHandle.value,ID.value)
		self.vbufNode=vbufNode

	@property
	def obj(self):
		return self.document.getNVDAObjectFromIdentifier(*self.vbufFieldIdentifier)

	@property
	def label(self):
		if self.itemType == "landmark":
			attrs = self.textInfo._getControlFieldAttribs(self.vbufFieldIdentifier[0], self.vbufFieldIdentifier[1])
			name = attrs.get("name", "")
			if name:
				name += " "
			return name + aria.landmarkRoles[attrs["landmark"]]
		else:
			return super(VirtualBufferQuickNavItem,self).label

	def isChild(self,parent): 
		if self.itemType == "heading":
			try:
				if (int(self.textInfo._getControlFieldAttribs(self.vbufFieldIdentifier[0], self.vbufFieldIdentifier[1])["level"])
						> int(parent.textInfo._getControlFieldAttribs(parent.vbufFieldIdentifier[0], parent.vbufFieldIdentifier[1])["level"])):
					return True
			except (KeyError, ValueError, TypeError):
				return False
		return super(VirtualBufferQuickNavItem,self).isChild(parent)

class VirtualBufferTextInfo(browseMode.BrowseModeDocumentTextInfo,textInfos.offsets.OffsetsTextInfo):

	allowMoveToOffsetPastEnd=False #: no need for end insertion point as vbuf is not editable. 

	UNIT_CONTROLFIELD = "controlField"

	def _getControlFieldAttribs(self,  docHandle, id):
		info = self.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		for field in reversed(info.getTextWithFields()):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			if int(attrs["controlIdentifier_docHandle"]) == docHandle and int(attrs["controlIdentifier_ID"]) == id:
				return attrs
		raise LookupError

	def _getFieldIdentifierFromOffset(self, offset):
		startOffset = ctypes.c_int()
		endOffset = ctypes.c_int()
		docHandle = ctypes.c_int()
		ID = ctypes.c_int()
		node=VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_locateControlFieldNodeAtOffset(self.obj.VBufHandle, offset, ctypes.byref(startOffset), ctypes.byref(endOffset), ctypes.byref(docHandle), ctypes.byref(ID),ctypes.byref(node))
		return docHandle.value, ID.value

	def _getOffsetsFromFieldIdentifier(self, docHandle, ID):
		node=VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_getControlFieldNodeWithIdentifier(self.obj.VBufHandle, docHandle, ID,ctypes.byref(node))
		if not node:
			raise LookupError
		start = ctypes.c_int()
		end = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getFieldNodeOffsets(self.obj.VBufHandle, node, ctypes.byref(start), ctypes.byref(end))
		return start.value, end.value

	def _getPointFromOffset(self,offset):
		o = self._getNVDAObjectFromOffset(offset)
		left, top, width, height = o.location
		return textInfos.Point(left + width / 2, top + height / 2)

	def _getNVDAObjectFromOffset(self,offset):
		docHandle,ID=self._getFieldIdentifierFromOffset(offset)
		return self.obj.getNVDAObjectFromIdentifier(docHandle,ID)

	def _getOffsetsFromNVDAObjectInBuffer(self,obj):
		docHandle,ID=self.obj.getIdentifierFromNVDAObject(obj)
		return self._getOffsetsFromFieldIdentifier(docHandle,ID)

	def _getOffsetsFromNVDAObject(self, obj):
		while True:
			try:
				return self._getOffsetsFromNVDAObjectInBuffer(obj)
			except LookupError:
				pass
			# Interactive list/combo box/tree view descendants aren't rendered into the buffer, even though they are still considered part of it.
			# Use the container in this case.
			obj = obj.parent
			if not obj or obj.role not in (controlTypes.ROLE_LIST, controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_GROUPING, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM):
				break
		raise LookupError

	def __init__(self,obj,position):
		self.obj=obj
		super(VirtualBufferTextInfo,self).__init__(obj,position)

	def _getSelectionOffsets(self):
		start=ctypes.c_int()
		end=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getSelectionOffsets(self.obj.VBufHandle,ctypes.byref(start),ctypes.byref(end))
		return start.value,end.value

	def _setSelectionOffsets(self,start,end):
		NVDAHelper.localLib.VBuf_setSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return NVDAHelper.localLib.VBuf_getTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		if start==end:
			return u""
		return NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle,start,end,False) or u""

	def getTextWithFields(self,formatConfig=None):
		start=self._startOffset
		end=self._endOffset
		if start==end:
			return ""
		text=NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle,start,end,True)
		if not text:
			return ""
		commandList=XMLFormatting.XMLTextParser().parse(text)
		for index in xrange(len(commandList)):
			if isinstance(commandList[index],textInfos.FieldCommand):
				field=commandList[index].field
				if isinstance(field,textInfos.ControlField):
					commandList[index].field=self._normalizeControlField(field)
				elif isinstance(field,textInfos.FormatField):
					commandList[index].field=self._normalizeFormatField(field)
		return commandList

	def _getWordOffsets(self,offset):
		#Use VBuf_getBufferLineOffsets with out screen layout to find out the range of the current field
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(self.obj.VBufHandle,offset,0,False,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		word_startOffset,word_endOffset=super(VirtualBufferTextInfo,self)._getWordOffsets(offset)
		return (max(lineStart.value,word_startOffset),min(lineEnd.value,word_endOffset))

	def _getLineOffsets(self,offset):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(self.obj.VBufHandle,offset,config.conf["virtualBuffers"]["maxLineLength"],config.conf["virtualBuffers"]["useScreenLayout"],ctypes.byref(lineStart),ctypes.byref(lineEnd))
		return lineStart.value,lineEnd.value
 
	def _getParagraphOffsets(self,offset):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(self.obj.VBufHandle,offset,0,True,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		return lineStart.value,lineEnd.value

	def _normalizeControlField(self,attrs):
		tableLayout=attrs.get('table-layout')
		if tableLayout:
			attrs['table-layout']=tableLayout=="1"

		isHidden=attrs.get('isHidden')
		if isHidden:
			attrs['isHidden']=isHidden=="1"

		# Handle table row and column headers.
		for axis in "row", "column":
			attr = attrs.pop("table-%sheadercells" % axis, None)
			if not attr:
				continue
			cellIdentifiers = [identifier.split(",") for identifier in attr.split(";") if identifier]
			# Get the text for the header cells.
			textList = []
			for docHandle, ID in cellIdentifiers:
				try:
					start, end = self._getOffsetsFromFieldIdentifier(int(docHandle), int(ID))
				except (LookupError, ValueError):
					continue
				textList.append(self.obj.makeTextInfo(textInfos.offsets.Offsets(start, end)).text)
			attrs["table-%sheadertext" % axis] = "\n".join(textList)

		if attrs.get("landmark") == "region" and not attrs.get("name"):
			# We only consider region to be a landmark if it has a name.
			del attrs["landmark"]

		# Expose a unique ID on the controlField for quick and safe comparison using the virtualBuffer field's docHandle and ID
		docHandle=attrs.get('controlIdentifier_docHandle')
		ID=attrs.get('controlIdentifier_ID')
		if docHandle is not None and ID is not None:
			attrs['uniqueID']=(docHandle,ID)

		return attrs

	def _normalizeFormatField(self, attrs):
		return attrs

	def _getLineNumFromOffset(self, offset):
		return None

	def _get_fieldIdentifierAtStart(self):
		return self._getFieldIdentifierFromOffset( self._startOffset)

	def _getUnitOffsets(self, unit, offset):
		if unit == self.UNIT_CONTROLFIELD:
			startOffset=ctypes.c_int()
			endOffset=ctypes.c_int()
			docHandle=ctypes.c_int()
			ID=ctypes.c_int()
			node=VBufRemote_nodeHandle_t()
			NVDAHelper.localLib.VBuf_locateControlFieldNodeAtOffset(self.obj.VBufHandle,offset,ctypes.byref(startOffset),ctypes.byref(endOffset),ctypes.byref(docHandle),ctypes.byref(ID),ctypes.byref(node))
			return startOffset.value,endOffset.value
		return super(VirtualBufferTextInfo, self)._getUnitOffsets(unit, offset)

	def _get_clipboardText(self):
		# Blocks should start on a new line, but they don't necessarily have an end of line indicator.
		# Therefore, get the text in block (paragraph) chunks and join the chunks with \r\n.
		blocks = (block.strip("\r\n") for block in self.getTextInChunks(textInfos.UNIT_PARAGRAPH))
		return "\r\n".join(blocks)

	def activate(self):
		self.obj._activatePosition(self)

	def getMathMl(self, field):
		docHandle = int(field["controlIdentifier_docHandle"])
		nodeId = int(field["controlIdentifier_ID"])
		obj = self.obj.getNVDAObjectFromIdentifier(docHandle, nodeId)
		return obj.mathMl

class VirtualBuffer(browseMode.BrowseModeDocumentTreeInterceptor):

	TextInfo=VirtualBufferTextInfo

	#: Maps root identifiers (docHandle and ID) to buffers.
	rootIdentifiers = weakref.WeakValueDictionary()

	def __init__(self,rootNVDAObject,backendName=None):
		super(VirtualBuffer,self).__init__(rootNVDAObject)
		self.backendName=backendName
		self.VBufHandle=None
		self.isLoading=False
		self.rootDocHandle,self.rootID=self.getIdentifierFromNVDAObject(self.rootNVDAObject)
		self.rootIdentifiers[self.rootDocHandle, self.rootID] = self

	def prepare(self):
		self.shouldPrepare=False
		self.loadBuffer()

	def _get_shouldPrepare(self):
		return not self.isLoading and not self.VBufHandle

	def terminate(self):
		super(VirtualBuffer,self).terminate()
		if not self.VBufHandle:
			return
		self.unloadBuffer()

	def _get_isReady(self):
		return bool(self.VBufHandle and not self.isLoading)

	def loadBuffer(self):
		self.isLoading = True
		self._loadProgressCallLater = wx.CallLater(1000, self._loadProgress)
		threading.Thread(target=self._loadBuffer).start()

	def _loadBuffer(self):
		try:
			self.VBufHandle=NVDAHelper.localLib.VBuf_createBuffer(self.rootNVDAObject.appModule.helperLocalBindingHandle,self.rootDocHandle,self.rootID,unicode(self.backendName))
			if not self.VBufHandle:
				raise RuntimeError("Could not remotely create virtualBuffer")
		except:
			log.error("", exc_info=True)
			queueHandler.queueFunction(queueHandler.eventQueue, self._loadBufferDone, success=False)
			return
		queueHandler.queueFunction(queueHandler.eventQueue, self._loadBufferDone)

	def _loadBufferDone(self, success=True):
		self._loadProgressCallLater.Stop()
		del self._loadProgressCallLater
		self.isLoading = False
		if not success:
			self.passThrough=True
			return
		if self._hadFirstGainFocus:
			# If this buffer has already had focus once while loaded, this is a refresh.
			# Translators: Reported when a page reloads (example: after refreshing a webpage).
			ui.message(_("Refreshed"))
		if api.getFocusObject().treeInterceptor == self:
			self.event_treeInterceptor_gainFocus()

	def _loadProgress(self):
		# Translators: Reported while loading a document.
		ui.message(_("Loading document..."))

	def unloadBuffer(self):
		if self.VBufHandle is not None:
			try:
				watchdog.cancellableExecute(NVDAHelper.localLib.VBuf_destroyBuffer, ctypes.byref(ctypes.c_int(self.VBufHandle)))
			except WindowsError:
				pass
			self.VBufHandle=None

	def isNVDAObjectPartOfLayoutTable(self,obj):
		docHandle,ID=self.getIdentifierFromNVDAObject(obj)
		ID=unicode(ID)
		info=self.makeTextInfo(obj)
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		fieldCommands=[x for x in info.getTextWithFields() if isinstance(x,textInfos.FieldCommand)]
		tableLayout=None
		tableID=None
		for fieldCommand in fieldCommands:
			fieldID=fieldCommand.field.get("controlIdentifier_ID") if fieldCommand.field else None
			if fieldID==ID:
				tableLayout=fieldCommand.field.get('table-layout')
				if tableLayout is not None:
					return tableLayout
				tableID=fieldCommand.field.get('table-id')
				break
		if tableID is None:
			return False
		for fieldCommand in fieldCommands:
			fieldID=fieldCommand.field.get("controlIdentifier_ID") if fieldCommand.field else None
			if fieldID==tableID:
				tableLayout=fieldCommand.field.get('table-layout',False)
				break
		return tableLayout

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		"""Retrieve an NVDAObject for a given node identifier.
		Subclasses must override this method.
		@param docHandle: The document handle.
		@type docHandle: int
		@param ID: The ID of the node.
		@type ID: int
		@return: The NVDAObject.
		@rtype: L{NVDAObjects.NVDAObject}
		"""
		raise NotImplementedError

	def getIdentifierFromNVDAObject(self,obj):
		"""Retreaves the virtualBuffer field identifier from an NVDAObject.
		@param obj: the NVDAObject to retreave the field identifier from.
		@type obj: L{NVDAObject}
		@returns: a the field identifier as a doc handle and ID paire.
		@rtype: 2-tuple.
		"""
		raise NotImplementedError

	def script_refreshBuffer(self,gesture):
		if scriptHandler.isScriptWaiting():
			# This script may cause subsequently queued scripts to fail, so don't execute.
			return
		self.unloadBuffer()
		self.loadBuffer()
	# Translators: the description for the refreshBuffer script on virtualBuffers.
	script_refreshBuffer.__doc__ = _("Refreshes the document content")

	def script_toggleScreenLayout(self,gesture):
		config.conf["virtualBuffers"]["useScreenLayout"]=not config.conf["virtualBuffers"]["useScreenLayout"]
		if config.conf["virtualBuffers"]["useScreenLayout"]:
			# Translators: Presented when use screen layout option is toggled.
			ui.message(_("Use screen layout on"))
		else:
			# Translators: Presented when use screen layout option is toggled.
			ui.message(_("Use screen layout off"))
	# Translators: the description for the toggleScreenLayout script on virtualBuffers.
	script_toggleScreenLayout.__doc__ = _("Toggles on and off if the screen layout is preserved while rendering the document content")

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		attribs=self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			raise NotImplementedError
		return self._iterNodesByAttribs(attribs, direction, pos,nodeType)

	def _iterNodesByAttribs(self, attribs, direction="next", pos=None,nodeType=None):
		offset=pos._startOffset if pos else -1
		reqAttrs, regexp = _prepareForFindByAttributes(attribs)
		startOffset=ctypes.c_int()
		endOffset=ctypes.c_int()
		if direction=="next":
			direction=VBufStorage_findDirection_forward
		elif direction=="previous":
			direction=VBufStorage_findDirection_back
		elif direction=="up":
			direction=VBufStorage_findDirection_up
		else:
			raise ValueError("unknown direction: %s"%direction)
		while True:
			try:
				node=VBufRemote_nodeHandle_t()
				NVDAHelper.localLib.VBuf_findNodeByAttributes(self.VBufHandle,offset,direction,reqAttrs,regexp,ctypes.byref(startOffset),ctypes.byref(endOffset),ctypes.byref(node))
			except:
				return
			if not node:
				return
			yield VirtualBufferQuickNavItem(nodeType,self,node,startOffset.value,endOffset.value)
			offset=startOffset

	def _getTableCellCoords(self, info):
		if info.isCollapsed:
			info = info.copy()
			info.expand(textInfos.UNIT_CHARACTER)
		for field in reversed(info.getTextWithFields()):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			if "table-id" in attrs and "table-rownumber" in attrs:
				break
		else:
			raise LookupError("Not in a table cell")
		return (int(attrs["table-id"]),
			int(attrs["table-rownumber"]), int(attrs["table-columnnumber"]),
			int(attrs.get("table-rowsspanned", 1)), int(attrs.get("table-columnsspanned", 1)))

	def _iterTableCells(self, tableID, startPos=None, direction="next", row=None, column=None):
		attrs = {"table-id": [str(tableID)]}
		# row could be 0.
		if row is not None:
			attrs["table-rownumber"] = [str(row)]
		if column is not None:
			attrs["table-columnnumber"] = [str(column)]
		results = self._iterNodesByAttribs(attrs, pos=startPos, direction=direction)
		if not startPos and not row and not column and direction == "next":
			# The first match will be the table itself, so skip it.
			next(results)
		for item in results:
			yield item.textInfo

	def _getNearestTableCell(self, tableID, startPos, origRow, origCol, origRowSpan, origColSpan, movement, axis):
		if not axis:
			# First or last.
			if movement == "first":
				startPos = None
				direction = "next"
			elif movement == "last":
				startPos = self.makeTextInfo(textInfos.POSITION_LAST)
				direction = "previous"
			try:
				return next(self._iterTableCells(tableID, startPos=startPos, direction=direction))
			except StopIteration:
				raise LookupError

		# Determine destination row and column.
		destRow = origRow
		destCol = origCol
		if axis == "row":
			destRow += origRowSpan if movement == "next" else -1
		elif axis == "column":
			destCol += origColSpan if movement == "next" else -1

		if destCol < 1:
			# Optimisation: We're definitely at the edge of the column.
			raise LookupError

		# Optimisation: Try searching for exact destination coordinates.
		# This won't work if they are covered by a cell spanning multiple rows/cols, but this won't be true in the majority of cases.
		try:
			return next(self._iterTableCells(tableID, row=destRow, column=destCol))
		except StopIteration:
			pass

		# Cells are grouped by row, so in most cases, we simply need to search in the right direction.
		for info in self._iterTableCells(tableID, direction=movement, startPos=startPos):
			_ignore, row, col, rowSpan, colSpan = self._getTableCellCoords(info)
			if row <= destRow < row + rowSpan and col <= destCol < col + colSpan:
				return info
			elif row > destRow and movement == "next":
				# Optimisation: We've gone forward past destRow, so we know we won't find the cell.
				# We can't reverse this logic when moving backwards because there might be a prior cell on an earlier row which spans multiple rows.
				break

		if axis == "row" or (axis == "column" and movement == "previous"):
			# In most cases, there's nothing more to try.
			raise LookupError

		else:
			# We're moving forward by column.
			# In this case, there might be a cell on an earlier row which spans multiple rows.
			# Therefore, try searching backwards.
			for info in self._iterTableCells(tableID, direction="previous", startPos=startPos):
				_ignore, row, col, rowSpan, colSpan = self._getTableCellCoords(info)
				if row <= destRow < row + rowSpan and col <= destCol < col + colSpan:
					return info
			else:
				raise LookupError

	def _tableMovementScriptHelper(self, movement="next", axis=None):
		if isScriptWaiting():
			return
		formatConfig=config.conf["documentFormatting"].copy()
		formatConfig["reportTables"]=True
		formatConfig["includeLayoutTables"]=True
		try:
			tableID, origRow, origCol, origRowSpan, origColSpan = self._getTableCellCoords(self.selection)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# when the cursor is not within a table.
			ui.message(_("Not in a table cell"))
			return

		try:
			info = self._getNearestTableCell(tableID, self.selection, origRow, origCol, origRowSpan, origColSpan, movement, axis)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# but the cursor can't be moved in that direction because it is at the edge of the table.
			ui.message(_("Edge of table"))
			# Retrieve the cell on which we started.
			info = next(self._iterTableCells(tableID, row=origRow, column=origCol))

		speech.speakTextInfo(info,formatConfig=formatConfig,reason=controlTypes.REASON_CARET)
		info.collapse()
		self.selection = info

	def script_nextRow(self, gesture):
		self._tableMovementScriptHelper(axis="row", movement="next")
	# Translators: the description for the next table row script on virtualBuffers.
	script_nextRow.__doc__ = _("moves to the next table row")


	def script_previousRow(self, gesture):
		self._tableMovementScriptHelper(axis="row", movement="previous")
	# Translators: the description for the previous table row script on virtualBuffers.
	script_previousRow.__doc__ = _("moves to the previous table row")

	def script_nextColumn(self, gesture):
		self._tableMovementScriptHelper(axis="column", movement="next")
	# Translators: the description for the next table column script on virtualBuffers.
	script_nextColumn.__doc__ = _("moves to the next table column")

	def script_previousColumn(self, gesture):
		self._tableMovementScriptHelper(axis="column", movement="previous")
	# Translators: the description for the previous table column script on virtualBuffers.
	script_previousColumn.__doc__ = _("moves to the previous table column")

	def _isSuitableNotLinkBlock(self,range):
		return (range._endOffset-range._startOffset)>=self.NOT_LINK_BLOCK_MIN_LEN

	def getEnclosingContainerRange(self,range):
		formatConfig=config.conf['documentFormatting'].copy()
		formatConfig.update({"reportBlockQuotes":True,"reportTables":True,"reportLists":True,"reportFrames":True})
		controlFields=[]
		for cmd in range.getTextWithFields():
			if not isinstance(cmd,textInfos.FieldCommand) or cmd.command!="controlStart":
				break
			controlFields.append(cmd.field)
		containerField=None
		while controlFields:
			field=controlFields.pop()
			if field.getPresentationCategory(controlFields,formatConfig)==field.PRESCAT_CONTAINER:
				containerField=field
				break
		if not containerField: return None
		docHandle=int(containerField['controlIdentifier_docHandle'])
		ID=int(containerField['controlIdentifier_ID'])
		offsets=range._getOffsetsFromFieldIdentifier(docHandle,ID)
		return self.makeTextInfo(textInfos.offsets.Offsets(*offsets))

	@classmethod
	def changeNotify(cls, rootDocHandle, rootID):
		try:
			queueHandler.queueFunction(queueHandler.eventQueue, cls.rootIdentifiers[rootDocHandle, rootID]._handleUpdate)
		except KeyError:
			pass

	def _handleUpdate(self):
		"""Handle an update to this buffer.
		"""
		braille.handler.handleUpdate(self)

	def getControlFieldForNVDAObject(self, obj):
		docHandle, objId = self.getIdentifierFromNVDAObject(obj)
		objId = unicode(objId)
		info = self.makeTextInfo(obj)
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		for item in info.getTextWithFields():
			if not isinstance(item, textInfos.FieldCommand) or not item.field:
				continue
			fieldId = item.field.get("controlIdentifier_ID")
			if fieldId == objId:
				return item.field
		raise LookupError

	__gestures = {
		"kb:NVDA+f5": "refreshBuffer",
		"kb:NVDA+v": "toggleScreenLayout",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+alt+leftArrow": "previousColumn",
	}
