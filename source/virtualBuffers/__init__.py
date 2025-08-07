# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2023 NV Access Limited, Peter Vágner, Cyrille Bougot

import time
import threading
import ctypes
import collections  # noqa: F401
import itertools  # noqa: F401
from typing import (
	Optional,
	Dict,
)
import weakref
import wx
import review  # noqa: F401
import NVDAHelper
import XMLFormatting
import scriptHandler
from scriptHandler import script
import speech  # noqa: F401
import NVDAObjects  # noqa: F401
import api
import controlTypes
import textInfos.offsets
import config
import cursorManager  # noqa: F401
import browseMode
import gui  # noqa: F401
import eventHandler  # noqa: F401
import braille
import queueHandler
from logHandler import log
import ui
import aria  # noqa: F401
import treeInterceptorHandler  # noqa: F401
import watchdog
from abc import abstractmethod
import documentBase


VBufStorage_findDirection_forward = 0
VBufStorage_findDirection_back = 1
VBufStorage_findDirection_up = 2
VBufRemote_nodeHandle_t = ctypes.c_ulonglong


class VBufStorage_findMatch_word(str):
	pass


VBufStorage_findMatch_notEmpty = object()

FINDBYATTRIBS_ESCAPE_TABLE = {
	# Symbols that are escaped in the attributes string.
	ord(":"): r"\\:",
	ord(";"): r"\\;",
	ord("\\"): "\\\\\\\\",
}
# Symbols that must be escaped for a regular expression.
FINDBYATTRIBS_ESCAPE_TABLE.update({(ord(s), "\\" + s) for s in "^$.*+?()[]{}|"})


def _prepareForFindByAttributes(attribs):
	# A lambda that coerces a value to a string and escapes characters suitable for a regular expression.
	escape = lambda val: str(val).translate(FINDBYATTRIBS_ESCAPE_TABLE)  # noqa: E731
	reqAttrs = []
	regexp = []
	if isinstance(attribs, dict):
		# Single option.
		attribs = (attribs,)
	# All options will match against all requested attributes,
	# so first build the list of requested attributes.
	for option in attribs:
		for name in option:
			reqAttrs.append(name)
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
				optRegexp.append("(?:")
				optRegexp.append("|".join((escape(val) + ";") if val is not None else ";" for val in values))
				optRegexp.append(")")
		regexp.append("".join(optRegexp))
	return " ".join(reqAttrs), "|".join(regexp)


class VirtualBufferQuickNavItem(browseMode.TextInfoQuickNavItem):
	def __init__(self, itemType, document, vbufNode, startOffset, endOffset):
		textInfo = document.makeTextInfo(textInfos.offsets.Offsets(startOffset, endOffset))
		super(VirtualBufferQuickNavItem, self).__init__(itemType, document, textInfo)
		docHandle = ctypes.c_int()
		ID = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getIdentifierFromControlFieldNode(
			document.VBufHandle,
			vbufNode,
			ctypes.byref(docHandle),
			ctypes.byref(ID),
		)
		self.vbufFieldIdentifier = (docHandle.value, ID.value)
		self.vbufNode = vbufNode

	@property
	def obj(self):
		return self.document.getNVDAObjectFromIdentifier(*self.vbufFieldIdentifier)

	@property
	def label(self):
		attrs = {}

		def propertyGetter(prop):
			if not attrs:
				# Lazily fetch the attributes the first time they're needed.
				# We do this because we don't want to do this if they're not needed at all.
				attrs.update(
					self.textInfo._getControlFieldAttribs(
						self.vbufFieldIdentifier[0],
						self.vbufFieldIdentifier[1],
					),
				)
			return attrs.get(prop)

		return self._getLabelForProperties(propertyGetter)

	def isChild(self, parent):
		if self.itemType == "heading":
			try:
				if int(
					self.textInfo._getControlFieldAttribs(
						self.vbufFieldIdentifier[0],
						self.vbufFieldIdentifier[1],
					)["level"],
				) > int(
					parent.textInfo._getControlFieldAttribs(
						parent.vbufFieldIdentifier[0],
						parent.vbufFieldIdentifier[1],
					)["level"],
				):
					return True
			except (KeyError, ValueError, TypeError):
				return False
		return super(VirtualBufferQuickNavItem, self).isChild(parent)


class VirtualBufferTextInfo(browseMode.BrowseModeDocumentTextInfo, textInfos.offsets.OffsetsTextInfo):
	allowMoveToOffsetPastEnd = False  #: no need for end insertion point as vbuf is not editable.

	def _getControlFieldAttribs(self, docHandle, id):
		info = self.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		for field in reversed(info.getTextWithFields()):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			if (
				int(attrs["controlIdentifier_docHandle"]) == docHandle
				and int(attrs["controlIdentifier_ID"]) == id
			):
				return attrs
		raise LookupError

	def _getFieldIdentifierFromOffset(self, offset):
		startOffset = ctypes.c_int()
		endOffset = ctypes.c_int()
		docHandle = ctypes.c_int()
		ID = ctypes.c_int()
		node = VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_locateControlFieldNodeAtOffset(
			self.obj.VBufHandle,
			offset,
			ctypes.byref(startOffset),
			ctypes.byref(endOffset),
			ctypes.byref(docHandle),
			ctypes.byref(ID),
			ctypes.byref(node),
		)
		if not any((docHandle.value, ID.value)):
			raise LookupError("Neither docHandle nor ID found for offset %d" % offset)
		return docHandle.value, ID.value

	def _getOffsetsFromFieldIdentifier(self, docHandle, ID):
		node = VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_getControlFieldNodeWithIdentifier(
			self.obj.VBufHandle,
			docHandle,
			ID,
			ctypes.byref(node),
		)
		if not node:
			raise LookupError
		start = ctypes.c_int()
		end = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getFieldNodeOffsets(
			self.obj.VBufHandle,
			node,
			ctypes.byref(start),
			ctypes.byref(end),
		)
		return start.value, end.value

	def _getBoundingRectFromOffset(self, offset):
		o = self._getNVDAObjectFromOffset(offset)
		if not o:
			raise LookupError("no NVDAObject at offset %d" % offset)
		if o.hasIrrelevantLocation:
			raise LookupError("Object is off screen, invisible or has no location")
		return o.location

	def _getNVDAObjectFromOffset(self, offset):
		try:
			docHandle, ID = self._getFieldIdentifierFromOffset(offset)
		except LookupError:
			log.debugWarning("Couldn't get NVDAObject from offset %d" % offset)
			return None
		return self.obj.getNVDAObjectFromIdentifier(docHandle, ID)

	def _getOffsetsFromNVDAObjectInBuffer(self, obj):
		docHandle, ID = self.obj.getIdentifierFromNVDAObject(obj)
		return self._getOffsetsFromFieldIdentifier(docHandle, ID)

	def _getOffsetsFromNVDAObject(self, obj):
		while True:
			try:
				return self._getOffsetsFromNVDAObjectInBuffer(obj)
			except LookupError:
				pass
			# Interactive list/combo box/tree view descendants aren't rendered into the buffer, even though they are still considered part of it.
			# Use the container in this case.
			obj = obj.parent
			if not obj or obj.role not in (
				controlTypes.Role.LIST,
				controlTypes.Role.COMBOBOX,
				controlTypes.Role.GROUPING,
				controlTypes.Role.TREEVIEW,
				controlTypes.Role.TREEVIEWITEM,
			):
				break
		raise LookupError

	def __init__(self, obj, position):
		self.obj = obj
		super(VirtualBufferTextInfo, self).__init__(obj, position)

	def _getSelectionOffsets(self):
		start = ctypes.c_int()
		end = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getSelectionOffsets(
			self.obj.VBufHandle,
			ctypes.byref(start),
			ctypes.byref(end),
		)
		return start.value, end.value

	def _setSelectionOffsets(self, start, end):
		NVDAHelper.localLib.VBuf_setSelectionOffsets(self.obj.VBufHandle, start, end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self, offset):
		return self._setSelectionOffsets(offset, offset)

	def _getStoryLength(self):
		return NVDAHelper.localLib.VBuf_getTextLength(self.obj.VBufHandle)

	def _getTextRange(self, start, end):
		if start == end:
			return ""
		return NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle, start, end, False) or ""

	def _getPlaceholderAttribute(self, attrs, placeholderAttrsKey):
		"""Gets the placeholder attribute to be used.
		@return: The placeholder attribute when there is no content within the ControlField.
		None when the ControlField has content.
		@note: The content is considered empty if it holds a single space.
		"""
		placeholder = attrs.get(placeholderAttrsKey)
		# For efficiency, only check if it is valid to return placeholder when we have a placeholder value to return.
		if not placeholder:
			return None
		# Get the start and end offsets for the field. This can be used to check if the field has any content.
		try:
			start, end = self._getOffsetsFromFieldIdentifier(
				int(attrs.get("controlIdentifier_docHandle")),
				int(attrs.get("controlIdentifier_ID")),
			)
		except (LookupError, ValueError):
			log.debugWarning("unable to get offsets used to fetch content")
			return placeholder
		else:
			valueLen = end - start
			if not valueLen:  # value is empty, use placeholder
				return placeholder
			# Because fetching the content of the field could result in a large amount of text
			# we only do it in order to check for space.
			# We first compare the length by comparing the offsets, if the length is less than 2 (ie
			# could hold space)
			if valueLen < 2:
				controlFieldText = self.obj.makeTextInfo(textInfos.offsets.Offsets(start, end)).text
				if not controlFieldText or controlFieldText == " ":
					return placeholder
		return None

	def _normalizeCommand(self, command: XMLFormatting.CommandsT) -> XMLFormatting.CommandsT:
		if not isinstance(command, textInfos.FieldCommand):
			return command  # no need to normalize str or None
		field = command.field
		if (
			isinstance(field, textInfos.ControlField)
			# #15830: only process controlStart commands.
			# Otherwise also processing controlEnd commands would double-process the same field attributes,
			# As controlStart and controlEnd commands now share the same field dictionary.
			and command.command == "controlStart"
		):
			command.field = self._normalizeControlField(field)
		elif isinstance(field, textInfos.FormatField):
			command.field = self._normalizeFormatField(field)
		return command

	def _getFieldsInRange(self, start: int, end: int) -> textInfos.TextInfo.TextWithFieldsT:
		text = NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle, start, end, True)
		if not text:
			return [""]
		commandList = XMLFormatting.XMLTextParser().parse(text)
		commandList = [
			self._normalizeCommand(command)
			for command in commandList
			# drop None to convert from XMLFormatting.CommandListT to textInfos.TextInfo.TextWithFieldsT
			if command is not None
		]
		return commandList

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.TextInfo.TextWithFieldsT:
		start = self._startOffset
		end = self._endOffset
		if start == end:
			return ""
		return self._getFieldsInRange(start, end)

	def _getWordOffsets(self, offset):
		# Use VBuf_getBufferLineOffsets with out screen layout to find out the range of the current field
		lineStart = ctypes.c_int()
		lineEnd = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(
			self.obj.VBufHandle,
			offset,
			0,
			False,
			ctypes.byref(lineStart),
			ctypes.byref(lineEnd),
		)
		word_startOffset, word_endOffset = super(VirtualBufferTextInfo, self)._getWordOffsets(offset)
		return (max(lineStart.value, word_startOffset), min(lineEnd.value, word_endOffset))

	def _getLineOffsets(self, offset):
		lineStart = ctypes.c_int()
		lineEnd = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(
			self.obj.VBufHandle,
			offset,
			config.conf["virtualBuffers"]["maxLineLength"],
			config.conf["virtualBuffers"]["useScreenLayout"],
			ctypes.byref(lineStart),
			ctypes.byref(lineEnd),
		)
		return lineStart.value, lineEnd.value

	def _getParagraphOffsets(self, offset):
		lineStart = ctypes.c_int()
		lineEnd = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(
			self.obj.VBufHandle,
			offset,
			0,
			True,
			ctypes.byref(lineStart),
			ctypes.byref(lineEnd),
		)
		return lineStart.value, lineEnd.value

	def _normalizeControlField(self, attrs: textInfos.ControlField):
		tableLayout = attrs.get("table-layout")
		if tableLayout:
			attrs["table-layout"] = tableLayout == "1"

		# convert some table attributes to ints
		for attr in (
			"table-id",
			"table-rownumber",
			"table-columnnumber",
			"table-rowsspanned",
			"table-columnsspanned",
			"table-rowcount",
			"table-columncount",
		):
			attrVal = attrs.get(attr)
			if attrVal is not None:
				attrs[attr] = int(attrVal)

		isHidden = attrs.get("isHidden")
		if isHidden:
			attrs["isHidden"] = isHidden == "1"

		# Handle table row and column headers.
		for axis in "row", "column":
			attr = attrs.pop("table-%sheadercells" % axis, None)
			if not attr:
				continue
			cellIdentifiers = [identifier.split(",") for identifier in attr.split(";") if identifier]
			# Get the text for the header cells.
			textList = []
			for docHandle, ID in cellIdentifiers:
				if (
					attrs.get("controlIdentifier_docHandle") == docHandle
					and attrs.get("controlIdentifier_ID") == ID
				):
					# This is a self-reference to a column or row header
					# Do not double up the cell header name. This is happening in Chrome.
					continue
				try:
					start, end = self._getOffsetsFromFieldIdentifier(int(docHandle), int(ID))
				except (LookupError, ValueError):
					continue
				textList.append(self.obj.makeTextInfo(textInfos.offsets.Offsets(start, end)).text)
			attrs["table-%sheadertext" % axis] = "\n".join(textList)

		if attrs.get("role") in (controlTypes.Role.LANDMARK, controlTypes.Role.REGION):
			attrs["alwaysReportName"] = True

		# Expose a unique ID on the controlField for quick and safe comparison using the virtualBuffer field's docHandle and ID
		docHandle = attrs.get("controlIdentifier_docHandle")
		ID = attrs.get("controlIdentifier_ID")
		if docHandle is not None and ID is not None:
			attrs["uniqueID"] = (docHandle, ID)

		return attrs

	def _normalizeFormatField(self, attrs: textInfos.FormatField):
		strippedCharsFromStart = attrs.get("strippedCharsFromStart")
		if strippedCharsFromStart is not None:
			assert strippedCharsFromStart.isdigit(), (
				"strippedCharsFromStart isn't a digit, %r" % strippedCharsFromStart
			)
			attrs["strippedCharsFromStart"] = int(strippedCharsFromStart)
		return attrs

	def _getLineNumFromOffset(self, offset):
		return None

	def _get_fieldIdentifierAtStart(self):
		return self._getFieldIdentifierFromOffset(self._startOffset)

	def _getUnitOffsets(self, unit, offset):
		if unit == textInfos.UNIT_CONTROLFIELD:
			startOffset = ctypes.c_int()
			endOffset = ctypes.c_int()
			docHandle = ctypes.c_int()
			ID = ctypes.c_int()
			node = VBufRemote_nodeHandle_t()
			NVDAHelper.localLib.VBuf_locateControlFieldNodeAtOffset(
				self.obj.VBufHandle,
				offset,
				ctypes.byref(startOffset),
				ctypes.byref(endOffset),
				ctypes.byref(docHandle),
				ctypes.byref(ID),
				ctypes.byref(node),
			)
			return startOffset.value, endOffset.value
		elif unit == textInfos.UNIT_FORMATFIELD:
			startOffset = ctypes.c_int()
			endOffset = ctypes.c_int()
			node = VBufRemote_nodeHandle_t()
			NVDAHelper.localLib.VBuf_locateTextFieldNodeAtOffset(
				self.obj.VBufHandle,
				offset,
				ctypes.byref(startOffset),
				ctypes.byref(endOffset),
				ctypes.byref(node),
			)
			return startOffset.value, endOffset.value
		return super(VirtualBufferTextInfo, self)._getUnitOffsets(unit, offset)

	def _get_clipboardText(self):
		# Blocks should start on a new line, but they don't necessarily have an end of line indicator.
		# Therefore, get the text in block (paragraph) chunks and join the chunks with \r\n.
		blocks = (block.strip("\r\n") for block in self.getTextInChunks(textInfos.UNIT_PARAGRAPH))
		return "\r\n".join(blocks)

	def activate(self):
		self.obj._activatePosition(info=self)

	def getMathMl(self, field):
		docHandle = int(field["controlIdentifier_docHandle"])
		nodeId = int(field["controlIdentifier_ID"])
		obj = self.obj.getNVDAObjectFromIdentifier(docHandle, nodeId)
		return obj.mathMl


class VirtualBuffer(browseMode.BrowseModeDocumentTreeInterceptor):
	TextInfo = VirtualBufferTextInfo

	# As NVDA manages the caret virtually,
	# It is necessary for 'gainFocus' events to update the caret.
	_focusEventMustUpdateCaretPosition = True

	#: Maps root identifiers (docHandle and ID) to buffers.
	rootIdentifiers = weakref.WeakValueDictionary()

	def __init__(self, rootNVDAObject, backendName=None):
		super(VirtualBuffer, self).__init__(rootNVDAObject)
		self.backendName = backendName
		self.VBufHandle = None
		self.isLoading = False
		self.rootDocHandle, self.rootID = self.getIdentifierFromNVDAObject(self.rootNVDAObject)
		self.rootIdentifiers[self.rootDocHandle, self.rootID] = self

	def prepare(self):
		if not self.rootNVDAObject.appModule.helperLocalBindingHandle:
			# #5758: If NVDA starts with a document already in focus, there will have been no focus event to inject nvdaHelper yet.
			# So at very least don't try to prepare a virtualBuffer as it will fail.
			# The user will most likely need to manually move focus away and back again to allow this virtualBuffer to work.
			log.debugWarning(
				"appModule has no binding handle to injected code, can't prepare virtualBuffer yet.",
			)
			return
		self.shouldPrepare = False
		self.loadBuffer()

	def _get_shouldPrepare(self):
		return not self.isLoading and not self.VBufHandle

	def terminate(self):
		super(VirtualBuffer, self).terminate()
		if not self.VBufHandle:
			return
		self.unloadBuffer()

	def _get_isReady(self):
		return bool(self.VBufHandle and not self.isLoading)

	def loadBuffer(self):
		self.isLoading = True
		self._loadProgressCallLater = wx.CallLater(1000, self._loadProgress)
		threading.Thread(
			name=f"{self.__class__.__module__}.{self.loadBuffer.__qualname__}",
			target=self._loadBuffer,
			daemon=True,
		).start()

	def _loadBuffer(self):
		try:
			if log.isEnabledFor(log.DEBUG):
				startTime = time.time()
			self.VBufHandle = NVDAHelper.localLib.VBuf_createBuffer(
				self.rootNVDAObject.appModule.helperLocalBindingHandle,
				self.rootDocHandle,
				self.rootID,
				self.backendName,
			)
			if not self.VBufHandle:
				raise RuntimeError("Could not remotely create virtualBuffer")
		except:  # noqa: E722
			log.error("", exc_info=True)
			queueHandler.queueFunction(queueHandler.eventQueue, self._loadBufferDone, success=False)
			return
		if log.isEnabledFor(log.DEBUG):
			log.debug(
				"Buffer load took %.3f sec, %d chars"
				% (
					time.time() - startTime,
					NVDAHelper.localLib.VBuf_getTextLength(self.VBufHandle),
				),
			)
		queueHandler.queueFunction(queueHandler.eventQueue, self._loadBufferDone)

	def _loadBufferDone(self, success=True):
		self._loadProgressCallLater.Stop()
		del self._loadProgressCallLater
		self.isLoading = False
		if not success:
			self.passThrough = True
			return
		textLength = NVDAHelper.localLib.VBuf_getTextLength(self.VBufHandle)
		if textLength == 0:
			log.debugWarning("Empty buffer. Waiting for documentLoadComplete event instead")
			# Empty buffer.
			# May be due to focus event too early in Chromium 100 documents
			# We may get a later chance to see content with a documentLoadComplete event
			return
		if self._hadFirstGainFocus:
			# If this buffer has already had focus once while loaded, this is a refresh.
			# Translators: Reported when a page reloads (example: after refreshing a webpage).
			ui.message(_("Refreshed"))
		if api.getFocusObject().treeInterceptor == self:
			self.event_treeInterceptor_gainFocus()

	def event_documentLoadComplete(self, obj, nextHandler):
		if not self._hadFirstGainFocus:
			# Any initial gainFocus events were too early to start reporting content in this buffer.
			# Therefore as we are now alerted the document load is complete,
			# We should handle the initial automatic say all etc.
			if api.getFocusObject().treeInterceptor == self:
				log.debug("Handling initial reporting of virtualBuffer via documentLoadComplete event")
				self.event_treeInterceptor_gainFocus()

	def _loadProgress(self):
		# Translators: Reported while loading a document.
		ui.message(_("Loading document..."))

	def unloadBuffer(self):
		if self.VBufHandle is not None:
			try:
				watchdog.cancellableExecute(
					NVDAHelper.localLib.VBuf_destroyBuffer,
					ctypes.byref(ctypes.c_int(self.VBufHandle)),
				)
			except WindowsError:
				pass
			self.VBufHandle = None

	def isNVDAObjectPartOfLayoutTable(self, obj):
		docHandle, ID = self.getIdentifierFromNVDAObject(obj)
		ID = str(ID)
		info = self.makeTextInfo(obj)
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		fieldCommands = [x for x in info.getTextWithFields() if isinstance(x, textInfos.FieldCommand)]
		tableLayout = None
		tableID = None
		for fieldCommand in fieldCommands:
			fieldID = fieldCommand.field.get("controlIdentifier_ID") if fieldCommand.field else None
			if fieldID == ID:
				tableLayout = fieldCommand.field.get("table-layout")
				if tableLayout is not None:
					return tableLayout
				tableID = fieldCommand.field.get("table-id")
				break
		if tableID is None:
			return False
		for fieldCommand in fieldCommands:
			fieldID = fieldCommand.field.get("controlIdentifier_ID") if fieldCommand.field else None
			if fieldID == tableID:
				tableLayout = fieldCommand.field.get("table-layout", False)
				break
		return tableLayout

	@abstractmethod
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

	@abstractmethod
	def getIdentifierFromNVDAObject(self, obj):
		"""Retreaves the virtualBuffer field identifier from an NVDAObject.
		@param obj: the NVDAObject to retreave the field identifier from.
		@type obj: L{NVDAObject}
		@returns: a the field identifier as a doc handle and ID paire.
		@rtype: 2-tuple.
		"""
		raise NotImplementedError

	def script_refreshBuffer(self, gesture):
		if scriptHandler.isScriptWaiting():
			# This script may cause subsequently queued scripts to fail, so don't execute.
			return
		self.unloadBuffer()
		self.loadBuffer()

	# Translators: the description for the refreshBuffer script on virtualBuffers.
	script_refreshBuffer.__doc__ = _("Refreshes the document content")

	@script(
		description=_(
			# Translators: the description for the toggleScreenLayout script on virtualBuffers.
			"Toggles on and off if the screen layout is preserved while rendering the document content",
		),
		gesture="kb:NVDA+v",
	)
	def script_toggleScreenLayout(self, gesture):
		config.conf["virtualBuffers"]["useScreenLayout"] = not config.conf["virtualBuffers"][
			"useScreenLayout"
		]
		if config.conf["virtualBuffers"]["useScreenLayout"]:
			# Translators: Presented when use screen layout option is toggled.
			ui.message(_("Use screen layout on"))
		else:
			# Translators: Presented when use screen layout option is toggled.
			ui.message(_("Use screen layout off"))

	def _searchableAttributesForNodeType(self, nodeType):
		pass

	def _iterNodesByType(self, nodeType, direction="next", pos=None):
		attribs = self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			raise NotImplementedError
		return self._iterNodesByAttribs(attribs, direction, pos, nodeType)

	def _iterNodesByAttribs(self, attribs, direction="next", pos=None, nodeType=None):
		offset = pos._startOffset if pos else -1
		reqAttrs, regexp = _prepareForFindByAttributes(attribs)
		startOffset = ctypes.c_int()
		endOffset = ctypes.c_int()
		if direction == "next":
			direction = VBufStorage_findDirection_forward
		elif direction == "previous":
			direction = VBufStorage_findDirection_back
		elif direction == "up":
			direction = VBufStorage_findDirection_up
		else:
			raise ValueError("unknown direction: %s" % direction)
		while True:
			try:
				node = VBufRemote_nodeHandle_t()
				NVDAHelper.localLib.VBuf_findNodeByAttributes(
					self.VBufHandle,
					offset,
					direction,
					reqAttrs,
					regexp,
					ctypes.byref(startOffset),
					ctypes.byref(endOffset),
					ctypes.byref(node),
				)
			except:  # noqa: E722
				return
			if not node:
				return
			yield VirtualBufferQuickNavItem(nodeType, self, node, startOffset.value, endOffset.value)
			offset = startOffset

	def _getTableCellAt(self, tableID, startPos, row, column):
		try:
			return next(self._iterTableCells(tableID, row=row, column=column))
		except StopIteration:
			raise LookupError

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

	def _getNearestTableCell(
		self,
		startPos: textInfos.TextInfo,
		cell: documentBase._TableCell,
		movement: documentBase._Movement,
		axis: documentBase._Axis,
	) -> textInfos.TextInfo:
		tableID, origRow, origCol, origRowSpan, origColSpan = (
			cell.tableID,
			cell.row,
			cell.col,
			cell.rowSpan,
			cell.colSpan,
		)
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
			return self._getTableCellAt(tableID, startPos, destRow, destCol)
		except LookupError:
			pass

		# Cells are grouped by row, so in most cases, we simply need to search in the right direction.
		for info in self._iterTableCells(tableID, direction=movement, startPos=startPos):
			cell = self._getTableCellCoords(info)
			if cell.row <= destRow < (cell.row + cell.rowSpan) and cell.col <= destCol < (
				cell.col + cell.colSpan
			):
				return info
			elif cell.row > destRow and movement == "next":
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
				cell = self._getTableCellCoords(info)
			if cell.row <= destRow < (cell.row + cell.rowSpan) and cell.col <= destCol < (
				cell.col + cell.colSpan
			):
				return info
			else:
				raise LookupError

	def _isSuitableNotLinkBlock(self, textRange):
		return (textRange._endOffset - textRange._startOffset) >= self.NOT_LINK_BLOCK_MIN_LEN

	def getEnclosingContainerRange(self, textRange):
		formatConfig = config.conf["documentFormatting"].copy()
		formatConfig.update(
			{"reportBlockQuotes": True, "reportTables": True, "reportLists": True, "reportFrames": True},
		)
		controlFields = []
		for cmd in textRange.getTextWithFields():
			if not isinstance(cmd, textInfos.FieldCommand) or cmd.command != "controlStart":
				break
			controlFields.append(cmd.field)
		containerField = None
		while controlFields:
			field = controlFields.pop()
			if field.getPresentationCategory(
				controlFields,
				formatConfig,
			) == field.PRESCAT_CONTAINER or field.get("landmark"):
				containerField = field
				break
		if not containerField:
			return None
		docHandle = int(containerField["controlIdentifier_docHandle"])
		ID = int(containerField["controlIdentifier_ID"])
		offsets = textRange._getOffsetsFromFieldIdentifier(docHandle, ID)
		return self.makeTextInfo(textInfos.offsets.Offsets(*offsets))

	@classmethod
	def changeNotify(cls, rootDocHandle, rootID):
		try:
			queueHandler.queueFunction(
				queueHandler.eventQueue,
				cls.rootIdentifiers[rootDocHandle, rootID]._handleUpdate,
			)
		except KeyError:
			pass

	def _handleUpdate(self):
		"""Handle an update to this buffer."""
		if not self.VBufHandle:
			# #4859: The buffer was unloaded after this method was queued.
			return
		braille.handler.handleUpdate(self)

	def getControlFieldForNVDAObject(self, obj):
		docHandle, objId = self.getIdentifierFromNVDAObject(obj)
		objId = str(objId)
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

	def _isNVDAObjectInApplication_noWalk(self, obj):
		inApp = super(VirtualBuffer, self)._isNVDAObjectInApplication_noWalk(obj)
		if inApp is not None:
			return inApp
		# If the object is in the buffer, it's definitely not in an application.
		try:
			docHandle, objId = self.getIdentifierFromNVDAObject(obj)
		except:  # noqa: E722
			log.debugWarning(
				"getIdentifierFromNVDAObject failed. Object probably died while walking ancestors.",
				exc_info=True,
			)
			return None
		node = VBufRemote_nodeHandle_t()
		if not self.VBufHandle:
			return None
		try:
			NVDAHelper.localLib.VBuf_getControlFieldNodeWithIdentifier(
				self.VBufHandle,
				docHandle,
				objId,
				ctypes.byref(node),
			)
		except WindowsError:
			return None
		if node:
			return False
		return None

	__gestures = {
		"kb:NVDA+f5": "refreshBuffer",
	}
