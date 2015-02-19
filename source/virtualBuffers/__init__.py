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
			elif values[0] is None:
				# There must be no value for this attribute.
				optRegexp.append(r";")
			elif isinstance(values[0], VBufStorage_findMatch_word):
				# Assume all are word matches.
				optRegexp.append(r"(?:\\;|[^;])*\b(?:")
				optRegexp.append("|".join(escape(val) for val in values))
				optRegexp.append(r")\b(?:\\;|[^;])*;")
			else:
				# Assume all are exact matches.
				optRegexp.append("(?:")
				optRegexp.append("|".join(escape(val) for val in values))
				optRegexp.append(");")
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

	canActivate=True
	def activate(self):
		self.textInfo.obj._activatePosition(self.textInfo)

	def moveTo(self):
		info=self.textInfo.copy()
		info.collapse()
		self.document._set_selection(info,reason=browseMode.REASON_QUICKNAV)

class VirtualBufferTextInfo(textInfos.offsets.OffsetsTextInfo):

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

	def getControlFieldSpeech(self, attrs, ancestorAttrs, fieldType, formatConfig=None, extraDetail=False, reason=None):
		textList = []
		landmark = attrs.get("landmark")
		if formatConfig["reportLandmarks"] and fieldType == "start_addedToControlFieldStack" and landmark:
			try:
				textList.append(attrs["name"])
			except KeyError:
				pass
			if landmark == "region":
				# The word landmark is superfluous for regions.
				textList.append(aria.landmarkRoles[landmark])
			else:
				textList.append(_("%s landmark") % aria.landmarkRoles[landmark])
		textList.append(super(VirtualBufferTextInfo, self).getControlFieldSpeech(attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason))
		return " ".join(textList)

	def getControlFieldBraille(self, field, ancestors, reportStart, formatConfig):
		textList = []
		landmark = field.get("landmark")
		if formatConfig["reportLandmarks"] and reportStart and landmark and field.get("_startOfNode"):
			try:
				textList.append(field["name"])
			except KeyError:
				pass
			if landmark == "region":
				# The word landmark is superfluous for regions.
				textList.append(aria.landmarkRoles[landmark])
			else:
				# Translators: This is spoken and brailled to indicate a landmark (example output: main landmark).
				textList.append(_("%s landmark") % aria.landmarkRoles[landmark])
		text = super(VirtualBufferTextInfo, self).getControlFieldBraille(field, ancestors, reportStart, formatConfig)
		if text:
			textList.append(text)
		return " ".join(textList)

	def _get_focusableNVDAObjectAtStart(self):
		try:
			item = next(self.obj._iterNodesByType("focusable", "up", self))
		except StopIteration:
			return self.obj.rootNVDAObject
		if not item:
			return self.obj.rootNVDAObject
		return self.obj.getNVDAObjectFromIdentifier(*item.vbufFieldIdentifier)

	def activate(self):
		self.obj._activatePosition(self)

	def getMathMl(self, field):
		docHandle = int(field["controlIdentifier_docHandle"])
		nodeId = int(field["controlIdentifier_ID"])
		obj = self.obj.getNVDAObjectFromIdentifier(docHandle, nodeId)
		return obj.mathMl

class VirtualBuffer(cursorManager.CursorManager, browseMode.BrowseModeTreeInterceptor):

	TextInfo=VirtualBufferTextInfo
	programmaticScrollMayFireEvent = False

	#: Maps root identifiers (docHandle and ID) to buffers.
	rootIdentifiers = weakref.WeakValueDictionary()

	def __init__(self,rootNVDAObject,backendName=None):
		super(VirtualBuffer,self).__init__(rootNVDAObject)
		self.backendName=backendName
		self.VBufHandle=None
		self.isLoading=False
		self.disableAutoPassThrough = False
		self.rootDocHandle,self.rootID=self.getIdentifierFromNVDAObject(self.rootNVDAObject)
		self._lastFocusObj = None
		self._hadFirstGainFocus = False
		self._lastProgrammaticScrollTime = None
		# We need to cache this because it will be unavailable once the document dies.
		self.documentConstantIdentifier = self.documentConstantIdentifier
		if not hasattr(self.rootNVDAObject.appModule, "_vbufRememberedCaretPositions"):
			self.rootNVDAObject.appModule._vbufRememberedCaretPositions = {}
		self._lastCaretPosition = None
		self.rootIdentifiers[self.rootDocHandle, self.rootID] = self
		self._enteringFromOutside = True

	def prepare(self):
		self.shouldPrepare=False
		self.loadBuffer()

	def _get_shouldPrepare(self):
		return not self.isLoading and not self.VBufHandle

	def terminate(self):
		if not self.VBufHandle:
			return

		if self.shouldRememberCaretPositionAcrossLoads and self._lastCaretPosition:
			try:
				self.rootNVDAObject.appModule._vbufRememberedCaretPositions[self.documentConstantIdentifier] = self._lastCaretPosition
			except AttributeError:
				# The app module died.
				pass

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
			speech.speakMessage(_("Refreshed"))
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

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

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

	def event_treeInterceptor_gainFocus(self):
		"""Triggered when this virtual buffer gains focus.
		This event is only fired upon entering this buffer when it was not the current buffer before.
		This is different to L{event_gainFocus}, which is fired when an object inside this buffer gains focus, even if that object is in the same buffer.
		"""
		doSayAll=False
		hadFirstGainFocus=self._hadFirstGainFocus
		if not hadFirstGainFocus:
			# This buffer is gaining focus for the first time.
			# Fake a focus event on the focus object, as the buffer may have missed the actual focus event.
			focus = api.getFocusObject()
			self.event_gainFocus(focus, lambda: focus.event_gainFocus())
			if not self.passThrough:
				# We only set the caret position if in browse mode.
				# If in focus mode, the document must have forced the focus somewhere,
				# so we don't want to override it.
				initialPos = self._getInitialCaretPos()
				if initialPos:
					self.selection = self.makeTextInfo(initialPos)
				browseMode.reportPassThrough(self)
				doSayAll=config.conf['virtualBuffers']['autoSayAllOnPageLoad']
			self._hadFirstGainFocus = True

		if not self.passThrough:
			if doSayAll:
				speech.speakObjectProperties(self.rootNVDAObject,name=True,states=True,reason=controlTypes.REASON_FOCUS)
				sayAllHandler.readText(sayAllHandler.CURSOR_CARET)
			else:
				# Speak it like we would speak focus on any other document object.
				# This includes when entering the treeInterceptor for the first time:
				if not hadFirstGainFocus:
					speech.speakObject(self.rootNVDAObject, reason=controlTypes.REASON_FOCUS)
				else:
					# And when coming in from an outside object
					# #4069 But not when coming up from a non-rendered descendant.
					ancestors=api.getFocusAncestors()
					fdl=api.getFocusDifferenceLevel()
					try:
						tl=ancestors.index(self.rootNVDAObject)
					except ValueError:
						tl=len(ancestors)
					if fdl<=tl:
						speech.speakObject(self.rootNVDAObject, reason=controlTypes.REASON_FOCUS)
				info = self.selection
				if not info.isCollapsed:
					speech.speakSelectionMessage(_("selected %s"), info.text)
				else:
					info.expand(textInfos.UNIT_LINE)
					speech.speakTextInfo(info, reason=controlTypes.REASON_CARET, unit=textInfos.UNIT_LINE)

		browseMode.reportPassThrough(self)
		braille.handler.handleGainFocus(self)

	def event_treeInterceptor_loseFocus(self):
		"""Triggered when this virtual buffer loses focus.
		This event is only fired when the focus moves to a new object which is not within this virtual buffer; i.e. upon leaving this virtual buffer.
		"""

	def event_caret(self, obj, nextHandler):
		if self.passThrough:
			nextHandler()

	def _activateNVDAObject(self, obj):
		"""Activate an object in response to a user request.
		This should generally perform the default action or click on the object.
		@param obj: The object to activate.
		@type obj: L{NVDAObjects.NVDAObject}
		"""
		obj.doAction()

	def _activateLongDesc(self,controlField):
		"""
		Activates (presents) the long description for a particular field (usually a graphic).
		@param controlField: the field who's long description should be activated. This field is guaranteed to have states containing HASLONGDESC state. 
		@type controlField: dict
		"""
		raise NotImplementedError

	def _activatePosition(self, info):
		obj = info.NVDAObjectAtStart
		if not obj:
			return
		if obj.role == controlTypes.ROLE_MATH:
			import mathPres
			try:
				return mathPres.interactWithMathMl(obj.mathMl)
			except (NotImplementedError, LookupError):
				pass
			return
		if self.shouldPassThrough(obj):
			obj.setFocus()
			self.passThrough = True
			browseMode.reportPassThrough(self)
		elif obj.role == controlTypes.ROLE_EMBEDDEDOBJECT or obj.role in self.APPLICATION_ROLES:
			obj.setFocus()
			speech.speakObject(obj, reason=controlTypes.REASON_FOCUS)
		else:
			self._activateNVDAObject(obj)

	def _set_selection(self, info, reason=controlTypes.REASON_CARET):
		super(VirtualBuffer, self)._set_selection(info)
		if isScriptWaiting() or not info.isCollapsed:
			return
		# Save the last caret position for use in terminate().
		# This must be done here because the buffer might be cleared just before terminate() is called,
		# causing the last caret position to be lost.
		caret = info.copy()
		caret.collapse()
		self._lastCaretPosition = caret.bookmark
		review.handleCaretMove(caret)
		if reason == controlTypes.REASON_FOCUS:
			focusObj = api.getFocusObject()
			if focusObj==self.rootNVDAObject:
				return
		else:
			focusObj=info.focusableNVDAObjectAtStart
			obj=info.NVDAObjectAtStart
			if not obj:
				log.debugWarning("Invalid NVDAObjectAtStart")
				return
			if obj==self.rootNVDAObject:
				return
			if focusObj and not eventHandler.isPendingEvents("gainFocus") and focusObj!=self.rootNVDAObject and focusObj != api.getFocusObject() and self._shouldSetFocusToObj(focusObj):
				focusObj.setFocus()
			obj.scrollIntoView()
			if self.programmaticScrollMayFireEvent:
				self._lastProgrammaticScrollTime = time.time()
		self.passThrough=self.shouldPassThrough(focusObj,reason=reason)
		# Queue the reporting of pass through mode so that it will be spoken after the actual content.
		queueHandler.queueFunction(queueHandler.eventQueue, browseMode.reportPassThrough, self)

	def _shouldSetFocusToObj(self, obj):
		"""Determine whether an object should receive focus.
		Subclasses may extend or override this method.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		"""
		return obj.role not in self.APPLICATION_ROLES and obj.isFocusable and obj.role!=controlTypes.ROLE_EMBEDDEDOBJECT

	def script_activateLongDesc(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand("character")
		for field in reversed(info.getTextWithFields()):
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				states=field.field.get('states')
				if states and controlTypes.STATE_HASLONGDESC in states:
					self._activateLongDesc(field.field)
					break
		else:
			# Translators: the message presented when the activateLongDescription script cannot locate a long description to activate.
			ui.message(_("No long description"))
	# Translators: the description for the activateLongDescription script on virtualBuffers.
	script_activateLongDesc.__doc__=_("Shows the long description at this position if one is found.")

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
			speech.speakMessage(_("use screen layout on"))
		else:
			# Translators: Presented when use screen layout option is toggled.
			speech.speakMessage(_("use screen layout off"))
	# Translators: the description for the toggleScreenLayout script on virtualBuffers.
	script_toggleScreenLayout.__doc__ = _("Toggles on and off if the screen layout is preserved while rendering the document content")

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType == "notLinkBlock":
			return self._iterNotLinkBlock(direction=direction, pos=pos)
		attribs=self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			return iter(())
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

	def shouldPassThrough(self, obj, reason=None):
		"""Determine whether pass through mode should be enabled or disabled for a given object.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@param reason: The reason for this query; one of the output reasons, L{REASON_QUICKNAV}, or C{None} for manual pass through mode activation by the user.
		@return: C{True} if pass through mode should be enabled, C{False} if it should be disabled.
		"""
		if reason and (
			self.disableAutoPassThrough
			or (reason == controlTypes.REASON_FOCUS and not config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"])
			or (reason == controlTypes.REASON_CARET and not config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"])
		):
			# This check relates to auto pass through and auto pass through is disabled, so don't change the pass through state.
			return self.passThrough
		if reason == browseMode.REASON_QUICKNAV:
			return False
		states = obj.states
		role = obj.role
		# Menus sometimes get focus due to menuStart events even though they don't report as focused/focusable.
		if not obj.isFocusable and controlTypes.STATE_FOCUSED not in states and role != controlTypes.ROLE_POPUPMENU:
			return False
		if controlTypes.STATE_READONLY in states and role not in (controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_COMBOBOX):
			return False
		if reason == controlTypes.REASON_CARET:
			return role == controlTypes.ROLE_EDITABLETEXT or (role == controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)
		if reason == controlTypes.REASON_FOCUS and role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_RADIOBUTTON, controlTypes.ROLE_TAB):
			return True
		if role in (controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_LIST, controlTypes.ROLE_SLIDER, controlTypes.ROLE_TABCONTROL, controlTypes.ROLE_MENUBAR, controlTypes.ROLE_POPUPMENU, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_SPINBUTTON, controlTypes.ROLE_TABLEROW, controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLEROWHEADER, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_CHECKMENUITEM, controlTypes.ROLE_RADIOMENUITEM) or controlTypes.STATE_EDITABLE in states:
			return True
		if reason == controlTypes.REASON_FOCUS:
			# If this is a focus change, pass through should be enabled for certain ancestor containers.
			while obj and obj != self.rootNVDAObject:
				if obj.role == controlTypes.ROLE_TOOLBAR:
					return True
				obj = obj.parent
		return False

	def event_caretMovementFailed(self, obj, nextHandler, gesture=None):
		if not self.passThrough or not gesture or not config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"]:
			return nextHandler()
		if gesture.mainKeyName in ("home", "end"):
			# Home, end, control+home and control+end should not disable pass through.
			return nextHandler()
		script = self.getScript(gesture)
		if not script:
			return nextHandler()

		# We've hit the edge of the focused control.
		# Therefore, move the virtual caret to the same edge of the field.
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(info.UNIT_CONTROLFIELD)
		if gesture.mainKeyName in ("leftArrow", "upArrow", "pageUp"):
			info.collapse()
		else:
			info.collapse(end=True)
			info.move(textInfos.UNIT_CHARACTER, -1)
		info.updateCaret()

		scriptHandler.queueScript(script, gesture)

	def script_disablePassThrough(self, gesture):
		if not self.passThrough or self.disableAutoPassThrough:
			return gesture.send()
		self.passThrough = False
		self.disableAutoPassThrough = False
		browseMode.reportPassThrough(self)
	script_disablePassThrough.ignoreTreeInterceptorPassThrough = True

	def script_collapseOrExpandControl(self, gesture):
		oldFocus = api.getFocusObject()
		oldFocusStates = oldFocus.states
		gesture.send()
		if controlTypes.STATE_COLLAPSED in oldFocusStates:
			self.passThrough = True
		elif not self.disableAutoPassThrough:
			self.passThrough = False
		browseMode.reportPassThrough(self)
	script_collapseOrExpandControl.ignoreTreeInterceptorPassThrough = True

	def _tabOverride(self, direction):
		"""Override the tab order if the virtual buffer caret is not within the currently focused node.
		This is done because many nodes are not focusable and it is thus possible for the virtual buffer caret to be unsynchronised with the focus.
		In this case, we want tab/shift+tab to move to the next/previous focusable node relative to the virtual buffer caret.
		If the virtual buffer caret is within the focused node, the tab/shift+tab key should be passed through to allow normal tab order navigation.
		Note that this method does not pass the key through itself if it is not overridden. This should be done by the calling script if C{False} is returned.
		@param direction: The direction in which to move.
		@type direction: str
		@return: C{True} if the tab order was overridden, C{False} if not.
		@rtype: bool
		"""
		focus = api.getFocusObject()
		try:
			focusInfo = self.makeTextInfo(focus)
		except:
			return False
		# We only want to override the tab order if the caret is not within the focused node.
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		#Only check that the caret is within the focus for things that ar not documents
		#As for documents we should always override
		if focus.role!=controlTypes.ROLE_DOCUMENT or controlTypes.STATE_EDITABLE in focus.states:
			# Expand to one character, as isOverlapping() doesn't yield the desired results with collapsed ranges.
			caretInfo.expand(textInfos.UNIT_CHARACTER)
			if focusInfo.isOverlapping(caretInfo):
				return False
		# If we reach here, we do want to override tab/shift+tab if possible.
		# Find the next/previous focusable node.
		try:
			item = next(self._iterNodesByType("focusable", direction, caretInfo))
		except StopIteration:
			return False
		obj=self.getNVDAObjectFromIdentifier(*item.vbufFieldIdentifier)
		newInfo=item.textInfo
		if obj == api.getFocusObject():
			# This node is already focused, so we need to move to and speak this node here.
			newCaret = newInfo.copy()
			newCaret.collapse()
			self._set_selection(newCaret,reason=controlTypes.REASON_FOCUS)
			if self.passThrough:
				obj.event_gainFocus()
			else:
				speech.speakTextInfo(newInfo,reason=controlTypes.REASON_FOCUS)
		else:
			# This node doesn't have the focus, so just set focus to it. The gainFocus event will handle the rest.
			obj.setFocus()
		return True

	def script_tab(self, gesture):
		if not self._tabOverride("next"):
			gesture.send()

	def script_shiftTab(self, gesture):
		if not self._tabOverride("previous"):
			gesture.send()

	def event_focusEntered(self,obj,nextHandler):
		if obj==self.rootNVDAObject:
			self._enteringFromOutside = True
		if self.passThrough:
			 nextHandler()

	def _shouldIgnoreFocus(self, obj):
		"""Determines whether focus on a given object should be ignored.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if focus on L{obj} should be ignored, C{False} otherwise.
		@rtype: bool
		"""
		return False

	def _postGainFocus(self, obj):
		"""Executed after a gainFocus within the virtual buffer.
		This will not be executed if L{event_gainFocus} determined that it should abort and call nextHandler.
		@param obj: The object that gained focus.
		@type obj: L{NVDAObjects.NVDAObject}
		"""

	def _replayFocusEnteredEvents(self):
		# We blocked the focusEntered events because we were in browse mode,
		# but now that we've switched to focus mode, we need to fire them.
		for parent in api.getFocusAncestors()[api.getFocusDifferenceLevel():]:
			try:
				parent.event_focusEntered()
			except:
				log.exception("Error executing focusEntered event: %s" % parent)

	def event_gainFocus(self, obj, nextHandler):
		enteringFromOutside=self._enteringFromOutside
		self._enteringFromOutside=False
		if not self.isReady:
			if self.passThrough:
				nextHandler()
			return
		if enteringFromOutside and not self.passThrough and self._lastFocusObj==obj:
			# We're entering the document from outside (not returning from an inside object/application; #3145)
			# and this was the last non-root node with focus, so ignore this focus event.
			# Otherwise, if the user switches away and back to this document, the cursor will jump to this node.
			# This is not ideal if the user was positioned over a node which cannot receive focus.
			return
		if obj==self.rootNVDAObject:
			if self.passThrough:
				return nextHandler()
			return 
		if not self.passThrough and self._shouldIgnoreFocus(obj):
			return
		self._lastFocusObj=obj

		try:
			focusInfo = self.makeTextInfo(obj)
		except:
			# This object is not in the virtual buffer, even though it resides beneath the document.
			# Automatic pass through should be enabled in certain circumstances where this occurs.
			if not self.passThrough and self.shouldPassThrough(obj,reason=controlTypes.REASON_FOCUS):
				self.passThrough=True
				browseMode.reportPassThrough(self)
				self._replayFocusEnteredEvents()
			return nextHandler()

		#We only want to update the caret and speak the field if we're not in the same one as before
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		if not self._hadFirstGainFocus or not focusInfo.isOverlapping(caretInfo):
			# The virtual buffer caret is not within the focus node.
			oldPassThrough=self.passThrough
			passThrough=self.shouldPassThrough(obj,reason=controlTypes.REASON_FOCUS)
			if not oldPassThrough and (passThrough or sayAllHandler.isRunning()):
				# If pass-through is disabled, cancel speech, as a focus change should cause page reading to stop.
				# This must be done before auto-pass-through occurs, as we want to stop page reading even if pass-through will be automatically enabled by this focus change.
				speech.cancelSpeech()
			self.passThrough=passThrough
			if not self.passThrough:
				# We read the info from the buffer instead of the control itself.
				speech.speakTextInfo(focusInfo,reason=controlTypes.REASON_FOCUS)
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,controlTypes.REASON_ONLYCACHE)
			else:
				if not oldPassThrough:
					self._replayFocusEnteredEvents()
				nextHandler()
			focusInfo.collapse()
			self._set_selection(focusInfo,reason=controlTypes.REASON_FOCUS)
		else:
			# The virtual buffer caret was already at the focused node.
			if not self.passThrough:
				# This focus change was caused by a virtual caret movement, so don't speak the focused node to avoid double speaking.
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,controlTypes.REASON_ONLYCACHE)
			else:
				return nextHandler()

		self._postGainFocus(obj)

	event_gainFocus.ignoreIsReady=True

	def _handleScrollTo(self, obj):
		"""Handle scrolling the buffer to a given object in response to an event.
		Subclasses should call this from an event which indicates that the buffer has scrolled.
		@postcondition: The buffer caret is moved to L{obj} and the buffer content for L{obj} is reported.
		@param obj: The object to which the buffer should scroll.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if the buffer was scrolled, C{False} if not.
		@rtype: bool
		@note: If C{False} is returned, calling events should probably call their nextHandler.
		"""
		if self.programmaticScrollMayFireEvent and self._lastProgrammaticScrollTime and time.time() - self._lastProgrammaticScrollTime < 0.4:
			# This event was probably caused by this buffer's call to scrollIntoView().
			# Therefore, ignore it. Otherwise, the cursor may bounce back to the scroll point.
			# However, pretend we handled it, as we don't want it to be passed on to the object either.
			return True

		try:
			scrollInfo = self.makeTextInfo(obj)
		except:
			return False

		#We only want to update the caret and speak the field if we're not in the same one as before
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		if not scrollInfo.isOverlapping(caretInfo):
			if scrollInfo.isCollapsed:
				scrollInfo.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(scrollInfo,reason=controlTypes.REASON_CARET)
			scrollInfo.collapse()
			self.selection = scrollInfo
			return True

		return False

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
			ui.message(_("edge of table"))
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

	APPLICATION_ROLES = (controlTypes.ROLE_APPLICATION, controlTypes.ROLE_DIALOG)
	def _isNVDAObjectInApplication(self, obj):
		"""Determine whether a given object is within an application.
		The object is considered to be within an application if it or one of its ancestors has an application role.
		This should only be called on objects beneath the buffer's root NVDAObject.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if L{obj} is within an application, C{False} otherwise.
		@rtype: bool
		"""
		while obj and obj != self.rootNVDAObject:
			if obj.role in self.APPLICATION_ROLES:
				return True
			obj = obj.parent
		return False

	NOT_LINK_BLOCK_MIN_LEN = 30
	def _iterNotLinkBlock(self, direction="next", pos=None):
		links = self._iterNodesByType("link", direction=direction, pos=pos)
		# We want to compare each link against the next link.
		item1 = next(links)
		while True:
			item2 = next(links)
			# If the distance between the links is small, this is probably just a piece of non-link text within a block of links; e.g. an inactive link of a nav bar.
			if direction == "next" and item2.textInfo._startOffset - item1.textInfo._endOffset > self.NOT_LINK_BLOCK_MIN_LEN:
				yield VirtualBufferQuickNavItem("notLinkBlock",self,0,item1.textInfo._endOffset, item2.textInfo._startOffset)
			# If we're moving backwards, the order of the links in the document will be reversed.
			elif direction == "previous" and item1.textInfo._startOffset - item2.textInfo._endOffset > self.NOT_LINK_BLOCK_MIN_LEN:
				yield VirtualBufferQuickNavItem("notLinkBlock",self,0,item2.textInfo._endOffset, item1.textInfo._startOffset)
			item1=item2

	def _getInitialCaretPos(self):
		"""Retrieve the initial position of the caret after the buffer has been loaded.
		This position, if any, will be passed to L{makeTextInfo}.
		Subclasses should extend this method.
		@return: The initial position of the caret, C{None} if there isn't one.
		@rtype: TextInfo position
		"""
		if self.shouldRememberCaretPositionAcrossLoads:
			try:
				return self.rootNVDAObject.appModule._vbufRememberedCaretPositions[self.documentConstantIdentifier]
			except KeyError:
				pass
		return None

	def _get_documentConstantIdentifier(self):
		"""Get the constant identifier for this document.
		This identifier should uniquely identify all instances (not just one instance) of a document for at least the current session of the hosting application.
		Generally, the document URL should be used.
		@return: The constant identifier for this document, C{None} if there is none.
		"""
		return None

	def _get_shouldRememberCaretPositionAcrossLoads(self):
		"""Specifies whether the position of the caret should be remembered when this document is loaded again.
		This is useful when the browser remembers the scroll position for the document,
		but does not communicate this information via APIs.
		The remembered caret position is associated with this document using L{documentConstantIdentifier}.
		@return: C{True} if the caret position should be remembered, C{False} if not.
		@rtype: bool
		"""
		docConstId = self.documentConstantIdentifier
		# Return True if the URL indicates that this is probably a web browser document.
		# We do this check because we don't want to remember caret positions for email messages, etc.
		return isinstance(docConstId, basestring) and docConstId.split("://", 1)[0] in ("http", "https", "ftp", "ftps", "file")

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

	def script_moveToStartOfContainer(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		container=self.getEnclosingContainerRange(info)
		if not container:
			# Translators: Reported when the user attempts to move to the start or end of a container (list, table, etc.) 
			# But there is no container. 
			ui.message(_("Not in a container"))
			return
		container.collapse()
		self._set_selection(container, reason=browseMode.REASON_QUICKNAV)
		if not willSayAllResume(gesture):
			container.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(container, reason=controlTypes.REASON_FOCUS)
	script_moveToStartOfContainer.resumeSayAllMode=sayAllHandler.CURSOR_CARET
	# Translators: Description for the Move to start of container command in browse mode. 
	script_moveToStartOfContainer.__doc__=_("Moves to the start of the container element, such as a list or table")

	def script_movePastEndOfContainer(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		container=self.getEnclosingContainerRange(info)
		if not container:
			ui.message(_("Not in a container"))
			return
		container.collapse(end=True)
		if container._startOffset>=container._getStoryLength():
			container.move(textInfos.UNIT_CHARACTER,-1)
			# Translators: a message reported when:
			# Review cursor is at the bottom line of the current navigator object.
			# Landing at the end of a browse mode document when trying to jump to the end of the current container. 
			ui.message(_("bottom"))
		self._set_selection(container, reason=browseMode.REASON_QUICKNAV)
		if not willSayAllResume(gesture):
			container.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(container, reason=controlTypes.REASON_FOCUS)
	script_movePastEndOfContainer.resumeSayAllMode=sayAllHandler.CURSOR_CARET
	# Translators: Description for the Move past end of container command in browse mode. 
	script_movePastEndOfContainer.__doc__=_("Moves past the end  of the container element, such as a list or table")

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
		"kb:NVDA+d": "activateLongDesc",
		"kb:NVDA+f5": "refreshBuffer",
		"kb:NVDA+v": "toggleScreenLayout",
		"kb:escape": "disablePassThrough",
		"kb:alt+upArrow": "collapseOrExpandControl",
		"kb:alt+downArrow": "collapseOrExpandControl",
		"kb:tab": "tab",
		"kb:shift+tab": "shiftTab",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+alt+leftArrow": "previousColumn",
		"kb:shift+,": "moveToStartOfContainer",
		"kb:,": "movePastEndOfContainer",
	}

