import ctypes
import os
import collections
import XMLFormatting
from keyUtils import sendKey
import scriptHandler
from scriptHandler import isScriptWaiting
import speech
import NVDAObjects
import api
import sayAllHandler
import controlTypes
import textInfos.offsets
import config
import cursorManager
import gui
import wx
import virtualBufferHandler
import eventHandler
import braille
import queueHandler
from logHandler import log
import ui
import aria

VBufStorage_findDirection_forward=0
VBufStorage_findDirection_back=1
VBufStorage_findDirection_up=2

def VBufStorage_findMatch_word(word):
	return "~w%s" % word

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

class VirtualBufferTextInfo(textInfos.offsets.OffsetsTextInfo):

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
		docHandle,ID=self.obj.getIdentifierFromNVDAObject(obj)
		node = VBufClient.VBufRemote_getControlFieldNodeWithIdentifier(self.obj.VBufHandle, docHandle, ID)
		if not node:
			raise LookupError
		start = ctypes.c_int()
		end = ctypes.c_int()
		VBufClient.VBufRemote_getFieldNodeOffsets(self.obj.VBufHandle, node, ctypes.byref(start), ctypes.byref(end))
		return start.value, end.value

	def __init__(self,obj,position):
		self.obj=obj
		if isinstance(position,NVDAObjects.NVDAObject):
			start,end=self._getOffsetsFromNVDAObject(position)
			position=textInfos.offsets.Offsets(start,end)
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
			if isinstance(commandList[index],textInfos.FieldCommand) and isinstance(commandList[index].field,textInfos.ControlField):
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
		tableLayout=attrs.get('table-layout')
		if tableLayout:
			attrs['table-layout']=tableLayout=="1"
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

	def copyToClipboard(self):
		# Blocks should start on a new line, but they don't necessarily have an end of line indicator.
		# Therefore, get the text in block (paragraph) chunks and join the chunks with \r\n.
		blocks = (block.strip("\r\n") for block in self.getTextInChunks(textInfos.UNIT_PARAGRAPH))
		return api.copyToClip("\r\n".join(blocks))

	def getControlFieldSpeech(self, attrs, ancestorAttrs, fieldType, formatConfig=None, extraDetail=False, reason=None):
		textList = []
		landmark = attrs.get("landmark")
		if fieldType == "start_addedToControlFieldStack" and landmark:
			textList.append(_("%s landmark") % aria.landmarkRoles[landmark])
		textList.append(super(VirtualBufferTextInfo, self).getControlFieldSpeech(attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason))
		return " ".join(textList)

class ElementsListDialog(wx.Dialog):
	ELEMENT_TYPES = (
		("link", _("Lin&ks")),
		("heading", _("&Headings")),
		("landmark", _("Lan&dmarks")),
	)
	Element = collections.namedtuple("Element", ("textInfo", "text", "parent"))

	def __init__(self, vbuf):
		self.vbuf = vbuf
		super(ElementsListDialog, self).__init__(gui.mainFrame, wx.ID_ANY, _("Elements List"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		child = wx.RadioBox(self, wx.ID_ANY, label=_("Type:"), choices=tuple(et[1] for et in self.ELEMENT_TYPES))
		child.Bind(wx.EVT_RADIOBOX, self.onElementTypeChange)
		mainSizer.Add(child)

		self.tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_SINGLE)
		# The enter key should be propagated to the dialog and thus activate the default button,
		# but this is broken (wx ticket #3725).
		# Therefore, we must catch the enter key here.
		self.tree.Bind(wx.EVT_CHAR, self.onTreeChar)
		self.treeRoot = self.tree.AddRoot("root")
		mainSizer.Add(self.tree)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.activateButton = wx.Button(self, wx.ID_ANY, _("&Activate"))
		self.activateButton.Bind(wx.EVT_BUTTON, lambda evt: self.onAction(True))
		sizer.Add(self.activateButton)
		self.moveButton = wx.Button(self, wx.ID_ANY, _("&Move to"))
		self.moveButton.Bind(wx.EVT_BUTTON, lambda evt: self.onAction(False))
		sizer.Add(self.moveButton)
		sizer.Add(wx.Button(self, wx.ID_CANCEL))
		mainSizer.Add(sizer)

		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

		self.tree.SetFocus()
		self.initElementType(self.ELEMENT_TYPES[0][0])

	def onElementTypeChange(self, evt):
		# We need to make sure this gets executed after the focus event.
		# Otherwise, NVDA doesn't seem to get the event.
		queueHandler.queueFunction(queueHandler.eventQueue, self.initElementType, self.ELEMENT_TYPES[evt.GetInt()][0])

	def initElementType(self, elType):
		if elType == "link":
			# Links can be activated.
			self.activateButton.Enable()
			self.SetAffirmativeId(self.activateButton.GetId())
		else:
			# No other element type can be activated.
			self.activateButton.Disable()
			self.SetAffirmativeId(self.moveButton.GetId())

		# Gather the elements of this type.
		self._elements = []
		self._initialElement = None

		caret = self.vbuf.selection
		caret.expand("character")

		parentElements = []
		for node, start, end in self.vbuf._iterNodesByType(elType):
			elInfo = self.vbuf.makeTextInfo(textInfos.offsets.Offsets(start, end))

			# Find the parent element, if any.
			for parent in reversed(parentElements):
				if self.isChildElement(elType, parent.textInfo, elInfo):
					break
				else:
					# We're not a child of this parent, so this parent has no more children and can be removed from the stack.
					parentElements.pop()
			else:
				# No parent found, so we're at the root.
				# Note that parentElements will be empty at this point, as all parents are no longer relevant and have thus been removed from the stack.
				parent = None

			element = self.Element(elInfo, self.getElementText(elInfo, elType), parent)
			self._elements.append(element)

			if not self._initialElement and elInfo.compareEndPoints(caret, "startToStart") > 0:
				# The element immediately preceding or overlapping the caret should be the initially selected element.
				# This element immediately follows the caret, so we want the previous element.
				try:
					self._initialElement = self._elements[-2]
				except IndexError:
					# No previous element.
					pass

			# This could be the parent of a subsequent element, so add it to the parents stack.
			parentElements.append(element)

		# Start with no filtering.
		self._filterText = ""
		self.updateFilter(newElementType=True)

	def updateFilter(self, newElementType=False):
		# If this is a new element type, use the element nearest the cursor.
		# Otherwise, use the currently selected element.
		defaultElement = self._initialElement if newElementType else self.tree.GetItemPyData(self.tree.GetSelection())
		# Clear the tree.
		self.tree.DeleteChildren(self.treeRoot)

		# Populate the tree with elements matching the filter text.
		elementsToTreeItems = {}
		item = None
		defaultItem = None
		matched = False
		for element in self._elements:
			if self._filterText not in element.text.lower():
				item = None
				continue
			matched = True
			parent = element.parent
			if parent:
				parent = elementsToTreeItems.get(parent)
			item = self.tree.AppendItem(parent or self.treeRoot, element.text)
			self.tree.SetItemPyData(item, element)
			elementsToTreeItems[element] = item
			if element == defaultElement:
				defaultItem = item

		self.tree.ExpandAll()

		if self._filterText and not matched:
			wx.Bell()
			return

		# If there's no default item, use the first item in the tree.
		self.tree.SelectItem(defaultItem or self.tree.GetFirstChild(self.treeRoot)[0])

	def _getControlFieldAttrib(self, info, attrib):
		info = info.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		for field in reversed(info.getTextWithFields()):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			val = field.field.get(attrib)
			if val:
				return val
		return None

	def getElementText(self, elInfo, elType):
		if elType == "landmark":
			landmark = self._getControlFieldAttrib(elInfo, "landmark")
			if landmark:
				return aria.landmarkRoles[landmark]

		else:
			return elInfo.text.strip()

	def isChildElement(self, elType, parent, child):
		if parent.isOverlapping(child):
			return True

		elif elType == "heading":
			try:
				if int(self._getControlFieldAttrib(child, "level")) > int(self._getControlFieldAttrib(parent, "level")):
					return True
			except (ValueError, TypeError):
				return False

		return False

	def onTreeChar(self, evt):
		key = evt.KeyCode

		if key == wx.WXK_RETURN:
			# Activate the current default button.
			evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_ANY)
			self.FindWindowById(self.GetAffirmativeId()).ProcessEvent(evt)

		elif key == wx.WXK_BACK:
			# Cancel filtering.
			if self._filterText:
				self._filterText = ""
				self.updateFilter()
			# If we don't pass this event on, we miss a subsequent character. No idea why, but it doesn't seem to have any effect anyway.
			evt.Skip()

		elif key >= wx.WXK_START:
			# Non-printable character.
			evt.Skip()

		else:
			# Filter the list.
			char = unichr(evt.UnicodeKey)
			self._filterText += char.lower()
			self.updateFilter()

	def onAction(self, activate):
		self.Close()

		item = self.tree.GetSelection()
		element = self.tree.GetItemPyData(item).textInfo
		newCaret = element.copy()
		newCaret.collapse()
		self.vbuf.selection = newCaret

		if activate:
			self.vbuf._activatePosition(element)
		else:
			wx.CallLater(100, self._reportElement, element)

		self.Destroy()

	def _reportElement(self, element):
		speech.cancelSpeech()
		speech.speakTextInfo(element,reason=speech.REASON_FOCUS)

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
		info=self.makeTextInfo(textInfos.POSITION_CARET)
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
		return controlTypes.STATE_FOCUSABLE in obj.states

	def script_activatePosition(self,keyPress):
		if self.VBufHandle is None:
			return sendKey(keyPress)
		info=self.makeTextInfo(textInfos.POSITION_CARET)
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
	script_refreshBuffer.__doc__ = _("Refreshes the virtual buffer content")

	def script_toggleScreenLayout(self,keyPress):
		config.conf["virtualBuffers"]["useScreenLayout"]=not config.conf["virtualBuffers"]["useScreenLayout"]
		onOff=_("on") if config.conf["virtualBuffers"]["useScreenLayout"] else _("off")
		speech.speakMessage(_("use screen layout %s")%onOff)
	script_toggleScreenLayout.__doc__ = _("Toggles on and off if the screen layout is preserved while rendering the virtual buffer content")

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _iterNodesByType(self,nodeType,direction="next",offset=-1):
		if nodeType == "notLinkBlock":
			return self._iterNotLinkBlock(direction=direction, offset=offset)
		attribs=self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			return iter(())
		return self._iterNodesByAttribs(attribs, direction, offset)

	def _iterNodesByAttribs(self, attribs, direction="next", offset=-1):
		attribs=dictToMultiValueAttribsString(attribs)
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
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		startOffset=info._startOffset
		endOffset=info._endOffset
		try:
			node, startOffset, endOffset = next(self._iterNodesByType(nodeType, direction, startOffset))
		except StopIteration:
			speech.speakMessage(errorMessage)
			return
		info = self.makeTextInfo(textInfos.offsets.Offsets(startOffset, endOffset))
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

	def script_elementsList(self,keyPress):
		if self.VBufHandle is None:
			return
		# We need this to be a modal dialog, but it mustn't block this script.
		def run():
			gui.mainFrame.prePopup()
			ElementsListDialog(self).ShowModal()
			gui.mainFrame.postPopup()
		wx.CallAfter(run)
	script_elementsList.__doc__ = _("Presents a list of links, headings or landmarks")

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
			return role == controlTypes.ROLE_EDITABLETEXT or (role == controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)
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
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(info.UNIT_CONTROLFIELD)
		if keyPress[1] in ("extendedleft", "extendedup", "extendedprior"):
			info.collapse()
		else:
			info.collapse(end=True)
			info.move(textInfos.UNIT_CHARACTER, -1)
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
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't yield the desired results with collapsed ranges.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
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
		newInfo = self.makeTextInfo(textInfos.offsets.Offsets(newStart, newEnd))
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
			sendKey(keyPress)

	def script_shiftTab(self, keyPress):
		if not self._tabOverride("previous"):
			sendKey(keyPress)

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
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
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
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		if not scrollInfo.isOverlapping(caretInfo):
			speech.speakTextInfo(scrollInfo,reason=speech.REASON_CARET)
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
		startPos = startPos._startOffset if startPos else -1
		results = self._iterNodesByAttribs(attrs, offset=startPos, direction=direction)
		if not startPos and not row and not column and direction == "next":
			# The first match will be the table itself, so skip it.
			next(results)
		for node, start, end in results:
			yield self.makeTextInfo(textInfos.offsets.Offsets(start, end))

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
			ui.message(_("Not in a table cell"))
			return

		try:
			info = self._getNearestTableCell(tableID, self.selection, origRow, origCol, origRowSpan, origColSpan, movement, axis)
		except LookupError:
			ui.message(_("edge of table"))
			# Retrieve the cell on which we started.
			info = next(self._iterTableCells(tableID, row=origRow, column=origCol))

		speech.speakTextInfo(info,formatConfig=formatConfig,reason=speech.REASON_CARET)
		info.collapse()
		self.selection = info

	def script_nextRow(self, keyPress):
		self._tableMovementScriptHelper(axis="row", movement="next")
	script_nextRow.__doc__ = _("moves to the next table row")

	def script_previousRow(self, keyPress):
		self._tableMovementScriptHelper(axis="row", movement="previous")
	script_previousRow.__doc__ = _("moves to the previous table row")

	def script_nextColumn(self, keyPress):
		self._tableMovementScriptHelper(axis="column", movement="next")
	script_nextColumn.__doc__ = _("moves to the next table column")

	def script_previousColumn(self, keyPress):
		self._tableMovementScriptHelper(axis="column", movement="previous")
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
				return False
			obj = obj.parent
		return True

	NOT_LINK_BLOCK_MIN_LEN = 30
	def _iterNotLinkBlock(self, direction="next", offset=-1):
		links = self._iterNodesByType("link", direction=direction, offset=offset)
		# We want to compare each link against the next link.
		link1node, link1start, link1end = next(links)
		while True:
			link2node, link2start, link2end = next(links)
			# If the distance between the links is small, this is probably just a piece of non-link text within a block of links; e.g. an inactive link of a nav bar.
			if direction == "next" and link2start - link1end > self.NOT_LINK_BLOCK_MIN_LEN:
				yield 0, link1end, link2start
			# If we're moving backwards, the order of the links in the document will be reversed.
			elif direction == "previous" and link1start - link2end > self.NOT_LINK_BLOCK_MIN_LEN:
				yield 0, link2end, link1start
			link1node, link1start, link1end = link2node, link2start, link2end

[VirtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in (
	("Return","activatePosition"),
	("Space","activatePosition"),
	("NVDA+f5","refreshBuffer"),
	("NVDA+v","toggleScreenLayout"),
	("NVDA+f7","elementsList"),
	("escape","disablePassThrough"),
	("alt+extendedUp","collapseOrExpandControl"),
	("alt+extendedDown","collapseOrExpandControl"),
	("tab", "tab"),
	("shift+tab", "shiftTab"),
	("control+alt+extendedDown", "nextRow"),
	("control+alt+extendedUp", "previousRow"),
	("control+alt+extendedRight", "nextColumn"),
	("control+alt+extendedLeft", "previousColumn"),
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
	prevDoc=_("moves to the previous table"), prevError=_("no previous table"), readUnit=textInfos.UNIT_LINE)
qn("link", key="k", nextDoc=_("moves to the next link"), nextError=_("no next link"),
	prevDoc=_("moves to the previous link"), prevError=_("no previous link"))
qn("visitedLink", key="v", nextDoc=_("moves to the next visited link"), nextError=_("no next visited link"),
	prevDoc=_("moves to the previous visited link"), prevError=_("no previous visited link"))
qn("unvisitedLink", key="u", nextDoc=_("moves to the next unvisited link"), nextError=_("no next unvisited link"),
	prevDoc=_("moves to the previous unvisited link"), prevError=_("no previous unvisited link"))
qn("formField", key="f", nextDoc=_("moves to the next form field"), nextError=_("no next form field"),
	prevDoc=_("moves to the previous form field"), prevError=_("no previous form field"), readUnit=textInfos.UNIT_LINE)
qn("list", key="l", nextDoc=_("moves to the next list"), nextError=_("no next list"),
	prevDoc=_("moves to the previous list"), prevError=_("no previous list"), readUnit=textInfos.UNIT_LINE)
qn("listItem", key="i", nextDoc=_("moves to the next list item"), nextError=_("no next list item"),
	prevDoc=_("moves to the previous list item"), prevError=_("no previous list item"))
qn("button", key="b", nextDoc=_("moves to the next button"), nextError=_("no next button"),
	prevDoc=_("moves to the previous button"), prevError=_("no previous button"))
qn("edit", key="e", nextDoc=_("moves to the next edit field"), nextError=_("no next edit field"),
	prevDoc=_("moves to the previous edit field"), prevError=_("no previous edit field"), readUnit=textInfos.UNIT_LINE)
qn("frame", key="m", nextDoc=_("moves to the next frame"), nextError=_("no next frame"),
	prevDoc=_("moves to the previous frame"), prevError=_("no previous frame"), readUnit=textInfos.UNIT_LINE)
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
qn("notLinkBlock", key="n", nextDoc=_("skips forward past a block of links"), nextError=_("no more text after a block of links"),
	prevDoc=_("skips backward past a block of links"), prevError=_("no more text before a block of links"), readUnit=textInfos.UNIT_LINE)
qn("landmark", key="d", nextDoc=_("moves to the next landmark"), nextError=_("no next landmark"),
	prevDoc=_("moves to the previous landmark"), prevError=_("no previous landmark"), readUnit=textInfos.UNIT_LINE)
del qn
