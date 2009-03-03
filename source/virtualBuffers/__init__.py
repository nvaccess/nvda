import ctypes
import weakref
import time
import os
import XMLFormatting
import baseObject
from keyUtils import sendKey
import scriptHandler
from scriptHandler import isScriptWaiting
import speech
import NVDAObjects
import winUser
import api
import sayAllHandler
import controlTypes
import textHandler
import globalVars
import config
import api
import cursorManager
from gui import scriptUI
import virtualBufferHandler
import eventHandler
import braille
import queueHandler
from logHandler import log
import keyUtils

VBufStorage_findDirection_forward=0
VBufStorage_findDirection_back=1
VBufStorage_findDirection_up=2

def dictToMultiValueAttribsString(d):
	mainList=[]
	for k,v in d.iteritems():
		k=unicode(k).replace(':','\\:').replace(';','\\;').replace(',','\\,')
		valList=[]
		for i in v:
			if i is None:
				i=""
			else:
				i=unicode(i).replace(':','\\:').replace(';','\\;').replace(',','\\,')
			valList.append(i)
		attrib="%s:%s"%(k,",".join(valList))
		mainList.append(attrib)
	return "%s;"%";".join(mainList)

VBufClient=ctypes.cdll.LoadLibrary('lib/VBufClient.dll')

class VirtualBufferTextInfo(NVDAObjects.NVDAObjectTextInfo):

	UNIT_CONTROLFIELD = "controlField"

	def _getFieldIdentifierFromOffset(self, offset):
		startOffset = ctypes.c_int()
		endOffset = ctypes.c_int()
		docHandle = ctypes.c_int()
		ID = ctypes.c_int()
		VBufClient.VBufRemote_locateControlFieldNodeAtOffset(self.obj.VBufHandle, offset, ctypes.byref(startOffset), ctypes.byref(endOffset), ctypes.byref(docHandle), ctypes.byref(ID))
		return docHandle.value, ID.value

	def _getNVDAObjectFromOffset(self,offset):
		docHandle,ID=self._getFieldIdentifierFromOffset(offset)
		return self.obj.getNVDAObjectFromIdentifier(docHandle,ID)

	def _getOffsetsFromNVDAObject(self,obj):
		while obj and obj!=self.obj:
			try:
				docHandle,ID=self.obj.getIdentifierFromNVDAObject(obj)
				node = VBufClient.VBufRemote_getControlFieldNodeWithIdentifier(self.obj.VBufHandle, docHandle, ID)
				start = ctypes.c_int()
				end = ctypes.c_int()
				VBufClient.VBufRemote_getFieldNodeOffsets(self.obj.VBufHandle, node, ctypes.byref(start), ctypes.byref(end))
				return start.value, end.value
			except:
				log.debugWarning("",exc_info=True)
				obj=obj.parent

	def __init__(self,obj,position):
		self.obj=obj
		if isinstance(position,NVDAObjects.NVDAObject):
			start,end=self._getOffsetsFromNVDAObject(position)
			position=textHandler.Offsets(start,end)
		super(VirtualBufferTextInfo,self).__init__(obj,position)

	def _get_NVDAObjectAtStart(self):
		return self._getNVDAObjectFromOffset(self._startOffset)

	def _getSelectionOffsets(self):
		start=ctypes.c_int()
		end=ctypes.c_int()
		VBufClient.VBufRemote_getSelectionOffsets(self.obj.VBufHandle,ctypes.byref(start),ctypes.byref(end))
		return start.value,end.value

	def _setSelectionOffsets(self,start,end):
		VBufClient.VBufRemote_setSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return VBufClient.VBufRemote_getTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		if start==end:
			return ""
		text=ctypes.c_wchar_p()
		VBufClient.VBufRemote_getTextInRange(self.obj.VBufHandle,start,end,ctypes.byref(text),False)
		return text.value

	def getTextWithFields(self,formatConfig=None):
		start=self._startOffset
		end=self._endOffset
		if start==end:
			return ""
		text=ctypes.c_wchar_p()
		VBufClient.VBufRemote_getTextInRange(self.obj.VBufHandle,start,end,ctypes.byref(text),True)
		commandList=XMLFormatting.XMLTextParser().parse(text.value)
		for index in xrange(len(commandList)):
			if isinstance(commandList[index],textHandler.FieldCommand) and isinstance(commandList[index].field,textHandler.ControlField):
				commandList[index].field=self._normalizeControlField(commandList[index].field)
		return commandList

	def _getWordOffsets(self,offset):
		#Use VBufClient_getBufferLineOffsets with out screen layout to find out the range of the current field
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		VBufClient.VBufRemote_getLineOffsets(self.obj.VBufHandle,offset,0,False,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		word_startOffset,word_endOffset=super(VirtualBufferTextInfo,self)._getWordOffsets(offset)
		return (max(lineStart.value,word_startOffset),min(lineEnd.value,word_endOffset))

	def _getLineOffsets(self,offset):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		VBufClient.VBufRemote_getLineOffsets(self.obj.VBufHandle,offset,config.conf["virtualBuffers"]["maxLineLength"],config.conf["virtualBuffers"]["useScreenLayout"],ctypes.byref(lineStart),ctypes.byref(lineEnd))
		return lineStart.value,lineEnd.value
 
	def _getParagraphOffsets(self,offset):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		VBufClient.VBufRemote_getLineOffsets(self.obj.VBufHandle,offset,0,True,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		return lineStart.value,lineEnd.value

	def _normalizeControlField(self,attrs):
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
			VBufClient.VBufRemote_locateControlFieldNodeAtOffset(self.obj.VBufHandle,offset,ctypes.byref(startOffset),ctypes.byref(endOffset),ctypes.byref(docHandle),ctypes.byref(ID))
			return startOffset.value,endOffset.value
		return super(VirtualBufferTextInfo, self)._getUnitOffsets(unit, offset)

	def getXMLFieldSpeech(self,attrs,fieldType,extraDetail=False,reason=None):
		return speech.getXMLFieldSpeech(self,attrs,fieldType,extraDetail=extraDetail,reason=reason)

class VirtualBuffer(cursorManager.CursorManager):

	REASON_QUICKNAV = "quickNav"

	TextInfo=VirtualBufferTextInfo

	def __init__(self,rootNVDAObject,backendLibPath=None):
		self.backendLibPath=os.path.join(os.getcwd(),backendLibPath)
		self.rootNVDAObject=rootNVDAObject
		super(VirtualBuffer,self).__init__()
		self.VBufHandle=None
		self._passThrough=False
		self.disableAutoPassThrough = False
		self.rootDocHandle,self.rootID=self.getIdentifierFromNVDAObject(self.rootNVDAObject)
		self._lastFocusObj = None

	def _get_passThrough(self):
		return self._passThrough

	def _set_passThrough(self, state):
		if self._passThrough == state:
			return
		self._passThrough = state
		if state:
			braille.handler.handleGainFocus(api.getFocusObject())
		else:
			braille.handler.handleGainFocus(self)

	def loadBuffer(self):
		self.bindingHandle=VBufClient.VBufClient_connect(self.rootNVDAObject.processID)
		if not self.bindingHandle:
			raise RuntimeError("Could not inject VBuf lib")
		self.VBufHandle=VBufClient.VBufRemote_createBuffer(self.bindingHandle,self.rootDocHandle,self.rootID,self.backendLibPath)
		if not self.VBufHandle:
			raise RuntimeError("Could not remotely create virtualBuffer")

	def unloadBuffer(self):
		if self.VBufHandle is not None:
			try:
				VBufClient.VBufRemote_destroyBuffer(ctypes.byref(ctypes.c_int(self.VBufHandle)))
			except WindowsError:
				pass
			try:
				VBufClient.VBufClient_disconnect(self.bindingHandle)
			except WindowsError:
				pass
			self.VBufHandle=None

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def isNVDAObjectInVirtualBuffer(self,obj):
		pass

	def isAlive(self):
		pass

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

	def event_virtualBuffer_firstGainFocus(self):
		"""Triggered the first time this virtual buffer ever gains focus.
		"""
		speech.cancelSpeech()
		virtualBufferHandler.reportPassThrough(self)
		speech.speakObjectProperties(self.rootNVDAObject,name=True)
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		sayAllHandler.readText(info,sayAllHandler.CURSOR_CARET)

	def event_virtualBuffer_gainFocus(self):
		"""Triggered when this virtual buffer gains focus.
		This event is only fired upon entering this buffer when it was not the current buffer before.
		This is different to L{event_gainFocus}, which is fired when an object inside this buffer gains focus, even if that object is in the same buffer.
		"""
		virtualBufferHandler.reportPassThrough(self)
		braille.handler.handleGainFocus(self)

	def event_virtualBuffer_loseFocus(self):
		"""Triggered when this virtual buffer loses focus.
		This event is only fired when the focus moves to a new object which is not within this virtual buffer; i.e. upon leaving this virtual buffer.
		"""

	def event_becomeNavigatorObject(self, obj, nextHandler):
		if self.passThrough:
			nextHandler()

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

	def _activatePosition(self, info):
		obj = info.NVDAObjectAtStart
		if self.shouldPassThrough(obj):
			obj.setFocus()
			self.passThrough = True
			virtualBufferHandler.reportPassThrough(self)
		else:
			self._activateNVDAObject(obj)

	def _set_selection(self, info, reason=speech.REASON_CARET):
		super(VirtualBuffer, self)._set_selection(info)
		if isScriptWaiting() or not info.isCollapsed:
			return
		api.setReviewPosition(info)
		if reason == speech.REASON_FOCUS:
			obj = api.getFocusObject()
		else:
			obj = info.NVDAObjectAtStart
			if not obj:
				log.debugWarning("Invalid NVDAObjectAtStart")
				return
		if obj == self.rootNVDAObject:
			return
		if reason != speech.REASON_FOCUS:
			obj.scrollIntoView()
			if not eventHandler.isPendingEvents("gainFocus") and obj != api.getFocusObject() and self._shouldSetFocusToObj(obj):
				obj.setFocus()
		self.passThrough=self.shouldPassThrough(obj,reason=reason)
		# Queue the reporting of pass through mode so that it will be spoken after the actual content.
		queueHandler.queueFunction(queueHandler.eventQueue, virtualBufferHandler.reportPassThrough, self)

	def _shouldSetFocusToObj(self, obj):
		"""Determine whether an object should receive focus.
		Subclasses should override this method.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		"""
		return False

	def script_activatePosition(self,keyPress):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		self._activatePosition(info)
	script_activatePosition.__doc__ = _("activates the current object in the virtual buffer")

	def _caretMovementScriptHelper(self, *args, **kwargs):
		if self.VBufHandle is None:
			return 
		super(VirtualBuffer, self)._caretMovementScriptHelper(*args, **kwargs)

	def script_refreshBuffer(self,keyPress):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		self.unloadBuffer()
		self.loadBuffer()
		speech.speakMessage(_("Refreshed"))

	def script_toggleScreenLayout(self,keyPress):
		config.conf["virtualBuffers"]["useScreenLayout"]=not config.conf["virtualBuffers"]["useScreenLayout"]
		onOff=_("on") if config.conf["virtualBuffers"]["useScreenLayout"] else _("off")
		speech.speakMessage(_("use screen layout %s")%onOff)

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _iterNodesByType(self,nodeType,direction="next",offset=-1):
		attribs=self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			return
		attribs=dictToMultiValueAttribsString(attribs)
		startOffset=ctypes.c_int()
		endOffset=ctypes.c_int()
		if direction=="next":
			direction=VBufStorage_findDirection_forward
		elif direction=="previous":
			direction=VBufStorage_findDirection_back
		else:
			raise ValueError("unknown direction: %s"%direction)
		while True:
			try:
				node=VBufClient.VBufRemote_findNodeByAttributes(self.VBufHandle,offset,direction,attribs,ctypes.byref(startOffset),ctypes.byref(endOffset))
			except:
				return
			if not node:
				return
			yield node, startOffset.value, endOffset.value
			offset=startOffset

	def _quickNavScript(self,keyPress, nodeType, direction, errorMessage, readUnit):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		startOffset=info._startOffset
		endOffset=info._endOffset
		try:
			node, startOffset, endOffset = next(self._iterNodesByType(nodeType, direction, startOffset))
		except StopIteration:
			speech.speakMessage(errorMessage)
			return
		info = self.makeTextInfo(textHandler.Offsets(startOffset, endOffset))
		if readUnit:
			fieldInfo = info.copy()
			info.collapse()
			info.move(readUnit, 1, endPoint="end")
			if info.compareEndPoints(fieldInfo, "endToEnd") > 0:
				# We've expanded past the end of the field, so limit to the end of the field.
				info.setEndPoint(fieldInfo, "endToEnd")
		speech.speakTextInfo(info, reason=speech.REASON_FOCUS)
		info.collapse()
		self._set_selection(info, reason=self.REASON_QUICKNAV)

	@classmethod
	def addQuickNav(cls, nodeType, key, nextDoc, nextError, prevDoc, prevError, readUnit=None):
		scriptSuffix = nodeType[0].upper() + nodeType[1:]
		scriptName = "next%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,keyPress: self._quickNavScript(keyPress, nodeType, "next", nextError, readUnit)
		script.__doc__ = nextDoc
		script.__name__ = funcName
		setattr(cls, funcName, script)
		cls.bindKey(key, scriptName)
		scriptName = "previous%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,keyPress: self._quickNavScript(keyPress, nodeType, "previous", prevError, readUnit)
		script.__doc__ = prevDoc
		script.__name__ = funcName
		setattr(cls, funcName, script)
		cls.bindKey("shift+%s" % key, scriptName)

	def script_linksList(self,keyPress):
		if self.VBufHandle is None:
			return

		nodes = []
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		caretOffset=info._startOffset
		defaultIndex = None
		for node, startOffset, endOffset in self._iterNodesByType("link"):
			if defaultIndex is None:
				if startOffset <= caretOffset and caretOffset < endOffset:
					# The caret is inside this link, so make it the default selection.
					defaultIndex = len(nodes)
				elif startOffset > caretOffset:
					# The caret wasn't inside a link, so set the default selection to be the next link.
					defaultIndex = len(nodes)
			text = self.makeTextInfo(textHandler.Offsets(startOffset,endOffset)).text
			nodes.append((text, startOffset, endOffset))

		def action(args):
			if args is None:
				return
			activate, index, text = args
			text, startOffset, endOffset = nodes[index]
			info=self.makeTextInfo(textHandler.Offsets(startOffset,endOffset))
			if activate:
				self._activatePosition(info)
			else:
				speech.cancelSpeech()
				speech.speakTextInfo(info,reason=speech.REASON_FOCUS)
				info.collapse()
				self.selection = info

		scriptUI.LinksListDialog(choices=[node[0] for node in nodes], default=defaultIndex if defaultIndex is not None else 0, callback=action).run()
	script_linksList.__doc__ = _("displays a list of links")

	def shouldPassThrough(self, obj, reason=None):
		"""Determine whether pass through mode should be enabled or disabled for a given object.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@param reason: The reason for this query; one of the speech reasons, L{REASON_QUICKNAV}, or C{None} for manual pass through mode activation by the user.
		@return: C{True} if pass through mode should be enabled, C{False} if it should be disabled.
		"""
		if reason and (
			self.disableAutoPassThrough
			or (reason == speech.REASON_FOCUS and not config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"])
			or (reason == speech.REASON_CARET and not config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"])
		):
			# This check relates to auto pass through and auto pass through is disabled, so don't change the pass through state.
			return self.passThrough
		if reason == self.REASON_QUICKNAV:
			return False
		states = obj.states
		if controlTypes.STATE_FOCUSABLE not in states or controlTypes.STATE_READONLY in states:
			return False
		role = obj.role
		if reason == speech.REASON_CARET:
			return role == controlTypes.ROLE_EDITABLETEXT
		if reason == speech.REASON_FOCUS and role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_RADIOBUTTON):
			return True
		if role in (controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_LIST, controlTypes.ROLE_SLIDER, controlTypes.ROLE_TABCONTROL, controlTypes.ROLE_TAB, controlTypes.ROLE_MENUBAR, controlTypes.ROLE_POPUPMENU, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_SPINBUTTON) or controlTypes.STATE_EDITABLE in states:
			return True
		return False

	def event_caretMovementFailed(self, obj, nextHandler, keyPress=None):
		if not self.passThrough or not keyPress or not config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"]:
			return nextHandler()
		if keyPress[1] in ("extendedhome", "extendedend"):
			# Home, end, control+home and control+end should not disable pass through.
			return nextHandler()
		script = self.getScript(keyPress)
		if not script:
			return nextHandler()

		# We've hit the edge of the focused control.
		# Therefore, move the virtual caret to the same edge of the field.
		info = self.makeTextInfo(textHandler.POSITION_CARET)
		info.expand(info.UNIT_CONTROLFIELD)
		if keyPress[1] in ("extendedleft", "extendedup", "extendedprior"):
			info.collapse()
		else:
			info.collapse(end=True)
			info.move(textHandler.UNIT_CHARACTER, -1)
		info.updateCaret()

		scriptHandler.queueScript(script, keyPress)

	def script_disablePassThrough(self, keyPress):
		if not self.passThrough or self.disableAutoPassThrough:
			return sendKey(keyPress)
		self.passThrough = False
		self.disableAutoPassThrough = False
		virtualBufferHandler.reportPassThrough(self)
	script_disablePassThrough.ignoreVirtualBufferPassThrough = True

	def script_collapseOrExpandControl(self, keyPress):
		sendKey(keyPress)
		if not self.passThrough:
			return
		self.passThrough = False
		virtualBufferHandler.reportPassThrough(self)
	script_collapseOrExpandControl.ignoreVirtualBufferPassThrough = True

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
		if self.VBufHandle is None:
			return False

		focus = api.getFocusObject()
		try:
			focusInfo = self.makeTextInfo(focus)
		except:
			return False
		# We only want to override the tab order if the caret is not within the focused node.
		caretInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't yield the desired results with collapsed ranges.
		caretInfo.expand(textHandler.UNIT_CHARACTER)
		if focusInfo.isOverlapping(caretInfo):
			return False

		# If we reach here, we do want to override tab/shift+tab if possible.
		# Find the next/previous focusable node.
		try:
			newNode, newStart, newEnd = next(self._iterNodesByType("focusable", direction, caretInfo._startOffset))
		except StopIteration:
			return False

		# Finally, focus the node.
		# TODO: Better way to get a field identifier from a node.
		newInfo = self.makeTextInfo(textHandler.Offsets(newStart, newEnd))
		obj = newInfo.NVDAObjectAtStart
		if obj == api.getFocusObject():
			# This node is already focused, so we need to move to and speak this node here.
			newCaret = newInfo.copy()
			newCaret.collapse()
			self._set_selection(newCaret,reason=speech.REASON_FOCUS)
			if self.passThrough:
				obj.event_gainFocus()
			else:
				speech.speakTextInfo(newInfo,reason=speech.REASON_FOCUS)
		else:
			# This node doesn't have the focus, so just set focus to it. The gainFocus event will handle the rest.
			obj.setFocus()
		return True

	def script_tab(self, keyPress):
		if not self._tabOverride("next"):
			keyUtils.sendKey(keyPress)

	def script_shiftTab(self, keyPress):
		if not self._tabOverride("previous"):
			keyUtils.sendKey(keyPress)

	def event_focusEntered(self,obj,nextHandler):
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

	def event_gainFocus(self, obj, nextHandler):
		if not self.passThrough and self._lastFocusObj==obj:
			# This was the last non-document node with focus, so don't handle this focus event.
			# Otherwise, if the user switches away and back to this document, the cursor will jump to this node.
			# This is not ideal if the user was positioned over a node which cannot receive focus.
			return
		if self.VBufHandle is None:
			return nextHandler()
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
			if not self.passThrough and self.shouldPassThrough(obj,reason=speech.REASON_FOCUS):
				self.passThrough=True
				virtualBufferHandler.reportPassThrough(self)
			return nextHandler()

		#We only want to update the caret and speak the field if we're not in the same one as before
		caretInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textHandler.UNIT_CHARACTER)
		if not focusInfo.isOverlapping(caretInfo):
			if not self.passThrough:
				# If pass-through is disabled, cancel speech, as a focus change should cause page reading to stop.
				# This must be done before auto-pass-through occurs, as we want to stop page reading even if pass-through will be automatically enabled by this focus change.
				speech.cancelSpeech()
			self.passThrough=self.shouldPassThrough(obj,reason=speech.REASON_FOCUS)
			if not self.passThrough:
				# We read the info from the buffer instead of the control itself.
				speech.speakTextInfo(focusInfo,reason=speech.REASON_FOCUS)
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,speech.REASON_ONLYCACHE)
			else:
				nextHandler()
			focusInfo.collapse()
			self._set_selection(focusInfo,reason=speech.REASON_FOCUS)
		else:
			# The virtual buffer caret was already at the focused node.
			if not self.passThrough:
				# This focus change was caused by a virtual caret movement, so don't speak the focused node to avoid double speaking.
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,speech.REASON_ONLYCACHE)
			else:
				return nextHandler()

		self._postGainFocus(obj)

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
		if not self.VBufHandle:
			return False

		try:
			scrollInfo = self.makeTextInfo(obj)
		except:
			return False

		#We only want to update the caret and speak the field if we're not in the same one as before
		caretInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textHandler.UNIT_CHARACTER)
		if not scrollInfo.isOverlapping(caretInfo):
			speech.speakTextInfo(scrollInfo,reason=speech.REASON_CARET)
			scrollInfo.collapse()
			self.selection = scrollInfo
			return True

		return False

[VirtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in (
	("Return","activatePosition"),
	("Space","activatePosition"),
	("NVDA+f5","refreshBuffer"),
	("NVDA+v","toggleScreenLayout"),
	("NVDA+f7","linksList"),
	("escape","disablePassThrough"),
	("alt+extendedUp","collapseOrExpandControl"),
	("alt+extendedDown","collapseOrExpandControl"),
	("tab", "tab"),
	("shift+tab", "shiftTab"),
)]

# Add quick navigation scripts.
qn = VirtualBuffer.addQuickNav
qn("heading", key="h", nextDoc=_("moves to the next heading"), nextError=_("no next heading"),
	prevDoc=_("moves to the previous heading"), prevError=_("no previous heading"))
qn("heading1", key="1", nextDoc=_("moves to the next heading at level 1"), nextError=_("no next heading at level 1"),
	prevDoc=_("moves to the previous heading at level 1"), prevError=_("no previous heading at level 1"))
qn("heading2", key="2", nextDoc=_("moves to the next heading at level 2"), nextError=_("no next heading at level 2"),
	prevDoc=_("moves to the previous heading at level 2"), prevError=_("no previous heading at level 2"))
qn("heading3", key="3", nextDoc=_("moves to the next heading at level 3"), nextError=_("no next heading at level 3"),
	prevDoc=_("moves to the previous heading at level 3"), prevError=_("no previous heading at level 3"))
qn("heading4", key="4", nextDoc=_("moves to the next heading at level 4"), nextError=_("no next heading at level 4"),
	prevDoc=_("moves to the previous heading at level 4"), prevError=_("no previous heading at level 4"))
qn("heading5", key="5", nextDoc=_("moves to the next heading at level 5"), nextError=_("no next heading at level 5"),
	prevDoc=_("moves to the previous heading at level 5"), prevError=_("no previous heading at level 5"))
qn("heading6", key="6", nextDoc=_("moves to the next heading at level 6"), nextError=_("no next heading at level 6"),
	prevDoc=_("moves to the previous heading at level 6"), prevError=_("no previous heading at level 6"))
qn("table", key="t", nextDoc=_("moves to the next table"), nextError=_("no next table"),
	prevDoc=_("moves to the previous table"), prevError=_("no previous table"), readUnit=textHandler.UNIT_LINE)
qn("link", key="k", nextDoc=_("moves to the next link"), nextError=_("no next link"),
	prevDoc=_("moves to the previous link"), prevError=_("no previous link"))
qn("visitedLink", key="v", nextDoc=_("moves to the next visited link"), nextError=_("no next visited link"),
	prevDoc=_("moves to the previous visited link"), prevError=_("no previous visited link"))
qn("unvisitedLink", key="u", nextDoc=_("moves to the next unvisited link"), nextError=_("no next unvisited link"),
	prevDoc=_("moves to the previous unvisited link"), prevError=_("no previous unvisited link"))
qn("formField", key="f", nextDoc=_("moves to the next form field"), nextError=_("no next form field"),
	prevDoc=_("moves to the previous form field"), prevError=_("no previous form field"), readUnit=textHandler.UNIT_LINE)
qn("list", key="l", nextDoc=_("moves to the next list"), nextError=_("no next list"),
	prevDoc=_("moves to the previous list"), prevError=_("no previous list"), readUnit=textHandler.UNIT_LINE)
qn("listItem", key="i", nextDoc=_("moves to the next list item"), nextError=_("no next list item"),
	prevDoc=_("moves to the previous list item"), prevError=_("no previous list item"))
qn("button", key="b", nextDoc=_("moves to the next button"), nextError=_("no next button"),
	prevDoc=_("moves to the previous button"), prevError=_("no previous button"))
qn("edit", key="e", nextDoc=_("moves to the next edit field"), nextError=_("no next edit field"),
	prevDoc=_("moves to the previous edit field"), prevError=_("no previous edit field"), readUnit=textHandler.UNIT_LINE)
qn("frame", key="m", nextDoc=_("moves to the next frame"), nextError=_("no next frame"),
	prevDoc=_("moves to the previous frame"), prevError=_("no previous frame"), readUnit=textHandler.UNIT_LINE)
qn("separator", key="s", nextDoc=_("moves to the next separator"), nextError=_("no next separator"),
	prevDoc=_("moves to the previous separator"), prevError=_("no previous separator"))
qn("radioButton", key="r", nextDoc=_("moves to the next radio button"), nextError=_("no next radio button"),
	prevDoc=_("moves to the previous radio button"), prevError=_("no previous radio button"))
qn("comboBox", key="c", nextDoc=_("moves to the next combo box"), nextError=_("no next combo box"),
	prevDoc=_("moves to the previous combo box"), prevError=_("no previous combo box"))
qn("checkBox", key="x", nextDoc=_("moves to the next check box"), nextError=_("no next check box"),
	prevDoc=_("moves to the previous check box"), prevError=_("no previous check box"))
qn("graphic", key="g", nextDoc=_("moves to the next graphic"), nextError=_("no next graphic"),
	prevDoc=_("moves to the previous graphic"), prevError=_("no previous graphic"))
qn("blockQuote", key="q", nextDoc=_("moves to the next block quote"), nextError=_("no next block quote"),
	prevDoc=_("moves to the previous block quote"), prevError=_("no previous block quote"))
del qn
